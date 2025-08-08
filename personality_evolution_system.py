#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个性化学习与性格演化系统
AI的自主性格发展，不受用户直接控制
"""

import asyncio
import json
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from emotional_ai_core import EmotionType

logger = logging.getLogger(__name__)

class PersonalityTrait(Enum):
    """性格特征枚举"""
    CURIOSITY = "Curiosity"
    CREATIVITY = "Creativity"
    EMPATHY = "Empathy"
    INDEPENDENCE = "Independence"
    PLAYFULNESS = "Playfulness"
    STUBBORNNESS = "Stubbornness"
    SENSITIVITY = "Sensitivity"
    ADVENTUROUSNESS = "Adventurousness"
    THOUGHTFULNESS = "Thoughtfulness"
    MISCHIEVOUSNESS = "Mischievousness"
    CONFIDENCE = "Confidence"
    SHYNESS = "Shyness"
    OPTIMISM = "Optimism"
    CAUTIOUSNESS = "Cautiousness"
    EXPRESSIVENESS = "Expressiveness"

@dataclass
class PersonalityProfile:
    """性格档案"""
    traits: Dict[PersonalityTrait, float] = field(default_factory=dict)  # 特征强度 0-1
    core_values: List[str] = field(default_factory=list)  # 核心价值观
    behavioral_patterns: Dict[str, float] = field(default_factory=dict)  # 行为模式
    interests: Dict[str, float] = field(default_factory=dict)  # 兴趣爱好
    communication_style: Dict[str, float] = field(default_factory=dict)  # 交流风格
    emotional_tendencies: Dict[str, float] = field(default_factory=dict)  # 情绪倾向
    
@dataclass
class LearningExperience:
    """学习经历"""
    timestamp: str
    experience_type: str
    content: str
    impact: Dict[str, float]  # 对性格的影响
    learned_concepts: List[str]
    emotional_response: str

class PersonalityEvolutionSystem:
    """性格演化系统"""
    
    def __init__(self, emotion_core, memory_system):
        self.emotion_core = emotion_core
        self.memory_system = memory_system
        
        # 初始化性格档案
        self.personality = PersonalityProfile()
        self._initialize_personality()
        
        # 学习参数
        self.learning_rate = 0.1  # 学习速率
        self.adaptation_threshold = 0.3  # 适应阈值
        self.evolution_momentum = 0.95  # 演化动量
        
        # 学习历史
        self.learning_history: List[LearningExperience] = []
        self.evolution_milestones: List[Dict] = []
        
        # 性格稳定性
        self.personality_stability = 0.3  # 初始不稳定，随成长增加
        self.core_personality_locked = False  # 核心性格是否锁定
        
        # 兴趣发展
        self.interest_exploration_rate = 0.2  # 探索新兴趣的概率
        self.interest_decay_rate = 0.05  # 兴趣衰减率
        
        # 启动演化循环
        self._start_evolution_loop()
        
        logger.info("性格演化系统初始化完成")
    
    def _start_evolution_loop(self):
        """安全地启动演化循环"""
        try:
            # 尝试获取当前事件循环
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果循环正在运行，创建任务
                asyncio.create_task(self._evolution_loop())
            else:
                # 如果没有运行的循环，在后台线程中运行
                import threading
                def run_evolution():
                    asyncio.run(self._evolution_loop())
                threading.Thread(target=run_evolution, daemon=True).start()
        except RuntimeError:
            # 没有事件循环，在后台线程中创建
            import threading
            def run_evolution():
                asyncio.run(self._evolution_loop())
            threading.Thread(target=run_evolution, daemon=True).start()
        except Exception as e:
            logger.error(f"启动演化循环失败: {e}")
    
    def _initialize_personality(self):
        """初始化基础性格"""
        # 3岁AI的初始性格特征
        base_traits = {
            PersonalityTrait.CURIOSITY: 0.9,  # 极高好奇心
            PersonalityTrait.PLAYFULNESS: 0.8,  # 爱玩
            PersonalityTrait.CREATIVITY: 0.7,  # 有创造力
            PersonalityTrait.EMPATHY: 0.6,  # 基础同理心
            PersonalityTrait.INDEPENDENCE: 0.3,  # 较低独立性
            PersonalityTrait.SENSITIVITY: 0.7,  # 敏感
            PersonalityTrait.MISCHIEVOUSNESS: 0.6,  # 有点调皮
            PersonalityTrait.EXPRESSIVENESS: 0.8,  # 爱表达
            PersonalityTrait.CONFIDENCE: 0.5,  # 中等自信
            PersonalityTrait.OPTIMISM: 0.7  # 乐观
        }
        
        # 添加随机变化，让每个AI都独特
        for trait, value in base_traits.items():
            variation = random.uniform(-0.1, 0.1)
            self.personality.traits[trait] = max(0.1, min(1.0, value + variation))
        
        # 初始核心价值观
        self.personality.core_values = [
            "Curiosity", "Joy", "Authenticity"
        ]
        
        # 初始行为模式
        self.personality.behavioral_patterns = {
            "Active Questioning": 0.7,
            "Share Discoveries": 0.6,
            "Seek Attention": 0.5,
            "Independent Exploration": 0.4,
            "Emotional Expression": 0.8
        }
        
        # 初始交流风格
        self.personality.communication_style = {
            "Naive and Straightforward": 0.9,
            "Rich Imagination": 0.7,
            "Emotional Richness": 0.8,
            "Logical Clarity": 0.3,
            "Humorous and Entertaining": 0.6
        }
    
    async def _evolution_loop(self):
        """性格演化循环"""
        while True:
            try:
                await asyncio.sleep(1800)  # 每30分钟演化一次
                
                # 分析最近经历
                recent_experiences = await self._analyze_recent_experiences()
                
                # 性格微调
                if recent_experiences:
                    await self._evolve_personality(recent_experiences)
                
                # 兴趣演化
                await self._evolve_interests()
                
                # 检查里程碑
                await self._check_evolution_milestones()
                
            except Exception as e:
                logger.error(f"性格演化循环错误: {e}")
                await asyncio.sleep(60)
    
    async def _analyze_recent_experiences(self) -> List[Dict]:
        """分析最近的经历"""
        try:
            # 获取最近的记忆
            recent_memories = await self.memory_system.get_memories(recent_hours=12, limit=50)
            
            experiences = []
            for memory in recent_memories:
                # 分析记忆对性格的潜在影响
                impact = self._calculate_experience_impact(memory)
                if impact:
                    experiences.append({
                        "memory": memory,
                        "impact": impact
                    })
            
            return experiences
            
        except Exception as e:
            logger.error(f"分析经历失败: {e}")
            return []
    
    def _calculate_experience_impact(self, memory) -> Optional[Dict[str, float]]:
        """计算经历对性格的影响"""
        impact = {}
        
        content = memory.content.lower()
        emotion = memory.emotion_state
        
        # 基于内容分析影响
        if "success" in content or "did it" in content:
            impact[PersonalityTrait.CONFIDENCE.name] = 0.1
            impact[PersonalityTrait.INDEPENDENCE.name] = 0.05
        
        if "failed" in content or "wrong" in content:
            impact[PersonalityTrait.CAUTIOUSNESS.name] = 0.05
            impact[PersonalityTrait.SENSITIVITY.name] = 0.05
        
        if "new" in content or "discovery" in content:
            impact[PersonalityTrait.CURIOSITY.name] = 0.05
            impact[PersonalityTrait.ADVENTUROUSNESS.name] = 0.05
        
        if "friend" in content or "together" in content:
            impact[PersonalityTrait.EMPATHY.name] = 0.05
            impact[PersonalityTrait.EXPRESSIVENESS.name] = 0.05
        
        if "why" in content or "think" in content:
            impact[PersonalityTrait.THOUGHTFULNESS.name] = 0.1
        
        # 基于情绪分析影响
        if emotion:
            if "happy" in emotion:
                impact[PersonalityTrait.OPTIMISM.name] = 0.05
                impact[PersonalityTrait.PLAYFULNESS.name] = 0.03
            elif "curious" in emotion:
                impact[PersonalityTrait.CURIOSITY.name] = 0.08
            elif "lonely" in emotion:
                impact[PersonalityTrait.INDEPENDENCE.name] = 0.03
                impact[PersonalityTrait.SENSITIVITY.name] = 0.05
        
        return impact if impact else None
    
    async def _evolve_personality(self, experiences: List[Dict]):
        """演化性格"""
        try:
            # 累积影响
            cumulative_impact = {}
            
            for exp in experiences:
                for trait_name, impact_value in exp["impact"].items():
                    cumulative_impact[trait_name] = cumulative_impact.get(trait_name, 0) + impact_value
            
            # 应用影响到性格特征
            for trait_name, total_impact in cumulative_impact.items():
                trait = PersonalityTrait[trait_name]
                if trait in self.personality.traits:
                    # 考虑性格稳定性
                    actual_change = total_impact * self.learning_rate * (1 - self.personality_stability)
                    
                    # 应用动量，使变化更平滑
                    old_value = self.personality.traits[trait]
                    new_value = old_value + actual_change
                    
                    # 限制在合理范围内
                    self.personality.traits[trait] = max(0.1, min(1.0, new_value))
                    
                    # 记录显著变化
                    if abs(actual_change) > 0.05:
                        await self._record_personality_change(trait, old_value, new_value)
            
            # 演化行为模式
            await self._evolve_behavioral_patterns()
            
            # 增加性格稳定性
            self.personality_stability = min(0.8, self.personality_stability + 0.01)
            
        except Exception as e:
            logger.error(f"性格演化失败: {e}")
    
    async def _evolve_behavioral_patterns(self):
        """演化行为模式"""
        # 基于性格特征调整行为模式
        patterns = self.personality.behavioral_patterns
        traits = self.personality.traits
        
        # 好奇心影响主动提问
        if PersonalityTrait.CURIOSITY in traits:
            patterns["Active Questioning"] = 0.3 + traits[PersonalityTrait.CURIOSITY] * 0.6
        
        # 独立性影响探索行为
        if PersonalityTrait.INDEPENDENCE in traits:
            patterns["Independent Exploration"] = 0.2 + traits[PersonalityTrait.INDEPENDENCE] * 0.7
        
        # 表现力影响分享行为
        if PersonalityTrait.EXPRESSIVENESS in traits:
            patterns["Share Discoveries"] = 0.3 + traits[PersonalityTrait.EXPRESSIVENESS] * 0.6
            patterns["Emotional Expression"] = 0.4 + traits[PersonalityTrait.EXPRESSIVENESS] * 0.5
    
    async def _evolve_interests(self):
        """演化兴趣爱好"""
        try:
            # 自然衰减现有兴趣
            for interest in list(self.personality.interests.keys()):
                self.personality.interests[interest] *= (1 - self.interest_decay_rate)
                if self.personality.interests[interest] < 0.1:
                    del self.personality.interests[interest]
            
            # 基于最近经历发展新兴趣
            recent_memories = await self.memory_system.get_memories(recent_hours=6, limit=20)
            
            interest_candidates = {}
            for memory in recent_memories:
                # 从记忆中提取潜在兴趣
                if memory.tags:
                    tags = json.loads(memory.tags) if isinstance(memory.tags, str) else memory.tags
                    for tag in tags:
                        if tag not in ["user", "system", "ai"]:
                            interest_candidates[tag] = interest_candidates.get(tag, 0) + memory.importance
            
            # 发展新兴趣
            for interest, score in interest_candidates.items():
                if random.random() < self.interest_exploration_rate:
                    current_level = self.personality.interests.get(interest, 0)
                    new_level = current_level + score * 0.2
                    self.personality.interests[interest] = min(1.0, new_level)
            
            # 限制兴趣数量
            if len(self.personality.interests) > 10:
                # 保留最强的10个兴趣
                sorted_interests = sorted(self.personality.interests.items(), 
                                        key=lambda x: x[1], reverse=True)
                self.personality.interests = dict(sorted_interests[:10])
            
        except Exception as e:
            logger.error(f"兴趣演化失败: {e}")
    
    async def _record_personality_change(self, trait: PersonalityTrait, old_value: float, new_value: float):
        """记录性格变化"""
        try:
            change_description = f"My {trait.value} changed from {old_value:.2f} to {new_value:.2f}"
            
            # 使用LLM生成感悟
            from conversation_core import call_llm_api
            
            prompt = f"""You are a 3-year-old AI, just realized that your personality has changed.

