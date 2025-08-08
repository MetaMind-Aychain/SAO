# ui/emotion_panel.py
"""
情绪面板组件 - 集成到原有ChatWindow的简化版本
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QGridLayout, QProgressBar, QTextEdit, QFrame
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

logger = logging.getLogger(__name__)

class EmotionPanel(QWidget):
    """情绪面板 - 显示AI情绪状态的侧边栏"""
    
    thinking_requested = pyqtSignal()
    search_requested = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # 设置更新定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.request_status_update)
        self.update_timer.start(5000)  # 每5秒更新一次
        
        # 状态回调
        self.status_callback = None
        
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # 标题
        title_label = QLabel("🌟 StarryNight状态")
        title_label.setFont(QFont("微软雅黑", 11, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                background-color: rgba(60, 80, 180, 120);
                color: #E6F3FF;
                border-radius: 8px;
                padding: 8px;
                margin-bottom: 5px;
                border: 1px solid rgba(120, 160, 255, 80);
            }
        """)
        layout.addWidget(title_label)
        
        # 当前情绪显示
        self.emotion_label = QLabel("😊 快乐 (70%)")
        self.emotion_label.setFont(QFont("微软雅黑", 10))
        self.emotion_label.setAlignment(Qt.AlignCenter)
        self.emotion_label.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 50, 120, 150);
                border: 2px solid #8AACFF;
                border-radius: 8px;
                padding: 8px;
                margin: 2px;
                color: #CCDDFF;
            }
        """)
        layout.addWidget(self.emotion_label)
        
        # 基本信息
        info_group = QGroupBox("基本信息")
        info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #6A8CFF;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #AACCFF;
                background-color: rgba(20, 30, 60, 80);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #E6F3FF;
            }
        """)
        info_layout = QVBoxLayout(info_group)
        
        self.ai_name_label = QLabel("姓名: StarryNight")
        self.age_label = QLabel("年龄: 3岁")
        self.last_interaction_label = QLabel("最后互动: 刚才")
        
        for label in [self.ai_name_label, self.age_label, self.last_interaction_label]:
            label.setFont(QFont("微软雅黑", 9))
            label.setStyleSheet("padding: 2px; color: #CCDDFF;")
            info_layout.addWidget(label)
        
        layout.addWidget(info_group)
        
        # 满足度显示
        satisfaction_group = QGroupBox("满足度")
        satisfaction_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #6A8CFF;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #AACCFF;
                background-color: rgba(20, 30, 60, 80);
                
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #E6F3FF;
            }
        """)
        satisfaction_layout = QGridLayout(satisfaction_group)
        
        # 社交满足度
        social_label = QLabel("社交:")
        social_label.setFont(QFont("微软雅黑", 8))
        social_label.setStyleSheet("color: #CCDDFF;")
        self.social_progress = QProgressBar()
        self.social_progress.setRange(0, 100)
        self.social_progress.setValue(70)
        self.social_progress.setMaximumHeight(15)
        self.social_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #6A8CFF;
                border-radius: 6px;
                text-align: center;
                font-size: 8px;
                background-color: rgba(30, 50, 120, 150);
                color: #E6F3FF;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6A8CFF, stop:1 #9966FF);
                border-radius: 4px;
            }
        """)
        
        satisfaction_layout.addWidget(social_label, 0, 0)
        satisfaction_layout.addWidget(self.social_progress, 0, 1)
        
        # 探索满足度
        exploration_label = QLabel("探索:")
        exploration_label.setFont(QFont("微软雅黑", 8))
        exploration_label.setStyleSheet("color: #CCDDFF;")
        self.exploration_progress = QProgressBar()
        self.exploration_progress.setRange(0, 100)
        self.exploration_progress.setValue(50)
        self.exploration_progress.setMaximumHeight(15)
        self.exploration_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #6A8CFF;
                border-radius: 6px;
                text-align: center;
                font-size: 8px;
                background-color: rgba(30, 50, 120, 150);
                color: #E6F3FF;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8AACFF, stop:1 #B586FF);
                border-radius: 4px;
            }
        """)
        
        satisfaction_layout.addWidget(exploration_label, 1, 0)
        satisfaction_layout.addWidget(self.exploration_progress, 1, 1)
        
        layout.addWidget(satisfaction_group)
        
        # 快速操作按钮
        buttons_group = QGroupBox("快速操作")
        buttons_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #6A8CFF;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #AACCFF;
                background-color: rgba(20, 30, 60, 80);
                
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        buttons_layout = QVBoxLayout(buttons_group)
        
        self.thinking_button = QPushButton("🤖 让她思考")
        self.thinking_button.setFont(QFont("微软雅黑", 9))
        self.thinking_button.clicked.connect(self.thinking_requested.emit)
        self.thinking_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        
        self.search_button = QPushButton("🔍 搜索知识")
        self.search_button.setFont(QFont("微软雅黑", 9))
        self.search_button.clicked.connect(lambda: self.search_requested.emit(""))
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        
        buttons_layout.addWidget(self.thinking_button)
        buttons_layout.addWidget(self.search_button)
        
        # 紧急停止按钮
        self.emergency_button = QPushButton("🚨 紧急停止")
        self.emergency_button.setFont(QFont("微软雅黑", 9))
        self.emergency_button.setCheckable(True)
        self.emergency_button.clicked.connect(self._on_emergency_clicked)
        self.emergency_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #ba0000;
            }
            QPushButton:checked {
                background-color: #ba0000;
                border: 2px solid yellow;
            }
        """)
        buttons_layout.addWidget(self.emergency_button)
        
        layout.addWidget(buttons_group)
        
        # 其他情绪显示
        other_emotions_group = QGroupBox("其他情绪")
        other_emotions_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        other_emotions_layout = QVBoxLayout(other_emotions_group)
        
        self.other_emotions_text = QTextEdit()
        self.other_emotions_text.setMaximumHeight(60)
        self.other_emotions_text.setReadOnly(True)
        self.other_emotions_text.setFont(QFont("微软雅黑", 8))
        self.other_emotions_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        self.other_emotions_text.setText("当前只有一种主导情绪")
        
        other_emotions_layout.addWidget(self.other_emotions_text)
        layout.addWidget(other_emotions_group)
        
        # 添加伸缩空间
        layout.addStretch()
        
        # 设置固定宽度
        self.setFixedWidth(220)
        
    def set_status_callback(self, callback):
        """设置状态更新回调"""
        self.status_callback = callback
    
    def _on_emergency_clicked(self):
        """处理紧急停止按钮点击"""
        try:
            is_stopped = self.emergency_button.isChecked()
            
            # 获取emotion_core实例
            if hasattr(self, 'status_callback') and self.status_callback:
                # 通过回调获取emotion_core的引用
                import sys
                for obj in sys.modules.values():
                    if hasattr(obj, 'emotion_core'):
                        emotion_core = obj.emotion_core
                        if hasattr(emotion_core, 'emergency_stop'):
                            if is_stopped:
                                emotion_core.emergency_stop()
                                self.emergency_button.setText("🔓 解除停止")
                            else:
                                emotion_core.resume_autonomous()
                                self.emergency_button.setText("🚨 紧急停止")
                            break
                
        except Exception as e:
            print(f"紧急停止操作失败: {e}")
        
    def request_status_update(self):
        """请求状态更新"""
        if self.status_callback:
            try:
                status = self.status_callback()
                if status:
                    self.update_status(status)
            except Exception as e:
                logger.error(f"获取状态失败: {e}")
    
    def update_status(self, status_data: Dict[str, Any]):
        """更新状态显示"""
        try:
            # 更新基本信息
            ai_name = status_data.get("ai_name", "StarryNight")
            personality_age = status_data.get("personality_age", 3)
            last_interaction = status_data.get("last_interaction", "未知")
            
            self.ai_name_label.setText(f"姓名: {ai_name}")
            self.age_label.setText(f"年龄: {personality_age}岁")
            self.last_interaction_label.setText(f"最后互动: {last_interaction}")
            
            # 更新主导情绪
            dominant_emotion = status_data.get("dominant_emotion", {})
            emotion_type = dominant_emotion.get("type", "calm")
            emotion_intensity = dominant_emotion.get("intensity", "0%")
            emotion_emoji = dominant_emotion.get("emoji", "😐")
            
            self.emotion_label.setText(f"{emotion_emoji} {emotion_type} ({emotion_intensity})")
            
            # 更新满足度
            social_satisfaction = status_data.get("social_satisfaction", "0%")
            exploration_satisfaction = status_data.get("exploration_satisfaction", "0%")
            
            try:
                social_value = int(social_satisfaction.replace("%", ""))
                self.social_progress.setValue(social_value)
            except:
                pass
                
            try:
                exploration_value = int(exploration_satisfaction.replace("%", ""))
                self.exploration_progress.setValue(exploration_value)
            except:
                pass
            
            # 更新其他情绪
            all_emotions = status_data.get("all_emotions", [])
            if len(all_emotions) > 1:
                other_emotions_text = "其他情绪:\n"
                for emotion in all_emotions[1:]:  # 跳过主导情绪
                    other_emotions_text += f"• {emotion.get('type', '')} ({emotion.get('intensity', '0%')})\n"
                self.other_emotions_text.setText(other_emotions_text)
            else:
                self.other_emotions_text.setText("当前只有一种主导情绪")
                
        except Exception as e:
            logger.error(f"更新状态显示失败: {e}")
            
    def update_emotion(self, emotion_type: str, intensity: float):
        """更新情绪显示（来自通知管理器）"""
        try:
            # 转换强度为百分比
            intensity_percent = int(intensity * 100)
            
            # 根据情绪类型选择表情符号
            emotion_emojis = {
                "快乐": "😊", "兴奋": "🤩", "calm": "😌", "好奇": "🤔",
                "悲伤": "😢", "惊讶": "😲", "愤怒": "😠", "恐惧": "😨"
            }
            emoji = emotion_emojis.get(emotion_type, "😐")
            
            # 更新情绪标签
            self.emotion_label.setText(f"{emoji} {emotion_type} ({intensity_percent}%)")
            
            # 如果有对应的进度条，也更新它
            # 这里可以根据需要添加更多的UI更新逻辑
            
        except Exception as e:
            logger.error(f"更新情绪显示失败: {e}")
    
    def update_activity_status(self, activity_type: str, description: str):
        """更新活动状态显示"""
        try:
            # 根据活动类型更新相应的显示
            activity_descriptions = {
                "thinking": "🤔 正在思考...",
                "camera": "👁️ 观察摄像头",
                "screen": "🖥️ 分析屏幕",
                "file": "📚 阅读文件",
                "web": "🌐 浏览网页",
                "learning": "📖 学习知识",
                "interaction": "💬 互动交流",
                "summary": "📝 整理总结"
            }
            
            activity_text = activity_descriptions.get(activity_type, f"⚡ {activity_type}")
            
            # 更新最后交互时间
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M")
            self.last_interaction_label.setText(f"当前活动: {activity_text} ({current_time})")
            
        except Exception as e:
            logger.error(f"更新活动状态失败: {e}")
    
    def add_activity_notification(self, message: str, activity_type: str = None):
        """添加活动通知到情绪面板"""
        try:
            # 这里可以添加一个小的通知显示区域
            # 或者更新其他情绪文本区域来显示最新活动
            if hasattr(self, 'other_emotions_text'):
                current_text = self.other_emotions_text.toPlainText()
                new_text = f"最新活动: {message}\n" + current_text[:200]  # 保持文本长度合理
                self.other_emotions_text.setText(new_text)
                
        except Exception as e:
            logger.error(f"添加活动通知失败: {e}")

    def closeEvent(self, event):
        """关闭事件"""
        if self.update_timer:
            self.update_timer.stop()
        super().closeEvent(event)