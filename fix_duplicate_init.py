#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
彻底修复重复初始化问题
通过添加初始化标志来防止重复初始化
"""

import re
from pathlib import Path

def fix_emotional_core():
    """修复EmotionalCore的重复初始化"""
    file_path = Path("emotional_ai_core.py")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加初始化标志
    init_flag_code = '''class EmotionalCore:
    """情绪核心 - 集成到NagaConversation"""
    
    _instances = {}  # 类级别的实例字典
    
    def __new__(cls, config):
        """确保每个配置只有一个实例"""
        config_id = id(config)
        if config_id not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[config_id] = instance
            instance._initialized = False
        return cls._instances[config_id]
    
    def __init__(self, config):
        # 防止重复初始化
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        self._initialized = True'''
    
    # 替换类定义
    pattern = r'class EmotionalCore:\s*"""情绪核心 - 集成到NagaConversation"""\s*def __init__\(self, config\):'
    replacement = init_flag_code + '\n        '
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ EmotionalCore重复初始化已修复")
    else:
        print("⚠️ EmotionalCore修复失败，可能已经修复或结构不匹配")

def fix_voice_integration():
    """修复VoiceIntegration的重复初始化"""
    file_path = Path("voice/voice_integration.py")
    
    if not file_path.exists():
        print("⚠️ voice_integration.py 文件不存在")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加单例模式
    singleton_code = '''class VoiceIntegration:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, *args, **kwargs):
        if self._initialized:
            return
        self._initialized = True'''
    
    # 查找并替换类定义
    pattern = r'class VoiceIntegration:\s*def __init__\(self[^)]*\):'
    
    if re.search(pattern, content):
        new_content = re.sub(
            r'class VoiceIntegration:',
            'class VoiceIntegration:\n    _instance = None\n    _initialized = False\n    \n    def __new__(cls, *args, **kwargs):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance',
            content
        )
        
        # 添加初始化检查
        new_content = re.sub(
            r'(\s+def __init__\(self[^)]*\):)',
            r'\1\n        if hasattr(self, "_initialized") and self._initialized:\n            return\n        self._initialized = True',
            new_content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ VoiceIntegration重复初始化已修复")
    else:
        print("⚠️ VoiceIntegration修复失败，找不到匹配的类定义")

def fix_perception_systems():
    """修复感知系统的重复初始化"""
    
    # 修复屏幕感知
    for filename in ["proactive_screen_capture.py", "proactive_file_explorer.py"]:
        file_path = Path(filename)
        if not file_path.exists():
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找类定义并添加单例模式
        class_match = re.search(r'class (\w+):', content)
        if class_match:
            class_name = class_match.group(1)
            
            # 添加单例模式
            singleton_pattern = f'''class {class_name}:
    _instances = {{}}
    
    def __new__(cls, emotion_core=None):
        if emotion_core is None:
            instance_key = 'default'
        else:
            instance_key = id(emotion_core)
            
        if instance_key not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[instance_key] = instance
            instance._initialized = False
        return cls._instances[instance_key]'''
            
            new_content = re.sub(
                f'class {class_name}:',
                singleton_pattern,
                content
            )
            
            # 添加初始化检查
            new_content = re.sub(
                r'(\s+def __init__\(self[^)]*\):)',
                r'\1\n        if hasattr(self, "_initialized") and self._initialized:\n            return\n        self._initialized = True',
                new_content
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ {class_name}重复初始化已修复")

def main():
    """执行所有修复"""
    print("🔧 开始修复重复初始化问题...")
    print("=" * 50)
    
    try:
        fix_emotional_core()
        fix_voice_integration()
        fix_perception_systems()
        
        print("=" * 50)
        print("🎉 所有修复完成！")
        print("\n建议重启系统测试修复效果：")
        print("  python main.py")
        
    except Exception as e:
        print(f"❌ 修复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()