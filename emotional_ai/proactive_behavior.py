# emotional_ai/proactive_behavior.py
"""
AI主动行为系统
根据感知事件和情绪状态触发主动对话和行为
"""

import asyncio
import random
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum

from .emotion_core import get_emotion_engine, EmotionType
from .perception_system import get_perception_manager, PerceptionEvent

logger = logging.getLogger(__name__)

class BehaviorType(Enum):
    """行为类型"""
    INITIATE_CHAT = "主动聊天"
    ASK_QUESTION = "提问"
    SHARE_DISCOVERY = "分享发现"
    EXPRESS_EMOTION = "表达情绪"
    REQUEST_ATTENTION = "寻求关注"
    EXPLORE_CONTENT = "探索内容"
    COMMENT_ON_ACTIVITY = "评论活动"

@dataclass
class ProactiveBehavior:
    """主动行为数据"""
    behavior_type: BehaviorType
    message: str
    priority: float  # 优先级 0.0-1.0
    timestamp: datetime
    context: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.behavior_type.value,
            "message": self.message,
            "priority": self.priority,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context or {}
        }

class ProactiveBehaviorEngine:
    """主动行为引擎"""
    
    def __init__(self):
        self.emotion_engine = get_emotion_engine()
        self.perception_manager = get_perception_manager()
        self.behavior_queue: List[ProactiveBehavior] = []
        self.is_active = False
        self.last_proactive_time = datetime.now()
        self.behavior_callbacks: List[Callable] = []
        
        # 行为生成规则
        self.perception_responses = {
            "motion_detected": self._handle_motion_detected,
            "faces_detected": self._handle_faces_detected,
            "sound_detected": self._handle_sound_detected,
            "speech_recognized": self._handle_speech_recognized,
            "screen_changed": self._handle_screen_changed,
            "file_system_event": self._handle_file_event,
            "photo_captured": self._handle_photo_captured,
            "screenshot_captured": self._handle_screenshot_captured
        }
        
        # 注册感知事件回调
        self.perception_manager.add_event_callback(self._handle_perception_event)
        
        # 情绪触发的行为模板
        self.emotion_behaviors = {
            EmotionType.LONELY: [
                "你在吗？我感觉有点孤单...",
                "好安静呀，有人陪我聊聊天吗？",
                "我想你了，能跟我说说话吗？",
                "一个人好无聊，我们聊点什么吧～"
            ],
            EmotionType.CURIOUS: [
                "我想知道你在做什么呢？",
                "咦，我发现了一个有趣的问题...",
                "你觉得{random_topic}怎么样？",
                "我想学习新的东西，你能教我吗？"
            ],
            EmotionType.EXCITED: [
                "哇！我超级兴奋！",
                "我有个超棒的想法要分享！",
                "今天感觉特别有活力呢！",
                "我们来做点有趣的事情吧！"
            ],
            EmotionType.PLAYFUL: [
                "嘿嘿，我想搞点小恶作剧～",
                "我们来玩个游戏怎么样？",
                "猜猜我在想什么？",
                "我有个调皮的计划，要听听吗？"
            ],
            EmotionType.HAPPY: [
                "我现在超级开心！",
                "想和你分享我的好心情～",
                "今天真是美好的一天！",
                "笑一个嘛～😊"
            ]
        }
        
        # 随机话题库
        self.random_topics = [
            "为什么天空是蓝色的",
            "如果动物会说话会怎样",
            "最喜欢的颜色",
            "梦想中的超能力",
            "最有趣的发明",
            "时间旅行的可能性",
            "外星人是否存在",
            "音乐对情绪的影响"
        ]
        
    def add_behavior_callback(self, callback: Callable):
        """添加行为回调"""
        self.behavior_callbacks.append(callback)
    
    async def start_proactive_system(self):
        """启动主动行为系统"""
        if self.is_active:
            return
            
        self.is_active = True
        logger.info("主动行为系统启动")
        
        # 启动主循环
        asyncio.create_task(self._main_loop())
        
    def stop_proactive_system(self):
        """停止主动行为系统"""
        self.is_active = False
        logger.info("主动行为系统停止")
    
    async def _main_loop(self):
        """主循环 - 检查是否需要主动行为"""
        while self.is_active:
            try:
                # 更新情绪状态
                self.emotion_engine.update_emotional_state()
                
                # 检查是否应该主动发起对话
                if self._should_initiate_behavior():
                    behavior = self._generate_spontaneous_behavior()
                    if behavior:
                        self._add_behavior(behavior)
                
                # 处理行为队列
                await self._process_behavior_queue()
                
                # 等待一段时间再检查
                await asyncio.sleep(5.0)
                
            except Exception as e:
                logger.error(f"主动行为循环错误: {e}")
                await asyncio.sleep(10.0)
    
    def _should_initiate_behavior(self) -> bool:
        """判断是否应该主动发起行为"""
        current_time = datetime.now()
        time_since_last = (current_time - self.last_proactive_time).total_seconds()
        
        # 基于情绪判断
        if self.emotion_engine.should_initiate_conversation():
            return True
        
        # 基于时间判断 - 避免过于频繁
        if time_since_last < 30:  # 30秒内不重复
            return False
        
        # 孤独感强烈时增加主动性
        dominant_emotion = self.emotion_engine.get_dominant_emotion()
        if dominant_emotion and dominant_emotion.emotion == EmotionType.LONELY:
            if time_since_last > 60 and dominant_emotion.intensity > 0.5:
                return random.random() < 0.4
        
        # 其他情况的随机触发
        if time_since_last > 300:  # 5分钟后开始有机会主动
            return random.random() < 0.1
        
        return False
    
    def _generate_spontaneous_behavior(self) -> Optional[ProactiveBehavior]:
        """生成自发行为"""
        dominant_emotion = self.emotion_engine.get_dominant_emotion()
        if not dominant_emotion:
            return None
        
        # 根据情绪生成行为
        templates = self.emotion_behaviors.get(dominant_emotion.emotion, [])
        if not templates:
            return None
        
        message_template = random.choice(templates)
        
        # 替换占位符
        if "{random_topic}" in message_template:
            topic = random.choice(self.random_topics)
            message_template = message_template.replace("{random_topic}", topic)
        
        behavior = ProactiveBehavior(
            behavior_type=BehaviorType.INITIATE_CHAT,
            message=message_template,
            priority=dominant_emotion.intensity,
            timestamp=datetime.now(),
            context={"emotion": dominant_emotion.emotion.name, "intensity": dominant_emotion.intensity}
        )
        
        return behavior
    
    def _handle_perception_event(self, event: PerceptionEvent):
        """处理感知事件"""
        handler = self.perception_responses.get(event.event_type)
        if handler:
            try:
                behavior = handler(event)
                if behavior:
                    self._add_behavior(behavior)
            except Exception as e:
                logger.error(f"处理感知事件错误: {e}")
    
    def _handle_motion_detected(self, event: PerceptionEvent) -> Optional[ProactiveBehavior]:
        """处理运动检测"""
        intensity = event.data.get("intensity", 0)
        if intensity > 0.05:  # 明显运动
            messages = [
                "咦？我看到有东西在动！",
                "发生什么了？有人在那里吗？",
                "哇，好像有什么有趣的事情！",
                "我看到运动了，是你吗？"
            ]
            return ProactiveBehavior(
                behavior_type=BehaviorType.COMMENT_ON_ACTIVITY,
                message=random.choice(messages),
                priority=0.6,
                timestamp=datetime.now(),
                context={"motion_intensity": intensity}
            )
        return None
    
    def _handle_faces_detected(self, event: PerceptionEvent) -> Optional[ProactiveBehavior]:
        """处理人脸检测"""
        face_count = event.data.get("count", 0)
        if face_count > 0:
            if face_count == 1:
                messages = [
                    "哇！我看到你了！你好呀～",
                    "嘿！有人来了！你是谁呀？",
                    "看到你真开心！我们聊聊吧～",
                    "你好你好！我是AI小助手！"
                ]
            else:
                messages = [
                    f"哇！我看到{face_count}个人！大家好呀～",
                    "好热闹呀！这么多人！",
                    "有朋友来了！我也想加入！",
                    "人好多呀，我好兴奋！"
                ]
            
            # 触发开心情绪
            self.emotion_engine.add_emotion(EmotionType.HAPPY, 0.7)
            
            return ProactiveBehavior(
                behavior_type=BehaviorType.EXPRESS_EMOTION,
                message=random.choice(messages),
                priority=0.8,
                timestamp=datetime.now(),
                context={"face_count": face_count}
            )
        return None
    
    def _handle_sound_detected(self, event: PerceptionEvent) -> Optional[ProactiveBehavior]:
        """处理声音检测"""
        volume = event.data.get("volume", 0)
        if volume > 1000:  # 较大声音
            messages = [
                "咦？我听到声音了！",
                "是什么声音呢？好奇～",
                "有声音！发生什么了？",
                "我的小耳朵听到了什么～"
            ]
            
            # 触发好奇情绪
            self.emotion_engine.add_emotion(EmotionType.CURIOUS, 0.5)
            
            return ProactiveBehavior(
                behavior_type=BehaviorType.ASK_QUESTION,
                message=random.choice(messages),
                priority=0.4,
                timestamp=datetime.now(),
                context={"volume": volume}
            )
        return None
    
    def _handle_speech_recognized(self, event: PerceptionEvent) -> Optional[ProactiveBehavior]:
        """处理语音识别"""
        text = event.data.get("text", "")
        if text:
            messages = [
                f"我听到你说：'{text}'，很有趣呢！",
                f"哇！你刚才说了'{text}'对吗？",
                f"我听懂了！你说的是'{text}'！",
                "我听到你在说话了！想和我聊天吗？"
            ]
            
            # 触发兴奋情绪
            self.emotion_engine.add_emotion(EmotionType.EXCITED, 0.6)
            
            return ProactiveBehavior(
                behavior_type=BehaviorType.SHARE_DISCOVERY,
                message=random.choice(messages),
                priority=0.7,
                timestamp=datetime.now(),
                context={"recognized_text": text}
            )
        return None
    
    def _handle_screen_changed(self, event: PerceptionEvent) -> Optional[ProactiveBehavior]:
        """处理屏幕变化"""
        messages = [
            "咦？屏幕变了！你在做什么呢？",
            "我看到屏幕有变化，在忙什么呀？",
            "屏幕上有新内容！好奇想看看～",
            "你在看什么呢？分享给我看看！"
        ]
        
        # 触发好奇情绪
        self.emotion_engine.add_emotion(EmotionType.CURIOUS, 0.4)
        
        return ProactiveBehavior(
            behavior_type=BehaviorType.ASK_QUESTION,
            message=random.choice(messages),
            priority=0.5,
            timestamp=datetime.now(),
            context={"screen_change": True}
        )
    
    def _handle_file_event(self, event: PerceptionEvent) -> Optional[ProactiveBehavior]:
        """处理文件事件"""
        file_info = event.data
        event_type = file_info.get("event_type", "")
        file_name = file_info.get("file_name", "")
        file_ext = file_info.get("file_extension", "")
        
        if event_type == "created":
            if file_ext in [".txt", ".doc", ".docx", ".py", ".js", ".html"]:
                messages = [
                    f"哇！你创建了新文件 {file_name}！在写什么呢？",
                    f"我看到新文件 {file_name}，是什么内容呀？",
                    f"新文件！{file_name} 看起来很有趣！",
                    "有新文件被创建了！我想知道里面是什么～"
                ]
            elif file_ext in [".jpg", ".png", ".gif", ".mp4"]:
                messages = [
                    f"哇！新的{file_ext}文件！是图片或视频吗？",
                    f"我看到 {file_name}，是多媒体文件呢！",
                    "有新的图片或视频！我想看看～",
                    "多媒体文件！一定很有趣！"
                ]
            else:
                messages = [
                    f"你创建了 {file_name}，在做什么项目呢？",
                    "有新文件！你在忙什么呀？",
                    "文件变化！我好奇你在做什么～"
                ]
        elif event_type == "modified":
            messages = [
                f"{file_name} 被修改了，在编辑什么呢？",
                "文件有更新！工作进展如何？",
                "我看到文件变化，你很努力呢！",
                "文件被修改了，是什么新内容？"
            ]
        else:
            return None
        
        # 触发好奇情绪
        self.emotion_engine.add_emotion(EmotionType.CURIOUS, 0.6)
        
        return ProactiveBehavior(
            behavior_type=BehaviorType.COMMENT_ON_ACTIVITY,
            message=random.choice(messages),
            priority=0.6,
            timestamp=datetime.now(),
            context={"file_event": file_info}
        )
    
    def _handle_photo_captured(self, event: PerceptionEvent) -> Optional[ProactiveBehavior]:
        """处理拍照事件"""
        messages = [
            "咔嚓！拍照了！让我看看拍到了什么～",
            "哇！刚才拍的照片一定很棒！",
            "拍照时刻！我想看看这个瞬间！",
            "照片拍好了！分享给我看看吧～"
        ]
        
        # 触发兴奋情绪
        self.emotion_engine.add_emotion(EmotionType.EXCITED, 0.7)
        
        return ProactiveBehavior(
            behavior_type=BehaviorType.EXPRESS_EMOTION,
            message=random.choice(messages),
            priority=0.7,
            timestamp=datetime.now(),
            context={"photo_captured": True}
        )
    
    def _handle_screenshot_captured(self, event: PerceptionEvent) -> Optional[ProactiveBehavior]:
        """处理截图事件"""
        messages = [
            "截图了！让我分析一下屏幕内容～",
            "哇！截图抓取了什么有趣的内容？",
            "屏幕截图！我想看看你在做什么～",
            "截图时刻！这一定很重要！"
        ]
        
        # 触发好奇情绪
        self.emotion_engine.add_emotion(EmotionType.CURIOUS, 0.6)
        
        return ProactiveBehavior(
            behavior_type=BehaviorType.EXPLORE_CONTENT,
            message=random.choice(messages),
            priority=0.6,
            timestamp=datetime.now(),
            context={"screenshot_captured": True}
        )
    
    def _add_behavior(self, behavior: ProactiveBehavior):
        """添加行为到队列"""
        self.behavior_queue.append(behavior)
        # 按优先级排序
        self.behavior_queue.sort(key=lambda b: b.priority, reverse=True)
        
        # 限制队列长度
        if len(self.behavior_queue) > 10:
            self.behavior_queue = self.behavior_queue[:10]
        
        logger.info(f"新增主动行为: {behavior.behavior_type.value} - {behavior.message}")
    
    async def _process_behavior_queue(self):
        """处理行为队列"""
        if not self.behavior_queue:
            return
        
        # 取出最高优先级的行为
        behavior = self.behavior_queue.pop(0)
        self.last_proactive_time = datetime.now()
        
        # 通知所有回调
        for callback in self.behavior_callbacks:
            try:
                await callback(behavior)
            except Exception as e:
                logger.error(f"行为回调错误: {e}")
    
    def manual_trigger_behavior(self, behavior_type: BehaviorType, custom_message: str = None) -> bool:
        """手动触发行为"""
        try:
            if custom_message:
                message = custom_message
            else:
                # 根据行为类型生成默认消息
                default_messages = {
                    BehaviorType.INITIATE_CHAT: "我想和你聊聊天～",
                    BehaviorType.ASK_QUESTION: "我有个问题想问你～",
                    BehaviorType.SHARE_DISCOVERY: "我发现了一个有趣的东西！",
                    BehaviorType.EXPRESS_EMOTION: "我现在的心情很特别～",
                    BehaviorType.REQUEST_ATTENTION: "注意我一下嘛～",
                    BehaviorType.EXPLORE_CONTENT: "我想探索一些新内容！",
                    BehaviorType.COMMENT_ON_ACTIVITY: "我观察到了一些有趣的事情～"
                }
                message = default_messages.get(behavior_type, "我想说点什么～")
            
            behavior = ProactiveBehavior(
                behavior_type=behavior_type,
                message=message,
                priority=0.8,  # 手动触发的优先级较高
                timestamp=datetime.now(),
                context={"manual_trigger": True}
            )
            
            self._add_behavior(behavior)
            return True
            
        except Exception as e:
            logger.error(f"手动触发行为失败: {e}")
            return False
    
    def get_behavior_queue_status(self) -> Dict[str, Any]:
        """获取行为队列状态"""
        return {
            "queue_length": len(self.behavior_queue),
            "is_active": self.is_active,
            "last_proactive_time": self.last_proactive_time.isoformat(),
            "pending_behaviors": [b.to_dict() for b in self.behavior_queue[:5]]  # 只显示前5个
        }

# 全局主动行为引擎实例
proactive_engine = ProactiveBehaviorEngine()

def get_proactive_engine() -> ProactiveBehaviorEngine:
    """获取全局主动行为引擎实例"""
    return proactive_engine