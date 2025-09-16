#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asuna状态面板
显示Asuna的记忆阶段、SAO元素和特殊状态
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QGridLayout, QProgressBar, QTextEdit, QFrame,
    QScrollArea, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor

logger = logging.getLogger(__name__)

class AsunaStatusPanel(QWidget):
    """Asuna状态面板 - 显示Asuna的特殊状态信息"""
    
    memory_supplement_requested = pyqtSignal(str)  # 请求补充记忆
    sao_element_clicked = pyqtSignal(str)  # SAO元素被点击
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # 设置更新定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(3000)  # 每3秒更新一次
        
        # 状态回调
        self.status_callback = None
        
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # 标题
        title_label = QLabel("⚔️ Asuna状态面板")
        title_label.setFont(QFont("微软雅黑", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                background-color: rgba(180, 60, 80, 120);
                color: #FFE6F3;
                border-radius: 8px;
                padding: 8px;
                margin-bottom: 5px;
                border: 1px solid rgba(255, 120, 160, 80);
            }
        """)
        layout.addWidget(title_label)
        
        # AI状态显示
        self.ai_status_group = QGroupBox("AI状态")
        self.ai_status_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4A90E2;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #CCDDFF;
                background-color: rgba(30, 60, 120, 80);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #E6F3FF;
            }
        """)
        ai_layout = QVBoxLayout(self.ai_status_group)
        
        self.ai_status_label = QLabel("🤖 AI状态：检查中...")
        self.ai_status_label.setFont(QFont("微软雅黑", 9))
        self.ai_status_label.setStyleSheet("color: #8AB4FF; padding: 3px;")
        ai_layout.addWidget(self.ai_status_label)
        
        self.ai_config_button = QPushButton("配置AI")
        self.ai_config_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(74, 144, 226, 120);
                color: white;
                border: 1px solid #4A90E2;
                border-radius: 3px;
                padding: 3px;
                font-size: 9px;
            }
            QPushButton:hover {
                background-color: rgba(74, 144, 226, 180);
            }
        """)
        self.ai_config_button.clicked.connect(self.show_ai_config_help)
        ai_layout.addWidget(self.ai_config_button)
        
        layout.addWidget(self.ai_status_group)
        
        # 记忆阶段显示
        self.memory_stage_group = QGroupBox("记忆恢复阶段")
        self.memory_stage_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #FF6B8A;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #FFCCDD;
                background-color: rgba(180, 30, 60, 80);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #FFE6F3;
            }
        """)
        stage_layout = QVBoxLayout(self.memory_stage_group)
        
        self.stage_label = QLabel("当前阶段: 不安期")
        self.stage_label.setFont(QFont("微软雅黑", 10, QFont.Bold))
        self.stage_label.setStyleSheet("color: #FF8A9B; padding: 5px;")
        stage_layout.addWidget(self.stage_label)
        
        self.stage_progress = QProgressBar()
        self.stage_progress.setRange(0, 100)
        self.stage_progress.setValue(25)
        self.stage_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #FF6B8A;
                border-radius: 5px;
                text-align: center;
                background-color: rgba(100, 20, 40, 100);
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF8A9B, stop:1 #FF6B8A);
                border-radius: 3px;
            }
        """)
        stage_layout.addWidget(self.stage_progress)
        
        self.stage_description = QLabel("正在恢复基础身份记忆...")
        self.stage_description.setFont(QFont("微软雅黑", 9))
        self.stage_description.setStyleSheet("color: #FFCCDD; padding: 2px;")
        self.stage_description.setWordWrap(True)
        stage_layout.addWidget(self.stage_description)
        
        layout.addWidget(self.memory_stage_group)
        
        # 记忆碎片显示
        self.memory_fragments_group = QGroupBox("记忆碎片")
        self.memory_fragments_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #FF6B8A;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #FFCCDD;
                background-color: rgba(180, 30, 60, 80);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #FFE6F3;
            }
        """)
        fragments_layout = QVBoxLayout(self.memory_fragments_group)
        
        self.fragments_scroll = QScrollArea()
        self.fragments_scroll.setMaximumHeight(150)
        self.fragments_scroll.setWidgetResizable(True)
        self.fragments_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #FF6B8A;
                border-radius: 3px;
                background-color: rgba(100, 20, 40, 100);
            }
        """)
        
        self.fragments_widget = QWidget()
        self.fragments_layout = QVBoxLayout(self.fragments_widget)
        self.fragments_scroll.setWidget(self.fragments_widget)
        fragments_layout.addWidget(self.fragments_scroll)
        
        layout.addWidget(self.memory_fragments_group)
        
        # SAO元素显示
        self.sao_elements_group = QGroupBox("SAO元素")
        self.sao_elements_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #FF6B8A;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #FFCCDD;
                background-color: rgba(180, 30, 60, 80);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #FFE6F3;
            }
        """)
        sao_layout = QGridLayout(self.sao_elements_group)
        
        # SAO元素按钮
        self.sao_buttons = {}
        sao_elements = [
            ("细剑", "⚔️", "sword"),
            ("白色连衣裙", "👗", "dress"),
            ("血盟骑士团徽章", "🛡️", "badge"),
            ("22层小屋", "🏠", "floor_22"),
            ("炖肉", "🍲", "stew"),
            ("血盟骑士团", "⚔️", "guild")
        ]
        
        for i, (name, icon, key) in enumerate(sao_elements):
            btn = QPushButton(f"{icon} {name}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 107, 138, 100);
                    border: 1px solid #FF6B8A;
                    border-radius: 3px;
                    padding: 5px;
                    color: #FFE6F3;
                    font-size: 9px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 138, 155, 150);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 80, 120, 200);
                }
            """)
            btn.clicked.connect(lambda checked, k=key: self.sao_element_clicked.emit(k))
            self.sao_buttons[key] = btn
            sao_layout.addWidget(btn, i // 2, i % 2)
        
        layout.addWidget(self.sao_elements_group)
        
        # 交互统计
        self.stats_group = QGroupBox("交互统计")
        self.stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #FF6B8A;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #FFCCDD;
                background-color: rgba(180, 30, 60, 80);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #FFE6F3;
            }
        """)
        stats_layout = QVBoxLayout(self.stats_group)
        
        self.interaction_count_label = QLabel("交互次数: 0")
        self.care_count_label = QLabel("关怀次数: 0")
        self.tasks_completed_label = QLabel("完成任务: 0")
        
        for label in [self.interaction_count_label, self.care_count_label, self.tasks_completed_label]:
            label.setFont(QFont("微软雅黑", 9))
            label.setStyleSheet("color: #FFCCDD; padding: 2px;")
            stats_layout.addWidget(label)
        
        layout.addWidget(self.stats_group)
        
        # 记忆补充按钮
        self.supplement_button = QPushButton("💭 补充记忆")
        self.supplement_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 107, 138, 120);
                border: 2px solid #FF6B8A;
                border-radius: 5px;
                padding: 8px;
                color: #FFE6F3;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 138, 155, 150);
            }
        """)
        self.supplement_button.clicked.connect(self.request_memory_supplement)
        layout.addWidget(self.supplement_button)
        
        # 初始化显示
        self.update_display()
    
    def update_display(self):
        """更新显示"""
        try:
            # 这里应该从Asuna集成系统获取状态
            # 暂时使用模拟数据
            self.update_memory_stage("anxious", 25, "正在恢复基础身份记忆...")
            self.update_interaction_stats(0, 0, 0)
            self.update_memory_fragments([])
            self.update_ai_status()
            
        except Exception as e:
            logger.error(f"更新Asuna状态显示失败: {e}")
    
    def update_ai_status(self, ai_status: Optional[Dict[str, Any]] = None):
        """更新AI状态显示"""
        try:
            if ai_status is None:
                # 尝试从集成系统获取状态
                try:
                    from asuna_integration import get_asuna_integration
                    integration = get_asuna_integration()
                    if integration and integration.is_initialized:
                        status = integration.get_asuna_status()
                        ai_status = status.get('ai_generator_info', {})
                    else:
                        ai_status = {}
                except Exception:
                    ai_status = {}
            
            # 更新AI状态显示
            if ai_status.get('ai_available', False):
                self.ai_status_label.setText("🤖 AI状态：✅ 智能模式")
                self.ai_status_label.setStyleSheet("color: #4CAF50; padding: 3px;")
            elif ai_status.get('fallback_mode', False):
                self.ai_status_label.setText("🤖 AI状态：⚠️ 降级模式")
                self.ai_status_label.setStyleSheet("color: #FF9800; padding: 3px;")
            else:
                self.ai_status_label.setText("🤖 AI状态：❌ 未初始化")
                self.ai_status_label.setStyleSheet("color: #F44336; padding: 3px;")
                
        except Exception as e:
            logger.error(f"更新AI状态显示失败: {e}")
            self.ai_status_label.setText("🤖 AI状态：❌ 错误")
            self.ai_status_label.setStyleSheet("color: #F44336; padding: 3px;")
    
    def update_memory_stage(self, stage: str, progress: int, description: str):
        """更新记忆阶段"""
        stage_names = {
            "anxious": "不安期",
            "relaxed": "放松期", 
            "trusting": "信任期",
            "dependent": "依赖期"
        }
        
        stage_name = stage_names.get(stage, stage)
        self.stage_label.setText(f"当前阶段: {stage_name}")
        self.stage_progress.setValue(progress)
        self.stage_description.setText(description)
    
    def update_interaction_stats(self, interaction_count: int, care_count: int, tasks_completed: int):
        """更新交互统计"""
        self.interaction_count_label.setText(f"交互次数: {interaction_count}")
        self.care_count_label.setText(f"关怀次数: {care_count}")
        self.tasks_completed_label.setText(f"完成任务: {tasks_completed}")
    
    def update_memory_fragments(self, fragments: list):
        """更新记忆碎片显示"""
        # 清除现有碎片
        for i in reversed(range(self.fragments_layout.count())):
            self.fragments_layout.itemAt(i).widget().setParent(None)
        
        # 添加新碎片
        for fragment in fragments:
            fragment_widget = self.create_fragment_widget(fragment)
            self.fragments_layout.addWidget(fragment_widget)
    
    def create_fragment_widget(self, fragment: dict) -> QWidget:
        """创建记忆碎片组件"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                border: 1px solid #FF6B8A;
                border-radius: 3px;
                background-color: rgba(100, 20, 40, 100);
                margin: 2px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 碎片标题
        title = QLabel(f"💭 {fragment.get('id', 'Unknown')}")
        title.setFont(QFont("微软雅黑", 9, QFont.Bold))
        title.setStyleSheet("color: #FF8A9B;")
        layout.addWidget(title)
        
        # 碎片内容
        content = QLabel(fragment.get('content', ''))
        content.setFont(QFont("微软雅黑", 8))
        content.setStyleSheet("color: #FFCCDD;")
        content.setWordWrap(True)
        layout.addWidget(content)
        
        # 解锁状态
        status = "✅ 已解锁" if fragment.get('unlocked', False) else "🔒 未解锁"
        status_label = QLabel(status)
        status_label.setFont(QFont("微软雅黑", 8))
        status_label.setStyleSheet("color: #FF8A9B;")
        layout.addWidget(status_label)
        
        return widget
    
    def request_memory_supplement(self):
        """请求补充记忆"""
        self.memory_supplement_requested.emit("user_requested")
    
    def set_status_callback(self, callback):
        """设置状态回调"""
        self.status_callback = callback
    
    def get_asuna_status(self) -> Dict[str, Any]:
        """获取Asuna状态"""
        return {
            "memory_stage": self.stage_label.text(),
            "stage_progress": self.stage_progress.value(),
            "interaction_count": self.interaction_count_label.text(),
            "care_count": self.care_count_label.text(),
            "tasks_completed": self.tasks_completed_label.text()
        }
    
    def show_ai_config_help(self):
        """显示AI配置帮助"""
        help_text = """
🔧 AI配置帮助

1. 打开 config.json 文件
2. 找到 "api" 部分
3. 设置正确的 api_key：
   "api_key": "your_actual_api_key_here"
4. 设置正确的 base_url（如果需要）：
   "base_url": "https://api.openai.com/v1"
5. 保存文件并重启系统

💡 支持的AI服务：
• OpenAI API
• 其他兼容OpenAI格式的API服务
• 本地部署的LLM服务

⚠️ 当前状态：
• 如果显示"降级模式"，说明AI不可用
• 如果显示"智能模式"，说明AI正常工作
• 如果显示"未初始化"，说明系统正在启动

🔄 重启系统后AI状态会自动更新
        """
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("AI配置帮助")
        msg_box.setText(help_text)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

