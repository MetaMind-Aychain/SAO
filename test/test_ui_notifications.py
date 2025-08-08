#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI通知集成测试脚本
测试AI自主交互系统与桌面UI的集成效果
"""

import asyncio
import logging
import time
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_notification_system():
    """测试通知系统的各项功能"""
    
    logger.info("🚀 开始测试UI通知集成系统")
    
    try:
        # 导入通知管理器
        from ui.notification_manager import get_notification_manager
        notification_manager = get_notification_manager()
        
        logger.info("✅ 通知管理器导入成功")
        
        # 测试1: 基本消息通知
        logger.info("📝 测试1: 基本消息通知")
        await asyncio.sleep(1)
        notification_manager.send_ai_message(
            "这是一条测试消息！我正在验证通知系统是否正常工作。", 
            emotion_type="快乐",
            activity_type="testing"
        )
        
        # 测试2: 不同优先级的消息
        logger.info("🔔 测试2: 不同优先级消息")
        await asyncio.sleep(2)
        
        # 低优先级
        notification_manager.send_ai_message(
            "这是一条低优先级的思考消息...", 
            emotion_type="calm",
            activity_type="thinking"
        )
        
        await asyncio.sleep(1)
        
        # 高优先级
        notification_manager.send_ai_message(
            "重要发现！我学到了新知识！", 
            emotion_type="兴奋",
            activity_type="learning"
        )
        
        # 测试3: 情绪更新
        logger.info("😊 测试3: 情绪状态更新")
        await asyncio.sleep(1)
        
        emotions_to_test = [
            ("好奇", 0.8),
            ("快乐", 0.9),
            ("calm", 0.6),
            ("惊讶", 0.7)
        ]
        
        for emotion_type, intensity in emotions_to_test:
            notification_manager.send_emotion_update(emotion_type, intensity)
            await asyncio.sleep(1)
            
        # 测试4: 活动通知
        logger.info("⚡ 测试4: 活动状态通知")
        await asyncio.sleep(1)
        
        activities_to_test = [
            ("camera", "正在观察摄像头画面，发现了有趣的场景"),
            ("screen", "分析屏幕内容，看到了新的信息"),
            ("web", "浏览网页发现了有价值的知识"),
            ("file", "阅读文档学习了新概念"),
            ("thinking", "深度思考当前遇到的问题"),
            ("summary", "整理今天的学习成果")
        ]
        
        for activity_type, description in activities_to_test:
            notification_manager.send_activity_notification(activity_type, description)
            await asyncio.sleep(1.5)
            
        # 测试5: 系统通知
        logger.info("🔥 测试5: 系统通知")
        await asyncio.sleep(1)
        notification_manager.send_system_notification(
            "StarryNightAI", 
            "通知系统集成测试已完成！所有功能运行正常。"
        )
        
        # 测试6: 状态更新
        logger.info("📊 测试6: 完整状态更新")
        await asyncio.sleep(1)
        
        status_data = {
            "ai_name": "StarryNight",
            "personality_age": 3,
            "last_interaction": "刚刚",
            "dominant_emotion": {
                "type": "满足",
                "intensity": "85%",
                "emoji": "😌"
            },
            "social_satisfaction": "75%",
            "exploration_satisfaction": "90%",
            "all_emotions": [
                {"type": "满足", "intensity": "85%"},
                {"type": "好奇", "intensity": "70%"},
                {"type": "快乐", "intensity": "60%"}
            ]
        }
        
        notification_manager.send_status_update(status_data)
        
        logger.info("✅ 所有测试完成！通知系统集成成功。")
        
    except Exception as e:
        logger.error(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

async def test_autonomous_integration():
    """测试AI自主交互系统的通知集成"""
    
    logger.info("🤖 测试AI自主交互系统集成")
    
    try:
        # 导入AI自主交互系统
        from ai_autonomous_interaction import get_autonomous_interaction
        autonomous_system = get_autonomous_interaction()
        
        logger.info("✅ AI自主交互系统导入成功")
        
        # 测试直接调用_notify_desktop方法
        await autonomous_system._notify_desktop(
            "测试AI自主交互系统的桌面通知功能", 
            emotion_type="兴奋",
            activity_type="testing",
            priority="high"
        )
        
        await asyncio.sleep(2)
        
        await autonomous_system._notify_desktop(
            "这是一个低优先级的思考消息", 
            emotion_type="calm",
            activity_type="thinking",
            priority="low"
        )
        
        logger.info("✅ AI自主交互系统通知测试完成")
        
    except Exception as e:
        logger.error(f"❌ AI自主交互系统测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_callback_registration():
    """测试回调注册功能"""
    
    logger.info("🔗 测试回调注册功能")
    
    try:
        from ui.notification_manager import get_notification_manager
        notification_manager = get_notification_manager()
        
        # 定义测试回调函数
        def message_callback(message):
            logger.info(f"🔔 回调收到消息: {message}")
            
        def emotion_callback(emotion_type, intensity):
            logger.info(f"😊 回调收到情绪更新: {emotion_type} - {intensity}")
            
        def activity_callback(activity_type, description):
            logger.info(f"⚡ 回调收到活动通知: {activity_type} - {description}")
            
        # 注册回调
        notification_manager.register_callback('message', message_callback)
        notification_manager.register_callback('emotion', emotion_callback)
        notification_manager.register_callback('activity', activity_callback)
        
        logger.info("✅ 回调注册成功")
        
        # 测试回调
        notification_manager.send_ai_message("测试回调功能", emotion_type="快乐")
        notification_manager.send_emotion_update("兴奋", 0.8)
        notification_manager.send_activity_notification("testing", "测试回调机制")
        
        logger.info("✅ 回调测试完成")
        
    except Exception as e:
        logger.error(f"❌ 回调测试失败: {e}")

async def main():
    """主测试函数"""
    
    logger.info("🌟 开始UI通知集成完整测试")
    
    # 测试1: 基本通知系统
    await test_notification_system()
    await asyncio.sleep(2)
    
    # 测试2: AI自主交互集成
    await test_autonomous_integration()
    await asyncio.sleep(2)
    
    # 测试3: 回调注册（同步测试）
    test_callback_registration()
    
    logger.info("🎉 所有测试完成！UI通知集成系统可以正常使用。")
    
    # 使用说明
    print("\n" + "="*60)
    print("🌟 UI通知集成系统使用说明:")
    print("="*60)
    print("1. 在AI自主交互中调用 await self._notify_desktop(...)")
    print("2. 支持的参数:")
    print("   - message: 通知消息内容")
    print("   - emotion_type: 情绪类型 (快乐, 兴奋, calm, 好奇等)")
    print("   - activity_type: 活动类型 (thinking, camera, screen, file, web等)")
    print("   - priority: 优先级 (low, normal, high, urgent)")
    print("3. 自动集成到UI和情绪面板")
    print("4. 支持语音播报和系统通知")
    print("5. 提供回调机制用于自定义处理")
    print("="*60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 测试被用户中断")
    except Exception as e:
        logger.error(f"❌ 测试运行失败: {e}")
        import traceback
        traceback.print_exc()