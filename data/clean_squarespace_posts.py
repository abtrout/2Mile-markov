#!/usr/bin/env python

import os
import re
import sys

from bs4 import BeautifulSoup
from unicodedata import normalize


def parse_posts_from_page(page_file, out_file, known_filler):
    soup = BeautifulSoup(open(page_file), "html.parser")
    num_skipped = 0
    for e in soup.find_all("article", {"class": "entry"}):
        # Grab text contents from .entry-content <div>s.
        content = e.find("div", {"class": "entry-content"}).get_text("")
        # Sanitize and fix up CHANNEL/PATCH headers.
        content = sanitize_string(content)
        content = content.replace("CHANNEL :", "CHANNEL:")
        content = content.replace("PATCH :", "PATCH:")
        # Trim beginning/end of post, hopefully only getting the report.
        start_offset = min(
                max(0, content.find("PATCH:")),
                max(0, content.find("CHANNEL:")))
        content = content[start_offset:]
        end_offset = find_first_end_offset(content, known_filler)
        content = content[:end_offset].strip()
        # FIXMEUP.
        if content.startswith("CHANNEL:"):
            offset = content.find("PATCH:")
            channel = content[:offset]
            patch = content[offset:]
            yield channel, patch
        elif content.startswith("PATCH:"):
            offset = content.find("CHANNEL:")
            channel = content[:offset]
            patch = content[offset:]
            yield channel, patch
        else:
            num_skipped += 1
    print(f"Skipped posts from page: page={page_file}, num_skipped={num_skipped}")


def find_first_end_offset(content, known_filler):
    return min([find_end_offset(content, kf) for kf in known_filler])


def find_end_offset(content, kf):
    offset = content.find(kf)
    if offset < 0:
        return len(content)
    return offset


def sanitize_string(body):
    x = body.strip()
    x = re.sub("\n", " ", x)
    x = re.sub("\s+", " ", x)
    x = re.sub(" , ", ", ", x)
    return x


if __name__ == "__main__":
    # Fixed set of common surf report endings.
    known_filler = [
        "PACK IT IN",
        "RENTAL INVENTORY",
        "2 Mile Surf Shop Rental Gear",
        "NOTE:",
        "LIMITED SEATING",
        "The second annual Mill Valley Surf Film",
        "Massive Surfboard and SUP sale",
        "Just a reminder to pack your",
        "We're cleaning house",
        "Customer Appreciation Sale",
        "Thank You! Our sincere thanks for",
        "Join us Thanksgiving",
        "Adult Surf Camp will be offered",
        "Important Note from the Bolinas Fishing Community",
        "Intermediate Surf Clinic",
        "This Saturday - 8/17/2013",
        "Strewnfield by Thomas Campbell",
        "This Saturday - 6/15/2013",
        "We still have a few open spots",
        "The Mill Valley Surf Film",
        "This week! All the details here",
        "The Kahuna Kupuna is the",
        "John Doe and Rambin' Jack Elliott",
    ]
    # Parse each HTML post separately and save text to another file.
    raw_dir = "squarespace_raw"
    with open("squarespace_posts.txt", "w") as out_file:
        for entry in os.scandir(raw_dir):
            if entry.name.endswith(".html") and entry.is_file():
                for channel, patch in parse_posts_from_page(entry.path, out_file, known_filler):
                    out_file.write(channel + "\n")
                    out_file.write(patch + "\n")
