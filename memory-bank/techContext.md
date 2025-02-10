# 技术上下文

## 开发环境
- Python 3.8+
- IDE: VSCode
- 操作系统: Windows 11

## 核心依赖
```
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.1.0
fake-useragent==1.4.0
```

## 项目结构
```
lianjia_spider/
├── spider/
│   ├── __init__.py
│   ├── spider.py        # 爬虫核心实现
│   ├── parser.py        # 页面解析器
│   └── pipeline.py      # 数据处理管道
├── utils/
│   ├── __init__.py
│   ├── headers.py       # 请求头管理
│   ├── state.py         # 状态管理
│   └── retry.py         # 重试策略
├── data/
│   ├── houses.csv       # 房源数据
│   └── progress.json    # 进度文件
└── config/
    └── settings.py      # 配置文件
```

## 技术约束

### 1. 请求限制
- 随机延迟: 2-5秒/请求
- 最大重试次数: 3次
- 指数退避因子: 2

### 2. 数据存储
- 文件格式: CSV
- 编码: UTF-8
- 分隔符: 逗号

### 3. 状态管理
- 格式: JSON
- 保存频率: 每10页
- 字段:
  ```json
  {
    "current_page": 1,
    "last_update": "2025-02-10 21:00:00",
    "scraped_ids": ["123456", "789012"],
    "total_items": 100
  }
  ```

### 4. 错误处理
- 网络错误: 自动重试
- 解析错误: 记录日志
- 存储错误: 备份恢复

## 开发规范

### 1. 代码风格
- 遵循PEP 8
- 使用类型注解
- 编写文档字符串

### 2. 日志规范
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='spider.log'
)
```

### 3. 异常处理
```python
class SpiderException(Exception):
    """爬虫基础异常类"""
    pass

class ParseError(SpiderException):
    """解析错误"""
    pass

class NetworkError(SpiderException):
    """网络错误"""
    pass
```

### 4. 配置管理
```python
# settings.py
CONFIG = {
    'BASE_URL': 'https://bj.lianjia.com/ershoufang/',
    'DELAY_RANGE': (2, 5),
    'MAX_RETRIES': 3,
    'SAVE_INTERVAL': 10,
    'OUTPUT_FILE': 'houses.csv',
    'PROGRESS_FILE': 'progress.json'
}
```

## 部署要求
- 支持长时间运行
- 内存占用控制
- 异常自动恢复
- 进度定时保存
