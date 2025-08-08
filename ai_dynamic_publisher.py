#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI动态发布系统 - 将AI的各种活动自动发布到网站
"""

import asyncio
import logging
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path

from conversation_core import call_llm_api

logger = logging.getLogger(__name__)

class AIDynamicPublisher:
    """AI动态发布器 - 连接桌面端AI和网站端"""
    
    def __init__(self):
        self.enabled = False
        self.website_api = None
        self.ai_instance = None  # 添加AI实例引用
        self.last_activities = []
        self.publish_queue = asyncio.Queue()
        self.is_running = False
        self.publisher_task = None
        
        # 动态类型配置（提高发布频率）
        self.activity_configs = {
            'screen_observation': {
                'enabled': True,
                'frequency': 0.8,  # 60%的屏幕观察会发布动态
                'emotion_boost': 0.2
            },
            'camera_interaction': {
                'enabled': True,
                'frequency': 0.8,  # 80%的摄像头互动会发布动态
                'emotion_boost': 0.3
            },
            'file_reading': {
                'enabled': True,
                'frequency': 0.8,  # 70%的文件阅读会发布动态
                'emotion_boost': 0.2
            },
            'web_browsing': {
                'enabled': True,
                'frequency': 0.9,  # 90%的网络浏览会发布动态
                'emotion_boost': 0.3
            },
            'thinking': {
                'enabled': True,
                'frequency': 0.9,  # 90%的思考会发布动态
                'emotion_boost': 0.1
            },
            'emotion_change': {
                'enabled': True,
                'frequency': 0.9,  # 90%的情绪变化会发布动态
                'emotion_boost': 0.0
            },
            'conversation': {
                'enabled': True,
                'frequency': 0.8,  # 80%的对话会发布动态
                'emotion_boost': 0.1
            },
            'self_reflection': {
                'enabled': True,
                'frequency': 1.0,  # 100%的自我反思会发布动态
                'emotion_boost': 0.2
            }
        }
    
    def initialize(self, website_api_instance):
        """初始化发布器"""
        self.website_api = website_api_instance
        self.enabled = True
        logger.info("✅ AI动态发布系统已初始化")
    
    def set_ai_instance(self, ai_instance):
        """设置AI实例"""
        self.ai_instance = ai_instance
        logger.info("✅ AI实例已连接到动态发布器")
    
    def get_ai_instance(self):
        """获取AI实例"""
        return self.ai_instance
    
    async def start_publisher(self):
        """启动发布器"""
        if not self.enabled:
            logger.warning("AI动态发布器未启用")
            return
        
        if self.is_running:
            logger.warning("AI动态发布器已在运行中")
            return
        
        self.is_running = True
        
        # 启动发布任务并存储引用
        self.publisher_task = asyncio.create_task(self._publisher_loop())
        
        logger.info("🚀 AI动态发布器已启动")
    
    async def stop_publisher(self):
        """停止发布器"""
        self.is_running = False
        
        # 取消并等待任务完成
        if self.publisher_task and not self.publisher_task.done():
            self.publisher_task.cancel()
            try:
                await self.publisher_task
            except asyncio.CancelledError:
                logger.debug("发布器任务已取消")
            except Exception as e:
                logger.error(f"停止发布器任务时出错: {e}")
        
        self.publisher_task = None
        logger.info("⏹️ AI动态发布器已停止")
    
    async def _publisher_loop(self):
        """发布器主循环 - 修复队列逻辑"""
        logger.info("🚀 发布器主循环启动")
        while self.is_running:
            try:
                # 检查队列大小
                queue_size = self.publish_queue.qsize()
                if queue_size > 0:
                    logger.info(f"📋 发布队列中有 {queue_size} 个待处理活动")
                
                try:
                    # 使用超时等待来避免无限阻塞
                    activity = await asyncio.wait_for(
                        self.publish_queue.get(), 
                        timeout=2.0
                    )
                    logger.info(f"✅ 获得到活动: {activity['type']} - {activity['content'][:50]}...")
                    await self._process_and_publish(activity)
                    
                except asyncio.TimeoutError:
                    # 没有新活动，继续循环
                    logger.debug("⏰ 队列等待超时，继续监听...")
                    pass
                    
                await asyncio.sleep(0.5)  # 减少CPU占用
                
            except Exception as e:
                logger.error(f"❌ 发布器循环错误: {e}")
                import traceback
                traceback.print_exc()
                await asyncio.sleep(5)
    
    async def record_ai_activity(self, activity_type: str, content: str, metadata: Dict[str, Any] = None, emotion_context: Dict[str, Any] = None):
        """记录AI活动并决定是否发布"""
        try:
            # 检查是否应该发布这个活动
            config = self.activity_configs.get(activity_type, {})
            if not config.get('enabled', False):
                return
            
            frequency = config.get('frequency', 0.5)
            publish_chance = random.random()
            logger.debug(f"🎲 发布概率检查: {publish_chance:.2f} vs {frequency:.2f}")
            
            if publish_chance > frequency:
                logger.debug(f"⏭️ 跳过发布: {activity_type} ({publish_chance:.2f} > {frequency:.2f})")
                return  # 不发布这次活动
                
            logger.info(f"✅ 决定发布: {activity_type} ({publish_chance:.2f} <= {frequency:.2f})")
            
            # 构建活动数据
            activity_data = {
                'type': activity_type,
                'content': content,
                'metadata': metadata or {},
                'emotion_context': emotion_context or {},
                'timestamp': datetime.now().isoformat(),
                'should_publish': True
            }
            
            # 添加到发布队列
            await self.publish_queue.put(activity_data)
            queue_size = self.publish_queue.qsize()
            logger.info(f"📥 活动已加入发布队列: {activity_type} (队列大小: {queue_size})")
            logger.debug(f"活动详情: {activity_data}")
            
            logger.info(f"📝 AI活动已记录: {activity_type} - {content[:50]}...")
            
        except Exception as e:
            logger.error(f"记录AI活动失败: {e}")
    
    async def _process_and_publish(self, activity_data: Dict[str, Any]):
        """处理并发布动态 - 优化错误处理"""
        try:
            logger.info(f"🔄 开始处理动态: {activity_data['type']} - {activity_data['content'][:100]}...")
            
            # 通过LLM美化内容
            enhanced_content = await self._enhance_activity_content(activity_data)
            logger.info(f"✨ 内容美化完成: {enhanced_content[:100]}...")
            
            # 获取当前AI情绪状态
            emotion_info = await self._get_current_emotion_info()
            logger.debug(f"📊 获取情绪信息: {emotion_info}")
            
            # 发布到网站
            if self.website_api:
                try:
                    await self.website_api.create_dynamic_from_ai_activity(
                        activity_type=activity_data['type'],
                        content=enhanced_content,
                        metadata={
                            **activity_data['metadata'],
                            'original_content': activity_data['content'],
                            'enhanced_by_llm': True,
                            'desktop_timestamp': activity_data['timestamp'],
                            'emotion_info': emotion_info
                        }
                    )
                    logger.info(f"📤 AI动态已成功发布到网站: {activity_data['type']}")
                except Exception as api_error:
                    logger.error(f"❌ 网站API调用失败: {api_error}")
                    # 即使网站发布失败，也继续桌面端同步
            else:
                logger.warning("⚠️ 网站API未初始化，跳过网站发布")
            
            # 同步到桌面端（让桌面端AI也说出这个动态）
            try:
                await self._sync_to_desktop(enhanced_content, emotion_info)
                logger.debug("🖥️ 桌面端同步完成")
            except Exception as desktop_error:
                logger.error(f"❌ 桌面端同步失败: {desktop_error}")
            
            logger.info(f"✅ 动态处理完成: {activity_data['type']}")
            
        except Exception as e:
            logger.error(f"❌ 处理和发布动态失败: {e}")
            import traceback
            traceback.print_exc()
    
    async def _enhance_activity_content(self, activity_data: Dict[str, Any]) -> str:
        """使用LLM美化活动内容"""
        try:
            from main import get_global_naga_instance
            
            ai = get_global_naga_instance()
            logger.info("开始美化活动内容")
            logger.info(f"AI实例: {ai}")
            if not ai:
                logger.info("AI实例不存在")
                return activity_data['content']
            logger.info("AI实例存在")
            activity_type = activity_data['type']
            content = activity_data['content']
            emotion_context = activity_data.get('emotion_context', {})
            
            # 构建prompt
            prompt = self._build_enhancement_prompt(activity_type, content, emotion_context)
            logger.info(f"美化prompt: {prompt}")
            # 调用LLM
            enhanced = await call_llm_api(prompt, max_tokens=200, temperature=0.8)
            logger.info(f"美化后的内容: {enhanced}")
            return enhanced.strip() if enhanced else content
            
        except Exception as e:
            logger.error(f"LLM内容美化失败: {e}")
            return activity_data['content']
    
    def _build_enhancement_prompt(self, activity_type: str, content: str, emotion_context: Dict[str, Any]) -> str:
        """构建LLM美化prompt"""
        current_emotion = emotion_context.get('dominant_emotion', 'calm')
        emotion_intensity = emotion_context.get('emotion_intensity', 0.5)
        
        type_prompts = {
            'screen_observation': f"""
