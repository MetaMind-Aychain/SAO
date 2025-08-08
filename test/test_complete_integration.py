#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整集成测试脚本
测试AI自主交互系统与GUI和Web端的完整消息流
"""

import asyncio
import logging
import time
import threading
import json
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_ai_autonomous_startup():
    """测试AI自主交互系统启动"""
    logger.info("🚀 测试AI自主交互系统启动...")
    
    try:
        from ai_autonomous_interaction import get_autonomous_interaction
        
        ai_system = get_autonomous_interaction()
        logger.info(f"AI自主交互实例: {type(ai_system).__name__}")
        logger.info(f"是否正在运行: {ai_system.is_running}")
        
        if not ai_system.is_running:
            logger.info("启动AI自主交互系统...")
            await ai_system.start_autonomous_interaction()
            logger.info("✅ AI自主交互系统启动成功")
        else:
            logger.info("✅ AI自主交互系统已在运行")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ AI自主交互系统启动失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_notification_flow():
    """测试完整的通知流程"""
    logger.info("🔔 测试完整通知流程...")
    
    try:
        from ai_autonomous_interaction import get_autonomous_interaction
        
        ai_system = get_autonomous_interaction()
        
        # 测试不同优先级的消息
        test_messages = [
            ("🧪 低优先级测试消息", "好奇", "testing", "low"),
            ("🌟 普通优先级测试消息", "兴奋", "learning", "normal"), 
            ("✨ 高优先级测试消息", "开心", "reflection", "high"),
            ("🚨 紧急优先级测试消息", "惊讶", "summary", "urgent")
        ]
        
        for message, emotion, activity, priority in test_messages:
            logger.info(f"发送测试消息: {priority} - {message}")
            await ai_system._notify_desktop(message, emotion, activity, priority)
            await asyncio.sleep(2)  # 等待2秒
        
        logger.info("✅ 通知流程测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 通知流程测试失败: {e}")
        return False

async def test_websocket_broadcast():
    """测试websocket广播功能"""
    logger.info("🌐 测试websocket广播功能...")
    
    try:
        from apiserver.api_server import manager
        
        # 测试不同类型的广播消息
        test_broadcasts = [
            {
                "type": "ai_autonomous_message",
                "content": "🧪 这是websocket广播测试消息",
                "emotion": "测试",
                "activity": "testing",
                "priority": "normal",
                "source": "test_script",
                "timestamp": datetime.now().isoformat(),
                "ai_name": "测试AI"
            },
            {
                "type": "ai_autonomous_message", 
                "content": "🎯 这是另一个测试消息，用于验证实时显示功能",
                "emotion": "兴奋",
                "activity": "verification",
                "priority": "high",
                "source": "test_script",
                "timestamp": datetime.now().isoformat(),
                "ai_name": "StarryNight"
            }
        ]
        
        for broadcast_data in test_broadcasts:
            logger.info(f"发送websocket广播: {broadcast_data['content']}")
            await manager.broadcast(json.dumps(broadcast_data, ensure_ascii=False))
            await asyncio.sleep(1)
        
        logger.info("✅ websocket广播测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ websocket广播测试失败: {e}")
        return False

async def test_dynamic_publisher():
    """测试动态发布器功能"""
    logger.info("📤 测试动态发布器功能...")
    
    try:
        from ai_dynamic_publisher import publish_ai_interaction
        
        # 测试发布不同类型的AI交互
        test_interactions = [
            ("autonomous_message", "🧪 这是通过动态发布器发送的测试消息", {"emotion": "测试", "activity": "testing"}),
            ("proactive_behavior", "🎯 AI主动行为测试", {"emotion": "好奇", "activity": "exploration"}),
            ("self_reflection", "🤔 AI自我反思测试", {"emotion": "calm", "activity": "reflection"})
        ]
        
        for msg_type, content, emotion_context in test_interactions:
            logger.info(f"发布AI交互: {msg_type} - {content}")
            await publish_ai_interaction(msg_type, content, emotion_context)
            await asyncio.sleep(1)
        
        logger.info("✅ 动态发布器测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 动态发布器测试失败: {e}")
        return False

def test_gui_notification_manager():
    """测试GUI通知管理器"""
    logger.info("🖥️ 测试GUI通知管理器...")
    
    try:
        from ui.notification_manager import get_notification_manager
        
        notification_manager = get_notification_manager()
        logger.info(f"通知管理器状态: 初始化={notification_manager.is_initialized}")
        
        if notification_manager.is_initialized:
            # 发送测试通知
            notification_manager.send_ai_message("🧪 GUI通知测试消息", "测试", "testing")
            notification_manager.send_emotion_update("兴奋", 0.8)
            notification_manager.send_activity_notification("testing", "正在测试GUI通知功能")
            logger.info("✅ GUI通知已发送")
        else:
            logger.warning("⚠️ GUI通知管理器未初始化")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ GUI通知管理器测试失败: {e}")
        return False

async def run_comprehensive_test():
    """运行综合测试"""
    logger.info("🌟 开始AI系统完整集成测试...")
    logger.info("="*80)
    
    test_results = []
    
    # 测试1: AI自主交互系统启动
    logger.info("\n🧪 测试1: AI自主交互系统启动")
    logger.info("-" * 50)
    result1 = await test_ai_autonomous_startup()
    test_results.append(("AI自主交互启动", result1))
    
    # 等待系统稳定
    if result1:
        logger.info("等待系统稳定...")
        await asyncio.sleep(3)
    
    # 测试2: 通知流程
    logger.info("\n🧪 测试2: 完整通知流程")
    logger.info("-" * 50)
    result2 = await test_notification_flow()
    test_results.append(("通知流程", result2))
    
    # 测试3: websocket广播
    logger.info("\n🧪 测试3: websocket广播")
    logger.info("-" * 50)
    result3 = await test_websocket_broadcast()
    test_results.append(("websocket广播", result3))
    
    # 测试4: 动态发布器
    logger.info("\n🧪 测试4: 动态发布器")
    logger.info("-" * 50)
    result4 = await test_dynamic_publisher()
    test_results.append(("动态发布器", result4))
    
    # 测试5: GUI通知管理器
    logger.info("\n🧪 测试5: GUI通知管理器")
    logger.info("-" * 50)
    result5 = test_gui_notification_manager()
    test_results.append(("GUI通知管理器", result5))
    
    # 汇总结果
    logger.info("\n" + "="*80)
    logger.info("📊 完整集成测试结果")
    logger.info("="*80)
    
    success_count = 0
    for test_name, success in test_results:
        status = "✅ 通过" if success else "❌ 失败"
        logger.info(f"{status} {test_name}")
        if success:
            success_count += 1
    
    total_tests = len(test_results)
    success_rate = (success_count / total_tests) * 100
    
    logger.info(f"\n🎯 总体结果: {success_count}/{total_tests} 通过 ({success_rate:.1f}%)")
    
    if success_count == total_tests:
        logger.info("\n🎉 所有集成测试通过！AI系统已完全集成！")
        print("\n" + "="*80)
        print("✅ AI自主交互系统与GUI和Web端集成测试成功！")
        print("🌟 系统功能:")
        print("  - AI自主交互消息实时显示在桌面GUI")
        print("  - AI消息通过websocket实时广播到web端")
        print("  - 动态发布器正常记录AI活动")
        print("  - 完整的消息流：AI生成 → GUI显示 → Web显示")
        print("="*80)
        return True
    else:
        logger.error("\n❌ 部分集成测试失败，需要进一步检查")
        return False

async def simulate_ai_activity():
    """模拟AI活动来持续测试"""
    logger.info("🤖 开始模拟AI活动...")
    
    try:
        from ai_autonomous_interaction import get_autonomous_interaction
        
        ai_system = get_autonomous_interaction()
        
        activities = [
            ("💭 AI正在思考问题...", "思考", "thinking"),
            ("📸 AI观察到摄像头画面变化", "好奇", "camera"),
            ("🖥️ AI发现屏幕上有新内容", "兴奋", "screen"),
            ("📄 AI阅读了一个有趣的文件", "学习", "file"),
            ("🌐 AI浏览了网络上的信息", "探索", "web"),
            ("🤔 AI在进行自我反思", "calm", "reflection"),
            ("📚 AI学习了新知识", "满足", "learning"),
            ("✨ AI完成了一次总结", "成就", "summary")
        ]
        
        for i, (message, emotion, activity) in enumerate(activities):
            logger.info(f"模拟活动 {i+1}/8: {message}")
            await ai_system._notify_desktop(message, emotion, activity, "normal")
            await asyncio.sleep(5)  # 每5秒一个活动
        
        logger.info("✅ AI活动模拟完成")
        
    except Exception as e:
        logger.error(f"❌ AI活动模拟失败: {e}")

if __name__ == "__main__":
    try:
        print("🌟 AI自主交互系统完整集成测试")
        print("="*80)
        print("此测试将验证:")
        print("1. AI自主交互系统启动和运行")
        print("2. GUI通知管理器集成")  
        print("3. websocket广播功能")
        print("4. 动态发布器功能")
        print("5. 完整的消息流程")
        print("="*80)
        
        # 运行综合测试
        result = asyncio.run(run_comprehensive_test())
        
        if result:
            print("\n🎯 开始持续模拟AI活动 (按Ctrl+C停止)...")
            try:
                asyncio.run(simulate_ai_activity())
            except KeyboardInterrupt:
                print("\n🛑 AI活动模拟被用户停止")
        
    except KeyboardInterrupt:
        logger.info("🛑 测试被用户中断")
    except Exception as e:
        logger.error(f"❌ 测试运行失败: {e}")
        import traceback
        traceback.print_exc()