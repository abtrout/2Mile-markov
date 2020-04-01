#!/usr/bin/env python

import os
import re

from bs4 import BeautifulSoup
from unicodedata import normalize


def sanitize_string(body):
    x = body.strip()
    x = re.sub("\n", " ", x)
    x = re.sub("\s+", " ", x)
    x = re.sub(" , ", ", ", x)
    return x


def parse_posts_from_page(page_file, out_file):
    soup = BeautifulSoup(open(page_file), "html.parser")
    for e in soup.find_all("article", {"class": "entry"}):
        # Grab text contents from .entry-content <div>s.
        content = e.find("div", {"class": "entry-content"}).get_text(" ")
        content = sanitize_string(content)
        # Fix up CHANNEL/PATCH headers.
        content = content.replace("CHANNEL :", "CHANNEL:")
        content = content.replace("PATCH :", "PATCH:")
        # Trim beginning/end of post, hopefully only getting the report.
        start_offset = min(
                max(0, content.find("PATCH:")),
                max(0, content.find("CHANNEL:")))
        end_offset = check_for_end_filler_text(content)
        # Bon voyage, content.
        yield content[start_offset:end_offset]


def check_for_end_filler_text(content):
    known_filler = [
        "PACK IT IN! PACK IT OUT!",
        "RENTAL INVENTORY SALE!",
        "PACK IT IN. PACK IT OUT.",
        "Join us Thanksgiving weekend for",
        "Don't forget - our Storewide",
    ]
    return min([find_end_offset(content, kf) for kf in known_filler])


def find_end_offset(content, kf):
    offset = content.find(kf)
    if offset < 0:
        return len(content)
    return offset


if __name__ == "__main__":
    raw_dir = "squarespace_raw"
    with os.scandir(raw_dir) as it, open("squarespace_posts.txt", "w") as out_file:
        for entry in it:
            if entry.name.endswith(".html") and entry.is_file():
                for post in parse_posts_from_page(entry.path, out_file):
                    out_file.write(post + "\n")
