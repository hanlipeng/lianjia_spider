"""
数据处理管道，负责数据清洗和存储
"""
import os
import csv
from typing import Dict, List
from datetime import datetime
from lianjia_spider.config.settings import CSV_HEADERS

class CSVPipeline:
    """CSV数据处理管道"""
    
    def __init__(self, file_path: str):
        """
        初始化CSV处理管道
        
        Args:
            file_path: CSV文件路径
        """
        self.file_path = file_path
        self._init_csv_file()
    
    def _init_csv_file(self) -> None:
        """初始化CSV文件，如果不存在则创建并写入表头"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        # 如果文件不存在，创建并写入表头
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADERS)
    
    def process_item(self, item: Dict) -> None:
        """
        处理单个房源数据并写入CSV
        
        Args:
            item: 房源数据字典
        """
        try:
            # 数据清洗和转换
            processed_item = self._clean_item(item)
            
            # 写入CSV文件
            self._write_to_csv(processed_item)
        except Exception as e:
            print(f"处理数据项失败: {e}")
    
    def process_items(self, items: List[Dict]) -> None:
        """
        批量处理房源数据
        
        Args:
            items: 房源数据列表
        """
        for item in items:
            self.process_item(item)
    
    def _clean_item(self, item: Dict) -> Dict:
        """
        清洗和标准化数据项
        
        Args:
            item: 原始数据字典
            
        Returns:
            Dict: 清洗后的数据字典
        """
        cleaned = {}
        
        # 提取数值
        def extract_number(text: str) -> str:
            if not text:
                return ''
            numbers = ''.join(filter(lambda x: x.isdigit() or x == '.', text))
            return numbers if numbers else ''
        
        # 字段映射关系（英文字段名到中文字段名）
        field_mapping = {
            'house_id': '房源ID',
            'title': '标题',
            'total_price': '总价',
            'unit_price': '单价',
            'community': '小区名',
            'district': '区域',
            'house_type': '户型',
            'area': '面积',
            'orientation': '朝向',
            'decoration': '装修',
            'has_elevator': '电梯',
            'floor': '楼层',
            'build_year': '建筑年代',
            'crawl_time': '抓取时间'
        }
        
        # 清洗规则
        clean_rules = {
            '房源ID': lambda x: str(x),
            '标题': lambda x: str(x).strip(),
            '总价': lambda x: extract_number(x),
            '单价': lambda x: extract_number(x),
            '小区名': lambda x: str(x).strip(),
            '区域': lambda x: str(x).strip(),
            '户型': lambda x: str(x).strip(),
            '面积': lambda x: str(x).strip(),
            '朝向': lambda x: str(x).strip(),
            '装修': lambda x: str(x).strip(),
            '电梯': lambda x: str(x).strip(),
            '楼层': lambda x: str(x).strip(),
            '建筑年代': lambda x: extract_number(x),
            '抓取时间': lambda x: str(x).strip()
        }
        
        # 应用清洗规则
        for en_field, value in item.items():
            if en_field in field_mapping:
                cn_field = field_mapping[en_field]
                if cn_field in clean_rules:
                    cleaned[cn_field] = clean_rules[cn_field](value)
        
        # 添加爬取时间
        if 'crawl_time' not in cleaned:
            cleaned['抓取时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return cleaned
    
    def _write_to_csv(self, item: Dict) -> None:
        """
        将数据写入CSV文件
        
        Args:
            item: 处理后的数据字典
        """
        try:
            with open(self.file_path, 'a', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
                writer.writerow(item)
        except Exception as e:
            print(f"写入CSV失败: {e}")
            # 可以考虑实现备份机制
            raise
