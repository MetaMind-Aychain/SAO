#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
干净启动脚本 - 确保系统正常启动，无重复初始化
"""

import os
import sys
import logging
import time

# 设置日志级别，减少重复信息
logging.basicConfig(level=logging.WARNING)

# 设置特定模块的日志级别
for logger_name in ['VoiceIntegration', 'emotional_ai_core', 'advanced_perception_system', 'ai_memory_system']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

def main():
    print("🌟 StarryNightAI - 干净启动")
    print("=" * 60)
    
    try:
        # 导入核心模块
        print("📍 加载配置...")
        from config import config
        
        print("📍 启动核心AI系统...")
        from main import get_global_naga_instance
        
        # 获取AI实例
        ai_instance = get_global_naga_instance()
        print("✅ AI核心系统启动完成")
        
        print("📍 启动AI展示网站...")
        import threading
        import uvicorn
        from ai_website.app import app
        
        def run_website():
            uvicorn.run(app, host="0.0.0.0", port=8001, log_level="error")
        
        website_thread = threading.Thread(target=run_website, daemon=True)
        website_thread.start()
        print("✅ AI展示网站已启动: http://localhost:8001")
        
        print("📍 启动自主交互系统...")
        def run_autonomous():
            try:
                import asyncio
                from ai_autonomous_interaction import start_autonomous_interaction
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(start_autonomous_interaction())
            except Exception as e:
                print(f"⚠️ 自主交互系统启动失败: {e}")
        
        autonomous_thread = threading.Thread(target=run_autonomous, daemon=True)
        autonomous_thread.start()
        print("✅ AI自主交互系统已启动")
        
        print("\n" + "=" * 60)
        print("🎉 StarryNightAI系统启动完成！")
        print("=" * 60)
        print("🌐 AI展示网站: http://localhost:8001")
        print("🤖 AI桌面交互: 输入文字与AI对话")
        print("📊 API文档: http://127.0.0.1:8000/docs")
        print("=" * 60)
        
        # 简单的交互循环
        print("\n💬 与StarryNight对话 (输入 'quit' 退出):")
        while True:
            try:
                user_input = input("\n👤 你: ")
                if user_input.lower() in ['quit', 'exit', '退出']:
                    break
                
                if user_input.strip():
                    print("🌟 StarryNight: 正在思考...")
                    response = ai_instance.generate_response(user_input)
                    print(f"🌟 StarryNight: {response}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"⚠️ 对话错误: {e}")
        
        print("\n👋 再见！StarryNight期待下次与你对话～")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()