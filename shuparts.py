#!/usr/bin/python3

import sys
import random

def shuf(parts):
    random.shuffle(parts)
    print(parts[0])
    for part in parts[1:]:
        input("<hit enter for next part>")
        print(part)

def main():
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} partname ...")
        return(1)

    elif len(sys.argv) == 2:
        parts = sys.argv[1].split()

    else:
        parts = sys.argv[1:]

    shuf(parts)

if __name__ == "__main__":
    sys.exit(main())
