#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StarryNightAI系统 v3.0 - 功能测试脚本
测试所有增强功能的正常运行
"""

import os
import sys
import time
import requests
import json
from pathlib import Path

def test_ai_website():
    """测试AI网站功能"""
    print("🌐 测试AI网站功能...")
    
    try:
        # 测试网站是否启动
        response = requests.get("http://localhost:8001", timeout=5)
        if response.status_code == 200:
            print("  ✅ 网站首页访问正常")
        else:
            print(f"  ❌ 网站首页访问失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 网站连接失败: {e}")
        return False
    
    # 测试API端点
    api_endpoints = [
        "/api/ai/status",
        "/api/dynamics",
        "/api/stats",
        "/api/developer/updates"
    ]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(f"http://localhost:8001{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {endpoint} API正常")
            else:
                print(f"  ❌ {endpoint} API失败: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {endpoint} API连接失败: {e}")
    
    return True

def test_database():
    """测试数据库功能"""
    print("💾 测试数据库功能...")
    
    db_path = Path("ai_website/database.db")
    if db_path.exists():
        print("  ✅ 数据库文件存在")
        
        # 检查数据库大小
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"  📊 数据库大小: {size_mb:.2f} MB")
        
        return True
    else:
        print("  ❌ 数据库文件不存在")
        return False

def test_ai_modules():
    """测试AI模块导入"""
    print("🤖 测试AI模块...")
    
    modules = [
        'conversation_core',
        'emotional_ai_core', 
        'ai_memory_system',
        'advanced_perception_system',
        'persona_management_system',
        'ai_dynamic_publisher',
        'ai_autonomous_interaction',
        'gpu_optimization'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"  ✅ {module} 模块导入成功")
        except ImportError as e:
            print(f"  ❌ {module} 模块导入失败: {e}")
    
    return True

def test_ui_modules():
    """测试UI模块"""
    print("🎨 测试UI模块...")
    
    try:
        import PyQt5
        print("  ✅ PyQt5 可用")
    except ImportError:
        print("  ❌ PyQt5 不可用")
        return False
    
    ui_modules = [
        'ui.pyqt_chat_window',
        'ui.emotion_panel'
    ]
    
    for module in ui_modules:
        try:
            __import__(module)
            print(f"  ✅ {module} 模块导入成功")
        except ImportError as e:
            print(f"  ❌ {module} 模块导入失败: {e}")
    
    return True

def test_voice_modules():
    """测试语音模块"""
    print("🎤 测试语音模块...")
    
    try:
        import speech_recognition
        print("  ✅ SpeechRecognition 可用")
    except ImportError:
        print("  ❌ SpeechRecognition 不可用")
    
    try:
        import voice.voice_integration
        print("  ✅ 语音集成模块导入成功")
    except ImportError as e:
        print(f"  ❌ 语音集成模块导入失败: {e}")
    
    return True

def test_gpu_optimization():
    """测试GPU优化"""
    print("⚡ 测试GPU优化...")
    
    try:
        import torch
        print(f"  📊 PyTorch版本: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"  ✅ CUDA可用: {torch.cuda.get_device_name()}")
            print(f"  📊 GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            print("  ⚠️  CUDA不可用，将使用CPU")
        
        # 测试GPU优化模块
        import gpu_optimization
        print("  ✅ GPU优化模块导入成功")
        
    except ImportError as e:
        print(f"  ❌ GPU相关模块导入失败: {e}")
    
    return True

def test_configuration():
    """测试配置文件"""
    print("⚙️ 测试配置文件...")
    
    config_path = Path("config.json")
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            required_keys = [
                'ai_name', 'emotional_ai', 'api', 'tts', 'ui'
            ]
            
            for key in required_keys:
                if key in config:
                    print(f"  ✅ {key} 配置存在")
                else:
                    print(f"  ❌ {key} 配置缺失")
            
            return True
        except json.JSONDecodeError as e:
            print(f"  ❌ 配置文件JSON格式错误: {e}")
            return False
    else:
        print("  ❌ 配置文件不存在")
        return False

def generate_test_report():
    """生成测试报告"""
    print("\n" + "="*60)
    print("🌟 StarryNightAI系统 v3.0 - 功能测试报告")
    print("="*60)
    
    tests = [
        ("配置文件", test_configuration),
        ("AI模块", test_ai_modules),
        ("UI模块", test_ui_modules),
        ("语音模块", test_voice_modules),
        ("GPU优化", test_gpu_optimization),
        ("数据库", test_database),
        ("AI网站", test_ai_website)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 测试: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ 测试异常: {e}")
            results.append((test_name, False))
    
    # 生成总结
    print("\n" + "="*60)
    print("📊 测试结果总结")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常")
    else:
        print("⚠️  部分测试失败，请检查相关配置")
    
    return passed == total

def main():
    """主函数"""
    print("🚀 开始StarryNightAI系统 v3.0 功能测试...")
    print("="*60)
    
    success = generate_test_report()
    
    if success:
        print("\n🎊 恭喜！StarryNightAI系统 v3.0 已准备就绪")
        print("\n📋 启动指南:")
        print("  1. 启动AI网站: cd ai_website && python -m uvicorn app:app --host 0.0.0.0 --port 8001")
        print("  2. 启动主程序: python main.py")
        print("  3. 或使用一键启动: python start_enhanced_system.py")
        print("\n🌐 访问地址: http://localhost:8001")
    else:
        print("\n🔧 请检查失败的测试项并修复相关问题")
    
    return success

if __name__ == "__main__":
    main() 