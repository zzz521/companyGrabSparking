@echo off
chcp 65001 >nul
echo Parking Grabber Tool
echo ====================

echo Checking device connection...
adb devices

echo.
echo Select running mode:
echo 1. Normal Run (Auto grab parking)
echo 2. Coordinate Calibration
echo 3. OCR Test
echo 4. Exit

set /p choice=Please enter your choice (1-4): 

if "%choice%"=="1" (
    echo Starting normal run mode...
    python main.py --mode run
) else if "%choice%"=="2" (
    echo Starting calibration mode...
    python main.py --mode calibrate
) else if "%choice%"=="3" (
    echo Starting OCR test mode...
    python main.py --mode test-ocr
) else if "%choice%"=="4" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice, please run again
)

echo.
pause