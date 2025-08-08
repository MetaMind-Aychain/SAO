#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统启动检查脚本
用于排查和修复系统启动时的各种问题
"""

import sys
import os
import logging
import traceback

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_imports():
    """测试基础模块导入"""
    logger.info("🔧 测试基础模块导入...")
    
    try:
        import asyncio
        logger.info("✅ asyncio导入成功")
    except Exception as e:
        logger.error(f"❌ asyncio导入失败: {e}")
        return False
    
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QObject
        logger.info("✅ PyQt5导入成功")
    except Exception as e:
        logger.error(f"❌ PyQt5导入失败: {e}")
        return False
    
    return True

def test_ui_imports():
    """测试UI相关模块导入"""
    logger.info("🎨 测试UI模块导入...")
    
    try:
        from ui.notification_manager import NotificationManager, get_notification_manager
        logger.info("✅ notification_manager导入成功")
    except Exception as e:
        logger.error(f"❌ notification_manager导入失败: {e}")
        traceback.print_exc()
        return False
    
    try:
        from ui.emotion_panel import EmotionPanel
        logger.info("✅ emotion_panel导入成功")
    except Exception as e:
        logger.error(f"❌ emotion_panel导入失败: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_ai_imports():
    """测试AI相关模块导入"""
    logger.info("🤖 测试AI模块导入...")
    
    try:
        from ai_autonomous_interaction import AIAutonomousInteraction, get_autonomous_interaction
        logger.info("✅ ai_autonomous_interaction导入成功")
    except Exception as e:
        logger.error(f"❌ ai_autonomous_interaction导入失败: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_notification_system():
    """测试通知系统"""
    logger.info("📢 测试通知系统...")
    
    try:
        from ui.notification_manager import get_notification_manager
        
        # 获取通知管理器
        notification_manager = get_notification_manager()
        logger.info("✅ 通知管理器获取成功")
        
        # 测试基本功能（不依赖UI）
        notification_manager.send_ai_message("测试消息", emotion_type="快乐")
        logger.info("✅ 消息发送测试成功")
        
        notification_manager.send_emotion_update("兴奋", 0.8)
        logger.info("✅ 情绪更新测试成功")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 通知系统测试失败: {e}")
        traceback.print_exc()
        return False

def test_ai_system():
    """测试AI系统"""
    logger.info("🧠 测试AI系统...")
    
    try:
        from ai_autonomous_interaction import get_autonomous_interaction
        
        # 获取AI实例
        ai_system = get_autonomous_interaction()
        logger.info("✅ AI自主交互系统获取成功")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ AI系统测试失败: {e}")
        traceback.print_exc()
        return False

async def test_async_notification():
    """测试异步通知功能"""
    logger.info("⚡ 测试异步通知功能...")
    
    try:
        from ai_autonomous_interaction import get_autonomous_interaction
        
        ai_system = get_autonomous_interaction()
        
        # 测试_notify_desktop方法
        await ai_system._notify_desktop(
            "这是一条测试通知",
            emotion_type="快乐", 
            activity_type="testing",
            priority="normal"
        )
        
        logger.info("✅ 异步通知测试成功")
        return True
        
    except Exception as e:
        logger.error(f"❌ 异步通知测试失败: {e}")
        traceback.print_exc()
        return False

def create_safe_startup_script():
    """创建安全启动脚本"""
    logger.info("🛡️ 创建安全启动脚本...")
    
    safe_startup_code = '''#!/usr/bin/env python3
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
'''
    
    try:
        with open('safe_startup.py', 'w', encoding='utf-8') as f:
            f.write(safe_startup_code)
        logger.info("✅ 安全启动脚本创建成功: safe_startup.py")
        return True
    except Exception as e:
        logger.error(f"❌ 创建安全启动脚本失败: {e}")
        return False

async def main():
    """主测试函数"""
    logger.info("🌟 开始系统启动检查...")
    
    # 基础测试
    if not test_basic_imports():
        logger.error("❌ 基础模块导入测试失败")
        return False
    
    if not test_ui_imports():
        logger.error("❌ UI模块导入测试失败")
        return False
    
    if not test_ai_imports():
        logger.error("❌ AI模块导入测试失败")
        return False
    
    # 功能测试
    if not test_notification_system():
        logger.error("❌ 通知系统测试失败")
        return False
    
    if not test_ai_system():
        logger.error("❌ AI系统测试失败")
        return False
    
    # 异步测试
    if not await test_async_notification():
        logger.error("❌ 异步通知测试失败")
        return False
    
    # 创建安全启动脚本
    create_safe_startup_script()
    
    logger.info("🎉 所有测试通过！系统应该可以正常启动。")
    
    print("\\n" + "="*60)
    print("🔧 如果仍然遇到问题，请尝试:")
    print("="*60)
    print("1. 使用安全启动脚本: python safe_startup.py")
    print("2. 检查启动日志: startup.log")
    print("3. 确保所有依赖都已安装")
    print("4. 检查Python版本兼容性")
    print("="*60)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 检查被用户中断")
    except Exception as e:
        logger.error(f"❌ 检查运行失败: {e}")
        traceback.print_exc()