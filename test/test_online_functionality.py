#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
联网模式功能测试脚本
测试所有修复的功能是否正常工作
"""

import asyncio
import os
import sys

async def test_online_functionality():
    """测试联网模式功能"""
    try:
        print("🌐 测试联网模式功能")
        print("=" * 50)
        
        # 清除演示模式环境变量
        env_vars = ["NAGAAGENT_DEMO_MODE", "TRANSFORMERS_OFFLINE", "HF_HUB_OFFLINE"]
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]
        
        from conversation_core import NagaConversation, call_llm_api
        
        # 创建对话实例
        print("✅ 创建对话实例...")
        naga = NagaConversation()
        
        if naga.demo_mode:
            print("❌ 仍处于演示模式")
            return False
        
        print("✅ 联网模式已启用")
        
        # 测试LLM API调用
        print("\n🧪 测试LLM API调用...")
        try:
            response = await call_llm_api("请回复'测试成功'", max_tokens=50)
            if "测试成功" in response or "成功" in response:
                print(f"✅ LLM API测试成功: {response}")
            else:
                print(f"⚠️ LLM API响应: {response}")
        except Exception as e:
            print(f"❌ LLM API测试失败: {e}")
            return False
        
        # 测试完整对话
        print("\n💬 测试完整对话...")
        test_message = "你好，这是一个测试"
        
        response_text = ""
        async for response in naga.process(test_message):
            if response[0] == "StarryNight":
                response_text = response[1]
                break
        
        if response_text and "API调用失败" not in response_text:
            print(f"✅ 对话测试成功: {response_text[:100]}...")
        else:
            print(f"❌ 对话测试失败: {response_text}")
            return False
        
        # 测试情绪AI
        print("\n🎭 测试情绪AI...")
        if naga.emotional_ai:
            emotions = naga.emotional_ai.current_emotions
            if emotions:
                emotion_display = f"[{emotions[0].emotion.value}: {emotions[0].intensity:.1f}]"
                print(f"✅ 情绪系统正常: {emotion_display}")
            else:
                print("⚠️ 暂无情绪状态")
        else:
            print("❌ 情绪AI未启用")
        
        # 测试记忆系统
        print("\n🧠 测试记忆系统...")
        if naga.emotional_ai and naga.emotional_ai.memory_system:
            try:
                await naga.emotional_ai.memory_system.store_memory(
                    memory_type="test",
                    content="测试记忆存储",
                    emotion_state="快乐",
                    importance=0.5,
                    tags=["test"],
                    source="test"
                )
                print("✅ 记忆系统测试成功")
            except Exception as e:
                print(f"❌ 记忆系统测试失败: {e}")
                return False
        else:
            print("⚠️ 记忆系统未启用")
        
        print("\n🎉 所有功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_online_functionality())
    if success:
        print("\n✅ 联网模式功能完全正常！")
        print("🚀 现在可以启动main.py体验完整功能")
    else:
        print("\n❌ 仍有问题需要修复")
        sys.exit(1)