#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动完整的修复后AI系统
包含：主程序 + AI网站 + 自主交互系统
"""

import asyncio
import threading
import time
import sys
import os

def start_main_app():
    """启动主应用程序"""
    print("启动主程序...")
    try:
        import main
    except Exception as e:
        print(f"主程序启动失败: {e}")

def start_ai_website():
    """启动AI网站"""
    print("启动AI网站...")
    try:
        import uvicorn
        from ai_website.app import app
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8080,
            log_level="info"
        )
    except Exception as e:
        print(f"AI网站启动失败: {e}")

def start_autonomous_system():
    """启动自主交互系统"""
    print("启动自主交互系统...")
    try:
        import asyncio
        from ai_autonomous_interaction import start_autonomous_interaction
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_autonomous_interaction())
    except Exception as e:
        print(f"自主交互系统启动失败: {e}")

if __name__ == "__main__":
    print("========================================")
    print("启动完整的修复后AI系统")
    print("========================================")
    
    # 启动AI网站（后台线程）
    website_thread = threading.Thread(target=start_ai_website, daemon=True)
    website_thread.start()
    print("AI网站已在后台启动 (http://127.0.0.1:8080)")
    
    time.sleep(2)
    
    # 启动自主交互系统（后台线程）
    autonomous_thread = threading.Thread(target=start_autonomous_system, daemon=True)
    autonomous_thread.start()
    print("自主交互系统已在后台启动")
    
    time.sleep(3)
    
    # 启动主程序（前台）
    print("现在启动主程序...")
    start_main_app()