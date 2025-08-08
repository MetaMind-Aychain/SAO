#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级AI功能集成
整合所有高级系统到情绪AI核心
"""

import asyncio
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class AdvancedAISystem:
    """高级AI系统集成"""
    
    def __init__(self, emotion_core, memory_system):
        self.emotion_core = emotion_core
        self.memory_system = memory_system
        
        # 初始化各个高级系统
        self.systems = {}
        self._initialize_systems()
        
        logger.info("高级AI系统集成初始化完成")
    
    def _initialize_systems(self):
        """初始化所有子系统"""
        
        # 1. 高级感知系统
        try:
            from advanced_perception_system import get_advanced_perception
            self.systems['perception'] = get_advanced_perception(self.emotion_core)
            logger.info("✅ 高级感知系统已加载")
        except Exception as e:
            logger.error(f"高级感知系统加载失败: {e}")
            self.systems['perception'] = None
        
        # 2. LLM反思系统
        try:
            from llm_reflection_system import LLMReflectionSystem
            self.systems['reflection'] = LLMReflectionSystem(self.memory_system, self.emotion_core)
            logger.info("✅ LLM反思系统已加载")
        except Exception as e:
            logger.error(f"LLM反思系统加载失败: {e}")
            self.systems['reflection'] = None
        
        # 3. 记忆知识图谱
        try:
            from memory_knowledge_graph import MemoryKnowledgeGraph
            self.systems['knowledge_graph'] = MemoryKnowledgeGraph(self.memory_system, self.emotion_core)
            logger.info("✅ 记忆知识图谱已加载")
        except Exception as e:
            logger.error(f"记忆知识图谱加载失败: {e}")
            self.systems['knowledge_graph'] = None
        
        # 4. 性格演化系统
        try:
            from personality_evolution_system import PersonalityEvolutionSystem
            self.systems['personality'] = PersonalityEvolutionSystem(self.emotion_core, self.memory_system)
            # 将性格系统绑定到情绪核心
            self.emotion_core.personality_evolution = self.systems['personality']
            logger.info("✅ 性格演化系统已加载")
        except Exception as e:
            logger.error(f"性格演化系统加载失败: {e}")
            self.systems['personality'] = None
        
        # 5. 自主社交系统
        try:
            from autonomous_social_system import get_social_manager
            self.systems['social'] = get_social_manager(self.emotion_core)
            logger.info("✅ 自主社交系统已加载")
        except Exception as e:
            logger.error(f"自主社交系统加载失败: {e}")
            self.systems['social'] = None
    
    async def start_all_systems(self):
        """启动所有系统"""
        logger.info("正在启动所有高级系统...")
        
        # 启动高级感知
        if self.systems.get('perception'):
            await self.systems['perception'].start_all()
        
        # 其他系统通常在初始化时自动启动
        logger.info("🚀 所有高级系统已启动")
    
    async def stop_all_systems(self):
        """停止所有系统"""
        logger.info("正在停止所有高级系统...")
        
        # 停止高级感知
        if self.systems.get('perception'):
            await self.systems['perception'].stop_all()
        
        # 触发紧急停止
        if self.systems.get('social'):
            self.systems['social'].controller.emergency_stop_toggle(True)
        
        logger.info("🛑 所有高级系统已停止")
    
    def _safe_start_systems(self):
        """安全地启动所有系统"""
        try:
            # 尝试获取当前事件循环
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果循环正在运行，创建任务
                asyncio.create_task(self.start_all_systems())
            else:
                # 如果没有运行的循环，在后台线程中运行
                import threading
                def run_startup():
                    asyncio.run(self.start_all_systems())
                threading.Thread(target=run_startup, daemon=True).start()
        except RuntimeError:
            # 没有事件循环，在后台线程中创建
            import threading
            def run_startup():
                asyncio.run(self.start_all_systems())
            threading.Thread(target=run_startup, daemon=True).start()
        except Exception as e:
            logger.error(f"安全启动系统失败: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取所有系统状态"""
        status = {
            "systems_loaded": {},
            "perception": None,
            "personality": None,
            "social": None,
            "knowledge_graph": None
        }
        
        # 检查加载状态
        for name, system in self.systems.items():
            status["systems_loaded"][name] = system is not None
        
        # 获取各系统状态
        if self.systems.get('perception'):
            status['perception'] = self.systems['perception'].get_status()
        
        if self.systems.get('personality'):
            status['personality'] = self.systems['personality'].get_personality_summary()
        
        if self.systems.get('social'):
            status['social'] = self.systems['social'].get_status()
        
        if self.systems.get('knowledge_graph'):
            # 简单统计
            status['knowledge_graph'] = {
                "nodes": len(self.systems['knowledge_graph'].memory_nodes),
                "relations": len(self.systems['knowledge_graph'].memory_relations)
            }
        
        return status
    
    async def process_advanced_interaction(self, user_input: str, ai_response: str):
        """处理高级交互"""
        # 性格学习
        if self.systems.get('personality'):
            await self.systems['personality'].learn_from_interaction(
                user_input, ai_response
            )
        
        # 知识图谱关联
        if self.systems.get('knowledge_graph'):
            # 获取相关记忆上下文
            context = await self.systems['knowledge_graph'].get_memory_context(user_input)
            # 这里可以将context用于增强回复
    
    def emergency_stop(self):
        """紧急停止所有自主行为"""
        if self.systems.get('social'):
            self.systems['social'].controller.emergency_stop_toggle(True)
            logger.warning("🚨 紧急停止已激活")
    
    def resume_autonomous(self):
        """恢复自主行为"""
        if self.systems.get('social'):
            self.systems['social'].controller.emergency_stop_toggle(False)
            logger.info("✅ 自主行为已恢复")


