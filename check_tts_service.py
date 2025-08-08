#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS服务状态检查和启动脚本
"""

import requests
import subprocess
import sys
import time
import threading
from config import config

def check_tts_service():
    """检查TTS服务是否运行"""
    try:
        response = requests.get(f"http://127.0.0.1:{config.tts.port}/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def start_tts_service():
    """启动TTS服务"""
    try:
        print("🚀 正在启动TTS语音服务...")
        
        # 在后台启动TTS服务
        process = subprocess.Popen([
            sys.executable, "-m", "voice.start_voice_service"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务启动
        for i in range(10):
            time.sleep(1)
            if check_tts_service():
                print(f"✅ TTS服务已启动 (端口: {config.tts.port})")
                return True
            print(f"⏳ 等待TTS服务启动... ({i+1}/10)")
        
        print("❌ TTS服务启动超时")
        return False
        
    except Exception as e:
        print(f"❌ 启动TTS服务失败: {e}")
        return False

def ensure_tts_service():
    """确保TTS服务运行"""
    if check_tts_service():
        print(f"✅ TTS服务已运行 (端口: {config.tts.port})")
        return True
    else:
        print("⚠️ TTS服务未运行，尝试启动...")
        return start_tts_service()

if __name__ == "__main__":
    print("🎤 TTS语音服务检查")
    print("=" * 30)
    
    if ensure_tts_service():
        print("🎉 TTS服务正常！")
    else:
        print("❌ TTS服务不可用")
        print("💡 语音功能将被禁用")
        print("   可以尝试手动启动: python -m voice.start_voice_service")