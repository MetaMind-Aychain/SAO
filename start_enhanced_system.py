#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StarryNightAI系统 - 增强版启动脚本
包含AI网站、动态发布、自主互动等所有功能
"""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🌟 StarryNightAI系统 v3.0 🌟                    ║
    ║                                                              ║
    ║  🎭 情绪AI系统    🧠 记忆学习    👁️ 视觉感知    🎤 语音交互    ║
    ║  🌐 网站展示      📊 数据统计    🤖 自主互动    ⚡ GPU加速    ║
    ║                                                              ║
    ║  🚀 正在启动增强版AI系统...                                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """检查依赖项"""
    print("🔍 检查系统依赖...")
    
    required_modules = [
        'torch', 'torchvision', 'torchaudio',
        'opencv-python', 'Pillow', 'numpy',
        'fastapi', 'uvicorn', 'sqlalchemy',
        'PyQt5', 'requests', 'aiohttp'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} - 缺失")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  缺少以下依赖项: {', '.join(missing_modules)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖项检查完成")
    return True

def start_ai_website():
    """启动AI网站"""
    print("🌐 启动AI展示网站...")
    try:
        # 切换到ai_website目录
        os.chdir('ai_website')
        
        # 启动FastAPI服务器
        cmd = [sys.executable, '-m', 'uvicorn', 'app:app', '--host', '0.0.0.0', '--port', '8001', '--reload']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务器启动
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ AI网站启动成功 - http://localhost:8001")
            return process
        else:
            print("❌ AI网站启动失败")
            return None
            
    except Exception as e:
        print(f"❌ 启动AI网站时出错: {e}")
        return None

def start_main_ai():
    """启动主AI程序"""
    print("🤖 启动主AI系统...")
    try:
        # 回到主目录
        os.chdir('..')
        
        # 启动主程序
        cmd = [sys.executable, 'main.py']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待程序启动
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ 主AI系统启动成功")
            return process
        else:
            print("❌ 主AI系统启动失败")
            return None
            
    except Exception as e:
        print(f"❌ 启动主AI系统时出错: {e}")
        return None

def monitor_processes(processes):
    """监控进程状态"""
    print("\n🔍 监控系统状态...")
    print("按 Ctrl+C 停止所有服务")
    
    try:
        while True:
            all_running = True
            for name, process in processes.items():
                if process and process.poll() is not None:
                    print(f"⚠️  {name} 已停止")
                    all_running = False
            
            if not all_running:
                print("❌ 部分服务已停止，请检查错误日志")
                break
                
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n🛑 收到停止信号，正在关闭服务...")
        
        for name, process in processes.items():
            if process and process.poll() is None:
                print(f"🛑 停止 {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()

def main():
    """主函数"""
    print_banner()
    
    # 检查依赖
    if not check_dependencies():
        return
    
    print("\n🚀 开始启动服务...")
    
    processes = {}
    
    # 启动AI网站
    website_process = start_ai_website()
    if website_process:
        processes['AI网站'] = website_process
    
    # 启动主AI系统
    ai_process = start_main_ai()
    if ai_process:
        processes['主AI系统'] = ai_process
    
    if not processes:
        print("❌ 没有成功启动任何服务")
        return
    
    print(f"\n✅ 成功启动 {len(processes)} 个服务")
    print("\n📋 服务状态:")
    for name in processes.keys():
        print(f"  🌟 {name}: 运行中")
    
    print("\n🌐 访问地址:")
    print("  📊 AI展示网站: http://localhost:8001")
    print("  🤖 桌面应用: 已启动")
    
    # 监控进程
    monitor_processes(processes)
    
    print("👋 StarryNightAI系统已关闭")

if __name__ == "__main__":
    main() 