#!/usr/bin/env bash
# slide-studio installer for Claude Code (macOS / Linux / Git Bash on Windows)
#
#   ./install.sh                 install for this user   (~/.claude/skills/slide-studio)
#   ./install.sh --project       install into this project (./.claude/skills/slide-studio)
#   ./install.sh --no-deps       skip the Python package install
#   ./install.sh --uninstall     remove the installed skill
#
# One-liner (no clone needed):
#   curl -fsSL https://raw.githubusercontent.com/owh-hwo/slide-studio-skill/main/install.sh | bash
#
# An existing install is moved to slide-studio.bak-<timestamp>, never deleted.
set -euo pipefail

REPO_URL="${SLIDE_STUDIO_REPO:-https://github.com/owh-hwo/slide-studio-skill.git}"
NAME="slide-studio"
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
DEPS=1
MODE=install

for arg in "$@"; do
  case "$arg" in
    --project)   SKILLS_DIR="$(pwd)/.claude/skills" ;;
    --no-deps)   DEPS=0 ;;
    --uninstall) MODE=uninstall ;;
    -h|--help)   sed -n '2,13p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

DEST="$SKILLS_DIR/$NAME"
say() { printf '\033[1;32m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m!!\033[0m %s\n' "$*"; }

if [ "$MODE" = uninstall ]; then
  if [ -d "$DEST" ]; then rm -rf "$DEST"; say "removed $DEST"; else warn "nothing at $DEST"; fi
  exit 0
fi

# 1. source: this clone, or a fresh shallow clone into a temp folder
SRC=""
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [ -n "$HERE" ] && [ -f "$HERE/$NAME/SKILL.md" ]; then
  SRC="$HERE/$NAME"
else
  command -v git >/dev/null || { echo "git is required for the one-line install" >&2; exit 1; }
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  say "downloading $REPO_URL"
  git clone --quiet --depth 1 "$REPO_URL" "$TMP/repo"
  SRC="$TMP/repo/$NAME"
fi

# 2. copy (back up any existing install)
mkdir -p "$SKILLS_DIR"
if [ -e "$DEST" ]; then
  BAK="$DEST.bak-$(date +%Y%m%d-%H%M%S)"
  mv "$DEST" "$BAK"
  warn "existing install moved to $BAK"
fi
cp -R "$SRC" "$DEST"
find "$DEST" -name "__pycache__" -type d -prune -exec rm -rf {} + 2>/dev/null || true
say "installed to $DEST"

# 3. python + packages
PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null && "$c" -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>/dev/null; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
  warn "Python 3.8+ not found: install it, then run: pip install python-pptx pillow pypdf pypdfium2"
elif [ "$DEPS" = 1 ]; then
  say "installing Python packages (python-pptx, pillow, pypdf, pypdfium2)"
  "$PY" -m pip install --quiet --user python-pptx pillow pypdf pypdfium2 2>/dev/null \
    || "$PY" -m pip install --quiet python-pptx pillow pypdf pypdfium2 \
    || warn "pip failed: run it yourself: $PY -m pip install python-pptx pillow pypdf pypdfium2"
fi

# 4. Chrome (used headless for checks, rendering and PPTX export)
if [ -n "$PY" ]; then
  SCRIPTS="$DEST/scripts"
  command -v cygpath >/dev/null && SCRIPTS="$(cygpath -w "$SCRIPTS")"   # Git Bash: Windows Python needs a Windows path
  if CH="$("$PY" -c "import sys; sys.path.insert(0, sys.argv[1]); import chrome; print(chrome.CHROME)" "$SCRIPTS" 2>/dev/null)"; then
    say "Chrome found: $CH"
  else
    warn "Chrome / Edge not found. Install Google Chrome, or set CHROME=/path/to/chrome"
  fi
fi

cat <<EOF

Done. Restart Claude Code (or start a new session), then ask for slides, e.g.
  "ทำสไลด์รายงานสถานะโครงการให้ผู้บริหาร"   or   /$NAME
Theme previews: $DEST/assets/previews/index.html
EOF
