"""
测试状态管理模块
"""
import unittest
import os
import json
import shutil
from datetime import datetime
from lianjia_spider.utils.state import StateManager

class TestStateManager(unittest.TestCase):
    """测试StateManager类的功能"""
    
    def setUp(self):
        """测试前准备"""
        # 创建测试目录
        self.test_dir = 'tests/test_data'
        os.makedirs(self.test_dir, exist_ok=True)
        self.state_file = os.path.join(self.test_dir, 'test_progress.json')
        
        # 初始化StateManager
        self.state_manager = StateManager(self.state_file)
        
        # 准备测试数据
        self.test_state = {
            'current_page': 1,
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scraped_ids': ['123456', '789012'],
            'total_items': 100
        }
    
    def tearDown(self):
        """测试后清理"""
        # 删除测试目录
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_init_state_file(self):
        """测试状态文件初始化"""
        # 验证文件是否创建
        self.assertTrue(os.path.exists(self.state_file))
        
        # 验证初始状态
        with open(self.state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
            self.assertEqual(state['current_page'], 1)
            self.assertEqual(state['scraped_ids'], [])
            self.assertEqual(state['total_items'], 0)
            self.assertIn('last_update', state)
    
    def test_save_and_load_state(self):
        """测试状态保存和加载"""
        # 保存测试状态
        self.state_manager.current_page = self.test_state['current_page']
        self.state_manager.scraped_ids = self.test_state['scraped_ids']
        self.state_manager.total_items = self.test_state['total_items']
        self.state_manager.save_state()
        
        # 创建新的StateManager实例加载状态
        new_manager = StateManager(self.state_file)
        
        # 验证加载的状态
        self.assertEqual(new_manager.current_page, self.test_state['current_page'])
        self.assertEqual(new_manager.scraped_ids, self.test_state['scraped_ids'])
        self.assertEqual(new_manager.total_items, self.test_state['total_items'])
    
    def test_update_progress(self):
        """测试进度更新"""
        page = 5
        house_ids = ['111111', '222222']
        total = 200
        
        # 更新进度
        self.state_manager.update_progress(page, house_ids, total)
        
        # 验证更新结果
        self.assertEqual(self.state_manager.current_page, page)
        self.assertEqual(self.state_manager.total_items, total)
        for house_id in house_ids:
            self.assertIn(house_id, self.state_manager.scraped_ids)
        
        # 验证文件内容
        with open(self.state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
            self.assertEqual(state['current_page'], page)
            self.assertEqual(state['total_items'], total)
            for house_id in house_ids:
                self.assertIn(house_id, state['scraped_ids'])
    
    def test_is_scraped(self):
        """测试房源ID检查"""
        house_id = '123456'
        
        # 初始状态
        self.assertFalse(self.state_manager.is_scraped(house_id))
        
        # 添加房源ID
        self.state_manager.update_progress(1, [house_id])
        
        # 验证状态
        self.assertTrue(self.state_manager.is_scraped(house_id))
    
    def test_get_progress(self):
        """测试获取进度信息"""
        # 设置测试数据
        self.state_manager.current_page = 5
        self.state_manager.total_items = 100
        self.state_manager.scraped_ids = ['123456', '789012']
        
        # 获取进度
        progress = self.state_manager.get_progress()
        
        # 验证进度信息
        self.assertEqual(progress['current_page'], 5)
        self.assertEqual(progress['total_items'], 100)
        self.assertEqual(len(progress['scraped_ids']), 2)
        self.assertIn('last_update', progress)
    
    def test_invalid_state_file(self):
        """测试无效状态文件处理"""
        # 创建无效的状态文件
        with open(self.state_file, 'w', encoding='utf-8') as f:
            f.write('invalid json')
        
        # 创建新的StateManager实例
        new_manager = StateManager(self.state_file)
        
        # 验证是否使用默认值
        self.assertEqual(new_manager.current_page, 1)
        self.assertEqual(new_manager.scraped_ids, [])
        self.assertEqual(new_manager.total_items, 0)
    
    def test_concurrent_access(self):
        """测试并发访问处理"""
        # 模拟多个实例同时访问
        manager1 = StateManager(self.state_file)
        manager2 = StateManager(self.state_file)
        
        # 更新状态
        manager1.update_progress(1, ['123456'])
        manager2.update_progress(2, ['789012'])
        
        # 验证最终状态
        with open(self.state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
            self.assertEqual(state['current_page'], 2)
            self.assertIn('123456', state['scraped_ids'])
            self.assertIn('789012', state['scraped_ids'])

if __name__ == '__main__':
    unittest.main()
