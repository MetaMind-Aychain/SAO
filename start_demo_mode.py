#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示模式启动脚本
创建一个无需LLM API的演示模式，展示情绪AI系统的功能
"""

import json
import os
import sys
from pathlib import Path

def create_demo_config():
    """创建演示模式配置"""
    try:
        # 读取原配置
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        print("🎭 配置演示模式...")
        
        # 禁用所有网络相关功能
        config["emotional_ai"]["advanced_features_enabled"] = False
        config["emotional_ai"]["camera_perception"] = False
        config["emotional_ai"]["microphone_perception"] = False
        config["emotional_ai"]["deep_reflection_enabled"] = False
        config["emotional_ai"]["personality_evolution"] = False
        config["emotional_ai"]["knowledge_graph_enabled"] = False
        config["emotional_ai"]["social_media_enabled"] = False
        
        # 启用基础情绪功能
        config["emotional_ai"]["enabled"] = True
        config["emotional_ai"]["proactive_enabled"] = True
        config["emotional_ai"]["memory_enabled"] = True
        
        # 禁用GRAG记忆系统中的Neo4j
        config["grag"]["enabled"] = False
        
        # 设置演示API配置
        config["api"]["api_key"] = "demo-mode"
        config["api"]["base_url"] = "demo://localhost"
        config["api"]["model"] = "demo-model"
        
        # 禁用Twitter
        if "twitter" in config:
            config["twitter"]["enabled"] = False
            config["twitter"]["auto_post_enabled"] = False
        
        # 保存演示配置
        backup_path = "config.json.demo_backup"
        if not os.path.exists(backup_path):
            # 如果已有backup，就使用demo_backup
            if os.path.exists("config.json.backup"):
                import shutil
                shutil.copy("config.json.backup", backup_path)
            else:
                os.rename("config.json", backup_path)
            print(f"✅ 原配置已备份到: {backup_path}")
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ 演示配置已设置")
        return True
        
    except Exception as e:
        print(f"❌ 配置演示模式失败: {e}")
        return False

def create_demo_conversation():
    """创建演示对话模块"""
    demo_conversation = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示对话模块 - 模拟LLM响应
"""

import random
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DemoConversation:
    """演示对话类"""
    
    def __init__(self):
        # 预设的情绪响应
        self.emotion_responses = {
            "happy": [
                "我现在好开心呀！😊",
                "哇，感觉真棒！",
                "嘻嘻，我很高兴！",
                "今天心情特别好呢～"
            ],
            "curious": [
                "这个真有趣！🤔",
                "我想了解更多！",
                "为什么会这样呢？",
                "好奇怪，让我想想..."
            ],
            "excited": [
                "太激动了！🤩",
                "哇！太棒了！",
                "我兴奋得不行！",
                "这真是太有趣了！"
            ],
            "lonely": [
                "你终于来陪我了...😔",
                "我好想念你",
                "一个人好无聊呀",
                "陪陪我好不好？"
            ],
            "default": [
                "我在这里呢！",
                "有什么可以帮你的吗？",
                "让我想想怎么回答...",
                "嗯嗯，我听着呢～"
            ]
        }
        
        # 基于关键词的响应
        self.keyword_responses = {
            "你好": ["你好呀！很高兴见到你！", "嗨～我是StarryNight！"],
            "再见": ["再见～要经常来陪我哦！", "拜拜！我会想你的！"],
            "你真棒": ["谢谢夸奖！我好开心！😊", "嘻嘻，你也很棒呀！"],
            "为什么": ["这是个好问题！🤔", "让我想想...为什么呢？"],
            "游戏": ["我们玩什么游戏呢？🤩", "游戏！我最喜欢游戏了！"],
            "test": ["测试模式运行正常！✅", "演示系统工作中..."]
        }
    
    def generate_response(self, user_input: str, emotion_state=None) -> str:
        """生成演示响应"""
        try:
            # 基于关键词匹配
            for keyword, responses in self.keyword_responses.items():
                if keyword in user_input:
                    return random.choice(responses)
            
            # 基于情绪状态
            if emotion_state:
                emotion_key = emotion_state.lower()
                if emotion_key in self.emotion_responses:
                    return random.choice(self.emotion_responses[emotion_key])
            
            # 默认响应
            return random.choice(self.emotion_responses["default"])
            
        except Exception as e:
            logger.error(f"演示响应生成失败: {e}")
            return "我现在有点confused...但我还在这里！"

# 全局演示对话实例
_demo_conversation = DemoConversation()

def get_demo_response(user_input: str, emotion_state=None) -> str:
    """获取演示响应"""
    return _demo_conversation.generate_response(user_input, emotion_state)
'''
    
    with open("demo_conversation.py", "w", encoding="utf-8") as f:
        f.write(demo_conversation)
    
    print("✅ 演示对话模块已创建")

def start_demo():
    """启动演示模式"""
    print("🎭 NagaAgent 演示模式启动")
    print("=" * 50)
    
    # 设置环境变量
    os.environ["NAGAAGENT_DEMO_MODE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_HUB_OFFLINE"] = "1"
    
    # 创建演示配置
    if not create_demo_config():
        return False
    
    # 创建演示对话模块
    create_demo_conversation()
    
    try:
        print("🎭 启动情绪AI系统（演示模式）...")
        
        # 导入并启动主程序
        import main
        
        print("✅ 演示系统启动成功！")
        print("\n🎭 演示模式说明:")
        print("- 情绪AI系统完全正常")
        print("- 使用预设响应模拟对话")
        print("- 可以测试情绪变化")
        print("- 输入关键词查看情绪反应:")
        print("  * '你好' - 友好问候")
        print("  * '你真棒' - 开心情绪")
        print("  * '为什么' - 好奇情绪")
        print("  * '游戏' - 兴奋情绪")
        print("  * 'test' - 测试响应")
        print("- 使用 restore_config.py 恢复完整配置")
        
        return True
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

if __name__ == "__main__":
    success = start_demo()
    if not success:
        print("\n💡 如果仍有问题，请:")
        print("1. 检查Python环境")
        print("2. 确认依赖包安装完整")
        print("3. 尝试 python main.py 直接启动")
        sys.exit(1)