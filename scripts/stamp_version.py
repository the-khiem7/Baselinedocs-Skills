"""Write one release version into every skill's SKILL.md frontmatter.

    uv run scripts/stamp_version.py v1.2.3

Replaces an existing top-level `version:` line or inserts one as the last
frontmatter line. Nothing else in the file is touched, and bytes are read and
written as-is so line endings survive. Running it twice with the same version
changes nothing.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"\d+\.\d+\.\d+")
FRONTMATTER = re.compile(r"\A(---\r?\n)(.*?)(\r?\n---\r?\n)", re.DOTALL)
VERSION_LINE = re.compile(r"^version:.*$", re.MULTILINE)


def parse_version(raw):
    version = raw[1:] if raw.startswith("v") else raw
    if not SEMVER.fullmatch(version):
        raise ValueError(f"{raw!r} is not vMAJOR.MINOR.PATCH")
    return version


def stamp_text(text, version):
    match = FRONTMATTER.match(text)
    if match is None:
        raise ValueError("no frontmatter block")
    opening, block, closing = match.groups()
    eol = "\r\n" if opening.endswith("\r\n") else "\n"
    line = f'version: "{version}"'
    if VERSION_LINE.search(block):
        block = VERSION_LINE.sub(lambda _: line, block, count=1)
    else:
        block = f"{block}{eol}{line}"
    return opening + block + closing + text[match.end():]


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    version = parse_version(argv[1])
    changed = 0
    for path in sorted(ROOT.glob("baselinedocs-*/SKILL.md")):
        before = path.read_bytes().decode("utf-8")
        after = stamp_text(before, version)
        if after != before:
            path.write_bytes(after.encode("utf-8"))
            changed += 1
    print(f"version {version}: {changed} SKILL.md file(s) changed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
