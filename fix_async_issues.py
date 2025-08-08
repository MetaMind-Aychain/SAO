#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复异步初始化问题
为高级功能创建安全的初始化配置
"""

import json
from pathlib import Path

def create_safe_config():
    """创建安全的配置，避免异步问题"""
    config_file = Path("config.json")
    
    if not config_file.exists():
        print("❌ config.json文件不存在")
        return
    
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 安全的配置 - 逐步启用功能
    safe_config = {
        "advanced_features_enabled": True,  # 启用高级功能框架
        "camera_perception": False,         # 暂时关闭摄像头
        "microphone_perception": False,     # 暂时关闭麦克风
        "deep_reflection_enabled": False,   # 暂时关闭深度反思（避免异步问题）
        "personality_evolution": False,     # 暂时关闭性格演化（避免异步问题）
        "knowledge_graph_enabled": False,   # 暂时关闭知识图谱（避免异步问题）
        "social_media_enabled": False,      # 关闭社交媒体
        "autonomous_level": "restricted",   # 限制自主等级
        "memory_enabled": True,             # 保留基础记忆
        "auto_exploration": False           # 关闭自动探索
    }
    
    # 更新配置
    if "emotional_ai" not in config:
        config["emotional_ai"] = {}
    
    config["emotional_ai"].update(safe_config)
    
    # 确保grag配置存在但禁用
    config["grag"] = {"enabled": False}
    
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ 安全配置已应用")
    print("\n📋 当前配置状态:")
    print("✅ 基础情绪系统")
    print("✅ 记忆存储")
    print("✅ 语音播放")
    print("❌ 高级感知（暂时关闭）")
    print("❌ 深度反思（暂时关闭）")
    print("❌ 性格演化（暂时关闭）")
    print("❌ 知识图谱（暂时关闭）")
    print("\n💡 这样配置可以避免异步初始化问题")
    print("💡 系统稳定运行后可以在GUI中逐步启用高级功能")

def create_step_by_step_guide():
    """创建分步启用指南"""
    guide = """
# 🚀 分步启用高级功能指南

## 第一步：确保基础功能运行
运行 `python main.py` 确保以下功能正常：
- ✅ 基础情绪系统
- ✅ 记忆存储
- ✅ 语音播放
- ✅ 主动对话

## 第二步：配置API（如果需要深度反思）
在 config.json 中配置：
```json
{
  "api": {
    "api_key": "your_openai_api_key_here",
    "base_url": "https://api.openai.com/v1",
    "model_name": "gpt-3.5-turbo"
  }
}
```

## 第三步：在GUI中逐步启用功能
1. 启动程序：`python main.py`
2. 点击设置 → "🎭 情绪AI系统"
3. 逐一启用功能：
   - ✅ 深度反思功能
   - ✅ 性格演化
   - ✅ 知识图谱构建（如果有Neo4j）
   - ✅ 摄像头感知（如果需要）
   - ✅ 麦克风感知（如果需要）

## 第四步：测试高级功能
每启用一个功能后，观察：
- 控制台日志是否有错误
- AI行为是否正常
- 内存使用是否合理

## 第五步：配置可选服务（进阶）
### Neo4j图数据库：
```bash
docker run -d --name nagaai-neo4j \\
  -p 7474:7474 -p 7687:7687 \\
  -e NEO4J_AUTH=neo4j/your_password \\
  neo4j:latest
```

### Twitter API：
创建 .env 文件：
```
TWITTER_CONSUMER_KEY=your_key
TWITTER_CONSUMER_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret
```

## ⚠️ 重要提醒
- 一次只启用一个新功能
- 出现问题立即禁用该功能
- 使用"🚨 紧急停止"按钮控制自主行为
- 定期检查日志和内存使用

## 🆘 如果还有问题
1. 查看 `TROUBLESHOOTING_GUIDE.md`
2. 运行 `python offline_mode_setup.py` 降级到离线模式
3. 检查依赖：`python setup_advanced_features.py`
"""
    
    with open("STEP_BY_STEP_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("📖 分步指南已创建：STEP_BY_STEP_GUIDE.md")

if __name__ == "__main__":
    print("🔧 修复异步初始化问题")
    print("=" * 50)
    
    create_safe_config()
    create_step_by_step_guide()
    
    print("\n🎯 下一步操作：")
    print("1. 运行 python main.py 测试基础功能")
    print("2. 配置OpenAI API（如果需要深度功能）")
    print("3. 在GUI中逐步启用高级功能")
    print("4. 查看 STEP_BY_STEP_GUIDE.md 了解详细步骤")