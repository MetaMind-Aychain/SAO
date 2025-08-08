#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
离线模式配置
为无网络环境配置基础AI功能
"""

import json
from pathlib import Path

def setup_offline_mode():
    """配置离线模式"""
    print("🔌 配置离线模式")
    print("在离线模式下，部分功能将被禁用，但基础AI功能仍可正常使用")
    
    config_file = Path("config.json")
    if not config_file.exists():
        print("❌ config.json文件不存在")
        return
    
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 离线模式配置
    offline_config = {
        "advanced_features_enabled": False,  # 禁用高级功能
        "camera_perception": False,
        "microphone_perception": False,
        "deep_reflection_enabled": False,  # 需要LLM API
        "personality_evolution": True,  # 可以离线运行
        "knowledge_graph_enabled": False,  # 需要嵌入模型
        "social_media_enabled": False,  # 需要网络
        "autonomous_level": "restricted",
        "memory_enabled": True,  # 基础记忆可以离线
        "auto_exploration": False  # 需要网络搜索
    }
    
    # 禁用GRAG
    config["grag"] = {"enabled": False}
    
    # 更新emotional_ai配置
    if "emotional_ai" not in config:
        config["emotional_ai"] = {}
    
    config["emotional_ai"].update(offline_config)
    
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ 离线模式配置完成")
    print("\n📋 离线模式功能:")
    print("✅ 基础情绪系统")
    print("✅ 记忆存储 (SQLite)")
    print("✅ 性格演化")
    print("✅ 语音播放")
    print("❌ 摄像头/麦克风感知")
    print("❌ 深度反思 (需要LLM)")
    print("❌ 网络搜索")
    print("❌ 社交媒体")
    print("❌ 知识图谱")

if __name__ == "__main__":
    setup_offline_mode()