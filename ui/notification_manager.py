#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI通知管理器
提供线程安全的UI通知机制，用于AI系统与桌面UI的交互
"""

import logging
import threading
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer, QMetaObject, Qt
from PyQt5.QtWidgets import QApplication

logger = logging.getLogger(__name__)

class NotificationManager(QObject):
    """UI通知管理器 - 负责管理AI与UI之间的通信"""
    
    # 信号定义
    ai_message_signal = pyqtSignal(str)  # AI主动消息
    ai_status_signal = pyqtSignal(dict)  # AI状态更新
    ai_emotion_signal = pyqtSignal(str, float)  # 情绪变化信号 (emotion_type, intensity)
    ai_activity_signal = pyqtSignal(str, str)  # 活动信号 (activity_type, description)
    system_notification_signal = pyqtSignal(str, str)  # 系统通知 (title, message)
    
    def __init__(self):
        super().__init__()
        self.ui_instance = None
        self.is_initialized = False
        self.message_queue = []
        self.max_queue_size = 50
        self.lock = threading.Lock()
        
        # 注册的回调函数
        self.callbacks = {
            'message': [],
            'status': [],
            'emotion': [],
            'activity': [],
            'notification': []
        }
        
    def initialize(self, ui_instance):
        """初始化通知管理器，绑定UI实例"""
        # 如果已经初始化过，先断开旧连接
        if self.is_initialized and self.ui_instance:
            try:
                # 断开旧的信号连接
                self.ai_message_signal.disconnect()
                self.ai_emotion_signal.disconnect()
                self.ai_status_signal.disconnect()
                self.ai_activity_signal.disconnect()
                logger.info("🔄 断开旧的UI连接")
            except:
                pass  # 忽略断开连接时的错误
        
        self.ui_instance = ui_instance
        self.is_initialized = True
        
        # 连接信号到UI方法（确保在主线程中连接）
        if hasattr(ui_instance, 'on_ai_proactive_message'):
            self.ai_message_signal.connect(ui_instance.on_ai_proactive_message, Qt.QueuedConnection)
            logger.info("✅ 连接AI消息信号到GUI")
        
        if hasattr(ui_instance, 'emotion_panel'):
            self.ai_emotion_signal.connect(self._update_emotion_panel, Qt.QueuedConnection)
            self.ai_status_signal.connect(self._update_status_panel, Qt.QueuedConnection)
            self.ai_activity_signal.connect(self._handle_activity_signal, Qt.QueuedConnection)
            logger.info("✅ 连接情绪面板信号到GUI")
        
        # 处理队列中的消息
        self._process_queued_messages()
        
        logger.info(f"✅ UI通知管理器初始化完成，UI实例: {type(ui_instance).__name__}")
        
    def send_ai_message(self, message: str, emotion_type: str = None, activity_type: str = None):
        """发送AI主动消息到UI（线程安全）"""
        try:
            # 添加时间戳和格式化
            timestamp = datetime.now().strftime("%H:%M")
            formatted_message = f"[{timestamp}] {message}"
            
            if self.is_initialized and self.ui_instance:
                # 检查是否有QApplication实例
                from PyQt5.QtWidgets import QApplication
                app = QApplication.instance()
                
                if app:
                    # 在PyQt环境中，优先使用直接调用，备用信号机制
                    logger.info(f"📤 通过信号发送AI消息到GUI: {message[:50]}...")
                    
                    # 🔥 修改策略：优先直接调用，确保消息到达
                    success = False
                    
                    # 方法1：直接调用UI方法（最可靠），跳过QTimer
                    if hasattr(self.ui_instance, 'on_ai_proactive_message'):
                        try:
                            logger.debug("🎯 尝试直接调用on_ai_proactive_message")
                            
                            # 🔥 重要修改：直接调用，不通过QTimer
                            logger.debug("🔥 绕过QTimer，直接同步调用UI更新")
                            
                            # 直接调用add_ai_message，跳过复杂的事件循环
                            if hasattr(self.ui_instance, 'add_ai_message'):
                                ai_name = "StarryNight"  # 硬编码避免config导入问题
                                logger.debug(f"🔄 直接调用add_ai_message: {formatted_message[:30]}...")
                                self.ui_instance.add_ai_message(ai_name, formatted_message, "ai_proactive")
                                logger.info("✅ 直接add_ai_message成功")
                                success = True
                            
                            # 备用：调用on_ai_proactive_message（如果add_ai_message失败）
                            if not success:
                                logger.debug("🔄 add_ai_message失败，尝试on_ai_proactive_message")
                                self.ui_instance.on_ai_proactive_message(formatted_message)
                                logger.info("✅ 直接调用UI方法成功")
                                success = True
                                
                        except Exception as direct_error:
                            logger.error(f"❌ 直接调用UI方法失败: {direct_error}")
                            import traceback
                            logger.error(traceback.format_exc())
                    
                    # 方法2：如果直接调用失败，尝试信号机制
                    if not success:
                        try:
                            logger.debug("🎯 尝试信号发射")
                            self._emit_signal_safe('ai_message_signal', formatted_message)
                            logger.debug("✅ 信号发射成功")
                            success = True
                        except Exception as signal_error:
                            logger.error(f"❌ 信号发射失败: {signal_error}")
                    
                    # 方法3：最后的备用方案 - 强制UI更新
                    if not success and hasattr(self.ui_instance, 'text'):
                        try:
                            logger.debug("🎯 尝试强制UI更新")
                            from PyQt5.QtCore import QTimer
                            def force_update():
                                try:
                                    self.ui_instance.text.append(f"🤖 StarryNight: {formatted_message}")
                                    self.ui_instance.text.ensureCursorVisible()
                                    logger.info("✅ 强制UI更新成功")
                                except Exception as e:
                                    logger.error(f"❌ 强制UI更新失败: {e}")
                            QTimer.singleShot(0, force_update)
                            success = True
                        except Exception as force_error:
                            logger.error(f"❌ 强制UI更新失败: {force_error}")
                    
                    if not success:
                        logger.error("❌ 所有GUI更新方法都失败了！")
                    
                    # 如果有情绪信息，也发送情绪信号
                    if emotion_type:
                        self._emit_signal_safe('ai_emotion_signal', emotion_type, 0.7)
                        
                    # 如果有活动信息，也发送活动信号
                    if activity_type:
                        self._emit_signal_safe('ai_activity_signal', activity_type, message)
                else:
                    # 非PyQt环境（如测试），直接调用UI方法
                    logger.debug("无PyQt环境，直接调用UI方法")
                    if hasattr(self.ui_instance, 'on_ai_proactive_message'):
                        self.ui_instance.on_ai_proactive_message(formatted_message)
                    
                    # 直接调用其他方法（如果存在）
                    if emotion_type and hasattr(self.ui_instance, 'update_emotion'):
                        self.ui_instance.update_emotion(emotion_type, 0.7)
                    
                    if activity_type and hasattr(self.ui_instance, 'update_activity_status'):
                        self.ui_instance.update_activity_status(activity_type, message)
                    
            else:
                # UI未初始化，加入队列
                self._queue_message('message', {
                    'content': formatted_message,
                    'emotion_type': emotion_type,
                    'activity_type': activity_type
                })
                
            # 调用注册的回调（在当前线程中）
            for callback in self.callbacks['message']:
                try:
                    callback(formatted_message)
                except Exception as e:
                    logger.error(f"消息回调失败: {e}")
                    
        except Exception as e:
            logger.error(f"发送AI消息失败: {e}")
            
    def send_status_update(self, status_data: Dict[str, Any]):
        """发送AI状态更新（线程安全）"""
        try:
            if self.is_initialized and self.ui_instance:
                self._emit_signal_safe('ai_status_signal', status_data)
            else:
                self._queue_message('status', status_data)
                
            # 调用注册的回调
            for callback in self.callbacks['status']:
                try:
                    callback(status_data)
                except Exception as e:
                    logger.error(f"状态回调失败: {e}")
                    
        except Exception as e:
            logger.error(f"发送状态更新失败: {e}")
            
    def send_emotion_update(self, emotion_type: str, intensity: float):
        """发送情绪更新（线程安全）"""
        try:
            if self.is_initialized and self.ui_instance:
                self._emit_signal_safe('ai_emotion_signal', emotion_type, intensity)
            else:
                self._queue_message('emotion', {'type': emotion_type, 'intensity': intensity})
                
            # 调用注册的回调
            for callback in self.callbacks['emotion']:
                try:
                    callback(emotion_type, intensity)
                except Exception as e:
                    logger.error(f"情绪回调失败: {e}")
                    
        except Exception as e:
            logger.error(f"发送情绪更新失败: {e}")
            
    def send_activity_notification(self, activity_type: str, description: str):
        """发送活动通知（线程安全）"""
        try:
            if self.is_initialized and self.ui_instance:
                self._emit_signal_safe('ai_activity_signal', activity_type, description)
                # 直接更新活动状态（使用线程安全的方式）
                self._safe_invoke_method(self._update_activity_status, activity_type, description)
            else:
                self._queue_message('activity', {'type': activity_type, 'description': description})
                
            # 调用注册的回调
            for callback in self.callbacks['activity']:
                try:
                    callback(activity_type, description)
                except Exception as e:
                    logger.error(f"活动回调失败: {e}")
                    
        except Exception as e:
            logger.error(f"发送活动通知失败: {e}")
            
    def send_system_notification(self, title: str, message: str):
        """发送系统通知（线程安全）"""
        try:
            if self.is_initialized and self.ui_instance:
                self._emit_signal_safe('system_notification_signal', title, message)
            else:
                self._queue_message('notification', {'title': title, 'message': message})
                
            # 调用注册的回调
            for callback in self.callbacks['notification']:
                try:
                    callback(title, message)
                except Exception as e:
                    logger.error(f"通知回调失败: {e}")
                    
        except Exception as e:
            logger.error(f"发送系统通知失败: {e}")
    
    def _emit_signal_safe(self, signal_name: str, *args):
        """线程安全的信号发射"""
        try:
            # 检查是否在主线程中
            app = QApplication.instance()
            current_thread = QThread.currentThread()
            main_thread = app.thread() if app else None
            
            logger.debug(f"🔍 信号发射调试: {signal_name}")
            logger.debug(f"  - 当前线程: {current_thread}")
            logger.debug(f"  - 主线程: {main_thread}")
            logger.debug(f"  - 是否在主线程: {current_thread == main_thread}")
            
            if app and main_thread == current_thread:
                # 在主线程中，直接发射信号
                logger.debug("📡 直接发射信号")
                signal = getattr(self, signal_name)
                signal.emit(*args)
                logger.debug("✅ 信号发射完成")
            else:
                # 不在主线程中，使用QTimer.singleShot在主线程中发射信号
                logger.debug("📡 通过QTimer在主线程中发射信号")
                def emit_in_main_thread():
                    try:
                        logger.debug(f"🎯 主线程中执行信号发射: {signal_name}")
                        signal = getattr(self, signal_name)
                        signal.emit(*args)
                        logger.debug("✅ 主线程信号发射完成")
                    except Exception as e:
                        logger.error(f"❌ 主线程信号发射失败: {e}")
                
                QTimer.singleShot(0, emit_in_main_thread)
                logger.debug("📋 QTimer.singleShot已调用")
                
        except Exception as e:
            logger.error(f"❌ 线程安全信号发射失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    def _safe_invoke_method(self, method, *args, **kwargs):
        """线程安全的方法调用"""
        try:
            app = QApplication.instance()
            if app and app.thread() == QThread.currentThread():
                # 在主线程中，直接调用
                method(*args, **kwargs)
            else:
                # 不在主线程中，使用QTimer在主线程中调用
                QTimer.singleShot(0, lambda: method(*args, **kwargs))
        except Exception as e:
            logger.error(f"线程安全方法调用失败: {e}")
            
    def register_callback(self, event_type: str, callback: Callable):
        """注册回调函数"""
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
            logger.info(f"注册回调: {event_type}")
        else:
            logger.error(f"不支持的事件类型: {event_type}")
            
    def unregister_callback(self, event_type: str, callback: Callable):
        """取消注册回调函数"""
        if event_type in self.callbacks and callback in self.callbacks[event_type]:
            self.callbacks[event_type].remove(callback)
            logger.info(f"取消注册回调: {event_type}")
            
    def _queue_message(self, msg_type: str, data: Any):
        """将消息加入队列"""
        with self.lock:
            if len(self.message_queue) >= self.max_queue_size:
                # 移除最旧的消息
                self.message_queue.pop(0)
                
            self.message_queue.append({
                'type': msg_type,
                'data': data,
                'timestamp': datetime.now()
            })
            
    def _process_queued_messages(self):
        """处理队列中的消息"""
        with self.lock:
            for msg in self.message_queue:
                try:
                    msg_type = msg['type']
                    data = msg['data']
                    
                    if msg_type == 'message':
                        self.ai_message_signal.emit(data['content'])
                        if data.get('emotion_type'):
                            self.ai_emotion_signal.emit(data['emotion_type'], 0.7)
                        if data.get('activity_type'):
                            self.ai_activity_signal.emit(data['activity_type'], data['content'])
                            
                    elif msg_type == 'status':
                        self.ai_status_signal.emit(data)
                        
                    elif msg_type == 'emotion':
                        self.ai_emotion_signal.emit(data['type'], data['intensity'])
                        
                    elif msg_type == 'activity':
                        self.ai_activity_signal.emit(data['type'], data['description'])
                        
                    elif msg_type == 'notification':
                        self.system_notification_signal.emit(data['title'], data['message'])
                        
                except Exception as e:
                    logger.error(f"处理队列消息失败: {e}")
                    
            # 清空队列
            self.message_queue.clear()
            
    def _update_emotion_panel(self, emotion_type: str, intensity: float):
        """更新情绪面板（线程安全）"""
        try:
            if hasattr(self.ui_instance, 'emotion_panel') and self.ui_instance.emotion_panel:
                emotion_panel = self.ui_instance.emotion_panel
                if hasattr(emotion_panel, 'update_emotion'):
                    self._safe_invoke_method(emotion_panel.update_emotion, emotion_type, intensity)
        except Exception as e:
            logger.error(f"更新情绪面板失败: {e}")
            
    def _update_status_panel(self, status_data: Dict[str, Any]):
        """更新状态面板（线程安全）"""
        try:
            if hasattr(self.ui_instance, 'emotion_panel') and self.ui_instance.emotion_panel:
                emotion_panel = self.ui_instance.emotion_panel
                if hasattr(emotion_panel, 'update_status'):
                    self._safe_invoke_method(emotion_panel.update_status, status_data)
        except Exception as e:
            logger.error(f"更新状态面板失败: {e}")
    
    def _update_activity_status(self, activity_type: str, description: str):
        """更新活动状态（线程安全）"""
        try:
            if hasattr(self.ui_instance, 'emotion_panel') and self.ui_instance.emotion_panel:
                emotion_panel = self.ui_instance.emotion_panel
                if hasattr(emotion_panel, 'update_activity_status'):
                    self._safe_invoke_method(emotion_panel.update_activity_status, activity_type, description)
                if hasattr(emotion_panel, 'add_activity_notification'):
                    self._safe_invoke_method(emotion_panel.add_activity_notification, description, activity_type)
        except Exception as e:
            logger.error(f"更新活动状态失败: {e}")
    
    def _handle_activity_signal(self, activity_type: str, description: str):
        """处理活动信号"""
        try:
            self._update_activity_status(activity_type, description)
        except Exception as e:
            logger.error(f"处理活动信号失败: {e}")

# 全局实例
_notification_manager = None
_init_lock = threading.Lock()

def get_notification_manager() -> NotificationManager:
    """获取全局通知管理器实例"""
    global _notification_manager
    if _notification_manager is None:
        with _init_lock:
            if _notification_manager is None:
                _notification_manager = NotificationManager()
    return _notification_manager

def initialize_ui_notifications(ui_instance):
    """初始化UI通知系统"""
    manager = get_notification_manager()
    manager.initialize(ui_instance)
    return manager