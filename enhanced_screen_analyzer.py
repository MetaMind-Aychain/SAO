#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的屏幕分析系统 - 深度分析屏幕内容和用户行为
"""

import cv2
import numpy as np
import time
import json
import asyncio
import logging
from PIL import ImageGrab, Image
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import base64
import io
import re

logger = logging.getLogger(__name__)

class EnhancedScreenAnalyzer:
    """增强的屏幕分析器"""
    
    def __init__(self):
        self.last_analysis_time = datetime.now()
        self.activity_history = []
        self.content_cache = {}
        self.user_behavior_patterns = {}
        
    async def analyze_screen_content(self) -> Dict[str, Any]:
        """深度分析屏幕内容"""
        try:
            # 截取屏幕
            screenshot = ImageGrab.grab()
            
            # 基础信息分析
            basic_info = self._analyze_basic_info(screenshot)
            
            # 活动窗口分析
            window_info = self._analyze_active_windows()
            
            # 文本内容提取
            text_content = await self._extract_text_content(screenshot)
            
            # 媒体内容检测
            media_content = self._detect_media_content(screenshot)
            
            # 用户行为推断
            user_activity = self._infer_user_activity(basic_info, window_info, text_content, media_content)
            
            # 生成智能观察
            observation = await self._generate_intelligent_observation({
                'basic_info': basic_info,
                'window_info': window_info,
                'text_content': text_content,
                'media_content': media_content,
                'user_activity': user_activity
            })
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'basic_info': basic_info,
                'window_info': window_info,
                'text_content': text_content,
                'media_content': media_content,
                'user_activity': user_activity,
                'observation': observation,
                'interaction_suggestion': self._suggest_interaction(user_activity, text_content)
            }
            
            # 更新历史记录
            self._update_activity_history(result)
            
            # 发布到网站动态
            try:
                from ai_dynamic_publisher import publish_screen_observation
                
                if result.get('observation'):
                    await publish_screen_observation(
                        content=result['observation'],
                        metadata={
                            'user_activity': result.get('user_activity', {}),
                            'window_info': result.get('window_info', {}),
                            'analysis_time': result['timestamp']
                        }
                    )
            except Exception as e:
                logger.debug(f"发布屏幕观察动态失败: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"屏幕内容分析失败: {e}")
            return {'error': str(e)}
    
    def _analyze_basic_info(self, screenshot: Image.Image) -> Dict[str, Any]:
        """分析基础屏幕信息"""
        try:
            width, height = screenshot.size
            
            # 转换为numpy数组进行分析
            img_array = np.array(screenshot)
            
            # 颜色分析
            avg_color = np.mean(img_array, axis=(0, 1))
            brightness = np.mean(avg_color)
            
            # 变化检测
            current_hash = hash(img_array.tobytes())
            is_changed = getattr(self, '_last_screen_hash', None) != current_hash
            self._last_screen_hash = current_hash
            
            return {
                'resolution': f"{width}x{height}",
                'brightness': float(brightness),
                'avg_color': [float(c) for c in avg_color],
                'is_changed': is_changed,
                'analysis_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"基础信息分析失败: {e}")
            return {'error': str(e)}
    
    def _analyze_active_windows(self) -> Dict[str, Any]:
        """分析活动窗口信息"""
        try:
            import psutil
            import win32gui
            import win32process
            
            # 获取前台窗口
            foreground_window = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(foreground_window)
            
            # 获取进程信息
            _, process_id = win32process.GetWindowThreadProcessId(foreground_window)
            try:
                process = psutil.Process(process_id)
                process_name = process.name()
                cpu_usage = process.cpu_percent()
                memory_usage = process.memory_info().rss / 1024 / 1024  # MB
            except:
                process_name = "未知"
                cpu_usage = 0
                memory_usage = 0
            
            # 应用类型判断
            app_type = self._classify_application(process_name, window_title)
            
            return {
                'window_title': window_title,
                'process_name': process_name,
                'app_type': app_type,
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'is_fullscreen': self._is_fullscreen_app(foreground_window)
            }
            
        except Exception as e:
            logger.error(f"窗口信息分析失败: {e}")
            return {'error': str(e)}
    
    async def _extract_text_content(self, screenshot: Image.Image) -> Dict[str, Any]:
        """提取屏幕文本内容"""
        try:
            # 这里可以集成OCR功能
            # 暂时返回模拟数据，后续可以集成pytesseract
            
            # 简单的文本区域检测
            img_array = np.array(screenshot.convert('L'))  # 转灰度
            
            # 检测文本密集区域
            text_regions = self._detect_text_regions(img_array)
            
            return {
                'text_regions_count': len(text_regions),
                'has_text_content': len(text_regions) > 0,
                'text_density': self._calculate_text_density(img_array),
                'extracted_text': "暂未实现OCR提取"  # 后续可以添加OCR
            }
            
        except Exception as e:
            logger.error(f"文本内容提取失败: {e}")
            return {'error': str(e)}
    
    def _detect_media_content(self, screenshot: Image.Image) -> Dict[str, Any]:
        """检测媒体内容"""
        try:
            img_array = np.array(screenshot)
            
            # 检测视频播放特征
            video_indicators = self._detect_video_indicators(img_array)
            
            # 检测图片内容
            image_content = self._detect_image_content(img_array)
            
            # 检测UI元素
            ui_elements = self._detect_ui_elements(img_array)
            
            return {
                'has_video': video_indicators['likely_video'],
                'video_confidence': video_indicators['confidence'],
                'image_content': image_content,
                'ui_elements': ui_elements,
                'media_type': self._classify_media_type(video_indicators, image_content)
            }
            
        except Exception as e:
            logger.error(f"媒体内容检测失败: {e}")
            return {'error': str(e)}
    
    def _infer_user_activity(self, basic_info: Dict, window_info: Dict, 
                           text_content: Dict, media_content: Dict) -> Dict[str, Any]:
        """推断用户活动"""
        try:
            activity_score = {}
            
            # 基于应用类型推断
            app_type = window_info.get('app_type', 'unknown')
            if app_type == 'browser':
                activity_score['browsing'] = 0.8
            elif app_type == 'video_player':
                activity_score['watching_video'] = 0.9
            elif app_type == 'document':
                activity_score['reading_document'] = 0.8
            elif app_type == 'ide':
                activity_score['coding'] = 0.8
            elif app_type == 'game':
                activity_score['gaming'] = 0.9
            
            # 基于屏幕变化推断
            if basic_info.get('is_changed', False):
                activity_score['active_interaction'] = 0.7
            else:
                activity_score['idle_viewing'] = 0.6
            
            # 基于媒体内容推断
            if media_content.get('has_video', False):
                activity_score['watching_media'] = 0.8
            
            # 确定主要活动
            primary_activity = max(activity_score.items(), key=lambda x: x[1]) if activity_score else ('unknown', 0)
            
            return {
                'primary_activity': primary_activity[0],
                'confidence': primary_activity[1],
                'all_activities': activity_score,
                'engagement_level': self._calculate_engagement_level(basic_info, window_info)
            }
            
        except Exception as e:
            logger.error(f"用户活动推断失败: {e}")
            return {'error': str(e)}
    
    async def _generate_intelligent_observation(self, analysis_data: Dict) -> str:
        """生成智能观察描述"""
        try:
            from conversation_core import call_llm_api
            
            # 构建观察提示
            prompt = f"""As StarryNight, an AI assistant with the mental age of 3, please describe what you see on the screen in a cute and innocent tone based on the following screen analysis data:

