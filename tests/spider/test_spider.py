"""
测试爬虫核心模块
"""
import unittest
import os
import shutil
from unittest.mock import Mock, patch
from lianjia_spider.spider.spider import LianjiaSpider
from lianjia_spider.utils.headers import HeadersManager
from lianjia_spider.utils.state import StateManager
from lianjia_spider.spider.parser import Parser
from lianjia_spider.spider.pipeline import CSVPipeline

class TestLianjiaSpider(unittest.TestCase):
    """测试LianjiaSpider类的功能"""
    
    def setUp(self):
        """测试前准备"""
        # 创建测试目录
        self.test_dir = 'tests/test_data'
        os.makedirs(self.test_dir, exist_ok=True)
        
        # 准备测试数据
        self.test_list_html = '''
        <div class="leftContent">
            <h2 class="total">共找到<span>2</span>套北京二手房</h2>
            <div class="info clear">
                <div class="title">
                    <a href="/ershoufang/123456.html" class="title">测试房源1</a>
                </div>
                <div class="priceInfo">
                    <div class="totalPrice"><span>500</span>万</div>
                    <div class="unitPrice"><span>50000</span>元/平米</div>
                </div>
                <div class="houseInfo">2室1厅 | 89.12平米 | 南 | 精装</div>
                <div class="positionInfo">中楼层(共18层) 2010年建</div>
            </div>
        </div>
        '''
        
        self.test_detail_html = '''
        <div class="house-title">
            <h1 class="main">测试房源详情</h1>
        </div>
        <div class="price">
            <span class="total">500</span>万
            <div class="text">
                <span class="unitPriceValue">50000</span>元/平米
            </div>
        </div>
        '''
        
        # 初始化爬虫
        self.spider = LianjiaSpider()
        
        # 修改文件路径到测试目录
        self.spider.state_manager = StateManager(
            os.path.join(self.test_dir, 'test_progress.json')
        )
        self.spider.pipeline = CSVPipeline(
            os.path.join(self.test_dir, 'test_houses.csv')
        )
    
    def tearDown(self):
        """测试后清理"""
        # 删除测试目录
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @patch('requests.get')
    def test_fetch_page(self, mock_get):
        """测试页面获取"""
        # 配置mock
        mock_response = Mock()
        mock_response.text = self.test_list_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # 获取页面
        html = self.spider._fetch_page('http://test.url')
        
        # 验证结果
        self.assertEqual(html, self.test_list_html)
        mock_get.assert_called_once()
        
        # 验证请求头
        headers = mock_get.call_args[1]['headers']
        self.assertIn('User-Agent', headers)
    
    @patch('time.sleep')
    def test_random_delay(self, mock_sleep):
        """测试随机延迟"""
        self.spider._random_delay()
        mock_sleep.assert_called_once()
        delay = mock_sleep.call_args[0][0]
        self.assertGreaterEqual(delay, 2)
        self.assertLessEqual(delay, 5)
    
    @patch('requests.get')
    def test_crawl_list_page(self, mock_get):
        """测试列表页爬取"""
        # 配置mock
        mock_response = Mock()
        mock_response.text = self.test_list_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # 爬取列表页
        houses, total = self.spider.crawl_list_page(1)
        
        # 验证结果
        self.assertEqual(total, 2)
        self.assertEqual(len(houses), 1)
        self.assertEqual(houses[0]['house_id'], '123456')
    
    @patch('requests.get')
    def test_crawl_detail_page(self, mock_get):
        """测试详情页爬取"""
        # 配置mock
        mock_response = Mock()
        mock_response.text = self.test_detail_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # 爬取详情页
        detail = self.spider.crawl_detail_page('123456', 'http://test.url')
        
        # 验证结果
        self.assertEqual(detail['house_id'], '123456')
        self.assertEqual(detail['title'], '测试房源详情')
        self.assertEqual(detail['total_price'], '500')
    
    @patch('requests.get')
    def test_retry_mechanism(self, mock_get):
        """测试重试机制"""
        # 配置mock先失败后成功
        mock_get.side_effect = [
            Exception("Connection error"),
            Exception("Timeout"),
            Mock(text=self.test_list_html, raise_for_status=Mock())
        ]
        
        # 获取页面
        html = self.spider._fetch_page('http://test.url')
        
        # 验证结果
        self.assertEqual(html, self.test_list_html)
        self.assertEqual(mock_get.call_count, 3)
    
    @patch('requests.get')
    @patch('time.sleep')
    def test_run(self, mock_sleep, mock_get):
        """测试爬虫运行"""
        # 配置mock
        mock_get.side_effect = [
            # 列表页
            Mock(text=self.test_list_html, raise_for_status=Mock()),
            # 详情页
            Mock(text=self.test_detail_html, raise_for_status=Mock())
        ]
        
        try:
            # 运行爬虫
            self.spider.run()
        except StopIteration:
            pass  # 预期的停止
        
        # 验证状态保存
        state = self.spider.state_manager.get_progress()
        self.assertGreater(state['current_page'], 0)
        self.assertIn('123456', state['scraped_ids'])
        
        # 验证数据保存
        self.assertTrue(os.path.exists(self.spider.pipeline.file_path))
    
    @patch('requests.get')
    def test_error_handling(self, mock_get):
        """测试错误处理"""
        # 配置mock始终失败
        mock_get.side_effect = Exception("Persistent error")
        
        with self.assertRaises(Exception):
            self.spider._fetch_page('http://test.url')
        
        # 验证重试次数
        self.assertEqual(mock_get.call_count, 3)  # 默认最大重试次数
    
    def test_keyboard_interrupt_handling(self):
        """测试中断处理"""
        # 模拟运行时的键盘中断
        with patch('requests.get') as mock_get:
            mock_get.side_effect = KeyboardInterrupt()
            
            try:
                self.spider.run()
            except KeyboardInterrupt:
                pass
            
            # 验证状态是否保存
            self.assertTrue(os.path.exists(self.spider.state_manager.file_path))

if __name__ == '__main__':
    unittest.main()
