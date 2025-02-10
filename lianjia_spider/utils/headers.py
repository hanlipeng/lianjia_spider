"""
请求头管理模块
"""
import random
from typing import Dict
from ..config.settings import USER_AGENTS

class HeadersManager:
    """请求头管理器"""
    
    def __init__(self):
        """初始化请求头管理器"""
        self.user_agents = USER_AGENTS
        self.base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }
    
    def get_headers(self) -> Dict[str, str]:
        """
        获取随机的请求头
        
        Returns:
            Dict[str, str]: 包含随机User-Agent的请求头
        """
        headers = self.base_headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        return headers
    
    def add_user_agent(self, user_agent: str) -> None:
        """
        添加新的User-Agent到池中
        
        Args:
            user_agent: 要添加的User-Agent字符串
        """
        if user_agent not in self.user_agents:
            self.user_agents.append(user_agent)
    
    def remove_user_agent(self, user_agent: str) -> None:
        """
        从池中移除指定的User-Agent
        
        Args:
            user_agent: 要移除的User-Agent字符串
        """
        if user_agent in self.user_agents and len(self.user_agents) > 1:
            self.user_agents.remove(user_agent)
