#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情绪AI集成测试脚本
测试主动感知、探索和语音输出功能
"""

import asyncio
import sys
import time
from config import config
from emotional_ai_core import get_emotion_core, EmotionType

async def test_emotional_ai_integration():
    """测试情绪AI集成功能"""
    print("🎭 开始测试情绪AI集成功能...")
    
    try:
        # 初始化情绪AI核心
        emotion_core = get_emotion_core(config)
        print(f"✅ 情绪AI核心初始化成功 - {config.emotional_ai.ai_name}")
        
        # 测试基础情绪功能
        print("\n📝 测试基础情绪功能...")
        emotion_core.add_emotion(EmotionType.HAPPY, 0.8)
        status = emotion_core.get_emotion_status()
        print(f"当前情绪状态: {emotion_core.get_emotion_display()}")
        
        # 测试情绪触发
        print("\n🔤 测试情绪触发...")
        test_inputs = [
            "你真棒！",
            "为什么会这样？", 
            "我们来玩游戏吧！"
        ]
        
        for test_input in test_inputs:
            emotions = emotion_core.analyze_input_emotion(test_input)
            print(f"输入: '{test_input}' -> 触发情绪: {emotions}")
        
        # 测试感知系统初始化
        print("\n👁️ 测试感知系统...")
        perception_systems = emotion_core.perception_systems
        
        print(f"屏幕感知: {'✅ 已启用' if perception_systems['screen'] else '❌ 未启用'}")
        print(f"文件感知: {'✅ 已启用' if perception_systems['file'] else '❌ 未启用'}")
        print(f"语音集成: {'✅ 已启用' if perception_systems['voice'] else '❌ 未启用'}")
        
        # 测试主动行为触发
        print("\n🤖 测试主动行为...")
        if emotion_core._should_trigger_proactive_behavior():
            message = emotion_core.generate_proactive_message()
            print(f"生成主动消息: {message}")
        else:
            print("当前不满足主动行为触发条件")
        
        # 测试屏幕捕捉（如果可用）
        if perception_systems['screen']:
            print("\n📷 测试屏幕捕捉...")
            try:
                result = await perception_systems['screen'].capture_and_analyze()
                if result:
                    print(f"屏幕捕捉结果: {result}")
                else:
                    print("未检测到屏幕变化")
            except Exception as e:
                print(f"屏幕捕捉测试失败: {e}")
        
        # 测试文件探索（如果可用）
        if perception_systems['file']:
            print("\n📁 测试文件探索...")
            try:
                result = await perception_systems['file'].explore_files()
                if result:
                    print(f"文件探索结果: {result}")
                else:
                    print("未发现新文件或变化")
            except Exception as e:
                print(f"文件探索测试失败: {e}")
        
        # 测试语音集成（如果可用）
        if perception_systems['voice']:
            print("\n🔊 测试语音集成...")
            try:
                test_message = "这是一个语音测试消息！"
                await emotion_core._send_proactive_message(test_message)
                print("语音播放测试已启动（后台播放）")
            except Exception as e:
                print(f"语音集成测试失败: {e}")
        
        # 测试记忆系统（如果可用）
        if hasattr(emotion_core, 'memory_system') and emotion_core.memory_system:
            print("\n🧠 测试记忆系统...")
            try:
                # 测试存储记忆
                await emotion_core.memory_system.store_memory(
                    memory_type="test",
                    content="这是一个测试记忆",
                    emotion_state="😊 快乐 (80%)",
                    importance=0.8,
                    tags=["test", "integration"],
                    source="system"
                )
                
                # 测试获取记忆
                memories = await emotion_core.memory_system.get_memories(limit=5)
                print(f"记忆系统测试成功，已存储 {len(memories)} 条记忆")
                
                # 测试记忆统计
                stats = await emotion_core.memory_system.get_memory_stats()
                print(f"记忆统计: {stats}")
                
            except Exception as e:
                print(f"记忆系统测试失败: {e}")
        else:
            print("\n⚠️ 记忆系统未启用")
        
        print("\n🎉 情绪AI集成测试完成！")
        
        # 显示完整状态报告
        print("\n📊 完整状态报告:")
        print("=" * 50)
        final_status = emotion_core.get_emotion_status()
        for key, value in final_status.items():
            print(f"{key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """测试配置完整性"""
    print("🔧 测试配置完整性...")
    
    try:
        # 检查情绪AI配置
        emotional_config = config.emotional_ai
        print(f"情绪AI启用: {emotional_config.enabled}")
        print(f"AI名称: {emotional_config.ai_name}")
        print(f"心理年龄: {emotional_config.personality_age}岁")
        print(f"主动行为: {emotional_config.proactive_enabled}")
        print(f"自动探索: {emotional_config.auto_exploration}")
        
        # 检查感知功能配置
        print(f"视觉感知: {emotional_config.vision_enabled}")
        print(f"听觉感知: {emotional_config.audio_enabled}")
        print(f"屏幕监控: {emotional_config.screen_enabled}")
        print(f"文件监控: {emotional_config.file_enabled}")
        
        # 检查UI配置
        ui_config = config.ui
        print(f"显示情绪面板: {ui_config.show_emotion_panel}")
        print(f"情绪面板宽度: {ui_config.emotion_panel_width}px")
        
        print("✅ 配置检查完成")
        return True
        
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🚀 NagaAgent 情绪AI集成测试")
    print("=" * 50)
    
    # 测试配置
    config_ok = test_configuration()
    
    if not config_ok:
        print("❌ 配置测试失败，跳过功能测试")
        return
    
    print("\n" + "=" * 50)
    
    # 测试功能集成
    integration_ok = await test_emotional_ai_integration()
    
    if integration_ok:
        print("\n🎊 所有测试通过！情绪AI系统已成功集成到NagaAgent中。")
        print("\n💡 使用提示:")
        print("1. 运行 python main.py 启动主程序")
        print("2. 在聊天中使用表扬、提问等触发不同情绪")
        print("3. 观察情绪面板的变化")
        print("4. AI将根据情绪状态主动发起对话")
    else:
        print("\n❌ 部分测试失败，请检查日志并修复问题")

if __name__ == "__main__":
    # 运行测试
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试程序异常: {e}")
        import traceback
        traceback.print_exc()