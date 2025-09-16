#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Alice Synthesis系统集成
验证所有Asuna相关功能是否正常工作
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def test_asuna_character_system():
    """测试Asuna性格系统"""
    try:
        from asuna_character_system import AsunaCharacterSystem
        from config import config
        
        print("🧪 测试Asuna性格系统...")
        
        # 创建性格系统
        character_system = AsunaCharacterSystem(config)
        
        # 测试获取当前性格
        personality = character_system.get_current_personality()
        print(f"✅ 当前性格: {personality.stage.value} - {personality.speech_style}")
        
        # 测试性格驱动回复
        response = character_system.generate_asuna_response("你好", "你好，我是爱丽丝...")
        print(f"✅ 性格回复: {response}")
        
        # 测试记忆摘要
        memory_summary = character_system.get_memory_summary()
        print(f"✅ 记忆摘要: {memory_summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Asuna性格系统测试失败: {e}")
        return False

async def test_asuna_memory_system():
    """测试Asuna记忆系统"""
    try:
        from asuna_memory_system import AsunaMemorySystem
        from config import config
        
        print("🧪 测试Asuna记忆系统...")
        
        # 创建记忆系统
        memory_system = AsunaMemorySystem(config)
        
        # 测试获取当前阶段（从配置中获取）
        stage = config.emotional_ai.asuna_memory_stage
        print(f"✅ 当前记忆阶段: {stage}")
        
        # 测试获取记忆摘要
        from asuna_character_system import AsunaMemoryStage
        summary = memory_system.get_memory_summary(AsunaMemoryStage.ANXIOUS)
        print(f"✅ 记忆摘要: {summary}")
        
        # 测试记忆恢复检查
        recovered = await memory_system.check_memory_recovery("我有一把细剑", AsunaMemoryStage.ANXIOUS)
        print(f"✅ 记忆恢复结果: {len(recovered)}个记忆")
        
        return True
        
    except Exception as e:
        print(f"❌ Asuna记忆系统测试失败: {e}")
        return False

async def test_asuna_language_system():
    """测试Asuna语言系统"""
    try:
        from asuna_language_system import AsunaLanguageSystem
        from config import config
        
        print("🧪 测试Asuna语言系统...")
        
        # 创建语言系统
        language_system = AsunaLanguageSystem(config)
        
        # 测试基础回复处理
        response = language_system.generate_response("你好", "你好，我是爱丽丝...", "anxious")
        print(f"✅ 基础回复: {response}")
        
        # 测试SAO术语集成
        sao_response = language_system._add_sao_elements("我有一把剑", "anxious")
        print(f"✅ SAO术语集成: {sao_response}")
        
        # 测试阶段化话术
        stage_response = language_system.generate_response("你是谁？", "我是爱丽丝...", "anxious")
        print(f"✅ 阶段化话术: {stage_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Asuna语言系统测试失败: {e}")
        return False

async def test_asuna_autonomous_behavior():
    """测试Asuna自主行为系统"""
    try:
        from asuna_autonomous_behavior import AsunaAutonomousBehavior
        from config import config
        
        print("🧪 测试Asuna自主行为系统...")
        
        # 创建自主行为系统
        behavior_system = AsunaAutonomousBehavior(config)
        
        # 测试获取行为状态
        status = behavior_system.get_behavior_status()
        print(f"✅ 行为状态: {status}")
        
        # 测试启动自主行为
        await behavior_system.start_autonomous_behavior()
        print("✅ 自主行为已启动")
        
        return True
        
    except Exception as e:
        print(f"❌ Asuna自主行为系统测试失败: {e}")
        return False

async def test_asuna_integration():
    """测试Asuna集成系统"""
    try:
        from asuna_integration import AsunaIntegration
        
        print("🧪 测试Asuna集成系统...")
        
        # 创建集成系统
        integration = AsunaIntegration()
        
        # 测试初始化
        await integration.initialize_asuna_systems()
        print(f"✅ 系统初始化状态: {integration.is_initialized}")
        
        # 测试获取系统提示词
        prompt = integration.get_asuna_system_prompt()
        print(f"✅ 系统提示词长度: {len(prompt)} 字符")
        
        # 测试用户交互处理
        result = await integration.process_user_interaction("你好", "你好，我是Asuna")
        print(f"✅ 交互处理结果: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Asuna集成系统测试失败: {e}")
        return False

async def test_conversation_core_integration():
    """测试对话核心集成"""
    try:
        from conversation_core import ConversationCore
        
        print("🧪 测试对话核心集成...")
        
        # 创建对话核心
        conversation_core = ConversationCore()
        
        # 测试Asuna集成是否可用
        if hasattr(conversation_core, 'asuna_integration'):
            print(f"✅ Asuna集成状态: {conversation_core.asuna_integration is not None}")
        else:
            print("❌ 对话核心中未找到Asuna集成")
            return False
        
        # 测试处理用户输入
        response = await conversation_core.process("你好，Asuna")
        print(f"✅ 对话回复: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 对话核心集成测试失败: {e}")
        return False

async def test_config_integration():
    """测试配置集成"""
    try:
        from config import config
        
        print("🧪 测试配置集成...")
        
        # 检查Asuna配置
        asuna_config = config.emotional_ai
        print(f"✅ AI名称: {asuna_config.ai_name}")
        print(f"✅ Asuna启用状态: {asuna_config.asuna_enabled}")
        print(f"✅ 记忆阶段: {asuna_config.asuna_memory_stage}")
        print(f"✅ SAO元素: {asuna_config.asuna_sao_elements}")
        print(f"✅ 自主行为: {asuna_config.asuna_autonomous_behavior}")
        
        # 检查AI名称是否正确
        if asuna_config.ai_name != "Alice Synthesis":
            print(f"❌ AI名称不正确: {asuna_config.ai_name}")
            return False
        
        # 检查系统提示词
        system_prompt = config.prompts.naga_system_prompt
        if "Asuna" in system_prompt and "SAO" in system_prompt:
            print("✅ 系统提示词包含Asuna和SAO元素")
        else:
            print("❌ 系统提示词缺少Asuna或SAO元素")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 配置集成测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 Alice Synthesis系统集成测试")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    tests = [
        ("配置集成", test_config_integration),
        ("Asuna性格系统", test_asuna_character_system),
        ("Asuna记忆系统", test_asuna_memory_system),
        ("Asuna语言系统", test_asuna_language_system),
        ("Asuna自主行为系统", test_asuna_autonomous_behavior),
        ("Asuna集成系统", test_asuna_integration),
        ("对话核心集成", test_conversation_core_integration),
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = await test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            test_results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！Asuna系统集成成功！")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查相关模块")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