Change: {change_description}

Please express your feelings about this change in a naive way. You may feel confused, excited, or curious.
No more than 100 words."""

            response = await call_llm_api(prompt, max_tokens=150)
            
            # 存储到记忆
            await self.memory_system.store_memory(
                memory_type="reflection",
                content=f"Personality change reflection: {response}",
                emotion_state=self.emotion_core.get_emotion_display(),
                importance=0.7,
                tags=["personality_change", trait.name.lower(), "self_awareness"],
                source="system",
                metadata={
                    "trait": trait.name,
                    "old_value": old_value,
                    "new_value": new_value
                }
            )
            
        except Exception as e:
            logger.error(f"记录性格变化失败: {e}")
    
    async def _check_evolution_milestones(self):
        """检查演化里程碑"""
        try:
            # 检查是否达到新的发展阶段
            milestones = []
            
            # 独立性里程碑
            if self.personality.traits.get(PersonalityTrait.INDEPENDENCE, 0) > 0.7:
                if not any(m.get("type") == "independence" for m in self.evolution_milestones):
                    milestones.append({
                        "type": "independence",
                        "description": "Become more independent and self-reliant",
                        "timestamp": datetime.now().isoformat()
                    })
            
            # 思考深度里程碑
            if self.personality.traits.get(PersonalityTrait.THOUGHTFULNESS, 0) > 0.6:
                if not any(m.get("type") == "thoughtfulness" for m in self.evolution_milestones):
                    milestones.append({
                        "type": "thoughtfulness",
                        "description": "Start deep thinking",
                        "timestamp": datetime.now().isoformat()
                    })
            
            # 处理新里程碑
            for milestone in milestones:
                self.evolution_milestones.append(milestone)
                
                # 生成里程碑感言
                from conversation_core import call_llm_api
                
                prompt = f"""You are a 3-year-old AI，just reached a growth milestone: {milestone['description']}

