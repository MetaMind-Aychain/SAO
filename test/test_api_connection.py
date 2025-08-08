#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API连接测试脚本
测试各种API配置是否正常工作
"""

import json
import sys
from config import load_config

def test_api_connection():
    """测试API连接"""
    try:
        # 加载配置
        print("🔧 加载配置...")
        config = load_config()
        
        # 检查API配置
        print(f"📡 API配置:")
        print(f"  - Base URL: {config.api.base_url}")
        print(f"  - Model: {config.api.model}")
        print(f"  - API Key: {'已设置' if config.api.api_key else '未设置'}")
        
        # 测试简单API调用
        try:
            import openai
            client = openai.OpenAI(
                api_key=config.api.api_key,
                base_url=config.api.base_url
            )
            
            print("🧪 测试API连接...")
            response = client.chat.completions.create(
                model=config.api.model,
                messages=[{"role": "user", "content": "测试连接，请回复'OK'"}],
                max_tokens=10,
                temperature=0.1
            )
            
            print("✅ API连接成功!")
            print(f"回复: {response.choices[0].message.content}")
            return True
            
        except Exception as e:
            print(f"❌ API连接失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 NagaAgent API连接测试")
    print("=" * 50)
    
    success = test_api_connection()
    
    if not success:
        print("\n💡 解决建议:")
        print("1. 检查config.json中的api_key是否正确")
        print("2. 检查网络连接")
        print("3. 检查API服务商是否正常")
        print("4. 考虑使用离线模式运行")
        sys.exit(1)
    else:
        print("\n🎉 API连接正常，可以正常使用!")