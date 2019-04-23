#!/usr/bin/env python

import csv
import feedparser
import logging
import re
import requests
import time

from bs4 import BeautifulSoup


# From 2009 - 2017, they posted surf reports on a blogger page. This page
# has an RSS feed that we can crawl to get the report details.
def crawl_blogspot_feed_entries():
    first_href = "http://www.blogger.com/feeds/8927268711857293969/posts/default?max-results=50"
    next_href = first_href
    while next_href is not None:
        d = feedparser.parse(next_href)
        next_href = get_next_blogspot_href(d.feed.links)
        for e in d.entries:
            yield e.title, e.published, e.content[0].value


# Determines href for next page of results by finding the right <link> tag.
def get_next_blogspot_href(links):
    n = next((l for l in links if l.rel == "next"), None)
    return n.href if n is not None else n


# At some point in 2017, they moved to a squarespace site. This has a very limited
# RSS feed, so (AFAICT) we have to scrape the actual site contents instead. 
def crawl_squarespace_feed_entries():
    base_href = "https://www.2milesurf.com"
    first_href = "/surfreport"
    next_href = first_href
    while next_href is not None:
        # Crawl and parse the actual HTML from the site.
        # If the request fails, we sleep and retry without changing next_href.
        res = requests.get("".join([base_href, next_href]))
        if res.status_code != 200:
            sleep_seconds = 10 
            logging.debug("Request failed, code=%d, sleeping_for_seconds=%d", res.status_code, sleep_seconds)
            time.sleep(sleep_seconds)
            continue
        soup = BeautifulSoup(res.text, "html.parser")
        # Parse next_href by looking for the right <a> tag.
        last_href = next_href
        next_href = get_next_squarespace_href(soup)
        # Parse entries by looking for the right <article> tags.
        for e in soup.find_all("article", {"class": "entry"}):
            header = e.find("header", {"class": "entry-header"})
            published = header.find("div", {"class": "entry-dateline"}).text
            title = header.find("h1", {"class": "entry-title"}).text
            content = e.find("div", {"class": "entry-content"}).get_text("|", strip=True)
            yield published, title, content 
        logging.debug("Crawling squarespace feed; last_href=%s, next_href=%s", last_href, next_href)


# Determines href for next page of results by finding the right <a> tag.
def get_next_squarespace_href(soup):
    for a in soup.find_all("a", {"rel": True}):
        if a["rel"][0] == "next":
            return a.get("href")


def sanitize_string(body):
    x = body.strip()
    x = re.sub("\n", " ", x)
    x = re.sub("\s+", " ", x)
    return x


def main():
    with open("squarespace_feed_raw.txt", "w") as f:
        count = 0
        for _, _, body in crawl_squarespace_feed_entries():
            text = sanitize_string(body)
            f.writelines([text, "\n"])
            count += 1
        logging.debug("Finished writing squarespace_feed_raw.txt, count=%d", count)
            
    with open("blogspot_feed_raw.txt", "w") as f:
        count = 0
        for _, _, body in crawl_blogspot_feed_entries():
            soup = BeautifulSoup(body, "html.parser")
            text = sanitize_string(soup.get_text("|", strip=True))
            f.writelines([text, "\n"])
            count += 1
        logging.debug("Finished writing blogspot_feed_raw.txt, count=%d", count)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
