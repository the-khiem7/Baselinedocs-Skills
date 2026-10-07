#!/bin/sh
# packtool - read-only structural checks and locators for a baseline pack.
#
# POSIX sh and POSIX awk only (no gawk extensions, no regex intervals), so the
# same file runs under dash and mawk, macOS sh and BWK awk, and Git for
# Windows sh and gawk. It never writes a file, never touches the network, and
# runs git only to read HEAD and the working-tree status.
#
#   sh packtool.sh outline <file|dir>              every heading with file:line
#   sh packtool.sh find    <dir> <ID>              every occurrence of one identifier
#   sh packtool.sh next-id <dir> <D|Q|P> [PREFIX]  the next free identifier
#   sh packtool.sh check   <dir>                   FAIL and WARN findings
#
# Line numbers describe the file as it is now and go stale on the next write.
# Exit status: 0 clean (find: found), 1 FAIL present (find: not found), 2 usage.

set -u
LC_ALL=C
export LC_ALL
AWK=${AWK:-awk}

usage() {
  cat >&2 <<'EOF'
usage: sh packtool.sh outline <file|dir>
       sh packtool.sh find    <dir> <ID>
       sh packtool.sh next-id <dir> <D|Q|P> [PREFIX]
       sh packtool.sh check   <dir>
EOF
  exit 2
}

# Baseline documents only, by the contract's filename shape, down to an
# initiative's pack folders. Globs, not find(1): on Windows a bare `find` can
# resolve to FIND.EXE.
list_files() {
  for f in "$1"/*.md "$1"/*/*.md "$1"/*/*/*.md; do
    [ -f "$f" ] || continue
    if [ "$2" = baseline ]; then
      case $f in
        *.introduction.md|*.roadmap.md|*.hallucination.md|*.sourcecode.md|*.useguide.md|*.index.md) ;;
        *) continue ;;
      esac
    fi
    printf '%s\n' "$f"
  done
}

[ $# -ge 2 ] || usage
cmd=$1
target=${2%/}
[ -e "$target" ] || { echo "packtool: no such path: $target" >&2; exit 2; }
arg=
prefix=
case $cmd in
  outline|check) [ $# -eq 2 ] || usage ;;
  find)
    [ $# -eq 3 ] || usage
    arg=$3
    case $arg in
      [A-Z][A-Z]-[DQP][0-9]*|[A-Z][A-Z][A-Z]-[DQP][0-9]*) ;;
      *) usage ;;
    esac ;;
  next-id)
    [ $# -ge 3 ] && [ $# -le 4 ] || usage
    arg=$3
    prefix=${4:-}
    case $arg in D|Q|P) ;; *) usage ;; esac
    case $prefix in ''|[A-Z][A-Z]|[A-Z][A-Z][A-Z]) ;; *) usage ;; esac ;;
  *) usage ;;
esac

kind=baseline
[ "$cmd" = outline ] && kind=all
if [ -f "$target" ]; then
  files=$target
else
  files=$(list_files "$target" "$kind")
fi
if [ -z "$files" ] && [ "$cmd" = next-id ] && [ -n "$prefix" ]; then
  # A new pack has no identifier yet, so the first one is 1 by definition.
  printf '%s-%s1\n' "$prefix" "$arg"
  exit 0
fi
if [ -z "$files" ]; then
  echo "packtool: no baseline documents under $target" >&2
  [ "$cmd" = next-id ] && echo "packtool: for a new pack pass the prefix: next-id <dir> <D|Q|P> <PREFIX>" >&2
  exit 2
fi

# The pack folder's name is read from the absolute path, so `check .` run from
# inside a pack sees the folder's real name and not ".".
PT_TYPED=$target
if [ -d "$target" ]; then
  PT_ABS=$(cd "$target" && pwd)
else
  PT_ABS=$(cd "$(dirname "$target")" && pwd)/$(basename "$target")
fi
export PT_TYPED PT_ABS

