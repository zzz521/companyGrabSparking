# 车位抢占自动化工具 - 使用指南

## 快速开始

### 1. 环境准备

1. **安装 Python 3.8+**
   - 下载地址: https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

2. **安装 ADB 工具**
   - 下载 Android SDK Platform Tools
   - 下载地址: https://developer.android.com/studio/releases/platform-tools
   - 解压后将 `adb.exe` 所在目录添加到系统环境变量 PATH

3. **安装 Tesseract OCR**
   - 下载地址: https://github.com/UB-Mannheim/tesseract/wiki
   - 安装后记录安装路径，可能需要在代码中配置

### 2. 安装依赖

双击运行 `install.bat` 或在命令行执行：
```bash
pip install -r requirements.txt
```

### 3. 配置模拟器

1. **启动安卓模拟器**（推荐使用夜神、雷电等）
2. **开启 USB 调试模式**
3. **连接 ADB**：
   ```bash
   adb connect 127.0.0.1:5555
   ```
   注意：不同模拟器端口可能不同，请查看模拟器设置

### 4. 坐标校准

首次使用前必须进行坐标校准：

1. 打开目标 APP 到主页面
2. 运行校准模式：
   ```bash
   python main.py --mode calibrate
   ```
3. 根据生成的截图，修改 `config.py` 中的坐标配置

### 5. 测试 OCR 识别

确保 OCR 能正确识别车位数量：

1. 进入车位预订页面
2. 运行 OCR 测试：
   ```bash
   python main.py --mode test-ocr
   ```
3. 检查识别结果，必要时调整 `PARKING_COUNT_REGION` 配置

### 6. 正式运行

```bash
python main.py
```

或双击运行 `run.bat` 选择运行模式。

## 配置说明

### 主要配置项 (config.py)

```python
# ADB 连接配置
ADB_HOST = "127.0.0.1"
ADB_PORT = 5555  # 根据模拟器调整

# 关键坐标（需要校准）
PARKING_BUTTON_COORDS = (391, 230)  # "车位临停"按钮
BOOK_NOW_BUTTON_COORDS = (360, 672)  # "立即预订"按钮
PARKING_COUNT_REGION = (50, 140, 150, 180)  # 车位数字区域

# 时间配置
WAIT_BETWEEN_CHECKS = 60  # 检查间隔（秒）
```

### 坐标校准步骤

1. 运行校准模式生成截图
2. 使用图片查看器打开 `calibration_screenshot.png`
3. 记录关键元素的坐标位置：
   - **车位临停按钮**: 按钮中心坐标
   - **立即预订按钮**: 按钮中心坐标
   - **车位数字区域**: 矩形区域 (x1, y1, x2, y2)
4. 更新 `config.py` 中的对应配置

## 常见问题

### Q1: ADB 连接失败
**解决方案:**
- 确保模拟器已启动且开启 USB 调试
- 检查端口号是否正确（常见端口：5555, 5554, 21503）
- 尝试重启模拟器和 ADB 服务

### Q2: OCR 识别不准确
**解决方案:**
- 调整 `PARKING_COUNT_REGION` 区域，确保只包含数字
- 检查截图质量，确保数字清晰可见
- 考虑安装中文 OCR 语言包

### Q3: 点击位置不准确
**解决方案:**
- 重新进行坐标校准
- 确保模拟器分辨率设置固定
- 检查模拟器是否有缩放设置

### Q4: 程序运行缓慢
**解决方案:**
- 减少 `PAGE_LOAD_DELAY` 等待时间
- 优化截图频率
- 确保模拟器性能设置合理

## 高级功能

### 自定义配置文件
可以创建多个配置文件适应不同的模拟器或应用版本。

### 日志分析
程序会生成详细日志文件 `parking_grabber.log`，可用于问题诊断。

### 统计信息
程序运行时会显示实时统计信息，包括成功率、运行时间等。

## 安全提醒

- 本工具仅供学习和个人使用
- 请遵守相关服务条款
- 建议在测试环境中充分验证后再正式使用
- 注意保护个人隐私和账户安全

## 技术支持

如遇到问题，请检查：
1. 日志文件中的错误信息
2. 配置文件是否正确
3. 模拟器和 ADB 连接状态
4. 目标应用是否有界面变化