#!/usr/bin/python3

import os
import sys
import random
import zipfile
import xml.etree.ElementTree as ET

def shuf(parts):
    print("Selecting from parts:", ", ".join(parts))
    print("<hit enter to pick the next part, or ctrl-C to exit early>")

    maxlen = max(map(len, parts))

    random.shuffle(parts)
    try:
        last_i = len(parts) - 1
        for i, part in enumerate(parts):
            (print if i == last_i else input)(f"-->  {part:{maxlen}}  <--")
        print("Done!")
    except KeyboardInterrupt:
        print("\n<exiting early due to ctrl-C>")

def extract_parts_from_file(fname):
    if fname.endswith('.mscz'):
        return extract_parts_from_mscz(fname)
    elif fname.endswith('.mscx'):
        return extract_parts_from_mscx(fname)
    elif fname.endswith('.mxl'):
        return extract_parts_from_mxl(fname)
    elif fname.endswith('.xml'):
        return extract_parts_from_xml(fname)
    else:
        return [fname]

def extract_parts_from_mscz(fname):
    """Parse all rehearsal marks from the given mscz file.
    """
    with zipfile.ZipFile(fname, 'r') as mscz:
        # Read the contents of the internal mscx file as bytes
        mscx_name = os.path.basename(fname[:-1] + "x")
        mscx_str = mscz.read(mscx_name).decode('utf-8')

    return extract_parts_from_mscx_str(mscx_str)

def extract_parts_from_mscx(fname):
    """Parse all rehearsal marks from the given mscx file.
    """
    with open(fname, 'r') as mscx:
        # Read the contents of the internal mscx file
        mscx_str = mscx.read()

    return extract_parts_from_mscx_str(mscx_str)

def extract_parts_from_mscx_str(mscx_str):
    root = ET.fromstring(mscx_str)
    parts = []
    for mark in root.iter('RehearsalMark'):
        part_element = mark.find('text')
        parts.append(part_element.text.strip())

    return parts

def extract_parts_from_mxl(fname):
    """Parse all rehearsal marks from the given compressed MusicXML mxl file.
    """
    with zipfile.ZipFile(fname, 'r') as mxl:
        # Read the contents of the internal MusicXML file as bytes
        xml_name = 'score.xml'
        xml_str = mxl.read(xml_name).decode('utf-8')

    return extract_parts_from_xml_str(xml_str)

def extract_parts_from_xml(fname):
    """Parse all rehearsal marks from the given uncompressed MusicXML .xml file.
    """
    with open(fname, 'r') as xml:
        # Read the contents of the internal xml file
        xml_str = xml.read()

    return extract_parts_from_xml_str(xml_str)

def extract_parts_from_xml_str(xml_str):
    root = ET.fromstring(xml_str)
    parts = []
    for mark in root.iter('rehearsal'):
        parts.append(mark.text.strip())

    return parts


def main():
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} partname ...")
        return(1)

    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if os.path.exists(arg):
            parts = extract_parts_from_file(arg)
        else:
            parts = arg.split()

    else:
        parts = sys.argv[1:]

    shuf(parts)

if __name__ == "__main__":
    sys.exit(main())
