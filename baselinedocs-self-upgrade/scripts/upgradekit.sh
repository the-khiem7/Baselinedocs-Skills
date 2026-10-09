#!/bin/sh
# upgradekit - list every installed baselinedocs skill under a home directory and compare its version with a release.
#
# POSIX sh and POSIX awk only (no gawk extensions, no regex intervals), so the
# same file runs under dash and mawk, macOS sh and BWK awk, and Git for Windows
# sh and gawk. It never writes a file, never touches the network, and does not
# run git. The agent fetches the latest release and runs every command that
# writes; this file only reports what is installed and how it compares.
#
#   sh upgradekit.sh inventory [<root> ...]            one row per installed baselinedocs skill
#   sh upgradekit.sh compare <latest> [<root> ...]     the same rows, each marked current, ahead, behind, or unparsable
#
# A root is a directory scanned for agent skill folders and defaults to $HOME.
# Under a root it looks for <root>/.<agent>/skills/ and <root>/.<agent>/<sub>/skills/
# holding baselinedocs-*/SKILL.md, which covers ~/.claude, ~/.agents, ~/.kiro,
# ~/.gemini/config, ~/.config/crush, ~/.snowflake/cortex and any later agent that
# follows the same layout, without a list that goes stale.
#
# A row is tab-separated: skill, version, kind, path. Version is the top-level
# `version:` of SKILL.md, or - when it is absent or not MAJOR.MINOR.PATCH. Kind is
# link when the skill folder is a symbolic link and dir otherwise. A Windows
# junction reads as dir, so kind is a hint and never proof that a copy is real.
# The same skill appears once per agent folder that holds it.
#
# Exit status: 0 clean, 1 compare found a skill behind or unparsable, 2 usage.
# Both commands print an OK line on a pass and a NONE line when no install was
# found, so a pass cannot be mistaken for a scan that found nothing.

set -u
LC_ALL=C
export LC_ALL
AWK=${AWK:-awk}

usage() {
  cat >&2 <<'EOF'
usage: sh upgradekit.sh inventory [<root> ...]
       sh upgradekit.sh compare <latest> [<root> ...]
EOF
  exit 2
}

[ $# -ge 1 ] || usage
cmd=$1
shift

SEMVER='^[0-9]+[.][0-9]+[.][0-9]+$'

# The version of one SKILL.md, read from the frontmatter only.
VERSION_AWK='
BEGIN { q = sprintf("%c", 39); out = "-" }
{ sub(/\r$/, "") }
NR == 1 { if ($0 == "---") { infm = 1; next } exit }
infm && $0 == "---" { exit }
infm && $0 ~ /^version:/ {
  v = $0
  sub(/^version:/, "", v)
  gsub(/"/, "", v)
  gsub(q, "", v)
  gsub(/[ \t]/, "", v)
  if (v ~ semver) out = v
  exit
}
END { print out }
'

# One row per install under each root. Globs are sorted by the shell and `.[!.]*`
# skips `.` and `..`; an unmatched glob stays literal and fails the -f test.
rows() {
  for root in "$@"; do
    for f in "$root"/.[!.]*/skills/baselinedocs-*/SKILL.md "$root"/.[!.]*/*/skills/baselinedocs-*/SKILL.md; do
      [ -f "$f" ] || continue
      dir=${f%/SKILL.md}
      skill=${dir##*/}
      ver=$($AWK -v semver="$SEMVER" "$VERSION_AWK" "$f")
      kind=dir
      [ -L "$dir" ] && kind=link
      printf '%s\t%s\t%s\t%s\n' "$skill" "$ver" "$kind" "$dir"
    done
  done
}

latest=
case $cmd in
  inventory) ;;
  compare)
    [ $# -ge 1 ] || usage
    latest=${1#v}
    shift
    printf '%s\n' "$latest" | $AWK -v semver="$SEMVER" '$0 ~ semver { ok = 1 } END { exit !ok }' || {
      echo "upgradekit: latest must be MAJOR.MINOR.PATCH, got '$latest'" >&2
      exit 2
    }
    ;;
  *) usage ;;
esac

if [ $# -eq 0 ]; then
  [ -n "${HOME:-}" ] || {
    echo "upgradekit: HOME is not set and no root was given" >&2
    exit 2
  }
  set -- "$HOME"
fi

case $cmd in
  inventory)
    rows "$@" | $AWK -F '\t' '
      { print; n++ }
      END {
        if (n == 0) print "NONE no baselinedocs install found"
        else printf "OK %d install(s)\n", n
      }'
    ;;
  compare)
    rows "$@" | $AWK -F '\t' -v latest="$latest" -v semver="$SEMVER" '
      function cmp(a, b,   x, y, i) {
        split(a, x, ".")
        split(b, y, ".")
        for (i = 1; i <= 3; i++) {
          if (x[i] + 0 < y[i] + 0) return -1
          if (x[i] + 0 > y[i] + 0) return 1
        }
        return 0
      }
      {
        n++
        if ($2 !~ semver) { s = "unparsable"; bad++ }
        else {
          c = cmp($2, latest)
          if (c < 0) { s = "behind"; bad++ }
          else if (c > 0) s = "ahead"
          else s = "current"
        }
        printf "%s\t%s\t%s\t%s\t%s\n", s, $1, $2, $3, $4
      }
      END {
        if (n == 0) print "NONE no baselinedocs install found"
        else if (bad > 0) printf "FAIL %d of %d install(s) behind %s or unparsable\n", bad, n, latest
        else printf "OK %d install(s) at or above %s\n", n, latest
        exit (bad > 0 ? 1 : 0)
      }'
    ;;
esac
