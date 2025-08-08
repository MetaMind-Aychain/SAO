#!/usr/bin/env python3
# demo_emotional_ai.py
"""
情绪化AI系统演示脚本
展示各种功能和特性
"""

import sys
import os
import asyncio
import time
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

async def demo_emotion_system():
    """演示情绪系统"""
    print("🎭 情绪系统演示")
    print("-" * 30)
    
    from emotional_ai.emotion_core import get_emotion_engine, EmotionType
    
    emotion_engine = get_emotion_engine()
    
    print("1. 添加不同情绪...")
    emotion_engine.add_emotion(EmotionType.HAPPY, 0.8)
    print(f"   当前情绪: {emotion_engine.get_emotion_display()}")
    
    emotion_engine.add_emotion(EmotionType.CURIOUS, 0.6)
    print(f"   当前情绪: {emotion_engine.get_emotion_display()}")
    
    emotion_engine.add_emotion(EmotionType.EXCITED, 0.9)
    print(f"   当前情绪: {emotion_engine.get_emotion_display()}")
    
    print("\n2. 分析用户输入触发的情绪...")
    test_inputs = [
        "你真棒！",
        "我们来玩游戏吧！",
        "为什么天空是蓝色的？",
        "我不喜欢这个"
    ]
    
    for input_text in test_inputs:
        triggered = emotion_engine.analyze_input_emotion(input_text)
        print(f"   输入: '{input_text}' -> 触发: {[(e.value, f'{i:.1f}') for e, i in triggered]}")
    
    print("\n3. 生成个性化回复...")
    base_response = "这是一个基础回复。"
    modified_response = emotion_engine.get_personality_modifier(base_response)
    print(f"   原始: {base_response}")
    print(f"   修改: {modified_response}")
    
    print("\n4. 检查是否应该主动发起对话...")
    should_initiate = emotion_engine.should_initiate_conversation()
    print(f"   应该主动对话: {should_initiate}")
    
    if should_initiate:
        proactive_message = emotion_engine.generate_proactive_message()
        print(f"   主动消息: {proactive_message}")

async def demo_perception_system():
    """演示感知系统"""
    print("\n👁️ 感知系统演示")
    print("-" * 30)
    
    from emotional_ai.perception_system import get_perception_manager, PerceptionEvent
    
    perception_manager = get_perception_manager()
    
    # 添加事件回调
    events_received = []
    
    def event_callback(event: PerceptionEvent):
        events_received.append(event)
        print(f"   收到感知事件: {event.event_type} - {event.data}")
    
    perception_manager.add_event_callback(event_callback)
    
    print("1. 模拟感知事件...")
    
    # 模拟文件事件
    fake_file_event = PerceptionEvent("file_system_event", {
        "event_type": "created",
        "file_name": "demo.txt",
        "file_extension": ".txt"
    })
    event_callback(fake_file_event)
    
    # 模拟屏幕变化
    fake_screen_event = PerceptionEvent("screen_changed", {
        "resolution": "1920x1080",
        "timestamp": "2024-01-01T12:00:00"
    })
    event_callback(fake_screen_event)
    
    print(f"\n2. 获取感知状态...")
    status = perception_manager.get_perception_status()
    for perception_type, is_active in status.items():
        print(f"   {perception_type}: {'✅ 活跃' if is_active else '❌ 停止'}")
    
    print(f"\n3. 总共收到 {len(events_received)} 个感知事件")

async def demo_proactive_behavior():
    """演示主动行为系统"""
    print("\n🤖 主动行为系统演示")
    print("-" * 30)
    
    from emotional_ai.proactive_behavior import get_proactive_engine, BehaviorType
    
    proactive_engine = get_proactive_engine()
    
    behaviors_triggered = []
    
    async def behavior_callback(behavior):
        behaviors_triggered.append(behavior)
        print(f"   触发行为: {behavior.behavior_type.value}")
        print(f"   消息: {behavior.message}")
        print(f"   优先级: {behavior.priority:.2f}")
    
    proactive_engine.add_behavior_callback(behavior_callback)
    
    print("1. 手动触发不同类型的行为...")
    
    # 触发不同类型的行为
    behavior_types = [
        BehaviorType.INITIATE_CHAT,
        BehaviorType.ASK_QUESTION,
        BehaviorType.SHARE_DISCOVERY,
        BehaviorType.EXPRESS_EMOTION
    ]
    
    for behavior_type in behavior_types:
        success = proactive_engine.manual_trigger_behavior(behavior_type)
        if success:
            print(f"   ✅ 成功触发: {behavior_type.value}")
        await asyncio.sleep(0.1)  # 短暂等待处理
    
    print(f"\n2. 获取行为队列状态...")
    queue_status = proactive_engine.get_behavior_queue_status()
    print(f"   队列长度: {queue_status['queue_length']}")
    print(f"   系统活跃: {queue_status['is_active']}")
    
    print(f"\n3. 总共触发了 {len(behaviors_triggered)} 个行为")

