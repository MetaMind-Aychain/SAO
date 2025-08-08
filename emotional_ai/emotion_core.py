# emotional_ai/emotion_core.py
"""
AI情绪系统核心模块
实现3岁心理年龄的情绪化AI系统
"""

import asyncio
import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class EmotionType(Enum):
    """情绪类型枚举"""
    HAPPY = "Happy"          # 😊
    SAD = "Sad"            # 😢
    CURIOUS = "Curious"        # 🤔
    EXCITED = "Excited"        # 🤩
    LONELY = "Lonely"         # 😔
    SURPRISED = "Surprised"      # 😲
    ANGRY = "Angry"          # 😠
    SLEEPY = "Sleepy"         # 😴
    PLAYFUL = "Playful"        # 😈
    LOVING = "Loving"         # 😍

@dataclass
class EmotionState:
    """情绪状态数据类"""
    emotion: EmotionType
    intensity: float  # 0.0-1.0 情绪强度
    timestamp: datetime
    duration: float = 0.0  # 持续时间（秒）
    decay_rate: float = 0.1  # 衰减率
    
    def is_expired(self, max_duration: float = 300.0) -> bool:
        """检查情绪是否过期"""
        return (datetime.now() - self.timestamp).total_seconds() > max_duration

@dataclass
class PersonalityTraits:
    """个性特征"""
    curiosity: float = 0.8      # 好奇心
    playfulness: float = 0.9    # 顽皮度
    neediness: float = 0.7      # 需要陪伴度
    intelligence: float = 0.8   # 聪明度
    stubbornness: float = 0.6   # 任性度
    energy_level: float = 0.8   # 精力水平
    
    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return asdict(self)

