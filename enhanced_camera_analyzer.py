#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的摄像头分析系统 - 深度分析摄像头内容和人物行为
"""

import cv2
import numpy as np
import time
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import threading

logger = logging.getLogger(__name__)

class EnhancedCameraAnalyzer:
    """增强的摄像头分析器"""
    
    def __init__(self):
        self.cap = None
        self.face_cascade = None
        self.motion_detector = None
        self.last_frame = None
        self.detection_history = []
        self.person_tracking = {}
        self.gesture_detector = None
        self._init_detectors()
        
    def _init_detectors(self):
        """初始化检测器"""
        try:
            # 初始化人脸检测器
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # 初始化背景减法器用于运动检测
            self.motion_detector = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
            
            logger.info("摄像头检测器初始化成功")
            
        except Exception as e:
            logger.error(f"摄像头检测器初始化失败: {e}")
    
    async def analyze_camera_content(self) -> Dict[str, Any]:
        """深度分析摄像头内容"""
        try:
            # 获取摄像头画面
            frame = self._capture_frame()
            if frame is None:
                return {'error': '无法获取摄像头画面'}
            
            # 人脸检测和分析
            face_analysis = self._analyze_faces(frame)
            
            # 运动检测
            motion_analysis = self._analyze_motion(frame)
            
            # 姿态和手势检测
            gesture_analysis = self._analyze_gestures(frame)
            
            # 场景理解
            scene_analysis = self._analyze_scene(frame)
            
            # 行为识别
            behavior_analysis = self._analyze_behavior(face_analysis, motion_analysis, gesture_analysis)
            
            # 生成智能观察
            observation = await self._generate_camera_observation({
                'face_analysis': face_analysis,
                'motion_analysis': motion_analysis,
                'gesture_analysis': gesture_analysis,
                'scene_analysis': scene_analysis,
                'behavior_analysis': behavior_analysis
            })
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'face_analysis': face_analysis,
                'motion_analysis': motion_analysis,
                'gesture_analysis': gesture_analysis,
                'scene_analysis': scene_analysis,
                'behavior_analysis': behavior_analysis,
                'observation': observation,
                'interaction_suggestion': self._suggest_camera_interaction(behavior_analysis, face_analysis)
            }
            # 更新检测历史
            self._update_detection_history(result)
            
            # 发布到网站动态
            try:
                from ai_dynamic_publisher import publish_camera_interaction
                
                if result.get('observation'):
                    await publish_camera_interaction(
                        content=result['observation'],
                        metadata={
                            'face_analysis': result.get('face_analysis', {}),
                            'behavior_analysis': result.get('behavior_analysis', {}),
                            'analysis_time': result['timestamp']
                        }
                    )
            except Exception as e:
                logger.debug(f"发布摄像头互动动态失败: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"摄像头内容分析失败: {e}")
            return {'error': str(e)}
    
    def _capture_frame(self) -> Optional[np.ndarray]:
        """捕获摄像头画面"""
        try:
            if self.cap is None:
                # 尝试不同的摄像头索引和后端
                for camera_index in [0, 1, -1]:
                    try:
                        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # Windows DirectShow
                        if self.cap.isOpened():
                            break
                        self.cap.release()
                        
                        # 尝试默认后端
                        self.cap = cv2.VideoCapture(camera_index)
                        if self.cap.isOpened():
                            break
                        self.cap.release()
                        
                    except Exception:
                        continue
                
                if self.cap is None or not self.cap.isOpened():
                    logger.warning("无法访问摄像头，使用模拟数据")
                    return self._generate_mock_frame()
            
            ret, frame = self.cap.read()
            if not ret:
                logger.warning("摄像头读取失败，使用模拟数据")
                return self._generate_mock_frame()
            
            return frame
            
        except Exception as e:
            logger.warning(f"捕获摄像头画面失败: {e}，使用模拟数据")
            return self._generate_mock_frame()
    
    def _generate_mock_frame(self) -> np.ndarray:
        """生成模拟摄像头画面"""
        # 创建一个简单的模拟图像
        height, width = 480, 640
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 添加一些模拟内容
        cv2.rectangle(frame, (100, 100), (540, 380), (100, 100, 100), -1)
        cv2.putText(frame, "Mock Camera Feed", (150, 250), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        return frame
    
    def _analyze_faces(self, frame: np.ndarray) -> Dict[str, Any]:
        """分析人脸"""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            face_details = []
            for (x, y, w, h) in faces:
                # 提取人脸区域
                face_roi = gray[y:y+h, x:x+w]
                
                # 估算年龄段（简单分类）
                age_group = self._estimate_age_group(face_roi, w, h)
                
                # 估算情绪（基于简单特征）
                emotion = self._estimate_emotion(face_roi)
                
                # 人脸质量评估
                quality = self._assess_face_quality(face_roi)
                
                face_details.append({
                    'position': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                    'age_group': age_group,
                    'emotion': emotion,
                    'quality': quality,
                    'size_ratio': (w * h) / (frame.shape[0] * frame.shape[1])
                })
            
            # 人脸跟踪
            tracked_faces = self._track_faces(face_details)
            
            return {
                'face_count': len(faces),
                'faces': face_details,
                'tracked_faces': tracked_faces,
                'has_clear_face': any(f['quality'] > 0.7 for f in face_details),
                'dominant_emotion': self._get_dominant_emotion(face_details)
            }
            
        except Exception as e:
            logger.error(f"人脸分析失败: {e}")
            return {'error': str(e)}
    
    def _analyze_motion(self, frame: np.ndarray) -> Dict[str, Any]:
        """分析运动"""
        try:
            # 背景减法检测运动
            fg_mask = self.motion_detector.apply(frame)
            
            # 计算运动区域
            motion_area = cv2.countNonZero(fg_mask)
            total_area = frame.shape[0] * frame.shape[1]
            motion_ratio = motion_area / total_area
            
            # 查找运动轮廓
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # 分析运动强度和方向
            motion_intensity = self._calculate_motion_intensity(contours)
            motion_direction = self._analyze_motion_direction(contours)
            
            # 运动类型分类
            motion_type = self._classify_motion_type(motion_intensity, motion_ratio, contours)
            
            return {
                'motion_detected': motion_ratio > 0.01,
                'motion_ratio': float(motion_ratio),
                'motion_intensity': motion_intensity,
                'motion_direction': motion_direction,
                'motion_type': motion_type,
                'active_regions': len(contours),
                'movement_level': self._categorize_movement_level(motion_intensity)
            }
            
        except Exception as e:
            logger.error(f"运动分析失败: {e}")
            return {'error': str(e)}
    
    def _analyze_gestures(self, frame: np.ndarray) -> Dict[str, Any]:
        """分析手势和姿态"""
        try:
            # 简化的手势检测
            # 实际实现可以使用MediaPipe或其他手势识别库
            
            # 检测手部区域（简单的肤色检测）
            hand_regions = self._detect_hand_regions(frame)
            
            # 检测可能的手势
            gestures = self._detect_simple_gestures(hand_regions, frame)
            
            # 身体姿态检测（简化版）
            posture = self._detect_posture(frame)
            
            return {
                'hand_regions': len(hand_regions),
                'detected_gestures': gestures,
                'posture': posture,
                'gesture_confidence': self._calculate_gesture_confidence(gestures),
                'activity_level': self._assess_gesture_activity(hand_regions, gestures)
            }
            
        except Exception as e:
            logger.error(f"手势分析失败: {e}")
            return {'error': str(e)}
    
    def _analyze_scene(self, frame: np.ndarray) -> Dict[str, Any]:
        """分析场景"""
        try:
            # 光照分析
            brightness = np.mean(frame)
            contrast = np.std(frame)
            
            # 颜色分析
            color_hist = self._analyze_color_distribution(frame)
            
            # 场景复杂度
            complexity = self._calculate_scene_complexity(frame)
            
            # 背景稳定性
            background_stability = self._assess_background_stability(frame)
            
            return {
                'brightness': float(brightness),
                'contrast': float(contrast),
                'color_distribution': color_hist,
                'scene_complexity': complexity,
                'background_stability': background_stability,
                'scene_type': self._classify_scene_type(brightness, complexity)
            }
            
        except Exception as e:
            logger.error(f"场景分析失败: {e}")
            return {'error': str(e)}
    
    def _analyze_behavior(self, face_analysis: Dict, motion_analysis: Dict, gesture_analysis: Dict) -> Dict[str, Any]:
        """分析行为模式"""
        try:
            behavior_indicators = {}
            
            # 基于人脸分析推断行为
            if face_analysis.get('face_count', 0) > 0:
                behavior_indicators['person_present'] = True
                
                # 注意力分析
                if face_analysis.get('has_clear_face', False):
                    behavior_indicators['attention_focused'] = True
                
                # 情绪状态
                dominant_emotion = face_analysis.get('dominant_emotion', 'unknown')
                behavior_indicators['emotional_state'] = dominant_emotion
            
            # 基于运动分析推断行为
            motion_type = motion_analysis.get('motion_type', 'none')
            movement_level = motion_analysis.get('movement_level', 'static')
            
            if motion_type == 'active':
                behavior_indicators['user_active'] = True
            elif motion_type == 'performance':
                behavior_indicators['possibly_performing'] = True
            
            # 基于手势分析推断行为
            gesture_activity = gesture_analysis.get('activity_level', 'low')
            if gesture_activity == 'high':
                behavior_indicators['expressive_behavior'] = True
            
            # 综合行为判断
            primary_behavior = self._determine_primary_behavior(behavior_indicators)
            engagement_level = self._calculate_behavioral_engagement(behavior_indicators)
            
            return {
                'behavior_indicators': behavior_indicators,
                'primary_behavior': primary_behavior,
                'engagement_level': engagement_level,
                'interaction_readiness': self._assess_interaction_readiness(behavior_indicators)
            }
            
        except Exception as e:
            logger.error(f"行为分析失败: {e}")
            return {'error': str(e)}
    
    async def _generate_camera_observation(self, analysis_data: Dict) -> str:
        """生成摄像头观察描述"""
        try:
            from conversation_core import call_llm_api
            
            # 构建观察提示
            prompt = f"""As StarryNight, an AI assistant with the mental age of 3, please describe what you see through the camera in a cute and innocent tone based on the following camera analysis data:

