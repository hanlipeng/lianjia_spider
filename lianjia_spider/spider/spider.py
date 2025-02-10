"""
爬虫核心实现模块
"""
import os
import time
import random
import requests
from typing import Optional, List, Dict, Tuple
from lianjia_spider.utils.headers import HeadersManager
from lianjia_spider.utils.state import StateManager
from lianjia_spider.utils.retry import retry_on_failure
from lianjia_spider.spider.parser import Parser
from lianjia_spider.spider.pipeline import CSVPipeline
from lianjia_spider.config.settings import CONFIG

class LianjiaSpider:
    """链家爬虫实现"""
    
    def __init__(self):
        """初始化爬虫"""
        self.headers_manager = HeadersManager()
        self.state_manager = StateManager(
            os.path.join(CONFIG['DATA_DIR'], CONFIG['PROGRESS_FILE'])
        )
        self.pipeline = CSVPipeline(
            os.path.join(CONFIG['DATA_DIR'], CONFIG['OUTPUT_FILE'])
        )
        self.parser = Parser()
        
    @retry_on_failure(max_retries=CONFIG['MAX_RETRIES'])
    def _fetch_page(self, url: str) -> str:
        """
        获取页面内容
        
        Args:
            url: 页面URL
            
        Returns:
            str: 页面HTML内容
        """
        headers = self.headers_manager.get_headers()
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    
    def _random_delay(self) -> None:
        """随机延迟，避免请求过快"""
        delay = random.uniform(CONFIG['DELAY_RANGE'][0], CONFIG['DELAY_RANGE'][1])
        time.sleep(delay)
    
    def crawl_list_page(self, page: int) -> Tuple[List[Dict], Optional[int]]:
        """
        爬取列表页
        
        Args:
            page: 页码
            
        Returns:
            tuple: (房源列表, 总数量)
        """
        url = f"{CONFIG['BASE_URL']}pg{page}/"
        html = self._fetch_page(url)
        houses, total = self.parser.parse_list_page(html)
        return houses, total
    
    def crawl_detail_page(self, house_id: str, url: str) -> Dict:
        """
        爬取详情页
        
        Args:
            house_id: 房源ID
            url: 详情页URL
            
        Returns:
            Dict: 房源详细信息
        """
        html = self._fetch_page(url)
        return self.parser.parse_detail_page(html, house_id)
    
    def run(self) -> None:
        """运行爬虫"""
        current_page = self.state_manager.get_current_page()
        print(f"从第{current_page}页开始爬取...")
        
        try:
            while True:
                # 爬取列表页
                houses, total = self.crawl_list_page(current_page)
                if not houses:
                    print(f"第{current_page}页没有找到房源，爬虫结束")
                    break
                
                print(f"正在处理第{current_page}页，找到{len(houses)}个房源")
                
                # 更新总数量
                if total is not None:
                    self.state_manager.update_progress(current_page, [], total)
                
                # 处理每个房源
                for house in houses:
                    house_id = house['house_id']
                    
                    # 检查是否已爬取
                    if self.state_manager.is_scraped(house_id):
                        print(f"房源{house_id}已爬取，跳过")
                        continue
                    
                    try:
                        # 爬取详情页
                        detail = self.crawl_detail_page(house_id, house['link'])
                        
                        # 处理数据
                        self.pipeline.process_item(detail)
                        
                        # 更新进度
                        self.state_manager.update_progress(
                            current_page,
                            [house_id]
                        )
                        
                        print(f"成功爬取房源: {house_id}")
                        
                        # 随机延迟
                        self._random_delay()
                        
                    except Exception as e:
                        print(f"处理房源{house_id}失败: {e}")
                        continue
                
                # 定期保存进度
                if current_page % CONFIG['SAVE_INTERVAL'] == 0:
                    self.state_manager.save_state()
                    print(f"已保存爬取进度到第{current_page}页")
                
                current_page += 1
                
        except KeyboardInterrupt:
            print("\n检测到中断信号，正在保存进度...")
            self.state_manager.save_state()
            print("进度已保存，爬虫已安全停止")
            
        except Exception as e:
            print(f"爬虫运行异常: {e}")
            self.state_manager.save_state()
            raise
        
        finally:
            # 保存最终进度
            self.state_manager.save_state()
            print("爬虫运行完成")
