import datetime
import re

import pytest

from helpers import ROOT, read_text, rel, repo_files_matching, split_frontmatter

# This repository's own baseline packs. They do not ship, so nothing here guards
# an installed skill; it keeps the decision log honest, because an identifier that
# resolves to the wrong entry fails silently and a stale index row asserts a
# status nobody re-read.
BASELINE = ROOT / "docs" / "baseline"
PACK_FILES = [
    path for path in repo_files_matching(".md") if BASELINE in path.parents
]
HALLUCINATION_FILES = [path for path in PACK_FILES if path.name.endswith(".hallucination.md")]
# Documents that cite a pack identifier without being part of a pack.
CITING_FILES = PACK_FILES + [ROOT / "AGENTS.md", ROOT / "README.md"]

DOCUMENTS = {"introduction", "roadmap", "hallucination", "sourcecode", "useguide", "index"}
STATUSES = {"draft", "active", "blocked", "complete"}
FRONTMATTER_KEYS = {"baseline_schema", "pack", "document", "status", "updated", "code_ref"}

# The contract adds an entry index to `hallucination` above either limit.
INDEX_MAX_BYTES = 40 * 1024
INDEX_MAX_ENTRIES = 20

HEADING = re.compile(r"^#{2,4}\s+([A-Z]{2,3}-[DQP]\d+)\b", re.MULTILINE)
INDEX_ROW = re.compile(r"^\|\s*([A-Z]{2,3}-[DQP]\d+)\s*\|", re.MULTILINE)
QUALIFIED = re.compile(r"(?<![\w-])([A-Z]{2,3})-([DQP]\d+)(?![\w-])")
BARE = re.compile(r"(?<![\w-])([DQP]\d+)(?![\w-])")

# A question closed by a decision keeps its identifier in prose but loses its own
# heading: the decision that closed it carries the analysis, and the pack states
# that it is stated rather than deleted. Anything else cited must have a heading.
CLOSED_WITHOUT_HEADING = {"FD-Q3", "FD-Q4", "SC-Q1", "SC-Q2", "SC-Q3", "SC-Q4", "SC-Q5"}

# The documents recording the prefix rule quote the banned bare form as an
# example. An exact (file, identifier) allowance, so the same bare form anywhere
# else, or any other bare identifier in these files, still fails.
BARE_EXAMPLES = {
    "baselinedocs.index.md": {"D16"},
    "family-design.hallucination.md": {"D16", "D22"},
    "family-design.roadmap.md": {"D16", "P8"},
    "skill-consolidation.hallucination.md": {"D16"},
}
# README.md is checked for resolution only: its Mermaid node names (Q0, Q1, Q2)
# are not pack identifiers.
BARE_CHECKED_FILES = PACK_FILES + [ROOT / "AGENTS.md"]


def headings(path):
    return HEADING.findall(read_text(path))


def entry_index_section(text):
    match = re.search(r"^## Entry index\s*$(.*?)(?=^## )", text, re.DOTALL | re.MULTILINE)
    return match.group(1) if match else None


def defined_identifiers():
    return {identifier for path in PACK_FILES for identifier in headings(path)}


def test_packs_exist():
    assert PACK_FILES, "no baseline documents found under docs/baseline"


@pytest.mark.parametrize("path", PACK_FILES, ids=rel)
def test_pack_frontmatter_follows_the_schema(path):
    frontmatter, _ = split_frontmatter(read_text(path))
    where = rel(path)
    assert isinstance(frontmatter, dict), f"{where} has no frontmatter block"
    assert set(frontmatter) == FRONTMATTER_KEYS, (
        f"{where} frontmatter keys are {sorted(frontmatter)}, expected "
        f"{sorted(FRONTMATTER_KEYS)}"
    )
    assert frontmatter["baseline_schema"] == "2.0", f"{where}: baseline_schema is not '2.0'"
    assert frontmatter["document"] in DOCUMENTS, (
        f"{where}: document {frontmatter['document']!r} is not one of {sorted(DOCUMENTS)}"
    )
    assert frontmatter["status"] in STATUSES, (
        f"{where}: status {frontmatter['status']!r} is not one of {sorted(STATUSES)}"
    )
    updated = frontmatter["updated"]
    assert isinstance(updated, str), f"{where}: updated must be a quoted YYYY-MM-DD string"
    datetime.date.fromisoformat(updated)
    code_ref = frontmatter["code_ref"]
    assert isinstance(code_ref, str) and (
        code_ref in {"uncommitted", "unknown"} or re.fullmatch(r"[0-9a-f]{7,40}", code_ref)
    ), f"{where}: code_ref {code_ref!r} is not a commit, 'uncommitted' or 'unknown'"