# code_ref is the code state inspected. Compare it with HEAD and with the
# working tree outside the checked path, so edits to the pack itself do not
# count as uncommitted code.
git_head=
git_state=nogit
if [ "$cmd" = check ] && command -v git >/dev/null 2>&1; then
  dir=$target
  [ -d "$dir" ] || dir=$(dirname "$target")
  if git_head=$(git -C "$dir" rev-parse HEAD 2>/dev/null); then
    sub=$(git -C "$dir" rev-parse --show-prefix 2>/dev/null)
    sub=${sub%/}
    if [ -n "$sub" ]; then
      dirty=$(git -C "$dir" status --porcelain -- ":/" ":(top,exclude)$sub" 2>/dev/null) && git_state=ok
    else
      dirty=$(git -C "$dir" status --porcelain 2>/dev/null) && git_state=ok
    fi
    if [ "$git_state" = ok ]; then
      if [ -n "$dirty" ]; then git_state=dirty; else git_state=clean; fi
    fi
  else
    git_head=
  fi
fi

set --
while IFS= read -r f; do
  set -- "$@" "$f"
done <<EOF
$files
EOF

PROG='
function report(level, where, rule, msg) {
  print level " " where " " rule " " msg
  if (level == "FAIL") nfail++; else nwarn++
}
function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
function unq(s) {
  s = trim(s)
  if (s ~ /^".*"$/) s = substr(s, 2, length(s) - 2)
  return s
}
function base(p,   b) { b = p; sub(".*/", "", b); return b }
function parent(p,   d) {
  d = p
  if (PT_TYPED != "" && substr(d, 1, length(PT_TYPED)) == PT_TYPED) d = PT_ABS substr(d, length(PT_TYPED) + 1)
  if (d !~ "/") return "."
  sub("/[^/]*$", "", d); sub(".*/", "", d)
  return d
}
function short(s) { s = trim(s); return length(s) > 160 ? substr(s, 1, 157) "..." : s }
function curdoc() { return doc != "" ? doc : fdoc }
function packname() { return pack != "" ? pack : parent(file) }
function isid(s) { return s ~ /^[A-Z][A-Z][A-Z]?-[DQP][0-9]+$/ }
function idpfx(id) { return substr(id, 1, index(id, "-") - 1) }
function idkind(id) { return substr(id, index(id, "-") + 1, 1) }

# Every identifier in s, bounded so FD-D1 never matches inside XFD-D12 or FD-D1a.
function ids_in(s, out,   n, rest, off, pre, post) {
  split("", out)
  n = 0; off = 0; rest = s
  while (match(rest, /[A-Z][A-Z][A-Z]?-[DQP][0-9]+/)) {
    pre = (off + RSTART > 1) ? substr(s, off + RSTART - 1, 1) : ""
    post = substr(s, off + RSTART + RLENGTH, 1)
    if (pre !~ /[A-Za-z0-9_-]/ && post !~ /[A-Za-z0-9_-]/) out[++n] = substr(rest, RSTART, RLENGTH)
    off += RSTART + RLENGTH - 1
    rest = substr(s, off + 1)
  }
  return n
}

function occ(id, kind,   p, k, n) {
  p = idpfx(id); k = idkind(id); n = substr(id, index(id, "-") + 2) + 0
  if (n > maxn[p, k]) maxn[p, k] = n
  # One line per location and kind: an ID cited twice on one line is one hit.
  if (mode == "find" && id == target && !((loc, kind) in printed)) { printed[loc, kind] = 1; found++; print loc "\t" kind "\t" short(line) }
  if (kind == "citation") {
    if (!(id in cloc)) { cloc[id] = loc; cord[++ncd] = id }
    if (tolower(line) ~ /clos/) closedcite[id] = 1
  }
}

