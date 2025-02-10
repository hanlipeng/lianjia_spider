"""
状态管理模块，用于处理爬虫进度的保存和恢复
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class StateManager:
    """状态管理器，负责爬虫断点续爬功能"""
    
    def __init__(self, progress_file: str):
        """
        初始化状态管理器
        
        Args:
            progress_file: 进度文件路径
        """
        self.file_path = progress_file
        self.progress_file = progress_file  # 保持向后兼容
        self.current_state = {
            'current_page': 1,
            'scraped_ids': [],
            'total_items': 0,
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self._load_state()
        # 确保状态文件存在
        self.save_state()
    
    def _load_state(self) -> None:
        """从文件加载状态"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    saved_state = json.load(f)
                    self.current_state.update(saved_state)
        except Exception as e:
            print(f"加载状态文件失败: {e}")
    
    def save_state(self) -> None:
        """保存当前状态到文件"""
        try:
            self.current_state['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            os.makedirs(os.path.dirname(self.progress_file), exist_ok=True)
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存状态文件失败: {e}")
    
    def update_progress(self, page: int, house_ids: List[str], total_items: Optional[int] = None) -> None:
        """
        更新爬虫进度
        
        Args:
            page: 当前页码
            house_ids: 新爬取的房源ID列表
            total_items: 总房源数量（可选）
        """
        self.current_state['current_page'] = page
        self.current_state['scraped_ids'].extend(house_ids)
        if total_items is not None:
            self.current_state['total_items'] = total_items
    
    @property
    def current_page(self) -> int:
        """当前页码"""
        return self.current_state['current_page']
    
    @current_page.setter
    def current_page(self, value: int) -> None:
        """设置当前页码"""
        self.current_state['current_page'] = value
    
    def get_current_page(self) -> int:
        """获取当前页码"""
        return self.current_state['current_page']
    
    def get_scraped_ids(self) -> List[str]:
        """获取已爬取的房源ID列表"""
        return self.current_state['scraped_ids']
    
    def get_total_items(self) -> int:
        """获取总房源数量"""
        return self.current_state['total_items']
    
    def is_scraped(self, house_id: str) -> bool:
        """
        检查房源是否已被爬取
        
        Args:
            house_id: 房源ID
            
        Returns:
            bool: 是否已爬取
        """
        return house_id in self.current_state['scraped_ids']
    
    def get_progress(self) -> Dict:
        """
        获取进度信息
        
        Returns:
            Dict: 包含进度信息的字典
        """
        return {
            'current_page': self.current_state['current_page'],
            'scraped_count': len(self.current_state['scraped_ids']),
            'total_items': self.current_state['total_items'],
            'last_update': self.current_state['last_update']
        }
