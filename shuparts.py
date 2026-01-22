#!/usr/bin/python3

import os
import sys
import random
import zipfile
import xml.etree.ElementTree as ET

def shuf(parts):
    print("Selecting from parts:", ", ".join(parts))
    print("<hit enter to pick the next part, or ctrl-C to exit early>")

    maxlen = max(*map(len, parts))

    random.shuffle(parts)
    try:
        last_i = len(parts) - 1
        for i, part in enumerate(parts):
            (print if i == last_i else input)(f"-->  {part:{maxlen}}  <--")
    except KeyboardInterrupt:
        print("\n<exiting early due to ctrl-C>")

def extract_parts_from_mscz(fname):
    """Parse all rehearsal marks from the given mscz file.
    """
    with zipfile.ZipFile(fname, 'r') as mscz:
        # Read the contents of the internal mscx file as bytes
        mscx_name = os.path.basename(fname[:-1] + "x")
        mscx_str = mscz.read(mscx_name).decode('utf-8')

    root = ET.fromstring(mscx_str)
    parts = []
    for mark in root.iter('RehearsalMark'):
        part_element = mark.find('text')
        parts.append(part_element.text.strip())

    return parts

def main():
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} partname ...")
        return(1)

    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if os.path.exists(arg):
            parts = extract_parts_from_mscz(arg)
        else:
            parts = arg.split()

    else:
        parts = sys.argv[1:]

    shuf(parts)

if __name__ == "__main__":
    sys.exit(main())
