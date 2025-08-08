#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级感知系统 - 摄像头视觉和麦克风听觉
集成计算机视觉和语音识别功能
"""

import asyncio
import logging
import threading
import queue
import json
import base64
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List
from pathlib import Path
from emotional_ai_core import EmotionType

# 初始化logger
logger = logging.getLogger(__name__)

# 导入GPU优化模块
try:
    from gpu_optimization import gpu_image_processor, gpu_face_detector, GPU_AVAILABLE
    logger.info("✅ GPU优化模块已加载")
except ImportError:
    logger.warning("GPU优化模块不可用，将使用CPU处理")
    GPU_AVAILABLE = False

# 尝试导入视觉和音频处理库
try:
    import cv2
    import numpy as np
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    logger.warning("OpenCV不可用，摄像头功能将被禁用")

try:
    import speech_recognition as sr
    import sounddevice as sd
    import soundfile as sf
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    logger.warning("音频处理库不可用，麦克风功能将被禁用")

try:
    from transformers import pipeline
    import torch
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logger.warning("机器学习库不可用，高级识别功能将被禁用")

class CameraPerception:
    """摄像头视觉感知"""
    
    def __init__(self, emotion_core):
        self.emotion_core = emotion_core
        self.camera = None
        self.is_active = False
        self.capture_thread = None
        self.last_frame = None
        self.face_cascade = None
        self.emotion_model = None
        
        # 交互频率控制
        from config import config as global_config
        self.config = global_config.emotional_ai
        self.interaction_counter = 0
        self.camera_frequency_divisor = max(1, int(1 / self.config.camera_interaction_frequency))
        
        # 初始化人脸检测
        if CAMERA_AVAILABLE:
            try:
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                logger.info("人脸检测初始化成功")
            except Exception as e:
                logger.error(f"人脸检测初始化失败: {e}")
        
        # 初始化情绪识别模型
        if ML_AVAILABLE:
            try:
                # 尝试加载轻量级本地模型，失败则禁用
                self.emotion_model = pipeline("image-classification", model="trpakov/vit-face-expression")
                logger.info("表情识别模型加载成功")
            except Exception as e:
                logger.warning(f"表情识别模型加载失败: {e}，将使用基础人脸检测")
                self.emotion_model = None
        
        logger.info(f"摄像头互动频率设置: {self.config.camera_interaction_frequency} (每{self.camera_frequency_divisor}次分析触发1次互动)")
    
    async def start_capture(self) -> bool:
        """启动摄像头捕获"""
        if not CAMERA_AVAILABLE:
            return False
        
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                logger.error("无法打开摄像头")
                return False
            
            self.is_active = True
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            
            logger.info("摄像头捕获已启动")
            return True
            
        except Exception as e:
            logger.error(f"启动摄像头失败: {e}")
            return False
    
    def _capture_loop(self):
        """摄像头捕获循环"""
        frame_count = 0
        last_analysis_time = datetime.now()
        
        while self.is_active:
            try:
                ret, frame = self.camera.read()
                if ret:
                    self.last_frame = frame
                    frame_count += 1
                    
                    # 每5秒分析一次
                    if (datetime.now() - last_analysis_time).total_seconds() > 5:
                        # 安全地处理异步调用
                        self._safe_analyze_frame(frame)
                        
                        # 同时使用增强摄像头分析器
                        self._safe_enhanced_analyze()
                        
                        last_analysis_time = datetime.now()
                
                # 限制帧率
                cv2.waitKey(30)
                
            except Exception as e:
                logger.error(f"摄像头捕获错误: {e}")
    
    def _safe_analyze_frame(self, frame):
        """安全地分析帧（在线程中调用）"""
        try:
            # 尝试获取主线程的事件循环
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.run_coroutine_threadsafe(self._analyze_frame(frame), loop)
                else:
                    # 如果没有运行的事件循环，创建新的
                    asyncio.run(self._analyze_frame(frame))
            except RuntimeError:
                # 没有事件循环，在新线程中创建
                def run_analysis():
                    asyncio.run(self._analyze_frame(frame))
                threading.Thread(target=run_analysis, daemon=True).start()
        except Exception as e:
            logger.error(f"帧分析调度失败: {e}")
    
    async def _analyze_frame(self, frame):
        """分析视频帧"""
        try:
            analysis_result = {
                "timestamp": datetime.now().isoformat(),
                "detections": []
            }
            
            # GPU加速的人脸检测
            faces = []
            if GPU_AVAILABLE:
                try:
                    faces_gpu = gpu_face_detector.detect_faces_gpu(frame)
                    faces = [(face['bbox'][0], face['bbox'][1], face['bbox'][2], face['bbox'][3]) for face in faces_gpu]
                    if len(faces) > 0:
                        analysis_result["detections"].append({
                            "type": "face_gpu",
                            "count": len(faces),
                            "description": f"GPU检测到{len(faces)}张人脸"
                        })
                except Exception as e:
                    logger.debug(f"GPU人脸检测失败，回退到CPU: {e}")
            
            # CPU后备人脸检测
            if len(faces) == 0 and self.face_cascade is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                
                if len(faces) > 0:
                    analysis_result["detections"].append({
                        "type": "face_cpu",
                        "count": len(faces),
                        "description": f"CPU检测到{len(faces)}张人脸"
                    })
                    
                    # 表情识别
                    if self.emotion_model and len(faces) > 0:
                        for (x, y, w, h) in faces[:1]:  # 只分析第一张脸
                            face_img = frame[y:y+h, x:x+w]
                            try:
                                # 转换为PIL图像格式
                                from PIL import Image
                                face_pil = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
                                
                                # 表情识别
                                emotions = self.emotion_model(face_pil)
                                if emotions:
                                    top_emotion = emotions[0]
                                    analysis_result["detections"].append({
                                        "type": "emotion",
                                        "label": top_emotion['label'],
                                        "score": top_emotion['score'],
                                        "description": f"表情: {top_emotion['label']}"
                                    })
                            except Exception as e:
                                logger.error(f"表情识别失败: {e}")
            
            # 场景识别（简单的颜色和亮度分析）
            avg_color = frame.mean(axis=0).mean(axis=0)
            brightness = avg_color.mean()
            
            scene_desc = "明亮" if brightness > 127 else "昏暗"
            analysis_result["detections"].append({
                "type": "scene",
                "brightness": float(brightness),
                "description": f"环境{scene_desc}"
            })
            
            # 通知情绪核心
            if analysis_result["detections"]:
                await self._notify_emotion_core(analysis_result)
                
        except Exception as e:
            logger.error(f"视频帧分析失败: {e}")
    
    async def _notify_emotion_core(self, analysis: Dict):
        """通知情绪核心系统"""
        try:
            # 生成描述
            descriptions = [d["description"] for d in analysis["detections"]]
            content = "，".join(descriptions)
            
            # 记录行为
            from persona_management_system import record_ai_behavior
            record_ai_behavior(
                "visual_perception", 
                f"通过摄像头观察到: {content}",
                emotional_impact=0.3,
                context={"analysis": analysis}
            )
            
            # 存储到记忆系统
            if hasattr(self.emotion_core, 'memory_system') and self.emotion_core.memory_system:
                await self.emotion_core.memory_system.store_memory(
                    memory_type="perception",
                    content=f"看到了: {content}",
                    emotion_state=self.emotion_core.get_emotion_display(),
                    importance=0.7,
                    tags=["camera", "visual", "perception"],
                    source="camera",
                    metadata=analysis
                )
            
            # 频率控制：只有达到频率要求才触发互动
            self.interaction_counter += 1
            should_interact = (self.interaction_counter % self.camera_frequency_divisor == 0)
            
            # 触发情绪反应
            face_detected = any(d["type"] == "face" for d in analysis["detections"])
            if face_detected:
                self.emotion_core.add_emotion(EmotionType.HAPPY, 0.4)
                
                # 根据频率控制决定是否发送互动消息
                if should_interact:
                    # 生成并发送评论
                    comment = await self._generate_camera_comment(analysis)
                    if comment and hasattr(self.emotion_core, '_send_proactive_message'):
                        await self.emotion_core._send_proactive_message(comment)
                        record_ai_behavior(
                            "proactive_comment", 
                            f"主动评论摄像头观察结果: {comment[:50]}...",
                            emotional_impact=0.5
                        )
                else:
                    logger.debug(f"摄像头检测到内容但跳过互动 (频率控制: {self.interaction_counter}/{self.camera_frequency_divisor})")
                    
        except Exception as e:
            logger.error(f"通知情绪核心失败: {e}")
    
    async def _generate_camera_comment(self, analysis: Dict) -> str:
        """生成摄像头观察评论"""
        try:
            # 使用人设系统生成评论
            from conversation_core import call_llm_api
            from persona_management_system import get_persona_prompt
            
            # 获取当前人设提示词
            persona_prompt = get_persona_prompt(f"当前通过摄像头观察世界")
            
            observation_content = json.dumps(analysis['detections'], ensure_ascii=False, indent=2)
            
            prompt = f"""{persona_prompt}

