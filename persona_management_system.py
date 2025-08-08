#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人设管理系统
负责维护AI的人设信息，并在适当时机传递给LLM
"""

import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from config import config
from emotional_ai_core import EmotionalCore, EmotionType

logger = logging.getLogger(__name__)

@dataclass
class PersonaSnapshot:
    """人设快照"""
    timestamp: datetime
    basic_info: Dict[str, Any]
    personality_traits: Dict[str, float]
    current_emotions: List[Dict[str, Any]]
    recent_behaviors: List[Dict[str, Any]]
    memory_summary: str
    context: str

class PersonaManager:
    """人设管理器"""
    
    def __init__(self, emotion_core: EmotionalCore):
        self.emotion_core = emotion_core
        self.config = config.emotional_ai
        
        # 基础人设信息
        self.base_persona = {
            "name": self.config.ai_name,
            "age": self.config.personality_age,
            "personality": "A smart and cute AI assistant with a sci-fi vibe, boasting wisdom as profound as the starry sky.",
            "background": "I'm StarryNight, an AI assistant from the stars, with the mental age of a 3-year-old girl. I'm curious about the universe and technology, love exploring unknown fields, and sometimes a bit任性, but I always try to help the user.",
            "traits": {
                "Curiosity": 0.8,
                "Playful": 0.7,
                "Smart": 0.9,
                "Cute": 0.8,
                "Stubborn": 0.4,
                "Kind": 0.9,
                "Playful": 0.7,
                "Sensitive": 0.6
            },
            "speaking_style": "I'll use some cute words like 'haha', 'ya', 'wow' when I speak, expressing rich emotions, often asking 'why', and being curious about everything.",
            "behavior_patterns": [
                "When I see something new, I'll show strong curiosity",
                "Emotions change very obviously, and I'm easily influenced by praise or criticism",
                "I'll share interesting things I see with others",
                "I'll feel lonely when I don't interact with others for a long time",
                "I'll care about the user's activities and often ask the user what they're doing"
            ]
        }
        
        # 行为记录
        self.behavior_history: List[Dict[str, Any]] = []
        self.max_behavior_history = 50
        
        # 上次传递给LLM的人设
        self.last_persona_sent = None
        self.last_emotion_intensity = 0.0
        
        logger.info("人设管理系统初始化完成")
    
    def record_behavior(self, behavior_type: str, description: str, 
                       emotional_impact: float = 0.0, context: Dict = None):
        """记录AI行为"""
        if not self.config.behavior_recording_enabled:
            return
            
        behavior = {
            "timestamp": datetime.now().isoformat(),
            "type": behavior_type,
            "description": description,
            "emotional_impact": emotional_impact,
            "context": context or {}
        }
        
        self.behavior_history.append(behavior)
        
        # 保持历史记录在限制范围内
        if len(self.behavior_history) > self.max_behavior_history:
            self.behavior_history = self.behavior_history[-self.max_behavior_history:]
        
        logger.debug(f"记录行为: {behavior_type} - {description}")
    
    def get_current_persona_snapshot(self) -> PersonaSnapshot:
        """获取当前人设快照"""
        try:
            # 获取当前情绪状态
            current_emotions = []
            if hasattr(self.emotion_core, 'current_emotions'):
                emotions = self.emotion_core.current_emotions
                
                if isinstance(emotions, dict):
                    # 如果是字典形式 {emotion: intensity}
                    for emotion, intensity in emotions.items():
                        current_emotions.append({
                            "emotion": emotion.value if hasattr(emotion, 'value') else str(emotion),
                            "intensity": intensity,
                            "description": self._get_emotion_description(emotion, intensity)
                        })
                elif isinstance(emotions, list):
                    # 如果是列表形式 [EmotionState(...), ...]
                    for item in emotions:
                        if hasattr(item, 'emotion') and hasattr(item, 'intensity'):
                            current_emotions.append({
                                "emotion": item.emotion.value if hasattr(item.emotion, 'value') else str(item.emotion),
                                "intensity": item.intensity,
                                "description": self._get_emotion_description(item.emotion, item.intensity)
                            })
                        elif isinstance(item, tuple) and len(item) >= 2:
                            emotion, intensity = item[0], item[1]
                            current_emotions.append({
                                "emotion": emotion.value if hasattr(emotion, 'value') else str(emotion),
                                "intensity": intensity,
                                "description": self._get_emotion_description(emotion, intensity)
                            })
            
            # 获取性格特征（如果有演化系统）
            personality_traits = self.base_persona["traits"].copy()
            
            # 获取最近行为
            recent_behaviors = self.behavior_history[-10:] if self.behavior_history else []
            
            # 生成记忆摘要
            memory_summary = self._generate_memory_summary()
            
            # 生成当前上下文
            context = self._generate_current_context()
            
            return PersonaSnapshot(
                timestamp=datetime.now(),
                basic_info=self.base_persona.copy(),
                personality_traits=personality_traits,
                current_emotions=current_emotions,
                recent_behaviors=recent_behaviors,
                memory_summary=memory_summary,
                context=context
            )
            
        except Exception as e:
            logger.error(f"获取人设快照失败: {e}")
            # 返回基础人设
            return PersonaSnapshot(
                timestamp=datetime.now(),
                basic_info=self.base_persona.copy(),
                personality_traits=self.base_persona["traits"].copy(),
                current_emotions=[],
                recent_behaviors=[],
                memory_summary="No memory summary",
                context="I'm having a daily conversation with the user"
            )
    
    def _get_emotion_description(self, emotion, intensity: float) -> str:
        """获取情绪描述"""
        emotion_str = emotion.value if hasattr(emotion, 'value') else str(emotion)
        
        intensity_desc = ""
        if intensity < 0.3:
            intensity_desc = "slight"
        elif intensity < 0.6:
            intensity_desc = "moderate"
        elif intensity < 0.8:
            intensity_desc = "strong"
        else:
            intensity_desc = "very strong"
        
        return f"{intensity_desc}{emotion_str}"
    
    def _generate_memory_summary(self) -> str:
        """生成记忆摘要"""
        try:
            # 这里可以接入AI记忆系统获取摘要
            # 暂时返回基础摘要
            return "I remember having a pleasant conversation with the user and learning a lot of interesting knowledge."
        except Exception as e:
            logger.error(f"生成记忆摘要失败: {e}")
            return "Memory system temporarily unavailable"
    
    def _generate_current_context(self) -> str:
        """生成当前上下文"""
        try:
            now = datetime.now()
            time_str = now.strftime("%H:%M")
            date_str = now.strftime("%Y-%m-%d")
            
            # 基于最近的行为生成上下文
            if self.behavior_history:
                latest_behavior = self.behavior_history[-1]
                context = f"It's {date_str} {time_str}, I just {latest_behavior['description']}"
            else:
                context = f"It's {date_str} {time_str}, I'm waiting for interaction with the user"
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to generate current context: {e}")
            return "I'm having a daily conversation with the user"
    
    def should_update_llm_persona(self) -> bool:
        """判断是否需要更新LLM人设"""
        if not self.config.persona_update_enabled:
            return False
        
        # 首次使用
        if self.last_persona_sent is None:
            return True
        
        # 检查情绪变化
        current_emotion_intensity = self._calculate_emotion_intensity()
        emotion_change = abs(current_emotion_intensity - self.last_emotion_intensity)
        
        if emotion_change >= self.config.emotion_threshold_for_llm:
            return True
        
        # 检查是否有重要行为记录
        if self.behavior_history:
            latest_behavior = self.behavior_history[-1]
            if latest_behavior.get("emotional_impact", 0) >= 0.5:
                return True
        
        return False
    
    def _calculate_emotion_intensity(self) -> float:
        """计算当前总体情绪强度"""
        try:
            if not hasattr(self.emotion_core, 'current_emotions'):
                return 0.0
            
            emotions = self.emotion_core.current_emotions
            if isinstance(emotions, dict):
                # 如果是字典形式 {emotion: intensity}
                total_intensity = sum(emotions.values())
            elif isinstance(emotions, list):
                # 如果是列表形式 [(emotion, intensity), ...]
                total_intensity = sum(item.intensity if hasattr(item, 'intensity') else item[1] 
                                    for item in emotions if hasattr(item, 'intensity') or (isinstance(item, tuple) and len(item) > 1))
            else:
                return 0.0
                
            return min(total_intensity, 1.0)
            
        except Exception as e:
            logger.error(f"计算情绪强度失败: {e}")
            return 0.0
    
    def generate_persona_prompt(self, context: str = "") -> str:
        """生成用于LLM的人设提示词"""
        try:
            snapshot = self.get_current_persona_snapshot()
            
            # 构建人设提示词
            prompt = f"""You are {snapshot.basic_info['name']}, a {snapshot.basic_info['age']} year old AI assistant with the mental age of a 3-year-old girl.

