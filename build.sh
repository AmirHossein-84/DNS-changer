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

# 1. Install build dependencies
echo "[1/2] Installing Python build dependencies..."
pip3 install -r requirements.txt

echo
echo "[2/2] Compiling standalone executable with PyInstaller..."
echo "      * Architecture: $(uname -m) (Native macOS Binary)"
echo "      * Clean native fast compression"
echo

pyinstaller \
    --console \
    --onefile \
    --noupx \
    --name "DNS-Changer" \
    --clean \
    main.py

# 3. Create double-clickable Finder launcher (DNS-Changer.command)
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

echo
echo "====================================================================="
echo "  [SUCCESS] macOS standalone executable generated in: dist/"
echo
echo "  🚀 How to run on macOS:"
echo "     1. Double-click: dist/DNS-Changer.command (Opens in Terminal.app)"
echo "     2. Or CLI:       sudo ./dist/DNS-Changer"
echo "====================================================================="
echo
