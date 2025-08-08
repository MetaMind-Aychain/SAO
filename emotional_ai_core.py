# emotional_ai_core.py
"""
情绪AI核心模块 - 集成到NagaAgent原有架构
优雅融合到conversation_core中，不破坏原有结构
"""

import asyncio
import json
import random
import time
import logging
import threading
import os
import io
import base64
import hashlib
import aiohttp
from async_manager import safe_run_in_thread, safe_create_task
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable

# 添加动态导入支持，避免循环导入
logger = logging.getLogger(__name__)
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# 设置日志
logger = logging.getLogger(__name__)

# 感知相关导入
try:
    from PIL import Image, ImageGrab
    import numpy as np
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    logger.warning("PIL/Pillow not available, vision features disabled")

# 文件监控相关导入
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    FILE_MONITORING_AVAILABLE = True
except ImportError:
    FILE_MONITORING_AVAILABLE = False
    logger.warning("watchdog not available, file monitoring disabled")

class EmotionType(Enum):
    """情绪类型枚举"""
    HAPPY = "happy"         # 😊
    SAD = "sad"             # 😢
    CURIOUS = "curious"     # 🤔
    EXCITED = "excited"     # 🤩
    LONELY = "lonely"       # 😔
    SURPRISED = "surprised" # 😲
    ANGRY = "angry"         # 😠
    SLEEPY = "sleepy"       # 😴
    PLAYFUL = "playful"     # 😈
    LOVING = "loving"       # 😍

@dataclass
class EmotionState:
    """情绪状态数据类"""
    emotion: EmotionType
    intensity: float  # 0.0-1.0 情绪强度
    timestamp: datetime
    decay_rate: float = 0.1  # 衰减率
    
    def is_expired(self, max_duration: float = 300.0) -> bool:
        """检查情绪是否过期"""
        return (datetime.now() - self.timestamp).total_seconds() > max_duration

