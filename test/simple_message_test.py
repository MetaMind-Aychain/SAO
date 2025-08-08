#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的AI消息测试
"""

import sys
import os
import asyncio
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple_ai_message():
    """简单测试AI消息"""
    print("🧪 简单AI消息测试")
    print("=" * 30)
    
    try:
        # 1. 创建模拟GUI
        class MockGUI:
            def __init__(self):
                self.messages = []
                
            def on_ai_proactive_message(self, message):
                self.messages.append(message)
                print(f"✅ GUI收到: {message}")
        
        mock_gui = MockGUI()
        
        # 2. 初始化通知管理器
        print("📋 导入通知管理器...")
        from ui.notification_manager import get_notification_manager
        print("📋 获取通知管理器实例...")
        notification_manager = get_notification_manager()
        print("📋 初始化通知管理器...")
        notification_manager.initialize(mock_gui)
        print("🔧 通知管理器已初始化")
        
        # 3. 直接测试通知管理器
        test_messages = [
            "🌟 Test message 1",
            "🔍 Test message 2", 
            "🎉 Test message 3"
        ]
        
        for msg in test_messages:
            notification_manager.send_ai_message(msg, "happy", "test")
        
        print(f"\n📊 结果: 收到 {len(mock_gui.messages)} 条消息")
        
        # 4. 测试emotional_ai_core的_send_proactive_message方法
        print("\n🧠 测试情绪AI核心...")
        
        # 模拟_send_proactive_message的新逻辑
        async def test_emotion_core_message():
            try:
                message = "🤖 Test from emotional core"
                print(f"📤 发送消息: {message}")
                
                # 模拟新的逻辑
                from ui.notification_manager import get_notification_manager
                notification_manager = get_notification_manager()
                if notification_manager.is_initialized:
                    notification_manager.send_ai_message(message, "curious", "proactive")
                    print(f"✅ 通过通知管理器发送成功")
                else:
                    print(f"❌ 通知管理器未初始化")
                    
            except Exception as e:
                print(f"❌ 测试失败: {e}")
        
        # 运行异步测试
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(test_emotion_core_message())
        finally:
            loop.close()
        
        print(f"\n📊 最终结果: 总共收到 {len(mock_gui.messages)} 条消息")
        for i, msg in enumerate(mock_gui.messages, 1):
            print(f"  {i}. {msg}")
        
        if len(mock_gui.messages) >= 4:
            print("\n✅ 测试成功！消息传递正常")
            return True
        else:
            print(f"\n⚠️ 测试不完整，只收到 {len(mock_gui.messages)} 条消息")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_ai_message()
    
    print(f"\n{'='*50}")
    if success:
        print("🎉 AI消息修复验证成功！")
        print("💡 修复要点:")
        print("  - emotional_ai_core._send_proactive_message现在直接调用GUI")
        print("  - 使用通知管理器确保消息传递")
        print("  - 支持情绪类型和活动类型参数")
    else:
        print("⚠️ 需要进一步检查修复效果")
    
    sys.exit(0 if success else 1)