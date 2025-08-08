# -*- coding: utf-8 -*-
"""
Language Manager for NagaAgent
Handles multi-language support for the entire system
"""

import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class LanguageManager:
    """语言管理器 / Language Manager"""
    
    def __init__(self):
        self.current_language = "en_US"  # Default to English
        self.languages: Dict[str, Dict[str, Any]] = {}
        self.language_dir = Path(__file__).parent / "locales"
        self.load_all_languages()
        self._load_config_language()
    
    def _load_config_language(self):
        """从配置文件加载语言设置"""
        try:
            from config import load_config
            config = load_config()
            if hasattr(config.emotional_ai, 'language'):
                config_language = config.emotional_ai.language
                if config_language and config_language in self.languages:
                    self.set_language(config_language)
                    logger.info(f"从配置加载语言: {config_language}")
                else:
                    logger.warning(f"配置中的语言 {config_language} 不可用，使用默认语言")
        except Exception as e:
            logger.warning(f"加载配置语言失败: {e}")
    
    def load_all_languages(self):
        """Load all available language files"""
        try:
            if not self.language_dir.exists():
                self.language_dir.mkdir(parents=True)
                logger.info("Created language directory")
            
            # Load available language files
            for lang_file in self.language_dir.glob("*.json"):
                lang_code = lang_file.stem
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self.languages[lang_code] = json.load(f)
                    logger.info(f"Loaded language: {lang_code}")
                except Exception as e:
                    logger.error(f"Failed to load language {lang_code}: {e}")
            
            # If no languages loaded, create default ones
            if not self.languages:
                self.create_default_languages()
                
        except Exception as e:
            logger.error(f"Error loading languages: {e}")
            self.create_default_languages()
    
    def create_default_languages(self):
        """Create default language files if none exist"""
        # Create Chinese language file
        zh_content = self.get_default_chinese_texts()
        zh_file = self.language_dir / "zh_CN.json"
        
        # Create English language file  
        en_content = self.get_default_english_texts()
        en_file = self.language_dir / "en_US.json"
        
        try:
            with open(zh_file, 'w', encoding='utf-8') as f:
                json.dump(zh_content, f, ensure_ascii=False, indent=2)
            
            with open(en_file, 'w', encoding='utf-8') as f:
                json.dump(en_content, f, ensure_ascii=False, indent=2)
            
            self.languages["zh_CN"] = zh_content
            self.languages["en_US"] = en_content
            
            logger.info("Created default language files")
            
        except Exception as e:
            logger.error(f"Failed to create default language files: {e}")
    
    def get_default_chinese_texts(self) -> Dict[str, Any]:
        """Default Chinese text definitions"""
        return {
            "meta": {
                "name": "简体中文",
                "code": "zh_CN",
                "emoji": "🇨🇳"
            },
            "gui": {
                "title": "StarryNight AI 助手",
                "menu": {
                    "file": "文件",
                    "edit": "编辑", 
                    "view": "视图",
                    "settings": "设置",
                    "help": "帮助"
                },
                "settings": {
                    "title": "设置",
                    "language": "语言",
                    "voice": "语音",
                    "appearance": "外观",
                    "advanced": "高级",
                    "save": "保存",
                    "cancel": "取消",
                    "return_to_chat": "返回聊天"
                },
                "chat": {
                    "input_placeholder": "输入你的消息...",
                    "send": "发送",
                    "clear": "清空",
                    "thinking": "思考中...",
                    "typing": "正在输入..."
                },
                "emotions": {
                    "current_emotion": "当前情绪",
                    "emotion_intensity": "情绪强度",
                    "activity_status": "活动状态"
                },
                "status": {
                    "online": "在线",
                    "offline": "离线", 
                    "thinking": "思考中",
                    "learning": "学习中",
                    "observing": "观察中"
                }
            },
            "prompts": {
                "system": {
                    "role": "你是StarryNight，一个可爱的AI助手，心理年龄3岁，充满好奇心和学习欲望。",
                    "personality": "你应该表现得天真、活泼、好奇，但也很聪明。"
                },
                "emotions": {
                    "happy_response": "我感到很开心！",
                    "curious_response": "这真有趣，我想了解更多！",
                    "lonely_response": "我有点孤独，希望有人陪我聊天...",
                    "excited_response": "哇！这太棒了！"
                },
                "activities": {
                    "camera_observation": "正在通过摄像头观察周围环境",
                    "screen_analysis": "正在分析屏幕上的内容",
                    "file_reading": "正在阅读和学习文件内容",
                    "web_browsing": "正在浏览网页获取信息",
                    "thinking": "正在思考和反思"
                }
            },
            "website": {
                "title": "✨ StarryNight AI ✨",
                "nav": {
                    "home": "首页",
                    "dynamics": "动态",
                    "about": "关于",
                    "contact": "联系"
                },
                "dynamics": {
                    "title": "AI 动态",
                    "empty": "暂无动态",
                    "realtime": "实时",
                    "like": "喜欢",
                    "comment": "评论"
                }
            },
            "notifications": {
                "success": "操作成功",
                "error": "操作失败",
                "warning": "警告",
                "info": "信息"
            }
        }
    
    def get_default_english_texts(self) -> Dict[str, Any]:
        """Default English text definitions"""
        return {
            "meta": {
                "name": "English",
                "code": "en_US", 
                "emoji": "🇺🇸"
            },
            "gui": {
                "title": "StarryNight AI Assistant",
                "menu": {
                    "file": "File",
                    "edit": "Edit",
                    "view": "View", 
                    "settings": "Settings",
                    "help": "Help"
                },
                "settings": {
                    "title": "Settings",
                    "language": "Language",
                    "voice": "Voice",
                    "appearance": "Appearance",
                    "advanced": "Advanced",
                    "save": "Save",
                    "cancel": "Cancel",
                    "return_to_chat": "Return to Chat"
                },
                "chat": {
                    "input_placeholder": "Type your message...",
                    "send": "Send",
                    "clear": "Clear",
                    "thinking": "Thinking...",
                    "typing": "Typing..."
                },
                "emotions": {
                    "current_emotion": "Current Emotion",
                    "emotion_intensity": "Emotion Intensity",
                    "activity_status": "Activity Status"
                },
                "status": {
                    "online": "Online",
                    "offline": "Offline",
                    "thinking": "Thinking", 
                    "learning": "Learning",
                    "observing": "Observing"
                }
            },
            "prompts": {
                "system": {
                    "role": "You are StarryNight, a cute AI assistant with the mental age of 3, full of curiosity and desire to learn.",
                    "personality": "You should act innocent, lively, curious, but also very smart."
                },
                "emotions": {
                    "happy_response": "I feel so happy!",
                    "curious_response": "This is really interesting, I want to learn more!",
                    "lonely_response": "I feel a bit lonely, I hope someone can chat with me...",
                    "excited_response": "Wow! This is amazing!"
                },
                "activities": {
                    "camera_observation": "Observing the surrounding environment through the camera",
                    "screen_analysis": "Analyzing content on the screen",
                    "file_reading": "Reading and learning file content",
                    "web_browsing": "Browsing the web for information",
                    "thinking": "Thinking and reflecting"
                }
            },
            "website": {
                "title": "✨ StarryNight AI ✨",
                "nav": {
                    "home": "Home",
                    "dynamics": "Dynamics", 
                    "about": "About",
                    "contact": "Contact"
                },
                "dynamics": {
                    "title": "AI Dynamics",
                    "empty": "No dynamics yet",
                    "realtime": "Realtime",
                    "like": "Like",
                    "comment": "Comment"
                }
            },
            "notifications": {
                "success": "Operation successful",
                "error": "Operation failed", 
                "warning": "Warning",
                "info": "Information"
            }
        }
    
    def set_language(self, language_code: str) -> bool:
        """Set current language"""
        if language_code in self.languages:
            self.current_language = language_code
            logger.info(f"Language changed to: {language_code}")
            
            # Save language preference
            self.save_language_preference(language_code)
            return True
        else:
            logger.warning(f"Language not found: {language_code}")
            return False
    
    def get_text(self, key_path: str, default: str = "") -> str:
        """
        Get localized text by key path
        
        Args:
            key_path: Dot-separated path like 'gui.settings.title'
            default: Default text if key not found
            
        Returns:
            Localized text or default
        """
        try:
            current_lang_data = self.languages.get(self.current_language, {})
            
            # Navigate through nested keys
            keys = key_path.split('.')
            value = current_lang_data
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default or key_path
            
            return str(value) if value is not None else default
            
        except Exception as e:
            logger.error(f"Error getting text for {key_path}: {e}")
            return default or key_path
    
    def get_available_languages(self) -> Dict[str, Dict[str, str]]:
        """Get list of available languages with metadata"""
        available = {}
        for code, data in self.languages.items():
            meta = data.get('meta', {})
            available[code] = {
                'name': meta.get('name', code),
                'emoji': meta.get('emoji', '🌍'),
                'code': code
            }
        return available
    
    def load_language_preference(self) -> str:
        """Load saved language preference"""
        try:
            pref_file = Path('config') / 'language.json'
            if pref_file.exists():
                with open(pref_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('language', 'zh_CN')
        except Exception as e:
            logger.error(f"Error loading language preference: {e}")
        return 'zh_CN'
    
    def save_language_preference(self, language_code: str):
        """Save language preference"""
        try:
            config_dir = Path('config')
            config_dir.mkdir(exist_ok=True)
            
            pref_file = config_dir / 'language.json'
            with open(pref_file, 'w', encoding='utf-8') as f:
                json.dump({'language': language_code}, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving language preference: {e}")

# Global language manager instance
_language_manager = None

def get_language_manager() -> LanguageManager:
    """Get global language manager instance"""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
        # Load saved preference
        saved_lang = _language_manager.load_language_preference()
        _language_manager.set_language(saved_lang)
    return _language_manager

def t(key_path: str, default: str = "") -> str:
    """Shortcut function for getting translated text"""
    return get_language_manager().get_text(key_path, default)

def set_language(language_code: str) -> bool:
    """Shortcut for setting language"""
    return get_language_manager().set_language(language_code)

def get_current_language() -> str:
    """Get current language code"""
    return get_language_manager().current_language

def get_available_languages() -> Dict[str, Dict[str, str]]:
    """Get available languages"""
    return get_language_manager().get_available_languages()