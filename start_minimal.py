#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小化启动脚本 - 避免重复初始化
只启动核心功能，避免多次重复初始化问题
"""

import os
import sys
import time
import threading
import logging
from pathlib import Path

# 设置日志级别，减少噪音
logging.basicConfig(level=logging.WARNING)
for logger_name in ['VoiceIntegration', 'emotional_ai_core', 'advanced_perception_system']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

def main():
    """最小化启动主程序"""
    print("🌟 StarryNightAI - 最小化启动")
    print("=" * 50)
    
    try:
        # 只导入必要的模块
        print("📍 导入核心模块...")
        from config import config
        
        print("📍 初始化主AI实例...")
        from main import get_global_naga_instance
        
        # 获取AI实例（应该只初始化一次）
        ai_instance = get_global_naga_instance()
        print("✅ AI实例初始化完成")
        
        # 测试AI是否正常工作
        print("📍 测试AI功能...")
        response = ai_instance.generate_response("你好，测试一下")
        print(f"🤖 AI回复: {response[:50]}...")
        
        # 可选：启动网站
        start_website = input("是否启动AI展示网站？(y/n): ").lower() == 'y'
        
        if start_website:
            print("🌐 启动AI展示网站...")
            
            def run_website():
                try:
                    import uvicorn
                    from ai_website.app import app
                    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="error")
                except Exception as e:
                    print(f"❌ 网站启动失败: {e}")
            
            website_thread = threading.Thread(target=run_website, daemon=True)
            website_thread.start()
            print("✅ 网站已启动: http://localhost:8001")
            
            # 保持程序运行
            print("🔄 系统运行中，按 Ctrl+C 退出...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 程序退出")
        else:
            print("✅ 最小化启动完成")
            
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()