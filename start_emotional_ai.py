#!/usr/bin/env python3
# start_emotional_ai.py
"""
启动情绪化AI系统
整合NagaAgent原有功能与新的情绪AI功能
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
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('emotional_ai.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

def check_dependencies():
    """检查依赖是否安装"""
    required_packages = [
        'PyQt5', 'opencv-python', 'pyaudio', 'speechrecognition',
        'watchdog', 'pillow', 'numpy', 'aiohttp'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"缺少以下依赖包: {', '.join(missing_packages)}")
        logger.info("请运行以下命令安装:")
        logger.info(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_config():
    """检查配置文件"""
    try:
        from config import config
        
        # 检查API密钥
        if not config.api.api_key or config.api.api_key == "sk-placeholder-key-not-set":
            logger.warning("⚠️ API密钥未配置，请在config.json中设置api.api_key")
            logger.warning("⚠️ 某些功能可能无法正常工作")
        
        logger.info("✅ 配置文件检查完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 配置文件检查失败: {e}")
        return False

def start_emotional_ai():
    """启动情绪化AI系统"""
    try:
        logger.info("🚀 启动情绪化NagaAgent系统...")
        
        # 检查依赖
        if not check_dependencies():
            return False
        
        # 检查配置
        if not check_config():
            return False
        
        # 导入并启动情绪化聊天窗口
        from ui.emotional_chat_window import main
        
        logger.info("✅ 启动情绪化聊天界面...")
        main()
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ 导入模块失败: {e}")
        logger.info("💡 请确保所有依赖都已正确安装")
        return False
    except Exception as e:
        logger.error(f"❌ 启动失败: {e}")
        return False

def start_console_mode():
    """启动控制台模式（无GUI）"""
    try:
        logger.info("🖥️ 启动控制台模式...")
        
        # 导入情绪AI管理器
        from emotional_ai.emotional_ai_manager import get_emotional_ai_manager
        
        emotional_ai = get_emotional_ai_manager()
        
        async def console_loop():
            """控制台循环"""
            # 启动情绪AI系统
            await emotional_ai.start_emotional_ai()
            
            print("\n=== 情绪化AI控制台模式 ===")
            print("输入 'quit' 退出")
            print("输入 'status' 查看状态")
            print("输入 'help' 查看帮助")
            print("直接输入文字与AI对话")
            print("=============================\n")
            
            while True:
                try:
                    user_input = input(f"{emotional_ai.ai_name} > ").strip()
                    
                    if user_input.lower() == 'quit':
                        print("再见！")
                        break
                    elif user_input.lower() == 'status':
                        status = emotional_ai.get_system_status()
                        print(f"状态: {status['ai_info']['name']} - {status['emotion_status']['dominant_emotion']['type']}")
                    elif user_input.lower() == 'help':
                        print("可用命令:")
                        print("  quit   - 退出程序")
                        print("  status - 查看AI状态")
                        print("  help   - 显示帮助")
                        print("  其他   - 与AI对话")
                    else:
                        # 处理用户输入
                        response = await emotional_ai.process_user_input(user_input)
                        print(f"{emotional_ai.ai_name}: {response}")
                        
                except KeyboardInterrupt:
                    print("\n程序被中断")
                    break
                except Exception as e:
                    logger.error(f"控制台循环错误: {e}")
            
            # 停止情绪AI系统
            emotional_ai.stop_emotional_ai()
        
        # 运行异步循环
        asyncio.run(console_loop())
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 控制台模式启动失败: {e}")
        return False

def show_help():
    """显示帮助信息"""
    help_text = """
🎭 NagaAgent 情绪化AI系统

使用方法:
  python start_emotional_ai.py          # 启动GUI界面（推荐）
  python start_emotional_ai.py --console # 启动控制台模式
  python start_emotional_ai.py --help    # 显示此帮助

功能特性:
  🎭 情绪系统     - 10种基础情绪，动态变化
  👁️ 感知系统     - 视觉、听觉、屏幕、文件监控
  🤖 主动行为     - AI主动发起对话和互动
  🧠 自动探索     - 自主学习和知识获取
  🎨 个性化界面   - 3岁心理年龄的可爱表达

操作技巧:
  - 表扬夸奖会让AI开心
  - 提问会激发AI的好奇心
  - 邀请游戏会让AI兴奋
  - AI会感知您的活动并主动反应

注意事项:
  - 首次启动需要安装依赖包
  - 需要配置API密钥以使用LLM功能
  - 摄像头和麦克风需要权限授权
    """
    print(help_text)

def main():
    """主函数"""
    try:
        # 解析命令行参数
        if len(sys.argv) > 1:
            arg = sys.argv[1].lower()
            if arg in ['--help', '-h', 'help']:
                show_help()
                return
            elif arg in ['--console', '-c', 'console']:
                success = start_console_mode()
                sys.exit(0 if success else 1)
        
        # 默认启动GUI模式
        success = start_emotional_ai()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序异常退出: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()