import asyncio
import os
import sys
import threading
import time
import logging

# 在导入其他模块前先设置HTTP库日志级别
logging.getLogger("httpcore.http11").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore.connection").setLevel(logging.WARNING)

from conversation_core import NagaConversation

sys.path.append(os.path.dirname(__file__))
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

# 导入配置
from config import config
from summer_memory.memory_manager import memory_manager
from ui.pyqt_chat_window import ChatWindow

# 严格的全局单例管理
_global_naga_instance = None
_initialization_lock = threading.Lock()
_initialization_complete = False

def get_global_naga_instance():
    """获取全局NagaConversation实例（严格单例模式）"""
    global _global_naga_instance, _initialization_complete
    
    if _initialization_complete and _global_naga_instance is not None:
        return _global_naga_instance
    
    with _initialization_lock:
        # 双重检查锁定模式
        if _global_naga_instance is None and not _initialization_complete:
            print("🚀 正在初始化全局AI实例（严格单例）...")
            _global_naga_instance = NagaConversation()
            _initialization_complete = True
            print("✅ 全局AI实例初始化完成，已锁定")
        elif _global_naga_instance is not None:
            print("⚠️ 检测到重复初始化尝试，返回现有实例")
    
    return _global_naga_instance
def show_help():print('系统命令: 清屏, 查看索引, 帮助, 退出')
def show_index():print('主题分片索引已集成，无需单独索引查看')
def clear():os.system('cls' if os.name == 'nt' else 'clear')

def check_port_available(host, port):
    """检查端口是否可用"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            return True
    except OSError:
        return False

def start_api_server():
    """在后台启动API服务器"""
    try:
        # 检查端口是否被占用
        if not check_port_available(config.api_server.host, config.api_server.port):
            print(f"⚠️ 端口 {config.api_server.port} 已被占用，跳过API服务器启动")
            return
            
        import uvicorn
        # 使用字符串路径而不是直接导入，确保模块重新加载
        # from apiserver.api_server import app
        
        print("🚀 正在启动夏园API服务器...")
        print(f"📍 地址: http://{config.api_server.host}:{config.api_server.port}")
        print(f"📚 文档: http://{config.api_server.host}:{config.api_server.port}/docs")
        
        # 在新线程中启动API服务器
        def run_server():
            try:
                uvicorn.run(
                    "apiserver.api_server:app",  # 使用字符串路径
                    host=config.api_server.host,
                    port=config.api_server.port,
                    log_level="error",  # 减少日志输出
                    access_log=False,
                    reload=False  # 确保不使用自动重载
                )
            except Exception as e:
                print(f"❌ API服务器启动失败: {e}")
        
        api_thread = threading.Thread(target=run_server, daemon=True)
        api_thread.start()
        print("✅ API服务器已在后台启动")
        
        # 等待服务器启动
        time.sleep(1)
        
    except ImportError as e:
        print(f"⚠️ API服务器依赖缺失: {e}")
        print("   请运行: pip install fastapi uvicorn")
    except Exception as e:
        print(f"❌ API服务器启动异常: {e}")

with open('./ui/progress.txt','w')as f:
    f.write('0')
mm = memory_manager

# 只在需要时初始化全局实例
# n = get_global_naga_instance()  # 不在这里初始化，让它延迟到真正需要时

print('='*30+'\nStarryNight系统已启动\n'+'='*30)

# 情绪AI功能提示
if config.emotional_ai.enabled:
    print(f'🎭 情绪AI系统已启用 - {config.emotional_ai.ai_name} ({config.emotional_ai.personality_age}岁)')
    if config.ui.show_emotion_panel:
        print('💡 UI界面将显示情绪面板，可以观察和控制AI的情绪状态')
    if config.emotional_ai.proactive_enabled:
        print('🤖 AI具备主动行为能力，会根据情绪状态主动发起对话')
    print('🌟 情绪AI特性：')
    print('  - 表扬夸奖会让AI开心 (如：你真棒、好聪明)')
    print('  - 提问会激发AI的好奇心 (如：为什么、怎么样)')
    print('  - 邀请游戏会让AI兴奋 (如：我们玩游戏)')
    print('  - 长时间不互动AI会感到孤独')
    print('='*50)

# 自动启动API服务器
if config.api_server.enabled and config.api_server.auto_start:
    start_api_server()

def check_tts_port_available(port):
    """检查TTS端口是否可用"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", port))
            return True
    except OSError:
        return False

def start_tts_server():
    """在后台启动TTS服务"""
    try:
        if not check_tts_port_available(config.tts.port):
            print(f"⚠️ 端口 {config.tts.port} 已被占用，跳过TTS服务启动")
            return
        
        print("🚀 正在启动TTS服务...")
        print(f"📍 地址: http://127.0.0.1:{config.tts.port}")
        
        def run_tts():
            try:
                # 使用新的启动脚本
                from voice.start_voice_service import start_http_server
                start_http_server()
            except Exception as e:
                print(f"❌ TTS服务启动失败: {e}")
        
        tts_thread = threading.Thread(target=run_tts, daemon=True)
        tts_thread.start()
        print("✅ TTS服务已在后台启动")
        time.sleep(1)
    except Exception as e:
        print(f"❌ TTS服务启动异常: {e}")

