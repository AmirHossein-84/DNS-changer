@echo off
setlocal
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
echo Checking for UPX binary compressor...
set "UPX_FLAG="
where upx >nul 2>nul
if %errorlevel% equ 0 (
    echo [INFO] UPX detected! Enabling executable compression.
    set "UPX_FLAG=--upx-dir upx"
) else (
    echo [INFO] UPX not found on PATH. Proceeding with standard compression.
)

echo.
echo Compiling with PyInstaller (Console TUI, UAC Admin & Custom Icon)...
pyinstaller --console --uac-admin --onefile --name "DNS-Changer" --icon="assets\DNS-Changer.ico" %UPX_FLAG% --clean main.py

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
endlocal
