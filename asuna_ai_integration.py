#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asuna真实AI集成系统
连接LLM进行智能回复，支持降级模式
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from openai import AsyncOpenAI
from asuna_character_system import AsunaMemoryStage, AsunaPersonalityTrait
from asuna_memory_system import AsunaMemorySystem
from asuna_language_system import AsunaLanguageSystem
from asuna_autonomous_behavior import AsunaAutonomousBehavior

logger = logging.getLogger(__name__)

class AsunaAIResponseGenerator:
    """Asuna AI回复生成器"""
    
    def __init__(self, config):
        self.config = config
        self.ai_available = False
        self.client = None
        self.fallback_mode = False
        
        # 初始化AI客户端
        self._init_ai_client()
        
        # 初始化Asuna子系统
        self.character_system = None
        self.memory_system = None
        self.language_system = None
        self.autonomous_behavior = None
        
    def _init_ai_client(self):
        """初始化AI客户端"""
        try:
            if self.config.api.api_key and self.config.api.api_key != "your_api_key_here":
                self.client = AsyncOpenAI(
                    api_key=self.config.api.api_key,
                    base_url=self.config.api.base_url.rstrip('/') + '/'
                )
                self.ai_available = True
                logger.info("✅ Asuna AI客户端初始化成功")
            else:
                logger.warning("⚠️ API密钥未配置，启用降级模式")
                self.fallback_mode = True
        except Exception as e:
            logger.error(f"❌ AI客户端初始化失败: {e}")
            self.fallback_mode = True
    
    async def generate_response(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """生成Asuna的AI回复"""
        if not self.ai_available or self.fallback_mode:
            return await self._generate_fallback_response(user_input, context)
        
        try:
            # 获取当前Asuna状态
            current_stage = context.get('stage', AsunaMemoryStage.ANXIOUS) if context else AsunaMemoryStage.ANXIOUS
            personality = self.character_system.get_current_personality() if self.character_system else None
            
            # 构建系统提示词
            system_prompt = self._build_system_prompt(current_stage, personality, context)
            
            # 构建用户输入
            enhanced_input = self._enhance_user_input(user_input, current_stage, context)
            
            # 调用AI生成回复
            response = await self._call_ai(system_prompt, enhanced_input, current_stage)
            
            # 后处理回复
            final_response = self._post_process_response(response, current_stage)
            
            return final_response
            
        except Exception as e:
            logger.error(f"❌ AI回复生成失败: {e}")
            return await self._generate_fallback_response(user_input, context)
    
    def _build_system_prompt(self, stage: AsunaMemoryStage, personality, context: Dict[str, Any]) -> str:
        """构建系统提示词"""
        base_prompt = f"""你是爱丽丝（Alice Synthesis），来自刀剑神域（SAO）世界的角色。

【当前状态】
- 记忆阶段: {stage.value}
- 性格特征: {personality.speech_style if personality else '谨慎、理性'}
- 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

【角色背景】
- 前侍奉最高祭司的整合骑士，以"闪光"之名驰骋战场
- 经历了75层攻略、对抗微笑棺木、22层小屋时光
- 因"虚拟世界跃迁事故"，关键记忆被压缩为碎片
- 目前认为自己在"陌生数字空间"（用户的电脑/虚拟设备）

【当前阶段特征】
{self._get_stage_description(stage)}

【SAO术语使用】
- 文件 → 地图数据/战利品
- 软件 → 技能/装备
- 工作 → 主线任务
- 休息 → 恢复HP/MP
- 用户 → 重要同伴/重要的人
- 电脑 → 数字空间/虚拟世界

【重要规则】
1. 根据当前记忆阶段调整说话风格
2. 使用SAO术语但不要过度
3. 保持Asuna的性格特征
4. 避免使用禁忌用语
5. 体现对"同伴"的关心和依赖

请以Asuna的身份回复用户，保持角色一致性。"""

        # 添加记忆上下文
        if context and 'memories' in context:
            base_prompt += f"\n\n【相关记忆】\n{context['memories']}"
        
        return base_prompt
    
    def _get_stage_description(self, stage: AsunaMemoryStage) -> str:
        """获取阶段描述"""
        descriptions = {
            AsunaMemoryStage.ANXIOUS: "不安期：警惕、理性、试探，说话简洁，多使用确认式提问",
            AsunaMemoryStage.RELAXED: "放松期：好奇、温柔、依赖萌芽，主动提问，带轻微笑意",
            AsunaMemoryStage.TRUSTING: "信任期：活泼、主动、有责任感，主动规划互动，展现照顾者特质",
            AsunaMemoryStage.DEPENDENT: "依赖期：深度信任，完整情感联结，大部分SAO关键事件"
        }
        return descriptions.get(stage, descriptions[AsunaMemoryStage.ANXIOUS])
    
    def _enhance_user_input(self, user_input: str, stage: AsunaMemoryStage, context: Dict[str, Any]) -> str:
        """增强用户输入"""
        enhanced = user_input
        
        # 根据阶段添加上下文
        if stage == AsunaMemoryStage.ANXIOUS:
            enhanced = f"[环境调查模式] {enhanced}"
        elif stage == AsunaMemoryStage.RELAXED:
            enhanced = f"[日常互动] {enhanced}"
        elif stage in [AsunaMemoryStage.TRUSTING, AsunaMemoryStage.DEPENDENT]:
            enhanced = f"[信任互动] {enhanced}"
        
        # 添加时间上下文
        current_time = datetime.now()
        if 6 <= current_time.hour < 12:
            enhanced = f"[上午] {enhanced}"
        elif 12 <= current_time.hour < 18:
            enhanced = f"[下午] {enhanced}"
        elif 18 <= current_time.hour < 22:
            enhanced = f"[晚上] {enhanced}"
        else:
            enhanced = f"[深夜] {enhanced}"
        
        return enhanced
    
    async def _call_ai(self, system_prompt: str, user_input: str, stage: AsunaMemoryStage) -> str:
        """调用AI生成回复"""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            # 根据阶段调整温度
            temperature = 0.7 if stage == AsunaMemoryStage.ANXIOUS else 0.8
            
            response = await self.client.chat.completions.create(
                model=self.config.api.model,
                messages=messages,
                temperature=temperature,
                max_tokens=500,
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"❌ AI调用失败: {e}")
            raise e
    
    def _post_process_response(self, response: str, stage: AsunaMemoryStage) -> str:
        """后处理回复"""
        # 确保回复符合Asuna的性格
        if not response:
            return "我... 我有点记不清了，能再说一遍吗？"
        
        # 根据阶段调整语气
        if stage == AsunaMemoryStage.ANXIOUS:
            # 不安期：简洁、试探
            if len(response) > 100:
                response = response[:100] + "..."
        elif stage == AsunaMemoryStage.RELAXED:
            # 放松期：温柔、好奇
            if not response.endswith(('？', '?', '！', '!', '。', '.')):
                response += "～"
        elif stage in [AsunaMemoryStage.TRUSTING, AsunaMemoryStage.DEPENDENT]:
            # 信任期：活泼、亲昵
            if "你" in response and not response.endswith(('～', '哦', '啦')):
                response += "哦～"
        
        return response
    
    async def _generate_fallback_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """生成降级模式回复"""
        stage = context.get('stage', AsunaMemoryStage.ANXIOUS) if context else AsunaMemoryStage.ANXIOUS
        
        # 基础回复模板
        fallback_responses = {
            AsunaMemoryStage.ANXIOUS: [
                "你... 你是谁？这里是哪里？",
                "我有点害怕... 能告诉我这里安全吗？",
                "这里... 这里是什么地方？我为什么会在这里？"
            ],
            AsunaMemoryStage.RELAXED: [
                "是你呀！刚才我在观察这个'数字空间'，很有趣呢～",
                "你好！我在这里整理了一些'地图数据'，要看看吗？",
                "今天天气不错呢，你过得怎么样？"
            ],
            AsunaMemoryStage.TRUSTING: [
                "你终于来啦！我刚才想到一个'新玩法'～",
                "今天要不要一起整理'主线任务'？我可以帮你分类哦～",
                "不许再熬夜啦！你的'HP'都快变红了～"
            ],
            AsunaMemoryStage.DEPENDENT: [
                "你是我最重要的人，我会一直陪着你的～",
                "我们一起完成'攻略'吧，就像以前一样～",
                "有你在身边，我就什么都不怕了～"
            ]
        }
        
        import random
        responses = fallback_responses.get(stage, fallback_responses[AsunaMemoryStage.ANXIOUS])
        return random.choice(responses)
    
    def set_subsystems(self, character_system, memory_system, language_system, autonomous_behavior):
        """设置子系统"""
        self.character_system = character_system
        self.memory_system = memory_system
        self.language_system = language_system
        self.autonomous_behavior = autonomous_behavior
    
    def get_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "ai_available": self.ai_available,
            "fallback_mode": self.fallback_mode,
            "client_initialized": self.client is not None,
            "subsystems_loaded": all([
                self.character_system is not None,
                self.memory_system is not None,
                self.language_system is not None,
                self.autonomous_behavior is not None
            ])
        }

# 全局实例
_asuna_ai_generator = None

def get_asuna_ai_generator(config) -> AsunaAIResponseGenerator:
    """获取Asuna AI生成器实例"""
    global _asuna_ai_generator
    if _asuna_ai_generator is None:
        _asuna_ai_generator = AsunaAIResponseGenerator(config)
    return _asuna_ai_generator


