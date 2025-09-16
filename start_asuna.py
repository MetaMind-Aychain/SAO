#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动Alice Synthesis AI系统
专门为Asuna角色优化的启动脚本
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/asuna_startup.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

def check_asuna_dependencies():
    """检查Asuna系统依赖"""
    try:
        # 检查必要的模块
        required_modules = [
            'asuna_character_system',
            'asuna_memory_system', 
            'asuna_language_system',
            'asuna_autonomous_behavior',
            'asuna_integration'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            logger.error(f"缺少Asuna系统模块: {missing_modules}")
            return False
        
        logger.info("Asuna系统依赖检查通过")
        return True
        
    except Exception as e:
        logger.error(f"检查Asuna依赖失败: {e}")
        return False

def initialize_asuna_config():
    """初始化Asuna配置"""
    try:
        from config import config
        
        # 确保Asuna配置已启用
        if not config.emotional_ai.asuna_enabled:
            logger.warning("Asuna功能未启用，正在启用...")
            config.emotional_ai.asuna_enabled = True
            config.emotional_ai.asuna_memory_stage = "anxious"
            config.emotional_ai.asuna_sao_elements = True
            config.emotional_ai.asuna_autonomous_behavior = True
        
        logger.info("Asuna配置初始化完成")
        return True
        
    except Exception as e:
        logger.error(f"初始化Asuna配置失败: {e}")
        return False

def start_asuna_gui():
    """启动Asuna GUI界面"""
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.emotional_chat_window import EmotionalChatWindow
        
        # 创建应用程序
        app = QApplication(sys.argv)
        app.setApplicationName("Alice Synthesis AI助手")
        app.setApplicationVersion("3.0")
        
        # 设置Asuna主题
        app.setStyleSheet("""
            QMainWindow {
                background-color: #1a0f1a;
            }
            QWidget {
                color: #FFE6F3;
                background-color: #2a1a2a;
            }
            QPushButton {
                background-color: rgba(255, 107, 138, 120);
                border: 2px solid #FF6B8A;
                border-radius: 5px;
                padding: 8px;
                color: #FFE6F3;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 138, 155, 150);
            }
            QTextEdit {
                background-color: #1a0f1a;
                border: 1px solid #FF6B8A;
                border-radius: 5px;
                color: #FFE6F3;
            }
        """)
        
        # 创建并显示窗口
        window = EmotionalChatWindow()
        window.setWindowTitle("⚔️ Alice Synthesis AI助手 - 记忆恢复中...")
        
        # 居中显示
        from PyQt5.QtWidgets import QDesktopWidget
        desktop = QDesktopWidget()
        screen_rect = desktop.screenGeometry()
        window_rect = window.geometry()
        x = (screen_rect.width() - window_rect.width()) // 2
        y = (screen_rect.height() - window_rect.height()) // 2
        window.move(x, y)
        
        window.show()
        
        logger.info("Asuna GUI界面启动成功")
        return app.exec_()
        
    except Exception as e:
        logger.error(f"启动Asuna GUI失败: {e}")
        return 1

def start_asuna_console():
    """启动Asuna控制台模式"""
    try:
        from conversation_core import ConversationCore
        from config import config
        
        async def console_main():
            # 创建对话核心
            conversation_core = ConversationCore()
            
            print("=" * 60)
            print("⚔️ Alice Synthesis AI助手 - 控制台模式")
            print("=" * 60)
            print("Asuna正在恢复记忆中...")
            print("输入 'exit' 或 'quit' 退出")
            print("=" * 60)
            
            while True:
                try:
                    user_input = input("\n你: ").strip()
                    
                    if user_input.lower() in ['exit', 'quit', '退出']:
                        print("Asuna: 再见...我会想念你的...")
                        break
                    
                    if not user_input:
                        continue
                    
                    # 处理用户输入
                    response = await conversation_core.process(user_input)
                    print(f"Asuna: {response}")
                    
                except KeyboardInterrupt:
                    print("\nAsuna: 你要离开了吗...")
                    break
                except Exception as e:
                    print(f"错误: {e}")
        
        # 运行控制台模式
        asyncio.run(console_main())
        return 0
        
    except Exception as e:
        logger.error(f"启动Asuna控制台失败: {e}")
        return 1

def main():
    """主函数"""
    try:
        print("=" * 60)
        print("⚔️ 启动Alice Synthesis AI系统")
        print("=" * 60)
        
        # 检查依赖
        if not check_asuna_dependencies():
            print("❌ Asuna系统依赖检查失败")
            return 1
        
        # 初始化配置
        if not initialize_asuna_config():
            print("❌ Asuna配置初始化失败")
            return 1
        
        print("✅ Asuna系统准备就绪")
        
        # 选择启动模式
        if len(sys.argv) > 1 and sys.argv[1] == '--console':
            print("启动控制台模式...")
            return start_asuna_console()
        else:
            print("启动GUI模式...")
            return start_asuna_gui()
            
    except Exception as e:
        logger.error(f"启动Asuna系统失败: {e}")
        print(f"❌ 启动失败: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())



