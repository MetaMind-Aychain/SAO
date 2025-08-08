#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地LLM快速启动脚本
避免复杂的高级功能初始化，专注于基础对话功能
"""

import os
import sys
import asyncio
import logging

def setup_minimal_environment():
    """设置最小化环境，禁用可能有问题的功能"""
    # 禁用一些高级功能以避免初始化错误
    os.environ["NAGAAGENT_MINIMAL_MODE"] = "1"
    os.environ["DISABLE_ADVANCED_PERCEPTION"] = "1"
    os.environ["DISABLE_SOCIAL_MEDIA"] = "1"
    
    # 设置日志级别，减少噪音
    logging.basicConfig(level=logging.WARNING)

async def test_basic_functionality():
    """测试基础功能"""
    print("🧪 测试基础对话功能...")
    
    try:
        from conversation_core import NagaConversation
        from config import config
        
        print(f"📡 API配置: {config.api.base_url}")
        print(f"🔑 模型: {config.api.model}")
        
        # 创建对话实例（最小化配置）
        naga = NagaConversation()
        
        # 测试简单对话
        test_message = "你好，请简单回复"
        
        print(f"💬 发送测试消息: {test_message}")
        
        response_text = ""
        async for response in naga.process(test_message):
            if response[0] == "StarryNight":
                response_text += response[1] + "\n"
        
        if response_text.strip():
            print(f"✅ 对话成功: {response_text.strip()}")
            return True
        else:
            print("❌ 没有收到有效回复")
            return False
            
    except Exception as e:
        print(f"❌ 基础功能测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 NagaAgent 本地LLM快速启动")
    print("=" * 40)
    
    # 设置最小化环境
    setup_minimal_environment()
    
    try:
        # Windows事件循环策略
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        # 测试基础功能
        success = asyncio.run(test_basic_functionality())
        
        if success:
            print("\n🎉 基础功能测试成功！")
            print("💡 现在可以尝试启动完整系统:")
            print("   python main.py")
        else:
            print("\n❌ 基础功能测试失败")
            print("💡 请检查本地LLM服务是否正常运行")
            print("   确保服务地址: http://localhost:11434")
            
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")

if __name__ == "__main__":
    main()