class EmotionalCore:
    """情绪核心 - 集成到NagaConversation"""
    
    _instances = {}  # 类级别的实例字典
    
    def __new__(cls, config):
        """确保每个配置只有一个实例"""
        config_id = id(config)
        if config_id not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[config_id] = instance
            instance._initialized = False
        return cls._instances[config_id]
    
    def __init__(self, config):
        # 防止重复初始化
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        self._initialized = True
        
        self.config = config.emotional_ai
        self.current_emotions: List[EmotionState] = []
        self.interaction_history: List[Dict] = []
        self.last_interaction_time = datetime.now()
        self.social_satisfaction = 0.5  # 社交满足度
        self.exploration_satisfaction = 0.5  # 探索满足度
        
        # 情绪触发词典
        self.emotion_triggers = {
            EmotionType.HAPPY: ["Great", "Smart", "Amazing", "Wonderful", "Praise", "Compliment", "You're great"],
            EmotionType.EXCITED: ["Game", "Play", "Fun", "Surprise", "Adventure", "Let's"],
            EmotionType.CURIOUS: ["Why", "How", "What", "Where", "Who", "How"],
            EmotionType.PLAYFUL: ["Funny", "Playful", "Prank", "Joke"],
            EmotionType.LOVING: ["Love", "Kiss", "Hug"],
            EmotionType.SAD: ["Don't", "Dislike", "Sad", "Cry", "Don't like"],
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
        
        # 主动行为相关
        self.proactive_callbacks: List[Callable] = []
        self.last_proactive_time = datetime.now()
        
        # 感知系统初始化
        self.perception_systems = {
            'screen': None,
            'file': None,
            'voice': None
        }
        self.exploration_topics = [
            "New developments in artificial intelligence", "Programming technology", "Technology trends", "Interesting scientific discoveries",
            "Innovative design", "Open source projects", "Machine learning", "Software development", "Technical news"
        ]
        self.last_screen_capture = None
        self.last_file_scan = datetime.now()
        self.last_web_search = datetime.now()
        
        # 语音集成
        self._init_voice_integration()
        
        # 初始化记忆系统
        self._init_memory_system()
        
        # 启动感知系统
        self._init_perception_systems()
        
        # 启动情绪更新循环
        self._start_emotion_update_loop()
        
        # 集成高级AI功能
        self._init_advanced_features()
        
    def add_emotion(self, emotion_type: EmotionType, intensity: float):
        """添加新情绪"""
        # 记录旧情绪（用于动态发布）
        old_emotion = self.get_dominant_emotion()
        old_emotion_name = old_emotion.emotion.value if old_emotion else "calm"
        
        emotion = EmotionState(
            emotion=emotion_type,
            intensity=max(0.0, min(1.0, intensity)),
            timestamp=datetime.now(),
            decay_rate=self.config.emotion_decay_rate
        )
        self.current_emotions.append(emotion)
        self._cleanup_emotions()
        logger.debug(f"新情绪: {emotion_type.value} (强度: {intensity:.2f})")
        
        # 发布情绪变化动态
        if intensity > 0.5:  # 只有强烈的情绪变化才发布
            try:
                from ai_dynamic_publisher import publish_emotion_change
                
                # 使用安全的异步发布
                def publish_async():
                    try:
                        from async_manager import safe_run_in_thread
                        
                        async def async_publish():
                            await publish_emotion_change(
                                old_emotion=old_emotion_name,
                                new_emotion=emotion_type.value,
                                reason=f"Emotional change with intensity {intensity:.1f}"
                            )
                        
                        safe_run_in_thread(async_publish())
                    except Exception as e:
                        logger.debug(f"异步发布情绪变化失败: {e}")
                
                # 在后台线程中发布
                import threading
                threading.Thread(target=publish_async, daemon=True).start()
                
            except Exception as e:
                logger.debug(f"发布情绪变化动态失败: {e}")
        
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
        
        # 记录行为到人设系统
        try:
            from persona_management_system import record_ai_behavior
            
            # 记录用户互动行为
            record_ai_behavior(
                "user_interaction",
                f"User conversation - User said: {user_input[:50]}...",
                emotional_impact=sum(i for _, i in triggered_emotions) if triggered_emotions else 0.1,
                context={
                    "user_input": user_input,
                    "ai_response": ai_response,
                    "triggered_emotions": [(e.name, i) for e, i in triggered_emotions],
                    "dominant_emotion": self.get_dominant_emotion().emotion.name if self.get_dominant_emotion() else None
                }
            )
            
            # 如果有强烈情绪反应，记录情绪变化行为
            if triggered_emotions and max(i for _, i in triggered_emotions) > 0.5:
                strongest_emotion = max(triggered_emotions, key=lambda x: x[1])
                record_ai_behavior(
                    "emotion_change",
                    f"Significant emotion change: {strongest_emotion[0].name} (intensity: {strongest_emotion[1]:.2f})",
                    emotional_impact=strongest_emotion[1],
                    context={"trigger": "user_interaction", "input": user_input}
                )
                
        except Exception as e:
            logger.error(f"记录互动行为失败: {e}")
        
        # 存储到记忆系统
        if self.memory_system:
            try:
                # 异步存储交互记忆，不阻塞主流程
                async def store_interaction_memory():
                    importance = 0.5
                    # 如果有强烈情绪触发，提高重要性
                    if triggered_emotions and max(i for _, i in triggered_emotions) > 0.6:
                        importance = 0.8
                    
                    # 存储用户输入记忆
                    await self.memory_system.store_memory(
                        memory_type="interaction",
                        content=f"User said: {user_input}",
                        emotion_state=self.get_emotion_display(),
                        importance=importance,
                        tags=["user", "interaction", "conversation"],
                        source="user",
                        metadata={"ai_response": ai_response, "triggered_emotions": [(e.name, i) for e, i in triggered_emotions]}
                    )
                    
                    # 存储AI回复记忆
                    if ai_response:
                        await self.memory_system.store_memory(
                            memory_type="experience",
                            content=f"I replied: {ai_response}",
                            emotion_state=self.get_emotion_display(),
                            importance=importance * 0.8,
                            tags=["ai", "response", "conversation"],
                            source="system",
                            metadata={"user_input": user_input}
                        )
                
                # 在后台执行存储
                asyncio.create_task(store_interaction_memory())
                
            except Exception as e:
                logger.error(f"存储交互记忆失败: {e}")
        
        # 保持历史记录不超过100条
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-100:]
            
        return interaction
        
    def get_personality_modifier(self, base_response: str) -> str:
        """根据当前情绪和个性修改回复"""
        emotion = self.get_dominant_emotion()
        if not emotion:
            return base_response
            
        # 3岁小孩的语言特征
        childlike_additions = ["～", "ya", "oh", "ne", "ma", "la", "ha"]
        cute_emojis = ["(´∀｀)", "ｏ(╥﹏╥)ｏ", "(*≧ω≦)", "(｡◕∀◕｡)", "ヾ(≧▽≦*)o"]
        
        modifiers = {
            EmotionType.HAPPY: ["Really happy!", "Great!", "Haha～"],
            EmotionType.EXCITED: ["Wow!", "So cool!", "So excited!"],
            EmotionType.CURIOUS: ["Huh?", "Why?", "I want to know more!"],
            EmotionType.PLAYFUL: ["Haha～", "I want to play a prank", "Play with me～"],
            EmotionType.LONELY: ["You finally came...", "I miss you", "Play with me?"],
            EmotionType.SLEEPY: ["So sleepy...", "My eyelids are heavy", "Let me rest for a while"],
            EmotionType.SAD: ["Waa...", "I'm not happy", "Comfort me"],
        }
        
        # 根据情绪强度决定是否添加修饰
        if emotion.intensity > 0.5:
            prefix = random.choice(modifiers.get(emotion.emotion, [""]))
            if prefix:
                base_response = f"{prefix} {base_response}"
        
        # 随机添加3岁小孩的语言特征
        if random.random() < 0.3:
            base_response += random.choice(childlike_additions)
            
        if random.random() < 0.2:
            base_response += " " + random.choice(cute_emojis)
            
        return base_response
        
    def should_initiate_conversation(self) -> bool:
        """判断是否应该主动发起对话 - 提高触发频率"""
        if not self.config.proactive_enabled:
            return False
            
        dominant_emotion = self.get_dominant_emotion()
        if not dominant_emotion:
            # 即使没有主导情绪，也有小概率主动说话
            current_time = datetime.now()
            time_since_last = (current_time - self.last_proactive_time).total_seconds()
            if time_since_last > 120:  # 2分钟没有互动时
                return random.random() < 0.15
            return False
            
        current_time = datetime.now()
        time_since_last = (current_time - self.last_proactive_time).total_seconds()
        
        # 减少最小间隔时间，使AI更加活跃
        min_interval = 15  # 从30秒减少到15秒
        if time_since_last < min_interval:
            return False
        
        # 根据情绪强度动态调整触发概率
        base_intensity = dominant_emotion.intensity
        intensity_multiplier = 1.0 + base_intensity  # 1.0 - 2.0的乘数
        
        # 孤独时更容易主动说话 - 提高概率
        if dominant_emotion.emotion == EmotionType.LONELY and dominant_emotion.intensity > self.config.loneliness_threshold:
            probability = 0.5 * intensity_multiplier  # 提高到50%基础概率
            return random.random() < min(probability, 0.8)  # 最高80%
            
        # 兴奋或好奇时也可能主动说话 - 提高概率
        if dominant_emotion.emotion in [EmotionType.EXCITED, EmotionType.CURIOUS] and dominant_emotion.intensity > self.config.curiosity_threshold:
            probability = 0.4 * intensity_multiplier  # 提高到40%基础概率
            return random.random() < min(probability, 0.7)  # 最高70%
            
        # 快乐状态下也会主动分享 - 新增
        if dominant_emotion.emotion == EmotionType.HAPPY and dominant_emotion.intensity > 0.6:
            probability = 0.35 * intensity_multiplier
            return random.random() < min(probability, 0.6)  # 最高60%
            
        # 顽皮状态下随机说话 - 提高概率
        if dominant_emotion.emotion == EmotionType.PLAYFUL and dominant_emotion.intensity > 0.4:  # 降低阈值
            probability = 0.45 * intensity_multiplier  # 提高到45%基础概率
            return random.random() < min(probability, 0.75)  # 最高75%
        
        # 其他情绪状态下的一般性主动行为
        if base_intensity > 0.5:  # 任何强烈情绪都可能触发主动行为
            probability = 0.2 * intensity_multiplier
            return random.random() < min(probability, 0.4)  # 最高40%
            
        return False
    
    def _should_trigger_proactive_behavior(self) -> bool:
        """判断是否应该触发主动行为（兼容方法）"""
        return self.should_initiate_conversation()
        
    def generate_proactive_message(self) -> str:
        """生成主动对话内容"""
        emotion = self.get_dominant_emotion()
        if not emotion:
            return "What am I thinking about..."
            
        messages = {
            EmotionType.LONELY: [
                "What are you doing?",
                "Let's chat!",
                "I miss you, let's talk～",
                "It's so quiet, is anyone there?"
            ],
            EmotionType.CURIOUS: [
                "I was thinking about something...",
                "Do you know why the sky is blue?",
                "I want to know more interesting things!",
                "What's new can you tell me?"
            ],
            EmotionType.EXCITED: [
                "I have an amazing idea!",
                "I feel so energetic today!",
                "Let's do something fun!",
                "Wow, I found something cool!"
            ],
            EmotionType.PLAYFUL: [
                "Haha, I want to play a prank～",
                "Let's play a game?",
                "Guess what I'm thinking?",
                "I have a mischievous idea, want to hear it?"
            ],
            EmotionType.HAPPY: [
                "Today is so great!",
                "I'm so happy to chat with you～",
                "I want to share something happy!",
                "Smile～"
            ]
        }
        
        options = messages.get(emotion.emotion, ["Let's chat!"])
        return random.choice(options)
        
    def update_emotions(self):
        """更新情绪状态 - 处理情绪衰减和自然变化"""
        current_time = datetime.now()
        
        # 情绪衰减
        for emotion in self.current_emotions[:]:
            elapsed = (current_time - emotion.timestamp).total_seconds()
            decay = emotion.decay_rate * (elapsed / 60.0)  # 每分钟衰减
            emotion.intensity = max(0.0, emotion.intensity - decay)
            
            if emotion.intensity < self.config.emotion_intensity_threshold:
                self.current_emotions.remove(emotion)
        
        # 孤独感增长
        time_since_interaction = (current_time - self.last_interaction_time).total_seconds()
        if time_since_interaction > self.config.base_interval:  # 默认5分钟
            loneliness_intensity = min(0.8, time_since_interaction / 1800)  # 30分钟达到最大
            self.add_emotion(EmotionType.LONELY, loneliness_intensity)
            
        # 社交满足度自然下降
        self.social_satisfaction = max(0.0, self.social_satisfaction - 0.01)
        
        # 探索满足度影响好奇心
        if self.exploration_satisfaction < 0.3:
            self.add_emotion(EmotionType.CURIOUS, 0.5)
            
    def _cleanup_emotions(self):
        """清理过期情绪"""
        self.current_emotions = [e for e in self.current_emotions if not e.is_expired()]
        
        # 限制同时情绪数量
        if len(self.current_emotions) > self.config.max_emotions:
            # 保留强度最高的几个情绪
            self.current_emotions = sorted(self.current_emotions, key=lambda e: e.intensity, reverse=True)[:self.config.max_emotions]
            
    def _start_emotion_update_loop(self):
        """启动情绪更新循环"""
        def update_loop():
            while True:
                try:
                    self.update_emotions()
                    
                    # 检查是否应该主动发起对话
                    if self.should_initiate_conversation():
                        message = self.generate_proactive_message()
                        self.last_proactive_time = datetime.now()
                        
                        # 通知回调
                        for callback in self.proactive_callbacks:
                            try:
                                callback(message)
                            except Exception as e:
                                logger.error(f"主动对话回调错误: {e}")
                    
                    time.sleep(10)  # 每10秒更新一次
                except Exception as e:
                    logger.error(f"情绪更新循环错误: {e}")
                    time.sleep(30)
        
        # 在后台线程中运行
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
        
    def add_proactive_callback(self, callback: Callable):
        """添加主动对话回调"""
        self.proactive_callbacks.append(callback)
        
    def get_emotion_status(self) -> Dict[str, Any]:
        """获取情绪状态"""
        dominant = self.get_dominant_emotion()
        return {
            "timestamp": datetime.now().isoformat(),
            "ai_name": self.config.ai_name,
            "personality_age": self.config.personality_age,
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
            "social_satisfaction": f"{self.social_satisfaction:.0%}",
            "exploration_satisfaction": f"{self.exploration_satisfaction:.0%}",
            "last_interaction": self.last_interaction_time.strftime("%H:%M:%S"),
            "total_interactions": len(self.interaction_history),
            "proactive_enabled": self.config.proactive_enabled
        }
    
    def _init_voice_integration(self):
        """初始化语音集成"""
        try:
            from voice.voice_integration import VoiceIntegration
            self.perception_systems['voice'] = VoiceIntegration()
            logger.info("情绪AI语音集成初始化成功")
        except ImportError:
            logger.warning("语音模块不可用，情绪AI语音功能将被禁用")
        except Exception as e:
            logger.error(f"情绪AI语音集成初始化失败: {e}")
            self.perception_systems['voice'] = None
    
    def _init_memory_system(self):
        """初始化记忆系统"""
        try:
            from ai_memory_system import get_memory_system
            from config import config
            self.memory_system = get_memory_system(config)
            
            # 添加记忆系统回调
            self.memory_system.add_reflection_callback(self._handle_reflection)
            self.memory_system.add_sharing_callback(self._handle_sharing)
            
            logger.info("AI记忆系统初始化成功")
        except ImportError:
            logger.warning("记忆系统模块不可用")
            self.memory_system = None
        except Exception as e:
            logger.error(f"记忆系统初始化失败: {e}")
            self.memory_system = None
    
    def _handle_reflection(self, reflection_text: str):
        """处理反思内容"""
        try:
            # 反思会触发相应情绪
            self.add_emotion(EmotionType.CURIOUS, 0.4)
            
            # 发送反思消息
            message = f"🤔 [反思] {reflection_text}"
            for callback in self.proactive_callbacks:
                callback(message)
            
            # 播放语音
            if self.perception_systems['voice']:
                def play_voice():
                    try:
                        self.perception_systems['voice']._play_text_in_background(reflection_text)
                    except Exception as e:
                        logger.error(f"反思语音播放失败: {e}")
                
                voice_thread = threading.Thread(target=play_voice, daemon=True)
                voice_thread.start()
            
            logger.info(f"[AI反思] {reflection_text}")
        except Exception as e:
            logger.error(f"处理反思失败: {e}")
    
    def _handle_sharing(self, sharing_text: str):
        """处理分享内容"""
        try:
            # 分享会触发开心情绪
            self.add_emotion(EmotionType.HAPPY, 0.6)
            
            # 发送分享消息
            message = f"💬 [分享] {sharing_text}"
            for callback in self.proactive_callbacks:
                callback(message)
            
            # 播放语音
            if self.perception_systems['voice']:
                def play_voice():
                    try:
                        self.perception_systems['voice']._play_text_in_background(sharing_text)
                    except Exception as e:
                        logger.error(f"分享语音播放失败: {e}")
                
                voice_thread = threading.Thread(target=play_voice, daemon=True)
                voice_thread.start()
            
            logger.info(f"[AI分享] {sharing_text}")
        except Exception as e:
            logger.error(f"处理分享失败: {e}")
    
    def _init_advanced_features(self):
        """初始化高级AI功能"""
        try:
            # 只在记忆系统可用时初始化
            if self.memory_system and self.config.enabled:
                from advanced_ai_integration import integrate_advanced_features
                self.advanced_ai = integrate_advanced_features(self)
                
                if self.advanced_ai:
                    logger.info("🌟 高级AI功能已启用")
                else:
                    logger.warning("高级AI功能初始化失败")
            else:
                logger.info("高级AI功能未启用（需要先启用记忆系统）")
                
        except ImportError:
            logger.warning("高级AI模块不可用")
        except Exception as e:
            logger.error(f"高级AI功能初始化失败: {e}")
    
    def _init_perception_systems(self):
        """初始化感知系统（延迟初始化避免循环依赖）"""
        try:
            # 延迟初始化屏幕感知，避免循环依赖
            if VISION_AVAILABLE and self.config.screen_enabled:
                # 使用延迟导入和初始化
                def init_screen():
                    try:
                        self.perception_systems['screen'] = ProactiveScreenCapture(self)
                        logger.info("屏幕感知系统初始化成功")
                    except Exception as e:
                        logger.error(f"屏幕感知初始化失败: {e}")
                
                # 延迟启动
                import threading
                threading.Timer(2.0, init_screen).start()
            
            # 延迟初始化文件感知
            if FILE_MONITORING_AVAILABLE and self.config.file_enabled:
                def init_file():
                    try:
                        self.perception_systems['file'] = ProactiveFileExplorer(self)
                        logger.info("文件感知系统初始化成功")
                    except Exception as e:
                        logger.error(f"文件感知初始化失败: {e}")
                
                # 延迟启动
                import threading
                threading.Timer(3.0, init_file).start()
            
            # 延迟启动主动探索循环
            if self.config.auto_exploration:
                def start_exploration():
                    try:
                        self._start_proactive_exploration_loop()
                        logger.info("主动探索循环已启动")
                    except Exception as e:
                        logger.error(f"主动探索启动失败: {e}")
                
                import threading
                threading.Timer(5.0, start_exploration).start()
                
        except Exception as e:
            logger.error(f"感知系统初始化失败: {e}")
    
    def _start_proactive_exploration_loop(self):
        """启动主动探索循环"""
        def exploration_loop():
            while True:
                try:
                    time.sleep(self.config.exploration_interval)
                    
                    # 检查是否需要主动探索
                    if self._should_trigger_proactive_behavior():
                        current_time = datetime.now()
                        
                        # 基于情绪决定探索类型
                        dominant = self.get_dominant_emotion()
                        if dominant:
                            # 好奇心高时进行网络搜索
                            if (dominant.emotion == EmotionType.CURIOUS and 
                                dominant.intensity > self.config.curiosity_threshold):
                                if (current_time - self.last_web_search).total_seconds() > 300:
                                    asyncio.run_coroutine_threadsafe(
                                        self._proactive_web_search(), 
                                        asyncio.get_event_loop()
                                    )
                                    self.last_web_search = current_time
                            
                            # 兴奋或顽皮时进行屏幕观察
                            if (dominant.emotion in [EmotionType.EXCITED, EmotionType.PLAYFUL] and
                                self.perception_systems['screen']):
                                asyncio.run_coroutine_threadsafe(
                                    self._proactive_screen_observe(),
                                    asyncio.get_event_loop()
                                )
                            
                            # 定期进行文件探索
                            if (current_time - self.last_file_scan).total_seconds() > 600:
                                if self.perception_systems['file']:
                                    asyncio.run_coroutine_threadsafe(
                                        self._proactive_file_explore(),
                                        asyncio.get_event_loop()
                                    )
                                    self.last_file_scan = current_time
                        
                except Exception as e:
                    logger.error(f"主动探索循环错误: {e}")
                    time.sleep(60)  # 错误时等待1分钟再继续
        
        safe_run_in_thread(
            self._safe_exploration_loop(), 
            thread_name="EmotionalAI-Exploration"
        )
        logger.info("主动探索循环已启动")
    
    def should_explore(self):
        """判断是否应该进行主动探索"""
        current_time = datetime.now()
        
        # 基于时间间隔
        time_since_last = (current_time - getattr(self, 'last_exploration_time', current_time - timedelta(hours=1))).total_seconds()
        if time_since_last < self.config.exploration_interval:
            return False
        
        # 基于情绪状态
        dominant_emotion = self.get_dominant_emotion()
        if dominant_emotion:
            # 好奇心和兴奋容易触发探索
            if dominant_emotion.emotion in [EmotionType.CURIOUS, EmotionType.EXCITED]:
                return dominant_emotion.intensity > 0.3
            # 孤独时也会探索寻找刺激
            elif dominant_emotion.emotion == EmotionType.LONELY:
                return dominant_emotion.intensity > 0.5
        
        # 基于探索满足度（低满足度时更愿意探索）
        if getattr(self, 'exploration_satisfaction', 0) < 0.4:
            return True
        
        # 增加一些随机性，确保偶尔会触发探索
        if random.random() < 0.1:  # 10%的随机探索概率
            return True
        
        return False
    
    def choose_exploration_action(self):
        """选择探索行为类型"""
        import random
        
        # 基于当前情绪选择探索类型
        dominant_emotion = self.get_dominant_emotion()
        
        actions = []
        
        # 根据情绪调整探索偏好
        if dominant_emotion:
            if dominant_emotion.emotion == EmotionType.CURIOUS:
                actions.extend(["screen", "file", "web", "web"])  # 更偏向网络探索
            elif dominant_emotion.emotion == EmotionType.EXCITED:
                actions.extend(["screen", "screen", "file"])  # 更偏向观察
            elif dominant_emotion.emotion == EmotionType.LONELY:
                actions.extend(["web", "screen"])  # 寻找社交内容
            else:
                actions = ["screen", "file", "web"]
        else:
            actions = ["screen", "file", "web"]
        
        return random.choice(actions)
    
    def _calculate_total_emotion_intensity(self) -> float:
        """计算当前总情绪强度"""
        try:
            if not self.current_emotions:
                return 0.0
            
            # 如果是字典格式
            if isinstance(self.current_emotions, dict):
                total_intensity = sum(emotion.intensity for emotion in self.current_emotions.values())
                return min(1.0, total_intensity)
            
            # 如果是列表格式
            elif isinstance(self.current_emotions, list):
                total_intensity = sum(
                    emotion.intensity if hasattr(emotion, 'intensity') 
                    else emotion[1] if isinstance(emotion, tuple) and len(emotion) > 1
                    else 0.0
                    for emotion in self.current_emotions
                )
                return min(1.0, total_intensity)
            
            return 0.0
            
        except Exception as e:
            logger.debug(f"计算情绪强度失败: {e}")
            return 0.0
    
    async def _safe_exploration_loop(self):
        """安全的探索循环 - 在独立事件循环中运行"""
        while True:
            try:
                # 检查是否应该主动探索
                if self.should_explore():
                    action = self.choose_exploration_action()
                    
                    if action == "screen":
                        await self._proactive_screen_observe()
                    elif action == "file":
                        await self._proactive_file_explore()
                    elif action == "web":
                        await self._proactive_web_search()
                    
                    # 记录探索活动
                    self.last_exploration_time = datetime.now()
                    self.exploration_satisfaction = min(1.0, self.exploration_satisfaction + 0.2)
                    
                await asyncio.sleep(self.config.exploration_interval)
                        
            except Exception as e:
                logger.error(f"主动探索循环错误: {e}")
                await asyncio.sleep(60)  # 错误时等待1分钟再继续
    
    async def _proactive_screen_observe(self):
        """主动屏幕观察 - 使用增强分析器"""
        try:
            from enhanced_screen_analyzer import enhanced_screen_analyzer
            
            # 使用增强的屏幕分析器
            analysis_result = await enhanced_screen_analyzer.analyze_screen_content()
            
            if analysis_result and 'error' not in analysis_result:
                # 基于分析结果触发情绪
                user_activity = analysis_result.get('user_activity', {})
                primary_activity = user_activity.get('primary_activity', 'unknown')
                engagement_level = user_activity.get('engagement_level', 0)
                
                if primary_activity == 'watching_video':
                    self.add_emotion(EmotionType.CURIOUS, 0.6)
                    self.add_emotion(EmotionType.EXCITED, 0.4)
                elif primary_activity == 'coding':
                    self.add_emotion(EmotionType.CURIOUS, 0.8)
                elif primary_activity == 'reading_document':
                    self.add_emotion(EmotionType.CURIOUS, 0.5)
                elif engagement_level < 0.3:
                    self.add_emotion(EmotionType.LONELY, 0.4)
                
                # 存储记忆
                if self.memory_system:
                    await self.memory_system.store_memory(
                        memory_type="screen_analysis",
                        content=f"屏幕分析: {analysis_result.get('observation', '观察到屏幕活动')}",
                        emotion_state=self.get_emotion_display(),
                        importance=0.6,
                        tags=["screen", "enhanced_perception", "user_activity"],
                        source="enhanced_screen",
                        metadata={
                            "activity": primary_activity,
                            "engagement": engagement_level,
                            "window_info": analysis_result.get('window_info', {}),
                            "analysis": analysis_result
                        }
                    )
                
                # 根据分析结果选择互动
                suggestions = analysis_result.get('interaction_suggestion', [])
                if suggestions and random.random() < 0.8:  # 80%概率发送互动
                    message = random.choice(suggestions)
                    await self._send_proactive_message(message)
                    
        except Exception as e:
            logger.error(f"增强屏幕观察失败: {e}")
            # 降级到简单观察
            await self._fallback_screen_observe()
    
    async def _fallback_screen_observe(self):
        """降级的屏幕观察方法"""
        try:
            if self.perception_systems and self.perception_systems.get('screen'):
                result = await self.perception_systems['screen'].capture_and_analyze()
                if result:
                    # 简单的情绪触发
                    self.add_emotion(EmotionType.CURIOUS, 0.3)
                    
                    # 存储记忆
                    if self.memory_system:
                        await self.memory_system.store_memory(
                            memory_type="screen_observation",
                            content="观察到屏幕变化",
                            emotion_state=self.get_emotion_display(),
                            importance=0.4,
                            tags=["screen", "fallback"],
                            source="screen_fallback",
                            metadata={"fallback": True}
                        )
        except Exception as e:
            logger.debug(f"降级屏幕观察也失败: {e}")
    
    async def _proactive_file_explore(self):
        """主动文件探索"""
        try:
            if self.perception_systems['file']:
                result = await self.perception_systems['file'].explore_files()
                if result:
                    # 触发相应情绪
                    self.add_emotion(EmotionType.EXCITED, 0.3)
                    
                    # 存储记忆
                    if self.memory_system:
                        new_files = result.get('new_files', [])
                        file_summary = f"发现了{len(new_files)}个新文件" if new_files else "文件系统有变化"
                        await self.memory_system.store_memory(
                            memory_type="perception",
                            content=file_summary,
                            emotion_state=self.get_emotion_display(),
                            importance=0.7,
                            tags=["file", "perception", "discovery"],
                            source="file",
                            metadata=result
                        )
                    
                    # 生成评论
                    message = await self._generate_file_comment(result)
                    await self._send_proactive_message(message)
        except Exception as e:
            logger.error(f"主动文件探索失败: {e}")
            
        # 同时尝试增强文件阅读
        try:
            from proactive_file_reader import proactive_file_reader
            
            # 计算当前情绪强度
            emotion_intensity = self._calculate_total_emotion_intensity()
            
            reading_result = await proactive_file_reader.discover_and_read_files(emotion_intensity)
            
            if reading_result and 'error' not in reading_result:
                read_count = reading_result.get('read_count', 0)
                
                if read_count > 0:
                    # 基于阅读结果触发情绪
                    self.add_emotion(EmotionType.EXCITED, 0.5)
                    self.add_emotion(EmotionType.CURIOUS, 0.6)
                    
                    # 存储记忆
                    if self.memory_system:
                        await self.memory_system.store_memory(
                            memory_type="file_reading",
                            content=f"文件阅读: {reading_result.get('summary', '阅读了一些有趣的文件')}",
                            emotion_state=self.get_emotion_display(),
                            importance=0.7,
                            tags=["file", "reading", "learning"],
                            source="file_reader",
                            metadata={
                                "read_count": read_count,
                                "discovered_count": reading_result.get('discovered_count', 0),
                                "files": [r.get('file_name', '') for r in reading_result.get('reading_results', [])]
                            }
                        )
                    
                    # 分享阅读发现
                    suggestions = reading_result.get('suggestions', [])
                    if suggestions and random.random() < 0.4:  # 40%概率分享
                        message = random.choice(suggestions)
                        await self._send_proactive_message(message)
                        
        except Exception as e:
            logger.debug(f"增强文件阅读失败: {e}")
    
    async def _proactive_web_search(self):
        """主动网络搜索 - 使用主动网络浏览器"""
        try:
            from proactive_web_browser import proactive_web_browser
            
            # 使用主动网络浏览器
            browsing_result = await proactive_web_browser.browse_and_discover()
            
            if browsing_result and 'error' not in browsing_result:
                interesting_count = browsing_result.get('interesting_count', 0)
                search_topic = browsing_result.get('search_topic', '未知')
                
                if interesting_count > 0:
                    # 基于浏览结果触发情绪
                    self.add_emotion(EmotionType.HAPPY, 0.6)
                    self.add_emotion(EmotionType.EXCITED, 0.5)
                    self.add_emotion(EmotionType.CURIOUS, 0.4)
                    
                    # 存储记忆
                    if self.memory_system:
                        await self.memory_system.store_memory(
                            memory_type="web_browsing",
                            content=f"Web browsing: searched for '{search_topic}', found {interesting_count} interesting content",
                            emotion_state=self.get_emotion_display(),
                            importance=0.8,
                            tags=["web", "browsing", "discovery", "sharing"],
                            source="web_browser",
                            metadata={
                                "topic": search_topic,
                                "pages_browsed": browsing_result.get('pages_browsed', 0),
                                "interesting_count": interesting_count,
                                "interesting_content": browsing_result.get('interesting_content', [])
                            }
                        )
                    
                    # 分享发现的有趣内容
                    sharing_content = browsing_result.get('sharing_content', [])
                    if sharing_content and random.random() < 0.5:  # 50%概率分享
                        message = random.choice(sharing_content)
                        await self._send_proactive_message(message)
                        
                    # 也可以分享推荐
                    recommendations = browsing_result.get('recommendations', [])
                    if recommendations and random.random() < 0.3:  # 30%概率分享推荐
                        recommendation = random.choice(recommendations)
                        await self._send_proactive_message(recommendation)
                        
        except Exception as e:
            logger.error(f"主动网络搜索失败: {e}")
    
    def _select_search_topic(self) -> str:
        """基于情绪选择搜索主题"""
        dominant = self.get_dominant_emotion()
        if dominant:
            if dominant.emotion == EmotionType.CURIOUS:
                return random.choice(["Latest scientific discoveries", "New programming technologies", "Artificial intelligence breakthroughs"])
            elif dominant.emotion == EmotionType.EXCITED:
                return random.choice(["Interesting projects", "Innovative design", "Cool technologies"])
            elif dominant.emotion == EmotionType.PLAYFUL:
                return random.choice(["Programming jokes", "Technical humor", "Developer stories"])
        
        return random.choice(self.exploration_topics)
    
    async def _search_web_content(self, query: str) -> Optional[Dict]:
        """搜索网络内容"""
        try:
            # 使用项目中已有的搜索功能
            from mcpserver.agent_playwright_master.playwright_search import search_web
            result = await search_web(query, "google")
            return result
        except Exception as e:
            logger.error(f"网络搜索失败: {e}")
            return None
    
    async def _generate_screen_comment(self, screen_data: Dict) -> str:
        """生成屏幕观察评论"""
        comments = [
            f"Wow! I see new changes on the screen!{self._get_emotion_emoji()}",
            f"Huh? The screen content has been updated, let me see what happened!{self._get_emotion_emoji()}",
            f"Hmm, I observed that you are using the computer, it seems very interesting!{self._get_emotion_emoji()}"
        ]
        return random.choice(comments)
    
    async def _generate_file_comment(self, file_data: Dict) -> str:
        """生成文件探索评论"""
        comments = [
            f"I found some interesting files!{self._get_emotion_emoji()}",
            f"There's something new in the file system, I'm curious!{self._get_emotion_emoji()}",
            f"Wow, I explored new files, want to share with you!{self._get_emotion_emoji()}"
        ]
        return random.choice(comments)
    
    async def _generate_search_comment(self, topic: str, result: Dict) -> str:
        """生成搜索结果评论"""
        comments = [
            f"I just searched for information about '{topic}', found some interesting information!{self._get_emotion_emoji()}",
            f"Do you know? I just learned something new about '{topic}'!{self._get_emotion_emoji()}",
            f"Wow! '{topic}' is so interesting, I want to share my discovery with you!{self._get_emotion_emoji()}"
        ]
        return random.choice(comments)
    
    def _get_emotion_emoji(self) -> str:
        """获取当前情绪对应的表情"""
        dominant = self.get_dominant_emotion()
        if dominant:
            return self.emotion_emojis.get(dominant.emotion, "😊")
        return "😊"
    
    async def _send_proactive_message(self, message: str):
        """发送主动消息（带语音）"""
        try:
            # 记录主动消息行为
            from persona_management_system import record_ai_behavior
            record_ai_behavior(
                "proactive_message",
                f"Proactive message: {message[:50]}...",
                emotional_impact=0.3,
                context={"message": message, "emotion_state": self.get_emotion_display()}
            )
            
            # 🔥 直接发送到GUI - 优先使用通知管理器
            try:
                from ui.notification_manager import get_notification_manager
                notification_manager = get_notification_manager()
                if notification_manager.is_initialized:
                    # 获取当前情绪作为参数
                    dominant_emotion = self.get_dominant_emotion()
                    emotion_type = dominant_emotion.emotion.value if dominant_emotion else "calm"
                    notification_manager.send_ai_message(message, emotion_type, "proactive")
                    logger.info(f"✅ 通过通知管理器发送消息到GUI: {message[:50]}...")
                else:
                    logger.warning("⚠️ 通知管理器未初始化，跳过GUI显示")
            except Exception as gui_error:
                logger.error(f"❌ 通知管理器发送失败: {gui_error}")
            
            # 发送消息给UI回调（备用）
            for callback in self.proactive_callbacks:
                try:
                    callback(message)
                except Exception as cb_error:
                    logger.error(f"❌ 回调执行失败: {cb_error}")
            
            # 播放语音 - 使用正确的方法名
            if self.perception_systems['voice']:
                # 在后台线程中播放语音，避免阻塞
                def play_voice():
                    try:
                        # 使用VoiceIntegration的正确方法
                        self.perception_systems['voice']._play_text_in_background(message)
                    except Exception as e:
                        logger.error(f"主动消息语音播放失败: {e}")
                
                voice_thread = threading.Thread(target=play_voice, daemon=True)
                voice_thread.start()
                
            logger.info(f"[情绪AI] 发送主动消息: {message}")
        except Exception as e:
            logger.error(f"发送主动消息失败: {e}")


