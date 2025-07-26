"""
配置文件 - 车位抢占自动化工具
"""

class Config:
    """配置类，包含所有可配置的参数"""
    
    # ADB 连接配置
    ADB_HOST = "127.0.0.1"
    ADB_PORT = 5555  # 默认端口，根据模拟器调整
    
    # 点击坐标配置（需要根据实际屏幕分辨率调整）
    PARKING_BUTTON_COORDS = (391, 230)  # "车位临停"按钮坐标
    BOOK_NOW_BUTTON_COORDS = (360, 672)  # "立即预订"按钮坐标
    BACK_BUTTON_COORDS = (30, 54)  # 返回按钮坐标
    
    # 时间配置
    WAIT_BETWEEN_CHECKS = 60  # 检查间隔时间（秒）
    CLICK_DELAY = 2  # 点击后等待时间（秒）
    PAGE_LOAD_DELAY = 3  # 页面加载等待时间（秒）
    
    # OCR 识别配置
    PARKING_COUNT_REGION = (50, 140, 150, 180)  # 剩余车位数字识别区域 (x1, y1, x2, y2)
    OCR_CONFIDENCE_THRESHOLD = 0.7  # OCR 识别置信度阈值
    
    # 截图配置
    SCREENSHOT_PATH = "temp_screenshot.png"
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    
    # 重试配置
    MAX_RETRY_ATTEMPTS = 3  # 最大重试次数
    RETRY_DELAY = 5  # 重试间隔时间（秒）