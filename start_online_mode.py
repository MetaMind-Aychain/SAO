#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
联网模式启动脚本
启用所有高级功能，包括在线模型、API调用、社交媒体等
"""

import os
import sys
import json
from pathlib import Path

def ensure_online_config():
    """确保联网模式配置正确"""
    try:
        # 读取配置
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        print("🌐 配置联网模式...")
        
        # 启用所有高级功能
        config["emotional_ai"]["advanced_features_enabled"] = True
        config["emotional_ai"]["camera_perception"] = True
        config["emotional_ai"]["microphone_perception"] = True
        config["emotional_ai"]["deep_reflection_enabled"] = True
        config["emotional_ai"]["personality_evolution"] = True
        config["emotional_ai"]["knowledge_graph_enabled"] = True
        config["emotional_ai"]["social_media_enabled"] = True
        
        # 启用GRAG记忆系统
        config["grag"]["enabled"] = True
        
        # 启用Twitter
        if "twitter" in config:
            config["twitter"]["enabled"] = True
            config["twitter"]["auto_post_enabled"] = True
        
        # 确保API配置不是演示模式
        if config["api"]["api_key"] == "demo-mode":
            print("⚠️ 检测到演示模式API配置，请设置正确的API密钥")
            return False
        
        # 保存配置
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ 联网模式配置已设置")
        return True
        
    except Exception as e:
        print(f"❌ 配置联网模式失败: {e}")
        return False

def check_dependencies():
    """检查依赖库"""
    print("🔍 检查必要依赖...")
    
    missing_deps = []
    
    try:
        import sentence_transformers
        print("✅ sentence-transformers")
    except ImportError:
        missing_deps.append("sentence-transformers")
    
    try:
        import tweepy
        print("✅ tweepy")
    except ImportError:
        missing_deps.append("tweepy")
    
    try:
        import py2neo
        print("✅ py2neo")
    except ImportError:
        missing_deps.append("py2neo")
    
    if missing_deps:
        print(f"❌ 缺少依赖: {', '.join(missing_deps)}")
        print("请运行: pip install " + " ".join(missing_deps))
        return False
    
    print("✅ 所有依赖检查通过")
    return True

def start_online():
    """启动联网模式"""
    print("🌐 NagaAgent 联网模式启动")
    print("=" * 50)
    
    # 清除所有离线环境变量
    env_vars_to_clear = [
        "NAGAAGENT_DEMO_MODE",
        "TRANSFORMERS_OFFLINE", 
        "HF_HUB_OFFLINE"
    ]
    
    for var in env_vars_to_clear:
        if var in os.environ:
            del os.environ[var]
            print(f"✅ 清除环境变量: {var}")
    
    # 确保配置正确
    if not ensure_online_config():
        return False
    
    # 检查依赖
    if not check_dependencies():
        print("\n💡 可以运行 `pip install -r requirements.txt` 安装所有依赖")
        return False
    
    try:
        print("🚀 启动完整NagaAgent系统...")
        
        # 导入并启动主程序
        import main
        
        print("✅ 联网模式启动成功！")
        print("\n🌐 联网模式特性:")
        print("- ✅ 完整LLM对话功能")
        print("- ✅ 情绪AI系统")
        print("- ✅ 高级感知系统（摄像头、麦克风）")
        print("- ✅ 在线模型下载和更新")
        print("- ✅ GRAG知识图谱记忆")
        print("- ✅ 深度反思和学习")
        print("- ✅ 性格演化系统")
        print("- ✅ 社交媒体集成")
        print("- ✅ 自主探索和学习")
        print("\n💡 使用说明:")
        print("- 可以进行完整的AI对话")
        print("- AI会主动探索和学习")
        print("- 支持语音输入输出")
        print("- 具备完整的情绪和记忆系统")
        
        return True
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = start_online()
    if not success:
        print("\n💡 故障排除建议:")
        print("1. 检查API密钥配置是否正确")
        print("2. 确认网络连接正常")
        print("3. 运行 python test_api_connection.py 测试API")
        print("4. 如果仍有问题，可以使用 python start_demo_mode.py 启动演示模式")
        sys.exit(1)