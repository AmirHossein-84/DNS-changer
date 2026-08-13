@echo off
@chcp 65001 >nul 2>nul
setlocal EnableDelayedExpansion
title DNS Changer Pro - Build System

echo =====================================================================
echo           DNS CHANGER PRO - WINDOWS EXECUTABLE BUILDER
echo =====================================================================
echo.

:: 1. Ensure Python dependencies are installed
echo [1/3] Installing Python build dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install Python dependencies. Please check your internet connection.
    pause
    exit /b %errorlevel%
)

echo.
echo =====================================================================
echo  Select Executable Compression Mode:
echo =====================================================================
echo.
echo   [1] UPX Compression (Recommended)
echo       * Smallest binary size (~12MB)
echo       * Auto-installs UPX via Windows Package Manager (winget) if missing
echo.
echo   [2] Native Fast Compression
echo       * Fastest startup latency (~190ms)
echo       * 100%% clean antivirus compatibility (~30MB)
echo       * Zero external tools required
echo.
set "CHOICE=1"
set /p "CHOICE=Enter choice [1 or 2] (Default = 1): "

if "%CHOICE%"=="2" goto NATIVE_BUILD

:CHECK_UPX
echo.
echo [2/3] Checking UPX binary compressor...
where upx >nul 2>nul
if %errorlevel% equ 0 goto UPX_FOUND

:: Search winget packages folder if already installed
for /f "delims=" %%i in ('dir /s /b "%LOCALAPPDATA%\Microsoft\WinGet\Packages\*upx.exe" 2^>nul') do (
    set "UPX_PATH=%%~dpi"
    set "PATH=%%~dpi;!PATH!"
    goto UPX_FOUND
)

echo [INFO] UPX not found on PATH. Attempting automatic install via winget...
winget install --id "UPX.UPX" -e --accept-source-agreements --accept-package-agreements

:: Re-check after winget installation
for /f "delims=" %%i in ('dir /s /b "%LOCALAPPDATA%\Microsoft\WinGet\Packages\*upx.exe" 2^>nul') do (
    set "UPX_PATH=%%~dpi"
    set "PATH=%%~dpi;!PATH!"
    goto UPX_FOUND
)

where upx >nul 2>nul
if %errorlevel% equ 0 goto UPX_FOUND

echo [WARN] Could not locate UPX after install. Proceeding with Native Fast Compression.
set "UPX_FLAG=--noupx"
goto DO_BUILD

:UPX_FOUND
echo [INFO] UPX detected! Enabling high-ratio binary compression.
set "UPX_FLAG="
goto DO_BUILD

:NATIVE_BUILD
echo.
echo [2/3] Selected Native Fast Compression (Skipping UPX).
set "UPX_FLAG=--noupx"
goto DO_BUILD

:DO_BUILD
echo.
echo [3/3] Compiling standalone executable with PyInstaller...
echo       * Console TUI enabled
echo       * Embedded UAC Administrator elevation manifest
echo       * Custom application icon (assets\DNS-Changer.ico)
echo.

pyinstaller --console --uac-admin --onefile --name "DNS-Changer" --icon="assets\DNS-Changer.ico" %UPX_FLAG% --clean main.py

if %errorlevel% equ 0 (
    echo.
    echo =====================================================================
    echo   [SUCCESS] Standalone executable created: dist\DNS-Changer.exe
    echo =====================================================================
    echo.
) else (
    echo.
    echo =====================================================================
    echo   [ERROR] PyInstaller compilation encountered an error.
    echo =====================================================================
    echo.
)

pause
endlocal
