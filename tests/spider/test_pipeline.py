"""
测试数据处理管道模块
"""
import unittest
import os
import csv
import shutil
from datetime import datetime
from lianjia_spider.spider.pipeline import CSVPipeline
from lianjia_spider.config.settings import CSV_HEADERS

class TestCSVPipeline(unittest.TestCase):
    """测试CSVPipeline类的功能"""
    
    def setUp(self):
        """测试前准备"""
        # 创建测试目录
        self.test_dir = 'tests/test_data'
        os.makedirs(self.test_dir, exist_ok=True)
        self.csv_file = os.path.join(self.test_dir, 'test_houses.csv')
        
        # 初始化Pipeline
        self.pipeline = CSVPipeline(self.csv_file)
        
        # 准备测试数据
        self.test_item = {
            'house_id': '123456',
            'title': '测试房源',
            'total_price': '500万',
            'unit_price': '50000元/平米',
            'community': '测试小区',
            'area': '朝阳区 望京',
            'house_type': '2室1厅',
            'floor': '中楼层(共18层)',
            'orientation': '南',
            'decoration': '精装',
            'has_elevator': '有',
            'build_year': '2010年建',
            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def tearDown(self):
        """测试后清理"""
        # 删除测试目录
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_init_csv_file(self):
        """测试CSV文件初始化"""
        # 验证文件是否创建
        self.assertTrue(os.path.exists(self.csv_file))
        
        # 验证表头
        with open(self.csv_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.assertEqual(headers, CSV_HEADERS)
    
    def test_process_item(self):
        """测试单个数据项处理"""
        self.pipeline.process_item(self.test_item)
        
        # 验证数据写入
        with open(self.csv_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            
            row = rows[0]
            # 验证数据清洗结果
            self.assertEqual(row['房源ID'], '123456')
            self.assertEqual(row['总价'], '500')
            self.assertEqual(row['单价'], '50000')
            self.assertEqual(row['小区名'], '测试小区')
            self.assertEqual(row['区域'], '朝阳区 望京')
            self.assertEqual(row['户型'], '2室1厅')
            self.assertEqual(row['楼层'], '中楼层(共18层)')
            self.assertEqual(row['朝向'], '南')
            self.assertEqual(row['装修'], '精装')
            self.assertEqual(row['电梯'], '有')
            self.assertEqual(row['建筑年代'], '2010')
    
    def test_process_items(self):
        """测试批量数据处理"""
        items = [self.test_item.copy() for _ in range(3)]
        for i, item in enumerate(items):
            item['house_id'] = f'{i+1}'
        
        self.pipeline.process_items(items)
        
        # 验证数据写入
        with open(self.csv_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 3)
            
            for i, row in enumerate(rows):
                self.assertEqual(row['房源ID'], f'{i+1}')
    
    def test_clean_item(self):
        """测试数据清洗"""
        # 准备特殊测试数据
        special_item = {
            'house_id': ' 123456 ',  # 空格
            'total_price': '500万元',  # 带单位
            'unit_price': '50,000元/平米',  # 带千分位
            'build_year': '建于2010年',  # 年份提取
            'area': None,  # 空值
            'decoration': '',  # 空字符串
        }
        
        cleaned = self.pipeline._clean_item(special_item)
        
        # 验证清洗结果
        self.assertEqual(cleaned['房源ID'], '123456')
        self.assertEqual(cleaned['总价'], '500')
        self.assertEqual(cleaned['单价'], '50000')
        self.assertEqual(cleaned['建筑年代'], '2010')
        self.assertEqual(cleaned['区域'], '')
        self.assertEqual(cleaned['装修'], '')
    
    def test_invalid_data(self):
        """测试无效数据处理"""
        # 空数据
        self.pipeline.process_item({})
        
        # 无效字段
        invalid_item = {'invalid_field': 'value'}
        self.pipeline.process_item(invalid_item)
        
        # 验证文件仍然可以正常读取
        with open(self.csv_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)  # 表头 + 两条记录

if __name__ == '__main__':
    unittest.main()
