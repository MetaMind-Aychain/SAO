#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试真实GUI环境下的信号传递
"""

import sys
import os
import time
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_real_gui_signals():
    """测试真实GUI环境下的信号传递"""
    print("🧪 测试真实GUI信号传递")
    print("=" * 50)
    
    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
        from PyQt5.QtCore import QTimer
        
        # 创建应用
        app = QApplication(sys.argv)
        
        # 创建简化的GUI类
        class TestGUI(QWidget):
            def __init__(self):
                super().__init__()
                self.received_messages = []
                self.init_ui()
                
            def init_ui(self):
                layout = QVBoxLayout()
                self.text_area = QTextEdit()
                self.text_area.append("🧪 测试GUI已启动，等待AI消息...")
                layout.addWidget(self.text_area)
                
                # 添加测试按钮
                test_btn = QPushButton("发送测试消息")
                test_btn.clicked.connect(self.send_test_message)
                layout.addWidget(test_btn)
                
                self.setLayout(layout)
                self.setWindowTitle("AI消息测试GUI")
                self.resize(500, 300)
            
            def on_ai_proactive_message(self, message: str):
                """处理AI主动消息"""
                self.received_messages.append(message)
                self.text_area.append(f"✅ 收到AI消息: {message}")
                print(f"✅ GUI收到AI消息: {message}")
                
            def add_ai_message(self, name, content, message_type="ai_message"):
                """AI消息显示方法"""
                self.text_area.append(f"💬 {name}: {content} [{message_type}]")
                print(f"💬 add_ai_message被调用: {name} - {content} [{message_type}]")
            
            def send_test_message(self):
                """发送测试消息"""
                try:
                    from ui.notification_manager import get_notification_manager
                    notification_manager = get_notification_manager()
                    notification_manager.send_ai_message("🌟 Test message from button click!", "happy", "manual")
                    self.text_area.append("📤 手动发送测试消息")
                except Exception as e:
                    self.text_area.append(f"❌ 发送失败: {e}")
        
        # 创建GUI实例
        gui = TestGUI()
        gui.show()
        
        # 初始化通知管理器
        from ui.notification_manager import get_notification_manager
        notification_manager = get_notification_manager()
        notification_manager.initialize(gui)
        
        print("📋 通知管理器已初始化")
        
        # 定时发送测试消息
        def send_auto_messages():
            try:
                messages = [
                    "🌟 Auto test message 1",
                    "🔍 Auto test message 2", 
                    "🎉 Auto test message 3"
                ]
                
                for i, msg in enumerate(messages):
                    QTimer.singleShot(2000 + i * 1000, lambda m=msg: send_single_message(m))
                
                # 5秒后显示统计
                QTimer.singleShot(6000, show_statistics)
                
            except Exception as e:
                print(f"❌ 定时消息发送失败: {e}")
        
        def send_single_message(msg):
            try:
                print(f"📤 发送自动消息: {msg}")
                notification_manager.send_ai_message(msg, "curious", "auto")
            except Exception as e:
                print(f"❌ 单条消息发送失败: {e}")
        
        def show_statistics():
            print(f"\n📊 测试统计:")
            print(f"  - GUI收到消息数量: {len(gui.received_messages)}")
            for i, msg in enumerate(gui.received_messages, 1):
                print(f"    {i}. {msg}")
            
            if len(gui.received_messages) >= 3:
                gui.text_area.append("\n✅ 信号传递测试成功！")
                print("✅ 信号传递测试成功！")
            else:
                gui.text_area.append(f"\n❌ 信号传递有问题，只收到 {len(gui.received_messages)} 条消息")
                print(f"❌ 信号传递有问题，只收到 {len(gui.received_messages)} 条消息")
        
        # 2秒后开始自动测试
        QTimer.singleShot(2000, send_auto_messages)
        
        print("💡 GUI窗口已打开")
        print("   - 2秒后开始自动发送测试消息")
        print("   - 也可以点击按钮手动发送")
        print("   - 关闭窗口或按Ctrl+C退出")
        
        # 运行应用
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ GUI测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_gui_signals()