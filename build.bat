@echo off
@chcp 65001 >nul 2>nul
setlocal
title DNS Changer Pro - Build System

echo =====================================================================
echo           DNS CHANGER PRO - WINDOWS EXECUTABLE BUILDER
echo =====================================================================
echo.

:: 1. Ensure Python dependencies are installed
echo [1/2] Installing Python build dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install Python dependencies. Please check your internet connection.
    pause
    exit /b %errorlevel%
)

echo.
echo [2/2] Compiling standalone executable with PyInstaller...
echo       * Console TUI enabled
echo       * Embedded UAC Administrator elevation manifest
echo       * Custom application icon (assets\DNS-Changer.ico)
echo       * Clean native fast compression
echo.

pyinstaller --console --uac-admin --onefile --noupx --name "DNS-Changer" --icon="assets\DNS-Changer.ico" --clean main.py

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
