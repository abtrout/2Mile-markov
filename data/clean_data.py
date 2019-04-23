#!/usr/bin/env python

import csv
import re

from unicodedata import normalize


def main(infile, outfile):
    for line in infile:
        saved_parts = []
        content = normalize("NFKD", line)
        content = re.sub(r"\s+", " ", content)
        content_parts = iter(content.split("|"))
        for part in content_parts:
            # Ignore shop announcements and news.
            if part.startswith("WE WILL BE CLOSED"):
                continue
            elif part.startswith("NEWS"):
                break # ignore everything left
            elif part.startswith("PACK IT IN"):
                break
            if "Tamarindo" in part:
                break
            # Ignore inspiration quotes.
            elif part.startswith("Inspirational Quote"):
                _ = next(content_parts)  # skip the actual quote too!
                continue
            # Keep everything else.
            else:
                part = re.sub(r"^:\s+", "", part)
                part = re.sub(r"\s*:$", "", part)
                part = re.sub(r"^(?i)CHANNEL:?$", "CHANNEL:", part) 
                part = re.sub(r"^(?i)PATCH:?$", "PATCH:", part)
                saved_parts.append(part)
        # Save the new/clean line to outfile.
        new_line = " ".join(saved_parts)
        outfile.writelines([new_line, "\n"])

if __name__ == "__main__":
    input_file = "squarespace_feed_raw.txt"
    output_file = "out.txt"
    with open(input_file, "r") as f:
        with open(output_file, "w") as g:
            main(f, g)
