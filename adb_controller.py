"""
ADB 控制器 - 负责与安卓模拟器的交互
"""

import subprocess
import time
import logging
from typing import Tuple, Optional
from config import Config

class ADBController:
    """ADB 控制器类，封装所有与安卓设备交互的功能"""
    
    def __init__(self):
        """初始化 ADB 控制器"""
        self.device_id = f"{Config.ADB_HOST}:{Config.ADB_PORT}"
        self.logger = logging.getLogger(__name__)
        
    def connect_device(self) -> bool:
        """
        连接到安卓设备
        
        Returns:
            bool: 连接是否成功
        """
        try:
            # 连接设备
            result = subprocess.run(
                ["adb", "connect", self.device_id],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.logger.info(f"成功连接到设备: {self.device_id}")
                return True
            else:
                self.logger.error(f"连接设备失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("连接设备超时")
            return False
        except FileNotFoundError:
            self.logger.error("未找到 ADB 工具，请确保已安装并添加到环境变量")
            return False
        except Exception as e:
            self.logger.error(f"连接设备时发生错误: {e}")
            return False
    
    def is_device_connected(self) -> bool:
        """
        检查设备是否已连接
        
        Returns:
            bool: 设备是否已连接
        """
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            return self.device_id in result.stdout and "device" in result.stdout
            
        except Exception as e:
            self.logger.error(f"检查设备连接状态时发生错误: {e}")
            return False
    
    def click(self, x: int, y: int) -> bool:
        """
        在指定坐标点击
        
        Args:
            x (int): X 坐标
            y (int): Y 坐标
            
        Returns:
            bool: 点击是否成功
        """
        try:
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "input", "tap", str(x), str(y)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self.logger.info(f"成功点击坐标: ({x}, {y})")
                time.sleep(Config.CLICK_DELAY)
                return True
            else:
                self.logger.error(f"点击失败: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"点击时发生错误: {e}")
            return False
    
    def take_screenshot(self, save_path: str = None) -> bool:
        """
        截取屏幕截图
        
        Args:
            save_path (str): 保存路径，默认使用配置中的路径
            
        Returns:
            bool: 截图是否成功
        """
        if save_path is None:
            save_path = Config.SCREENSHOT_PATH
            
        try:
            # 在设备上截图
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "screencap", "-p", "/sdcard/screenshot.png"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                self.logger.error(f"设备截图失败: {result.stderr}")
                return False
            
            # 将截图拉取到本地
            result = subprocess.run(
                ["adb", "-s", self.device_id, "pull", "/sdcard/screenshot.png", save_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.logger.info(f"截图保存成功: {save_path}")
                return True
            else:
                self.logger.error(f"拉取截图失败: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"截图时发生错误: {e}")
            return False
    
    def press_back(self) -> bool:
        """
        按下返回键
        
        Returns:
            bool: 操作是否成功
        """
        try:
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "input", "keyevent", "KEYCODE_BACK"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self.logger.info("成功按下返回键")
                time.sleep(Config.CLICK_DELAY)
                return True
            else:
                self.logger.error(f"按下返回键失败: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"按下返回键时发生错误: {e}")
            return False
    
    def get_screen_size(self) -> Optional[Tuple[int, int]]:
        """
        获取屏幕尺寸
        
        Returns:
            Optional[Tuple[int, int]]: 屏幕尺寸 (width, height)，失败时返回 None
        """
        try:
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "wm", "size"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # 解析输出，格式类似: Physical size: 1080x1920
                output = result.stdout.strip()
                if ":" in output:
                    size_str = output.split(":")[-1].strip()
                    width, height = map(int, size_str.split("x"))
                    self.logger.info(f"屏幕尺寸: {width}x{height}")
                    return (width, height)
            
            self.logger.error(f"获取屏幕尺寸失败: {result.stderr}")
            return None
            
        except Exception as e:
            self.logger.error(f"获取屏幕尺寸时发生错误: {e}")
            return None