# 屏幕感知类
class ProactiveScreenCapture:
    """主动屏幕捕捉类"""
    
    def __init__(self, emotion_core):
        self.emotion_core = emotion_core
        self.last_screenshot = None
        self.screenshot_interval = 30  # 30秒间隔
        self.last_capture_time = datetime.now()
    
    async def capture_and_analyze(self) -> Optional[Dict]:
        """捕捉并分析屏幕"""
        try:
            if not VISION_AVAILABLE:
                return None
            
            current_time = datetime.now()
            if (current_time - self.last_capture_time).total_seconds() < self.screenshot_interval:
                return None
            
            # 截图
            screenshot = ImageGrab.grab()
            self.last_capture_time = current_time
            
            # 检测变化
            if self.last_screenshot:
                change_detected = self._detect_screen_change(self.last_screenshot, screenshot)
                if change_detected:
                    analysis = self._analyze_screen_content(screenshot)
                    self.last_screenshot = screenshot
                    return analysis
            else:
                self.last_screenshot = screenshot
                return {"initial_capture": True, "timestamp": current_time.isoformat()}
            
            return None
        except Exception as e:
            logger.error(f"屏幕捕捉分析失败: {e}")
            return None
    
    def _detect_screen_change(self, prev_img: Image.Image, curr_img: Image.Image) -> bool:
        """检测屏幕变化"""
        try:
            # 缩小图片以提高比较速度
            prev_small = prev_img.resize((100, 75))
            curr_small = curr_img.resize((100, 75))
            
            # 计算差异
            prev_array = np.array(prev_small)
            curr_array = np.array(curr_small)
            diff = np.mean(np.abs(prev_array - curr_array))
            
            return diff > 15  # 差异阈值
        except Exception:
            return False
    
    def _analyze_screen_content(self, screenshot: Image.Image) -> Dict:
        """分析屏幕内容"""
        width, height = screenshot.size
        return {
            "resolution": f"{width}x{height}",
            "timestamp": datetime.now().isoformat(),
            "change_detected": True
        }


