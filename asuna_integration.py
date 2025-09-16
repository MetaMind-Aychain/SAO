#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asuna集成模块
将Asuna角色系统优雅集成到现有AI架构中
"""

import asyncio
import logging
from typing import Dict, Any, Optional

from config import config
from asuna_character_system import AsunaCharacterSystem, get_asuna_system
from asuna_memory_system import AsunaMemorySystem, get_asuna_memory_system
from asuna_language_system import AsunaLanguageSystem, get_asuna_language_system
from asuna_autonomous_behavior import AsunaAutonomousBehavior, get_asuna_autonomous_behavior
from asuna_ai_integration import AsunaAIResponseGenerator, get_asuna_ai_generator
from asuna_emotion_integration import AsunaEmotionIntegration, get_asuna_emotion_integration
from asuna_autonomous_enhanced import AsunaAutonomousEnhanced, get_asuna_autonomous_enhanced

logger = logging.getLogger(__name__)

class AsunaIntegration:
    """Asuna集成管理器"""
    
    def __init__(self):
        self.config = config
        self.is_initialized = False
        
        # Asuna系统组件
        self.character_system: Optional[AsunaCharacterSystem] = None
        self.memory_system: Optional[AsunaMemorySystem] = None
        self.language_system: Optional[AsunaLanguageSystem] = None
        self.autonomous_behavior: Optional[AsunaAutonomousBehavior] = None
        self.ai_generator: Optional[AsunaAIResponseGenerator] = None
        self.emotion_integration: Optional[AsunaEmotionIntegration] = None
        self.autonomous_enhanced: Optional[AsunaAutonomousEnhanced] = None
        
        # 集成状态
        self.integration_status = {
            'character_system': False,
            'memory_system': False,
            'language_system': False,
            'autonomous_behavior': False,
            'ai_generator': False,
            'emotion_integration': False,
            'autonomous_enhanced': False
        }
        
        logger.info("Asuna集成模块初始化完成")
    
    async def initialize_asuna_systems(self):
        """初始化Asuna系统"""
        if self.is_initialized:
            logger.warning("Asuna系统已经初始化")
            return
        
        try:
            # 检查是否启用Asuna
            if not self.config.emotional_ai.asuna_enabled:
                logger.info("Asuna角色系统未启用")
                return
            
            logger.info("🚀 开始初始化Asuna角色系统...")
            
            # 初始化角色系统
            self.character_system = get_asuna_system(self.config)
            self.integration_status['character_system'] = True
            logger.info("✅ Asuna角色系统初始化完成")
            
            # 初始化记忆系统
            self.memory_system = get_asuna_memory_system(self.config)
            self.integration_status['memory_system'] = True
            logger.info("✅ Asuna记忆系统初始化完成")
            
            # 初始化用语系统
            self.language_system = get_asuna_language_system()
            self.integration_status['language_system'] = True
            logger.info("✅ Asuna用语系统初始化完成")
            
            # 初始化自主行为系统
            if self.config.emotional_ai.asuna_autonomous_behavior:
                self.autonomous_behavior = get_asuna_autonomous_behavior(self.config)
                self.integration_status['autonomous_behavior'] = True
                logger.info("✅ Asuna自主行为系统初始化完成")
            
            # 初始化AI生成器
            self.ai_generator = get_asuna_ai_generator(self.config)
            self.ai_generator.set_subsystems(
                self.character_system,
                self.memory_system,
                self.language_system,
                self.autonomous_behavior
            )
            self.integration_status['ai_generator'] = True
            logger.info("✅ Asuna AI生成器初始化完成")
            
            # 初始化情感集成
            self.emotion_integration = get_asuna_emotion_integration(self.config)
            self.integration_status['emotion_integration'] = True
            logger.info("✅ Asuna情感集成初始化完成")
            
            # 初始化增强自主行为
            self.autonomous_enhanced = get_asuna_autonomous_enhanced(self.config)
            self.integration_status['autonomous_enhanced'] = True
            logger.info("✅ Asuna增强自主行为初始化完成")
            
            self.is_initialized = True
            logger.info("🎉 Asuna角色系统集成完成！")
            
        except Exception as e:
            logger.error(f"Asuna系统初始化失败: {e}")
            raise
    
    async def process_user_interaction(self, user_input: str, base_response: str = "") -> Dict[str, Any]:
        """处理用户交互"""
        if not self.is_initialized:
            return {"asuna_response": base_response, "stage": "not_initialized"}
        
        try:
            # 角色系统处理
            character_result = self.character_system.process_interaction(user_input, base_response)
            
            # 记忆系统检查
            memory_recovered = []
            if self.memory_system:
                current_stage = self.character_system.current_stage
                memory_recovered = await self.memory_system.check_memory_recovery(user_input, current_stage)
            
            # 使用AI生成器生成真实回复
            asuna_response = base_response
            if self.ai_generator:
                # 构建上下文
                context = {
                    'stage': self.character_system.current_stage,
                    'personality': self.character_system.get_current_personality(),
                    'memories': [m.content for m in memory_recovered],
                    'interaction_count': character_result["interaction_count"],
                    'care_count': character_result["care_count"]
                }
                
                # 生成AI回复
                asuna_response = await self.ai_generator.generate_response(user_input, context)
                
                # 情感增强处理
                if self.emotion_integration:
                    asuna_response = await self.emotion_integration.generate_emotion_enhanced_response(
                        user_input, asuna_response, context
                    )
            elif self.language_system:
                # 降级到语言系统
                current_stage = self.character_system.current_stage
                asuna_response = self.language_system.generate_response(
                    user_input, base_response, current_stage
                )
            
            # 返回结果
            result = {
                "asuna_response": asuna_response,
                "stage": character_result["stage"],
                "interaction_count": character_result["interaction_count"],
                "care_count": character_result["care_count"],
                "tasks_completed": character_result["tasks_completed"],
                "unlocked_memories": character_result["unlocked_memories"],
                "memory_recovered": [m.id for m in memory_recovered],
                "sao_elements_used": self.config.emotional_ai.asuna_sao_elements,
                "ai_mode": "real" if self.ai_generator and self.ai_generator.ai_available else "fallback"
            }
            
            return result
            
        except Exception as e:
            logger.error(f"处理用户交互失败: {e}")
            return {"asuna_response": base_response, "error": str(e)}
    
    def get_asuna_system_prompt(self) -> str:
        """获取Asuna系统提示词"""
        if not self.is_initialized or not self.character_system:
            return "Asuna系统未初始化"
        
        try:
            # 获取角色系统提示词
            character_prompt = self.character_system.get_sao_style_prompt()
            
            # 获取记忆系统上下文
            memory_context = ""
            if self.memory_system:
                memory_context = self.memory_system.get_sao_context_prompt()
            
            # 获取用语系统提示词
            language_prompt = ""
            if self.language_system:
                current_stage = self.character_system.current_stage
                language_prompt = self.language_system.get_sao_style_prompt(current_stage)
            
            # 组合提示词
            full_prompt = f"{character_prompt}\n\n{memory_context}\n\n{language_prompt}"
            
            return full_prompt
            
        except Exception as e:
            logger.error(f"获取Asuna系统提示词失败: {e}")
            return "Asuna系统提示词生成失败"
    
    def get_asuna_status(self) -> Dict[str, Any]:
        """获取Asuna状态"""
        if not self.is_initialized:
            return {"status": "not_initialized"}
        
        try:
            status = {
                "status": "initialized",
                "integration_status": self.integration_status,
                "character_info": {},
                "memory_info": {},
                "behavior_info": {}
            }
            
            # 角色信息
            if self.character_system:
                status["character_info"] = {
                    "current_stage": self.character_system.current_stage.value,
                    "interaction_count": self.character_system.interaction_count,
                    "care_count": self.character_system.user_care_count,
                    "tasks_completed": self.character_system.virtual_tasks_completed,
                    "personality": self.character_system.get_current_personality().__dict__
                }
            
            # 记忆信息
            if self.memory_system:
                current_stage = self.character_system.current_stage if self.character_system else None
                status["memory_info"] = {
                    "total_memories": len(self.memory_system.sao_memories),
                    "recovered_memories": len(self.memory_system.get_recovered_memories()),
                    "stage_memories": len(self.memory_system.get_recovered_memories(current_stage)) if current_stage else 0,
                    "memory_summary": self.memory_system.get_memory_summary(current_stage) if current_stage else "No stage info"
                }
            
            # 行为信息
            if self.autonomous_behavior:
                status["behavior_info"] = self.autonomous_behavior.get_behavior_status()
            
            # AI生成器信息
            if self.ai_generator:
                status["ai_generator_info"] = self.ai_generator.get_status()
            
            return status
            
        except Exception as e:
            logger.error(f"获取Asuna状态失败: {e}")
            return {"status": "error", "error": str(e)}
    
    async def start_asuna_autonomous_behavior(self):
        """启动Asuna自主行为"""
        if not self.is_initialized or not self.autonomous_behavior:
            logger.warning("Asuna自主行为系统未初始化")
            return
        
        try:
            await self.autonomous_behavior.start_autonomous_behavior()
        except Exception as e:
            logger.error(f"启动Asuna自主行为失败: {e}")
    
    def supplement_memory(self, memory_id: str, user_content: str):
        """用户补充记忆"""
        if not self.is_initialized:
            logger.warning("Asuna系统未初始化")
            return
        
        try:
            if self.character_system:
                self.character_system.supplement_memory(memory_id, user_content)
            
            if self.memory_system:
                self.memory_system.supplement_memory(memory_id, user_content)
            
            logger.info(f"用户补充记忆: {memory_id} - {user_content}")
            
        except Exception as e:
            logger.error(f"补充记忆失败: {e}")
    
    def get_memory_fragments(self) -> list:
        """获取记忆碎片列表"""
        if not self.is_initialized or not self.character_system:
            return []
        
        try:
            fragments = []
            for fragment in self.character_system.memory_fragments:
                fragments.append({
                    "id": fragment.id,
                    "stage": fragment.stage.value if hasattr(fragment, 'stage') else 'unknown',
                    "content": fragment.content,
                    "trigger_condition": fragment.trigger_condition,
                    "unlocked": fragment.unlocked,
                    "user_supplement_needed": fragment.user_supplement_needed
                })
            return fragments
        except Exception as e:
            logger.error(f"获取记忆碎片失败: {e}")
            return []
    
    def get_sao_elements(self) -> Dict[str, str]:
        """获取SAO元素"""
        if not self.is_initialized or not self.character_system:
            return {}
        
        try:
            return self.character_system.sao_elements
        except Exception as e:
            logger.error(f"获取SAO元素失败: {e}")
            return {}

# 全局实例
_asuna_integration = None

def get_asuna_integration() -> AsunaIntegration:
    """获取Asuna集成实例"""
    global _asuna_integration
    if _asuna_integration is None:
        _asuna_integration = AsunaIntegration()
    return _asuna_integration

async def initialize_asuna_systems():
    """初始化Asuna系统（便捷函数）"""
    integration = get_asuna_integration()
    await integration.initialize_asuna_systems()
    return integration