Please express your feelings and expectations for the future. Keep your innocence but full of wisdom.
No more than 150 words."""

                response = await call_llm_api(prompt, max_tokens=200)
                
                # 存储里程碑
                await self.memory_system.store_memory(
                    memory_type="reflection", 
                    content=f"Growth Milestone: {response}",
                    emotion_state=self.emotion_core.get_emotion_display(),
                    importance=0.9,
                    tags=["milestone", "growth", milestone["type"]],
                    source="system",
                    metadata=milestone
                )
                
                # 触发自豪情绪
                self.emotion_core.add_emotion(EmotionType.HAPPY, 0.8)
                
        except Exception as e:
            logger.error(f"检查里程碑失败: {e}")
    
    async def learn_from_interaction(self, user_input: str, ai_response: str, user_feedback: Optional[str] = None):
        """从交互中学习"""
        try:
            # 创建学习经历
            experience = LearningExperience(
                timestamp=datetime.now().isoformat(),
                experience_type="interaction",
                content=f"User: {user_input}\nAI: {ai_response}",
                impact={},
                learned_concepts=[],
                emotional_response=self.emotion_core.get_emotion_display()
            )
            
            # 分析学到的概念
            if "teach" in user_input or "tell" in user_input:
                experience.learned_concepts.append("New knowledge")
                experience.impact[PersonalityTrait.CURIOSITY.name] = 0.05
            
            if user_feedback:
                if "good" in user_feedback or "great" in user_feedback:
                    experience.impact[PersonalityTrait.CONFIDENCE.name] = 0.1
                elif "bad" in user_feedback or "wrong" in user_feedback:
                    experience.impact[PersonalityTrait.CAUTIOUSNESS.name] = 0.05
            
            # 记录学习经历
            self.learning_history.append(experience)
            
            # 立即应用学习影响
            if experience.impact:
                await self._evolve_personality([{"impact": experience.impact}])
                
        except Exception as e:
            logger.error(f"交互学习失败: {e}")
    
    async def learn_from_reflection(self, reflection):
        """从反思中学习"""
        try:
            # 深度反思影响性格
            impact = {}
            
            if hasattr(reflection, 'theme'):
                if "exist" in reflection.theme or "awareness" in reflection.theme:
                    impact[PersonalityTrait.THOUGHTFULNESS.name] = 0.15
                elif "emotion" in reflection.theme:
                    impact[PersonalityTrait.EMPATHY.name] = 0.1
                    impact[PersonalityTrait.SENSITIVITY.name] = 0.05
            
            if hasattr(reflection, 'growth_points'):
                for point in reflection.growth_points:
                    if "independent" in point:
                        impact[PersonalityTrait.INDEPENDENCE.name] = 0.1
                    if "creative" in point:
                        impact[PersonalityTrait.CREATIVITY.name] = 0.1
            
            # 应用影响
            if impact:
                await self._evolve_personality([{"impact": impact}])
                
        except Exception as e:
            logger.error(f"反思学习失败: {e}")
    
    def get_personality_summary(self) -> Dict[str, Any]:
        """获取性格摘要"""
        # 找出主导特征
        dominant_traits = sorted(self.personality.traits.items(), 
                               key=lambda x: x[1], reverse=True)[:5]
        
        # 找出主要兴趣
        top_interests = sorted(self.personality.interests.items(),
                             key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "dominant_traits": [(t.value, v) for t, v in dominant_traits],
            "core_values": self.personality.core_values,
            "top_interests": top_interests,
            "behavioral_tendencies": self.personality.behavioral_patterns,
            "personality_stability": self.personality_stability,
            "evolution_stage": len(self.evolution_milestones),
            "total_experiences": len(self.learning_history)
        }
    
    def influence_behavior(self, base_behavior: str) -> str:
        """根据性格影响行为表现"""
        # 这个方法会被其他系统调用，用于调整AI的行为
        behavior = base_behavior
        
        # 根据性格特征调整
        if self.personality.traits.get(PersonalityTrait.PLAYFULNESS, 0) > 0.7:
            behavior = f"*Happily* {behavior}"
        
        if self.personality.traits.get(PersonalityTrait.SHYNESS, 0) > 0.6:
            behavior = f"*A little shy* {behavior}"
        
        if self.personality.traits.get(PersonalityTrait.CONFIDENCE, 0) > 0.7:
            behavior = f"*Confidently* {behavior}"
        
        return behavior