function heading(id, lv,   k, p, pk, d) {
  k = idkind(id); p = idpfx(id); pk = packname(); d = curdoc()
  if (!(id in hc)) horder[++nids] = id
  hc[id]++
  hlocs[id] = (hc[id] == 1) ? loc : hlocs[id] ", " loc
  hpfx[p] = 1
  if (!(p in ppack)) ppack[p] = pk
  else if (ppack[p] != pk && !((p, pk) in collided)) {
    collided[p, pk] = 1
    report("FAIL", loc, "prefix-collision", p "- is used by packs " ppack[p] " and " pk "; a prefix is unique across an initiative")
  }
  if (mode != "check") return
  if (k == "Q") {
    if (d == "hallucination" && section == "Open questions" && lv >= 3) { qk[++nqk] = file SUBSEP id; qloc[file, id] = loc }
    else report("FAIL", loc, "question-outside-open-questions", id " belongs under ## Open questions in hallucination as ### " id ": <question>")
  } else if (k == "D") {
    if (d != "hallucination") report("FAIL", loc, "decision-outside-hallucination", id " is a decision entry; decisions live in hallucination")
    else if (section == "Open questions" && lv >= 3) report("FAIL", loc, "decision-under-open-questions", id " is a decision filed under ## Open questions")
  } else if (k == "P") {
    if (d != "roadmap") report("FAIL", loc, "phase-outside-roadmap", id " names a phase; phases live in roadmap")
  }
  if (d == "hallucination" && (k == "D" || k == "Q")) {
    if (!((file, id) in hfile)) { hk[++nhk] = file SUBSEP id; hfirst[file, id] = loc }
    hfile[file, id]++
  }
}

function checkfm(where,   i, k, v) {
  for (i = 1; i <= 6; i++) if (!(KEYS[i] in fmv)) report("FAIL", where, "frontmatter-key-missing", KEYS[i])
  for (k in fmv) {
    if (!(k in want)) report("FAIL", where, "frontmatter-key-unknown", k)
    else if (fmn[k] > 1) report("FAIL", where, "frontmatter-key-duplicate", k)
  }
  if (("baseline_schema" in fmv) && fmv["baseline_schema"] != "2.0") report("FAIL", where, "frontmatter-value", "baseline_schema is not \"2.0\"")
  if (("document" in fmv) && !(fmv["document"] in docs)) report("FAIL", where, "frontmatter-value", "document " fmv["document"] " is not one of introduction|roadmap|hallucination|sourcecode|useguide|index")
  if (("status" in fmv) && !(fmv["status"] in stats)) report("FAIL", where, "frontmatter-value", "status " fmv["status"] " is not one of draft|active|blocked|complete")
  if (("updated" in fmv) && fmv["updated"] !~ /^[0-9][0-9][0-9][0-9]-[01][0-9]-[0-3][0-9]$/) report("FAIL", where, "frontmatter-value", "updated is not YYYY-MM-DD")
  v = fmv["code_ref"]
  if ("code_ref" in fmv) {
    if (v != "uncommitted" && v != "unknown" && !(v ~ /^[0-9a-f]+$/ && length(v) >= 7 && length(v) <= 40)) report("FAIL", where, "frontmatter-value", "code_ref is not a commit, uncommitted or unknown")
    else if (v == "uncommitted" && git_state == "clean") report("WARN", where, "code-ref-stale", "code_ref says uncommitted but the working tree outside the pack is clean at " substr(git_head, 1, 12) "; re-run git and record the inspected commit")
    else if (v ~ /^[0-9a-f]+$/ && git_head != "" && index(git_head, v) != 1) report("WARN", where, "code-ref-behind-head", "code_ref " v " is not HEAD " substr(git_head, 1, 12) "; a drift signal, not proof of drift")
  }
  if (pack != "" && doc != "") {
    if (base(file) != pack "." doc ".md") report("FAIL", where, "filename-mismatch", "should be named " pack "." doc ".md")
    if (doc != "index" && parent(file) != pack) report("WARN", where, "directory-mismatch", "sits in " parent(file) "/ but its pack is " pack "; a readable folder title is fine, the pack id in the frontmatter is what citations use")
  }
}

function endrun() {
  if (run > 1 && mode == "check") report("WARN", runstart, "possible-hard-wrap", "consecutive plain lines read as one paragraph; one paragraph is one line")
  run = 0
}

function startfile(   b) {
  file = FILENAME
  nfiles++
  fm = 0; fence = 0; section = ""; doc = ""; pack = ""; has_index = 0; run = 0
  split("", fmv); split("", fmn)
  b = base(file); fdoc = ""
  if (match(b, /\.[a-z]+\.md$/)) fdoc = substr(b, RSTART + 1, RLENGTH - 4)
}

function endfile() {
  endrun()
  if (mode != "check") return
  if (fm == 1) report("FAIL", file ":1", "unterminated-frontmatter", "the frontmatter block has no closing ---")
  if (curdoc() == "hallucination" && !has_index) report("FAIL", file ":1", "missing-entry-index", "hallucination carries ## Entry index from the first entry")
}

