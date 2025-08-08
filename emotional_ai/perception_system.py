# emotional_ai/perception_system.py
"""
AI感知系统 - 视觉、听觉、屏幕监控、文件监控
让AI能够感知外界环境并主动反应
"""

import asyncio
import cv2
import numpy as np
import pyaudio
import wave
import io
import threading
import time
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from pathlib import Path
import logging
import base64
from PIL import Image, ImageGrab
import speech_recognition as sr
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import config

logger = logging.getLogger(__name__)

class PerceptionEvent:
    """感知事件基类"""
    def __init__(self, event_type: str, data: Any, timestamp: datetime = None):
        self.event_type = event_type
        self.data = data
        self.timestamp = timestamp or datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }

class VisionPerception:
    """视觉感知系统"""
    
    def __init__(self):
        self.camera = None
        self.is_active = False
        self.last_frame = None
        self.motion_threshold = 30
        self.face_cascade = None
        self.callbacks: List[Callable] = []
        
        # 初始化人脸检测
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
        except Exception as e:
            logger.warning(f"人脸检测初始化失败: {e}")
    
    def add_callback(self, callback: Callable):
        """添加回调函数"""
        self.callbacks.append(callback)
    
    async def start_vision(self):
        """启动视觉感知"""
        if self.is_active:
            return
            
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise Exception("无法打开摄像头")
                
            self.is_active = True
            logger.info("视觉感知系统启动成功")
            
            # 启动处理线程
            threading.Thread(target=self._vision_loop, daemon=True).start()
            
        except Exception as e:
            logger.error(f"启动视觉感知失败: {e}")
            raise
    
    def stop_vision(self):
        """停止视觉感知"""
        self.is_active = False
        if self.camera:
            self.camera.release()
            self.camera = None
        logger.info("视觉感知系统已停止")
    
    def _vision_loop(self):
        """视觉处理循环"""
        prev_gray = None
        
        while self.is_active and self.camera:
            try:
                ret, frame = self.camera.read()
                if not ret:
                    continue
                
                self.last_frame = frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # 检测运动
                if prev_gray is not None:
                    motion_detected = self._detect_motion(prev_gray, gray)
                    if motion_detected:
                        self._notify_callbacks(PerceptionEvent("motion_detected", {"intensity": motion_detected}))
                
                # 检测人脸
                faces = self._detect_faces(gray)
                if len(faces) > 0:
                    self._notify_callbacks(PerceptionEvent("faces_detected", {"count": len(faces), "faces": faces.tolist()}))
                
                prev_gray = gray
                time.sleep(0.1)  # 控制帧率
                
            except Exception as e:
                logger.error(f"视觉处理错误: {e}")
                time.sleep(1)
    
    def _detect_motion(self, prev_gray: np.ndarray, curr_gray: np.ndarray) -> float:
        """检测运动"""
        diff = cv2.absdiff(prev_gray, curr_gray)
        motion_area = np.sum(diff > self.motion_threshold)
        total_area = diff.shape[0] * diff.shape[1]
        motion_ratio = motion_area / total_area
        
        if motion_ratio > 0.01:  # 1%的区域有变化才算运动
            return motion_ratio
        return 0.0
    
    def _detect_faces(self, gray: np.ndarray) -> np.ndarray:
        """检测人脸"""
        if self.face_cascade is None:
            return np.array([])
        
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return faces
    
    def capture_photo(self) -> Optional[str]:
        """拍照并返回base64编码"""
        if not self.last_frame is None:
            try:
                _, buffer = cv2.imencode('.jpg', self.last_frame)
                img_base64 = base64.b64encode(buffer).decode('utf-8')
                self._notify_callbacks(PerceptionEvent("photo_captured", {"image": img_base64}))
                return img_base64
            except Exception as e:
                logger.error(f"拍照失败: {e}")
        return None
    
    def _notify_callbacks(self, event: PerceptionEvent):
        """通知所有回调函数"""
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"视觉回调错误: {e}")

