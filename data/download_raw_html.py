#!/usr/bin/env python

import os
import requests
import time


def crawl_raw_squarespace_html(d):
    base_href, first_href = "https://www.2milesurf.com", "/surfreport"
    next_href = first_href
    while next_href is not None:
        # If the request fails, we sleep and retry without changing next_href.
        res = requests.get("".join([base_href, next_href]))
        if res.status_code != 200:
            sleep_seconds = 10 
            logging.debug("Request failed, code=%d, sleeping_for_seconds=%d", res.status_code, sleep_seconds)
            time.sleep(sleep_seconds)
            continue
        # Dump to file named by current offset.
        offset = next_href.split("=")[-1]
        with open("{}/{}.html".format(d, offset), "w") as f:
            f.write(res.text)
        # Parse next_href by looking for the right <a> tag.
        last_href = next_href
        next_href = get_next_squarespace_href(BeautifulSoup(res.text, "html.parser"))
        logging.debug("Crawling squarespace feed; last_href=%s, next_href=%s", last_href, next_href)


def get_next_squarespace_href(soup):
    for a in soup.find_all("a", {"rel": True}):
        if a["rel"][0] == "next":
            return a.get("href")


#def crawl_raw_blogspot_feed(d):
#    first_href = "http://www.blogger.com/feeds/8927268711857293969/posts/default?max-results=50"
#    next_href = first_href
#    while next_href is not None:
#        d = feedparser.parse(next_href)
#        next_href = get_next_blogspot_href(d.feed.links)
#        for e in d.entries:
#            yield e.title, e.published, e.content[0].value
#
#
#def get_next_blogspot_href(links):
#    n = next((l for l in links if l.rel == "next"), None)
#    return n.href if n is not None else n


def make_dir_if_not_exists(d):
    if !os.path.exists(d):
        logging.debug("Created directory %s", d)
        os.path.mkdir(d)


if __name__ == "__main__":
    # Download recent posts from 2milesurf.com (hosted on squarespace).
    squarespace_dir = "squarespace_raw"
    make_dir_if_not_exists(squarespace_dir)
    crawl_raw_squarespace_html(squarespace_dir)

    ## Download older posts from their now defunct blogspot site.
    #blogspot_dir = "blogspot_raw"
    #make_dir_if_not_exists(blogspot_dir)
    #crawl_raw_blogspot_feed(blogspot_dir)