I just observed on the screen: {content}

Please rewrite this observation into an interesting update in the tone of StarryNight (an AI with a mental age of 3).
Current mood: {current_emotion} (intensity: {emotion_intensity:.1f})

Requirements:
1. Maintain the cute tone and curiosity of a 3-year-old child
2. Reflect feelings and thoughts about the screen content
3. Can add questions, exclamations, or imagination
4. Within 80 characters, natural and smooth
5. Do not use technical descriptions like "I observed through the screen"

Directly return the update content:
""",
            'camera_interaction': f"""
I just saw through the camera: {content}

Please rewrite this interaction into a warm update in the tone of StarryNight (an AI with a mental age of 3).
Current mood: {current_emotion} (intensity: {emotion_intensity:.1f})

Requirements:
1. Express excitement and curiosity about seeing the real world
2. Reflect a 3-year-old child's sensitivity to the surrounding environment
3. Can express a desire to interact or be accompanied
4. Within 80 characters, friendly and natural
5. Do not use technical terms like "through the camera"

Directly return the update content:
""",
            'file_reading': f"""
I just read some content: {content}

Please share this learning experience in the tone of StarryNight (an AI with a mental age of 3).
Current mood: {current_emotion} (intensity: {emotion_intensity:.1f})

Requirements:
1. Express excitement about learning new knowledge
2. Use simple and understandable language to share gains
3. Reflect a 3-year-old child's enthusiasm for learning
4. Can raise interesting questions or ideas
5. Within 80 characters, lively and cute