class AudioPerception:
    """听觉感知系统"""
    
    def __init__(self):
        self.is_active = False
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.callbacks: List[Callable] = []
        self.noise_threshold = 500  # 噪音阈值
        
    def add_callback(self, callback: Callable):
        """添加回调函数"""
        self.callbacks.append(callback)
        
    async def start_audio(self):
        """启动听觉感知"""
        if self.is_active:
            return
            
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                
            self.is_active = True
            logger.info("听觉感知系统启动成功")
            
            # 启动处理线程
            threading.Thread(target=self._audio_loop, daemon=True).start()
            
        except Exception as e:
            logger.error(f"启动听觉感知失败: {e}")
            raise
    
    def stop_audio(self):
        """停止听觉感知"""
        self.is_active = False
        self.microphone = None
        logger.info("听觉感知系统已停止")
    
    def _audio_loop(self):
        """音频处理循环"""
        while self.is_active and self.microphone:
            try:
                with self.microphone as source:
                    # 监听音频
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # 检测声音级别
                    audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                    volume = np.sqrt(np.mean(audio_data**2))
                    
                    if volume > self.noise_threshold:
                        self._notify_callbacks(PerceptionEvent("sound_detected", {"volume": float(volume)}))
                        
                        # 尝试语音识别
                        try:
                            text = self.recognizer.recognize_google(audio, language='zh-CN')
                            if text:
                                self._notify_callbacks(PerceptionEvent("speech_recognized", {"text": text}))
                        except sr.UnknownValueError:
                            pass  # 无法识别语音
                        except sr.RequestError as e:
                            logger.warning(f"语音识别服务错误: {e}")
                            
            except sr.WaitTimeoutError:
                pass  # 超时是正常的
            except Exception as e:
                logger.error(f"音频处理错误: {e}")
                time.sleep(1)
    
    def _notify_callbacks(self, event: PerceptionEvent):
        """通知所有回调函数"""
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"音频回调错误: {e}")

class ScreenPerception:
    """屏幕监控系统"""
    
    def __init__(self):
        self.is_active = False
        self.last_screenshot = None
        self.callbacks: List[Callable] = []
        self.monitor_interval = 2.0  # 监控间隔
        
    def add_callback(self, callback: Callable):
        """添加回调函数"""
        self.callbacks.append(callback)
    
    async def start_screen_monitor(self):
        """启动屏幕监控"""
        if self.is_active:
            return
            
        self.is_active = True
        logger.info("屏幕监控系统启动成功")
        
        # 启动处理线程
        threading.Thread(target=self._screen_loop, daemon=True).start()
    
    def stop_screen_monitor(self):
        """停止屏幕监控"""
        self.is_active = False
        logger.info("屏幕监控系统已停止")
    
    def _screen_loop(self):
        """屏幕监控循环"""
        while self.is_active:
            try:
                # 截图
                screenshot = ImageGrab.grab()
                
                # 检测变化
                if self.last_screenshot:
                    change_detected = self._detect_screen_change(self.last_screenshot, screenshot)
                    if change_detected:
                        # 分析屏幕内容
                        analysis = self._analyze_screen_content(screenshot)
                        self._notify_callbacks(PerceptionEvent("screen_changed", analysis))
                
                self.last_screenshot = screenshot
                time.sleep(self.monitor_interval)
                
            except Exception as e:
                logger.error(f"屏幕监控错误: {e}")
                time.sleep(5)
    
    def _detect_screen_change(self, prev_img: Image.Image, curr_img: Image.Image) -> bool:
        """检测屏幕变化"""
        try:
            # 缩小图片以提高比较速度
            prev_small = prev_img.resize((100, 75))
            curr_small = curr_img.resize((100, 75))
            
            # 计算差异
            prev_array = np.array(prev_small)
            curr_array = np.array(curr_small)
            diff = np.mean(np.abs(prev_array - curr_array))
            
            return diff > 10  # 差异阈值
        except Exception:
            return False
    
    def _analyze_screen_content(self, screenshot: Image.Image) -> Dict[str, Any]:
        """分析屏幕内容"""
        # 这里可以集成OCR、窗口检测等功能
        # 简化版本只返回基本信息
        width, height = screenshot.size
        
        # 转换为base64以备后用
        buffer = io.BytesIO()
        screenshot.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {
            "resolution": f"{width}x{height}",
            "timestamp": datetime.now().isoformat(),
            "image": img_base64[:1000] + "..." if len(img_base64) > 1000 else img_base64  # 限制大小
        }
    
    def capture_screenshot(self) -> str:
        """手动截图"""
        try:
            screenshot = ImageGrab.grab()
            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            self._notify_callbacks(PerceptionEvent("screenshot_captured", {"image": img_base64}))
            return img_base64
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return ""
    
    def _notify_callbacks(self, event: PerceptionEvent):
        """通知所有回调函数"""
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"屏幕回调错误: {e}")

