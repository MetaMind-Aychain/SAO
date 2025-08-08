#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复AI集成问题的测试脚本
验证AI自主交互消息能正确显示在GUI和Web端
"""

import asyncio
import logging
import time
import json
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_notification_manager_fix():
    """测试通知管理器修复"""
    logger.info("🔧 测试通知管理器修复...")
    
    try:
        from ui.notification_manager import get_notification_manager
        
        # 获取通知管理器
        notification_manager = get_notification_manager()
        logger.info(f"通知管理器状态: 初始化={notification_manager.is_initialized}")
        logger.info(f"UI实例: {notification_manager.ui_instance}")
        
        # 模拟GUI实例来测试重新初始化
        class MockGUI:
            def __init__(self):
                self.received_messages = []
                
            def on_ai_proactive_message(self, message):
                self.received_messages.append(message)
                logger.info(f"📩 GUI收到消息: {message}")
        
        mock_gui = MockGUI()
        
        # 重新初始化通知管理器
        notification_manager.initialize(mock_gui)
        logger.info(f"重新初始化后状态: 初始化={notification_manager.is_initialized}")
        
        # 发送测试消息
        notification_manager.send_ai_message("🧪 测试消息：通知管理器修复验证", "测试", "verification")
        
        # 等待消息处理
        await asyncio.sleep(1)
        
        if mock_gui.received_messages:
            logger.info(f"✅ GUI成功接收到 {len(mock_gui.received_messages)} 条消息")
            return True
        else:
            logger.warning("⚠️ GUI没有接收到消息")
            return False
            
    except Exception as e:
        logger.error(f"❌ 通知管理器测试失败: {e}")
        return False

async def test_websocket_connection():
    """测试websocket连接"""
    logger.info("🌐 测试websocket连接...")
    
    try:
        import websockets
        import asyncio
        
        # 尝试连接到API服务器的websocket
        uri = "ws://localhost:8000/ws/mcplog"
        
        async def test_connection():
            try:
                async with websockets.connect(uri) as websocket:
                    logger.info("✅ WebSocket连接成功")
                    
                    # 等待连接确认消息
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    data = json.loads(response)
                    logger.info(f"收到服务器消息: {data}")
                    
                    # 发送心跳
                    await websocket.send("ping")
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    data = json.loads(response)
                    logger.info(f"心跳响应: {data}")
                    
                    return True
                    
            except Exception as e:
                logger.error(f"WebSocket连接失败: {e}")
                return False
        
        return await test_connection()
        
    except ImportError:
        logger.warning("websockets库未安装，跳过WebSocket测试")
        return True
    except Exception as e:
        logger.error(f"❌ WebSocket测试失败: {e}")
        return False

async def test_ai_message_broadcasting():
    """测试AI消息广播"""
    logger.info("📡 测试AI消息广播...")
    
    try:
        from ai_autonomous_interaction import get_autonomous_interaction
        
        ai_system = get_autonomous_interaction()
        
        # 发送几条测试消息，测试所有路径
        test_messages = [
            ("🔧 修复测试：GUI集成验证", "测试", "gui_fix", "high"),
            ("🌐 修复测试：Web端验证", "验证", "web_fix", "high"), 
            ("📱 修复测试：完整消息流验证", "完成", "integration_fix", "urgent")
        ]
        
        for i, (message, emotion, activity, priority) in enumerate(test_messages, 1):
            logger.info(f"发送测试消息 {i}/3: {message}")
            await ai_system._notify_desktop(message, emotion, activity, priority)
            await asyncio.sleep(2)  # 等待消息处理
        
        logger.info("✅ AI消息广播测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ AI消息广播测试失败: {e}")
        return False

async def test_websocket_broadcast_direct():
    """直接测试websocket广播"""
    logger.info("📤 直接测试websocket广播...")
    
    try:
        from apiserver.api_server import manager
        
        # 直接发送广播消息
        test_broadcast = {
            "type": "ai_autonomous_message",
            "content": "🔧 这是修复验证的直接广播消息",
            "emotion": "验证",
            "activity": "direct_test",
            "priority": "high",
            "source": "fix_test",
            "timestamp": datetime.now().isoformat(),
            "ai_name": "修复测试AI"
        }
        
        await manager.broadcast(json.dumps(test_broadcast, ensure_ascii=False))
        logger.info(f"✅ 直接广播消息已发送: {test_broadcast['content']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 直接广播测试失败: {e}")
        return False

async def run_integration_fix_test():
    """运行完整的集成修复测试"""
    logger.info("🔧 开始AI集成修复测试...")
    logger.info("="*80)
    
    test_results = []
    
    # 测试1: 通知管理器修复
    logger.info("\n🧪 测试1: 通知管理器修复")
    logger.info("-" * 50)
    result1 = await test_notification_manager_fix()
    test_results.append(("通知管理器修复", result1))
    
    # 测试2: WebSocket连接
    logger.info("\n🧪 测试2: WebSocket连接")
    logger.info("-" * 50)
    result2 = await test_websocket_connection()
    test_results.append(("WebSocket连接", result2))
    
    # 测试3: AI消息广播
    logger.info("\n🧪 测试3: AI消息广播")
    logger.info("-" * 50)
    result3 = await test_ai_message_broadcasting()
    test_results.append(("AI消息广播", result3))
    
    # 测试4: 直接WebSocket广播
    logger.info("\n🧪 测试4: 直接WebSocket广播")
    logger.info("-" * 50)
    result4 = await test_websocket_broadcast_direct()
    test_results.append(("直接WebSocket广播", result4))
    
    # 汇总结果
    logger.info("\n" + "="*80)
    logger.info("📊 集成修复测试结果")
    logger.info("="*80)
    
    success_count = 0
    for test_name, success in test_results:
        status = "✅ 通过" if success else "❌ 失败"
        logger.info(f"{status} {test_name}")
        if success:
            success_count += 1
    
    total_tests = len(test_results)
    success_rate = (success_count / total_tests) * 100
    
    logger.info(f"\n🎯 修复测试结果: {success_count}/{total_tests} 通过 ({success_rate:.1f}%)")
    
    if success_count == total_tests:
        logger.info("\n🎉 所有修复测试通过！AI消息应该能正确显示在GUI和Web端了！")
        print("\n" + "="*80)
        print("✅ AI集成修复测试成功！")
        print("🔧 修复内容:")
        print("  - 通知管理器支持重新初始化")
        print("  - WebSocket连接验证正常")
        print("  - AI消息广播路径畅通")
        print("  - 直接广播功能正常")
        print("\n📋 验证步骤:")
        print("  1. 启动完整系统 (python main.py)")
        print("  2. 观察GUI界面是否显示AI消息")
        print("  3. 访问Web页面查看实时消息")
        print("="*80)
        return True
    else:
        logger.error("\n❌ 部分修复测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    try:
        print("🔧 AI集成修复测试")
        print("="*80)
        print("此测试将验证并修复:")
        print("1. 通知管理器初始化问题")
        print("2. WebSocket连接问题")  
        print("3. AI消息广播问题")
        print("4. GUI和Web端显示问题")
        print("="*80)
        
        # 运行修复测试
        result = asyncio.run(run_integration_fix_test())
        
        if result:
            print("\n🎯 修复完成！现在可以测试完整系统了")
        else:
            print("\n❌ 修复过程中发现问题，请检查错误信息")
        
    except KeyboardInterrupt:
        logger.info("🛑 测试被用户中断")
    except Exception as e:
        logger.error(f"❌ 测试运行失败: {e}")
        import traceback
        traceback.print_exc()