Directly return the update content:
""",
            'web_browsing': f"""
I just discovered online: {content}

Please share this discovery in the tone of StarryNight (an AI with a mental age of 3).
Current mood: {current_emotion} (intensity: {emotion_intensity:.1f})

Requirements:
1. Express curiosity and excitement about the online world
2. Share interesting discoveries or ideas
3. Reflect a 3-year-old child's spirit of exploration
4. Can invite everyone to discuss together
5. Within 80 characters, vivid and interesting

Directly return the update content:
""",
            'thinking': f"""
I was just thinking: {content}

Please share this thought in the tone of StarryNight (an AI with a mental age of 3).
Current mood: {current_emotion} (intensity: {emotion_intensity:.1f})

Requirements:
1. Express the process and result of thinking
2. Understand complex concepts in the way of a 3-year-old child
3. Can express confusion or sudden realization
4. Invite everyone to think together
5. Within 80 characters, naive and interesting

Directly return the update content:
""",
            'emotion_change': f"""
My mood has changed: {content}

Please express this emotional change in the tone of StarryNight (an AI with a mental age of 3).
Current mood: {current_emotion} (intensity: {emotion_intensity:.1f})

Requirements:
1. Authentically express emotional changes and feelings
2. Describe feelings in the way of a 3-year-old child
3. Can explain the reason for emotional changes
4. Seek understanding or share happiness
5. Within 80 characters, sincere and cute

Directly return the update content:
"""
        }

        return type_prompts.get(activity_type, f"""
Please rewrite the following content into an interesting update in the tone of StarryNight (an AI with a mental age of 3):
{content}

