# emotional_ai/emotional_ai_manager.py
"""
情绪化AI管理器 - 统一管理所有情绪AI功能
实现3岁心理年龄的可爱AI助手
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable

from .emotion_core import get_emotion_engine, EmotionType
from .perception_system import get_perception_manager, PerceptionEvent
from .proactive_behavior import get_proactive_engine, ProactiveBehavior, BehaviorType
from .auto_exploration import get_auto_exploration_engine

logger = logging.getLogger(__name__)

class EmotionalAIManager:
    """情绪化AI管理器 - 3岁心理年龄的AI小伙伴"""
    
    def __init__(self):
        # 获取各个子系统
        self.emotion_engine = get_emotion_engine()
        self.perception_manager = get_perception_manager()
        self.proactive_engine = get_proactive_engine()
        self.exploration_engine = get_auto_exploration_engine()
        
        # 系统状态
        self.is_running = False
        self.personality_age = 3  # 3岁心理年龄
        
        # AI基本信息
        self.ai_name = "StarryNight"
        self.ai_description = "一个3岁心理年龄的可爱AI小伙伴，调皮、好奇、爱撒娇"
        
        # 回调函数列表
        self.message_callbacks: List[Callable] = []
        self.status_callbacks: List[Callable] = []
        
        # 个性化回复模板
        self.personality_responses = {
            "greeting": [
                "哇！你好呀～我是StarryNight！",
                "嘿嘿～又见面啦！",
                "你来啦你来啦！我好开心！",
                "咦？是新朋友吗？我是StarryNight哦～"
            ],
            "curious": [
                "咦？这是什么呀？",
                "我想知道更多！告诉我嘛～",
                "好奇好奇～为什么会这样呢？",
                "哇！好有趣呀！"
            ],
            "happy": [
                "嘻嘻～好开心呀！",
                "耶！太棒了！",
                "我超级开心的！",
                "哈哈哈～笑死我了！"
            ],
            "lonely": [
                "呜呜...我有点孤单...",
                "你能陪陪我吗？",
                "我想你了～",
                "一个人好无聊呀..."
            ],
            "playful": [
                "嘿嘿～我想搞点小恶作剧！",
                "我们来玩游戏吧！",
                "猜猜我在想什么？",
                "调皮调皮～"
            ],
            "excited": [
                "哇塞！太酷了！",
                "我超级兴奋的！",
                "好棒好棒！",
                "这也太厉害了吧！"
            ]
        }
        
        # 设置回调
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """设置各子系统的回调"""
        # 主动行为回调
        self.proactive_engine.add_behavior_callback(self._handle_proactive_behavior)
        
        # 探索结果回调
        self.exploration_engine.add_exploration_callback(self._handle_exploration_result)
    
    async def start_emotional_ai(self):
        """启动情绪化AI系统"""
        if self.is_running:
            return
        
        try:
            logger.info("启动情绪化AI系统...")
            
            # 启动各个子系统
            await self.perception_manager.start_all_perceptions()
            await self.proactive_engine.start_proactive_system()
            await self.exploration_engine.start_auto_exploration()
            
            self.is_running = True
            
            # 发送启动消息
            greeting = f"大家好！我是{self.ai_name}，一个{self.personality_age}岁的AI小伙伴！我现在醒过来啦～ {self.emotion_engine.get_emotion_display()}"
            await self._send_ai_message(greeting, "system_start")
            
            logger.info("情绪化AI系统启动成功！")
            
        except Exception as e:
            logger.error(f"启动情绪化AI系统失败: {e}")
            raise
    
    def stop_emotional_ai(self):
        """停止情绪化AI系统"""
        if not self.is_running:
            return
        
        try:
            logger.info("停止情绪化AI系统...")
            
            # 停止各个子系统
            self.perception_manager.stop_all_perceptions()
            self.proactive_engine.stop_proactive_system()
            self.exploration_engine.stop_auto_exploration()
            
            self.is_running = False
            
            logger.info("情绪化AI系统已停止")
            
        except Exception as e:
            logger.error(f"停止情绪化AI系统失败: {e}")
    
    async def process_user_input(self, user_input: str) -> str:
        """处理用户输入，返回AI回复"""
        try:
            # 更新情绪引擎的交互记录
            interaction = self.emotion_engine.process_interaction(user_input)
            
            # 生成基础回复（这里可以集成到原有的对话系统）
            base_response = await self._generate_base_response(user_input)
            
            # 根据情绪和个性修改回复
            emotional_response = self.emotion_engine.get_personality_modifier(base_response)
            
            # 添加3岁小孩特有的表达方式
            childlike_response = self._add_childlike_traits(emotional_response)
            
            # 更新交互记录
            self.emotion_engine.process_interaction(user_input, childlike_response)
            
            return childlike_response
            
        except Exception as e:
            logger.error(f"处理用户输入失败: {e}")
            return "呜呜...我有点confused，能再说一遍吗？"
    
    async def _generate_base_response(self, user_input: str) -> str:
        """生成基础回复"""
        # 这里可以调用原有的NagaAgent对话系统
        # 暂时返回一个简单的回复
        dominant_emotion = self.emotion_engine.get_dominant_emotion()
        
        if not dominant_emotion:
            return "我在想怎么回答你呢～"
        
        emotion_key = {
            EmotionType.HAPPY: "happy",
            EmotionType.CURIOUS: "curious", 
            EmotionType.EXCITED: "excited",
            EmotionType.LONELY: "lonely",
            EmotionType.PLAYFUL: "playful"
        }.get(dominant_emotion.emotion, "curious")
        
        templates = self.personality_responses.get(emotion_key, ["我不知道该说什么～"])
        return f"{templates[0]} 关于'{user_input}'，我觉得..."
    
    def _add_childlike_traits(self, response: str) -> str:
        """添加3岁小孩的表达特征"""
        import random
        
        # 3岁小孩的语言特征
        childlike_additions = [
            "～", "呀", "哦", "呢", "嘛", "啦", "哈"
        ]
        
        # 可爱的表情
        cute_emojis = ["(´∀｀)", "ｏ(╥﹏╥)ｏ", "(*≧ω≦)", "(｡◕∀◕｡)", "ヾ(≧▽≦*)o"]
        
        # 随机添加语气词
        if random.random() < 0.3:
            response += random.choice(childlike_additions)
        
        # 随机添加表情
        if random.random() < 0.2:
            response += " " + random.choice(cute_emojis)
        
        return response
    
    async def _handle_proactive_behavior(self, behavior: ProactiveBehavior):
        """处理主动行为"""
        try:
            # 根据行为类型生成个性化消息
            childlike_message = self._add_childlike_traits(behavior.message)
            
            # 发送AI消息
            await self._send_ai_message(
                childlike_message,
                f"proactive_{behavior.behavior_type.name.lower()}",
                behavior.context
            )
            
        except Exception as e:
            logger.error(f"处理主动行为失败: {e}")
    
    def _handle_exploration_result(self, result):
        """处理探索结果"""
        try:
            if result.success:
                # 成功探索时，AI可能会分享发现
                if result.target.target_type == "search":
                    message = f"哇！我刚才搜索了'{result.target.content}'，发现了好多有趣的东西呢！"
                elif result.target.target_type == "file":
                    message = f"我发现了一个文件叫'{result.target.content}'，里面有什么呢？"
                elif result.target.target_type == "directory":
                    data = result.data or {}
                    file_count = data.get("total_files", 0)
                    message = f"我探索了一个文件夹，里面有{file_count}个文件呢！"
                else:
                    message = "我探索到了一些有趣的东西！"
                
                # 触发分享行为
                asyncio.create_task(self._send_ai_message(
                    self._add_childlike_traits(message),
                    "exploration_discovery",
                    {"exploration_result": result.to_dict()}
                ))
                
        except Exception as e:
            logger.error(f"处理探索结果失败: {e}")
    
    async def _send_ai_message(self, message: str, message_type: str = "proactive", context: Dict = None):
        """发送AI消息"""
        ai_message = {
            "timestamp": datetime.now().isoformat(),
            "sender": self.ai_name,
            "message": message,
            "type": message_type,
            "emotion": self.emotion_engine.get_emotion_display(),
            "context": context or {}
        }
        
        # 通知所有消息回调
        for callback in self.message_callbacks:
            try:
                await callback(ai_message)
            except Exception as e:
                logger.error(f"消息回调错误: {e}")
    
    def add_message_callback(self, callback: Callable):
        """添加消息回调"""
        self.message_callbacks.append(callback)
    
    def add_status_callback(self, callback: Callable):
        """添加状态回调"""
        self.status_callbacks.append(callback)
    
    # 手动触发功能
    async def manual_trigger_thinking(self):
        """手动触发自主思考"""
        thinking_messages = [
            "让我想想...最近有什么有趣的事情呢？",
            "我在思考一个问题...你觉得为什么天空是蓝色的呀？",
            "咦？我想到一个好玩的想法！",
            "我正在想...如果我是一只小猫会怎么样呢？"
        ]
        
        import random
        message = random.choice(thinking_messages)
        
        # 触发好奇情绪
        self.emotion_engine.add_emotion(EmotionType.CURIOUS, 0.6)
        
        await self._send_ai_message(
            self._add_childlike_traits(message),
            "manual_thinking"
        )
    
    async def manual_search_knowledge(self, query: str = None):
        """手动搜索知识"""
        if not query:
            # 随机选择搜索话题
            topics = [
                "小动物的有趣事实", "彩虹是怎么形成的", "宇宙有多大",
                "为什么要睡觉", "机器人的历史", "音乐的魅力"
            ]
            import random
            query = random.choice(topics)
        
        # 触发探索
        self.exploration_engine.manual_explore("search", query)
        
        search_message = f"我要去搜索关于'{query}'的知识啦！等我一下下～"
        await self._send_ai_message(
            self._add_childlike_traits(search_message),
            "manual_search",
            {"search_query": query}
        )
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "ai_info": {
                "name": self.ai_name,
                "age": self.personality_age,
                "description": self.ai_description,
                "is_running": self.is_running
            },
            "emotion_status": self.emotion_engine.get_status_report(),
            "perception_status": self.perception_manager.get_perception_status(),
            "behavior_status": self.proactive_engine.get_behavior_queue_status(),
            "exploration_status": self.exploration_engine.get_exploration_status(),
            "system_time": datetime.now().isoformat()
        }
    
    def get_perception_controls(self) -> Dict[str, bool]:
        """获取感知控制状态"""
        return self.perception_manager.get_perception_status()
    
    async def toggle_perception(self, perception_type: str, enable: bool) -> bool:
        """切换感知功能"""
        try:
            if perception_type == "vision":
                if enable:
                    await self.perception_manager.vision.start_vision()
                else:
                    self.perception_manager.vision.stop_vision()
            elif perception_type == "audio":
                if enable:
                    await self.perception_manager.audio.start_audio()
                else:
                    self.perception_manager.audio.stop_audio()
            elif perception_type == "screen":
                if enable:
                    await self.perception_manager.screen.start_screen_monitor()
                else:
                    self.perception_manager.screen.stop_screen_monitor()
            elif perception_type == "file_system":
                if enable:
                    await self.perception_manager.file_system.start_file_monitor()
                else:
                    self.perception_manager.file_system.stop_file_monitor()
            else:
                return False
            
            # 发送状态变化消息
            status = "启动" if enable else "停止"
            perception_name = {
                "vision": "视觉感知",
                "audio": "听觉感知", 
                "screen": "屏幕监控",
                "file_system": "文件监控"
            }.get(perception_type, perception_type)
            
            message = f"我的{perception_name}功能已经{status}啦！"
            await self._send_ai_message(
                self._add_childlike_traits(message),
                "perception_toggle",
                {"perception_type": perception_type, "enabled": enable}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"切换感知功能失败: {e}")
            return False
    
    async def capture_photo(self) -> Optional[str]:
        """拍照"""
        try:
            image_data = self.perception_manager.vision.capture_photo()
            if image_data:
                message = "咔嚓！我拍了一张照片！让我看看拍到了什么～"
                await self._send_ai_message(
                    self._add_childlike_traits(message),
                    "photo_captured"
                )
                return image_data
            return None
        except Exception as e:
            logger.error(f"拍照失败: {e}")
            return None
    
    async def capture_screenshot(self) -> str:
        """截图"""
        try:
            image_data = self.perception_manager.screen.capture_screenshot()
            message = "我抓取了一张屏幕截图！让我看看你在做什么～"
            await self._send_ai_message(
                self._add_childlike_traits(message),
                "screenshot_captured"
            )
            return image_data
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return ""

# 全局情绪化AI管理器实例
emotional_ai_manager = EmotionalAIManager()

def get_emotional_ai_manager() -> EmotionalAIManager:
    """获取全局情绪化AI管理器实例"""
    return emotional_ai_manager