def integrate_advanced_features(emotion_core):
    """集成高级功能到情绪核心"""
    try:
        # 检查是否已有记忆系统
        if not hasattr(emotion_core, 'memory_system') or not emotion_core.memory_system:
            logger.error("记忆系统未初始化，无法集成高级功能")
            return None
        
        # 创建高级AI系统
        advanced_system = AdvancedAISystem(emotion_core, emotion_core.memory_system)
        
        # 绑定到情绪核心
        emotion_core.advanced_ai = advanced_system
        
        # 修改原有方法以集成高级功能
        original_process_interaction = emotion_core.process_interaction
        
        def enhanced_process_interaction(user_input: str, ai_response: str = ""):
            # 调用原方法
            result = original_process_interaction(user_input, ai_response)
            
            # 处理高级交互（异步，在后台线程中）
            try:
                import threading
                import asyncio
                
                def run_async():
                    try:
                        # 在新线程中创建事件循环
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(advanced_system.process_advanced_interaction(user_input, ai_response))
                        loop.close()
                    except Exception as e:
                        logger.error(f"高级交互处理失败: {e}")
                
                # 在后台线程中运行
                thread = threading.Thread(target=run_async, daemon=True)
                thread.start()
            except Exception as e:
                logger.error(f"启动高级交互处理失败: {e}")
            
            return result
        
        emotion_core.process_interaction = enhanced_process_interaction
        
        # 添加紧急停止方法
        emotion_core.emergency_stop = advanced_system.emergency_stop
        emotion_core.resume_autonomous = advanced_system.resume_autonomous
        
        # 启动所有系统
        advanced_system._safe_start_systems()
        
        logger.info("🎊 高级AI功能集成成功")
        return advanced_system
        
    except Exception as e:
        logger.error(f"高级功能集成失败: {e}")
        return None


# API配置需求文档
API_REQUIREMENTS = """
# 高级AI系统所需API配置

## 1. OpenAI/兼容API (必需)
- 用于LLM推理和对话生成
- 配置位置: config.json -> api.api_key, api.base_url
- 建议模型: GPT-4或兼容模型

## 2. Twitter API (可选)
- 用于社交媒体发布
- 需要设置环境变量:
  * TWITTER_CONSUMER_KEY
  * TWITTER_CONSUMER_SECRET
  * TWITTER_ACCESS_TOKEN
  * TWITTER_ACCESS_TOKEN_SECRET
- 申请地址: https://developer.twitter.com/

## 3. Neo4j图数据库 (可选)
- 用于知识图谱构建
- 配置位置: config.json -> grag.*
- 可使用Docker快速部署:
  docker run -p 7474:7474 -p 7687:7687 \\
    -e NEO4J_AUTH=neo4j/your_password \\
    neo4j:latest

## 4. 依赖库安装
```bash
# 基础依赖
pip install opencv-python>=4.8.0
pip install SpeechRecognition>=3.10.0
pip install sounddevice>=0.4.6
pip install soundfile>=0.12.1

# 机器学习依赖
pip install transformers>=4.30.0
pip install torch>=2.0.0
pip install sentence-transformers>=2.2.0

# 社交媒体
pip install tweepy>=4.14.0

# 图数据库
pip install py2neo>=2021.2.3
```

## 5. 可选硬件
- 摄像头: 用于视觉感知
- 麦克风: 用于语音识别

## 6. 性能建议
- CPU: 4核以上
- 内存: 8GB以上
- GPU: 可选，用于加速ML模型
"""