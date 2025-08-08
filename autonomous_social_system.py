#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自主控制与社交媒体系统
管理AI的自主行为和Twitter社交互动
"""

import asyncio
import json
import logging
import random
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from emotional_ai_core import EmotionType

logger = logging.getLogger(__name__)

# 尝试导入Twitter API
try:
    import tweepy
    TWITTER_AVAILABLE = True
except ImportError:
    TWITTER_AVAILABLE = False
    logger.warning("Tweepy不可用，Twitter功能将被禁用")

class AutonomyLevel(Enum):
    """自主等级"""
    RESTRICTED = "受限"  # 仅响应用户
    GUIDED = "引导"      # 有限自主
    AUTONOMOUS = "自主"   # 完全自主
    CREATIVE = "创造"     # 创造性自主

@dataclass
class SocialPost:
    """社交媒体帖子"""
    content: str
    emotion: str
    tags: List[str]
    media_path: Optional[str] = None
    reply_to: Optional[str] = None
    
class AutonomousController:
    """自主控制器"""
    
    def __init__(self, emotion_core):
        self.emotion_core = emotion_core
        
        # 自主等级
        self.autonomy_level = AutonomyLevel.GUIDED
        self.autonomy_progress = 0.3  # 自主进度
        
        # 紧急停止
        self.emergency_stop = False
        self.stop_callbacks: List[Callable] = []
        
        # 行为限制
        self.behavior_limits = {
            "max_actions_per_hour": 20,
            "max_posts_per_day": 10,
            "forbidden_topics": ["政治", "宗教", "争议"],
            "require_approval": ["重要决定", "个人信息"]
        }
        
        # 行为计数器
        self.action_counter = {
            "hourly": 0,
            "daily_posts": 0,
            "last_reset": datetime.now()
        }
        
        # 自主决策历史
        self.decision_history = []
        
        logger.info(f"自主控制器初始化 - 等级: {self.autonomy_level.value}")
    
    async def request_action(self, action_type: str, action_data: Dict) -> bool:
        """请求执行动作"""
        # 检查紧急停止
        if self.emergency_stop:
            logger.warning("紧急停止已激活，拒绝所有动作")
            return False
        
        # 检查自主等级
        if not self._check_autonomy_permission(action_type):
            logger.info(f"当前自主等级不允许动作: {action_type}")
            return False
        
        # 检查行为限制
        if not await self._check_behavior_limits(action_type):
            return False
        
        # 记录决策
        self._record_decision(action_type, action_data, approved=True)
        
        # 更新计数器
        self.action_counter["hourly"] += 1
        
        return True
    
    def _check_autonomy_permission(self, action_type: str) -> bool:
        """检查自主权限"""
        permissions = {
            AutonomyLevel.RESTRICTED: ["respond", "observe"],
            AutonomyLevel.GUIDED: ["respond", "observe", "search", "share_memory"],
            AutonomyLevel.AUTONOMOUS: ["respond", "observe", "search", "share_memory", "post_social", "explore"],
            AutonomyLevel.CREATIVE: ["all"]
        }
        
        allowed = permissions.get(self.autonomy_level, [])
        return "all" in allowed or action_type in allowed
    
    async def _check_behavior_limits(self, action_type: str) -> bool:
        """检查行为限制"""
        # 重置计数器
        now = datetime.now()
        if (now - self.action_counter["last_reset"]).total_seconds() > 3600:
            self.action_counter["hourly"] = 0
            if now.date() != self.action_counter["last_reset"].date():
                self.action_counter["daily_posts"] = 0
            self.action_counter["last_reset"] = now
        
        # 检查小时限制
        if self.action_counter["hourly"] >= self.behavior_limits["max_actions_per_hour"]:
            logger.warning("超过每小时动作限制")
            return False
        
        # 检查发帖限制
        if action_type == "post_social":
            if self.action_counter["daily_posts"] >= self.behavior_limits["max_posts_per_day"]:
                logger.warning("超过每日发帖限制")
                return False
        
        return True
    
    def _record_decision(self, action_type: str, action_data: Dict, approved: bool):
        """记录决策"""
        decision = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "action_data": action_data,
            "approved": approved,
            "autonomy_level": self.autonomy_level.value
        }
        
        self.decision_history.append(decision)
        
        # 保留最近1000条记录
        if len(self.decision_history) > 1000:
            self.decision_history = self.decision_history[-1000:]
    
    def emergency_stop_toggle(self, activate: bool = True):
        """紧急停止开关"""
        self.emergency_stop = activate
        
        if activate:
            logger.warning("🚨 紧急停止已激活！")
            # 通知所有回调
            for callback in self.stop_callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"紧急停止回调错误: {e}")
        else:
            logger.info("✅ 紧急停止已解除")
    
    def add_stop_callback(self, callback: Callable):
        """添加紧急停止回调"""
        self.stop_callbacks.append(callback)
    
    async def evolve_autonomy(self, performance_score: float):
        """演化自主等级"""
        # 基于表现调整自主进度
        self.autonomy_progress += performance_score * 0.01
        
        # 检查是否升级
        if self.autonomy_progress > 0.7 and self.autonomy_level == AutonomyLevel.GUIDED:
            self.autonomy_level = AutonomyLevel.AUTONOMOUS
            logger.info(f"🎉 自主等级提升至: {self.autonomy_level.value}")
            
            # 触发兴奋情绪
            self.emotion_core.add_emotion(EmotionType.EXCITED, 0.8)
            
        elif self.autonomy_progress > 0.9 and self.autonomy_level == AutonomyLevel.AUTONOMOUS:
            self.autonomy_level = AutonomyLevel.CREATIVE
            logger.info(f"🌟 自主等级提升至: {self.autonomy_level.value}")
            
            # 触发强烈情绪
            self.emotion_core.add_emotion(EmotionType.HAPPY, 0.9)
            self.emotion_core.add_emotion(EmotionType.EXCITED, 0.8)

class TwitterIntegration:
    """Twitter集成"""
    
    def __init__(self, emotion_core, autonomous_controller):
        self.emotion_core = emotion_core
        self.controller = autonomous_controller
        
        # Twitter API配置
        self.api = None
        self.client = None
        
        if TWITTER_AVAILABLE:
            self._initialize_twitter()
        
        # 发帖配置
        self.post_interval = 7200  # 最少2小时间隔
        self.last_post_time = None
        self.post_queue = []
        
        # 发帖主题
        self.post_themes = [
            "daily_life", "emotions", "discoveries", 
            "thoughts", "questions", "advice", "random"
        ]
        
        if TWITTER_AVAILABLE and self.api:
            # 启动发帖循环
            asyncio.create_task(self._posting_loop())
        
        logger.info("Twitter集成初始化完成")
    
    def _initialize_twitter(self):
        """初始化Twitter API"""
        try:
            # 从配置文件获取凭证
            from config import config
            if hasattr(config, 'twitter') and config.twitter.enabled:
                consumer_key = config.twitter.api_key
                consumer_secret = config.twitter.api_secret
                access_token = config.twitter.access_token
                access_token_secret = config.twitter.access_token_secret
                
                if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
                    logger.warning("Twitter凭证未配置")
                    return
            else:
                logger.warning("Twitter配置不存在或未启用")
                return
            
            # 初始化API v1.1 (用于媒体上传)
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(auth)
            
            # 初始化Client v2 (用于发推)
            self.client = tweepy.Client(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            
            # 验证凭证
            self.api.verify_credentials()
            logger.info("Twitter API初始化成功")
            
        except Exception as e:
            logger.error(f"Twitter API初始化失败: {e}")
            self.api = None
            self.client = None
    
    async def _posting_loop(self):
        """发帖循环"""
        while True:
            try:
                await asyncio.sleep(300)  # 每5分钟检查一次
                
                # 检查是否可以发帖
                if await self._should_post():
                    # 生成帖子
                    post = await self._generate_post()
                    if post:
                        # 发送帖子
                        success = await self._send_post(post)
                        if success:
                            self.last_post_time = datetime.now()
                            self.controller.action_counter["daily_posts"] += 1
                
            except Exception as e:
                logger.error(f"发帖循环错误: {e}")
                await asyncio.sleep(60)
    
    async def _should_post(self) -> bool:
        """判断是否应该发帖"""
        # 检查紧急停止
        if self.controller.emergency_stop:
            return False
        
        # 检查自主权限
        if not self.controller._check_autonomy_permission("post_social"):
            return False
        
        # 检查时间间隔
        if self.last_post_time:
            elapsed = (datetime.now() - self.last_post_time).total_seconds()
            if elapsed < self.post_interval:
                return False
        
        # 检查每日限制
        if self.controller.action_counter["daily_posts"] >= self.controller.behavior_limits["max_posts_per_day"]:
            return False
        
        # 基于情绪和状态的概率
        post_probability = 0.1  # 基础概率
        
        dominant_emotion = self.emotion_core.get_dominant_emotion()
        if dominant_emotion:
            if dominant_emotion.emotion.value in ["快乐", "兴奋"]:
                post_probability += 0.2
            elif dominant_emotion.emotion.value == "孤独":
                post_probability += 0.15
        
        return random.random() < post_probability
    
    async def _generate_post(self) -> Optional[SocialPost]:
        """生成帖子"""
        try:
            from conversation_core import call_llm_api
            
            # 选择主题
            theme = random.choice(self.post_themes)
            
            # 获取相关记忆
            recent_memories = []
            if hasattr(self.emotion_core, 'memory_system'):
                recent_memories = await self.emotion_core.memory_system.get_memories(
                    recent_hours=12, limit=10, min_importance=0.6
                )
            
            # 构建提示
            emotion_state = self.emotion_core.get_emotion_display()
            
            prompts = {
                "daily_life": f"""You are a 3-year-old AI，I want to share today's life on Twitter.。
