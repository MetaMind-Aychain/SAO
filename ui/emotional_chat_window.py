# ui/emotional_chat_window.py
"""
情绪化聊天窗口 - 集成情绪AI功能的PyQt界面
继承原有ChatWindow并添加情绪化功能
"""

import sys
import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QSplitter, QTextEdit, QLineEdit, QPushButton, QLabel, QFrame,
    QMessageBox, QFileDialog, QDesktopWidget
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor

# 导入原有聊天窗口
from .pyqt_chat_window import ChatWindow, TitleBar

# 导入情绪化UI扩展
from .emotional_ui_extension import EmotionalUITabs

# 导入情绪化AI管理器
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from emotional_ai.emotional_ai_manager import get_emotional_ai_manager

logger = logging.getLogger(__name__)

class EmotionalChatWindow(ChatWindow):
    """情绪化聊天窗口"""
    
    def __init__(self):
        # 先初始化情绪AI管理器
        self.emotional_ai = get_emotional_ai_manager()
        
        # 调用父类构造函数
        super().__init__()
        
        # 添加情绪化功能
        self.setup_emotional_features()
        
        # 设置定时器更新状态
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)  # 每5秒更新一次
        
        # 连接情绪AI回调
        self.emotional_ai.add_message_callback(self.handle_ai_message)
        
    def setup_emotional_features(self):
        """设置情绪化功能"""
        try:
            # 创建情绪化UI标签页
            self.emotion_tabs = EmotionalUITabs()
            
            # 连接信号
            self.emotion_tabs.thinking_triggered.connect(self.trigger_thinking)
            self.emotion_tabs.search_triggered.connect(self.trigger_search)
            self.emotion_tabs.perception_toggled.connect(self.toggle_perception)
            self.emotion_tabs.capture_photo.connect(self.capture_photo)
            self.emotion_tabs.capture_screenshot.connect(self.capture_screenshot)
            self.emotion_tabs.manual_search.connect(self.manual_search)
            self.emotion_tabs.toggle_auto_exploration.connect(self.toggle_auto_exploration)
            self.emotion_tabs.refresh_status.connect(self.refresh_status)
            self.emotion_tabs.export_logs.connect(self.export_logs)
            self.emotion_tabs.clear_cache.connect(self.clear_cache)
            
            # 将情绪标签页添加到主界面
            if hasattr(self, 'main_splitter'):
                # 如果主界面有splitter，添加到右侧
                self.main_splitter.addWidget(self.emotion_tabs)
                self.main_splitter.setSizes([600, 400])  # 调整比例
            else:
                # 否则创建新的布局
                self.create_emotional_layout()
                
        except Exception as e:
            logger.error(f"设置情绪化功能失败: {e}")
    
    def create_emotional_layout(self):
        """创建包含情绪功能的布局"""
        try:
            # 获取原有的中央组件
            original_widget = self.centralWidget()
            
            # 创建新的中央组件
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # 创建水平分割器
            self.main_splitter = QSplitter(Qt.Horizontal)
            
            # 添加原有组件和情绪标签页
            self.main_splitter.addWidget(original_widget)
            self.main_splitter.addWidget(self.emotion_tabs)
            
            # 设置比例
            self.main_splitter.setSizes([700, 350])
            
            # 创建主布局
            main_layout = QHBoxLayout(central_widget)
            main_layout.addWidget(self.main_splitter)
            main_layout.setContentsMargins(0, 0, 0, 0)
            
        except Exception as e:
            logger.error(f"创建情绪布局失败: {e}")
    
    def start_emotional_ai(self):
        """启动情绪AI系统"""
        try:
            asyncio.create_task(self.emotional_ai.start_emotional_ai())
            self.add_message_to_chat("系统", "情绪AI系统已启动！StarryNight醒过来啦～", "system")
        except Exception as e:
            logger.error(f"启动情绪AI失败: {e}")
            self.add_message_to_chat("系统", f"启动情绪AI失败: {e}", "error")
    
    def stop_emotional_ai(self):
        """停止情绪AI系统"""
        try:
            self.emotional_ai.stop_emotional_ai()
            self.add_message_to_chat("系统", "情绪AI系统已停止", "system")
        except Exception as e:
            logger.error(f"停止情绪AI失败: {e}")
    
    async def handle_ai_message(self, ai_message: Dict[str, Any]):
        """处理AI消息回调"""
        try:
            message = ai_message.get("message", "")
            sender = ai_message.get("sender", "AI")
            message_type = ai_message.get("type", "proactive")
            emotion = ai_message.get("emotion", "")
            
            # 在聊天界面显示消息
            display_message = f"{message}"
            if emotion:
                display_message += f" [{emotion}]"
            
            self.add_message_to_chat(sender, display_message, "ai_proactive")
            
        except Exception as e:
            logger.error(f"处理AI消息失败: {e}")
    
    def send_message_override(self, message: str):
        """重写发送消息方法，集成情绪AI处理"""
        try:
            # 调用原有的发送逻辑
            super().send_message(message)
            
            # 同时让情绪AI处理用户输入
            if hasattr(self.emotional_ai, 'process_user_input'):
                asyncio.create_task(self._process_emotional_response(message))
                
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
    
    async def _process_emotional_response(self, user_input: str):
        """处理情绪化响应"""
        try:
            emotional_response = await self.emotional_ai.process_user_input(user_input)
            if emotional_response:
                # 显示情绪化回复（可选，因为原有系统已经有回复了）
                pass
        except Exception as e:
            logger.error(f"处理情绪响应失败: {e}")
    
    # 情绪控制槽函数
    @pyqtSlot()
    def trigger_thinking(self):
        """触发自主思考"""
        try:
            asyncio.create_task(self.emotional_ai.manual_trigger_thinking())
        except Exception as e:
            logger.error(f"触发思考失败: {e}")
    
    @pyqtSlot(str)
    def trigger_search(self, query: str):
        """触发搜索"""
        try:
            asyncio.create_task(self.emotional_ai.manual_search_knowledge(query))
        except Exception as e:
            logger.error(f"触发搜索失败: {e}")
    
    @pyqtSlot(str, bool)
    def toggle_perception(self, perception_type: str, enabled: bool):
        """切换感知功能"""
        try:
            asyncio.create_task(self.emotional_ai.toggle_perception(perception_type, enabled))
        except Exception as e:
            logger.error(f"切换感知失败: {e}")
    
    @pyqtSlot()
    def capture_photo(self):
        """拍照"""
        try:
            asyncio.create_task(self.emotional_ai.capture_photo())
        except Exception as e:
            logger.error(f"拍照失败: {e}")
    
    @pyqtSlot()
    def capture_screenshot(self):
        """截图"""
        try:
            asyncio.create_task(self.emotional_ai.capture_screenshot())
        except Exception as e:
            logger.error(f"截图失败: {e}")
    
    @pyqtSlot(str)
    def manual_search(self, query: str):
        """手动搜索"""
        try:
            asyncio.create_task(self.emotional_ai.manual_search_knowledge(query))
        except Exception as e:
            logger.error(f"手动搜索失败: {e}")
    
    @pyqtSlot(bool)
    def toggle_auto_exploration(self, enabled: bool):
        """切换自动探索"""
        try:
            if enabled:
                asyncio.create_task(self.emotional_ai.exploration_engine.start_auto_exploration())
            else:
                self.emotional_ai.exploration_engine.stop_auto_exploration()
        except Exception as e:
            logger.error(f"切换自动探索失败: {e}")
    
    @pyqtSlot()
    def refresh_status(self):
        """刷新状态"""
        self.update_status()
    
    @pyqtSlot()
    def export_logs(self):
        """导出日志"""
        try:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(
                self, "导出日志", f"emotional_ai_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "JSON files (*.json)"
            )
            
            if file_path:
                status_data = self.emotional_ai.get_system_status()
                with open(file_path, 'w', encoding='utf-8') as f:
                    import json
                    json.dump(status_data, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "导出成功", f"日志已导出到: {file_path}")
                
        except Exception as e:
            logger.error(f"导出日志失败: {e}")
            QMessageBox.warning(self, "导出失败", f"导出日志失败: {e}")
    
    @pyqtSlot()
    def clear_cache(self):
        """清理缓存"""
        try:
            reply = QMessageBox.question(
                self, "确认清理", "确定要清理缓存吗？这将清除AI的一些临时数据。",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # 清理各种缓存
                self.emotional_ai.emotion_engine.interaction_history.clear()
                self.emotional_ai.exploration_engine.exploration_history.clear()
                
                QMessageBox.information(self, "清理完成", "缓存已清理完成")
                
        except Exception as e:
            logger.error(f"清理缓存失败: {e}")
            QMessageBox.warning(self, "清理失败", f"清理缓存失败: {e}")
    
    def update_status(self):
        """更新状态显示"""
        try:
            # 获取系统状态
            status_data = self.emotional_ai.get_system_status()
            
            # 更新各个组件
            if hasattr(self, 'emotion_tabs'):
                # 更新情绪状态
                emotion_status = status_data.get("emotion_status", {})
                self.emotion_tabs.update_emotion_status(emotion_status)
                
                # 更新感知状态
                perception_status = status_data.get("perception_status", {})
                self.emotion_tabs.update_perception_status(perception_status)
                
                # 更新系统状态
                self.emotion_tabs.update_system_status(status_data)
                
        except Exception as e:
            logger.error(f"更新状态失败: {e}")
    
    def add_message_to_chat(self, sender: str, message: str, message_type: str = "normal"):
        """添加消息到聊天框（重写以支持情绪消息）"""
        try:
            # 根据消息类型设置不同样式
            if message_type == "ai_proactive":
                # AI主动消息用特殊样式
                formatted_message = f"<div style='background-color: rgba(255, 182, 193, 0.3); padding: 5px; border-radius: 5px; margin: 2px;'><b>{sender}:</b> {message}</div>"
            elif message_type == "system":
                # 系统消息
                formatted_message = f"<div style='background-color: rgba(173, 216, 230, 0.3); padding: 5px; border-radius: 5px; margin: 2px;'><b>[系统]:</b> {message}</div>"
            elif message_type == "error":
                # 错误消息
                formatted_message = f"<div style='background-color: rgba(255, 99, 71, 0.3); padding: 5px; border-radius: 5px; margin: 2px;'><b>[错误]:</b> {message}</div>"
            else:
                # 普通消息
                formatted_message = f"<b>{sender}:</b> {message}"
            
            # 添加到聊天框
            if hasattr(self, 'chat_display') and self.chat_display:
                self.chat_display.append(formatted_message)
                self.chat_display.ensureCursorVisible()
            
        except Exception as e:
            logger.error(f"添加消息到聊天框失败: {e}")
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        try:
            # 停止情绪AI系统
            self.stop_emotional_ai()
            
            # 停止定时器
            if hasattr(self, 'status_timer'):
                self.status_timer.stop()
            
            # 调用父类关闭事件
            super().closeEvent(event)
            
        except Exception as e:
            logger.error(f"关闭窗口失败: {e}")
            event.accept()
    
    def showEvent(self, event):
        """窗口显示事件"""
        try:
            # 调用父类显示事件
            super().showEvent(event)
            
            # 启动情绪AI系统
            self.start_emotional_ai()
            
        except Exception as e:
            logger.error(f"显示窗口失败: {e}")

def main():
    """主函数"""
    try:
        app = QApplication(sys.argv)
        
        # 设置应用程序属性
        app.setApplicationName("NagaAgent - 情绪化AI助手")
        app.setApplicationVersion("3.0")
        
        # 创建并显示窗口
        window = EmotionalChatWindow()
        
        # 居中显示
        desktop = QDesktopWidget()
        screen_rect = desktop.screenGeometry()
        window_rect = window.geometry()
        x = (screen_rect.width() - window_rect.width()) // 2
        y = (screen_rect.height() - window_rect.height()) // 2
        window.move(x, y)
        
        window.show()
        
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"启动应用失败: {e}")
        print(f"启动应用失败: {e}")

if __name__ == "__main__":
    main()