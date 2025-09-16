#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asuna AI状态显示系统
提供AI连接状态和降级模式的用户友好提示
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class AsunaAIStatusDisplay:
    """Asuna AI状态显示管理器"""
    
    def __init__(self):
        self.last_status_check = None
        self.status_history = []
        
    def get_ai_status_message(self, ai_status: Dict[str, Any]) -> str:
        """获取AI状态消息"""
        if not ai_status:
            return "❌ AI状态信息不可用"
        
        if ai_status.get('ai_available', False):
            return "✅ AI连接正常 - 使用智能回复模式"
        elif ai_status.get('fallback_mode', False):
            return "⚠️ AI不可用 - 使用降级模式（固定回复）"
        else:
            return "❌ AI系统未初始化"
    
    def get_detailed_status_info(self, ai_status: Dict[str, Any]) -> Dict[str, Any]:
        """获取详细状态信息"""
        if not ai_status:
            return {
                "status": "error",
                "message": "AI状态信息不可用",
                "recommendations": ["检查系统配置", "重新初始化AI系统"]
            }
        
        status_info = {
            "ai_available": ai_status.get('ai_available', False),
            "fallback_mode": ai_status.get('fallback_mode', False),
            "client_initialized": ai_status.get('client_initialized', False),
            "subsystems_loaded": ai_status.get('subsystems_loaded', False),
            "last_check": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 生成状态消息
        if status_info['ai_available']:
            status_info['message'] = "AI系统运行正常"
            status_info['recommendations'] = []
        elif status_info['fallback_mode']:
            status_info['message'] = "AI不可用，使用降级模式"
            status_info['recommendations'] = [
                "在config.json中配置正确的API密钥",
                "检查网络连接",
                "验证API服务是否可用"
            ]
        else:
            status_info['message'] = "AI系统未正确初始化"
            status_info['recommendations'] = [
                "检查API配置",
                "重新启动系统",
                "查看错误日志"
            ]
        
        return status_info
    
    def get_user_friendly_message(self, ai_status: Dict[str, Any]) -> str:
        """获取用户友好的状态消息"""
        if not ai_status:
            return "🤖 Asuna AI状态：系统错误，请检查配置"
        
        if ai_status.get('ai_available', False):
            return "🤖 Asuna AI状态：✅ 智能模式 - 我可以进行真实的AI对话"
        elif ai_status.get('fallback_mode', False):
            return "🤖 Asuna AI状态：⚠️ 降级模式 - 我只能使用预设回复，请配置AI以启用智能对话"
        else:
            return "🤖 Asuna AI状态：❌ 未初始化 - 系统正在启动中..."
    
    def get_configuration_help(self) -> str:
        """获取配置帮助信息"""
        return """
🔧 AI配置帮助：

1. 打开 config.json 文件
2. 找到 "api" 部分
3. 设置正确的 api_key：
   "api_key": "your_actual_api_key_here"
4. 设置正确的 base_url（如果需要）：
   "base_url": "https://api.openai.com/v1"
5. 保存文件并重启系统

💡 支持的AI服务：
- OpenAI API
- 其他兼容OpenAI格式的API服务
- 本地部署的LLM服务
        """
    
    def format_status_for_ui(self, ai_status: Dict[str, Any]) -> Dict[str, Any]:
        """为UI格式化状态信息"""
        status_info = self.get_detailed_status_info(ai_status)
        
        return {
            "display_message": self.get_user_friendly_message(ai_status),
            "status_icon": self._get_status_icon(ai_status),
            "is_ai_available": status_info['ai_available'],
            "is_fallback_mode": status_info['fallback_mode'],
            "recommendations": status_info['recommendations'],
            "last_check": status_info['last_check'],
            "configuration_help": self.get_configuration_help() if not status_info['ai_available'] else None
        }
    
    def _get_status_icon(self, ai_status: Dict[str, Any]) -> str:
        """获取状态图标"""
        if not ai_status:
            return "❌"
        
        if ai_status.get('ai_available', False):
            return "✅"
        elif ai_status.get('fallback_mode', False):
            return "⚠️"
        else:
            return "❌"
    
    def log_status_change(self, old_status: Dict[str, Any], new_status: Dict[str, Any]):
        """记录状态变化"""
        if old_status != new_status:
            change_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.status_history.append({
                "timestamp": change_time,
                "old_status": old_status,
                "new_status": new_status
            })
            
            # 保持历史记录在合理范围内
            if len(self.status_history) > 10:
                self.status_history.pop(0)
            
            logger.info(f"Asuna AI状态变化: {old_status} -> {new_status}")

# 全局实例
_ai_status_display = None

def get_ai_status_display() -> AsunaAIStatusDisplay:
    """获取AI状态显示实例"""
    global _ai_status_display
    if _ai_status_display is None:
        _ai_status_display = AsunaAIStatusDisplay()
    return _ai_status_display


