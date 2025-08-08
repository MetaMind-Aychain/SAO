#!/usr/bin/env python3
# install_emotional_ai.py
"""
情绪化AI系统安装脚本
自动安装依赖并配置环境
"""

import sys
import os
import subprocess
import json
from pathlib import Path

def run_command(command, description=""):
    """运行命令并处理错误"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False

def install_dependencies():
    """安装Python依赖"""
    print("📦 安装Python依赖包...")
    
    # 基础依赖
    basic_deps = [
        "PyQt5",
        "opencv-python", 
        "numpy",
        "pillow",
        "aiohttp",
        "watchdog"
    ]
    
    # 音频相关依赖（可选）
    audio_deps = [
        "pyaudio",
        "speechrecognition"
    ]
    
    # 安装基础依赖
    for dep in basic_deps:
        if not run_command(f"pip install {dep}", f"安装 {dep}"):
            print(f"⚠️ {dep} 安装失败，可能需要手动安装")
    
    # 尝试安装音频依赖
    print("\n🎤 安装音频依赖（如果失败可跳过）...")
    for dep in audio_deps:
        run_command(f"pip install {dep}", f"安装 {dep}")
    
    print("\n✅ 依赖安装完成！")

def create_config():
    """创建默认配置文件"""
    print("⚙️ 创建配置文件...")
    
    config_file = Path("config.json")
    
    if config_file.exists():
        print(f"⚠️ 配置文件 {config_file} 已存在，跳过创建")
        return
    
    # 默认配置
    default_config = {
        "system": {
            "version": "3.0",
            "voice_enabled": True,
            "stream_mode": True,
            "debug": False,
            "log_level": "INFO"
        },
        "api": {
            "api_key": "",
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
            "temperature": 0.7,
            "max_tokens": 2000,
            "max_history_rounds": 10
        },
        "api_server": {
            "enabled": True,
            "host": "127.0.0.1",
            "port": 8000,
            "auto_start": True,
            "docs_enabled": True
        },
        "grag": {
            "enabled": True,
            "auto_extract": True,
            "context_length": 5,
            "similarity_threshold": 0.6,
            "neo4j_uri": "neo4j://127.0.0.1:7687",
            "neo4j_user": "neo4j",
            "neo4j_password": "",
            "neo4j_database": "neo4j"
        },
        "ui": {
            "user_name": "用户",
            "bg_alpha": 0.5,
            "window_bg_alpha": 110,
            "mac_btn_size": 36,
            "mac_btn_margin": 16,
            "mac_btn_gap": 12,
            "animation_duration": 600
        }
    }
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        print(f"✅ 配置文件已创建: {config_file}")
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")

def check_system_requirements():
    """检查系统要求"""
    print("🔍 检查系统要求...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"❌ Python版本过低: {python_version.major}.{python_version.minor}")
        print("需要Python 3.8或更高版本")
        return False
    else:
        print(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查操作系统
    import platform
    os_name = platform.system()
    print(f"✅ 操作系统: {os_name}")
    
    if os_name == "Windows":
        print("💡 Windows用户请确保已安装Visual C++ Build Tools")
    elif os_name == "Darwin":  # macOS
        print("💡 macOS用户可能需要安装Homebrew和相关依赖")
    
    return True

def setup_directories():
    """创建必要的目录"""
    print("📁 创建目录结构...")
    
    directories = [
        "logs",
        "emotional_ai",
        "ui",
        "mcpserver"
    ]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ 创建目录: {dir_name}")
            except Exception as e:
                print(f"❌ 创建目录失败 {dir_name}: {e}")

def main():
    """主安装流程"""
    print("🎭 NagaAgent 情绪化AI系统安装程序")
    print("=" * 50)
    
    # 检查系统要求
    if not check_system_requirements():
        sys.exit(1)
    
    # 创建目录
    setup_directories()
    
    # 安装依赖
    install_dependencies()
    
    # 创建配置
    create_config()
    
    print("\n" + "=" * 50)
    print("🎉 安装完成！")
    print("\n📖 下一步:")
    print("1. 编辑 config.json 文件，配置您的API密钥")
    print("2. 运行: python start_emotional_ai.py")
    print("3. 查看详细说明: EMOTIONAL_AI_README.md")
    print("\n⚠️ 注意事项:")
    print("- 首次使用需要授权摄像头和麦克风权限")
    print("- 部分功能需要网络连接")
    print("- 如遇问题请查看日志文件: emotional_ai.log")

if __name__ == "__main__":
    main()