function dq(d,   s, q, dates, nd, i, tok, post, key) {
  s = line; nd = 0
  while (match(s, /20[0-9][0-9]-[01][0-9]-[0-3][0-9]/)) {
    dates[++nd] = substr(s, RSTART, RLENGTH)
    s = substr(s, 1, RSTART - 1) " " substr(s, RSTART + RLENGTH)
  }
  if (!nd) return
  q = s
  while (match(q, /[0-9][0-9.,]* ?(GB|GiB|MB|MiB|TB|TiB|KB|KiB|vCPU|IOPS|ms|%)/)) {
    tok = substr(q, RSTART, RLENGTH); post = substr(q, RSTART + RLENGTH, 1)
    q = substr(q, RSTART + RLENGTH)
    if (post ~ /[A-Za-z]/) continue
    gsub(/ /, "", tok)
    for (i = 1; i <= nd; i++) {
      key = packname() SUBSEP dates[i] SUBSEP tok
      if (d == "roadmap" && !(key in dqr)) { dqr[key] = loc; dqorder[++ndq] = key }
      if (d == "hallucination" && !(key in dqh)) dqh[key] = loc
    }
  }
}

BEGIN {
  PT_TYPED = ENVIRON["PT_TYPED"]; PT_ABS = ENVIRON["PT_ABS"]
  EN ="\342\200\223"; EM = "\342\200\224"
  split("baseline_schema pack document status updated code_ref", KEYS, " ")
  for (i = 1; i <= 6; i++) want[KEYS[i]] = 1
  split("introduction roadmap hallucination sourcecode useguide index", t, " ")
  for (i in t) docs[t[i]] = 1
  split("draft active blocked complete", t, " ")
  for (i in t) stats[t[i]] = 1
}

FNR == 1 { if (nfiles) endfile(); startfile() }