# 自动启动TTS服务
start_tts_server()

show_help()
loop=asyncio.new_event_loop()
threading.Thread(target=loop.run_forever,daemon=True).start()

class NagaAgentAdapter:
 def __init__(s):s.naga=get_global_naga_instance()  # 使用全局单例实例
 async def respond_stream(s,txt):
     async for resp in s.naga.process(txt):
         yield "StarryNight",resp,None,True,False

if __name__=="__main__":
    try:
        # 导入异步管理器
        from async_manager import async_manager
        
        # 启动AI网站（如果配置允许）
        website_thread = None
        try:
            if getattr(config, 'ai_website', {}).get('enabled', True):
                def start_website():
                    try:
                        from ai_website.app import app as website_app, ai_publisher
                        from ai_dynamic_publisher import initialize_publisher, start_publisher
                        
                        # 初始化动态发布器
                        initialize_publisher(ai_publisher)
                        
                        # 启动网站
                        import uvicorn
                        uvicorn.run(website_app, host="0.0.0.0", port=8001, log_level="error")
                    except Exception as e:
                        print(f"❌ AI网站启动失败: {e}")
                
                website_thread = threading.Thread(target=start_website, daemon=True)
                website_thread.start()
                print("🌐 AI展示网站已启动: http://localhost:8001")
                
                # 延迟启动动态发布器并连接AI实例
                def delayed_start_publisher():
                    time.sleep(3)  # 等待网站启动
                    try:
                        import asyncio
                        from ai_dynamic_publisher import start_publisher, ai_dynamic_publisher
                        
                        # 获取AI实例并连接到发布器
                        ai_instance = get_global_naga_instance()
                        ai_dynamic_publisher.set_ai_instance(ai_instance)
                        
                        # 在新的事件循环中启动
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(start_publisher())
                        print("✅ AI动态发布器已启动并连接到AI实例")
                    except Exception as e:
                        print(f"⚠️ 动态发布器启动失败: {e}")
                
                publisher_thread = threading.Thread(target=delayed_start_publisher, daemon=True)
                publisher_thread.start()
                
                # 启动AI自主交互系统
                def delayed_start_autonomous():
                    time.sleep(3)  # 等待AI系统完全初始化
                    try:
                        import asyncio
                        from ai_autonomous_interaction import start_autonomous_interaction
                        
                        # 在新的事件循环中启动自主交互
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        async def run_autonomous():
                            print("🚀 正在启动AI自主交互系统...")
                            await start_autonomous_interaction()
                            print("✅ AI自主交互系统已成功启动")
                            
                            # 保持事件循环运行
                            while True:
                                await asyncio.sleep(1)
                        
                        try:
                            loop.run_until_complete(run_autonomous())
                        except KeyboardInterrupt:
                            print("🛑 AI自主交互系统被中断")
                        finally:
                            loop.close()
                            
                    except Exception as e:
                        print(f"⚠️ 自主交互系统启动失败: {e}")
                        import traceback
                        traceback.print_exc()
                
                autonomous_thread = threading.Thread(target=delayed_start_autonomous, daemon=True)
                autonomous_thread.start()
                print("🤖 正在初始化AI自主交互系统...")
                
        except Exception as e:
            print(f"⚠️ AI网站初始化失败: {e}")
        
        app=QApplication(sys.argv)
        icon_path = os.path.join(os.path.dirname(__file__), "ui", "window_icon.png")
        app.setWindowIcon(QIcon(icon_path))
        win=ChatWindow()
        win.setWindowTitle("StarryNight AGENT")
        
        # 延迟初始化AI自主交互与GUI的连接
        def delayed_connect_ai():
            time.sleep(2)  # 等待GUI完全初始化
            try:
                from ui.notification_manager import get_notification_manager
                from ai_autonomous_interaction import get_autonomous_interaction
                
                # 重新初始化通知管理器，连接到GUI
                notification_manager = get_notification_manager()
                notification_manager.initialize(win)
                
                # 确保AI系统知道GUI已准备好
                ai_system = get_autonomous_interaction()
                print(f"🔗 AI自主交互系统已连接到GUI: {type(win).__name__}")
                
                # 发送测试消息验证连接
                notification_manager.send_ai_message("🌟 AI autonomous interaction system connected to GUI successfully!", "happy", "system")
                
            except Exception as e:
                print(f"❌ AI-GUI连接失败: {e}")
        
        # 在后台线程中延迟连接
        connection_thread = threading.Thread(target=delayed_connect_ai, daemon=True)
        connection_thread.start()
        
        win.show()
        
        # 注册应用退出时的清理
        app.aboutToQuit.connect(async_manager.cleanup_all)
        
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("\n⚠️ 程序被用户中断")
        async_manager.cleanup_all()
        sys.exit(0)
    except Exception as e:
        print(f"❌ 程序异常退出: {e}")
        async_manager.cleanup_all()
        sys.exit(1)
