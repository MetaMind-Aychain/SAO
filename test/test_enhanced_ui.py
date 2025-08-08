#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试增强的科幻风格界面
90%不透明度 + 毛玻璃效果
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

def test_enhanced_ui():
    """测试增强的科幻风格界面"""
    print("🎨 测试StarryNight AGENT增强科幻界面")
    print("=" * 50)
    
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
        window.setWindowTitle("StarryNight AGENT - 科幻星际界面")
        
        print("✅ 增强界面创建成功")
        print("🌟 全新科幻特性:")
        print("   - 透明度: 90% (毛玻璃质感)")
        print("   - 配色方案: 深空蓝紫主调")
        print("   - 边框效果: 发光科幻边框")
        print("   - 滚动条: 星际蓝渐变")
        print("   - 进度条: 蓝紫渐变效果")
        print("   - 文字颜色: 星光蓝白色调")
        print("   - 背景模糊: 高级毛玻璃效果")
        
        # 显示窗口
        window.show()
        
        print("\n💫 科幻界面预览已启动！")
        print("🌌 视觉特色:")
        print("   • 深空背景色 rgba(15,25,45)")
        print("   • 星际蓝边框 rgba(150,200,255)")
        print("   • 银河紫按钮 #9966FF")
        print("   • 星光文字 #E6F3FF")
        print("   • 毛玻璃模糊效果")
        print("\n💡 按 Ctrl+C 或关闭窗口退出")
        
        # 运行应用
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请确保所有依赖已安装")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    test_enhanced_ui()