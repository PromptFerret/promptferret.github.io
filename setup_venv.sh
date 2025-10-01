#!/usr/bin/env sh
set -e

SHELL_NAME="$(basename "${SHELL:-sh}")"
echo "[*] Detected shell: $SHELL_NAME"

# Create venv (idempotent)
if [ ! -d ".venv" ]; then
  echo "[*] Creating virtual environment..."
  python3 -m venv .venv
else
  echo "[*] Using existing virtual environment (.venv)"
fi

# Install/upgrade via the correct shell so activation works for this process
case "$SHELL_NAME" in
  fish)
    echo "[*] Using fish for pip setup..."
    fish -C 'source .venv/bin/activate.fish; python -m pip install --upgrade pip; pip install mkdocs-material mkdocs-roamlinks-plugin mkdocs-rss-plugin pymdown-extensions'
    ;;
  csh|tcsh)
    echo "[*] Using csh for pip setup..."
    csh -c 'source .venv/bin/activate.csh; python -m pip install --upgrade pip; pip install mkdocs-material mkdocs-roamlinks-plugin mkdocs-rss-plugin pymdown-extensions'
    ;;
  *)
    echo "[*] Using POSIX shell for pip setup..."
    # shellcheck disable=SC1091
    . .venv/bin/activate
    python -m pip install --upgrade pip
    pip install mkdocs-material mkdocs-roamlinks-plugin mkdocs-rss-plugin pymdown-extensions
    ;;
esac

echo "[✓] Setup complete. Next: run ./start_venv.sh"
