"""
链家爬虫配置文件
"""

# 爬虫基础配置
CONFIG = {
    # 链家成都二手房URL
    'BASE_URL': 'https://cd.lianjia.com/ershoufang/',
    
    # 请求配置
    'DELAY_RANGE': (2, 5),  # 随机延迟范围（秒）
    'MAX_RETRIES': 3,       # 最大重试次数
    'BACKOFF_FACTOR': 2,    # 重试退避因子
    
    # 存储配置
    'DATA_DIR': 'data',
    'OUTPUT_FILE': 'houses.csv',
    'PROGRESS_FILE': 'progress.json',
    'SAVE_INTERVAL': 10,    # 每爬取10页保存一次进度
    
    # 日志配置
    'LOG_LEVEL': 'INFO',
    'LOG_FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'LOG_FILE': 'spider.log'
}

# CSV文件表头
CSV_HEADERS = [
    '房源ID',
    '标题',
    '总价',
    '单价',
    '小区名',
    '区域',
    '户型',
    '面积',
    '朝向',
    '装修',
    '电梯',
    '楼层',
    '建筑年代',
    '抓取时间'
]

# User-Agent池
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
]
