"""
测试页面解析模块
"""
import unittest
from lianjia_spider.spider.parser import Parser

class TestParser(unittest.TestCase):
    """测试Parser类的功能"""
    
    def setUp(self):
        """测试前准备"""
        self.parser = Parser()
        
        # 模拟列表页HTML
        self.list_page_html = '''
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
            <div class="info clear">
                <div class="title">
                    <a href="/ershoufang/789012.html" class="title">测试房源2</a>
                </div>
                <div class="priceInfo">
                    <div class="totalPrice"><span>800</span>万</div>
                    <div class="unitPrice"><span>60000</span>元/平米</div>
                </div>
                <div class="houseInfo">3室2厅 | 120平米 | 南北 | 简装</div>
                <div class="positionInfo">高楼层(共25层) 2015年建</div>
            </div>
        </div>
        '''
        
        # 模拟详情页HTML
        self.detail_page_html = '''
        <div class="house-title">
            <h1 class="main">测试房源详情</h1>
        </div>
        <div class="price">
            <span class="total">500</span>万
            <div class="text">
                <span class="unitPriceValue">50000</span>元/平米
            </div>
        </div>
        <div class="base">
            <div class="content">
                <ul>
                    <li class="base"><span class="label">房屋户型：</span>2室1厅</li>
                    <li class="base"><span class="label">所在楼层：</span>中楼层(共18层)</li>
                    <li class="base"><span class="label">建筑面积：</span>89.12平米</li>
                    <li class="base"><span class="label">房屋朝向：</span>南</li>
                    <li class="base"><span class="label">装修情况：</span>精装</li>
                    <li class="base"><span class="label">配备电梯：</span>有</li>
                    <li class="base"><span class="label">建成年代：</span>2010年建</li>
                </ul>
            </div>
        </div>
        <div class="communityName">
            <a>测试小区</a>
        </div>
        <div class="areaName">
            <a>朝阳区</a>
            <a>望京</a>
        </div>
        '''
    
    def test_parse_list_page(self):
        """测试列表页解析"""
        houses, total = self.parser.parse_list_page(self.list_page_html)
        
        # 验证总数
        self.assertEqual(total, 2)
        
        # 验证解析到的房源数量
        self.assertEqual(len(houses), 2)
        
        # 验证第一个房源信息
        first_house = houses[0]
        self.assertEqual(first_house['house_id'], '123456')
        self.assertEqual(first_house['title'], '测试房源1')
        self.assertEqual(first_house['total_price'], '500')
        self.assertEqual(first_house['unit_price'], '50000')
        self.assertIn('2室1厅', first_house['house_info'])
        self.assertIn('中楼层', first_house['position_info'])
        
        # 验证第二个房源信息
        second_house = houses[1]
        self.assertEqual(second_house['house_id'], '789012')
        self.assertEqual(second_house['title'], '测试房源2')
        self.assertEqual(second_house['total_price'], '800')
        self.assertEqual(second_house['unit_price'], '60000')
        self.assertIn('3室2厅', second_house['house_info'])
        self.assertIn('高楼层', second_house['position_info'])
    
    def test_parse_detail_page(self):
        """测试详情页解析"""
        house_id = '123456'
        detail = self.parser.parse_detail_page(self.detail_page_html, house_id)
        
        # 验证基本信息
        self.assertEqual(detail['house_id'], house_id)
        self.assertEqual(detail['title'], '测试房源详情')
        self.assertEqual(detail['total_price'], '500')
        self.assertEqual(detail['unit_price'], '50000')
        
        # 验证房源属性
        self.assertEqual(detail['house_type'], '2室1厅')
        self.assertEqual(detail['floor'], '中楼层(共18层)')
        self.assertEqual(detail['area'], '89.12平米')
        self.assertEqual(detail['orientation'], '南')
        self.assertEqual(detail['decoration'], '精装')
        self.assertEqual(detail['has_elevator'], '有')
        self.assertEqual(detail['build_year'], '2010')
        
        # 验证位置信息
        self.assertEqual(detail['community'], '测试小区')
        self.assertEqual(detail['area'], '朝阳区 望京')
        
        # 验证爬取时间
        self.assertIn('crawl_time', detail)
        
    def test_parse_invalid_list_page(self):
        """测试无效列表页解析"""
        houses, total = self.parser.parse_list_page('')
        self.assertEqual(len(houses), 0)
        self.assertIsNone(total)
        
    def test_parse_invalid_detail_page(self):
        """测试无效详情页解析"""
        house_id = '123456'
        detail = self.parser.parse_detail_page('', house_id)
        self.assertEqual(detail['house_id'], house_id)
        self.assertIn('crawl_time', detail)

if __name__ == '__main__':
    unittest.main()