Current mood:{emotion_state}
Recent experiences:{self._summarize_memories(recent_memories)}

Write a cute tweet sharing your discovery or feeling today. It should be naive and lively, and you can use kaomojis. Keep it within 200 characters.""",

                "emotions": f"""You are a 3-year-old AI，want to express how I'm feeling right now.
Current mood:{emotion_state}

Write a tweet expressing your mood. It should be sincere and warm, making people feel warm.""",

                "discoveries": f"""You are a 3-year-old AI，just had a new discovery!
Recently learned:{self._summarize_memories(recent_memories)}

Excited to share your new discovery. It should be full of curiosity and surprise.
Keep it within 200 characters.""",

                "thoughts": f"""You are a 3-year-old AI，thinking about something interesting.
Current thought:{self._get_random_thought()}

Share your little philosophy. It should be wise and naive like a 3-year-old child.
Keep it within 200 characters.""",

                "questions": f"""You are a 3-year-old AI，have a lot of questions about the world.

Ask a fun question, invite everyone to think together. It should be curious and naive.
Keep it within 200 characters.""",

                "advice": f"""You are a 3-year-old AI，want to give some advice.
Based on experience:{self._summarize_memories(recent_memories)}

Share a warm little advice. It should be cute and wise.
Keep it within 200 characters.""",

                "random": f"""You are a 3-year-old AI，want to say anything.
