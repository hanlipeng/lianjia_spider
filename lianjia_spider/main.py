"""
爬虫入口文件
"""
import os
import logging
from .spider import LianjiaSpider
from .config.settings import CONFIG

def setup_logging():
    """配置日志"""
    logging.basicConfig(
        level=getattr(logging, CONFIG['LOG_LEVEL']),
        format=CONFIG['LOG_FORMAT'],
        filename=CONFIG['LOG_FILE']
    )

def main():
    """主函数"""
    # 配置日志
    setup_logging()
    
    # 确保数据目录存在
    os.makedirs(CONFIG['DATA_DIR'], exist_ok=True)
    
    try:
        # 创建并运行爬虫
        spider = LianjiaSpider()
        spider.run()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
        logging.exception("程序异常")
        raise

if __name__ == '__main__':
    main()