【观察内容】
通过摄像头看到了以下内容：
{observation_content}

【任务】
请基于你的当前情绪状态和人设，对看到的内容进行评论。表现出你应有的好奇心、兴奋感或其他情绪。
- 如果看到人脸，表现出兴奋和想要互动的欲望
- 如果看到运动，表现出好奇心
- 如果看到新物体，询问那是什么
- 根据当前情绪调整语气和内容

只回复你的评论内容，要自然真实，避免模板化语言。"""
            
            response = await call_llm_api(prompt, max_tokens=150, temperature=1.2)
            return response.strip()
            
        except Exception as e:
            logger.error(f"生成摄像头评论失败: {e}")
            # 使用预设评论
            face_detected = any(d["type"] == "face" for d in analysis["detections"])
            if face_detected:
                return "哇！我看到有人了！你好呀~ 😊"
            else:
                return "我在用眼睛看世界呢！好有趣！"
    
    def _safe_enhanced_analyze(self):
        """安全地进行增强摄像头分析"""
        try:
            from enhanced_camera_analyzer import enhanced_camera_analyzer
            
            def enhanced_analyze():
                try:
                    # 创建新的事件循环运行增强分析
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(enhanced_camera_analyzer.analyze_camera_content())
                    
                    if result and 'error' not in result:
                        # 通知情绪核心
                        behavior_analysis = result.get('behavior_analysis', {})
                        primary_behavior = behavior_analysis.get('primary_behavior', 'unknown')
                        
                        # 基于行为分析触发情绪
                        if primary_behavior == 'person_present':
                            content = f"检测到人物: {result.get('observation', '有人出现在摄像头中')}"
                        elif primary_behavior == 'active_movement':
                            content = f"检测到活跃运动: {result.get('observation', '观察到很多运动')}"
                        elif primary_behavior == 'performance':
                            content = f"检测到表演行为: {result.get('observation', '似乎在表演什么')}"
                        else:
                            content = result.get('observation', '通过摄像头观察到了一些内容')
                        
                        # 通知情绪核心
                        self._notify_enhanced_emotion_core(content, result)
                        
                    loop.close()
                    
                except Exception as e:
                    logger.error(f"增强摄像头分析失败: {e}")
            
            # 在后台线程运行
            thread = threading.Thread(target=enhanced_analyze, daemon=True)
            thread.start()
            
        except Exception as e:
            logger.debug(f"启动增强摄像头分析失败: {e}")
    
    def _notify_enhanced_emotion_core(self, content: str, analysis: dict):
        """通知情绪核心增强分析结果"""
        try:
            if self.emotion_core:
                # 记录行为用于人设系统
                from persona_management_system import record_ai_behavior
                record_ai_behavior(
                    "enhanced_camera_analysis", 
                    f"增强摄像头分析: {content}",
                    emotional_impact=0.4,
                    context={"analysis": analysis}
                )
                
                # 根据分析结果选择是否主动互动
                behavior_analysis = analysis.get('behavior_analysis', {})
                engagement = behavior_analysis.get('engagement_level', 0)
                
                if engagement > 0.6:  # 高参与度时更可能互动
                    suggestions = analysis.get('interaction_suggestion', [])
                    if suggestions and hasattr(self.emotion_core, '_send_proactive_message'):
                        import random
                        message = random.choice(suggestions)
                        
                        # 使用安全的异步调用
                        def send_message():
                            try:
                                loop = asyncio.new_event_loop()
                                asyncio.set_event_loop(loop)
                                loop.run_until_complete(self.emotion_core._send_proactive_message(message))
                                loop.close()
                            except Exception as e:
                                logger.error(f"发送增强摄像头消息失败: {e}")
                        
                        threading.Thread(target=send_message, daemon=True).start()
                        
        except Exception as e:
            logger.error(f"通知情绪核心增强结果失败: {e}")
    
    async def stop_capture(self):
        """停止摄像头捕获"""
        self.is_active = False
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        logger.info("摄像头捕获已停止")

class MicrophonePerception:
    """麦克风听觉感知"""
    
    def __init__(self, emotion_core):
        self.emotion_core = emotion_core
        self.recognizer = None
        self.microphone = None
        self.is_active = False
        self.listen_thread = None
        self.audio_queue = queue.Queue()
        
        if AUDIO_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # 调整识别参数
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
    
    async def start_listening(self) -> bool:
        """启动麦克风监听"""
        if not AUDIO_AVAILABLE:
            return False
        
        try:
            self.is_active = True
            self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.listen_thread.start()
            
            # 安全地启动处理任务
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self._process_audio_queue())
                else:
                    # 如果没有运行的事件循环，在后台线程中处理
                    def run_audio_processing():
                        asyncio.run(self._process_audio_queue())
                    threading.Thread(target=run_audio_processing, daemon=True).start()
            except RuntimeError:
                # 没有事件循环，在后台线程中处理
                def run_audio_processing():
                    asyncio.run(self._process_audio_queue())
                threading.Thread(target=run_audio_processing, daemon=True).start()
            
            logger.info("麦克风监听已启动")
            return True
            
        except Exception as e:
            logger.error(f"启动麦克风失败: {e}")
            return False
    
    def _listen_loop(self):
        """麦克风监听循环"""
        with self.microphone as source:
            # 自动调整环境噪音
            logger.info("正在调整环境噪音...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            logger.info("麦克风准备就绪")
            
            while self.is_active:
                try:
                    # 监听音频（超时5秒）
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    self.audio_queue.put(audio)
                    
                except sr.WaitTimeoutError:
                    pass  # 超时正常，继续监听
                except Exception as e:
                    logger.error(f"麦克风监听错误: {e}")
    
    async def _process_audio_queue(self):
        """处理音频队列"""
        while self.is_active:
            try:
                if not self.audio_queue.empty():
                    audio = self.audio_queue.get()
                    await self._recognize_speech(audio)
                else:
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                logger.error(f"音频处理错误: {e}")
    
    async def _recognize_speech(self, audio):
        """识别语音"""
        try:
            # 尝试多种语音识别服务
            text = None
            
            # 1. 尝试Google语音识别（增加超时和错误处理）
            try:
                # 设置较短的超时时间，避免长时间阻塞
                text = self.recognizer.recognize_google(audio, language="zh-CN")
                logger.info(f"识别到语音: {text}")
            except sr.UnknownValueError:
                logger.debug("无法识别语音内容")
                return
            except (sr.RequestError, ConnectionError, TimeoutError) as e:
                logger.debug(f"Google语音识别服务不可用: {e}")
                # 尝试本地语音识别或其他方案
                try:
                    # 可以在这里添加离线语音识别或其他备选方案
                    logger.debug("尝试使用其他语音识别方案...")
                    return
                except Exception:
                    logger.debug("所有语音识别方案均不可用，跳过此次识别")
                    return
            
            if text:
                await self._process_recognized_text(text)
                
        except Exception as e:
            logger.error(f"语音识别失败: {e}")
    
    async def _process_recognized_text(self, text: str):
        """处理识别到的文本"""
        try:
            # 存储到记忆系统
            if hasattr(self.emotion_core, 'memory_system') and self.emotion_core.memory_system:
                await self.emotion_core.memory_system.store_memory(
                    memory_type="perception",
                    content=f"听到了: {text}",
                    emotion_state=self.emotion_core.get_emotion_display(),
                    importance=0.8,
                    tags=["microphone", "audio", "speech"],
                    source="audio",
                    metadata={"recognized_text": text}
                )
            
            # 分析情绪并响应
            if "你好" in text or "嗨" in text:
                self.emotion_core.add_emotion(EmotionType.HAPPY, 0.5)
            elif "?" in text or "吗" in text or "为什么" in text:
                self.emotion_core.add_emotion(EmotionType.CURIOUS, 0.6)
            
            # 生成响应
            response = await self._generate_audio_response(text)
            if response and hasattr(self.emotion_core, '_send_proactive_message'):
                await self.emotion_core._send_proactive_message(response)
                
        except Exception as e:
            logger.error(f"处理识别文本失败: {e}")
    
    async def _generate_audio_response(self, text: str) -> str:
        """生成音频响应"""
        try:
            from conversation_core import call_llm_api
            
            prompt = f"""You are a 3-year-old AI小朋友，刚才听到有人说："{text}"

