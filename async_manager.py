#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步任务管理器 - 用于安全管理异步任务和事件循环
"""

import asyncio
import logging
import threading
import atexit
from typing import Optional, Callable, Any
import signal
import sys

logger = logging.getLogger(__name__)

class AsyncManager:
    """异步任务管理器"""
    
    def __init__(self):
        self.background_tasks = set()
        self.shutdown_event = asyncio.Event()
        self.cleanup_handlers = []
        self._register_cleanup()
    
    def _register_cleanup(self):
        """注册清理处理器"""
        atexit.register(self.cleanup_all)
        
        # 注册信号处理
        def signal_handler(signum, frame):
            logger.info(f"收到信号 {signum}，开始清理...")
            self.cleanup_all()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def create_task(self, coro, name: Optional[str] = None):
        """创建并跟踪异步任务"""
        try:
            task = asyncio.create_task(coro, name=name)
            self.background_tasks.add(task)
            task.add_done_callback(self.background_tasks.discard)
            return task
        except RuntimeError:
            # 没有运行的事件循环
            logger.warning("没有运行的事件循环，无法创建任务")
            return None
    
    def run_in_thread(self, coro, thread_name: Optional[str] = None):
        """在新线程中运行异步协程"""
        def thread_func():
            try:
                # 为线程创建新的事件循环
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    # 运行协程
                    loop.run_until_complete(coro)
                finally:
                    # 清理所有待处理任务
                    pending = asyncio.all_tasks(loop)
                    if pending:
                        # 取消所有任务
                        for task in pending:
                            task.cancel()
                        
                        # 等待任务完成取消
                        try:
                            loop.run_until_complete(
                                asyncio.gather(*pending, return_exceptions=True)
                            )
                        except Exception as e:
                            logger.debug(f"清理待处理任务时出现异常: {e}")
                    
                    # 关闭事件循环
                    loop.close()
                    
            except Exception as e:
                logger.error(f"线程异步任务执行失败: {e}")
        
        thread = threading.Thread(
            target=thread_func,
            name=thread_name or "AsyncWorker",
            daemon=True
        )
        thread.start()
        return thread
    
    def add_cleanup_handler(self, handler: Callable):
        """添加清理处理器"""
        self.cleanup_handlers.append(handler)
    
    def cleanup_all(self):
        """清理所有资源"""
        logger.info("开始清理异步资源...")
        
        # 调用自定义清理处理器
        for handler in self.cleanup_handlers:
            try:
                handler()
            except Exception as e:
                logger.error(f"清理处理器执行失败: {e}")
        
        # 取消所有后台任务
        for task in self.background_tasks.copy():
            if not task.done():
                task.cancel()
        
        # 设置关闭事件
        try:
            if not self.shutdown_event.is_set():
                self.shutdown_event.set()
        except RuntimeError:
            pass  # 事件循环可能已关闭
        
        logger.info("异步资源清理完成")

# 全局异步管理器实例
async_manager = AsyncManager()

def safe_create_task(coro, name: Optional[str] = None):
    """安全创建异步任务"""
    return async_manager.create_task(coro, name)

def safe_run_in_thread(coro, thread_name: Optional[str] = None):
    """安全在线程中运行异步任务"""
    return async_manager.run_in_thread(coro, thread_name)

def add_cleanup_handler(handler: Callable):
    """添加清理处理器"""
    async_manager.add_cleanup_handler(handler)

async def safe_aiohttp_request(method: str, url: str, **kwargs) -> Any:
    """安全的aiohttp请求"""
    import aiohttp
    
    timeout = kwargs.pop('timeout', 30)
    
    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as session:
            async with session.request(method, url, **kwargs) as response:
                return await response.text()
    except Exception as e:
        logger.error(f"HTTP请求失败 {method} {url}: {e}")
        raise

# 安全的HTTP请求别名
async def safe_get(url: str, **kwargs) -> str:
    """安全的GET请求"""
    return await safe_aiohttp_request('GET', url, **kwargs)

async def safe_post(url: str, **kwargs) -> str:
    """安全的POST请求"""
    return await safe_aiohttp_request('POST', url, **kwargs)