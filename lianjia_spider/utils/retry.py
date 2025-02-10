"""
重试机制模块，处理请求失败的重试逻辑
"""
import time
import random
from typing import Callable, TypeVar, Any
from functools import wraps

T = TypeVar('T')

class RetryStrategy:
    """重试策略实现"""
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        """
        初始化重试策略
        
        Args:
            max_retries: 最大重试次数
            backoff_factor: 退避因子，用于计算重试等待时间
        """
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def execute(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        执行带重试的函数调用
        
        Args:
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            函数执行结果
            
        Raises:
            Exception: 重试耗尽后仍然失败
        """
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt == self.max_retries:
                    raise last_exception
                
                wait_time = self._calculate_wait_time(attempt)
                print(f"请求失败，{wait_time:.2f}秒后进行第{attempt + 1}次重试: {str(e)}")
                time.sleep(wait_time)
    
    def _calculate_wait_time(self, attempt: int) -> float:
        """
        计算重试等待时间
        
        Args:
            attempt: 当前重试次数
            
        Returns:
            float: 需要等待的秒数
        """
        wait_time = self.backoff_factor ** attempt
        # 添加随机抖动，避免多个请求同时重试
        jitter = random.uniform(0, 0.1) * wait_time
        return wait_time + jitter

def retry_on_failure(max_retries: int = 3, backoff_factor: float = 2.0) -> Callable:
    """
    重试装饰器
    
    Args:
        max_retries: 最大重试次数
        backoff_factor: 退避因子
        
    Returns:
        Callable: 装饰器函数
    """
    retry_strategy = RetryStrategy(max_retries, backoff_factor)
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return retry_strategy.execute(func, *args, **kwargs)
        return wrapper
    return decorator