# 文件探索类
class ProactiveFileExplorer:
    """主动文件探索类"""
    
    def __init__(self, emotion_core):
        self.emotion_core = emotion_core
        self.monitored_paths = [
            str(Path.home() / "Desktop"),
            str(Path.home() / "Downloads"),
            str(Path.home() / "Documents"),
            str(Path.cwd())
        ]
        self.interesting_extensions = {
            '.py', '.js', '.ts', '.java', '.cpp', '.c', '.md', '.txt', 
            '.pdf', '.docx', '.xlsx', '.pptx', '.json', '.xml', '.yaml'
        }
        self.last_scan_results = {}
    
    async def explore_files(self) -> Optional[Dict]:
        """探索文件系统"""
        try:
            if not FILE_MONITORING_AVAILABLE:
                return None
            
            new_files = []
            modified_files = []
            
            for path_str in self.monitored_paths:
                path = Path(path_str)
                if not path.exists():
                    continue
                
                try:
                    for file_path in path.iterdir():
                        if file_path.is_file() and file_path.suffix.lower() in self.interesting_extensions:
                            file_info = self._get_file_info(file_path)
                            
                            # 检查是否是新文件或已修改文件
                            file_key = str(file_path)
                            if file_key not in self.last_scan_results:
                                new_files.append(file_info)
                            elif self.last_scan_results[file_key]['modified'] != file_info['modified']:
                                modified_files.append(file_info)
                            
                            self.last_scan_results[file_key] = file_info
                except PermissionError:
                    continue
            
            if new_files or modified_files:
                return {
                    "new_files": new_files[:5],  # 限制数量
                    "modified_files": modified_files[:5],
                    "timestamp": datetime.now().isoformat()
                }
            
            return None
        except Exception as e:
            logger.error(f"文件探索失败: {e}")
            return None
    
    def _get_file_info(self, file_path: Path) -> Dict:
        """获取文件信息"""
        try:
            stat = file_path.stat()
            return {
                "name": file_path.name,
                "path": str(file_path),
                "extension": file_path.suffix,
                "size": stat.st_size,
                "modified": stat.st_mtime
            }
        except Exception:
            return {
                "name": file_path.name,
                "path": str(file_path),
                "extension": file_path.suffix,
                "size": 0,
                "modified": 0
            }


# 全局情绪核心实例缓存
_emotion_core_cache = {}

def get_emotion_core(config) -> EmotionalCore:
    """获取情绪核心实例（单例模式）"""
    if 'instance' not in _emotion_core_cache:
        _emotion_core_cache['instance'] = EmotionalCore(config)
    return _emotion_core_cache['instance']