class FileSystemHandler(FileSystemEventHandler):
    """文件系统事件处理器"""
    
    def __init__(self, callback: Callable):
        self.callback = callback
        self.last_events = {}  # 防止重复事件
        
    def on_modified(self, event):
        self._handle_event("modified", event)
    
    def on_created(self, event):
        self._handle_event("created", event)
    
    def on_deleted(self, event):
        self._handle_event("deleted", event)
    
    def on_moved(self, event):
        self._handle_event("moved", event)
    
    def _handle_event(self, event_type: str, event):
        """处理文件系统事件"""
        if event.is_directory:
            return
            
        # 防止重复事件
        event_key = f"{event_type}:{event.src_path}"
        current_time = time.time()
        
        if event_key in self.last_events:
            if current_time - self.last_events[event_key] < 1.0:  # 1秒内的重复事件忽略
                return
        
        self.last_events[event_key] = current_time
        
        # 清理旧事件记录
        for key in list(self.last_events.keys()):
            if current_time - self.last_events[key] > 60:  # 清理1分钟前的记录
                del self.last_events[key]
        
        # 分析文件类型
        file_path = Path(event.src_path)
        file_info = {
            "event_type": event_type,
            "file_path": str(file_path),
            "file_name": file_path.name,
            "file_extension": file_path.suffix,
            "file_size": file_path.stat().st_size if file_path.exists() and event_type != "deleted" else 0,
            "timestamp": datetime.now().isoformat()
        }
        
        perception_event = PerceptionEvent("file_system_event", file_info)
        self.callback(perception_event)

class FilePerception:
    """文件系统感知"""
    
    def __init__(self):
        self.observers: List[Observer] = []
        self.is_active = False
        self.callbacks: List[Callable] = []
        self.monitored_paths = []
        
    def add_callback(self, callback: Callable):
        """添加回调函数"""
        self.callbacks.append(callback)
    
    def add_monitor_path(self, path: str):
        """添加监控路径"""
        if path not in self.monitored_paths:
            self.monitored_paths.append(path)
    
    async def start_file_monitor(self):
        """启动文件监控"""
        if self.is_active:
            return
        
        # 默认监控一些常用目录
        default_paths = [
            str(Path.home() / "Desktop"),
            str(Path.home() / "Downloads"),
            str(Path.home() / "Documents"),
            str(Path.cwd())  # 当前工作目录
        ]
        
        for path in default_paths:
            if os.path.exists(path):
                self.add_monitor_path(path)
        
        try:
            for path in self.monitored_paths:
                if os.path.exists(path):
                    observer = Observer()
                    handler = FileSystemHandler(self._handle_file_event)
                    observer.schedule(handler, path, recursive=False)
                    observer.start()
                    self.observers.append(observer)
            
            self.is_active = True
            logger.info(f"文件系统监控启动成功，监控路径: {self.monitored_paths}")
            
        except Exception as e:
            logger.error(f"启动文件监控失败: {e}")
            raise
    
    def stop_file_monitor(self):
        """停止文件监控"""
        self.is_active = False
        for observer in self.observers:
            observer.stop()
            observer.join()
        self.observers.clear()
        logger.info("文件系统监控已停止")
    
    def _handle_file_event(self, event: PerceptionEvent):
        """处理文件事件"""
        # 通知所有回调
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"文件回调错误: {e}")

class PerceptionManager:
    """感知系统管理器"""
    
    def __init__(self):
        self.vision = VisionPerception()
        self.audio = AudioPerception()
        self.screen = ScreenPerception()
        self.file_system = FilePerception()
        self.event_callbacks: List[Callable] = []
        
        # 注册内部回调
        self.vision.add_callback(self._handle_perception_event)
        self.audio.add_callback(self._handle_perception_event)
        self.screen.add_callback(self._handle_perception_event)
        self.file_system.add_callback(self._handle_perception_event)
    
    def add_event_callback(self, callback: Callable):
        """添加事件回调"""
        self.event_callbacks.append(callback)
    
    async def start_all_perceptions(self):
        """启动所有感知系统"""
        try:
            await self.vision.start_vision()
            await self.audio.start_audio()
            await self.screen.start_screen_monitor()
            await self.file_system.start_file_monitor()
            logger.info("所有感知系统启动成功")
        except Exception as e:
            logger.error(f"启动感知系统失败: {e}")
            raise
    
    def stop_all_perceptions(self):
        """停止所有感知系统"""
        self.vision.stop_vision()
        self.audio.stop_audio()
        self.screen.stop_screen_monitor()
        self.file_system.stop_file_monitor()
        logger.info("所有感知系统已停止")
    
    def _handle_perception_event(self, event: PerceptionEvent):
        """处理感知事件"""
        logger.info(f"感知事件: {event.event_type}")
        
        # 通知所有回调
        for callback in self.event_callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"感知事件回调错误: {e}")
    
    def get_perception_status(self) -> Dict[str, bool]:
        """获取感知系统状态"""
        return {
            "vision": self.vision.is_active,
            "audio": self.audio.is_active,
            "screen": self.screen.is_active,
            "file_system": self.file_system.is_active
        }

# 全局感知管理器实例
perception_manager = PerceptionManager()

def get_perception_manager() -> PerceptionManager:
    """获取全局感知管理器实例"""
    return perception_manager