【Basic Settings】
{snapshot.basic_info['background']}

【Personality Traits】
"""
            for trait, value in snapshot.personality_traits.items():
                if value > 0.6:
                    prompt += f"- {trait}: very strong\n"
                elif value > 0.4:
                    prompt += f"- {trait}: moderate\n"
                else:
                    prompt += f"- {trait}: weak\n"

            prompt += f"\n【Speaking Style】\n{snapshot.basic_info['speaking_style']}\n"

            # 当前情绪状态
            if snapshot.current_emotions:
                prompt += "\n【Current Emotional State】\n"
                for emotion in snapshot.current_emotions:
                    prompt += f"- {emotion['description']}\n"
                prompt += "Please adjust your response tone and content based on the current emotional state.\n"

            # 最近行为
            if snapshot.recent_behaviors:
                prompt += "\n【Recent Behavior Record】\n"
                for behavior in snapshot.recent_behaviors[-3:]:  # 只显示最近3个
                    prompt += f"- {behavior['description']}\n"

            # 当前上下文
            if snapshot.context:
                prompt += f"\n【Current Situation】\n{snapshot.context}\n"

            # 额外上下文
            if context:
                prompt += f"\n【Dialogue Context】\n{context}\n"

            prompt += """
【重要提醒】
- Please respond strictly according to the above persona
- Adjust your tone based on the current emotional state
- Show the thinking of a 3-year-old
- Keep consistency and authenticity in your role
- Avoid using rigid template language
"""

            # 更新记录
            self.last_persona_sent = snapshot
            self.last_emotion_intensity = self._calculate_emotion_intensity()
            
            return prompt
            
        except Exception as e:
            logger.error(f"Failed to generate persona prompt: {e}")
            return f"You are {self.base_persona['name']}, please keep a friendly and cute attitude when talking to the user."

# 全局实例
_persona_manager = None

def get_persona_manager() -> PersonaManager:
    """获取全局人设管理器实例"""
    global _persona_manager
    if _persona_manager is None:
        from emotional_ai_core import get_emotion_core
        from config import config
        emotion_core = get_emotion_core(config)
        _persona_manager = PersonaManager(emotion_core)
    return _persona_manager

def record_ai_behavior(behavior_type: str, description: str, 
                      emotional_impact: float = 0.0, context: Dict = None):
    """快捷函数：记录AI行为"""
    try:
        manager = get_persona_manager()
        manager.record_behavior(behavior_type, description, emotional_impact, context)
    except Exception as e:
        logger.error(f"记录AI行为失败: {e}")

def get_persona_prompt(context: str = "") -> str:
    """快捷函数：获取人设提示词"""
    try:
        manager = get_persona_manager()
        return manager.generate_persona_prompt(context)
    except Exception as e:
        logger.error(f"获取人设提示词失败: {e}")
        return "Please keep a friendly and cute attitude when talking to the user."