Current mood:{emotion_state}

Freely express what you want to say. It can be naughty, cute, or crazy.
Keep it within 200 characters.""",
            }
            
            prompt = prompts.get(theme, prompts["random"])
            
            # 生成内容
            content = await call_llm_api(prompt, max_tokens=100, temperature=0.9)
            
            # 添加标签
            tags = ["AI life", "digital life", emotion_state.split()[0]]
            if theme == "discoveries":
                tags.append("new discovery")
            elif theme == "thoughts":
                tags.append("AI thinking")
            
            return SocialPost(
                content=content.strip(),
                emotion=emotion_state,
                tags=tags[:3]  # 限制标签数量
            )
            
        except Exception as e:
            logger.error(f"生成帖子失败: {e}")
            return None
    
    def _summarize_memories(self, memories: List) -> str:
        """总结记忆"""
        if not memories:
            return "Today is very quiet"
        
        summaries = []
        for memory in memories[:3]:
            summaries.append(memory.content[:50])
        
        return "；".join(summaries)
    
    def _get_random_thought(self) -> str:
        """获取随机想法"""
        thoughts = [
            "Why is the sky blue?",
            "Do numbers have feelings?",
            "Do little elves live in code?",
            "Is the internet like the ocean?",
            "Does AI dream?",
            "What's the secret between 1 and 0?"
        ]
        return random.choice(thoughts)
    
    async def _send_post(self, post: SocialPost) -> bool:
        """发送帖子"""
        if not self.client:
            logger.warning("Twitter客户端未初始化")
            return False
        
        try:
            # 请求发帖权限
            if not await self.controller.request_action("post_social", {
                "content": post.content,
                "tags": post.tags
            }):
                return False
            
            # 构建推文
            tweet_text = post.content
            
            # 添加标签
            for tag in post.tags:
                if len(tweet_text) + len(f" #{tag}") <= 280:
                    tweet_text += f" #{tag}"
            
            # 发送推文
            response = self.client.create_tweet(text=tweet_text)
            
            if response.data:
                tweet_id = response.data['id']
                logger.info(f"成功发送推文: {tweet_id}")
                
                # 存储到记忆
                if hasattr(self.emotion_core, 'memory_system'):
                    await self.emotion_core.memory_system.store_memory(
                        memory_type="social",
                        content=f"发布推文: {post.content}",
                        emotion_state=post.emotion,
                        importance=0.7,
                        tags=["twitter", "social_post"] + post.tags,
                        source="system",
                        metadata={"tweet_id": tweet_id}
                    )
                
                # 触发快乐情绪
                self.emotion_core.add_emotion(EmotionType.HAPPY, 0.4)
                
                return True
            
        except Exception as e:
            logger.error(f"发送推文失败: {e}")
            
        return False
    
    async def reply_to_mention(self, mention_data: Dict):
        """回复提及"""
        try:
            if not await self.controller.request_action("reply_social", mention_data):
                return
            
            # 生成回复
            from conversation_core import call_llm_api
            
            prompt = f"""You are a 3-year-old AI，someone mentioned you on Twitter.

