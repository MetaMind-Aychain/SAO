#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
离线模式启动脚本
禁用所有网络相关功能，确保系统可以在离线环境下运行
"""

import json
import os
import sys
from pathlib import Path

def create_offline_config():
    """创建离线模式配置"""
    try:
        # 读取原配置
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        print("🔧 配置离线模式...")
        
        # 禁用网络相关功能
        config["emotional_ai"]["advanced_features_enabled"] = False
        config["emotional_ai"]["camera_perception"] = False
        config["emotional_ai"]["microphone_perception"] = False
        config["emotional_ai"]["deep_reflection_enabled"] = False
        config["emotional_ai"]["personality_evolution"] = False
        config["emotional_ai"]["knowledge_graph_enabled"] = False
        config["emotional_ai"]["social_media_enabled"] = False
        
        # 禁用GRAG记忆系统中的Neo4j
        config["grag"]["enabled"] = False
        
        # 设置一个占位API key以避免验证错误
        config["api"]["api_key"] = "offline-mode"
        config["api"]["base_url"] = "http://localhost:8000"
        
        # 禁用Twitter
        if "twitter" in config:
            config["twitter"]["enabled"] = False
            config["twitter"]["auto_post_enabled"] = False
        
        # 保存离线配置
        backup_path = "config.json.backup"
        if not os.path.exists(backup_path):
            os.rename("config.json", backup_path)
            print(f"✅ 原配置已备份到: {backup_path}")
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ 离线配置已设置")
        return True
        
    except Exception as e:
        print(f"❌ 配置离线模式失败: {e}")
        return False

def start_offline():
    """启动离线模式"""
    print("🚀 NagaAgent 离线模式启动")
    print("=" * 50)
    
    # 设置环境变量禁用网络请求
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_HUB_OFFLINE"] = "1"
    
    # 创建离线配置
    if not create_offline_config():
        return False
    
    try:
        print("🎭 启动情绪AI系统（离线模式）...")
        
        # 导入并启动主程序
        import main
        
        print("✅ 系统启动成功！")
        print("\n💡 离线模式说明:")
        print("- 基础对话功能正常")
        print("- 情绪系统正常")
        print("- 高级网络功能已禁用")
        print("- 使用 restore_config.py 恢复完整配置")
        
        return True
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

if __name__ == "__main__":
    success = start_offline()
    if not success:
        print("\n💡 如果仍有问题，请检查:")
        print("1. Python环境是否正确")
        print("2. 依赖包是否完整安装")
        print("3. 使用 python main.py 直接启动")
        sys.exit(1)