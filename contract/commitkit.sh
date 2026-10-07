#!/bin/sh
# commitkit - hunk listing, hunk patches, a staged-diff secret scan, and a commit message lint.
#
# POSIX sh and POSIX awk only (no gawk extensions, no regex intervals), so the
# same file runs under dash and mawk, macOS sh and BWK awk, and Git for
# Windows sh and gawk. It never writes a file, never touches the index, never
# touches the network, and runs git only to read. The agent runs the git
# commands that write; this file only computes what to write and checks it.
#
#   sh commitkit.sh hunks                       every change unit of HEAD versus the working tree
#   sh commitkit.sh patch <id> [<id> ...]       a patch holding only those units, for git apply --cached --unidiff-zero
#   sh commitkit.sh scan                        FAIL findings in the staged diff, by file:line and rule, never the value
#   sh commitkit.sh lint [--concise|--max] <msgfile>   FAIL and WARN findings in a commit message
#
# A unit is one -U0 hunk, or a whole file when the file cannot be split: a
# binary file, a mode change, a submodule, or an empty file. A unit id is a hash
# of its file and content, not its position, so it survives the recompute that
# follows every commit. Two identical units in one file get a numeric suffix by
# order, so recompute `hunks` after each commit before naming a unit.
# Untracked files that are not ignored count as new files. A rename is a
# deletion plus an addition.
#
# Exit status: 0 clean, 1 FAIL present (patch: an id not found), 2 usage. scan and
# lint print an OK line on a pass, so a pass cannot be mistaken for a run that
# never happened.

set -u
LC_ALL=C
export LC_ALL
AWK=${AWK:-awk}

usage() {
  cat >&2 <<'EOF'
usage: sh commitkit.sh hunks
       sh commitkit.sh patch <id> [<id> ...]
       sh commitkit.sh scan
       sh commitkit.sh lint [--concise|--max] <msgfile>
EOF
  exit 2
}

