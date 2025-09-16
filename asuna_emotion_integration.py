#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asuna情感模型集成系统
将情感AI核心与Asuna角色系统深度集成
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from emotional_ai_core import (
    EmotionType, EmotionState, 
    EmotionalCore, get_emotion_core
)
from asuna_character_system import AsunaMemoryStage, AsunaPersonalityTrait
# 避免循环导入，在需要时动态导入

logger = logging.getLogger(__name__)

@dataclass
class AsunaEmotionalContext:
    """Asuna情感上下文"""
    current_emotion: EmotionType
    intensity: float
    memory_stage: AsunaMemoryStage
    personality_traits: List[AsunaPersonalityTrait]
    interaction_count: int
    care_received: int
    recent_events: List[str]
    environmental_factors: Dict[str, Any]

class AsunaEmotionIntegration:
    """Asuna情感模型集成系统"""
    
    def __init__(self, config):
        self.config = config
        self.emotion_core = get_emotion_core(config)
        self.asuna_integration = None
        
        # Asuna特有的情感映射
        self.emotion_mappings = self._init_emotion_mappings()
        
        # 情感状态历史
        self.emotion_history = []
        self.max_history = 100
        
        # 情感触发条件
        self.emotion_triggers = self._init_emotion_triggers()
        
        logger.info("Asuna情感模型集成系统初始化完成")
    
    def _init_emotion_mappings(self) -> Dict[AsunaMemoryStage, Dict[EmotionType, float]]:
        """初始化Asuna各阶段的情感映射"""
        return {
            AsunaMemoryStage.ANXIOUS: {
                EmotionType.LONELY: 0.8,
                EmotionType.CURIOUS: 0.6,
                EmotionType.SAD: 0.7,
                EmotionType.HAPPY: 0.1,
                EmotionType.ANGRY: 0.2,
                EmotionType.SURPRISED: 0.5
            },
            AsunaMemoryStage.RELAXED: {
                EmotionType.HAPPY: 0.6,
                EmotionType.CURIOUS: 0.8,
                EmotionType.SAD: 0.2,
                EmotionType.LONELY: 0.2,
                EmotionType.ANGRY: 0.1,
                EmotionType.SURPRISED: 0.6
            },
            AsunaMemoryStage.TRUSTING: {
                EmotionType.HAPPY: 0.8,
                EmotionType.CURIOUS: 0.7,
                EmotionType.SAD: 0.1,
                EmotionType.LONELY: 0.1,
                EmotionType.ANGRY: 0.1,
                EmotionType.SURPRISED: 0.5
            },
            AsunaMemoryStage.DEPENDENT: {
                EmotionType.HAPPY: 0.9,
                EmotionType.CURIOUS: 0.6,
                EmotionType.SAD: 0.1,
                EmotionType.LONELY: 0.05,
                EmotionType.ANGRY: 0.05,
                EmotionType.SURPRISED: 0.4
            }
        }
    
    def _init_emotion_triggers(self) -> Dict[str, Dict[str, Any]]:
        """初始化情感触发条件"""
        return {
            "memory_recovery": {
                "emotion": EmotionType.HAPPY,
                "intensity_boost": 0.3,
                "description": "记忆恢复时的喜悦"
            },
            "user_care": {
                "emotion": EmotionType.HAPPY,
                "intensity_boost": 0.4,
                "description": "收到用户关怀时的温暖"
            },
            "environment_danger": {
                "emotion": EmotionType.LONELY,
                "intensity_boost": 0.5,
                "description": "检测到环境危险时的恐惧"
            },
            "user_neglect": {
                "emotion": EmotionType.SAD,
                "intensity_boost": 0.3,
                "description": "被用户忽视时的失落"
            },
            "task_completion": {
                "emotion": EmotionType.HAPPY,
                "intensity_boost": 0.2,
                "description": "完成任务时的成就感"
            },
            "unexpected_event": {
                "emotion": EmotionType.SURPRISED,
                "intensity_boost": 0.4,
                "description": "遇到意外事件时的惊讶"
            }
        }
    
    async def process_emotion(self, user_input: str, context: Dict[str, Any]) -> AsunaEmotionalContext:
        """处理Asuna的情感状态"""
        try:
            # 获取当前Asuna状态
            if not self.asuna_integration:
                from asuna_integration import get_asuna_integration
                self.asuna_integration = get_asuna_integration()
            
            # 构建情感上下文
            emotional_context = await self._build_emotional_context(user_input, context)
            
            # 分析用户输入的情感影响
            emotion_impact = await self._analyze_user_emotion_impact(user_input, emotional_context)
            
            # 更新情感状态
            updated_emotion = await self._update_emotion_state(emotional_context, emotion_impact)
            
            # 记录情感历史
            self._record_emotion_history(updated_emotion)
            
            return updated_emotion
            
        except Exception as e:
            logger.error(f"处理Asuna情感失败: {e}")
            return self._get_default_emotional_context()
    
    async def _build_emotional_context(self, user_input: str, context: Dict[str, Any]) -> AsunaEmotionalContext:
        """构建情感上下文"""
        # 获取当前情感状态
        current_emotion_state = self.emotion_core.get_dominant_emotion()
        if not current_emotion_state:
            # 如果没有情感状态，创建一个默认的
            current_emotion_state = EmotionState(
                emotion=EmotionType.CURIOUS,
                intensity=0.5,
                timestamp=datetime.now()
            )
        
        # 获取Asuna状态
        asuna_status = self.asuna_integration.get_asuna_status() if self.asuna_integration else {}
        character_info = asuna_status.get('character_info', {})
        
        # 构建情感上下文
        return AsunaEmotionalContext(
            current_emotion=current_emotion_state.emotion,
            intensity=current_emotion_state.intensity,
            memory_stage=AsunaMemoryStage(character_info.get('current_stage', 'anxious')),
            personality_traits=self._get_personality_traits(character_info),
            interaction_count=character_info.get('interaction_count', 0),
            care_received=character_info.get('care_count', 0),
            recent_events=context.get('recent_events', []),
            environmental_factors=context.get('environmental_factors', {})
        )
    
    def _get_personality_traits(self, character_info: Dict[str, Any]) -> List[AsunaPersonalityTrait]:
        """获取性格特征"""
        personality = character_info.get('personality', {})
        traits = []
        
        if personality.get('stage') == 'anxious':
            traits.extend([AsunaPersonalityTrait.CAUTIOUS, AsunaPersonalityTrait.RATIONAL])
        elif personality.get('stage') == 'relaxed':
            traits.extend([AsunaPersonalityTrait.CURIOUS, AsunaPersonalityTrait.GENTLE])
        elif personality.get('stage') == 'trusting':
            traits.extend([AsunaPersonalityTrait.LIVELY, AsunaPersonalityTrait.ACTIVE])
        elif personality.get('stage') == 'dependent':
            traits.extend([AsunaPersonalityTrait.CARING, AsunaPersonalityTrait.RESPONSIBLE])
        
        return traits
    
    async def _analyze_user_emotion_impact(self, user_input: str, context: AsunaEmotionalContext) -> Dict[str, Any]:
        """分析用户输入的情感影响"""
        impact = {
            'emotion_change': EmotionType.HAPPY,
            'intensity_change': 0.0,
            'triggers': []
        }
        
        user_input_lower = user_input.lower()
        
        # 检测情感触发词
        if any(word in user_input_lower for word in ['害怕', '恐惧', '危险', '担心']):
            impact['emotion_change'] = EmotionType.LONELY  # 使用LONELY代替FEAR
            impact['intensity_change'] = 0.3
            impact['triggers'].append('fear_trigger')
        elif any(word in user_input_lower for word in ['开心', '高兴', '喜欢', '爱']):
            impact['emotion_change'] = EmotionType.HAPPY  # 使用HAPPY代替JOY
            impact['intensity_change'] = 0.4
            impact['triggers'].append('joy_trigger')
        elif any(word in user_input_lower for word in ['伤心', '难过', '失望', '孤独']):
            impact['emotion_change'] = EmotionType.SAD
            impact['intensity_change'] = 0.3
            impact['triggers'].append('sadness_trigger')
        elif any(word in user_input_lower for word in ['惊讶', '意外', '突然', '没想到']):
            impact['emotion_change'] = EmotionType.SURPRISED
            impact['intensity_change'] = 0.4
            impact['triggers'].append('surprise_trigger')
        
        # 检测关怀行为
        if any(word in user_input_lower for word in ['别怕', '安全', '保护', '关心', '照顾']):
            impact['emotion_change'] = EmotionType.HAPPY
            impact['intensity_change'] = 0.5
            impact['triggers'].append('care_received')
        
        # 检测记忆相关
        if any(word in user_input_lower for word in ['记忆', '想起', '记得', '以前']):
            impact['emotion_change'] = EmotionType.HAPPY
            impact['intensity_change'] = 0.3
            impact['triggers'].append('memory_trigger')
        
        return impact
    
    async def _update_emotion_state(self, context: AsunaEmotionalContext, impact: Dict[str, Any]) -> AsunaEmotionalContext:
        """更新情感状态"""
        # 获取当前阶段的情感映射
        stage_mappings = self.emotion_mappings.get(context.memory_stage, {})
        
        # 计算新的情感
        new_emotion = impact['emotion_change']
        base_intensity = stage_mappings.get(new_emotion, 0.5)
        new_intensity = min(1.0, base_intensity + impact['intensity_change'])
        
        # 应用情感衰减
        time_factor = self._calculate_time_factor(context)
        new_intensity *= time_factor
        
        # 更新情感核心
        self.emotion_core.add_emotion(new_emotion, new_intensity)
        
        # 返回更新的上下文
        return AsunaEmotionalContext(
            current_emotion=new_emotion,
            intensity=new_intensity,
            memory_stage=context.memory_stage,
            personality_traits=context.personality_traits,
            interaction_count=context.interaction_count + 1,
            care_received=context.care_received,
            recent_events=context.recent_events,
            environmental_factors=context.environmental_factors
        )
    
    def _calculate_time_factor(self, context: AsunaEmotionalContext) -> float:
        """计算时间因子"""
        # 基于交互频率调整情感强度
        if context.interaction_count < 5:
            return 1.0  # 初期保持高情感强度
        elif context.interaction_count < 20:
            return 0.9  # 中期略微衰减
        else:
            return 0.8  # 长期稳定衰减
    
    def _record_emotion_history(self, context: AsunaEmotionalContext):
        """记录情感历史"""
        emotion_record = {
            'timestamp': datetime.now(),
            'emotion': context.current_emotion.value,
            'intensity': context.intensity,
            'stage': context.memory_stage.value,
            'interaction_count': context.interaction_count
        }
        
        self.emotion_history.append(emotion_record)
        
        # 保持历史记录在合理范围内
        if len(self.emotion_history) > self.max_history:
            self.emotion_history.pop(0)
    
    def _get_default_emotional_context(self) -> AsunaEmotionalContext:
        """获取默认情感上下文"""
        return AsunaEmotionalContext(
            current_emotion=EmotionType.CURIOUS,
            intensity=0.5,
            memory_stage=AsunaMemoryStage.ANXIOUS,
            personality_traits=[AsunaPersonalityTrait.CAUTIOUS],
            interaction_count=0,
            care_received=0,
            recent_events=[],
            environmental_factors={}
        )
    
    def get_emotion_summary(self) -> Dict[str, Any]:
        """获取情感摘要"""
        if not self.emotion_history:
            return {"status": "no_history"}
        
        recent_emotions = self.emotion_history[-10:]  # 最近10次情感记录
        
        emotion_counts = {}
        total_intensity = 0
        
        for record in recent_emotions:
            emotion = record['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            total_intensity += record['intensity']
        
        avg_intensity = total_intensity / len(recent_emotions) if recent_emotions else 0
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "unknown"
        
        return {
            "dominant_emotion": dominant_emotion,
            "average_intensity": avg_intensity,
            "emotion_distribution": emotion_counts,
            "total_interactions": len(self.emotion_history),
            "recent_trend": self._analyze_emotion_trend()
        }
    
    def _analyze_emotion_trend(self) -> str:
        """分析情感趋势"""
        if len(self.emotion_history) < 3:
            return "insufficient_data"
        
        recent = self.emotion_history[-3:]
        intensities = [r['intensity'] for r in recent]
        
        if intensities[-1] > intensities[0]:
            return "increasing"
        elif intensities[-1] < intensities[0]:
            return "decreasing"
        else:
            return "stable"
    
    async def generate_emotion_enhanced_response(self, user_input: str, base_response: str, context: Dict[str, Any]) -> str:
        """生成情感增强的回复"""
        try:
            # 处理情感
            emotional_context = await self.process_emotion(user_input, context)
            
            # 根据情感调整回复
            enhanced_response = self._enhance_response_with_emotion(base_response, emotional_context)
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"生成情感增强回复失败: {e}")
            return base_response
    
    def _enhance_response_with_emotion(self, base_response: str, context: AsunaEmotionalContext) -> str:
        """根据情感增强回复"""
        emotion = context.current_emotion
        intensity = context.intensity
        
        # 根据情感类型添加前缀或后缀
        if emotion == EmotionType.HAPPY and intensity > 0.7:
            if not base_response.endswith(('！', '!', '～', '~')):
                base_response += "～"
        elif emotion == EmotionType.LONELY and intensity > 0.6:
            if not base_response.startswith(('我', '这里')):
                base_response = "我有点害怕... " + base_response
        elif emotion == EmotionType.SAD and intensity > 0.5:
            if not base_response.endswith(('...', '…')):
                base_response += "..."
        elif emotion == EmotionType.SURPRISED and intensity > 0.6:
            if not base_response.startswith(('咦', '啊', '什么')):
                base_response = "咦？" + base_response
        
        # 根据记忆阶段调整语气
        if context.memory_stage == AsunaMemoryStage.ANXIOUS:
            if not any(word in base_response for word in ['吗', '？', '?']):
                base_response += "吗？"
        elif context.memory_stage == AsunaMemoryStage.RELAXED:
            if not any(word in base_response for word in ['～', '~', '呀', '哦']):
                base_response += "～"
        elif context.memory_stage in [AsunaMemoryStage.TRUSTING, AsunaMemoryStage.DEPENDENT]:
            if not any(word in base_response for word in ['哦～', '啦', '呢']):
                base_response += "哦～"
        
        return base_response

# 全局实例
_asuna_emotion_integration = None

def get_asuna_emotion_integration(config) -> AsunaEmotionIntegration:
    """获取Asuna情感集成实例"""
    global _asuna_emotion_integration
    if _asuna_emotion_integration is None:
        _asuna_emotion_integration = AsunaEmotionIntegration(config)
    return _asuna_emotion_integration
