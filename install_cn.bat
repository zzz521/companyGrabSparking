@echo off
echo 车位抢占自动化工具 - 安装脚本
echo ================================

echo 正在检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo Python 环境检查通过！
)

echo.
echo 正在安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 依赖包安装失败
    echo 请检查网络连接后重试
    pause
    exit /b 1
) else (
    echo 依赖包安装成功！
)

echo.
echo 正在检查 ADB 工具...
adb version >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未找到 ADB 工具
    echo 请下载 Android SDK Platform Tools 并添加到环境变量
    echo 下载地址: https://developer.android.com/studio/releases/platform-tools
) else (
    echo ADB 工具检查通过！
)

echo.
echo 安装完成！
echo.
echo 使用方法:
echo   正常运行: python main.py
echo   坐标校准: python main.py --mode calibrate
echo   OCR测试: python main.py --mode test-ocr
echo.
echo 按任意键继续...
pause >nul