#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试语法错误修复
"""

import sys
import os

def test_imports():
    """测试所有关键模块的导入"""
    print("🔧 测试语法错误修复")
    print("=" * 50)
    
    try:
        # 测试 config.py 导入
        print("📋 测试 config.py...")
        from config import SystemPrompts
        print("✅ config.py 导入成功")
        
        # 测试 elegant_settings_widget.py 导入
        print("📋 测试 elegant_settings_widget.py...")
        from ui.elegant_settings_widget import ElegantSettingsWidget
        print("✅ elegant_settings_widget.py 导入成功")
        
        # 测试 pyqt_chat_window.py 导入
        print("📋 测试 pyqt_chat_window.py...")
        from ui.pyqt_chat_window import ChatWindow
        print("✅ pyqt_chat_window.py 导入成功")
        
        # 测试 main.py 导入
        print("📋 测试 main.py...")
        import main
        print("✅ main.py 导入成功")
        
        print("\n" + "=" * 50)
        print("🎉 所有语法错误已修复！")
        print("✅ 系统可以正常启动")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 