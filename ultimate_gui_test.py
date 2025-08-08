#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终极GUI显示测试
"""

import sys
import os
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def ultimate_test():
    """终极GUI显示测试"""
    print("🚀 终极GUI显示测试")
    print("=" * 50)
    
    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit
        from PyQt5.QtCore import QTimer
        
        # 创建真实的PyQt应用环境
        app = QApplication(sys.argv)
        
        # 创建真实的GUI组件
        class TestChatWindow(QWidget):
            def __init__(self):
                super().__init__()
                self.received_messages = []
                self.init_ui()
                
            def init_ui(self):
                layout = QVBoxLayout()
                self.text = QTextEdit()
                self.text.append("🧪 测试GUI已创建，等待AI消息...")
                layout.addWidget(self.text)
                self.setLayout(layout)
                self.setWindowTitle("Ultimate GUI Test")
                self.resize(600, 400)
                
            def on_ai_proactive_message(self, message):
                """处理AI主动消息"""
                self.received_messages.append(message)
                print(f"🎯 on_ai_proactive_message 被调用: {message[:50]}...")
                
                # 直接在这里更新UI，不使用QTimer
                try:
                    self.text.append(f"✅ AI消息: {message}")
                    self.text.ensureCursorVisible()
                    print(f"✅ 直接UI更新成功: {message[:30]}...")
                except Exception as e:
                    print(f"❌ 直接UI更新失败: {e}")
                    
            def add_ai_message(self, name, content, message_type="ai_message"):
                """AI消息显示方法"""
                try:
                    self.text.append(f"🤖 {name}: {content} [{message_type}]")
                    self.text.ensureCursorVisible()
                    print(f"✅ add_ai_message成功: {content[:30]}...")
                except Exception as e:
                    print(f"❌ add_ai_message失败: {e}")
        
        # 创建GUI实例
        gui = TestChatWindow()
        gui.show()
        
        # 初始化通知管理器
        from ui.notification_manager import get_notification_manager
        notification_manager = get_notification_manager()
        notification_manager.initialize(gui)
        
        print("📋 真实PyQt环境和通知管理器已初始化")
        
        # 测试消息发送
        test_results = {"success_count": 0, "total_count": 0}
        
        def send_test_message(message, delay):
            def send():
                try:
                    print(f"\n📤 发送测试消息: {message[:30]}...")
                    notification_manager.send_ai_message(message, "happy", "test")
                    test_results["total_count"] += 1
                    
                    # 检查是否成功
                    if len(gui.received_messages) >= test_results["total_count"]:
                        test_results["success_count"] += 1
                        print(f"✅ 消息 {test_results['total_count']} 成功传递")
                    else:
                        print(f"❌ 消息 {test_results['total_count']} 传递失败")
                        
                except Exception as e:
                    print(f"❌ 发送测试消息失败: {e}")
            
            QTimer.singleShot(delay, send)
        
        # 发送多个测试消息
        send_test_message("🌟 Ultimate test message 1", 1000)
        send_test_message("🔍 Ultimate test message 2", 2000)
        send_test_message("🎉 Ultimate test message 3", 3000)
        
        # 5秒后显示结果
        def show_results():
            print(f"\n📊 终极测试结果:")
            print(f"  - 发送消息数: {test_results['total_count']}")
            print(f"  - 成功接收数: {len(gui.received_messages)}")
            print(f"  - 成功率: {len(gui.received_messages)}/{test_results['total_count']}")
            
            print(f"\n📋 接收到的消息:")
            for i, msg in enumerate(gui.received_messages, 1):
                print(f"  {i}. {msg}")
            
            if len(gui.received_messages) >= 3:
                gui.text.append("\n🎉 终极测试成功！AI消息正常显示到GUI")
                print("🎉 终极测试成功！")
            else:
                gui.text.append(f"\n❌ 终极测试失败，只收到 {len(gui.received_messages)} 条消息")
                print("❌ 终极测试失败")
            
            # 再等待2秒后退出
            QTimer.singleShot(2000, app.quit)
        
        QTimer.singleShot(5000, show_results)
        
        print("💡 GUI窗口已打开，测试将自动进行")
        print("   请观察是否有AI消息出现在文本框中")
        
        # 运行应用
        app.exec_()
        
        return len(gui.received_messages) >= 3
        
    except Exception as e:
        print(f"❌ 终极测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = ultimate_test()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 终极GUI测试成功！")
        print("💡 修复完成，AI消息应该能在真实GUI中显示")
        print("   现在可以运行 python main.py 测试完整系统")
    else:
        print("⚠️ 终极GUI测试失败")
        print("💡 可能需要进一步修复GUI更新机制")
    
    # 清理
    try:
        os.remove("ultimate_gui_test.py")
    except:
        pass