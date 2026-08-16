#!/usr/bin/env bash
# =============================================================================
#  DNS CHANGER PRO - macOS Standalone Executable Builder
#  Compiles a standalone Mach-O Unix binary & double-clickable .command launcher
# =============================================================================
set -e

echo "====================================================================="
echo "        🍎 DNS CHANGER PRO - MACOS EXECUTABLE BUILDER 🍎"
echo "====================================================================="
echo

# 1. Setup isolated Virtual Environment (100% PEP 668 & Homebrew compliant)
VENV_DIR=".build_venv"

if [ -z "$VIRTUAL_ENV" ]; then
    if [ ! -d "$VENV_DIR" ]; then
        echo "[1/3] Creating isolated Python build environment (.build_venv)..."
        python3 -m venv "$VENV_DIR"
    else
        echo "[1/3] Using existing cached build environment (.build_venv)..."
    fi
    source "$VENV_DIR/bin/activate"
else
    echo "[1/3] Using active virtual environment: $VIRTUAL_ENV"
fi

# 2. Install build dependencies inside the virtual environment
echo "[2/3] Installing Python build dependencies..."
pip install --upgrade pip --quiet 2>/dev/null || true
pip install -r requirements.txt

# 3. Ensure macOS .icns icon exists
if [ ! -f "assets/DNS-Changer.icns" ] && [ -f "assets/DNS-Changer.ico" ]; then
    echo "[INFO] Converting application icon to Apple ICNS format..."
    python3 -c "
from PIL import Image
img = Image.open('assets/DNS-Changer.ico')
img.save('assets/DNS-Changer.icns', format='ICNS')
img.save('assets/DNS-Changer.png', format='PNG')
" 2>/dev/null || true
fi

ICON_FLAG=""
if [ -f "assets/DNS-Changer.icns" ]; then
    ICON_FLAG="--icon=assets/DNS-Changer.icns"
fi

echo
echo "[3/3] Compiling standalone executable with PyInstaller..."
echo "      * Architecture: $(uname -m) (Native macOS Binary)"
echo "      * Custom Application Icon: assets/DNS-Changer.icns"
echo "      * Clean native fast compression"
echo

pyinstaller \
    --console \
    --onefile \
    --noupx \
    --name "DNS-Changer" \
    $ICON_FLAG \
    --clean \
    main.py

# 4. Create double-clickable Finder launcher (DNS-Changer.command)
cat << 'EOF' > dist/DNS-Changer.command
#!/usr/bin/env bash
# Double-click launcher for macOS Finder / Terminal.app
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Ensure execution permissions
chmod +x ./DNS-Changer 2>/dev/null || true

# Execute with root elevation
if [ "$EUID" -ne 0 ]; then
    echo "🔐 DNS Changer Pro requires administrator privileges to modify DNS."
    sudo ./DNS-Changer "$@"
else
    ./DNS-Changer "$@"
fi
EOF

chmod +x dist/DNS-Changer.command 2>/dev/null || true
chmod +x dist/DNS-Changer 2>/dev/null || true

# 5. Set Finder Icon for DNS-Changer and DNS-Changer.command if Cocoa is available
if [ -f "assets/DNS-Changer.png" ]; then
    python3 -c "
try:
    import Cocoa
    ws = Cocoa.NSWorkspace.sharedWorkspace()
    img = Cocoa.NSImage.alloc().initWithContentsOfFile_('assets/DNS-Changer.png')
    if img:
        ws.setIcon_forFile_options_(img, 'dist/DNS-Changer.command', 0)
        ws.setIcon_forFile_options_(img, 'dist/DNS-Changer', 0)
except Exception:
    pass
" 2>/dev/null || true
fi

echo
echo "====================================================================="
echo "  [SUCCESS] macOS standalone executable generated in: dist/"
echo
echo "  🚀 How to run on macOS:"
echo "     1. Double-click: dist/DNS-Changer.command (Opens in Terminal.app)"
echo "     2. Or CLI:       sudo ./dist/DNS-Changer"
echo "====================================================================="
echo
