#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试真实Asuna AI集成
验证AI连接和降级模式
"""

import asyncio
import logging
from config import config
from asuna_integration import get_asuna_integration

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_real_asuna_ai():
    """测试真实Asuna AI集成"""
    print("=" * 60)
    print("🧪 测试真实Asuna AI集成")
    print("=" * 60)
    
    try:
        # 获取Asuna集成
        asuna_integration = get_asuna_integration()
        
        # 初始化Asuna系统
        print("🚀 初始化Asuna系统...")
        await asuna_integration.initialize_asuna_systems()
        
        # 检查AI状态
        status = asuna_integration.get_asuna_status()
        print(f"✅ Asuna系统状态: {status['status']}")
        
        if 'ai_generator_info' in status:
            ai_status = status['ai_generator_info']
            print(f"🤖 AI可用性: {ai_status['ai_available']}")
            print(f"🔄 降级模式: {ai_status['fallback_mode']}")
            print(f"🔗 客户端初始化: {ai_status['client_initialized']}")
            print(f"🧩 子系统加载: {ai_status['subsystems_loaded']}")
        
        # 测试AI回复
        print("\n" + "=" * 40)
        print("💬 测试AI回复生成")
        print("=" * 40)
        
        test_inputs = [
            "你好，你是谁？",
            "这里是什么地方？",
            "我有点害怕...",
            "你能帮我整理文件吗？",
            "我们一起玩游戏吧！"
        ]
        
        for i, user_input in enumerate(test_inputs, 1):
            print(f"\n📝 测试 {i}: {user_input}")
            
            try:
                # 处理用户交互
                result = await asuna_integration.process_user_interaction(user_input, "")
                
                print(f"🤖 Asuna回复: {result['asuna_response']}")
                print(f"📊 阶段: {result['stage']}")
                print(f"🔄 AI模式: {result.get('ai_mode', 'unknown')}")
                print(f"💭 记忆恢复: {len(result.get('memory_recovered', []))}个")
                
                # 等待一下避免过快请求
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ 测试失败: {e}")
        
        # 测试降级模式
        print("\n" + "=" * 40)
        print("🔄 测试降级模式")
        print("=" * 40)
        
        # 模拟AI不可用的情况
        if asuna_integration.ai_generator:
            original_ai_available = asuna_integration.ai_generator.ai_available
            asuna_integration.ai_generator.ai_available = False
            asuna_integration.ai_generator.fallback_mode = True
            
            print("🔄 切换到降级模式...")
            
            result = await asuna_integration.process_user_interaction("你好，测试降级模式", "")
            print(f"🔄 降级回复: {result['asuna_response']}")
            print(f"🔄 AI模式: {result.get('ai_mode', 'unknown')}")
            
            # 恢复原始状态
            asuna_integration.ai_generator.ai_available = original_ai_available
            asuna_integration.ai_generator.fallback_mode = not original_ai_available
        
        print("\n✅ 真实Asuna AI集成测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        logger.exception("测试过程中发生错误")

async def test_ai_connection():
    """测试AI连接"""
    print("\n" + "=" * 40)
    print("🔗 测试AI连接")
    print("=" * 40)
    
    try:
        from asuna_ai_integration import get_asuna_ai_generator
        
        ai_generator = get_asuna_ai_generator(config)
        status = ai_generator.get_status()
        
        print(f"🤖 AI可用: {status['ai_available']}")
        print(f"🔄 降级模式: {status['fallback_mode']}")
        print(f"🔗 客户端初始化: {status['client_initialized']}")
        
        if status['ai_available']:
            print("✅ AI连接正常")
            
            # 测试简单AI调用
            test_response = await ai_generator.generate_response("你好", {
                'stage': 'anxious',
                'personality': None,
                'memories': [],
                'interaction_count': 0,
                'care_count': 0
            })
            print(f"🤖 AI测试回复: {test_response}")
        else:
            print("⚠️ AI不可用，将使用降级模式")
            
    except Exception as e:
        print(f"❌ AI连接测试失败: {e}")
        logger.exception("AI连接测试错误")

async def main():
    """主函数"""
    print("🚀 开始真实Asuna AI集成测试")
    
    # 测试AI连接
    await test_ai_connection()
    
    # 测试完整集成
    await test_real_asuna_ai()
    
    print("\n🎉 所有测试完成！")

if __name__ == "__main__":
    asyncio.run(main())


