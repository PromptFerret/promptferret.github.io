#!/usr/bin/env sh
set -e

SHELL_NAME="$(basename "${SHELL:-sh}")"
echo "[*] Detected shell: $SHELL_NAME"

# Pick the right activation & launch mkdocs with that shell.
case "$SHELL_NAME" in
  fish)
    if [ ! -f ".venv/bin/activate.fish" ]; then
      echo "[!] .venv not found. Run ./setup_venv.sh first."
      exit 1
    fi
    echo "[*] Starting MkDocs (fish)…"
    exec fish -C 'source .venv/bin/activate.fish; mkdocs serve'
    ;;
  csh|tcsh)
    if [ ! -f ".venv/bin/activate.csh" ]; then
      echo "[!] .venv not found. Run ./setup_venv.sh first."
      exit 1
    fi
    echo "[*] Starting MkDocs (csh)…"
    exec csh -c 'source .venv/bin/activate.csh; mkdocs serve'
    ;;
  *)
    if [ ! -f ".venv/bin/activate" ]; then
      echo "[!] .venv not found. Run ./setup_venv.sh first."
      exit 1
    fi
    echo "[*] Starting MkDocs (POSIX)…"
    # shellcheck disable=SC1091
    . .venv/bin/activate
    export PYTHONWARNINGS=ignore::DeprecationWarning
    exec mkdocs serve
    ;;
esac
