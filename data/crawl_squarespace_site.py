#!/usr/bin/env python

import os
import logging
import requests
import time

from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"


def crawl_raw_squarespace_html(out_dir):
    base_href, first_href = "https://www.2milesurf.com", "/surfreport"
    next_href = first_href
    while next_href is not None:
        # If the request fails, we sleep and retry without changing next_href.
        res = requests.get("".join([base_href, next_href]), headers={"user-agent": USER_AGENT})
        if res.status_code != 200:
            sleep_seconds = 10 
            logging.debug("Request failed, code=%d, sleeping_for_seconds=%d", res.status_code, sleep_seconds)
            time.sleep(sleep_seconds)
            continue
        # Dump HTML to file named by current offset.
        offset = next_href.split("=")[-1]
        with open(f"{out_dir}/{offset}.html", "w") as f:
            f.write(res.text)
        # Parse next_href by looking for the right <a> tag.
        last_href = next_href
        next_href = get_next_squarespace_href(BeautifulSoup(res.text, "html.parser"))
        logging.debug("Crawling squarespace feed; last_href=%s, next_href=%s", last_href, next_href)


def get_next_squarespace_href(soup):
    for a in soup.find_all("a", {"rel": True}):
        if a["rel"][0] == "next":
            return a.get("href")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    out_dir = "squarespace_raw"
    if not os.path.exists(out_dir):
        logging.debug(f"Created directory {out_dir}")
        os.mkdir(out_dir)
    crawl_raw_squarespace_html(out_dir)
