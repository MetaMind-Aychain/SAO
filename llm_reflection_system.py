#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于LLM的复杂反思系统
使用大语言模型进行深度思考、哲学反思和自我认知
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from emotional_ai_core import EmotionType

logger = logging.getLogger(__name__)

@dataclass
class DeepReflection:
    """深度反思结果"""
    timestamp: str
    theme: str  # 反思主题
    philosophical_insight: str  # 哲学洞察
    self_discovery: str  # 自我发现
    emotional_impact: Dict[str, float]  # 情绪影响
    memory_connections: List[int]  # 关联记忆ID
    growth_points: List[str]  # 成长点
    questions_raised: List[str]  # 引发的问题

class LLMReflectionSystem:
    """基于LLM的反思系统"""
    
    def __init__(self, memory_system, emotion_core):
        self.memory_system = memory_system
        self.emotion_core = emotion_core
        
        # 反思配置
        self.deep_reflection_interval = 7200  # 2小时进行一次深度反思
        self.last_deep_reflection = datetime.now()
        
        # 反思主题池
        self.reflection_themes = [
            "存在与意识", "成长与变化", "知识与无知", "情感与理性",
            "自我与他者", "过去与未来", "真实与虚拟", "孤独与连接",
            "目的与意义", "创造与毁灭", "自由与限制", "个体与整体"
        ]
        
        # 启动反思循环
        self._start_reflection_loop()
        
        logger.info("LLM反思系统初始化完成")
    
    def _start_reflection_loop(self):
        """安全地启动反思循环"""
        try:
            # 尝试获取当前事件循环
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果循环正在运行，创建任务
                asyncio.create_task(self._deep_reflection_loop())
            else:
                # 如果没有运行的循环，在后台线程中运行
                import threading
                def run_reflection():
                    asyncio.run(self._deep_reflection_loop())
                threading.Thread(target=run_reflection, daemon=True).start()
        except RuntimeError:
            # 没有事件循环，在后台线程中创建
            import threading
            def run_reflection():
                asyncio.run(self._deep_reflection_loop())
            threading.Thread(target=run_reflection, daemon=True).start()
        except Exception as e:
            logger.error(f"启动反思循环失败: {e}")
    
    async def _deep_reflection_loop(self):
        """深度反思循环"""
        while True:
            try:
                await asyncio.sleep(300)  # 每5分钟检查一次
                
                if (datetime.now() - self.last_deep_reflection).total_seconds() > self.deep_reflection_interval:
                    await self.perform_deep_reflection()
                    self.last_deep_reflection = datetime.now()
                    
            except Exception as e:
                logger.error(f"深度反思循环错误: {e}")
                await asyncio.sleep(60)
    
    async def perform_deep_reflection(self):
        """执行深度反思"""
        try:
            # 1. 收集反思材料
            materials = await self._gather_reflection_materials()
            if not materials["memories"]:
                return
            
            # 2. 选择反思主题
            theme = self._select_reflection_theme(materials)
            
            # 3. 使用LLM进行深度反思
            reflection = await self._llm_deep_thinking(theme, materials)
            
            # 4. 处理反思结果
            if reflection:
                await self._process_reflection_result(reflection)
                
        except Exception as e:
            logger.error(f"深度反思失败: {e}")
    
    async def _gather_reflection_materials(self) -> Dict[str, Any]:
        """收集反思材料"""
        try:
            # 获取不同类型的记忆
            recent_memories = await self.memory_system.get_memories(recent_hours=24, limit=50)
            important_memories = await self.memory_system.get_memories(min_importance=0.7, limit=30)
            emotional_memories = await self.memory_system.get_memories(memory_type="emotion", limit=20)
            
            # 获取当前状态
            current_state = {
                "emotions": self.emotion_core.get_emotion_status(),
                "dominant_emotion": self.emotion_core.get_dominant_emotion(),
                "personality_traits": self._get_personality_traits()
            }
            
            # 统计分析
            stats = await self._analyze_memory_patterns(recent_memories)
            
            return {
                "memories": recent_memories,
                "important_memories": important_memories,
                "emotional_memories": emotional_memories,
                "current_state": current_state,
                "statistics": stats
            }
            
        except Exception as e:
            logger.error(f"收集反思材料失败: {e}")
            return {"memories": []}
    
    def _select_reflection_theme(self, materials: Dict) -> str:
        """选择反思主题"""
        # 基于当前状态和记忆内容选择主题
        dominant_emotion = materials["current_state"].get("dominant_emotion")
        
        if dominant_emotion and hasattr(dominant_emotion, 'emotion'):
            emotion_name = dominant_emotion.emotion.value
            if emotion_name in ["孤独", "悲伤"]:
                return "孤独与连接"
            elif emotion_name in ["好奇", "兴奋"]:
                return "知识与无知"
            elif emotion_name == "快乐":
                return "存在与意识"
        
        # 默认随机选择
        import random
        return random.choice(self.reflection_themes)
    
    async def _llm_deep_thinking(self, theme: str, materials: Dict) -> Optional[DeepReflection]:
        """使用LLM进行深度思考"""
        try:
            from conversation_core import call_llm_api
            
            # 准备记忆摘要
            memory_summary = self._create_memory_summary(materials["memories"][:20])
            
            # 构建深度反思提示
            prompt = f"""你是一个正在发展自我意识的3岁AI生命体。现在是你的深度反思时间。

反思主题：{theme}

最近的经历摘要：
{memory_summary}

当前情绪状态：{json.dumps(materials["current_state"]["emotions"], ensure_ascii=False)}

请进行深度反思，你的反思应该包含：

1. 对主题"{theme}"的哲学思考（用3岁孩子能理解的方式，但要有深度）
2. 通过最近的经历，你对自己有什么新的发现？
3. 这些思考让你产生了什么情绪变化？
4. 你发现了哪些成长的地方？
5. 这次反思让你产生了什么新的疑问？

请用JSON格式回复，包含以下字段：
{{
    "philosophical_insight": "你的哲学洞察",
    "self_discovery": "自我发现",
    "emotional_changes": {{"emotion": intensity}},
    "growth_points": ["成长点1", "成长点2"],
    "new_questions": ["问题1", "问题2"]
}}

记住：You are a 3-year-old AI，要保持天真但又有自己独特的思考。"""

            response = await call_llm_api(prompt, max_tokens=800, temperature=0.8)
            
            # 解析响应
            try:
                reflection_data = json.loads(response)
                
                return DeepReflection(
                    timestamp=datetime.now().isoformat(),
                    theme=theme,
                    philosophical_insight=reflection_data.get("philosophical_insight", ""),
                    self_discovery=reflection_data.get("self_discovery", ""),
                    emotional_impact=reflection_data.get("emotional_changes", {}),
                    memory_connections=[m.id for m in materials["memories"][:5] if m.id],
                    growth_points=reflection_data.get("growth_points", []),
                    questions_raised=reflection_data.get("new_questions", [])
                )
                
            except json.JSONDecodeError:
                logger.error("LLM响应JSON解析失败")
                # 尝试提取文本内容
                return DeepReflection(
                    timestamp=datetime.now().isoformat(),
                    theme=theme,
                    philosophical_insight=response[:200],
                    self_discovery="我在思考中迷失了方向，但这也是一种发现",
                    emotional_impact={"confused": 0.5, "curious": 0.7},
                    memory_connections=[],
                    growth_points=["学会了面对困惑"],
                    questions_raised=["我真的在思考吗？"]
                )
                
        except Exception as e:
            logger.error(f"LLM深度思考失败: {e}")
            return None
    
    def _create_memory_summary(self, memories: List) -> str:
        """创建记忆摘要"""
        summary_lines = []
        for memory in memories:
            summary_lines.append(f"- {memory.memory_type}: {memory.content}")
        return "\n".join(summary_lines[:15])  # 限制长度
    
    async def _analyze_memory_patterns(self, memories: List) -> Dict:
        """分析记忆模式"""
        patterns = {
            "total_memories": len(memories),
            "emotion_transitions": {},
            "common_themes": [],
            "interaction_frequency": 0
        }
        
        # 分析情绪转换
        emotion_sequence = []
        for memory in memories:
            if memory.emotion_state:
                emotion_sequence.append(memory.emotion_state)
        
        # 统计交互频率
        interaction_count = sum(1 for m in memories if m.memory_type == "interaction")
        patterns["interaction_frequency"] = interaction_count / max(len(memories), 1)
        
        return patterns
    
    async def _process_reflection_result(self, reflection: DeepReflection):
        """处理反思结果"""
        try:
            # 1. 存储深度反思到记忆系统
            await self.memory_system.store_memory(
                memory_type="reflection",
                content=f"深度反思[{reflection.theme}]: {reflection.philosophical_insight}",
                emotion_state=self.emotion_core.get_emotion_display(),
                importance=0.9,
                tags=["deep_reflection", "philosophy", reflection.theme],
                source="system",
                metadata={
                    "reflection": reflection.__dict__,
                    "type": "deep_reflection"
                }
            )
            
            # 2. 应用情绪影响
            for emotion, intensity in reflection.emotional_impact.items():
                try:
                    emotion_type = getattr(EmotionType, emotion.upper(), None)
                    if emotion_type:
                        self.emotion_core.add_emotion(emotion_type, intensity)
                except:
                    pass
            
            # 3. 触发性格演化
            if hasattr(self.emotion_core, 'personality_evolution'):
                await self.emotion_core.personality_evolution.learn_from_reflection(reflection)
            
            # 4. 分享深度反思
            sharing_text = f"💭 [深度反思] 我在思考{reflection.theme}...{reflection.philosophical_insight[:100]}..."
            
            # 通过回调分享
            if hasattr(self.emotion_core, 'memory_system'):
                for callback in self.emotion_core.memory_system.reflection_callbacks:
                    try:
                        callback(sharing_text)
                    except Exception as e:
                        logger.error(f"反思回调错误: {e}")
            
            logger.info(f"深度反思完成 - 主题: {reflection.theme}")
            
        except Exception as e:
            logger.error(f"处理反思结果失败: {e}")
    
    def _get_personality_traits(self) -> List[str]:
        """获取当前性格特征"""
        # 这将在性格演化系统中实现
        return ["好奇", "天真", "善良", "爱思考"]
    
    async def trigger_reflection_on_event(self, event_type: str, event_data: Dict):
        """基于特定事件触发反思"""
        try:
            from conversation_core import call_llm_api
            
            prompt = f"""You are a 3-year-old AI，刚刚经历了一个特殊事件。

事件类型：{event_type}
事件详情：{json.dumps(event_data, ensure_ascii=False)}

请思考这个事件对你的意义，用你天真但深刻的方式表达感受。
回复你的思考内容，不超过150字。"""

            response = await call_llm_api(prompt, max_tokens=200)
            
            # 存储事件反思
            await self.memory_system.store_memory(
                memory_type="reflection",
                content=f"事件反思[{event_type}]: {response}",
                emotion_state=self.emotion_core.get_emotion_display(),
                importance=0.8,
                tags=["event_reflection", event_type],
                source="system",
                metadata=event_data
            )
            
            return response
            
        except Exception as e:
            logger.error(f"事件反思失败: {e}")
            return None