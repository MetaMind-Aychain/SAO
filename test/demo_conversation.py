#!/usr/bin/env python3
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
