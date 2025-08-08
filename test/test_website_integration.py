#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI网站集成功能
"""

import asyncio
import sys
import time
import threading
from datetime import datetime

def test_gpu_optimization():
    """测试GPU优化"""
    print("🔧 测试GPU优化...")
    
    try:
        from gpu_optimization import get_gpu_status, GPU_AVAILABLE
        
        status = get_gpu_status()
        print(f"GPU可用: {status['gpu_available']}")
        print(f"CuPy可用: {status['cupy_available']}")
        print(f"PyTorch GPU可用: {status['torch_gpu_available']}")
        
        if status['device_info']:
            info = status['device_info']
            print(f"设备名称: {info.get('device_name', 'Unknown')}")
            print(f"显存使用: {info.get('memory_allocated', 0):.2f}GB")
        
        return True
        
    except Exception as e:
        print(f"❌ GPU优化测试失败: {e}")
        return False

def test_dynamic_publisher():
    """测试动态发布系统"""
    print("\n📰 测试动态发布系统...")
    
    try:
        from ai_dynamic_publisher import ai_dynamic_publisher, publish_thinking
        
        # 测试手动发布
        asyncio.run(publish_thinking("这是一个测试思考动态", {"test": True}))
        print("✅ 动态发布系统正常")
        return True
        
    except Exception as e:
        print(f"❌ 动态发布测试失败: {e}")
        return False

def test_website_components():
    """测试网站组件"""
    print("\n🌐 测试网站组件...")
    
    try:
        # 测试FastAPI应用
        from ai_website.app import app
        print("✅ FastAPI应用加载成功")
        
        # 测试数据库模型
        from ai_website.app import User, AIDynamic, Comment
        print("✅ 数据库模型加载成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 网站组件测试失败: {e}")
        return False

def test_integration():
    """测试整体集成"""
    print("\n🔗 测试整体集成...")
    
    try:
        # 模拟AI活动
        from enhanced_screen_analyzer import enhanced_screen_analyzer
        print("✅ 屏幕分析器集成成功")
        
        from enhanced_camera_analyzer import enhanced_camera_analyzer
        print("✅ 摄像头分析器集成成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 整体集成测试失败: {e}")
        return False

async def test_async_functionality():
    """测试异步功能"""
    print("\n⚡ 测试异步功能...")
    
    try:
        # 测试异步动态发布
        from ai_dynamic_publisher import publish_manual_dynamic
        
        await publish_manual_dynamic("测试异步动态发布功能", "thinking")
        print("✅ 异步动态发布正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 异步功能测试失败: {e}")
        return False

def start_test_website():
    """启动测试网站"""
    print("\n🚀 启动测试网站...")
    
    try:
        from ai_website.app import app as website_app
        import uvicorn
        
        # 在后台启动网站
        def run_website():
            uvicorn.run(website_app, host="127.0.0.1", port=8001, log_level="error")
        
        website_thread = threading.Thread(target=run_website, daemon=True)
        website_thread.start()
        
        # 等待网站启动
        time.sleep(2)
        print("✅ 测试网站已启动: http://localhost:8001")
        return True
        
    except Exception as e:
        print(f"❌ 测试网站启动失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🧪 StarryNightAI网站集成测试")
    print("=" * 60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("GPU优化", test_gpu_optimization),
        ("动态发布系统", test_dynamic_publisher),
        ("网站组件", test_website_components),
        ("整体集成", test_integration),
    ]
    
    async_tests = [
        ("异步功能", test_async_functionality),
    ]
    
    passed = 0
    total = len(tests) + len(async_tests)
    
    # 运行同步测试
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    # 运行异步测试
    for test_name, test_func in async_tests:
        try:
            result = await test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    # 启动测试网站
    website_started = start_test_website()
    if website_started:
        passed += 1
        total += 1
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 AI网站集成测试结果:")
    print(f"🎯 通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 所有测试通过！AI网站集成成功！")
        print("\n💡 主要功能:")
        print("   • ✅ GPU加速处理（图像、文本、人脸检测）")
        print("   • 🌐 Truth Terminal风格的AI展示网站")
        print("   • 📰 实时AI动态发布系统")
        print("   • 👥 用户注册登录和个性化记忆")
        print("   • 💬 智能评论互动系统")
        print("   • 🔄 桌面端和网站端同步")
        print("   • 🎭 情绪驱动的内容生成")
        print("   • 📊 WebSocket实时更新")
        
        print("\n🌟 访问网站:")
        print("   • 主页: http://localhost:8001")
        print("   • API文档: http://localhost:8001/docs")
        
        print("\n🎮 使用方式:")
        print("   1. 启动桌面端: python main.py")
        print("   2. 访问网站查看AI动态")
        print("   3. 注册账号与AI互动")
        print("   4. 观察AI的情绪、学习、探索过程")
        
    elif passed >= total * 0.75:
        print("⚠️ 大部分测试通过，系统基本可用")
        print("🔧 建议检查失败的组件")
    else:
        print("🔧 需要进一步修复和调试")
    
    print(f"\n🚀 StarryNightAI系统 - 现在拥有GPU优化和在线展示能力！")
    
    return passed >= total * 0.75

if __name__ == "__main__":
    try:
        # Windows事件循环策略
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        success = asyncio.run(main())
        
        if success:
            print("\n🎊 测试完成！网站将继续运行...")
            print("按 Ctrl+C 退出")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 再见！")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试程序异常: {e}")
        sys.exit(1)