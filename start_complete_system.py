#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整AI系统启动脚本
启动所有组件：主程序、网站、自主交互系统、测试
"""

import asyncio
import threading
import time
import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_main_system():
    """启动主AI系统"""
    logger.info("🚀 启动主AI系统...")
    try:
        import main
        # 这里主程序会启动UI，在测试模式下我们跳过UI
        logger.info("✅ 主AI系统启动完成")
    except Exception as e:
        logger.error(f"❌ 主AI系统启动失败: {e}")

def start_website():
    """启动AI网站"""
    logger.info("🌐 启动AI展示网站...")
    try:
        import uvicorn
        from ai_website.app import app
        
        # 启动网站服务器
        uvicorn.run(app, host="0.0.0.0", port=8001, log_level="warning")
    except Exception as e:
        logger.error(f"❌ AI网站启动失败: {e}")

def start_autonomous_system():
    """启动自主交互系统"""
    logger.info("🤖 启动AI自主交互系统...")
    try:
        import asyncio
        from ai_autonomous_interaction import start_autonomous_interaction
        
        # 创建事件循环并运行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_autonomous_interaction())
    except Exception as e:
        logger.error(f"❌ 自主交互系统启动失败: {e}")

def run_tests():
    """运行系统测试"""
    logger.info("🧪 等待系统启动后运行测试...")
    time.sleep(15)  # 等待其他组件启动
    
    try:
        import asyncio
        from test_ai_autonomous_system import main as test_main
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(test_main())
    except Exception as e:
        logger.error(f"❌ 测试运行失败: {e}")

def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("🌟 StarryNightAI完整系统启动")
    logger.info("=" * 60)
    
    # 创建并启动各个组件的线程
    threads = []
    
    # 1. 启动网站服务器
    website_thread = threading.Thread(target=start_website, daemon=True)
    website_thread.start()
    threads.append(website_thread)
    logger.info("🌐 AI网站启动线程已启动")
    
    # 2. 启动自主交互系统
    autonomous_thread = threading.Thread(target=start_autonomous_system, daemon=True)
    autonomous_thread.start()
    threads.append(autonomous_thread)
    logger.info("🤖 自主交互系统启动线程已启动")
    
    # 3. 启动测试
    test_thread = threading.Thread(target=run_tests, daemon=True)
    test_thread.start()
    threads.append(test_thread)
    logger.info("🧪 测试线程已启动")
    
    # 等待一段时间观察系统运行
    logger.info("⏳ 系统运行中，60秒后自动退出...")
    
    try:
        time.sleep(60)
        logger.info("⏰ 测试时间结束")
    except KeyboardInterrupt:
        logger.info("⚠️ 用户中断")
    
    logger.info("🔚 系统测试完成")

if __name__ == "__main__":
    main()