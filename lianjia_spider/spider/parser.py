"""
页面解析模块，负责解析链家房源页面
"""
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
import re
from datetime import datetime

class Parser:
    """链家页面解析器"""
    
    @staticmethod
    def parse_list_page(html: str) -> Tuple[List[Dict], Optional[int]]:
        """
        解析列表页面
        
        Args:
            html: 页面HTML内容
            
        Returns:
            tuple: (房源列表, 总数量)
        """
        soup = BeautifulSoup(html, 'html.parser')
        houses = []
        
        # 解析总数量
        total_count = None
        try:
            count_div = soup.find('h2', class_='total')
            if count_div:
                count_text = count_div.find('span')
                if count_text:
                    total_count = int(count_text.text.strip())
        except Exception:
            pass
        
        # 解析房源列表
        house_items = soup.find_all('div', class_='info clear')
        for item in house_items:
            try:
                # 提取房源链接和ID
                title_elem = item.find('a', class_='title')
                if not title_elem:
                    continue
                    
                link = title_elem.get('href', '')
                house_id = re.search(r'/(\d+).html', link)
                if not house_id:
                    continue
                    
                # 提取价格信息
                total_price = ''
                unit_price = ''
                price_elem = item.find('div', class_='priceInfo')
                if price_elem:
                    total_price = price_elem.find('div', class_='totalPrice').find('span').text.strip()
                    unit_price = price_elem.find('div', class_='unitPrice').find('span').text.strip()
                
                # 提取房源信息
                house_info = item.find('div', class_='houseInfo').text.strip()
                position_info = item.find('div', class_='positionInfo').text.strip()
                
                houses.append({
                    'house_id': house_id.group(1),
                    'title': title_elem.text.strip(),
                    'link': link,
                    'total_price': total_price,
                    'unit_price': unit_price,
                    'house_info': house_info,
                    'position_info': position_info
                })
            except Exception as e:
                print(f"解析房源信息失败: {e}")
                continue
        
        return houses, total_count
    
    @staticmethod
    def parse_detail_page(html: str, house_id: str) -> Dict:
        """
        解析详情页面
        
        Args:
            html: 页面HTML内容
            house_id: 房源ID
            
        Returns:
            Dict: 房源详细信息
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = {
            'house_id': house_id,
            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            # 基本信息
            title = soup.find('h1', class_='main')
            result['title'] = title.text.strip() if title else ''
            
            # 总价
            total_price = soup.find('span', class_='total')
            unit_price = soup.find('span', class_='unitPriceValue')
            result['total_price'] = total_price.text.strip() if total_price else ''
            result['unit_price'] = unit_price.text.strip() if unit_price else ''
            
            # 房源信息
            info_list = soup.find_all('li', class_='base')
            for item in info_list:
                label = item.find('span', class_='label')
                if not label:
                    continue
                    
                label_text = label.text.strip().rstrip('：')
                value = item.text.replace(label.text, '').strip()
                
                # 映射字段名
                field_mapping = {
                    '房屋户型': 'house_type',
                    '所在楼层': 'floor',
                    '建筑面积': 'area',
                    '户型结构': 'structure',
                    '建筑类型': 'building_type',
                    '房屋朝向': 'orientation',
                    '建筑结构': 'construction',
                    '装修情况': 'decoration',
                    '梯户比例': 'elevator_ratio',
                    '配备电梯': 'has_elevator',
                    '产权年限': 'property_term',
                    '建成年代': 'build_year'
                }
                
                field_name = field_mapping.get(label_text)
                if field_name:
                    result[field_name] = value
            
            # 小区信息
            community = soup.find('div', class_='communityName')
            if community:
                result['community'] = community.find('a').text.strip()
            
            # 所在区域
            area_div = soup.find('div', class_='areaName')
            if area_div:
                result['district'] = ' '.join([a.text.strip() for a in area_div.find_all('a')])
                
        except Exception as e:
            print(f"解析详情页失败: {e}")
            
        return result