{
  line = $0
  sub(/\r$/, "", line)
  loc = FILENAME ":" FNR
  if (mode == "check" && (index(line, EN) || index(line, EM))) report("FAIL", loc, "typographic-dash", "use the ASCII hyphen, not an en dash or em dash")

  if (FNR == 1) {
    if (line == "---") { fm = 1; next }
    fm = 2
    if (mode == "check") report("FAIL", loc, "missing-frontmatter", "a baseline document starts with a --- frontmatter block")
  }
  if (fm == 1) {
    if (line == "---") { fm = 2; if (mode == "check") checkfm(file ":1"); next }
    if (match(line, /^[a-z_]+:/)) {
      k = substr(line, 1, RLENGTH - 1); v = unq(substr(line, RLENGTH + 1))
      fmv[k] = v; fmn[k]++
      if (k == "pack") pack = v
      if (k == "document") doc = v
    }
    next
  }
  if (line ~ /^```/) { fence = !fence; endrun(); next }
  if (fence) next

  if (line ~ /^#+[ \t]/) {
    endrun()
    lv = 0
    while (substr(line, lv + 1, 1) == "#") lv++
    text = trim(substr(line, lv + 1))
    if (mode == "outline") { print loc "\t" line; next }
    if (lv == 2) { section = text; if (text == "Entry index") has_index = 1 }
    own = ""
    if (lv >= 2 && lv <= 4 && match(text, /^[A-Z][A-Z][A-Z]?-[DQP][0-9]+/) && substr(text, RLENGTH + 1, 1) !~ /[A-Za-z0-9_-]/) {
      own = substr(text, 1, RLENGTH)
      heading(own, lv)
    }
    n = ids_in(line, found_ids)
    for (i = 1; i <= n; i++) occ(found_ids[i], found_ids[i] == own ? "heading" : "citation")
    next
  }
  if (mode == "outline") next

  d = curdoc()
  isrow = 0
  if (d == "hallucination" && section == "Entry index" && line ~ /^\|/) {
    split(line, cell, "|")
    rid = trim(cell[2])
    if (isid(rid)) {
      isrow = 1
      if ((file, rid) in rc) report("FAIL", loc, "duplicate-index-row", rid " already has a row at " rloc[file, rid])
      else { rloc[file, rid] = loc; rstat[file, rid] = trim(cell[4]); rorder[++nr] = file SUBSEP rid }
      rc[file, rid]++
    }
  }
  n = ids_in(line, found_ids)
  for (i = 1; i <= n; i++) occ(found_ids[i], (isrow && found_ids[i] == rid && i == 1) ? "index-row" : "citation")

  if (mode != "check") next

  if (match(line, /^\*\*[A-Z][A-Z][A-Z]?-[DQP][0-9]+(:|\*\*)/)) report("FAIL", loc, "bold-heading", "bold text is not a heading; write ## <PREFIX>-<KIND><N>: <subject>")

  if (line ~ /^[ \t]*$/ || line ~ /^([ \t]|#|\||>|[-*+][ \t]|[0-9]+[.)][ \t]|<|---|===)/) endrun()
  else {
    # A line opening with a bold label is a new field, not a wrapped continuation.
    if (line ~ /^\*\*[^*]+(:\*\*|\*\*:)/) endrun()
    if (!run) runstart = loc
    run++
  }

  if (d == "roadmap" && line !~ /^\|/ && tolower(line) ~ /root cause|rejected/ && line !~ /[A-Z][A-Z][A-Z]?-[DQ][0-9]/) report("WARN", loc, "reasoning-in-roadmap", "roadmap records outcomes; link the hallucination entry that holds the why")
  if (!isrow && (d == "roadmap" || d == "hallucination")) dq(d)
}

END {
  if (nfiles) endfile()

  if (mode == "next-id") {
    p = prefix
    if (p == "") {
      np = 0
      for (x in hpfx) { np++; p = x }
      if (np != 1) {
        print "packtool: " (np ? "several prefixes here" : "no prefix established yet") "; pass one: next-id <dir> " target " <PREFIX>" > "/dev/stderr"
        exit 2
      }
    }
    print p "-" target (maxn[p, target] + 1)
    exit 0
  }
  if (mode == "find") {
    if (!found) print "packtool: " target " does not occur under the given path" > "/dev/stderr"
    exit (found ? 0 : 1)
  }
  if (mode != "check") exit 0

  for (i = 1; i <= nids; i++) {
    id = horder[i]
    if (hc[id] > 1) { split(hlocs[id], first, ", "); report("FAIL", first[1], "duplicate-heading", id " has " hc[id] " headings: " hlocs[id]) }
  }
  for (i = 1; i <= nhk; i++) {
    split(hk[i], kv, SUBSEP)
    if (!(hk[i] in rc)) report("FAIL", hfirst[kv[1], kv[2]], "entry-without-index-row", kv[2] " has a heading but no ## Entry index row")
  }
  for (i = 1; i <= nr; i++) {
    split(rorder[i], kv, SUBSEP)
    if (!(rorder[i] in hfile)) report("FAIL", rloc[kv[1], kv[2]], "index-row-without-entry", kv[2] " has an index row but no entry heading in this document")
  }
  for (i = 1; i <= nqk; i++) {
    split(qk[i], kv, SUBSEP)
    if ((qk[i] in rstat) && tolower(rstat[qk[i]]) !~ /^open/) report("WARN", qloc[kv[1], kv[2]], "closed-question-under-open-questions", kv[2] " has index status \"" rstat[qk[i]] "\" but sits under ## Open questions")
  }
  for (i = 1; i <= ncd; i++) {
    id = cord[i]
    if ((idpfx(id) in ppack) && !(id in hc) && !(id in closedcite)) report("WARN", cloc[id], "unresolved-citation", id " is cited but no heading defines it")
  }
  for (i = 1; i <= ndq; i++) {
    if (dqorder[i] in dqh) {
      split(dqorder[i], kv, SUBSEP)
      report("WARN", dqr[dqorder[i]], "repeated-fact", kv[2] " " kv[3] " also appears at " dqh[dqorder[i]] "; roadmap keeps the outcome and links the entry")
    }
  }
  print "packtool check: " nfail + 0 " FAIL, " nwarn + 0 " WARN in " nfiles " documents"
  exit (nfail > 0)
}
'

exec "$AWK" -v mode="$cmd" -v target="$arg" -v prefix="$prefix" -v git_head="$git_head" -v git_state="$git_state" "$PROG" "$@"