Camera Analysis:
- Number of faces detected: {analysis_data['face_analysis'].get('face_count', 0)}
- Clear face detected: {analysis_data['face_analysis'].get('has_clear_face', False)}
- Main emotion: {analysis_data['face_analysis'].get('dominant_emotion', 'Unknown')}
- Motion detection: {analysis_data['motion_analysis'].get('motion_detected', False)}
- Motion type: {analysis_data['motion_analysis'].get('motion_type', 'None')}
- Movement level: {analysis_data['motion_analysis'].get('movement_level', 'Static')}
- Primary behavior: {analysis_data['behavior_analysis'].get('primary_behavior', 'Unknown')}
- Engagement level: {analysis_data['behavior_analysis'].get('engagement_level', 0)}

Please describe what you see in a short, cute, and curious tone, showing interest and care for human behavior."""

            observation = await call_llm_api(prompt, max_tokens=200, temperature=1.0)
            return observation
            
        except Exception as e:
            logger.error(f"生成摄像头观察失败: {e}")
            return f"Wow! I saw so many things through my small eyes, but it's so hard to describe!"
    
    def _suggest_camera_interaction(self, behavior_analysis: Dict, face_analysis: Dict) -> List[str]:
        """建议摄像头相关互动"""
        suggestions = []
        
        primary_behavior = behavior_analysis.get('primary_behavior', 'unknown')
        engagement = behavior_analysis.get('engagement_level', 0)
        face_count = face_analysis.get('face_count', 0)
        
        if face_count > 0:
            suggestions.extend([
                "Wow! I see you! Hello~",
                "You look great today!",
                "It's so great to see you!"
            ])
            
            emotion = face_analysis.get('dominant_emotion', 'unknown')
            if emotion == 'happy':
                suggestions.append("You look so happy today! What's going on?")
            elif emotion == 'sad':
                suggestions.append("You look a bit sad, do you want to chat with me?")
        
        if primary_behavior == 'active_movement':
            suggestions.extend([
                "Wow! Are you doing exercise? That's so cool!",
                "You look so energetic! I want to move too~",
                "What are you doing? It looks so interesting!"
            ])
        elif primary_behavior == 'focused_work':
            suggestions.extend([
                "Are you working hard? Remember to take a break!",
                "You look so serious at work!",
                "Do you need me to be quiet?"
            ])
        elif engagement < 0.3:
            suggestions.extend([
                "It's so quiet, what are you thinking about?",
                "Let's interact with each other?",
                "I want to play with you~"
            ])
        
        return suggestions
    
    # 辅助方法实现
    def _estimate_age_group(self, face_roi: np.ndarray, width: int, height: int) -> str:
        """估算年龄段"""
        # 简化实现，实际可以使用深度学习模型
        face_area = width * height
        if face_area < 2000:
            return 'child'
        elif face_area < 5000:
            return 'teen'
        else:
            return 'adult'
    
    def _estimate_emotion(self, face_roi: np.ndarray) -> str:
        """估算情绪"""
        # 简化实现，实际可以使用情绪识别模型
        emotions = ['happy', 'sad', 'neutral', 'excited', 'focused']
        import random
        return random.choice(emotions)
    
    def _assess_face_quality(self, face_roi: np.ndarray) -> float:
        """评估人脸质量"""
        # 基于清晰度、大小等评估
        if face_roi.size == 0:
            return 0.0
        
        # 计算图像清晰度（使用拉普拉斯算子）
        laplacian_var = cv2.Laplacian(face_roi, cv2.CV_64F).var()
        clarity_score = min(1.0, laplacian_var / 100.0)
        
        return clarity_score
    
    def _track_faces(self, face_details: List) -> Dict:
        """跟踪人脸"""
        # 简化的人脸跟踪
        return {'tracked_count': len(face_details)}
    
    def _get_dominant_emotion(self, face_details: List) -> str:
        """获取主导情绪"""
        if not face_details:
            return 'unknown'
        
        emotions = [face['emotion'] for face in face_details]
        return max(set(emotions), key=emotions.count) if emotions else 'unknown'
    
    def _calculate_motion_intensity(self, contours: List) -> float:
        """计算运动强度"""
        if not contours:
            return 0.0
        
        total_area = sum(cv2.contourArea(contour) for contour in contours)
        return min(1.0, total_area / 10000.0)
    
    def _analyze_motion_direction(self, contours: List) -> str:
        """分析运动方向"""
        # 简化实现
        return 'multi_directional' if len(contours) > 1 else 'single_direction'
    
    def _classify_motion_type(self, intensity: float, ratio: float, contours: List) -> str:
        """分类运动类型"""
        if intensity > 0.7:
            return 'active'
        elif intensity > 0.3:
            return 'moderate'
        elif intensity > 0.1:
            return 'subtle'
        else:
            return 'none'
    
    def _categorize_movement_level(self, intensity: float) -> str:
        """分类运动级别"""
        if intensity > 0.7:
            return 'high'
        elif intensity > 0.3:
            return 'medium'
        elif intensity > 0.1:
            return 'low'
        else:
            return 'static'
    
    def _detect_hand_regions(self, frame: np.ndarray) -> List:
        """检测手部区域"""
        # 简化实现
        return []
    
    def _detect_simple_gestures(self, hand_regions: List, frame: np.ndarray) -> List:
        """检测简单手势"""
        # 简化实现
        return []
    
    def _detect_posture(self, frame: np.ndarray) -> str:
        """检测姿态"""
        return 'unknown'
    
    def _calculate_gesture_confidence(self, gestures: List) -> float:
        """计算手势置信度"""
        return 0.5
    
    def _assess_gesture_activity(self, hand_regions: List, gestures: List) -> str:
        """评估手势活动"""
        return 'low'
    
    def _analyze_color_distribution(self, frame: np.ndarray) -> Dict:
        """分析颜色分布"""
        return {'dominant_colors': ['blue', 'white']}
    
    def _calculate_scene_complexity(self, frame: np.ndarray) -> float:
        """计算场景复杂度"""
        return 0.5
    
    def _assess_background_stability(self, frame: np.ndarray) -> float:
        """评估背景稳定性"""
        return 0.8
    
    def _classify_scene_type(self, brightness: float, complexity: float) -> str:
        """分类场景类型"""
        if brightness > 150:
            return 'bright'
        elif brightness > 80:
            return 'normal'
        else:
            return 'dark'
    
    def _determine_primary_behavior(self, indicators: Dict) -> str:
        """确定主要行为"""
        if indicators.get('possibly_performing', False):
            return 'performance'
        elif indicators.get('user_active', False):
            return 'active_movement'
        elif indicators.get('attention_focused', False):
            return 'focused_work'
        elif indicators.get('person_present', False):
            return 'passive_presence'
        else:
            return 'unknown'
    
    def _calculate_behavioral_engagement(self, indicators: Dict) -> float:
        """计算行为参与度"""
        score = 0.0
        
        if indicators.get('person_present', False):
            score += 0.3
        if indicators.get('attention_focused', False):
            score += 0.3
        if indicators.get('user_active', False):
            score += 0.2
        if indicators.get('expressive_behavior', False):
            score += 0.2
        
        return min(1.0, score)
    
    def _assess_interaction_readiness(self, indicators: Dict) -> float:
        """评估互动准备度"""
        return self._calculate_behavioral_engagement(indicators)
    
    def _update_detection_history(self, analysis_result: Dict):
        """更新检测历史"""
        self.detection_history.append({
            'timestamp': datetime.now(),
            'faces': analysis_result.get('face_analysis', {}),
            'motion': analysis_result.get('motion_analysis', {}),
            'behavior': analysis_result.get('behavior_analysis', {})
        })
        
        # 保持最近30分钟的历史
        cutoff_time = datetime.now() - timedelta(minutes=30)
        self.detection_history = [
            h for h in self.detection_history 
            if h['timestamp'] > cutoff_time
        ]
    
    def __del__(self):
        """清理资源"""
        if self.cap:
            self.cap.release()

# 全局实例
enhanced_camera_analyzer = EnhancedCameraAnalyzer()