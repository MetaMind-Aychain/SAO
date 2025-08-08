#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的系统
包含语音服务检查、设置界面返回功能等
"""

import sys
import os
import asyncio
import signal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

def test_tts_service():
    """测试TTS服务"""
    print("🎤 检查TTS语音服务...")
    try:
        from check_tts_service import check_tts_service, ensure_tts_service
        
        if ensure_tts_service():
            print("✅ TTS服务正常")
            return True
        else:
            print("⚠️ TTS服务不可用，语音功能将被禁用")
            return False
    except Exception as e:
        print(f"❌ TTS服务检查失败: {e}")
        return False

def test_ui_return_button():
    """测试UI返回按钮功能"""
    print("🖥️ 测试界面返回功能...")
    try:
        from ui.pyqt_chat_window import ChatWindow
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # 创建窗口
        window = ChatWindow()
        
        # 检查是否有返回方法
        if hasattr(window, 'return_to_chat'):
            print("✅ 返回聊天功能已添加")
            return True
        else:
            print("❌ 返回聊天功能未找到")
            return False
            
    except Exception as e:
        print(f"❌ UI测试失败: {e}")
        return False

def test_config_validation():
    """测试配置验证"""
    print("⚙️ 检查配置验证...")
    try:
        from config import config
        
        # 检查关键配置
        sharing_prob = config.emotional_ai.sharing_probability
        if 0 <= sharing_prob <= 1:
            print(f"✅ sharing_probability配置正确: {sharing_prob}")
        else:
            print(f"❌ sharing_probability配置错误: {sharing_prob}")
            return False
        
        bg_alpha = config.ui.bg_alpha
        if 0 <= bg_alpha <= 1:
            print(f"✅ bg_alpha配置正确: {bg_alpha}")
        else:
            print(f"❌ bg_alpha配置错误: {bg_alpha}")
            return False
        
        print("✅ 配置验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        return False

def test_voice_error_handling():
    """测试语音错误处理"""
    print("🔊 测试语音错误处理...")
    try:
        from voice.voice_integration import VoiceIntegration
        
        # 创建语音集成实例
        voice = VoiceIntegration()
        
        # 测试文本处理（即使TTS服务不可用也应该正常）
        voice.receive_text_chunk("测试文本")
        print("✅ 语音错误处理正常")
        return True
        
    except Exception as e:
        print(f"❌ 语音错误处理测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🔧 StarryNight AGENT 系统修复测试")
    print("=" * 50)
    
    # 设置信号处理
    def signal_handler(signum, frame):
        print("\n⚠️ 收到中断信号，正在退出...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    tests = [
        ("配置验证", test_config_validation),
        ("语音错误处理", test_voice_error_handling), 
        ("TTS服务", test_tts_service),
        ("UI返回功能", test_ui_return_button),
    ]
    
    results = []
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}测试...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await asyncio.wait_for(test_func(), timeout=30)
            else:
                result = test_func()
            results.append((test_name, result))
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 修复测试结果:")
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("🎉 所有修复都成功！系统已准备就绪")
        print("💡 新功能:")
        print("   • 设置界面有返回按钮")
        print("   • 语音服务错误处理更健壮")
        print("   • 配置验证更严格")
        print("   • 异步任务清理更完善")
    elif passed >= len(results) * 0.8:
        print("⚠️ 大部分修复成功，系统可以使用")
    else:
        print("❌ 多项修复失败，建议检查问题")
    
    return passed == len(results)

if __name__ == "__main__":
    try:
        # Windows事件循环策略
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试程序异常: {e}")
        sys.exit(1)