# ui/emotional_ui_extension.py
"""
情绪化UI扩展组件
为PyQt界面添加情绪显示和感知控制功能
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTabWidget, QTextEdit, QGroupBox, QGridLayout, QCheckBox,
    QProgressBar, QSlider, QSpinBox, QLineEdit, QScrollArea,
    QFrame, QSizePolicy, QSpacerItem, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor

logger = logging.getLogger(__name__)

class EmotionalStatusWidget(QWidget):
    """情绪状态显示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("🎭 AI情绪状态")
        title_label.setFont(QFont("微软雅黑", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 主情绪显示
        self.main_emotion_label = QLabel("😊 快乐 (70%)")
        self.main_emotion_label.setFont(QFont("微软雅黑", 14))
        self.main_emotion_label.setAlignment(Qt.AlignCenter)
        self.main_emotion_label.setStyleSheet("""
            QLabel {
                background-color: rgba(100, 200, 255, 100);
                border: 2px solid #66ccff;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
        """)
        layout.addWidget(self.main_emotion_label)
        
        # 情绪详情
        self.emotion_details = QTextEdit()
        self.emotion_details.setMaximumHeight(100)
        self.emotion_details.setReadOnly(True)
        self.emotion_details.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 10px;
            }
        """)
        layout.addWidget(self.emotion_details)
        
        # 个性特征显示
        personality_group = QGroupBox("个性特征")
        personality_layout = QGridLayout(personality_group)
        
        self.personality_traits = {
            "好奇心": QProgressBar(),
            "顽皮度": QProgressBar(),
            "需要陪伴": QProgressBar(),
            "聪明度": QProgressBar(),
            "精力水平": QProgressBar()
        }
        
        for i, (trait_name, progress_bar) in enumerate(self.personality_traits.items()):
            label = QLabel(trait_name)
            progress_bar.setRange(0, 100)
            progress_bar.setValue(70)  # 默认值
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #66ccff;
                    border-radius: 4px;
                }
            """)
            
            personality_layout.addWidget(label, i, 0)
            personality_layout.addWidget(progress_bar, i, 1)
        
        layout.addWidget(personality_group)
        
        # 快速操作按钮
        buttons_layout = QHBoxLayout()
        
        self.thinking_button = QPushButton("🤖 自主思考")
        self.thinking_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.search_button = QPushButton("🔍 搜索知识")
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        buttons_layout.addWidget(self.thinking_button)
        buttons_layout.addWidget(self.search_button)
        layout.addLayout(buttons_layout)
        
        self.setMaximumWidth(300)
        
    def update_emotion_status(self, emotion_data: Dict[str, Any]):
        """更新情绪状态显示"""
        try:
            # 更新主情绪
            dominant_emotion = emotion_data.get("dominant_emotion", {})
            emotion_type = dominant_emotion.get("type", "calm")
            emotion_intensity = dominant_emotion.get("intensity", "0%")
            emotion_emoji = dominant_emotion.get("emoji", "😐")
            
            self.main_emotion_label.setText(f"{emotion_emoji} {emotion_type} ({emotion_intensity})")
            
            # 更新情绪详情
            all_emotions = emotion_data.get("all_emotions", [])
            details_text = "当前所有情绪:\n"
            for emotion in all_emotions:
                details_text += f"• {emotion.get('type', '')} - {emotion.get('intensity', '0%')} ({emotion.get('duration', '0秒')})\n"
            
            if not all_emotions:
                details_text += "当前心情calm～"
            
            self.emotion_details.setText(details_text)
            
            # 更新个性特征
            personality = emotion_data.get("personality", {})
            for trait_name, progress_bar in self.personality_traits.items():
                trait_key = {
                    "好奇心": "curiosity",
                    "顽皮度": "playfulness", 
                    "需要陪伴": "neediness",
                    "聪明度": "intelligence",
                    "精力水平": "energy_level"
                }.get(trait_name, "")
                
                if trait_key in personality:
                    value = int(personality[trait_key] * 100)
                    progress_bar.setValue(value)
                    
        except Exception as e:
            logger.error(f"更新情绪状态失败: {e}")

