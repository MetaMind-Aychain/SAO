#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 直接测试AI消息修复")

# 1. 创建模拟GUI
class MockGUI:
    def __init__(self):
        self.messages = []
        
    def on_ai_proactive_message(self, message):
        self.messages.append(message)
        print(f"✅ GUI收到: {message}")

mock_gui = MockGUI()
print("📋 模拟GUI创建完成")

# 2. 测试通知管理器
try:
    from ui.notification_manager import get_notification_manager
    print("📋 通知管理器导入成功")
    
    notification_manager = get_notification_manager()
    print("📋 通知管理器实例获取成功")
    
    notification_manager.initialize(mock_gui)
    print("📋 通知管理器初始化完成")
    
    # 发送测试消息
    notification_manager.send_ai_message("🌟 Test message!", "happy", "test")
    print("📋 测试消息发送完成")
    
    print(f"📊 GUI收到消息数量: {len(mock_gui.messages)}")
    
    for msg in mock_gui.messages:
        print(f"  - {msg}")
        
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("🏁 测试完成")