@echo off
echo Environment Check Tool
echo ======================

echo [1/3] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo FAIL: Python not found
    goto :error
) else (
    echo PASS: Python is available
)

echo.
echo [2/3] Checking pip...
pip --version
if %errorlevel% neq 0 (
    echo FAIL: pip not found
    goto :error
) else (
    echo PASS: pip is available
)

echo.
echo [3/3] Checking requirements.txt...
if exist requirements.txt (
    echo PASS: requirements.txt found
) else (
    echo FAIL: requirements.txt not found
    goto :error
)

echo.
echo All checks passed! You can now run install.bat
goto :end

:error
echo.
echo Some checks failed. Please fix the issues above.

:end
echo.
pause