@echo off
echo ===================================================
echo   Building DNS Changer Standalone Executable (.exe)
echo ===================================================
echo.

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b %errorlevel%
)

echo.
echo Compiling with PyInstaller (Console TUI, UAC Admin & Custom Icon)...
pyinstaller --console --uac-admin --onefile --name "DNS-Changer" --icon="assets\DNS-Changer.ico" --clean main.py

if %errorlevel% equ 0 (
    echo.
    echo ===================================================
    echo  [SUCCESS] Executable built in dist\DNS-Changer.exe
    echo ===================================================
) else (
    echo.
    echo [ERROR] Build failed. Check errors above.
)

pause
