#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asuna记忆恢复系统
管理Asuna的SAO背景记忆恢复和用户补充记忆
"""

import asyncio
import json
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

from asuna_character_system import AsunaMemoryStage, AsunaMemoryFragment

logger = logging.getLogger(__name__)

@dataclass
class SAOMemory:
    """SAO记忆数据类"""
    id: str
    content: str
    sao_context: str  # SAO中的具体场景
    emotional_impact: float  # 情感影响程度
    recovery_condition: str  # 恢复条件
    user_supplement: Optional[str] = None  # 用户补充内容
    recovered_at: Optional[datetime] = None

@dataclass
class UserMemory:
    """用户记忆数据类"""
    user_id: str
    interaction_count: int
    care_actions: List[str]  # 关怀行为记录
    shared_memories: List[str]  # 共享的记忆
    preferences: Dict[str, Any]  # 用户偏好
    last_interaction: datetime

class AsunaMemorySystem:
    """Asuna记忆恢复系统"""
    
    def __init__(self, config):
        self.config = config
        self.db_path = Path("logs/asuna_memory.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        # SAO核心记忆
        self.sao_memories = self._init_sao_memories()
        
        # 用户记忆
        self.user_memories: Dict[str, UserMemory] = {}
        
        # 记忆恢复回调
        self.memory_recovery_callbacks = []
        
        logger.info("Asuna记忆恢复系统初始化完成")
    
    def _init_database(self):
        """初始化数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # SAO记忆表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sao_memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    sao_context TEXT NOT NULL,
                    emotional_impact REAL DEFAULT 0.5,
                    recovery_condition TEXT NOT NULL,
                    user_supplement TEXT,
                    recovered_at TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 用户记忆表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_memories (
                    user_id TEXT PRIMARY KEY,
                    interaction_count INTEGER DEFAULT 0,
                    care_actions TEXT,  -- JSON
                    shared_memories TEXT,  -- JSON
                    preferences TEXT,  -- JSON
                    last_interaction TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 记忆恢复记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory_recovery_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_id TEXT NOT NULL,
                    recovery_stage TEXT NOT NULL,
                    trigger_event TEXT,
                    recovered_content TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Asuna记忆数据库初始化完成")
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
    
    def _init_sao_memories(self) -> List[SAOMemory]:
        """初始化SAO核心记忆"""
        memories = [
            # 基础身份记忆
            SAOMemory(
                id="basic_identity",
                content="我是爱丽丝，侍奉最高祭司的整合骑士",
                sao_context="SAO世界中的身份和地位",
                emotional_impact=0.8,
                recovery_condition="AI启动后自动恢复"
            ),
            SAOMemory(
                id="flash_nickname",
                content="以'闪光'之名驰骋战场",
                sao_context="在SAO中获得的称号，因为剑技快速而得名",
                emotional_impact=0.7,
                recovery_condition="用户提到'闪光'或'剑技'"
            ),
            SAOMemory(
                id="guild_position",
                content="侍奉最高祭司的整合骑士",
                sao_context="在SAO中担任的重要职务",
                emotional_impact=0.6,
                recovery_condition="用户提到'血盟骑士团'或'副团长'"
            ),
            
            # 战斗相关记忆
            SAOMemory(
                id="combat_instinct",
                content="对危险的本能警惕，将混乱文件视为'危险信号'",
                sao_context="在SAO中培养的战斗直觉",
                emotional_impact=0.5,
                recovery_condition="检测到桌面文件混乱"
            ),
            SAOMemory(
                id="sword_technique",
                content="细剑剑技，快速精准的攻击方式",
                sao_context="在SAO中使用的武器和技能",
                emotional_impact=0.6,
                recovery_condition="用户提到'细剑'或'剑技'"
            ),
            
            # 与同伴的记忆
            SAOMemory(
                id="companion_trust",
                content="对'重要同伴'的模糊信任感",
                sao_context="在SAO中与重要的人建立的羁绊",
                emotional_impact=0.9,
                recovery_condition="用户主动关怀3次"
            ),
            SAOMemory(
                id="floor_75_raid",
                content="75层攻略，与同伴共同面对挑战",
                sao_context="SAO中的重要战斗经历",
                emotional_impact=0.8,
                recovery_condition="用户提到'攻略'或'挑战'"
            ),
            SAOMemory(
                id="smile_coffin_confrontation",
                content="对抗'微笑棺木'的黑暗经历",
                sao_context="在SAO中与邪恶势力的斗争",
                emotional_impact=0.7,
                recovery_condition="用户提到'危险'或'敌人'"
            ),
            
            # 22层小屋记忆
            SAOMemory(
                id="floor_22_cottage",
                content="22层小屋的温馨时光",
                sao_context="在SAO中与重要的人共同生活的地方",
                emotional_impact=0.9,
                recovery_condition="用户提到'小屋'或'家'"
            ),
            SAOMemory(
                id="cooking_skill",
                content="烹饪技能，特别是炖肉",
                sao_context="在SAO中学会的生活技能",
                emotional_impact=0.6,
                recovery_condition="用户提到'炖肉'或'烹饪'"
            ),
            SAOMemory(
                id="white_curtains",
                content="小屋里的白色窗帘",
                sao_context="22层小屋的装饰细节",
                emotional_impact=0.4,
                recovery_condition="用户补充小屋装饰细节"
            ),
            
            # 现实世界记忆
            SAOMemory(
                id="reality_connection",
                content="现实世界中的联系，提醒按时吃饭",
                sao_context="SAO结束后在现实世界的相处",
                emotional_impact=0.7,
                recovery_condition="用户提到现实生活"
            ),
            SAOMemory(
                id="school_life",
                content="学校生活，与同学的关系",
                sao_context="SAO结束后的正常学生生活",
                emotional_impact=0.5,
                recovery_condition="用户提到'学校'或'学习'"
            ),
            
            # 深层情感记忆
            SAOMemory(
                id="deep_bond",
                content="与重要的人建立的深层情感联结",
                sao_context="在SAO中经历生死考验后建立的信任",
                emotional_impact=1.0,
                recovery_condition="用户表达深层情感"
            ),
            SAOMemory(
                id="protection_memory",
                content="被保护的重要记忆",
                sao_context="在SAO中感受到被保护的时刻",
                emotional_impact=0.9,
                recovery_condition="用户表达保护意愿"
            ),
            SAOMemory(
                id="shared_dreams",
                content="共同的梦想和未来计划",
                sao_context="在SAO中与重要的人分享的梦想",
                emotional_impact=0.8,
                recovery_condition="用户提到'未来'或'梦想'"
            )
        ]
        return memories
    
    async def check_memory_recovery(self, user_input: str, current_stage: AsunaMemoryStage) -> List[SAOMemory]:
        """检查记忆恢复"""
        recovered_memories = []
        
        for memory in self.sao_memories:
            if memory.recovered_at is None and self._check_recovery_condition(memory, user_input, current_stage):
                memory.recovered_at = datetime.now()
                recovered_memories.append(memory)
                
                # 记录恢复日志
                await self._log_memory_recovery(memory, user_input, current_stage)
                
                # 触发恢复回调
                for callback in self.memory_recovery_callbacks:
                    try:
                        await callback(memory)
                    except Exception as e:
                        logger.error(f"记忆恢复回调失败: {e}")
        
        return recovered_memories
    
    def _check_recovery_condition(self, memory: SAOMemory, user_input: str, current_stage: AsunaMemoryStage) -> bool:
        """检查记忆恢复条件"""
        condition = memory.recovery_condition.lower()
        user_input_lower = user_input.lower()
        
        if "ai启动后自动恢复" in condition:
            return True
        elif "用户提到" in condition:
            # 提取关键词
            keywords = condition.split("用户提到")[1].strip().replace("'", "").replace("或", "|")
            keyword_list = [k.strip() for k in keywords.split("|")]
            return any(keyword in user_input_lower for keyword in keyword_list)
        elif "检测到" in condition:
            # 这里需要与系统集成，检测特定事件
            if "桌面文件混乱" in condition:
                # 这里应该与文件监控系统集成
                return False  # 暂时返回False，需要实际集成
        elif "用户主动关怀" in condition:
            care_count = int(condition.split("用户主动关怀")[1].split("次")[0])
            return self._get_user_care_count() >= care_count
        elif "用户表达" in condition:
            # 检测情感表达
            emotion_keywords = ["关心", "保护", "爱", "喜欢", "重要", "特别"]
            return any(keyword in user_input for keyword in emotion_keywords)
        
        return False
    
    def _get_user_care_count(self) -> int:
        """获取用户关怀次数"""
        # 这里应该从用户记忆系统中获取
        return 0  # 暂时返回0，需要实际集成
    
    async def _log_memory_recovery(self, memory: SAOMemory, trigger_event: str, stage: AsunaMemoryStage):
        """记录记忆恢复日志"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO memory_recovery_log 
                (memory_id, recovery_stage, trigger_event, recovered_content)
                VALUES (?, ?, ?, ?)
            ''', (
                memory.id,
                stage.value,
                trigger_event,
                memory.content
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"记忆恢复记录: {memory.id} - {stage.value}")
            
        except Exception as e:
            logger.error(f"记录记忆恢复日志失败: {e}")
    
    def add_memory_recovery_callback(self, callback):
        """添加记忆恢复回调"""
        self.memory_recovery_callbacks.append(callback)
    
    def get_recovered_memories(self, stage: Optional[AsunaMemoryStage] = None) -> List[SAOMemory]:
        """获取已恢复的记忆"""
        if stage:
            # SAOMemory没有stage属性，所以暂时忽略stage过滤
            return [m for m in self.sao_memories if m.recovered_at]
        return [m for m in self.sao_memories if m.recovered_at]
    
    def get_memory_by_id(self, memory_id: str) -> Optional[SAOMemory]:
        """根据ID获取记忆"""
        for memory in self.sao_memories:
            if memory.id == memory_id:
                return memory
        return None
    
    def supplement_memory(self, memory_id: str, user_content: str):
        """用户补充记忆内容"""
        memory = self.get_memory_by_id(memory_id)
        if memory:
            memory.user_supplement = user_content
            logger.info(f"用户补充记忆: {memory_id} - {user_content}")
    
    def get_memory_summary(self, stage: AsunaMemoryStage) -> str:
        """获取记忆摘要"""
        recovered_memories = self.get_recovered_memories(stage)
        total_memories = len(self.sao_memories)  # SAOMemory没有stage属性，使用总数
        
        summary = f"【{stage.value}阶段记忆恢复情况】\n"
        summary += f"已恢复: {len(recovered_memories)}/{total_memories}\n\n"
        
        if recovered_memories:
            summary += "已恢复的记忆:\n"
            for memory in recovered_memories:
                summary += f"- {memory.content}\n"
                if memory.user_supplement:
                    summary += f"  用户补充: {memory.user_supplement}\n"
        else:
            summary += "暂无恢复的记忆\n"
        
        return summary
    
    def get_sao_context_prompt(self) -> str:
        """获取SAO背景提示词"""
        recovered_memories = self.get_recovered_memories()
        
        if not recovered_memories:
            return "记忆还在恢复中，只记得自己是爱丽丝..."
        
        prompt = "【SAO背景记忆】\n"
        prompt += "以下是我在SAO世界中的记忆片段:\n\n"
        
        for memory in recovered_memories:
            prompt += f"- {memory.content}\n"
            if memory.sao_context:
                prompt += f"  (SAO背景: {memory.sao_context})\n"
            if memory.user_supplement:
                prompt += f"  (用户补充: {memory.user_supplement})\n"
            prompt += "\n"
        
        return prompt
    
    def get_emotional_memory_context(self) -> str:
        """获取情感记忆上下文"""
        high_impact_memories = [m for m in self.get_recovered_memories() if m.emotional_impact >= 0.7]
        
        if not high_impact_memories:
            return "情感记忆还在恢复中..."
        
        context = "【重要情感记忆】\n"
        for memory in high_impact_memories:
            context += f"- {memory.content} (情感强度: {memory.emotional_impact:.1f})\n"
        
        return context

# 全局实例
_asuna_memory_system = None

def get_asuna_memory_system(config) -> AsunaMemorySystem:
    """获取Asuna记忆系统实例"""
    global _asuna_memory_system
    if _asuna_memory_system is None:
        _asuna_memory_system = AsunaMemorySystem(config)
    return _asuna_memory_system