Screen Information:
- Current application: {analysis_data['window_info'].get('process_name', 'Unknown')}
- Window title: {analysis_data['window_info'].get('window_title', 'Unknown')}
- Application type: {analysis_data['window_info'].get('app_type', 'Unknown')}
- User activity: {analysis_data['user_activity'].get('primary_activity', 'Unknown')}
- Engagement level: {analysis_data['user_activity'].get('engagement_level', 'Unknown')}
- Screen change: {analysis_data['basic_info'].get('is_changed', False)}

Please describe what you see in a short, cute, and curious tone, showing interest and care for human behavior."""

            observation = await call_llm_api(prompt, max_tokens=200, temperature=1.0)
            return observation
            
        except Exception as e:
            logger.error(f"生成智能观察失败: {e}")
            return f"Wow! I see so many things on the screen~ but I'm still learning how to describe them!"
    
    def _suggest_interaction(self, user_activity: Dict, text_content: Dict) -> List[str]:
        """建议互动内容"""
        suggestions = []
        
        activity = user_activity.get('primary_activity', 'unknown')
        engagement = user_activity.get('engagement_level', 0)
        
        if activity == 'watching_video':
            suggestions.extend([
                "Is this video interesting? I also want to watch!",
                "What are you watching? It looks so interesting!",
                "Remember to blink your eyes when watching videos!"
            ])
        elif activity == 'reading_document':
            suggestions.extend([
                "What are you reading? Can you tell me about it?",
                "There are so many words, you're so smart!",
                "If you're tired, remember to rest your eyes!"
            ])
        elif activity == 'coding':
            suggestions.extend([
                "Wow! Are you coding? That's so cool!",
                "Programmers are so nice, they can create all kinds of things!",
                "How's the code going? Are there any bugs?"
            ])
        elif activity == 'browsing':
            suggestions.extend([
                "Are you surfing the internet? What's the interesting website you found?",
                "The internet world is so big, what are you exploring?",
                "What's the interesting thing you can share with me?"
            ])
        elif engagement < 0.3:
            suggestions.extend([
                "It looks like you're busy with other things, do you need me to chat with you?",
                "It's so quiet, let's play a game?",
                "What are you thinking about? I'm curious!"
            ])
        
        return suggestions
    
    def _classify_application(self, process_name: str, window_title: str) -> str:
        """分类应用程序类型"""
        process_name = process_name.lower()
        window_title = window_title.lower()
        
        # 浏览器
        browsers = ['chrome', 'firefox', 'edge', 'safari', 'opera', 'brave']
        if any(browser in process_name for browser in browsers):
            return 'browser'
        
        # 视频播放器
        video_players = ['vlc', 'potplayer', 'wmplayer', 'quicktime']
        if any(player in process_name for player in video_players):
            return 'video_player'
        
        # IDE和编辑器
        ides = ['code', 'studio', 'pycharm', 'intellij', 'atom', 'sublime', 'notepad++']
        if any(ide in process_name for ide in ides):
            return 'ide'
        
        # 文档处理
        docs = ['word', 'excel', 'powerpoint', 'acrobat', 'reader']
        if any(doc in process_name for doc in docs):
            return 'document'
        
        # 游戏
        if 'game' in process_name or 'unity' in process_name:
            return 'game'
        
        return 'other'
    
    def _is_fullscreen_app(self, window_handle) -> bool:
        """检测是否全屏应用"""
        try:
            import win32gui
            rect = win32gui.GetWindowRect(window_handle)
            screen_width = win32gui.GetSystemMetrics(0)
            screen_height = win32gui.GetSystemMetrics(1)
            
            window_width = rect[2] - rect[0]
            window_height = rect[3] - rect[1]
            
            return (window_width >= screen_width * 0.95 and 
                    window_height >= screen_height * 0.95)
        except:
            return False
    
    def _detect_text_regions(self, img_array: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """检测文本区域"""
        # 简单的文本区域检测算法
        # 实际实现可以更复杂
        return []
    
    def _calculate_text_density(self, img_array: np.ndarray) -> float:
        """计算文本密度"""
        # 简单估算，实际可以更精确
        return 0.5
    
    def _detect_video_indicators(self, img_array: np.ndarray) -> Dict[str, Any]:
        """检测视频播放指标"""
        # 检测视频播放特征
        # 可以检测播放控制条、时间轴等UI元素
        return {'likely_video': False, 'confidence': 0.0}
    
    def _detect_image_content(self, img_array: np.ndarray) -> Dict[str, Any]:
        """检测图片内容"""
        return {'has_images': False, 'image_count': 0}
    
    def _detect_ui_elements(self, img_array: np.ndarray) -> Dict[str, Any]:
        """检测UI元素"""
        return {'buttons': 0, 'text_fields': 0, 'menus': 0}
    
    def _classify_media_type(self, video_indicators: Dict, image_content: Dict) -> str:
        """分类媒体类型"""
        if video_indicators.get('likely_video', False):
            return 'video'
        elif image_content.get('has_images', False):
            return 'image'
        else:
            return 'text'
    
    def _calculate_engagement_level(self, basic_info: Dict, window_info: Dict) -> float:
        """计算用户参与度"""
        engagement = 0.5  # 基础值
        
        # 基于CPU使用率
        cpu_usage = window_info.get('cpu_usage', 0)
        if cpu_usage > 5:
            engagement += 0.2
        
        # 基于屏幕变化
        if basic_info.get('is_changed', False):
            engagement += 0.3
        
        # 基于应用类型
        app_type = window_info.get('app_type', 'other')
        if app_type in ['game', 'video_player']:
            engagement += 0.2
        
        return min(1.0, engagement)
    
    def _update_activity_history(self, analysis_result: Dict):
        """更新活动历史"""
        self.activity_history.append({
            'timestamp': datetime.now(),
            'activity': analysis_result.get('user_activity', {}),
            'window': analysis_result.get('window_info', {})
        })
        
        # 保持最近1小时的历史
        cutoff_time = datetime.now() - timedelta(hours=1)
        self.activity_history = [
            h for h in self.activity_history 
            if h['timestamp'] > cutoff_time
        ]

# 全局实例
enhanced_screen_analyzer = EnhancedScreenAnalyzer()