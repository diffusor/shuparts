#!/usr/bin/python3

import os
import sys
import random
import zipfile
from dataclasses import dataclass, field
import xml.etree.ElementTree as ET

def shuf(partspec):
    print("Available parts:\n")
    parts = []
    if partspec and isinstance(partspec[0], Section):
        for i, section in enumerate(partspec):
            print(f"{i+1}: {section.title} ({section.tempo})\n  {' '.join(section.parts)}\n")
            parts.extend(f"{i+1}:{part}" for part in section.parts)

        section_num = input("\nEnter section # to choose from, or hit enter to practice all: ")
        if section_num:
            i = int(section_num)
            parts = list(partspec[i-1])

    else:
        parts.extend(partspec)
        print(" ", " ".join(parts))

    print("Selecting from parts:\n ", " ".join(parts))
    print("\n<hit enter to pick the next part, or ctrl-C to exit early>")

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

    returns a list of sections, each section having a list of parts.
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

@dataclass
class Section:
    title: str = ""
    tempo: str = ""
    parts: [str] = field(default_factory=list)

replacements = {
    'metNoteQuarterUp': '♩',
}
def alltext(elt):
    def filter(e):
        return replacements.get(e, e).replace('\n', ' / ')
    return ''.join(filter(e) for e in elt.itertext()).strip()

def extract_parts_from_mscx_str(mscx_str):
    root = ET.fromstring(mscx_str)
    section = Section()
    sections = [section] # list of Section instances
    description = ""
    desc_uses = {}
    desc_subpart = 0

    # only scan for marks in the topmost staff
    staff1 = root.find(".//Score/Staff[@id='1']")
    for child in staff1:
        if child.tag == 'VBox':
            # use the last title box only - any prior title is overridden
            for title_elt in child.findall("Text[style='title']/text"):
                section.title = alltext(title_elt)

        if child.tag == 'Measure':
            measure = child
            # Find part description to append to each part until the next section
            for staff_text in measure.iter('StaffText'):
                text = alltext(staff_text.find('text'))
                if text.startswith('['):
                    description = text.replace(" ", "-")
                    desc_uses.setdefault(description, 0)
                    desc_uses[description] += 1
                    desc_subpart = 0

            if not section.tempo:
                for tempo in measure.iter('Tempo'):
                    if text := tempo.find('text'):
                        section.tempo = alltext(text)

            for mark in measure.iter('RehearsalMark'):
                part = alltext(mark.find('text'))
                if description:
                    part = f"{part}{description}"
                    desc_usecount = desc_uses[description]
                    if desc_usecount > 1:
                        part = f"{part}{desc_usecount}"

                    desc_subpart += 1
                    if desc_subpart > 1:
                        part = f"{part}.{desc_subpart}"
                section.parts.append(part)

            for layout_break in measure.iterfind("LayoutBreak[subtype='section']"):
                section = Section()
                sections.append(section)
                description = ""
                desc_subpart = 0
                break

    return sections

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

def showhelp():
    print(f"""Usage: {sys.argv[0]} partname ...

  This is a flashcard-like tool for testing your memorization.

  Given a list of part names, shuparts randomly shuffles them and prints them
  one at a time, waiting for the user to hit enter between each.

  Hit ctrl-C to exit early.  Otherwise, shuparts exits after each part has
  been printed, like going through one pass of a deck of flashcards.

Single-string support:

  If only one argument is passed to shuparts, it will be split at spaces.
  This makes it easy to copy-paste a space-separated list of parts from
  elsewhere or from shuparts' own output.

MuseScore Studio support:

  If only one argument is given and it ends it .mscz or .mscx, it's
  interpreted as a MuseScore file to parse.  The expected format is as follows:

  * The contents of each rehearsal mark is used as the list of parts

  * Section breaks are used to split up music files containing multiple pieces
    of music.  Each section is presented as a separate group of parts to
    practice.  When shuparts starts, it will query the user to select a section
    if there are more than one.

  * Staff text is used to provide descriptive names to each part.

Music layout hints:

  * Select a note in the top staff and use ctrl-M in MuseScore Studio to
    insert a new rehearsal mark.

  * Use section breaks to split up a single score into multiple sections.
    This allows reusing the same rehearsal marks without mixing up the
    list of parts.

  * Add "staff text" on the top staff to provide part descriptions.
    The staff text must be enclosed in [square brackets].
    Note: If a measure contains both a rehearsal mark and a part description,
    shuparts assumes the part description applies to that part, regardless of
    which notes each is actually attached to within the measure.

  * Only add rehearsal marks and [] staff text to the topmost staff -
    otherwise the marks may get jumbled up with the descriptive text
    and the section parsing.
""")

    # (This is because MuseScore stores music as lists of staffs, where each
    # staff contains a list of measures.  Section breaks are only stored in the
    # measures in the first staff.  To support putting rehearsal marks and
    # descriptions on separate staves, shuparts would need to re-zip the music
    # into a list of measures units at the top level, where each measure unit
    # contains multiple staffs, each with it's own measure.)

    # TODO - find a way to name the sections.

def main():
    if len(sys.argv) == 1 or sys.argv[1] in "-h --help /?".split():
        showhelp()
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
