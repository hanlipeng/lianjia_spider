# 链家房源爬虫

一个用于爬取链家房源数据的Python爬虫，支持断点续爬功能。

## 功能特点

- 支持断点续爬，中断后可从上次位置继续
- 自动处理反爬机制（随机User-Agent、请求延迟）
- 数据以CSV格式保存
- 异常自动重试
- 完整的日志记录

## 安装说明

1. 克隆代码库：
```bash
git clone [repository_url]
cd lianjia_spider
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 配置爬虫：
   - 编辑 `lianjia_spider/config/settings.py` 文件
   - 可以修改目标URL、延迟时间、保存路径等参数

2. 运行爬虫：
```bash
python -m lianjia_spider.main
```

3. 输出文件：
   - 房源数据：`data/houses.csv`
   - 进度文件：`data/progress.json`
   - 日志文件：`spider.log`

## 数据字段说明

CSV文件包含以下字段：
- 房源ID：链家房源唯一标识
- 标题：房源标题
- 总价：房源总价（万元）
- 单价：每平米单价
- 小区名：所在小区
- 区域：所在区域
- 户型：房屋户型
- 面积：建筑面积
- 朝向：房屋朝向
- 装修：装修情况
- 电梯：是否有电梯
- 楼层：所在楼层
- 建筑年代：建筑年份
- 抓取时间：数据抓取时间

## 中断恢复

爬虫支持以下中断恢复机制：
- Ctrl+C 中断：自动保存进度
- 异常中断：自动保存进度并记录日志
- 重启后自动从上次进度继续

## 注意事项

1. 合理使用
   - 建议适当调整请求延迟
   - 遵守网站robots.txt规则
   - 不要过于频繁请求

2. 异常处理
   - 网络错误自动重试
   - 解析失败自动跳过
   - 详细错误记录在日志中

## 开发说明

项目结构：
```
lianjia_spider/
├── spider/           # 爬虫核心实现
├── utils/            # 工具模块
├── config/           # 配置文件
└── data/             # 数据存储
```

主要模块：
- `spider.py`: 爬虫核心实现
- `parser.py`: 页面解析器
- `pipeline.py`: 数据处理管道
- `headers.py`: 请求头管理
- `state.py`: 状态管理
- `retry.py`: 重试机制
- `settings.py`: 配置参数
