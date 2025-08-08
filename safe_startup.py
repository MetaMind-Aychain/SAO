#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全启动脚本 - 带完整异常处理
"""

import sys
import os
import logging
import traceback

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('startup.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(__name__)

def safe_import(module_name, package=None):
    """安全导入模块"""
    try:
        if package:
            module = __import__(module_name, fromlist=[package])
            return getattr(module, package)
        else:
            return __import__(module_name)
    except Exception as e:
        logger.error(f"导入模块失败 {module_name}: {e}")
        traceback.print_exc()
        return None

def main():
    """安全启动主函数"""
    global logger
    logger = setup_logging()
    logger.info("🚀 开始安全启动...")
    
    try:
        # 测试基础导入
        logger.info("导入基础模块...")
        PyQt5 = safe_import('PyQt5.QtWidgets')
        if not PyQt5:
            logger.error("PyQt5导入失败，无法启动UI")
            return False
            
        # 导入UI组件
        logger.info("导入UI组件...")
        from ui.pyqt_chat_window import ChatWindow
        
        # 导入AI组件  
        logger.info("导入AI组件...")
        from ai_autonomous_interaction import get_autonomous_interaction
        
        # 启动应用
        logger.info("启动应用...")
        app = PyQt5.QApplication(sys.argv)
        
        try:
            window = ChatWindow()
            window.show()
            logger.info("✅ UI启动成功")
            
            # 启动AI系统（可选）
            # ai_system = get_autonomous_interaction()
            # logger.info("✅ AI系统初始化成功")
            
            sys.exit(app.exec_())
            
        except Exception as e:
            logger.error(f"UI启动失败: {e}")
            traceback.print_exc()
            return False
            
    except Exception as e:
        logger.error(f"启动失败: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