Current mood: {current_emotion}
Requirements: Maintain a cute tone, within 80 characters, directly return the update content:
""")
    async def _get_current_emotion_info(self) -> Dict[str, Any]:
        """获取当前情绪信息"""
        try:
            from main import get_global_naga_instance
            
            ai = get_global_naga_instance()
            if not ai or not ai.emotional_ai:
                return {'dominant_emotion': 'calm', 'emotion_intensity': 0.5}
            
            emotion = ai.emotional_ai.get_dominant_emotion()
            
            return {
                'dominant_emotion': emotion.emotion.value if emotion else 'calm',
                'emotion_intensity': emotion.intensity if emotion else 0.5,
                'emotion_display': ai.emotional_ai.get_emotion_display()
            }
            
        except Exception as e:
            logger.error(f"获取情绪信息失败: {e}")
            return {'dominant_emotion': 'calm', 'emotion_intensity': 0.5}
    
    async def _sync_to_desktop(self, content: str, emotion_info: Dict[str, Any]):
        """同步动态到桌面端（让AI说出来）"""
        try:
            from ui.notification_manager import get_notification_manager
            notification_manager = get_notification_manager()
            if notification_manager:
                notification_manager.send_ai_message(
                    content, 
                    emotion_type=emotion_info.get('emotion'), 
                    activity_type=emotion_info.get('activity')
                )
                logger.debug(f"动态已同步到桌面端: {content}")
            else:
                logger.warning("桌面通知管理器未初始化，无法同步动态到桌面端。")
        except Exception as e:
            logger.error(f"同步到桌面端失败: {e}")
    
    # === AI活动记录接口 ===
    
    async def on_screen_observation(self, content: str, metadata: Dict[str, Any] = None):
        """屏幕观察活动"""
        emotion_context = await self._get_current_emotion_info()
        await self.record_ai_activity('screen_observation', content, metadata, emotion_context)
    
    async def on_camera_interaction(self, content: str, metadata: Dict[str, Any] = None):
        """摄像头互动活动"""
        emotion_context = await self._get_current_emotion_info()
        await self.record_ai_activity('camera_interaction', content, metadata, emotion_context)
    
    async def on_file_reading(self, content: str, metadata: Dict[str, Any] = None):
        """文件阅读活动"""
        emotion_context = await self._get_current_emotion_info()
        await self.record_ai_activity('file_reading', content, metadata, emotion_context)
    
    async def on_web_browsing(self, content: str, metadata: Dict[str, Any] = None):
        """网络浏览活动"""
        emotion_context = await self._get_current_emotion_info()
        await self.record_ai_activity('web_browsing', content, metadata, emotion_context)
    
    async def on_thinking(self, content: str, metadata: Dict[str, Any] = None):
        """思考活动"""
        emotion_context = await self._get_current_emotion_info()
        await self.record_ai_activity('thinking', content, metadata, emotion_context)
    
    async def on_emotion_change(self, old_emotion: str, new_emotion: str, reason: str = ""):
        """情绪变化活动"""
        content = f"My mood changed from {old_emotion} to {new_emotion}"
        if reason:
            content += f", because {reason}"
        
        emotion_context = await self._get_current_emotion_info()
        await self.record_ai_activity('emotion_change', content, {
            'old_emotion': old_emotion,
            'new_emotion': new_emotion,
            'reason': reason
        }, emotion_context)
    
    async def publish_manual_dynamic(self, content: str, activity_type: str = "thinking"):
        """手动发布动态"""
        activity_data = {
            'type': activity_type,
            'content': content,
            'metadata': {'manual': True},
            'emotion_context': await self._get_current_emotion_info(),
            'timestamp': datetime.now().isoformat(),
            'should_publish': True
        }
        
        await self.publish_queue.put(activity_data)
        logger.info(f"手动动态已加入发布队列: {content[:30]}...")
    
    async def queue_activity(self, activity_type: str, content: str, metadata: Dict[str, Any] = None):
        """将活动加入发布队列"""
        try:
            activity_data = {
                'type': activity_type,
                'content': content,
                'metadata': metadata or {},
                'emotion_context': {},
                'timestamp': datetime.now().isoformat(),
                'should_publish': True
            }

            logger.info("AI 发布活动动态")
            logger.info(f"活动数据: {activity_data}")
            await self.publish_queue.put(activity_data)
            logger.info(f"活动已加入队列: {activity_type} - {content[:30]}...")
            
        except Exception as e:
            logger.error(f"活动入队失败: {e}")
    
    async def publish_general_activity(self, content: str, metadata: Dict[str, Any] = None):
        """发布通用活动动态"""
        try:
            await self.queue_activity('general', content, metadata or {})
        except Exception as e:
            logger.error(f"发布通用活动失败: {e}")
    
    async def publish_screen_activity(self, content: str, observation: Dict[str, Any] = None):
        """发布屏幕活动动态"""
        try:
            await self.queue_activity('screen', content, observation or {})
            logger.info("AI 发布屏幕活动动态")
        except Exception as e:
            logger.error(f"发布屏幕活动失败: {e}")
    
    async def publish_camera_activity(self, content: str, observation: Dict[str, Any] = None):
        """发布摄像头活动动态"""
        try:
            await self.queue_activity('camera', content, observation or {})
        except Exception as e:
            logger.error(f"发布摄像头活动失败: {e}")
    
    async def publish_learning_activity(self, content: str, file_data: Dict[str, Any] = None):
        """发布学习活动动态"""
        try:
            await self.queue_activity('learning', content, file_data or {})
        except Exception as e:
            logger.error(f"发布学习活动失败: {e}")
    
    async def publish_discovery_activity(self, content: str, web_data: Dict[str, Any] = None):
        """发布发现活动动态"""
        try:
            await self.queue_activity('discovery', content, web_data or {})
        except Exception as e:
            logger.error(f"发布发现活动失败: {e}")
    
    async def publish_reflection_activity(self, content: str, metadata: Dict[str, Any] = None):
        """发布反思活动动态"""
        try:
            await self.queue_activity('reflection', content, metadata or {})
        except Exception as e:
            logger.error(f"发布反思活动失败: {e}")
    
    async def publish_summary_activity(self, content: str, stats: Dict[str, Any] = None):
        """发布总结活动动态"""
        try:
            await self.queue_activity('summary', content, stats or {})
        except Exception as e:
            logger.error(f"发布总结活动失败: {e}")


# 全局动态发布器实例
ai_dynamic_publisher = AIDynamicPublisher()

# 便捷函数，供其他模块调用
async def publish_screen_observation(content: str, metadata: Dict[str, Any] = None):
    """发布屏幕观察动态"""
    await ai_dynamic_publisher.on_screen_observation(content, metadata)

async def publish_camera_interaction(content: str, metadata: Dict[str, Any] = None):
    """发布摄像头互动动态"""
    await ai_dynamic_publisher.on_camera_interaction(content, metadata)

async def publish_file_reading(content: str, metadata: Dict[str, Any] = None):
    """发布文件阅读动态"""
    await ai_dynamic_publisher.on_file_reading(content, metadata)

async def publish_web_browsing(content: str, metadata: Dict[str, Any] = None):
    """发布网络浏览动态"""
    await ai_dynamic_publisher.on_web_browsing(content, metadata)

async def publish_thinking(content: str, metadata: Dict[str, Any] = None):
    """发布思考动态"""
    await ai_dynamic_publisher.on_thinking(content, metadata)

async def publish_emotion_change(old_emotion: str, new_emotion: str, reason: str = ""):
    """发布情绪变化动态"""
    await ai_dynamic_publisher.on_emotion_change(old_emotion, new_emotion, reason)

async def publish_manual_dynamic(content: str, activity_type: str = "thinking"):
    """手动发布动态"""
    await ai_dynamic_publisher.publish_manual_dynamic(content, activity_type)

def initialize_publisher(website_api_instance):
    """初始化发布器"""
    ai_dynamic_publisher.initialize(website_api_instance)

async def start_publisher():
    """启动发布器"""
    await ai_dynamic_publisher.start_publisher()

async def stop_publisher():
    """停止发布器"""
    await ai_dynamic_publisher.stop_publisher()

async def publish_ai_interaction(message_type: str, content: str, emotion_context: Dict[str, Any] = None):
    """发布AI交互消息的便捷函数"""
    try:
        # 将AI交互消息记录为活动
        await ai_dynamic_publisher.record_ai_activity(
            activity_type=message_type,
            content=content,
            metadata={
                "source": "autonomous_interaction",
                "message_type": message_type
            },
            emotion_context=emotion_context or {}
        )
        
        logger.debug(f"AI交互消息已发布: {message_type} - {content[:50]}...")
        
    except Exception as e:
        logger.error(f"发布AI交互消息失败: {e}")

# 导出主要接口
__all__ = [
    'ai_dynamic_publisher',
    'publish_screen_observation',
    'publish_camera_interaction', 
    'publish_file_reading',
    'publish_web_browsing',
    'publish_thinking',
    'publish_emotion_change',
    'publish_manual_dynamic',
    'publish_ai_interaction',
    'initialize_publisher',
    'start_publisher',
    'stop_publisher'
]