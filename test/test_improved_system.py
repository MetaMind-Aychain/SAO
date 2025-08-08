#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试改进后的真实化AI系统
"""

import asyncio
import os
import sys
import signal
import logging

async def test_persona_system():
    """测试人设系统"""
    print("🎭 测试人设管理系统...")
    
    try:
        from persona_management_system import get_persona_manager, record_ai_behavior, get_persona_prompt
        
        # 测试行为记录
        record_ai_behavior("test", "测试行为记录功能", emotional_impact=0.3)
        print("✅ 行为记录功能正常")
        
        # 测试人设提示词生成
        prompt = get_persona_prompt("测试对话上下文")
        print(f"✅ 人设提示词生成成功 (长度: {len(prompt)} 字符)")
        
        # 测试人设管理器
        manager = get_persona_manager()
        snapshot = manager.get_current_persona_snapshot()
        print(f"✅ 人设快照获取成功 - 情绪数: {len(snapshot.current_emotions)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 人设系统测试失败: {e}")
        return False

async def test_camera_frequency():
    """测试摄像头频率控制"""
    print("📷 测试摄像头频率控制...")
    
    try:
        from config import config
        from advanced_perception_system import CameraPerception
        from emotional_ai_core import get_emotion_core
        
        print(f"🔧 摄像头互动频率配置: {config.emotional_ai.camera_interaction_frequency}")
        print(f"🔧 情绪阈值配置: {config.emotional_ai.emotion_threshold_for_llm}")
        
        # 测试摄像头初始化
        emotion_core = get_emotion_core(config)
        camera = CameraPerception(emotion_core)
        print(f"✅ 摄像头频率控制器初始化成功 - 每{camera.camera_frequency_divisor}次分析触发1次互动")
        
        return True
        
    except Exception as e:
        print(f"❌ 摄像头频率测试失败: {e}")
        return False

async def test_conversation_integration():
    """测试对话集成"""
    print("💬 测试对话系统集成...")
    
    try:
        from conversation_core import NagaConversation
        
        # 创建对话实例
        naga = NagaConversation()
        
        if naga.demo_mode:
            print("⚠️ 当前处于演示模式")
        else:
            print("✅ 联网模式已启用")
        
        # 测试简单对话
        test_message = "你好"
        
        response_count = 0
        async for response in naga.process(test_message):
            if response[0] == "StarryNight":
                response_count += 1
                if response_count == 1:  # 只显示第一行
                    print(f"✅ 对话测试成功: {response[1][:100]}...")
                break
        
        return True
        
    except Exception as e:
        print(f"❌ 对话集成测试失败: {e}")
        return False

async def test_api_connection():
    """测试API连接"""
    print("🔗 测试API连接...")
    
    try:
        from conversation_core import call_llm_api
        from config import config
        
        if config.api.api_key == "demo-mode" or not config.api.api_key:
            print("⚠️ 演示模式或API密钥未配置")
            return True
        
        # 测试API调用
        response = await call_llm_api("请回复'测试成功'", max_tokens=20)
        
        if "测试" in response or "成功" in response or len(response) > 0:
            print(f"✅ API连接正常: {response[:50]}...")
            return True
        else:
            print(f"⚠️ API响应异常: {response}")
            return False
            
    except Exception as e:
        print(f"❌ API连接测试失败: {e}")
        return False

def test_config_validation():
    """测试配置验证"""
    print("⚙️ 测试配置验证...")
    
    try:
        from config import config
        
        # 检查关键配置
        print(f"📡 API配置: {config.api.base_url}")
        print(f"🔑 模型: {config.api.model}")
        print(f"🎭 情绪AI: {'启用' if config.emotional_ai.advanced_features_enabled else '禁用'}")
        print(f"📷 摄像头感知: {'启用' if config.emotional_ai.camera_perception else '禁用'}")
        print(f"🎤 麦克风感知: {'启用' if config.emotional_ai.microphone_perception else '禁用'}")
        print(f"🧠 深度反思: {'启用' if config.emotional_ai.deep_reflection_enabled else '禁用'}")
        print(f"📊 知识图谱: {'启用' if config.emotional_ai.knowledge_graph_enabled else '禁用'}")
        print(f"📱 社交媒体: {'启用' if config.emotional_ai.social_media_enabled else '禁用'}")
        
        # 检查新配置
        print(f"🎯 摄像头频率: {config.emotional_ai.camera_interaction_frequency}")
        print(f"🎯 情绪阈值: {config.emotional_ai.emotion_threshold_for_llm}")
        print(f"🎯 人设更新: {'启用' if config.emotional_ai.persona_update_enabled else '禁用'}")
        print(f"🎯 行为记录: {'启用' if config.emotional_ai.behavior_recording_enabled else '禁用'}")
        
        print("✅ 配置验证完成")
        return True
        
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🌟 NagaAgent 真实化AI系统测试")
    print("=" * 50)
    
    # 设置信号处理
    def signal_handler(signum, frame):
        print("\n⚠️ 收到中断信号，正在退出...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    tests = [
        ("配置验证", lambda: test_config_validation()),
        ("人设系统", test_persona_system),
        ("摄像头频率控制", test_camera_frequency),
        ("API连接", test_api_connection),
        ("对话集成", test_conversation_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}测试...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await asyncio.wait_for(test_func(), timeout=30)
            else:
                result = test_func()
            results.append((test_name, result))
        except asyncio.TimeoutError:
            print(f"❌ {test_name}测试超时")
            results.append((test_name, False))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！系统已准备就绪")
        print("💡 现在可以运行 python main.py 启动完整系统")
    elif passed >= len(results) * 0.7:
        print("⚠️ 大部分功能正常，可以尝试启动系统")
    else:
        print("❌ 多项测试失败，建议检查配置和依赖")
    
    return passed == len(results)

if __name__ == "__main__":
    try:
        # 设置日志级别
        logging.basicConfig(level=logging.WARNING)
        
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