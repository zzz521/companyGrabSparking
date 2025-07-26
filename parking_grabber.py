"""
车位抢占自动化工具 - 主要业务逻辑
"""

import time
import logging
from typing import Optional
from adb_controller import ADBController
from image_recognizer import ImageRecognizer
from config import Config

class ParkingGrabber:
    """车位抢占器类，实现主要的自动化逻辑"""
    
    def __init__(self):
        """初始化车位抢占器"""
        self.adb = ADBController()
        self.recognizer = ImageRecognizer()
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        
    def start(self) -> bool:
        """
        启动车位抢占程序
        
        Returns:
            bool: 启动是否成功
        """
        self.logger.info("=== 车位抢占工具启动 ===")
        
        # 连接设备
        if not self.adb.connect_device():
            self.logger.error("无法连接到安卓设备，程序退出")
            return False
        
        # 检查设备连接状态
        if not self.adb.is_device_connected():
            self.logger.error("设备未正确连接，程序退出")
            return False
        
        self.is_running = True
        self.logger.info("开始监控车位...")
        
        try:
            while self.is_running:
                success = self._attempt_booking()
                
                if success:
                    self.logger.info("🎉 车位预订成功！程序结束")
                    break
                else:
                    self.logger.info(f"暂无车位，等待 {Config.WAIT_BETWEEN_CHECKS} 秒后重试...")
                    time.sleep(Config.WAIT_BETWEEN_CHECKS)
                    
        except KeyboardInterrupt:
            self.logger.info("用户中断程序")
            self.is_running = False
        except Exception as e:
            self.logger.error(f"程序运行时发生错误: {e}")
            return False
        
        return True
    
    def stop(self):
        """停止车位抢占程序"""
        self.is_running = False
        self.logger.info("程序已停止")
    
    def _attempt_booking(self) -> bool:
        """
        尝试预订车位的完整流程
        
        Returns:
            bool: 是否成功预订
        """
        try:
            # 步骤1: 点击"车位临停"按钮
            if not self._click_parking_button():
                return False
            
            # 步骤2: 等待页面加载
            time.sleep(Config.PAGE_LOAD_DELAY)
            
            # 步骤3: 截图并检查车位数量
            parking_count = self._check_parking_availability()
            
            if parking_count is None:
                self.logger.warning("无法识别车位数量，返回上一页")
                self._go_back()
                return False
            
            # 步骤4: 根据车位数量决定操作
            if parking_count > 0:
                self.logger.info(f"发现可用车位 {parking_count} 个，尝试预订...")
                return self._book_parking()
            else:
                self.logger.info("暂无可用车位，返回上一页")
                self._go_back()
                return False
                
        except Exception as e:
            self.logger.error(f"预订流程中发生错误: {e}")
            self._go_back()  # 确保返回到主页面
            return False
    
    def _click_parking_button(self) -> bool:
        """
        点击"车位临停"按钮
        
        Returns:
            bool: 点击是否成功
        """
        x, y = Config.PARKING_BUTTON_COORDS
        success = self.adb.click(x, y)
        
        if success:
            self.logger.info("成功点击车位临停按钮")
        else:
            self.logger.error("点击车位临停按钮失败")
            
        return success
    
    def _check_parking_availability(self) -> Optional[int]:
        """
        检查车位可用性
        
        Returns:
            Optional[int]: 可用车位数量，识别失败时返回 None
        """
        # 截图
        if not self.adb.take_screenshot():
            self.logger.error("截图失败")
            return None
        
        # 识别车位数量
        parking_count = self.recognizer.extract_parking_count(Config.SCREENSHOT_PATH)
        
        if parking_count is not None:
            self.logger.info(f"当前剩余车位: {parking_count}")
        else:
            self.logger.warning("无法识别车位数量")
            # 保存调试图像
            self.recognizer.save_debug_image(Config.SCREENSHOT_PATH)
        
        return parking_count
    
    def _book_parking(self) -> bool:
        """
        执行车位预订操作
        
        Returns:
            bool: 预订是否成功
        """
        # 点击"立即预订"按钮
        x, y = Config.BOOK_NOW_BUTTON_COORDS
        success = self.adb.click(x, y)
        
        if success:
            self.logger.info("成功点击立即预订按钮")
            
            # 等待预订结果
            time.sleep(Config.PAGE_LOAD_DELAY)
            
            # 可以在这里添加预订结果验证逻辑
            # 例如检查是否出现"预订成功"的提示
            
            return True
        else:
            self.logger.error("点击立即预订按钮失败")
            return False
    
    def _go_back(self) -> bool:
        """
        返回上一页面
        
        Returns:
            bool: 返回是否成功
        """
        success = self.adb.press_back()
        
        if success:
            self.logger.info("成功返回上一页")
            time.sleep(Config.CLICK_DELAY)
        else:
            self.logger.error("返回上一页失败")
            
        return success
    
    def calibrate_coordinates(self):
        """
        坐标校准功能，帮助用户确定正确的点击坐标
        """
        self.logger.info("=== 坐标校准模式 ===")
        
        if not self.adb.connect_device():
            self.logger.error("无法连接到设备")
            return
        
        # 获取屏幕尺寸
        screen_size = self.adb.get_screen_size()
        if screen_size:
            self.logger.info(f"屏幕尺寸: {screen_size[0]}x{screen_size[1]}")
        
        # 截图用于分析
        if self.adb.take_screenshot("calibration_screenshot.png"):
            self.logger.info("校准截图已保存: calibration_screenshot.png")
            self.logger.info("请根据截图调整 config.py 中的坐标配置")
        
        # 测试当前配置的坐标
        self.logger.info("测试当前配置的坐标...")
        
        # 测试车位临停按钮
        x, y = Config.PARKING_BUTTON_COORDS
        self.logger.info(f"车位临停按钮坐标: ({x}, {y})")
        
        # 测试立即预订按钮
        x, y = Config.BOOK_NOW_BUTTON_COORDS
        self.logger.info(f"立即预订按钮坐标: ({x}, {y})")
        
        # 测试车位数量识别区域
        region = Config.PARKING_COUNT_REGION
        self.logger.info(f"车位数量识别区域: {region}")
    
    def test_ocr(self):
        """
        测试OCR识别功能
        """
        self.logger.info("=== OCR识别测试 ===")
        
        if not self.adb.connect_device():
            self.logger.error("无法连接到设备")
            return
        
        # 截图
        if not self.adb.take_screenshot("ocr_test.png"):
            self.logger.error("截图失败")
            return
        
        # 测试车位数量识别
        parking_count = self.recognizer.extract_parking_count("ocr_test.png")
        
        if parking_count is not None:
            self.logger.info(f"识别结果: {parking_count} 个车位")
        else:
            self.logger.warning("OCR识别失败")
        
        # 保存调试图像
        self.recognizer.save_debug_image("ocr_test.png", "ocr_debug.png")
        self.logger.info("调试图像已保存: ocr_debug.png")