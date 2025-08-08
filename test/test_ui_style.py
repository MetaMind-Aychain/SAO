#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试UI样式修改效果
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

def test_ui_style():
    """测试UI样式"""
    print("🎨 测试StarryNight AGENT界面样式")
    print("=" * 40)
    
    try:
        # 导入主界面
        from ui.pyqt_chat_window import ChatWindow
        
        # 创建应用
        app = QApplication(sys.argv)
        
        # 设置图标
        icon_path = os.path.join(os.path.dirname(__file__), "ui", "window_icon.png")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
        
        # 创建窗口
        window = ChatWindow()
        window.setWindowTitle("StarryNight AGENT - 样式测试")
        
        print("✅ 界面创建成功")
        print("🌟 新样式特性:")
        print("   - 标题: StarryNight AGENT")
        print("   - AI名称: StarryNight") 
        print("   - 透明度: 20%")
        print("   - 配色: 科幻蓝白紫主调")
        print("   - 按钮: 科幻风格渐变色")
        
        # 显示窗口
        window.show()
        
        print("\n💡 界面预览已启动，检查样式效果...")
        print("   按 Ctrl+C 或关闭窗口退出")
        
        # 运行应用
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请确保所有依赖已安装")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    test_ui_style()