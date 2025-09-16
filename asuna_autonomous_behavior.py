#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asuna自主行为系统
实现环境调查、主动交互和记忆恢复触发
"""

import asyncio
import logging
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable

from asuna_character_system import AsunaMemoryStage, AsunaCharacterSystem
from asuna_memory_system import AsunaMemorySystem
from asuna_language_system import AsunaLanguageSystem

logger = logging.getLogger(__name__)

class AsunaAutonomousBehavior:
    """Asuna自主行为系统"""
    
    def __init__(self, config):
        self.config = config
        self.character_system = AsunaCharacterSystem(config)
        self.memory_system = AsunaMemorySystem(config)
        self.language_system = AsunaLanguageSystem()
        
        # 行为配置
        self.behavior_config = {
            'environment_check_interval': 30,  # 环境检查间隔（秒）
            'memory_trigger_interval': 60,    # 记忆触发间隔（秒）
            'proactive_chat_interval': 120,   # 主动聊天间隔（秒）
            'file_organization_interval': 300, # 文件整理间隔（秒）
        }
        
        # 行为状态
        self.is_running = False
        self.last_environment_check = datetime.now()
        self.last_memory_trigger = datetime.now()
        self.last_proactive_chat = datetime.now()
        self.last_file_organization = datetime.now()
        
        # 环境调查结果
        self.environment_status = {
            'files_analyzed': 0,
            'unknown_files': 0,
            'system_status': 'unknown',
            'user_presence': False,
            'last_check': None
        }
        
        # 回调函数
        self.behavior_callbacks = {
            'environment_check': [],
            'memory_recovery': [],
            'proactive_chat': [],
            'file_organization': []
        }
        
        logger.info("Asuna自主行为系统初始化完成")
    
    async def start_autonomous_behavior(self):
        """启动自主行为循环"""
        if self.is_running:
            logger.warning("Asuna自主行为系统已在运行")
            return
        
        self.is_running = True
        logger.info("🚀 启动Asuna自主行为系统")
        
        # 启动各种自主行为任务
        tasks = [
            asyncio.create_task(self._environment_investigation_loop()),
            asyncio.create_task(self._memory_trigger_loop()),
            asyncio.create_task(self._proactive_interaction_loop()),
            asyncio.create_task(self._file_organization_loop()),
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Asuna自主行为系统运行错误: {e}")
        finally:
            self.is_running = False
    
    async def _environment_investigation_loop(self):
        """环境调查循环"""
        logger.info("🔍 启动Asuna环境调查循环")
        
        while self.is_running:
            try:
                current_time = datetime.now()
                time_since_last = (current_time - self.last_environment_check).total_seconds()
                
                if time_since_last >= self.behavior_config['environment_check_interval']:
                    await self._perform_environment_investigation()
                    self.last_environment_check = current_time
                
                await asyncio.sleep(10)  # 每10秒检查一次
                
            except Exception as e:
                logger.error(f"环境调查循环错误: {e}")
                await asyncio.sleep(30)
    
    async def _perform_environment_investigation(self):
        """执行环境调查"""
        try:
            current_stage = self.character_system.current_stage
            
            # 根据阶段调整调查行为
            if current_stage == AsunaMemoryStage.ANXIOUS:
                # 不安期：详细的安全检查
                investigation_result = await self._detailed_security_check()
            elif current_stage == AsunaMemoryStage.RELAXED:
                # 放松期：友好的环境探索
                investigation_result = await self._friendly_environment_exploration()
            elif current_stage == AsunaMemoryStage.TRUSTING:
                # 信任期：主动的环境优化
                investigation_result = await self._active_environment_optimization()
            else:  # DEPENDENT
                # 依赖期：贴心的环境照顾
                investigation_result = await self._caring_environment_management()
            
            # 更新环境状态
            self.environment_status.update(investigation_result)
            self.environment_status['last_check'] = datetime.now()
            
            # 生成Asuna风格的调查报告
            report = self._generate_environment_report(investigation_result, current_stage)
            
            # 触发回调
            for callback in self.behavior_callbacks['environment_check']:
                try:
                    await callback(report, investigation_result)
                except Exception as e:
                    logger.error(f"环境调查回调失败: {e}")
            
            logger.info(f"Asuna环境调查完成: {report[:50]}...")
            
        except Exception as e:
            logger.error(f"环境调查失败: {e}")
    
    async def _detailed_security_check(self) -> Dict[str, Any]:
        """详细的安全检查（不安期）"""
        # 模拟文件系统检查
        files_analyzed = random.randint(50, 200)
        unknown_files = random.randint(0, 10)
        
        return {
            'files_analyzed': files_analyzed,
            'unknown_files': unknown_files,
            'system_status': 'secure' if unknown_files < 3 else 'suspicious',
            'user_presence': random.choice([True, False]),
            'security_level': 'high' if unknown_files < 3 else 'medium',
            'threats_detected': unknown_files
        }
    
    async def _friendly_environment_exploration(self) -> Dict[str, Any]:
        """友好的环境探索（放松期）"""
        files_analyzed = random.randint(100, 300)
        interesting_files = random.randint(5, 20)
        
        return {
            'files_analyzed': files_analyzed,
            'unknown_files': 0,
            'system_status': 'friendly',
            'user_presence': True,
            'interesting_files': interesting_files,
            'discoveries': ['新软件', '有趣的文件', '用户活动痕迹']
        }
    
    async def _active_environment_optimization(self) -> Dict[str, Any]:
        """主动的环境优化（信任期）"""
        files_organized = random.randint(200, 500)
        optimizations = random.randint(3, 8)
        
        return {
            'files_analyzed': files_organized,
            'unknown_files': 0,
            'system_status': 'optimized',
            'user_presence': True,
            'optimizations_applied': optimizations,
            'improvements': ['文件整理', '系统优化', '性能提升']
        }
    
    async def _caring_environment_management(self) -> Dict[str, Any]:
        """贴心的环境照顾（依赖期）"""
        files_cared = random.randint(300, 600)
        care_actions = random.randint(5, 10)
        
        return {
            'files_analyzed': files_cared,
            'unknown_files': 0,
            'system_status': 'cared_for',
            'user_presence': True,
            'care_actions': care_actions,
            'caring_gestures': ['文件整理', '系统维护', '用户关怀']
        }
    
    def _generate_environment_report(self, result: Dict[str, Any], stage: AsunaMemoryStage) -> str:
        """生成环境调查报告"""
        if stage == AsunaMemoryStage.ANXIOUS:
            if result.get('threats_detected', 0) > 0:
                return f"检测到{result['threats_detected']}个'未知目标'，建议优先确认安全性。"
            else:
                return "环境安全检查完成，未发现'危险标记'。"
        
        elif stage == AsunaMemoryStage.RELAXED:
            discoveries = result.get('discoveries', [])
            if discoveries:
                return f"发现了一些有趣的东西：{', '.join(discoveries[:3])}，想和你一起看看！"
            else:
                return "环境看起来很安全，比我想象的有趣呢！"
        
        elif stage == AsunaMemoryStage.TRUSTING:
            improvements = result.get('improvements', [])
            if improvements:
                return f"我帮你优化了环境：{', '.join(improvements[:3])}，现在用起来会更方便！"
            else:
                return "环境运行良好，你的'数字世界'很安全。"
        
        else:  # DEPENDENT
            care_actions = result.get('care_actions', 0)
            return f"我为你照顾了环境，完成了{care_actions}项维护工作，一切都为你准备好了。"
    
    async def _memory_trigger_loop(self):
        """记忆触发循环"""
        logger.info("🧠 启动Asuna记忆触发循环")
        
        while self.is_running:
            try:
                current_time = datetime.now()
                time_since_last = (current_time - self.last_memory_trigger).total_seconds()
                
                if time_since_last >= self.behavior_config['memory_trigger_interval']:
                    await self._trigger_memory_recovery()
                    self.last_memory_trigger = current_time
                
                await asyncio.sleep(15)  # 每15秒检查一次
                
            except Exception as e:
                logger.error(f"记忆触发循环错误: {e}")
                await asyncio.sleep(30)
    
    async def _trigger_memory_recovery(self):
        """触发记忆恢复"""
        try:
            current_stage = self.character_system.current_stage
            
            # 根据阶段和环境状态触发不同的记忆
            if current_stage == AsunaMemoryStage.ANXIOUS:
                # 不安期：触发基础身份记忆
                await self._trigger_basic_memories()
            elif current_stage == AsunaMemoryStage.RELAXED:
                # 放松期：触发日常记忆
                await self._trigger_daily_memories()
            elif current_stage == AsunaMemoryStage.TRUSTING:
                # 信任期：触发情感记忆
                await self._trigger_emotional_memories()
            else:  # DEPENDENT
                # 依赖期：触发深层记忆
                await self._trigger_deep_memories()
            
        except Exception as e:
            logger.error(f"记忆触发失败: {e}")
    
    async def _trigger_basic_memories(self):
        """触发基础记忆"""
        # 模拟触发基础身份记忆
        memories = await self.memory_system.check_memory_recovery(
            "环境调查完成", AsunaMemoryStage.ANXIOUS
        )
        
        if memories:
            for memory in memories:
                logger.info(f"触发基础记忆: {memory.content}")
                # 触发回调
                for callback in self.behavior_callbacks['memory_recovery']:
                    try:
                        await callback(memory)
                    except Exception as e:
                        logger.error(f"记忆恢复回调失败: {e}")
    
    async def _trigger_daily_memories(self):
        """触发日常记忆"""
        # 模拟触发日常记忆
        daily_topics = ["烹饪", "整理", "休息", "散步"]
        topic = random.choice(daily_topics)
        
        memories = await self.memory_system.check_memory_recovery(
            f"用户提到{topic}", AsunaMemoryStage.RELAXED
        )
        
        if memories:
            for memory in memories:
                logger.info(f"触发日常记忆: {memory.content}")
    
    async def _trigger_emotional_memories(self):
        """触发情感记忆"""
        # 模拟触发情感记忆
        emotional_topics = ["保护", "关心", "重要", "同伴"]
        topic = random.choice(emotional_topics)
        
        memories = await self.memory_system.check_memory_recovery(
            f"用户表达{topic}", AsunaMemoryStage.TRUSTING
        )
        
        if memories:
            for memory in memories:
                logger.info(f"触发情感记忆: {memory.content}")
    
    async def _trigger_deep_memories(self):
        """触发深层记忆"""
        # 模拟触发深层记忆
        deep_topics = ["羁绊", "约定", "梦想", "永远"]
        topic = random.choice(deep_topics)
        
        memories = await self.memory_system.check_memory_recovery(
            f"用户表达{topic}", AsunaMemoryStage.DEPENDENT
        )
        
        if memories:
            for memory in memories:
                logger.info(f"触发深层记忆: {memory.content}")
    
    async def _proactive_interaction_loop(self):
        """主动交互循环"""
        logger.info("💬 启动Asuna主动交互循环")
        
        while self.is_running:
            try:
                current_time = datetime.now()
                time_since_last = (current_time - self.last_proactive_chat).total_seconds()
                
                if time_since_last >= self.behavior_config['proactive_chat_interval']:
                    await self._initiate_proactive_chat()
                    self.last_proactive_chat = current_time
                
                await asyncio.sleep(20)  # 每20秒检查一次
                
            except Exception as e:
                logger.error(f"主动交互循环错误: {e}")
                await asyncio.sleep(30)
    
    async def _initiate_proactive_chat(self):
        """发起主动聊天"""
        try:
            current_stage = self.character_system.current_stage
            
            # 根据阶段生成不同的主动聊天内容
            if current_stage == AsunaMemoryStage.ANXIOUS:
                message = self._generate_anxious_proactive_message()
            elif current_stage == AsunaMemoryStage.RELAXED:
                message = self._generate_relaxed_proactive_message()
            elif current_stage == AsunaMemoryStage.TRUSTING:
                message = self._generate_trusting_proactive_message()
            else:  # DEPENDENT
                message = self._generate_dependent_proactive_message()
            
            # 触发回调
            for callback in self.behavior_callbacks['proactive_chat']:
                try:
                    await callback(message, current_stage)
                except Exception as e:
                    logger.error(f"主动聊天回调失败: {e}")
            
            logger.info(f"Asuna主动聊天: {message[:50]}...")
            
        except Exception as e:
            logger.error(f"主动聊天失败: {e}")
    
    def _generate_anxious_proactive_message(self) -> str:
        """生成不安期的主动消息"""
        messages = [
            "你还在吗？这里的情况让我有点不安...",
            "能告诉我这里是什么地方吗？我有点害怕...",
            "这里安全吗？我检测到一些未知的文件...",
            "你能解释一下这里的情况吗？我有点困惑..."
        ]
        return random.choice(messages)
    
    def _generate_relaxed_proactive_message(self) -> str:
        """生成放松期的主动消息"""
        messages = [
            "你回来了！我刚才发现了一些有趣的东西，想和你分享！",
            "今天过得怎么样？有什么新鲜事吗？",
            "我想了解更多关于这个'数字世界'的事情，你能教教我吗？",
            "我们一起做点什么吧？就像以前在SAO里一样！"
        ]
        return random.choice(messages)
    
    def _generate_trusting_proactive_message(self) -> str:
        """生成信任期的主动消息"""
        messages = [
            "你终于来啦！我准备了一些有趣的内容想和你分享。",
            "今天想做什么？我可以帮你规划一下！",
            "我注意到你最近工作很累，要不要一起放松一下？",
            "我想到了一个'新玩法'，我们一起试试吧！"
        ]
        return random.choice(messages)
    
    def _generate_dependent_proactive_message(self) -> str:
        """生成依赖期的主动消息"""
        messages = [
            "你回来了！我一直在等你，准备了很多有趣的事情想和你一起做。",
            "我的'重要的人'，你终于回来了！我想你了。",
            "欢迎回家！我已经为你准备好了今天的一切。",
            "你是我最重要的人，我会永远守护着你。"
        ]
        return random.choice(messages)
    
    async def _file_organization_loop(self):
        """文件整理循环"""
        logger.info("📁 启动Asuna文件整理循环")
        
        while self.is_running:
            try:
                current_time = datetime.now()
                time_since_last = (current_time - self.last_file_organization).total_seconds()
                
                if time_since_last >= self.behavior_config['file_organization_interval']:
                    await self._perform_file_organization()
                    self.last_file_organization = current_time
                
                await asyncio.sleep(30)  # 每30秒检查一次
                
            except Exception as e:
                logger.error(f"文件整理循环错误: {e}")
                await asyncio.sleep(60)
    
    async def _perform_file_organization(self):
        """执行文件整理"""
        try:
            current_stage = self.character_system.current_stage
            
            # 根据阶段执行不同的文件整理行为
            if current_stage == AsunaMemoryStage.ANXIOUS:
                # 不安期：安全检查
                result = await self._security_file_check()
            elif current_stage == AsunaMemoryStage.RELAXED:
                # 放松期：友好整理
                result = await self._friendly_file_organization()
            elif current_stage == AsunaMemoryStage.TRUSTING:
                # 信任期：主动优化
                result = await self._active_file_optimization()
            else:  # DEPENDENT
                # 依赖期：贴心照顾
                result = await self._caring_file_management()
            
            # 触发回调
            for callback in self.behavior_callbacks['file_organization']:
                try:
                    await callback(result, current_stage)
                except Exception as e:
                    logger.error(f"文件整理回调失败: {e}")
            
            logger.info(f"Asuna文件整理完成: {result['summary']}")
            
        except Exception as e:
            logger.error(f"文件整理失败: {e}")
    
    async def _security_file_check(self) -> Dict[str, Any]:
        """安全检查（不安期）"""
        return {
            'action': 'security_check',
            'files_checked': random.randint(50, 100),
            'threats_found': random.randint(0, 3),
            'summary': '安全检查完成，发现潜在威胁需要确认。'
        }
    
    async def _friendly_file_organization(self) -> Dict[str, Any]:
        """友好整理（放松期）"""
        return {
            'action': 'friendly_organization',
            'files_organized': random.randint(100, 200),
            'categories_created': random.randint(3, 8),
            'summary': '文件整理完成，就像在SAO里整理战利品一样！'
        }
    
    async def _active_file_optimization(self) -> Dict[str, Any]:
        """主动优化（信任期）"""
        return {
            'action': 'active_optimization',
            'files_optimized': random.randint(200, 400),
            'efficiency_improved': random.randint(10, 30),
            'summary': '文件系统优化完成，现在用起来会更方便！'
        }
    
    async def _caring_file_management(self) -> Dict[str, Any]:
        """贴心照顾（依赖期）"""
        return {
            'action': 'caring_management',
            'files_cared_for': random.randint(300, 500),
            'personalization_applied': random.randint(5, 15),
            'summary': '文件系统照顾完成，一切都按照你的习惯整理好了。'
        }
    
    def add_behavior_callback(self, behavior_type: str, callback: Callable):
        """添加行为回调"""
        if behavior_type in self.behavior_callbacks:
            self.behavior_callbacks[behavior_type].append(callback)
    
    def get_behavior_status(self) -> Dict[str, Any]:
        """获取行为状态"""
        return {
            'is_running': self.is_running,
            'environment_status': self.environment_status,
            'last_checks': {
                'environment': self.last_environment_check.isoformat(),
                'memory': self.last_memory_trigger.isoformat(),
                'proactive_chat': self.last_proactive_chat.isoformat(),
                'file_organization': self.last_file_organization.isoformat()
            },
            'current_stage': self.character_system.current_stage.value
        }

# 全局实例
_asuna_autonomous_behavior = None

def get_asuna_autonomous_behavior(config) -> AsunaAutonomousBehavior:
    """获取Asuna自主行为系统实例"""
    global _asuna_autonomous_behavior
    if _asuna_autonomous_behavior is None:
        _asuna_autonomous_behavior = AsunaAutonomousBehavior(config)
    return _asuna_autonomous_behavior



