"""
工具函数模块 - 提供辅助功能
"""

import os
import json
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime

class Utils:
    """工具类，提供各种辅助功能"""
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """
        确保目录存在，不存在则创建
        
        Args:
            path (str): 目录路径
            
        Returns:
            bool: 操作是否成功
        """
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            logging.error(f"创建目录失败: {e}")
            return False
    
    @staticmethod
    def save_config(config_data: Dict[str, Any], file_path: str) -> bool:
        """
        保存配置到JSON文件
        
        Args:
            config_data (Dict[str, Any]): 配置数据
            file_path (str): 文件路径
            
        Returns:
            bool: 保存是否成功
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logging.error(f"保存配置失败: {e}")
            return False
    
    @staticmethod
    def load_config(file_path: str) -> Optional[Dict[str, Any]]:
        """
        从JSON文件加载配置
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            Optional[Dict[str, Any]]: 配置数据，失败时返回None
        """
        try:
            if not os.path.exists(file_path):
                return None
                
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"加载配置失败: {e}")
            return None
    
    @staticmethod
    def get_timestamp() -> str:
        """
        获取当前时间戳字符串
        
        Returns:
            str: 格式化的时间戳
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def retry_operation(func, max_attempts: int = 3, delay: float = 1.0, *args, **kwargs):
        """
        重试操作装饰器
        
        Args:
            func: 要重试的函数
            max_attempts (int): 最大重试次数
            delay (float): 重试间隔时间
            *args, **kwargs: 函数参数
            
        Returns:
            函数执行结果
        """
        logger = logging.getLogger(__name__)
        
        for attempt in range(max_attempts):
            try:
                result = func(*args, **kwargs)
                if result:  # 如果操作成功
                    return result
            except Exception as e:
                logger.warning(f"操作失败 (尝试 {attempt + 1}/{max_attempts}): {e}")
            
            if attempt < max_attempts - 1:  # 不是最后一次尝试
                time.sleep(delay)
        
        logger.error(f"操作在 {max_attempts} 次尝试后仍然失败")
        return None
    
    @staticmethod
    def validate_coordinates(coords: tuple, screen_size: tuple = None) -> bool:
        """
        验证坐标是否有效
        
        Args:
            coords (tuple): 坐标 (x, y)
            screen_size (tuple): 屏幕尺寸 (width, height)，可选
            
        Returns:
            bool: 坐标是否有效
        """
        if not isinstance(coords, tuple) or len(coords) != 2:
            return False
        
        x, y = coords
        if not isinstance(x, int) or not isinstance(y, int):
            return False
        
        if x < 0 or y < 0:
            return False
        
        if screen_size:
            width, height = screen_size
            if x >= width or y >= height:
                return False
        
        return True
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        格式化时间长度
        
        Args:
            seconds (float): 秒数
            
        Returns:
            str: 格式化的时间字符串
        """
        if seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}分钟"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}小时"
    
    @staticmethod
    def clean_temp_files(pattern: str = "temp_*.png") -> int:
        """
        清理临时文件
        
        Args:
            pattern (str): 文件匹配模式
            
        Returns:
            int: 清理的文件数量
        """
        import glob
        
        try:
            files = glob.glob(pattern)
            count = 0
            
            for file in files:
                try:
                    os.remove(file)
                    count += 1
                except Exception as e:
                    logging.warning(f"删除临时文件失败 {file}: {e}")
            
            if count > 0:
                logging.info(f"清理了 {count} 个临时文件")
            
            return count
            
        except Exception as e:
            logging.error(f"清理临时文件时发生错误: {e}")
            return 0

class Statistics:
    """统计信息类"""
    
    def __init__(self):
        """初始化统计信息"""
        self.start_time = time.time()
        self.attempts = 0
        self.successful_bookings = 0
        self.failed_attempts = 0
        self.total_wait_time = 0
    
    def record_attempt(self, success: bool = False):
        """
        记录一次尝试
        
        Args:
            success (bool): 是否成功
        """
        self.attempts += 1
        if success:
            self.successful_bookings += 1
        else:
            self.failed_attempts += 1
    
    def add_wait_time(self, seconds: float):
        """
        添加等待时间
        
        Args:
            seconds (float): 等待秒数
        """
        self.total_wait_time += seconds
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取统计摘要
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        current_time = time.time()
        total_runtime = current_time - self.start_time
        
        return {
            "运行时间": Utils.format_duration(total_runtime),
            "总尝试次数": self.attempts,
            "成功预订次数": self.successful_bookings,
            "失败次数": self.failed_attempts,
            "总等待时间": Utils.format_duration(self.total_wait_time),
            "成功率": f"{(self.successful_bookings / max(self.attempts, 1) * 100):.1f}%"
        }
    
    def print_summary(self):
        """打印统计摘要"""
        summary = self.get_summary()
        
        print("\n=== 运行统计 ===")
        for key, value in summary.items():
            print(f"{key}: {value}")
        print("=" * 20)