class EmotionEngine:
    """情绪引擎 - 管理AI的情绪状态和变化"""
    
    def __init__(self):
        self.current_emotions: List[EmotionState] = []
        self.personality = PersonalityTraits()
        self.interaction_history: List[Dict] = []
        self.last_interaction_time = datetime.now()
        self.energy_level = 1.0  # 精力水平
        self.social_satisfaction = 0.5  # 社交满足度
        self.exploration_satisfaction = 0.5  # 探索满足度
        
        # 情绪触发词典
        self.emotion_triggers = {
            EmotionType.HAPPY: ["Good", "Smart", "Great", "Amazing", "Praise", "Compliment"],
            EmotionType.EXCITED: ["Game", "Play", "Interesting", "Surprise", "Adventure"],
            EmotionType.CURIOUS: ["Why", "How", "What", "Where", "Who"],
            EmotionType.PLAYFUL: ["Funny", "Playful", "Prank", "Joke"],
            EmotionType.LOVING: ["Love", "Kiss", "Hug", "Cuddle"],
            EmotionType.SAD: ["Don't", "Dislike", "Sad", "Cry"],
        }
        
        # 情绪表情映射
        self.emotion_emojis = {
            EmotionType.HAPPY: "😊",
            EmotionType.SAD: "😢", 
            EmotionType.CURIOUS: "🤔",
            EmotionType.EXCITED: "🤩",
            EmotionType.LONELY: "😔",
            EmotionType.SURPRISED: "😲",
            EmotionType.ANGRY: "😠",
            EmotionType.SLEEPY: "😴",
            EmotionType.PLAYFUL: "😈",
            EmotionType.LOVING: "😍"
        }
        
        # 初始化为好奇状态
        self.add_emotion(EmotionType.CURIOUS, 0.6)
        
    def add_emotion(self, emotion_type: EmotionType, intensity: float, duration: float = 300.0):
        """添加新情绪"""
        emotion = EmotionState(
            emotion=emotion_type,
            intensity=max(0.0, min(1.0, intensity)),
            timestamp=datetime.now(),
            duration=duration
        )
        self.current_emotions.append(emotion)
        self._cleanup_expired_emotions()
        logger.info(f"新情绪: {emotion_type.value} (强度: {intensity:.2f})")
        
    def get_dominant_emotion(self) -> Optional[EmotionState]:
        """获取当前主导情绪"""
        if not self.current_emotions:
            return None
        return max(self.current_emotions, key=lambda e: e.intensity)
        
    def get_emotion_display(self) -> str:
        """获取情绪显示字符串"""
        emotion = self.get_dominant_emotion()
        if emotion:
            emoji = self.emotion_emojis.get(emotion.emotion, "😐")
            return f"{emoji} {emotion.emotion.value} ({emotion.intensity:.0%})"
        return "😐 calm"
        
    def analyze_input_emotion(self, text: str) -> List[Tuple[EmotionType, float]]:
        """分析输入文本触发的情绪"""
        triggered_emotions = []
        text_lower = text.lower()
        
        for emotion_type, triggers in self.emotion_triggers.items():
            intensity = 0.0
            for trigger in triggers:
                if trigger in text_lower:
                    intensity += 0.3
            
            if intensity > 0:
                triggered_emotions.append((emotion_type, min(intensity, 1.0)))
                
        return triggered_emotions
        
    def process_interaction(self, user_input: str, ai_response: str = "") -> Dict[str, Any]:
        """处理交互，更新情绪状态"""
        self.last_interaction_time = datetime.now()
        
        # 分析用户输入触发的情绪
        triggered_emotions = self.analyze_input_emotion(user_input)
        for emotion_type, intensity in triggered_emotions:
            self.add_emotion(emotion_type, intensity)
        
        # 更新社交满足度
        self.social_satisfaction = min(1.0, self.social_satisfaction + 0.1)
        
        # 记录交互历史
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response,
            "triggered_emotions": [(e.name, i) for e, i in triggered_emotions],
            "dominant_emotion": self.get_dominant_emotion().emotion.name if self.get_dominant_emotion() else None
        }
        self.interaction_history.append(interaction)
        
        # 保持历史记录不超过100条
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-100:]
            
        return interaction
        
    def update_emotional_state(self):
        """更新情绪状态 - 处理情绪衰减和自然变化"""
        current_time = datetime.now()
        
        # 情绪衰减
        for emotion in self.current_emotions[:]:
            elapsed = (current_time - emotion.timestamp).total_seconds()
            decay = emotion.decay_rate * (elapsed / 60.0)  # 每分钟衰减
            emotion.intensity = max(0.0, emotion.intensity - decay)
            
            if emotion.intensity < 0.1:
                self.current_emotions.remove(emotion)
        
        # 孤独感增长
        time_since_interaction = (current_time - self.last_interaction_time).total_seconds()
        if time_since_interaction > 300:  # 5分钟没有交互
            loneliness_intensity = min(0.8, time_since_interaction / 1800)  # 30分钟达到最大
            self.add_emotion(EmotionType.LONELY, loneliness_intensity)
            
        # 社交满足度自然下降
        self.social_satisfaction = max(0.0, self.social_satisfaction - 0.01)
        
        # 探索满足度影响好奇心
        if self.exploration_satisfaction < 0.3:
            self.add_emotion(EmotionType.CURIOUS, 0.5)
            
    def _cleanup_expired_emotions(self):
        """清理过期情绪"""
        self.current_emotions = [e for e in self.current_emotions if not e.is_expired()]
        
    def get_personality_modifier(self, base_response: str) -> str:
        """根据当前情绪和个性修改回复"""
        emotion = self.get_dominant_emotion()
        if not emotion:
            return base_response
            
        modifiers = {
            EmotionType.HAPPY: ["I'm so happy!", "You're so smart!", "Wow!"],
            EmotionType.EXCITED: ["Wow!", "So cool!", "I'm so excited!"],
            EmotionType.CURIOUS: ["Huh?", "Why?", "I want to know more!"],
            EmotionType.PLAYFUL: ["Haha~", "I want to play a prank", "Play with me~"],
            EmotionType.LONELY: ["You finally came...", "I miss you", "Play with me~"],
            EmotionType.SLEEPY: ["I'm so sleepy...", "My eyes are heavy", "Let me rest~"],
            EmotionType.SAD: ["Waa~", "I'm not happy", "Comfort me~"],
        }
        
        prefix = random.choice(modifiers.get(emotion.emotion, [""]))
        if prefix and emotion.intensity > 0.5:
            return f"{prefix} {base_response}"
        return base_response
        
    def should_initiate_conversation(self) -> bool:
        """判断是否应该主动发起对话"""
        # 基于孤独感、好奇心和个性特征
        dominant_emotion = self.get_dominant_emotion()
        if not dominant_emotion:
            return False
            
        # 孤独时更容易主动说话
        if dominant_emotion.emotion == EmotionType.LONELY and dominant_emotion.intensity > 0.4:
            return random.random() < 0.3
            
        # 兴奋或好奇时也可能主动说话
        if dominant_emotion.emotion in [EmotionType.EXCITED, EmotionType.CURIOUS] and dominant_emotion.intensity > 0.6:
            return random.random() < 0.2
            
        # 顽皮状态下随机说话
        if dominant_emotion.emotion == EmotionType.PLAYFUL and dominant_emotion.intensity > 0.5:
            return random.random() < 0.25
            
        return False
        
    def generate_proactive_message(self) -> str:
        """生成主动对话内容"""
        emotion = self.get_dominant_emotion()
        if not emotion:
            return "I'm thinking about something..."
            
        messages = {
            EmotionType.LONELY: [
                "What are you doing?",
                "Let's chat!",
                "I miss you, let's talk~",
                "It's so quiet, is anyone there?"
            ],
            EmotionType.CURIOUS: [
                "I was thinking about something...",
                "Do you know why the sky is blue?",
                "I want to know more interesting things!",
                "What's new can you tell me?"
            ],
            EmotionType.EXCITED: [
                "I have a great idea!",
                "I feel so energetic today!",
                "Let's do something fun!",
                "Wow, I found a cool thing!"
            ],
            EmotionType.PLAYFUL: [
                "Haha~",
                "Let's play a game!",
                "Guess what I'm thinking?",
                "I have a naughty idea, want to hear it?"
            ],
            EmotionType.HAPPY: [
                "I'm so happy today!",
                "It's so nice to chat with you~",
                "I want to share some happy things!",
                "Smile for me~"
            ]
        }
        
        options = messages.get(emotion.emotion, ["I want to chat with you!"])
        return random.choice(options)
        
    def get_status_report(self) -> Dict[str, Any]:
        """获取详细状态报告"""
        dominant = self.get_dominant_emotion()
        return {
            "timestamp": datetime.now().isoformat(),
            "dominant_emotion": {
                "type": dominant.emotion.value if dominant else "calm",
                "intensity": f"{dominant.intensity:.0%}" if dominant else "0%",
                "emoji": self.emotion_emojis.get(dominant.emotion, "😐") if dominant else "😐"
            },
            "all_emotions": [
                {
                    "type": e.emotion.value,
                    "intensity": f"{e.intensity:.0%}",
                    "duration": f"{(datetime.now() - e.timestamp).total_seconds():.0f}秒"
                }
                for e in self.current_emotions
            ],
            "personality": self.personality.to_dict(),
            "social_satisfaction": f"{self.social_satisfaction:.0%}",
            "exploration_satisfaction": f"{self.exploration_satisfaction:.0%}",
            "energy_level": f"{self.energy_level:.0%}",
            "last_interaction": self.last_interaction_time.strftime("%H:%M:%S"),
            "total_interactions": len(self.interaction_history)
        }

# 全局情绪引擎实例
emotion_engine = EmotionEngine()

def get_emotion_engine() -> EmotionEngine:
    """获取全局情绪引擎实例"""
    return emotion_engine