class PerceptionControlWidget(QWidget):
    """感知控制组件"""
    
    perception_toggled = pyqtSignal(str, bool)  # 感知类型, 启用状态
    capture_photo = pyqtSignal()
    capture_screenshot = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("👁️ 感知控制")
        title_label.setFont(QFont("微软雅黑", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 视觉感知
        vision_group = QGroupBox("📷 视觉感知")
        vision_layout = QVBoxLayout(vision_group)
        
        self.vision_checkbox = QCheckBox("启动摄像头")
        self.vision_checkbox.stateChanged.connect(
            lambda state: self.perception_toggled.emit("vision", state == Qt.Checked)
        )
        vision_layout.addWidget(self.vision_checkbox)
        
        self.photo_button = QPushButton("📸 拍照")
        self.photo_button.clicked.connect(self.capture_photo.emit)
        self.photo_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        vision_layout.addWidget(self.photo_button)
        
        layout.addWidget(vision_group)
        
        # 听觉感知
        audio_group = QGroupBox("🎤 听觉感知")
        audio_layout = QVBoxLayout(audio_group)
        
        self.audio_checkbox = QCheckBox("启动麦克风")
        self.audio_checkbox.stateChanged.connect(
            lambda state: self.perception_toggled.emit("audio", state == Qt.Checked)
        )
        audio_layout.addWidget(self.audio_checkbox)
        
        layout.addWidget(audio_group)
        
        # 屏幕监控
        screen_group = QGroupBox("🖥️ 屏幕监控")
        screen_layout = QVBoxLayout(screen_group)
        
        self.screen_checkbox = QCheckBox("启动监控")
        self.screen_checkbox.stateChanged.connect(
            lambda state: self.perception_toggled.emit("screen", state == Qt.Checked)
        )
        screen_layout.addWidget(self.screen_checkbox)
        
        self.screenshot_button = QPushButton("📱 截图")
        self.screenshot_button.clicked.connect(self.capture_screenshot.emit)
        self.screenshot_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        screen_layout.addWidget(self.screenshot_button)
        
        layout.addWidget(screen_group)
        
        # 文件监控
        file_group = QGroupBox("📁 文件监控")
        file_layout = QVBoxLayout(file_group)
        
        self.file_checkbox = QCheckBox("启动监控")
        self.file_checkbox.stateChanged.connect(
            lambda state: self.perception_toggled.emit("file_system", state == Qt.Checked)
        )
        file_layout.addWidget(self.file_checkbox)
        
        layout.addWidget(file_group)
        
        self.setMaximumWidth(250)
        
    def update_perception_status(self, status: Dict[str, bool]):
        """更新感知状态"""
        self.vision_checkbox.setChecked(status.get("vision", False))
        self.audio_checkbox.setChecked(status.get("audio", False))
        self.screen_checkbox.setChecked(status.get("screen", False))
        self.file_checkbox.setChecked(status.get("file_system", False))

class KnowledgeExplorationWidget(QWidget):
    """知识探索组件"""
    
    manual_search = pyqtSignal(str)  # 搜索查询
    toggle_auto_exploration = pyqtSignal(bool)  # 切换自动探索
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("🧠 知识探索")
        title_label.setFont(QFont("微软雅黑", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 手动搜索
        search_group = QGroupBox("🔍 手动搜索")
        search_layout = QVBoxLayout(search_group)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入感兴趣的内容...")
        self.search_input.returnPressed.connect(self._on_search)
        search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("🚀 开始搜索")
        self.search_button.clicked.connect(self._on_search)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        search_layout.addWidget(self.search_button)
        
        layout.addWidget(search_group)
        
        # 自动探索
        auto_group = QGroupBox("🚀 自动探索")
        auto_layout = QVBoxLayout(auto_group)
        
        self.auto_exploration_checkbox = QCheckBox("启动自动探索")
        self.auto_exploration_checkbox.setChecked(True)
        self.auto_exploration_checkbox.stateChanged.connect(
            lambda state: self.toggle_auto_exploration.emit(state == Qt.Checked)
        )
        auto_layout.addWidget(self.auto_exploration_checkbox)
        
        auto_info = QLabel("AI会根据情绪和兴趣自动搜索知识")
        auto_info.setWordWrap(True)
        auto_info.setStyleSheet("color: #666; font-size: 11px;")
        auto_layout.addWidget(auto_info)
        
        layout.addWidget(auto_group)
        
        # 探索结果显示
        results_group = QGroupBox("📋 最近发现")
        results_layout = QVBoxLayout(results_group)
        
        self.results_list = QListWidget()
        self.results_list.setMaximumHeight(200)
        self.results_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
        """)
        results_layout.addWidget(self.results_list)
        
        layout.addWidget(results_group)
        
        self.setMaximumWidth(350)
        
    def _on_search(self):
        """搜索按钮点击处理"""
        query = self.search_input.text().strip()
        if query:
            self.manual_search.emit(query)
            self.search_input.clear()
            
            # 添加到结果列表
            item = QListWidgetItem(f"🔍 搜索: {query}")
            self.results_list.insertItem(0, item)
            
            # 限制列表长度
            if self.results_list.count() > 10:
                self.results_list.takeItem(10)
    
    def add_exploration_result(self, result_text: str):
        """添加探索结果"""
        item = QListWidgetItem(f"🌟 发现: {result_text}")
        self.results_list.insertItem(0, item)
        
        # 限制列表长度
        if self.results_list.count() > 10:
            self.results_list.takeItem(10)

class SystemStatusWidget(QWidget):
    """系统状态组件"""
    
    refresh_status = pyqtSignal()
    export_logs = pyqtSignal()
    clear_cache = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("📊 系统状态")
        title_label.setFont(QFont("微软雅黑", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 状态显示区域
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 200);
                color: #00ff00;
                border: 1px solid #333;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        layout.addWidget(self.status_text)
        
        # 控制按钮
        buttons_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("🔄 刷新状态")
        self.refresh_button.clicked.connect(self.refresh_status.emit)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        self.export_button = QPushButton("💾 导出日志")
        self.export_button.clicked.connect(self.export_logs.emit)
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        self.clear_button = QPushButton("🗑️ 清理缓存")
        self.clear_button.clicked.connect(self.clear_cache.emit)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addWidget(self.export_button)
        buttons_layout.addWidget(self.clear_button)
        layout.addLayout(buttons_layout)
        
    def update_status(self, status_data: Dict[str, Any]):
        """更新状态显示"""
        try:
            status_text = f"=== AI系统状态 ===\n"
            status_text += f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # AI基本信息
            ai_info = status_data.get("ai_info", {})
            status_text += f"AI名称: {ai_info.get('name', 'Unknown')}\n"
            status_text += f"心理年龄: {ai_info.get('age', 0)}岁\n"
            status_text += f"运行状态: {'运行中' if ai_info.get('is_running', False) else '已停止'}\n\n"
            
            # 情绪状态
            emotion_status = status_data.get("emotion_status", {})
            dominant_emotion = emotion_status.get("dominant_emotion", {})
            status_text += f"主导情绪: {dominant_emotion.get('type', 'calm')} ({dominant_emotion.get('intensity', '0%')})\n"
            status_text += f"社交满足度: {emotion_status.get('social_satisfaction', '0%')}\n"
            status_text += f"探索满足度: {emotion_status.get('exploration_satisfaction', '0%')}\n\n"
            
            # 感知状态
            perception_status = status_data.get("perception_status", {})
            status_text += "感知系统:\n"
            for perception_type, is_active in perception_status.items():
                status = "✅ 活跃" if is_active else "❌ 停止"
                status_text += f"  {perception_type}: {status}\n"
            status_text += "\n"
            
            # 行为状态
            behavior_status = status_data.get("behavior_status", {})
            status_text += f"行为队列长度: {behavior_status.get('queue_length', 0)}\n"
            status_text += f"最后主动时间: {behavior_status.get('last_proactive_time', 'Never')}\n\n"
            
            # 探索状态
            exploration_status = status_data.get("exploration_status", {})
            status_text += f"探索队列: {exploration_status.get('queue_size', 0)} 个任务\n"
            status_text += f"总探索次数: {exploration_status.get('total_explorations', 0)}\n"
            
            self.status_text.setText(status_text)
            
        except Exception as e:
            logger.error(f"更新状态显示失败: {e}")
            self.status_text.setText(f"状态更新失败: {e}")

class EmotionalUITabs(QTabWidget):
    """情绪化UI标签页容器"""
    
    # 信号定义
    thinking_triggered = pyqtSignal()
    search_triggered = pyqtSignal(str)
    perception_toggled = pyqtSignal(str, bool)
    capture_photo = pyqtSignal()
    capture_screenshot = pyqtSignal()
    manual_search = pyqtSignal(str)
    toggle_auto_exploration = pyqtSignal(bool)
    refresh_status = pyqtSignal()
    export_logs = pyqtSignal()
    clear_cache = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_tabs()
        
    def setup_tabs(self):
        """设置标签页"""
        # 情绪状态标签页
        self.emotion_widget = EmotionalStatusWidget()
        self.emotion_widget.thinking_button.clicked.connect(self.thinking_triggered.emit)
        self.emotion_widget.search_button.clicked.connect(lambda: self.search_triggered.emit(""))
        self.addTab(self.emotion_widget, "🎭 情绪状态")
        
        # 感知控制标签页
        self.perception_widget = PerceptionControlWidget()
        self.perception_widget.perception_toggled.connect(self.perception_toggled.emit)
        self.perception_widget.capture_photo.connect(self.capture_photo.emit)
        self.perception_widget.capture_screenshot.connect(self.capture_screenshot.emit)
        self.addTab(self.perception_widget, "👁️ 感知控制")
        
        # 知识探索标签页
        self.knowledge_widget = KnowledgeExplorationWidget()
        self.knowledge_widget.manual_search.connect(self.manual_search.emit)
        self.knowledge_widget.toggle_auto_exploration.connect(self.toggle_auto_exploration.emit)
        self.addTab(self.knowledge_widget, "🧠 知识探索")
        
        # 系统状态标签页
        self.status_widget = SystemStatusWidget()
        self.status_widget.refresh_status.connect(self.refresh_status.emit)
        self.status_widget.export_logs.connect(self.export_logs.emit)
        self.status_widget.clear_cache.connect(self.clear_cache.emit)
        self.addTab(self.status_widget, "📊 系统状态")
        
        # 样式设置
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 230);
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: rgba(200, 200, 200, 150);
                padding: 8px 12px;
                margin: 2px;
                border-radius: 5px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background-color: rgba(100, 150, 255, 200);
                color: white;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: rgba(150, 180, 255, 180);
            }
        """)
    
    def update_emotion_status(self, emotion_data: Dict[str, Any]):
        """更新情绪状态"""
        self.emotion_widget.update_emotion_status(emotion_data)
    
    def update_perception_status(self, status: Dict[str, bool]):
        """更新感知状态"""
        self.perception_widget.update_perception_status(status)
    
    def update_system_status(self, status_data: Dict[str, Any]):
        """更新系统状态"""
        self.status_widget.update_status(status_data)
    
    def add_exploration_result(self, result_text: str):
        """添加探索结果"""
        self.knowledge_widget.add_exploration_result(result_text)