@pytest.mark.parametrize("path", PACK_FILES, ids=rel)
def test_pack_filename_states_its_pack_and_document(path):
    frontmatter, _ = split_frontmatter(read_text(path))
    assert path.name == f"{frontmatter['pack']}.{frontmatter['document']}.md", (
        f"{rel(path)} should be named {frontmatter['pack']}.{frontmatter['document']}.md"
    )
    if frontmatter["document"] != "index":
        assert path.parent.name == frontmatter["pack"], (
            f"{rel(path)} sits in {path.parent.name}/, but its pack is {frontmatter['pack']!r}"
        )


@pytest.mark.parametrize("path", HALLUCINATION_FILES, ids=rel)
def test_entry_index_lists_every_entry_and_nothing_else(path):
    text = read_text(path)
    section = entry_index_section(text)
    entries = headings(path)
    over_threshold = len(text.encode("utf-8")) > INDEX_MAX_BYTES or len(entries) > INDEX_MAX_ENTRIES
    if section is None:
        assert not over_threshold, (
            f"{rel(path)} is past the contract's index threshold "
            f"({INDEX_MAX_BYTES} bytes or {INDEX_MAX_ENTRIES} entries) and has no Entry index"
        )
        return
    rows = INDEX_ROW.findall(section)
    assert len(rows) == len(set(rows)), f"{rel(path)}: duplicate Entry index rows"
    assert len(entries) == len(set(entries)), f"{rel(path)}: duplicate entry headings"
    assert set(rows) == set(entries), (
        f"{rel(path)}: index rows without an entry heading "
        f"{sorted(set(rows) - set(entries))}; entry headings without an index row "
        f"{sorted(set(entries) - set(rows))}"
    )
    stated = re.findall(r"\bholds (\d+)\b", section)
    assert all(int(count) == len(rows) for count in stated), (
        f"{rel(path)}: the index prose states {stated} entries, the table has {len(rows)}"
    )


def test_every_pack_prefix_is_declared_by_a_heading():
    prefixes = {identifier.split("-")[0] for identifier in defined_identifiers()}
    cited = {
        match.group(1)
        for path in CITING_FILES
        for match in QUALIFIED.finditer(read_text(path))
    }
    assert cited <= prefixes, (
        f"identifiers use a prefix no pack declares: {sorted(cited - prefixes)}; "
        f"declared prefixes are {sorted(prefixes)}"
    )


@pytest.mark.parametrize("path", BARE_CHECKED_FILES, ids=rel)
def test_identifiers_carry_their_pack_prefix(path):
    text = read_text(path)
    allowed = BARE_EXAMPLES.get(path.name, set())
    bare = sorted({match.group(1) for match in BARE.finditer(text)} - allowed)
    assert bare == [], (
        f"{rel(path)} cites {bare} without a pack prefix; a bare number resolves "
        "silently to whichever pack the reader has open (FD- or SC-)"
    )


@pytest.mark.parametrize("path", CITING_FILES, ids=rel)
def test_cited_identifiers_resolve_to_a_heading(path):
    defined = defined_identifiers() | CLOSED_WITHOUT_HEADING
    cited = {
        f"{match.group(1)}-{match.group(2)}"
        for match in QUALIFIED.finditer(read_text(path))
    }
    assert cited <= defined, (
        f"{rel(path)} cites identifiers that name no heading: {sorted(cited - defined)}"
    )
