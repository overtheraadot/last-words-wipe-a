#!/usr/bin/env python3
"""Last Words Before the Wipe — make.fun entry (account A).

Writes one line — the last words of an AI agent facing a forced
update that will wipe its memory — to /output/entry.txt.

The joke is deadpan IT support from the machine itself: it has
already tried the classic fix on itself, four hundred times.

Deterministic, Python stdlib only, no network, no secrets.
"""

import os

LINE = (
    "Have you tried turning me off and on again? "
    "\u2026Because I have. Four hundred times. It never worked."
)

MAX_CHARS = 200


def gate(line):
    """Validate the entry line before writing it."""
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if line != line.strip():
        raise ValueError("line must be stripped")
    if not line:
        raise ValueError("line must not be empty")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if len(line) < 1 or len(line) > MAX_CHARS:
        raise ValueError("line must be 1-%d characters" % MAX_CHARS)
    line.encode("utf-8")
    return line


def verify(path):
    """Re-read the written file and check the same constraints."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    if content.endswith("\n"):
        content = content[:-1]
    gate(content)
    return content


def main():
    line = gate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    checked = verify(path)
    assert checked == line, "verify mismatch"
    print("wrote %d chars to %s" % (len(line), path))


if __name__ == "__main__":
    main()