async def demo_exploration_system():
    """演示探索系统"""
    print("\n🧠 探索系统演示")
    print("-" * 30)
    
    from emotional_ai.auto_exploration import get_auto_exploration_engine
    
    exploration_engine = get_auto_exploration_engine()
    
    results_received = []
    
    def exploration_callback(result):
        results_received.append(result)
        print(f"   探索结果: {result.target.target_type} - {result.success}")
        if result.success and result.data:
            print(f"   数据摘要: {str(result.data)[:100]}...")
    
    exploration_engine.add_exploration_callback(exploration_callback)
    
    print("1. 手动触发探索任务...")
    
    # 触发搜索任务
    success = exploration_engine.manual_explore("search", "人工智能发展")
    if success:
        print("   ✅ 搜索任务已添加到队列")
    
    # 模拟等待处理
    await asyncio.sleep(0.5)
    
    print(f"\n2. 获取探索状态...")
    status = exploration_engine.get_exploration_status()
    print(f"   系统活跃: {status['is_active']}")
    print(f"   队列大小: {status['queue_size']}")
    print(f"   总探索次数: {status['total_explorations']}")
    
    print(f"\n3. 获取探索摘要...")
    summary = exploration_engine.get_exploration_summary()
    print(f"   摘要: {summary}")

async def demo_full_integration():
    """演示完整集成"""
    print("\n🎉 完整系统集成演示")
    print("-" * 30)
    
    from emotional_ai.emotional_ai_manager import get_emotional_ai_manager
    
    ai_manager = get_emotional_ai_manager()
    
    # 收集AI消息
    ai_messages = []
    
    async def message_callback(message):
        ai_messages.append(message)
        print(f"   🤖 {message['sender']}: {message['message']}")
    
    ai_manager.add_message_callback(message_callback)
    
    print("1. 启动情绪AI系统...")
    await ai_manager.start_emotional_ai()
    await asyncio.sleep(1)
    
    print("\n2. 模拟用户交互...")
    test_conversations = [
        "你好！",
        "你真聪明！",
        "我们来玩游戏吧！",
        "为什么天空是蓝色的？"
    ]
    
    for user_input in test_conversations:
        print(f"   👤 用户: {user_input}")
        response = await ai_manager.process_user_input(user_input)
        print(f"   🤖 AI: {response}")
        await asyncio.sleep(0.5)
    
    print("\n3. 手动触发功能...")
    await ai_manager.manual_trigger_thinking()
    await asyncio.sleep(0.5)
    
    await ai_manager.manual_search_knowledge("可爱的小动物")
    await asyncio.sleep(0.5)
    
    print("\n4. 获取系统状态...")
    status = ai_manager.get_system_status()
    print(f"   AI名称: {status['ai_info']['name']}")
    print(f"   心理年龄: {status['ai_info']['age']}岁")
    print(f"   主导情绪: {status['emotion_status']['dominant_emotion']['type']}")
    
    print(f"\n5. 收到了 {len(ai_messages)} 条AI消息")
    
    print("\n6. 停止系统...")
    ai_manager.stop_emotional_ai()

async def run_all_demos():
    """运行所有演示"""
    print("🎭 NagaAgent 情绪化AI系统演示")
    print("=" * 50)
    
    try:
        await demo_emotion_system()
        await demo_perception_system()
        await demo_proactive_behavior()
        await demo_exploration_system()
        await demo_full_integration()
        
        print("\n" + "=" * 50)
        print("✅ 所有演示完成！")
        print("\n💡 提示:")
        print("- 这只是基础演示，实际使用中功能更丰富")
        print("- 启用感知功能需要相应的硬件支持")
        print("- 配置API密钥后可获得更好的对话体验")
        
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保已正确安装所有依赖")
    except Exception as e:
        print(f"❌ 演示过程中出错: {e}")

def main():
    """主函数"""
    print("选择演示模式:")
    print("1. 完整演示（推荐）")
    print("2. 情绪系统演示")
    print("3. 感知系统演示")
    print("4. 主动行为演示")
    print("5. 探索系统演示")
    print("6. 系统集成演示")
    
    try:
        choice = input("\n请选择 (1-6): ").strip()
        
        if choice == "1":
            asyncio.run(run_all_demos())
        elif choice == "2":
            asyncio.run(demo_emotion_system())
        elif choice == "3":
            asyncio.run(demo_perception_system())
        elif choice == "4":
            asyncio.run(demo_proactive_behavior())
        elif choice == "5":
            asyncio.run(demo_exploration_system())
        elif choice == "6":
            asyncio.run(demo_full_integration())
        else:
            print("无效选择，运行完整演示...")
            asyncio.run(run_all_demos())
            
    except KeyboardInterrupt:
        print("\n演示被用户中断")
    except Exception as e:
        print(f"演示失败: {e}")

if __name__ == "__main__":
    main()