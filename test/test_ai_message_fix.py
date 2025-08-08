#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI消息修复效果
"""

import sys
import os
import asyncio
import time
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置日志级别
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_ai_message_display_fix():
    """测试AI消息显示修复"""
    print("🔧 测试AI消息显示修复")
    print("=" * 50)
    
    try:
        # 1. 创建模拟GUI
        class MockGUI:
            def __init__(self):
                self.received_messages = []
                self.proactive_messages = []
                
            def on_ai_proactive_message(self, message):
                """接收AI主动消息"""
                self.proactive_messages.append(message)
                print(f"🤖 GUI收到主动消息: {message}")
                
            def add_ai_message(self, name, content, message_type="ai_message"):
                """AI消息显示方法"""
                self.received_messages.append((name, content, message_type))
                print(f"💬 GUI显示AI消息: {name} - {content}")
        
        mock_gui = MockGUI()
        
        # 2. 初始化通知管理器
        print("📋 初始化通知管理器...")
        from ui.notification_manager import get_notification_manager
        notification_manager = get_notification_manager()
        notification_manager.initialize(mock_gui)
        print("✅ 通知管理器初始化完成")
        
        # 3. 获取情绪AI核心
        print("\n📋 获取情绪AI核心...")
        from emotional_ai_core import EmotionalCore
        from config import load_config
        config = load_config()
        emotion_core = EmotionalCore(config.emotional_ai if hasattr(config, 'emotional_ai') else config)
        print("✅ 情绪AI核心获取成功")
        
        # 4. 测试_send_proactive_message方法
        print("\n📋 测试_send_proactive_message方法...")
        
        async def test_proactive_messages():
            """测试主动消息发送"""
            test_messages = [
                "🌟 Hello! I'm testing the fixed message display system!",
                "🔍 Now I can properly send messages to the GUI interface!",
                "🎉 This should appear directly in the chat window!",
                "💭 The fix allows all AI autonomous messages to be displayed!",
                "✨ No more missing messages in the GUI!"
            ]
            
            for i, message in enumerate(test_messages, 1):
                print(f"📤 发送测试消息 {i}: {message[:40]}...")
                await emotion_core._send_proactive_message(message)
                await asyncio.sleep(1)  # 等待处理
        
        # 运行异步测试
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(test_proactive_messages())
        finally:
            loop.close()
        
        # 5. 检查结果
        print(f"\n📊 测试结果:")
        print(f"  - 主动消息收到数量: {len(mock_gui.proactive_messages)}")
        print(f"  - 所有消息收到数量: {len(mock_gui.received_messages)}")
        
        print(f"\n📋 收到的主动消息列表:")
        for i, msg in enumerate(mock_gui.proactive_messages, 1):
            print(f"  {i}. {msg}")
        
        # 6. 验证修复效果
        if len(mock_gui.proactive_messages) >= 5:
            print("\n✅ 修复成功！AI消息现在可以正确显示在GUI上")
            return True
        else:
            print(f"\n❌ 修复可能有问题，只收到了 {len(mock_gui.proactive_messages)} 条消息")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ai_message_display_fix()
    
    if success:
        print(f"\n🎉 AI消息显示修复验证成功！")
        print("💡 现在运行 python main.py 启动完整系统")
        print("   AI的所有自主行为消息都会显示在GUI聊天界面上")
    else:
        print(f"\n⚠️ 修复验证失败，需要进一步检查")
    
    # 清理
    try:
        from async_manager import cleanup_all_async_resources
        asyncio.run(cleanup_all_async_resources())
    except:
        pass
    
    sys.exit(0 if success else 1)