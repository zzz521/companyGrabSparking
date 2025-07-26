@echo off
chcp 65001 >nul
echo Parking Grabber Tool - Installation Script
echo ==========================================

echo Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo Python found successfully!
)

echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
) else (
    echo Dependencies installed successfully!
)

echo.
echo Checking ADB tools...
adb version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: ADB tools not found
    echo Please download Android SDK Platform Tools
    echo Download URL: https://developer.android.com/studio/releases/platform-tools
    echo Add the tools to your system PATH
) else (
    echo ADB tools found successfully!
)

echo.
echo Installation completed!
echo.
echo Usage:
echo   Normal run: python main.py
echo   Calibrate:  python main.py --mode calibrate
echo   Test OCR:   python main.py --mode test-ocr
echo.
echo Press any key to continue...
pause >nul