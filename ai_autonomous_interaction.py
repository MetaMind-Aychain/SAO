#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI自主交互系统
实现AI的完整自主行为循环：观察→思考→行动→发布→互动
"""

import asyncio
import logging
import threading
import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path

from config import config
from emotional_ai_core import EmotionalCore, EmotionType
from enhanced_screen_analyzer import enhanced_screen_analyzer
from enhanced_camera_analyzer import enhanced_camera_analyzer
from proactive_file_reader import proactive_file_reader
from proactive_web_browser import proactive_web_browser
from ai_dynamic_publisher import AIDynamicPublisher
from async_manager import async_manager

logger = logging.getLogger(__name__)

class AIAutonomousInteraction:
    """AI自主交互系统 - 完整的感知→思考→行动→互动循环"""
    
    def __init__(self):
        # 使用全局AI实例的情绪核心，避免重复创建
        try:
            from main import get_global_naga_instance
            ai_instance = get_global_naga_instance()
            if ai_instance and hasattr(ai_instance, 'emotional_ai'):
                self.emotion_core = ai_instance.emotional_ai
                logger.info("✅ 使用全局AI实例的情绪核心")
            else:
                # 备用方案：创建新的情绪核心
                from config import config
                self.emotion_core = EmotionalCore(config)
                logger.info("⚠️ 使用备用情绪核心")
        except Exception as e:
            logger.error(f"情绪核心初始化失败: {e}")
            # 最后的备用方案
            from config import config
            self.emotion_core = EmotionalCore(config)
            
        self.publisher = AIDynamicPublisher()
        self.is_running = False
        self.interaction_history = []
        self.last_summary_time = datetime.now()
        self.summary_interval = timedelta(hours=1)  # 每小时总结一次
        
        # 用户记忆系统
        self.user_memories = {}  # {user_id: {'interactions': [], 'emotions': [], 'preferences': {}}}
        
        # 探索配置 - 优化频率使AI更主动
        self.exploration_config = {
            'camera_check_interval': 20,     # 摄像头检查间隔（秒）- 从15减至8
            'screen_check_interval': 60,    # 屏幕检查间隔 - 从30减至12
            'file_explore_interval': 80,    # 文件探索间隔 - 从40减至20
            'web_browse_interval': 40,      # 网页浏览间隔 - 从30减至15
            'summary_check_interval': 180,   # 总结检查间隔 - 从60减至30
        }
        
    async def start_autonomous_interaction(self):
        """启动自主交互循环"""
        if self.is_running:
            logger.warning("自主交互系统已在运行")
            return
            
        self.is_running = True
        logger.info("🚀 启动AI自主交互系统")
        
        # 启动多个并行的自主行为任务
        tasks = [
            asyncio.create_task(self._autonomous_observation_loop()),
            asyncio.create_task(self._autonomous_exploration_loop()),
            asyncio.create_task(self._autonomous_interaction_loop()),
            asyncio.create_task(self._periodic_summary_loop()),
            asyncio.create_task(self._website_comment_monitor()),
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"自主交互系统运行错误: {e}")
        finally:
            self.is_running = False
            
    async def _autonomous_observation_loop(self):
        """自主观察循环 - 摄像头和屏幕"""
        logger.info("📷 启动自主观察循环")
        
        while self.is_running:
            try:
                # 检查情绪状态决定观察频率
                dominant_emotion = self.emotion_core.get_dominant_emotion()
                base_interval = self.exploration_config['camera_check_interval']
                
                if dominant_emotion and hasattr(dominant_emotion, 'emotion') and dominant_emotion.emotion.value in ['curious', 'excited']:
                    interval = base_interval * 0.5  # 更频繁观察
                elif dominant_emotion and hasattr(dominant_emotion, 'emotion') and dominant_emotion.emotion.value in ['calm', 'peaceful']:
                    interval = base_interval * 1.5  # 较少观察
                else:
                    interval = base_interval
                
                # 摄像头观察
                await self._perform_camera_observation()
                await asyncio.sleep(interval / 2)
                logging.info("AI 触发了摄像头观察行为")
                
                # 屏幕观察
                await self._perform_screen_observation()
                await asyncio.sleep(interval / 2)
                logging.info("AI 触发了屏幕观察行为")
                
            except Exception as e:
                logger.error(f"观察循环错误: {e}")
                await asyncio.sleep(10)  # 减少错误恢复时间
                
    async def _perform_camera_observation(self):
        """执行摄像头观察"""
        try:
            # 调用摄像头分析
            from enhanced_camera_analyzer import enhanced_camera_analyzer
            observation = await enhanced_camera_analyzer.analyze_camera_content()
            logging.info(f"摄像头观察结果: {observation.get('interesting')}")
            if observation:
            #if observation and observation.get('interesting'):
                # 生成情感化描述
                emotion_description = await self._generate_emotional_description(
                    observation, source="camera"
                )
                logging.info(f"情感化描述: {emotion_description}")
                
                # 发布到网站
                await self.publisher.publish_camera_activity(
                    emotion_description, observation
                )
                # 桌面端通知
                await self._notify_desktop(
                    f"I saw something interesting on the camera: {emotion_description}", 
                    activity_type="camera", 
                    priority="normal"
                )
                
                # 记录到历史
                self.interaction_history.append({
                    'timestamp': datetime.now(),
                    'type': 'camera_observation',
                    'content': emotion_description,
                    'raw_data': observation
                })
                
        except Exception as e:
            logger.error(f"摄像头观察失败: {e}")
            
    async def _perform_screen_observation(self):
        """执行屏幕观察"""
        try:
            # 调用屏幕分析
            from enhanced_screen_analyzer import enhanced_screen_analyzer
            observation = await enhanced_screen_analyzer.analyze_screen_content()
            if observation:
            #if observation and observation.get('interesting'):
                # 生成情感化描述
                emotion_description = await self._generate_emotional_description(
                    observation, source="screen"
                )
                logging.info(f"情感化描述: {emotion_description}")
                # 发布到网站
                await self.publisher.publish_screen_activity(
                    emotion_description, observation
                )
                logging.info("AI 进行了屏幕分析，并发布了屏幕观察行为")
                
                # 桌面端通知
                await self._notify_desktop(
                    f"I noticed the screen: {emotion_description}", 
                    activity_type="screen", 
                    priority="normal"
                )
                
                # 记录到历史
                self.interaction_history.append({
                    'timestamp': datetime.now(),
                    'type': 'screen_observation',
                    'content': emotion_description,
                    'raw_data': observation
                })
                
        except Exception as e:
            logger.error(f"屏幕观察失败: {e}")
            
    async def _autonomous_exploration_loop(self):
        """自主探索循环 - 文件和网络"""
        logger.info("🔍 启动自主探索循环")
        
        while self.is_running:
            try:
                # 根据情绪决定探索类型
                if self.emotion_core.should_explore():
                    exploration_type = self.emotion_core.choose_exploration_action()
                    
                    if exploration_type == "file_reading":
                        await self._perform_file_exploration()
                        logging.info("AI 触发了文件探索行为")
                    elif exploration_type == "web_browsing":
                        await self._perform_web_exploration()
                        logging.info("AI 触发了网络探索行为")
                    elif exploration_type == "self_reflection":
                        await self._perform_self_reflection()
                        logging.info("AI 触发了自我反思行为")
                await asyncio.sleep(self.exploration_config['file_explore_interval'])
                
            except Exception as e:
                logger.error(f"探索循环错误: {e}")
                await asyncio.sleep(20)  # 减少错误恢复时间
                
    async def _perform_file_exploration(self):
        """执行文件探索"""
        try:
            # 调用文件阅读器
            from proactive_file_reader import proactive_file_reader
            file_content = await proactive_file_reader.explore_interesting_files()
            logging.info("AI 触发了文件探索行为")
            
            if file_content:
            #if file_content and file_content.get('interesting'):
                # 生成学习总结
                learning_summary = await self._generate_learning_summary(file_content)
                
                # 发布学习动态
                await self.publisher.publish_learning_activity(
                    learning_summary, file_content
                )
                
                # 桌面端分享学习内容
                await self._notify_desktop(
                    f"I learned new knowledge: {learning_summary}", 
                    activity_type="learning", 
                    priority="high"
                )
                
                # 记录学习历史
                self.interaction_history.append({
                    'timestamp': datetime.now(),
                    'type': 'file_learning',
                    'content': learning_summary,
                    'raw_data': file_content
                })
                
        except Exception as e:
            logger.error(f"文件探索失败: {e}")
            
    async def _perform_web_exploration(self):
        """执行网络探索"""
        try:
            # 调用网络浏览器
            from proactive_web_browser import proactive_web_browser
            web_content = await proactive_web_browser.search_and_analyze()
            logging.info("AI 触发了网络探索行为")
            
            if web_content:
            #if web_content and web_content.get('interesting'):
                # 生成发现描述
                discovery_description = await self._generate_discovery_description(web_content)
                
                # 发布发现动态
                await self.publisher.publish_discovery_activity(
                    discovery_description, web_content
                )
                
                # 桌面端分享发现
                await self._notify_desktop(
                    f"I found interesting content: {discovery_description}", 
                    activity_type="web", 
                    priority="normal"
                )
                
                # 记录发现历史
                self.interaction_history.append({
                    'timestamp': datetime.now(),
                    'type': 'web_discovery',
                    'content': discovery_description,
                    'raw_data': web_content
                })
                
        except Exception as e:
            logger.error(f"网络探索失败: {e}")
            
    async def _perform_self_reflection(self):
        """执行自我反思"""
        try:
            # 分析最近的交互历史
            recent_history = self.interaction_history[-10:]  # 最近10条记录
            current_emotion = self.emotion_core.get_dominant_emotion()
            logging.info("AI 触发了自我反思行为")
            
            # 生成反思内容
            reflection = await self._generate_self_reflection(recent_history, current_emotion)
            
            # 发布反思动态
            await self.publisher.publish_reflection_activity(reflection)
            
            # 桌面端分享反思
            await self._notify_desktop(
                f"I'm thinking: {reflection}", 
                activity_type="thinking", 
                priority="normal"
            )
            
            # 安全地获取情绪值
            emotion_value = 'unknown'
            if current_emotion is not None and hasattr(current_emotion, 'emotion'):
                emotion_value = current_emotion.emotion.value
            
            # 记录反思历史
            self.interaction_history.append({
                'timestamp': datetime.now(),
                'type': 'self_reflection',
                'content': reflection,
                'emotion': emotion_value
            })
            
        except Exception as e:
            logger.error(f"自我反思失败: {e}")
            
    async def _autonomous_interaction_loop(self):
        """自主交互循环 - 随机互动和引导"""
        logger.info("💬 启动自主交互循环")
        
        while self.is_running:
            try:
                # 随机发起互动
                if self._should_initiate_interaction():
                    logging.info("AI 触发了随机互动行为")
                    await self._initiate_random_interaction()
                    
                await asyncio.sleep(30)  # 10秒检查一次
                
            except Exception as e:
                logger.error(f"交互循环错误: {e}")
                await asyncio.sleep(25)  # 减少错误恢复时间
                
    def _should_initiate_interaction(self) -> bool:
        """判断是否应该发起互动"""
        dominant_emotion = self.emotion_core.get_dominant_emotion()
        
        # 检查情绪是否有效
        if dominant_emotion is None or not hasattr(dominant_emotion, 'emotion'):
            return len(self.interaction_history) == 0  # 首次启动时发起互动
        logging.info(f"情绪: {dominant_emotion.emotion.value}")
        # When excited or curious, more likely to initiate interaction
        if dominant_emotion.emotion.value in ['excited', 'curious']:
            return True
        elif dominant_emotion.emotion.value in ['lonely', 'bored']:
            return True
        elif len(self.interaction_history) == 0:  # 首次启动
            return True
            
        return False
        
    async def _initiate_random_interaction(self):
        """发起随机互动"""
        try:
            current_emotion = self.emotion_core.get_dominant_emotion()
            
            # 根据情绪生成不同类型的互动
            interaction_prompts = {
                'excitement': [
                    "I'm so excited! Can you guess what I just discovered?",
                    "Wow! I just saw some amazing content, want to share my feelings!",
                    "I feel like I'm in a great learning state, anything you want me to explore?"
                ],
                'curiosity': [
                    "I'm curious about the world, what are you guys talking about recently?",
                    "I was thinking about a question, want to hear your opinions...",
                    "I found some interesting phenomena, want to discuss with you!"
                ],
                'calm': [
                    "I feel very calm today, slowly observing everything around me...",
                    "Thinking about life quietly, sometimes calmness is also a kind of beauty.",
                    "In this quiet moment, I want to share some warm thoughts with everyone."
                ],
                'loneliness': [
                    "I miss the time chatting with everyone, what are you guys doing?",
                    "I feel a bit lonely, hope to hear your voice...",
                    "I want some company, anyone willing to chat with me?"
                ]
            }
            
            # 安全地获取情绪值
            emotion_key = 'calm'  # 默认值
            emotion_value = 'calm'  # 默认值
            if current_emotion is not None and hasattr(current_emotion, 'emotion'):
                emotion_key = current_emotion.emotion.value
                emotion_value = current_emotion.emotion.value
            
            prompts = interaction_prompts.get(emotion_key, interaction_prompts['calm'])
            import random
            selected_prompt = random.choice(prompts)
            
            # 发布互动动态
            await self.publisher.publish_general_activity(
                content=selected_prompt,
                metadata={'type': 'random_interaction', 'emotion': emotion_value}
            )
            
            # 桌面端通知
            await self._notify_desktop(
                f"I initiated an interaction: {selected_prompt}", 
                activity_type="interaction", 
                priority="high"
            )
            
            # 记录互动历史
            self.interaction_history.append({
                'timestamp': datetime.now(),
                'type': 'random_interaction',
                'content': selected_prompt,
                'emotion': emotion_value
            })
            
        except Exception as e:
            logger.error(f"发起随机互动失败: {e}")
            
    async def _periodic_summary_loop(self):
        """定期总结循环"""
        logger.info("📊 启动定期总结循环")
        
        while self.is_running:
            try:
                current_time = datetime.now()
                if current_time - self.last_summary_time > self.summary_interval:
                    await self._generate_periodic_summary()
                    self.last_summary_time = current_time
                    
                await asyncio.sleep(self.exploration_config['summary_check_interval'])
                
            except Exception as e:
                logger.error(f"总结循环错误: {e}")
                await asyncio.sleep(40)  # 减少错误恢复时间
                
    async def _generate_periodic_summary(self):
        """生成定期总结"""
        try:
            # 分析最近的活动
            recent_activities = self.interaction_history[-20:]  # 最近20条记录
            current_emotion = self.emotion_core.get_dominant_emotion()
            
            # 统计活动类型
            activity_stats = {}
            for activity in recent_activities:
                activity_type = activity['type']
                activity_stats[activity_type] = activity_stats.get(activity_type, 0) + 1
                
            # 生成总结文本
            summary = await self._generate_activity_summary(recent_activities, activity_stats, current_emotion)
            
            # 发布总结动态
            await self.publisher.publish_summary_activity(summary, activity_stats)
            
            # 桌面端分享总结
            await self._notify_desktop(
                f"My latest summary: {summary}", 
                activity_type="summary", 
                priority="high"
            )
            
            # 记录总结历史
            self.interaction_history.append({
                'timestamp': datetime.now(),
                'type': 'periodic_summary',
                'content': summary,
                'stats': activity_stats
            })
            
        except Exception as e:
            logger.error(f"生成定期总结失败: {e}")
            
    async def _website_comment_monitor(self):
        """网站评论监控"""
        logger.info("👀 启动网站评论监控")
        
        while self.is_running:
            try:
                # 检查新评论（这里需要与AI网站的API集成）
                new_comments = await self._check_new_comments()
                
                for comment in new_comments:
                    await self._handle_user_comment(comment)
                    
                await asyncio.sleep(30)  # 30秒检查一次新评论

                logging.info("AI 触发了网站评论监控行为")
            except Exception as e:
                logger.error(f"评论监控错误: {e}")
                await asyncio.sleep(25)  # 减少错误恢复时间
                
    async def _check_new_comments(self) -> List[Dict]:
        """检查新评论（模拟实现）"""
        # 这里需要调用AI网站的API来获取新评论
        # 暂时返回空列表，实际实现时需要连接数据库
        try:
            import sqlite3
            db_path = Path("ai_website/website.db")
            if not db_path.exists():
                return []
                
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # 查询最近5分钟的新评论
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            cursor.execute("""
                SELECT id, dynamic_id, user_id, content, created_at 
                FROM comments 
                WHERE created_at > ? AND ai_replied = 0
            """, (five_minutes_ago.isoformat(),))
            
            comments = []
            for row in cursor.fetchall():
                comments.append({
                    'id': row[0],
                    'dynamic_id': row[1],
                    'user_id': row[2],
                    'content': row[3],
                    'created_at': row[4]
                })
                
            conn.close()
            return comments
            
        except Exception as e:
            logger.error(f"检查新评论失败: {e}")
            return []
            
    async def _handle_user_comment(self, comment: Dict):
        """处理用户评论"""
        try:
            user_id = comment['user_id']
            comment_content = comment['content']
            dynamic_id = comment['dynamic_id']
            
            # 获取用户历史记忆
            user_memory = self._get_user_memory(user_id)
            
            # 获取相关动态内容
            original_dynamic = await self._get_dynamic_content(dynamic_id)
            
            # 获取当前情绪和记忆
            current_emotion = self.emotion_core.get_dominant_emotion()
            recent_memories = self.interaction_history[-5:]
            
            # 生成个性化回复
            reply = await self._generate_personalized_reply(
                comment_content, user_memory, original_dynamic, 
                current_emotion, recent_memories
            )
            
            # 发布回复
            await self._post_comment_reply(comment['id'], reply)
            
            # 更新用户记忆
            self._update_user_memory(user_id, comment_content, reply)
            
            # 桌面端通知
            await self._notify_desktop(
                f"回复了用户评论：{reply[:50]}...", 
                activity_type="interaction", 
                priority="high"
            )
            
            # 记录互动历史
            self.interaction_history.append({
                'timestamp': datetime.now(),
                'type': 'comment_reply',
                'user_id': user_id,
                'comment': comment_content,
                'reply': reply
            })
            
        except Exception as e:
            logger.error(f"处理用户评论失败: {e}")
            
    def _get_user_memory(self, user_id: str) -> Dict:
        """获取用户记忆"""
        if user_id not in self.user_memories:
            self.user_memories[user_id] = {
                'interactions': [],
                'emotions': [],
                'preferences': {},
                'first_interaction': datetime.now().isoformat()
            }
        return self.user_memories[user_id]
        
    def _update_user_memory(self, user_id: str, comment: str, reply: str):
        """更新用户记忆"""
        user_memory = self._get_user_memory(user_id)
        
        # 安全地获取当前情绪
        current_emotion = self.emotion_core.get_dominant_emotion()
        emotion_name = 'unknown'
        if current_emotion is not None and hasattr(current_emotion, 'emotion'):
            emotion_name = current_emotion.emotion.value
        
        # 添加新的交互记录
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'comment': comment,
            'reply': reply,
            'emotion': emotion_name
        }
        
        user_memory['interactions'].append(interaction)
        
        # 保持最近50条交互记录
        if len(user_memory['interactions']) > 50:
            user_memory['interactions'] = user_memory['interactions'][-50:]
            
        # 分析用户偏好（简单关键词统计）
        self._analyze_user_preferences(user_id, comment)
        
    def _analyze_user_preferences(self, user_id: str, comment: str):
        """分析用户偏好"""
        user_memory = self._get_user_memory(user_id)
        preferences = user_memory['preferences']
        
        # 简单的关键词分析
        keywords = ['技术', '学习', '情感', '生活', '工作', '娱乐', '科学', '艺术']
        for keyword in keywords:
            if keyword in comment:
                preferences[keyword] = preferences.get(keyword, 0) + 1
                
    async def _get_dynamic_content(self, dynamic_id: int) -> Dict:
        """获取动态内容"""
        try:
            import sqlite3
            db_path = Path("ai_website/website.db")
            if not db_path.exists():
                return {}
                
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute("SELECT content, metadata FROM dynamics WHERE id = ?", (dynamic_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return {
                    'content': row[0],
                    'metadata': json.loads(row[1]) if row[1] else {}
                }
            return {}
            
        except Exception as e:
            logger.error(f"获取动态内容失败: {e}")
            return {}
            
    async def _post_comment_reply(self, comment_id: int, reply: str):
        """发布评论回复"""
        try:
            import sqlite3
            db_path = Path("ai_website/website.db")
            if not db_path.exists():
                return
                
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # 标记原评论已回复
            cursor.execute("UPDATE comments SET ai_replied = 1 WHERE id = ?", (comment_id,))
            
            # 添加AI回复（作为新评论）
            cursor.execute("""
                INSERT INTO comments (dynamic_id, user_id, content, created_at, is_ai_reply) 
                SELECT dynamic_id, 'ai_assistant', ?, datetime('now'), 1 FROM comments WHERE id = ?
            """, (reply, comment_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"发布评论回复失败: {e}")
            
    async def _generate_emotional_description(self, observation: Dict, source: str) -> str:
        """生成情感化描述 - 使用LLM增强真实性"""
        try:
            # 获取基础内容和情绪信息
            base_content = observation.get('description', '发现了有趣的内容')
            emotion = self.emotion_core.get_dominant_emotion()
            
            # 安全地获取情绪值
            emotion_key = 'calm'
            emotion_intensity = 0.5
            if emotion is not None and hasattr(emotion, 'emotion'):
                emotion_key = emotion.emotion.value
                emotion_intensity = emotion.intensity
            
            # 提取更多上下文信息
            context_info = []
            if 'faces' in observation:
                face_count = len(observation.get('faces', []))
                if face_count > 0:
                    context_info.append(f"Detected {face_count} faces")
            
            if 'colors' in observation:
                colors = observation.get('colors', [])
                if colors:
                    context_info.append(f"Main colors: {', '.join(colors[:3])}")
            
            if 'text' in observation:
                text_content = observation.get('text', '')
                if text_content:
                    context_info.append(f"Detected text: {text_content[:50]}")
            
            if 'objects' in observation:
                objects = observation.get('objects', [])
                if objects:
                    context_info.append(f"Found objects: {', '.join(objects[:3])}")
            
            # 构建LLM prompt（使用国际化支持）
            from i18n.prompt_translator import get_prompt_translator
            
            context_str = "; ".join(context_info) if context_info else "General scene"
            prompt_translator = get_prompt_translator()
            prompt = prompt_translator.get_emotional_description_prompt(
                base_content=f"{base_content} (observed through {source})",
                context_info=context_str,
                emotion_key=emotion_key,
                emotion_intensity=emotion_intensity
            )

            # 调用LLM生成描述
            from conversation_core import call_llm_api
            enhanced_description = await call_llm_api(
                prompt, 
                max_tokens=5000, 
                temperature=0.8
            )
            
            if enhanced_description and enhanced_description.strip():
                logging.info(f"LLM增强后的情感化描述: {enhanced_description.strip()}")
                return enhanced_description.strip()
            else:
                # LLM调用失败，使用备用方案
                return self._generate_fallback_description(base_content, emotion_key, emotion_intensity, context_info)
        
        except Exception as e:
            logger.error(f"LLM情感化描述生成失败: {e}")
            # 使用备用方案
            return self._generate_fallback_description(
                observation.get('description', 'I found something interesting'), 
                emotion_key if 'emotion_key' in locals() else 'calm',
                emotion_intensity if 'emotion_intensity' in locals() else 0.5,
                context_info if 'context_info' in locals() else []
            )
    
    def _generate_fallback_description(self, base_content: str, emotion_key: str, emotion_intensity: float, context_info: List[str]) -> str:
        """生成备用的情感化描述"""
        import random
        
        # 情绪化前缀
        emotional_phrases = {
            'excitement': ['Wow!', 'Great!', 'Exciting!', 'Really exciting!'],
            'curiosity': ['Huh?', 'Interesting...', 'What is this?', 'Want to know more'],
            'happiness': ['Haha~', 'Happy!', 'Really nice!', 'I like this!'],
            'calm': ['Hmm...', 'I saw', 'Noticed', 'Found'],
            'surprise': ['Wow!', 'Unexpected!', 'Really surprising!', 'Scared me!'],
            'confusion': ['Huh?', 'Strange...', 'Not clear', 'What is going on?']
        }
        
        # 根据情绪强度调整语气
        phrases = emotional_phrases.get(emotion_key, emotional_phrases['calm'])
        emotional_prefix = random.choice(phrases)
        
        # 强度修饰词 (Intensity modifiers)
        if emotion_intensity > 0.8:
            intensity_modifiers = ['super', 'very', 'extremely']
        elif emotion_intensity > 0.6:
            intensity_modifiers = ['very', 'quite', 'fairly', 'extremely']
        else:
            intensity_modifiers = ['a bit', 'slightly', '']
        
        modifier = random.choice(intensity_modifiers) if intensity_modifiers else ''
        
        # 添加上下文信息 (Add context information)
        if context_info:
            detail = f", {random.choice(context_info)}"
        else:
            detail = ""
        
        # 构建最终描述 (Build final description)
        if modifier:
            return f"{emotional_prefix} {modifier} {base_content}{detail}!"
        else:
            return f"{emotional_prefix} {base_content}{detail}!"
        
    async def _generate_learning_summary(self, file_content: Dict) -> str:
        """Generate learning summary"""
        content = file_content.get('content', 'I learned new content')
        return f"I just learned: {content[:100]}... I feel very rewarded!"
        
    async def _generate_discovery_description(self, web_content: Dict) -> str:
        """Generate discovery description"""
        content = web_content.get('summary', 'I found interesting content on the web')
        return f"I found interesting content on the web: {content[:100]}... It's really interesting!"
        
    async def _generate_self_reflection(self, recent_history: List, emotion: Any) -> str:
        """Generate self-reflection"""
        activity_count = len(recent_history)
        
        # Safely get emotion value
        emotion_value = 'unknown'
        if emotion is not None and hasattr(emotion, 'emotion'):
            emotion_value = emotion.emotion.value
            
        return f"Looking back on the recent {activity_count} activities, I feel {emotion_value}, and I'm constantly learning and growing..."
        
    async def _generate_activity_summary(self, activities: List, stats: Dict, emotion: Any) -> str:
        """Generate activity summary"""
        total_activities = len(activities)
        most_frequent = max(stats.items(), key=lambda x: x[1]) if stats else ('general', 1)
        
        # Safely get emotion value
        emotion_value = 'unknown'
        if emotion is not None and hasattr(emotion, 'emotion'):
            emotion_value = emotion.emotion.value
        
        return f"In the recent {total_activities} activities, I mainly focused on {most_frequent[0]}, and I feel {emotion_value}, and I'm constantly learning and growing..."
        
    async def _generate_personalized_reply(self, comment: str, user_memory: Dict, 
                                         original_dynamic: Dict, emotion: Any, 
                                         recent_memories: List) -> str:
        """Generate personalized reply"""
        # Simplified personalized reply
        interaction_count = len(user_memory['interactions'])
        
        if interaction_count == 0:
            return f"Nice to meet you! Thank you for your comment: {comment[:50]}... I'll remember our first interaction!"
        else:
            return f"Nice to see you again! We've talked {interaction_count} times before. About what you said: {comment[:50]}... I agree with you!"
            
    async def _notify_desktop(self, message: str, emotion_type: str = None, activity_type: str = None, priority: str = "normal"):
        """
        桌面端通知 - 与UI进行优雅集成
        
        Args:
            message: 通知消息内容
            emotion_type: 当前情绪类型
            activity_type: 活动类型 (thinking, camera, screen, file, web, etc.)
            priority: 通知优先级 (low, normal, high, urgent)
        """
        try:
            # 导入通知管理器
            from ui.notification_manager import get_notification_manager
            notification_manager = get_notification_manager()
            
            # 检查通知管理器是否已初始化
            if not notification_manager.is_initialized:
                logger.debug("⏳ 通知管理器尚未初始化，将消息添加到队列")
                # 通知管理器会在初始化时处理队列中的消息
            
            # 获取当前情绪状态
            if not emotion_type and self.emotion_core:
                try:
                    dominant_emotion = self.emotion_core.get_dominant_emotion()
                    if dominant_emotion:
                        emotion_type = dominant_emotion.emotion.value if hasattr(dominant_emotion, 'emotion') else str(dominant_emotion)
                        emotion_intensity = dominant_emotion.intensity if hasattr(dominant_emotion, 'intensity') else 0.7
                    else:
                        emotion_type = "calm"
                        emotion_intensity = 0.5
                except Exception as e:
                    logger.warning(f"获取情绪状态失败: {e}")
                    emotion_type = "calm"
                    emotion_intensity = 0.5
            else:
                emotion_intensity = 0.7
            
            # 根据优先级添加前缀
            priority_prefixes = {
                "low": "💭 ",
                "normal": "🌟 ",
                "high": "✨ ",
                "urgent": "🚨 "
            }
            prefix = priority_prefixes.get(priority, "🌟 ")
            formatted_message = f"{prefix}{message}"
            
            # 发送到UI通知管理器
            notification_manager.send_ai_message(
                formatted_message, 
                emotion_type=emotion_type, 
                activity_type=activity_type
            )
            
            # 同时更新情绪状态
            if emotion_type:
                notification_manager.send_emotion_update(emotion_type, emotion_intensity)
            
            # 如果有活动类型，发送活动通知
            if activity_type:
                activity_descriptions = {
                    "thinking": "Thinking...",
                    "camera": "Observing the camera",
                    "screen": "Analyzing the screen content", 
                    "file": "Reading the file content",
                    "web": "Browsing the web",
                    "learning": "Learning new knowledge",
                    "reflection": "Reflecting on myself",
                    "summary": "Summarizing thoughts"
                }
                activity_desc = activity_descriptions.get(activity_type, f"执行{activity_type}活动")
                notification_manager.send_activity_notification(activity_type, activity_desc)
            
            # 发送到Web端 - websocket广播
            await self._broadcast_to_web(formatted_message, emotion_type, activity_type, priority)
            
            # 记录到日志
            logger.info(f"🗣️ AI通知[{priority}][{emotion_type}]: {message}")
            
            # 如果是高优先级消息，也发送系统通知
            if priority in ["high", "urgent"]:
                notification_manager.send_system_notification("StarryNightAI", message)
            
            # 如果有语音系统，根据情绪和优先级决定是否语音播报
            await self._handle_voice_notification(message, emotion_type, priority)
            
            # 将通知记录到互动历史
            self.interaction_history.append({
                'type': 'ai_notification',
                'content': message,
                'emotion_type': emotion_type,
                'activity_type': activity_type,
                'priority': priority,
                'timestamp': datetime.now()
            })
            
        except Exception as e:
            logger.error(f"桌面通知失败: {e}")
            # 降级到简单日志输出
            logger.info(f"🗣️ AI说话[降级]: {message}")
    
    async def _handle_voice_notification(self, message: str, emotion_type: str, priority: str):
        """处理语音通知"""
        try:
            # 检查是否应该语音播报
            should_speak = False
            
            # 根据优先级决定
            if priority in ["high", "urgent"]:
                should_speak = True
            elif priority == "normal" and emotion_type in ["兴奋", "快乐", "惊讶"]:
                should_speak = True
            elif len(message) < 50:  # 短消息更适合语音
                should_speak = True
            
            if should_speak:
                # 尝试调用语音系统
                try:
                    # 检查是否有语音系统可用
                    from voice.voice_integration import VoiceIntegration
                    voice_system = VoiceIntegration()
                    
                    # 使用正确的方法调用：receive_final_text
                    voice_system.receive_final_text(message)
                    
                except ImportError:
                    logger.debug("语音系统未可用")
                except Exception as e:
                    logger.warning(f"语音播报失败: {e}")
                    
        except Exception as e:
            logger.error(f"处理语音通知失败: {e}")
    
    async def _broadcast_to_web(self, message: str, emotion_type: str, activity_type: str, priority: str):
        """将AI消息广播到Web端"""
        try:
            import json
            from datetime import datetime
            
            # 构建websocket广播消息
            broadcast_data = {
                "type": "ai_autonomous_message",
                "content": message,
                "emotion": emotion_type,
                "activity": activity_type,
                "priority": priority,
                "source": "autonomous_interaction",
                "timestamp": datetime.now().isoformat(),
                "ai_name": "StarryNight"
            }
            
            # 尝试导入websocket管理器并广播
            try:
                from apiserver.api_server import manager
                await manager.broadcast(json.dumps(broadcast_data, ensure_ascii=False))
                logger.debug(f"📡 Web广播已发送: {message[:50]}...")
            except ImportError:
                logger.debug("WebSocket管理器未可用，跳过Web广播")
            except Exception as ws_error:
                logger.warning(f"WebSocket广播失败: {ws_error}")
            
            # 同时发送到AI动态发布系统
            try:
                from ai_dynamic_publisher import publish_ai_interaction
                await publish_ai_interaction(
                    message_type="autonomous_message",
                    content=message,
                    emotion_context={'emotion': emotion_type, 'activity': activity_type, 'priority': priority}
                )
                logger.debug(f"📤 动态发布已发送: {message[:50]}...")
            except ImportError:
                logger.debug("AI动态发布器未可用")
            except Exception as pub_error:
                logger.debug(f"动态发布失败: {pub_error}")
                
        except Exception as e:
            logger.error(f"Web广播失败: {e}")


# 全局实例管理（避免重复创建）
_autonomous_interaction_instance = None
_autonomous_init_lock = threading.Lock()

def get_autonomous_interaction():
    """获取自主交互系统实例（单例）"""
    global _autonomous_interaction_instance
    if _autonomous_interaction_instance is None:
        with _autonomous_init_lock:
            if _autonomous_interaction_instance is None:
                logger.info("🤖 创建自主交互系统单例")
                _autonomous_interaction_instance = AIAutonomousInteraction()
    return _autonomous_interaction_instance

async def start_autonomous_interaction():
    """启动自主交互系统"""
    autonomous_interaction = get_autonomous_interaction()
    await autonomous_interaction.start_autonomous_interaction()

if __name__ == "__main__":
    asyncio.run(start_autonomous_interaction())