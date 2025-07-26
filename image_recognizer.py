"""
图像识别器 - 负责OCR文字识别和图像处理
"""

import cv2
import numpy as np
import pytesseract
import logging
from PIL import Image
from typing import Optional, Tuple
from config import Config

class ImageRecognizer:
    """图像识别器类，负责处理截图和识别文字"""
    
    def __init__(self):
        """初始化图像识别器"""
        self.logger = logging.getLogger(__name__)
        
        # 配置 Tesseract OCR（如果需要指定路径）
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def extract_parking_count(self, image_path: str) -> Optional[int]:
        """
        从截图中提取剩余车位数量
        
        Args:
            image_path (str): 截图文件路径
            
        Returns:
            Optional[int]: 剩余车位数量，识别失败时返回 None
        """
        try:
            # 读取图像
            image = cv2.imread(image_path)
            if image is None:
                self.logger.error(f"无法读取图像文件: {image_path}")
                return None
            
            # 裁剪到车位数量区域
            x1, y1, x2, y2 = Config.PARKING_COUNT_REGION
            roi = image[y1:y2, x1:x2]
            
            # 图像预处理
            processed_roi = self._preprocess_image(roi)
            
            # OCR 识别
            parking_count = self._ocr_extract_number(processed_roi)
            
            if parking_count is not None:
                self.logger.info(f"识别到剩余车位数量: {parking_count}")
            else:
                self.logger.warning("未能识别到车位数量")
                
            return parking_count
            
        except Exception as e:
            self.logger.error(f"提取车位数量时发生错误: {e}")
            return None
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        图像预处理，提高OCR识别准确率
        
        Args:
            image (np.ndarray): 原始图像
            
        Returns:
            np.ndarray: 处理后的图像
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 高斯模糊去噪
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # 自适应阈值二值化
        binary = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # 形态学操作，去除噪点
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        # 放大图像以提高识别精度
        resized = cv2.resize(cleaned, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        
        return resized
    
    def _ocr_extract_number(self, image: np.ndarray) -> Optional[int]:
        """
        使用OCR从图像中提取数字
        
        Args:
            image (np.ndarray): 预处理后的图像
            
        Returns:
            Optional[int]: 提取到的数字，失败时返回 None
        """
        try:
            # 配置OCR参数，只识别数字
            custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
            
            # 执行OCR识别
            text = pytesseract.image_to_string(image, config=custom_config)
            
            # 清理识别结果
            cleaned_text = ''.join(filter(str.isdigit, text))
            
            if cleaned_text:
                number = int(cleaned_text)
                return number
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"OCR识别时发生错误: {e}")
            return None
    
    def save_debug_image(self, image_path: str, output_path: str = "debug_roi.png") -> bool:
        """
        保存调试用的ROI区域图像
        
        Args:
            image_path (str): 原始截图路径
            output_path (str): 输出路径
            
        Returns:
            bool: 保存是否成功
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return False
            
            # 裁剪ROI区域
            x1, y1, x2, y2 = Config.PARKING_COUNT_REGION
            roi = image[y1:y2, x1:x2]
            
            # 预处理
            processed = self._preprocess_image(roi)
            
            # 保存处理后的图像
            cv2.imwrite(output_path, processed)
            self.logger.info(f"调试图像已保存: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存调试图像时发生错误: {e}")
            return False
    
    def detect_parking_button(self, image_path: str) -> Optional[Tuple[int, int]]:
        """
        检测"车位临停"按钮位置（可选功能，用于自动定位）
        
        Args:
            image_path (str): 截图文件路径
            
        Returns:
            Optional[Tuple[int, int]]: 按钮中心坐标，未找到时返回 None
        """
        try:
            # 这里可以实现模板匹配或其他图像识别算法
            # 暂时返回配置中的固定坐标
            return Config.PARKING_BUTTON_COORDS
            
        except Exception as e:
            self.logger.error(f"检测按钮位置时发生错误: {e}")
            return None
    
    def is_booking_page(self, image_path: str) -> bool:
        """
        判断当前是否在预订页面
        
        Args:
            image_path (str): 截图文件路径
            
        Returns:
            bool: 是否在预订页面
        """
        try:
            # 可以通过检测特定文字或UI元素来判断
            # 这里简化处理，可以根据需要扩展
            image = cv2.imread(image_path)
            if image is None:
                return False
            
            # 转换为灰度图进行文字识别
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray, lang='chi_sim')
            
            # 检查是否包含预订页面的关键词
            keywords = ["立即预订", "剩余车位", "临停申请"]
            return any(keyword in text for keyword in keywords)
            
        except Exception as e:
            self.logger.error(f"判断页面类型时发生错误: {e}")
            return False