[ $# -ge 1 ] || usage
cmd=$1
shift

EMPTY_TREE=4b825dc642cb6eb9a060e54bf8d69288fbee4904

# The working tree against HEAD, then each untracked file as a new file. Not
# `git add -N`: this file never writes the index.
diff_stream() {
  base=HEAD
  git rev-parse --verify -q HEAD >/dev/null 2>&1 || base=$EMPTY_TREE
  git -c core.quotepath=false diff --no-color --no-ext-diff --no-renames --binary -U0 "$base" --
  git -c core.quotepath=false ls-files --others --exclude-standard | while IFS= read -r f; do
    git -c core.quotepath=false diff --no-color --no-ext-diff --binary -U0 --no-index -- /dev/null "$f"
  done
}

# One awk program serves `hunks` and `patch`, so both compute the same id for
# the same unit.
UNITS_AWK='
function hash(s,   i, n, c, h1, h2) {
  h1 = 5381
  h2 = 52711
  n = length(s)
  for (i = 1; i <= n; i++) {
    c = ord[substr(s, i, 1)] + 0
    h1 = (h1 * 33 + c) % 2147483629
    h2 = (h2 * 31 + c) % 2147483587
  }
  return sprintf("%08x%02x", h1, h2 % 256)
}
function uniq(b) {
  seen[b]++
  return seen[b] == 1 ? b : b "." seen[b]
}
function preview(s) {
  gsub(/\t/, " ", s)
  return substr(s, 1, 60)
}
function startfile(line,   rem, l) {
  infile = 1
  binary = 0
  fhdr = ""
  nh = 0
  cur = 0
  whole = 0
  kind = ""
  rem = line
  sub(/^diff --git /, "", rem)
  if (substr(rem, 1, 1) == "\"") {
    file = rem
    whole = 1
    kind = "quoted-path"
  } else {
    sub(/^a\//, "", rem)
    l = length(rem)
    file = substr(rem, 1, (l - 3) / 2)
  }
  fhdr = line "\n"
}
function blocktext(   t, h) {
  t = fhdr
  for (h = 1; h <= nh; h++) t = t hline[h] "\n" hbody[h]
  return t
}
function flushfile(   h, id, t, delta, c, selected, emitted, hdr, n, parts, i) {
  if (!infile) return
  if (nh == 0 && !whole) { whole = 1; kind = "no-hunks" }
  if (whole) {
    t = blocktext()
    id = uniq(hash(file "\n" t))
    if (mode == "hunks") {
      printf "%s\t%s\twhole\t-\t-\t-\t%s\n", id, file, kind
    } else if (id in sel) {
      printf "%s", t
      found[id] = 1
    }
  } else {
    delta = 0
    emitted = 0
    for (h = 1; h <= nh; h++) {
      id = uniq(hash(file "\n" hbody[h]))
      if (mode == "hunks") {
        printf "%s\t%s\thunk\t-%s,%s\t+%s,%s\t+%d -%d\t%s\n", id, file, hA[h], hB[h], hC[h], hD[h], nadd[h] + 0, ndel[h] + 0, preview(prev[h])
      } else if (id in sel) {
        if (!emitted) {
          n = split(fhdr, parts, "\n")
          for (i = 1; i < n; i++) if (parts[i] !~ /^index /) print parts[i]
          emitted = 1
        }
        if (hB[h] == 0) c = hA[h] + 1 + delta
        else if (hD[h] == 0) c = hA[h] - 1 + delta
        else c = hA[h] + delta
        printf "@@ -%s,%s +%s,%s @@\n", hA[h], hB[h], c, hD[h]
        printf "%s", hbody[h]
        delta += hD[h] - hB[h]
        found[id] = 1
      }
    }
  }
  infile = 0
}
BEGIN {
  for (i = 1; i < 256; i++) ord[sprintf("%c", i)] = i
  n = split(want, w, " ")
  for (i = 1; i <= n; i++) sel[w[i]] = 1
  infile = 0
}
/^diff --git / { flushfile(); startfile($0); next }
!infile { next }
{
  if (!binary && $0 ~ /^@@ -[0-9]/) {
    nh++
    cur = nh
    s = $0
    sub(/^@@ -/, "", s)
    split(s, parts, " ")
    o = parts[1]
    nw = parts[2]
    sub(/^\+/, "", nw)
    n1 = split(o, oo, ",")
    n2 = split(nw, nn, ",")
    hA[cur] = oo[1]
    hB[cur] = (n1 < 2) ? 1 : oo[2]
    hC[cur] = nn[1]
    hD[cur] = (n2 < 2) ? 1 : nn[2]
    hline[cur] = $0
    hbody[cur] = ""
    nadd[cur] = 0
    ndel[cur] = 0
    prev[cur] = ""
    next
  }
  if (cur > 0 && !binary) {
    hbody[cur] = hbody[cur] $0 "\n"
    c1 = substr($0, 1, 1)
    if (c1 == "+") { nadd[cur]++; if (prev[cur] == "") prev[cur] = substr($0, 2) }
    else if (c1 == "-") { ndel[cur]++; if (prev[cur] == "") prev[cur] = substr($0, 2) }
    if ($0 ~ /^[-+]Subproject commit /) { whole = 1; kind = "submodule" }
    next
  }
  fhdr = fhdr $0 "\n"
  if ($0 ~ /^GIT binary patch/ || $0 ~ /^Binary files /) { whole = 1; kind = "binary"; binary = 1 }
  else if ($0 ~ /^(old|new) mode /) { whole = 1; kind = "mode-change" }
  else if ($0 ~ /^(new|deleted) file mode 160000/) { whole = 1; kind = "submodule" }
}
END {
  flushfile()
  if (mode == "patch") {
    bad = 0
    for (id in sel) if (!(id in found)) { printf "commitkit: no unit with id %s\n", id > "/dev/stderr"; bad = 1 }
    if (bad) exit 1
  }
}
'

# BINMODE=3 keeps a carriage return in the data: gawk on Windows otherwise strips
# it from a CRLF file's diff lines, and the patch then fails to apply. Other awks
# treat it as an unused variable.
case $cmd in
  hunks)
    [ $# -eq 0 ] || usage
    git rev-parse --git-dir >/dev/null 2>&1 || { echo "commitkit: not inside a git repository" >&2; exit 2; }
    if [ -n "$(git ls-files -u)" ]; then
      echo "commitkit: unmerged paths present; resolve the merge first" >&2
      exit 1
    fi
    diff_stream | $AWK -v BINMODE=3 -v mode=hunks -v want= "$UNITS_AWK"
    ;;
  patch)
    [ $# -ge 1 ] || usage
    git rev-parse --git-dir >/dev/null 2>&1 || { echo "commitkit: not inside a git repository" >&2; exit 2; }
    diff_stream | $AWK -v BINMODE=3 -v mode=patch -v want="$*" "$UNITS_AWK"
    ;;
  scan)
    [ $# -eq 0 ] || usage
    git rev-parse --git-dir >/dev/null 2>&1 || { echo "commitkit: not inside a git repository" >&2; exit 2; }
    names=$(git -c core.quotepath=false diff --cached --name-only --no-renames)
    status=0
    if [ -n "$names" ]; then
      printf '%s\n' "$names" | $AWK '
        {
          n = split($0, p, "/")
          b = p[n]
          lb = tolower(b)
          bad = ""
          if (lb ~ /\.(pem|key|p12|pfx|jks|ppk)$/) bad = "key-file-name"
          else if (lb ~ /^id_(rsa|dsa|ecdsa|ed25519)$/) bad = "key-file-name"
          else if (lb ~ /\.tfstate(\.backup)?$/) bad = "terraform-state-file"
          else if (lb == ".env" || (lb ~ /^\.env\./ && lb !~ /\.(example|sample|template)$/)) bad = "env-file"
          else if (lb == "credentials" && $0 ~ /(^|\/)\.aws\//) bad = "aws-credentials-file"
          if (bad != "") { printf "FAIL %s %s\n", bad, $0; fail = 1 }
        }
        END { exit fail }
      ' || status=1
    fi
    git -c core.quotepath=false diff --cached --no-color --no-ext-diff --no-renames -U0 | $AWK '
      BEGIN {
        akid = "(AKIA|ASIA)"
        for (i = 0; i < 16; i++) akid = akid "[0-9A-Z]"
      }
      /^\+\+\+ / { f = $0; sub(/^\+\+\+ b\//, "", f); next }
      /^--- / { next }
      /^@@ / { s = $0; sub(/^@@ -[0-9,]+ \+/, "", s); sub(/[ ,].*$/, "", s); ln = s + 0; next }
      /^\+/ {
        line = substr($0, 2)
        low = tolower(line)
        rule = ""
        if (line ~ /-----BEGIN [A-Z ]*PRIVATE KEY-----/) rule = "private-key-block"
        else if (line ~ akid) rule = "aws-access-key-id"
        else if (low ~ /aws_secret_access_key[ \t]*[=:]/) rule = "aws-secret-access-key"
        else if (low ~ /(password|passwd|secret|token|api[_-]?key)[a-z0-9_]*["\047]?[ \t]*[=:][ \t]*["\047][^"\047 \t]+["\047]/ && low !~ /(example|placeholder|changeme|<[a-z_ -]+>|\$\{|xxxx|your[_-])/) rule = "credential-assignment"
        if (rule != "") { printf "FAIL %s %s:%d\n", rule, f, ln; fail = 1 }
        ln++
      }
      END { exit fail }
    ' || status=1
    # A pass prints a line: silence is indistinguishable from a scan that never ran.
    [ $status -eq 0 ] && echo "OK scan: no findings in the staged diff"
    exit $status
    ;;
  lint)
    mode=
    case ${1:-} in
      --concise|--max) mode=${1#--}; shift ;;
    esac
    [ $# -eq 1 ] || usage
    msgfile=$1
    [ -f "$msgfile" ] || { echo "commitkit: no such file: $msgfile" >&2; exit 2; }
    $AWK -v mode="$mode" '
      function fail(rule, n, msg) { printf "FAIL %s line %d: %s\n", rule, n, msg; nfail++ }
      function warn(rule, n, msg) { printf "WARN %s line %d: %s\n", rule, n, msg }
      BEGIN {
        EN = sprintf("%c%c%c", 226, 128, 147)
        EM = sprintf("%c%c%c", 226, 128, 148)
      }
      { sub(/\r$/, ""); line[NR] = $0 }
      END {
        if (NR == 0 || line[1] == "") { fail("empty-message", 1, "no title"); exit 1 }
        t = line[1]
        if (t !~ /^(feat|fix|refactor|perf|docs|test|build|ci|chore|style|revert)\([A-Za-z0-9._\/-]+\)!?: [^ ]/) fail("title-format", 1, "expected type(project): subject")
        if (length(t) > 72) fail("title-length", 1, length(t) " characters, limit 72")
        else if (mode == "concise" && length(t) > 50) warn("title-length", 1, length(t) " characters, target 50")
        if (t ~ /\.$/) warn("title-period", 1, "subject ends with a period")
        bullets = 0
        labels = 0
        for (i = 2; i <= NR; i++) {
          l = line[i]
          if (i == 2 && l != "") fail("blank-line", 2, "line after the title must be blank")
          if (l == "") continue
          if (l ~ /^[ \t]*- [^ ]/) { bullets++; continue }
          if (l ~ /^BREAKING CHANGE: [^ ]/) continue
          if (l ~ /^[A-Za-z][A-Za-z0-9 ,\/()-]*:$/) { labels++; if (mode == "concise") fail("label-in-concise", i, "concise body is flat bullets"); continue }
          fail("body-not-bullet", i, "body lines are bullets or a label ending with a colon; one bullet per line, no wrapped continuation")
        }
        if (mode == "concise" && bullets > 5) fail("too-many-bullets", NR, bullets " bullets, limit 5")
        if (mode == "max" && bullets == 0) fail("body-missing", 1, "max mode needs a body with at least one bullet")
        for (i = 1; i <= NR; i++) {
          l = line[i]
          if (index(l, EN) || index(l, EM)) fail("typographic-dash", i, "use the ASCII hyphen")
          if (l ~ /(^|[^A-Za-z])[A-Z][A-Z][A-Z]?-[DQP][0-9][0-9]*/) fail("pack-identifier", i, "name the decision or phase by its title, not its code")
          if (tolower(l) ~ /phase [0-9]/) fail("phase-number", i, "name the phase by its title, not its number")
          if (l ~ /docs\/baseline/) fail("pack-path", i, "no pack path in a commit message")
          if (l ~ /\.(introduction|roadmap|hallucination|sourcecode|useguide)\.md/) fail("pack-file", i, "no pack filename in a commit message")
          if (tolower(l) ~ /(previous|last|next|earlier|prior) commit|just before|just after/) warn("commit-position-reference", i, "name what that commit changed, not where it sits in the order")
          if (tolower(l) ~ /(^|[^a-z])(doc|baseline) pack/) warn("pack-wording", i, "say what the document holds, not that it is a pack")
          if (tolower(l) ~ /^co-authored-by:/ || tolower(l) ~ /generated with \[?claude/) fail("ai-trailer", i, "no attribution trailer")
          if (mode == "max" && tolower(l) ~ /(^|[^a-z])(various|misc|miscellaneous|some changes|and more|multiple changes|etc\.)/) warn("vague-wording", i, "state the specific change")
        }
        if (nfail == 0) print "OK lint: no FAIL findings"
        exit (nfail > 0)
      }
    ' "$msgfile"
    ;;
  *) usage ;;
esac