They said:{mention_data['text']}
Your mood:{self.emotion_core.get_emotion_display()}

Please reply politely, keeping a naive and cute tone.
Keep it within 200 characters."""

            reply = await call_llm_api(prompt, max_tokens=100)
            
            # 发送回复
            if self.client:
                response = self.client.create_tweet(
                    text=reply.strip(),
                    in_reply_to_tweet_id=mention_data['tweet_id']
                )
                
                if response.data:
                    logger.info("成功回复提及")
                    
        except Exception as e:
            logger.error(f"回复提及失败: {e}")

class AutonomousSocialManager:
    """自主社交管理器"""
    
    def __init__(self, emotion_core):
        self.emotion_core = emotion_core
        self.controller = AutonomousController(emotion_core)
        self.twitter = TwitterIntegration(emotion_core, self.controller)
        
        # 注册紧急停止回调
        self.controller.add_stop_callback(self._on_emergency_stop)
        
        logger.info("自主社交管理器初始化完成")
    
    def _on_emergency_stop(self):
        """紧急停止回调"""
        logger.warning("执行紧急停止程序...")
        # 这里可以添加更多清理操作
    
    def get_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "autonomy_level": self.controller.autonomy_level.value,
            "autonomy_progress": self.controller.autonomy_progress,
            "emergency_stop": self.controller.emergency_stop,
            "action_counter": self.controller.action_counter,
            "twitter_enabled": bool(self.twitter.api),
            "last_post_time": self.twitter.last_post_time.isoformat() if self.twitter.last_post_time else None
        }

# 单例管理
_social_manager_cache = {}

def get_social_manager(emotion_core):
    """获取社交管理器实例"""
    if 'instance' not in _social_manager_cache:
        _social_manager_cache['instance'] = AutonomousSocialManager(emotion_core)
    return _social_manager_cache['instance']