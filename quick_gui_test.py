#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速GUI修复测试
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def quick_test():
    """快速测试修复效果"""
    print("⚡ 快速GUI修复测试")
    print("=" * 30)
    
    try:
        # 创建简化的测试GUI
        class QuickTestGUI:
            def __init__(self):
                self.messages = []
                self.text = MockTextWidget()
                
            def on_ai_proactive_message(self, message):
                self.messages.append(message)
                print(f"✅ on_ai_proactive_message: {message}")
        
        class MockTextWidget:
            def __init__(self):
                self.content = []
                
            def append(self, text):
                self.content.append(text)
                print(f"✅ text.append: {text}")
                
            def ensureCursorVisible(self):
                print("✅ ensureCursorVisible called")
        
        gui = QuickTestGUI()
        
        # 初始化通知管理器
        from ui.notification_manager import get_notification_manager
        notification_manager = get_notification_manager()
        notification_manager.initialize(gui)
        
        # 发送测试消息
        print("\n📤 发送测试消息...")
        notification_manager.send_ai_message("🌟 Quick test message!", "happy", "test")
        
        # 检查结果
        print(f"\n📊 结果:")
        print(f"  - GUI消息数量: {len(gui.messages)}")
        print(f"  - Text widget内容数量: {len(gui.text.content)}")
        
        if len(gui.messages) > 0 or len(gui.text.content) > 0:
            print("✅ 修复成功！消息能够到达GUI")
            return True
        else:
            print("❌ 修复失败，消息未到达GUI")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    
    if success:
        print("\n🎉 快速测试通过！")
        print("💡 现在启动 python main.py 测试实际效果")
    else:
        print("\n⚠️ 快速测试失败，需要进一步排查")
    
    # 清理
    try:
        os.remove("quick_gui_test.py")
    except:
        pass