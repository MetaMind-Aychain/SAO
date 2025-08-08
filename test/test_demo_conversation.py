#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试演示模式对话功能
"""

import asyncio
import os
import sys

async def test_demo_conversation():
    """测试演示对话功能"""
    try:
        # 设置演示模式环境变量
        os.environ["NAGAAGENT_DEMO_MODE"] = "1"
        
        print("🎭 测试演示模式对话功能")
        print("=" * 40)
        
        from conversation_core import NagaConversation
        
        # 创建对话实例
        naga = NagaConversation()
        
        if not naga.demo_mode:
            print("❌ 演示模式未启用")
            return False
        
        print("✅ 演示模式已启用")
        
        # 测试对话
        test_inputs = [
            "你好",
            "你真棒", 
            "为什么",
            "游戏",
            "test",
            "随便说点什么"
        ]
        
        for test_input in test_inputs:
            print(f"\n👤 用户: {test_input}")
            
            # 处理输入并获取响应
            response_text = ""
            async for response in naga.process(test_input):
                if response[0] == "StarryNight":
                    response_text = response[1]
                    break
            
            print(f"🤖 StarryNight: {response_text}")
            
            # 显示情绪状态
            if naga.emotional_ai:
                try:
                    emotions = naga.emotional_ai.current_emotions
                    if emotions:
                        emotion_display = f"[{emotions[0].emotion.value}: {emotions[0].intensity:.1f}]"
                        print(f"   情绪状态: {emotion_display}")
                except Exception as e:
                    print(f"   情绪状态获取失败: {e}")
        
        print("\n✅ 演示模式对话测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_demo_conversation())
    if success:
        print("\n🎉 演示模式正常工作！")
    else:
        print("\n💡 请检查配置和依赖")
        sys.exit(1)