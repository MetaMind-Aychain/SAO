#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试main.py中的GUI连接是否正常
"""

import sys
import os
import time
import threading

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_main_gui_connection():
    """测试main.py的GUI连接"""
    print("🧪 测试main.py的GUI连接")
    print("=" * 50)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QTimer
        
        # 创建应用
        app = QApplication(sys.argv)
        
        # 导入ChatWindow
        from ui.pyqt_chat_window import ChatWindow
        win = ChatWindow()
        win.setWindowTitle("Test StarryNight AGENT")
        
        # 添加连接计数器
        connection_status = {"connected": False, "test_message_received": False}
        
        # 重写on_ai_proactive_message来跟踪消息
        original_method = win.on_ai_proactive_message
        def tracked_on_ai_proactive_message(message):
            print(f"🎯 ChatWindow.on_ai_proactive_message 被调用: {message[:50]}...")
            if "AI autonomous interaction system connected" in message:
                connection_status["test_message_received"] = True
                print("✅ 检测到连接测试消息！")
            original_method(message)
        
        win.on_ai_proactive_message = tracked_on_ai_proactive_message
        
        # 模拟main.py中的延迟连接逻辑
        def delayed_connect_ai():
            time.sleep(2)  # 等待GUI完全初始化
            try:
                from ui.notification_manager import get_notification_manager
                from ai_autonomous_interaction import get_autonomous_interaction
                
                print("🔄 开始连接AI到GUI...")
                
                # 重新初始化通知管理器，连接到GUI
                notification_manager = get_notification_manager()
                notification_manager.initialize(win)
                connection_status["connected"] = True
                
                # 确保AI系统知道GUI已准备好
                ai_system = get_autonomous_interaction()
                print(f"🔗 AI自主交互系统已连接到GUI: {type(win).__name__}")
                
                # 发送测试消息验证连接
                print("📤 发送连接测试消息...")
                notification_manager.send_ai_message("🌟 AI autonomous interaction system connected to GUI successfully!", "happy", "system")
                
                print("✅ AI-GUI连接流程完成")
                
            except Exception as e:
                print(f"❌ AI-GUI连接失败: {e}")
                import traceback
                traceback.print_exc()
        
        # 在后台线程中延迟连接（模拟main.py）
        connection_thread = threading.Thread(target=delayed_connect_ai, daemon=True)
        connection_thread.start()
        
        win.show()
        
        # 5秒后检查结果
        def check_results():
            print(f"\n📊 连接测试结果:")
            print(f"  - 通知管理器已连接: {connection_status['connected']}")
            print(f"  - 测试消息已接收: {connection_status['test_message_received']}")
            
            if connection_status["connected"] and connection_status["test_message_received"]:
                print("✅ AI-GUI连接测试成功！")
                print("💡 main.py的连接逻辑是正常的")
            else:
                print("❌ AI-GUI连接测试失败")
                if not connection_status["connected"]:
                    print("  - 通知管理器连接失败")
                if not connection_status["test_message_received"]:
                    print("  - 测试消息未接收到")
            
            # 再发送一个手动测试消息
            try:
                from ui.notification_manager import get_notification_manager
                notification_manager = get_notification_manager()
                print("\n📤 发送额外测试消息...")
                notification_manager.send_ai_message("🔍 Additional test message for verification", "curious", "test")
            except Exception as e:
                print(f"❌ 额外测试消息发送失败: {e}")
        
        QTimer.singleShot(5000, check_results)
        
        # 10秒后退出
        QTimer.singleShot(10000, app.quit)
        
        print("💡 GUI窗口已打开，测试将在5秒后显示结果")
        print("   如果看到AI消息出现在聊天界面，说明连接正常")
        
        # 运行应用
        app.exec_()
        
        return connection_status["connected"] and connection_status["test_message_received"]
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_main_gui_connection()
    
    if success:
        print("\n🎉 main.py的GUI连接测试成功！")
        print("💡 问题可能在于AI自主行为的触发时机或其他地方")
    else:
        print("\n⚠️ main.py的GUI连接有问题，需要进一步修复")
    
    # 清理
    try:
        os.remove("test_main_gui_connection.py")
    except:
        pass