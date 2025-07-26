"""
车位抢占自动化工具 - 主程序入口
"""

import logging
import argparse
import sys
from parking_grabber import ParkingGrabber
from config import Config

def setup_logging():
    """配置日志系统"""
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=Config.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('parking_grabber.log', encoding='utf-8')
        ]
    )

def main():
    """主函数"""
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='车位抢占自动化工具')
    parser.add_argument('--mode', choices=['run', 'calibrate', 'test-ocr'], 
                       default='run', help='运行模式')
    parser.add_argument('--config', help='配置文件路径（可选）')
    
    args = parser.parse_args()
    
    # 配置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # 创建车位抢占器实例
    grabber = ParkingGrabber()
    
    try:
        if args.mode == 'run':
            # 正常运行模式
            logger.info("启动车位抢占工具...")
            success = grabber.start()
            
            if success:
                logger.info("程序正常结束")
                sys.exit(0)
            else:
                logger.error("程序异常结束")
                sys.exit(1)
                
        elif args.mode == 'calibrate':
            # 坐标校准模式
            grabber.calibrate_coordinates()
            
        elif args.mode == 'test-ocr':
            # OCR测试模式
            grabber.test_ocr()
            
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        grabber.stop()
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序发生未处理的错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=== 车位抢占自动化工具 ===")
    print("作者: AI Assistant")
    print("功能: 自动监控并预约车位")
    print("=" * 30)
    
    main()