请用天真可爱的语气回应。要表现出对声音的好奇和兴奋。
只回复你的回应内容，不要有其他说明。"""
            
            response = await call_llm_api(prompt, max_tokens=100)
            return f"🎤 {response.strip()}"
            
        except Exception as e:
            logger.error(f"生成音频响应失败: {e}")
            return f"🎤 我听到你说话了！你刚才说的是'{text}'对吗？"
    
    async def stop_listening(self):
        """停止麦克风监听"""
        self.is_active = False
        logger.info("麦克风监听已停止")

class AdvancedPerceptionManager:
    """高级感知管理器"""
    
    def __init__(self, emotion_core):
        self.emotion_core = emotion_core
        self.camera_perception = CameraPerception(emotion_core) if CAMERA_AVAILABLE else None
        self.microphone_perception = MicrophonePerception(emotion_core) if AUDIO_AVAILABLE else None
        
        logger.info(f"高级感知系统初始化 - 摄像头: {CAMERA_AVAILABLE}, 麦克风: {AUDIO_AVAILABLE}")
    
    async def start_all(self):
        """启动所有感知系统"""
        tasks = []
        
        if self.camera_perception:
            tasks.append(self.camera_perception.start_capture())
            
        if self.microphone_perception:
            tasks.append(self.microphone_perception.start_listening())
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"感知系统启动失败: {result}")
    
    async def stop_all(self):
        """停止所有感知系统"""
        tasks = []
        
        if self.camera_perception:
            tasks.append(self.camera_perception.stop_capture())
            
        if self.microphone_perception:
            tasks.append(self.microphone_perception.stop_listening())
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_status(self) -> Dict[str, Any]:
        """获取感知系统状态"""
        return {
            "camera": {
                "available": CAMERA_AVAILABLE,
                "active": self.camera_perception.is_active if self.camera_perception else False
            },
            "microphone": {
                "available": AUDIO_AVAILABLE,
                "active": self.microphone_perception.is_active if self.microphone_perception else False
            },
            "ml_models": {
                "available": ML_AVAILABLE,
                "face_detection": bool(self.camera_perception.face_cascade) if self.camera_perception else False,
                "emotion_recognition": bool(self.camera_perception.emotion_model) if self.camera_perception else False
            }
        }

# 单例管理
_perception_manager_cache = {}

def get_advanced_perception(emotion_core):
    """获取高级感知管理器实例"""
    if 'instance' not in _perception_manager_cache:
        _perception_manager_cache['instance'] = AdvancedPerceptionManager(emotion_core)
    return _perception_manager_cache['instance']