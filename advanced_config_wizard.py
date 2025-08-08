#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NagaAgent 高级功能配置向导
帮助用户配置所有必需的API密钥和服务
"""

import json
import os
import sys
from pathlib import Path

def print_header():
    """打印配置向导头部信息"""
    print("=" * 80)
    print("🐉 NagaAgent 3.0 高级功能配置向导")
    print("=" * 80)
    print("这个向导将帮助您配置以下高级功能:")
    print("📸 高级感知系统 (摄像头/麦克风)")
    print("🧠 深度反思系统 (LLM驱动)")
    print("🌱 性格演化系统")
    print("🕸️  知识图谱构建 (Neo4j可选)")
    print("🐦 社交媒体集成 (Twitter)")
    print("-" * 80)

def load_config():
    """加载当前配置"""
    config_path = Path("config.json")
    if not config_path.exists():
        print("❌ 错误: config.json 文件不存在!")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    """保存配置"""
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("✅ 配置已保存到 config.json")

def create_env_file():
    """创建或更新.env文件"""
    env_path = Path(".env")
    env_content = []
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.readlines()
    
    # 检查是否已有配置项
    env_dict = {}
    for line in env_content:
        if '=' in line and not line.strip().startswith('#'):
            key, value = line.strip().split('=', 1)
            env_dict[key] = value
    
    print("\n🔐 环境变量配置 (.env文件)")
    print("为了安全考虑，敏感的API密钥将保存在.env文件中")
    
    # Twitter API配置
    print("\n--- Twitter API 配置 ---")
    print("请访问 https://developer.twitter.com/en/portal/dashboard 获取Twitter API密钥")
    
    twitter_keys = [
        ("TWITTER_API_KEY", "Twitter API Key"),
        ("TWITTER_API_SECRET", "Twitter API Secret"),
        ("TWITTER_ACCESS_TOKEN", "Twitter Access Token"),
        ("TWITTER_ACCESS_TOKEN_SECRET", "Twitter Access Token Secret"),
        ("TWITTER_BEARER_TOKEN", "Twitter Bearer Token")
    ]
    
    for key, description in twitter_keys:
        current_value = env_dict.get(key, "")
        if current_value:
            print(f"{description}: 已配置 (****)")
            update = input(f"是否更新 {description}? (y/N): ").lower().strip()
            if update == 'y':
                value = input(f"请输入新的 {description}: ").strip()
                if value:
                    env_dict[key] = value
        else:
            value = input(f"请输入 {description} (可选，回车跳过): ").strip()
            if value:
                env_dict[key] = value
    
    # Neo4j配置
    print("\n--- Neo4j 数据库配置 (可选) ---")
    print("Neo4j用于知识图谱构建，您可以:")
    print("1. 安装本地Neo4j数据库")
    print("2. 使用Neo4j Aura云服务")
    print("3. 跳过（使用内存图谱）")
    
    neo4j_choice = input("请选择 (1/2/3): ").strip()
    
    if neo4j_choice in ['1', '2']:
        neo4j_keys = [
            ("NEO4J_URI", "Neo4j URI (例如: bolt://localhost:7687)"),
            ("NEO4J_USERNAME", "Neo4j 用户名"),
            ("NEO4J_PASSWORD", "Neo4j 密码")
        ]
        
        for key, description in neo4j_keys:
            current_value = env_dict.get(key, "")
            if current_value:
                print(f"{description}: 已配置")
                update = input(f"是否更新? (y/N): ").lower().strip()
                if update == 'y':
                    value = input(f"请输入新的 {description}: ").strip()
                    if value:
                        env_dict[key] = value
            else:
                value = input(f"请输入 {description}: ").strip()
                if value:
                    env_dict[key] = value
    
    # 写入.env文件
    with open(".env", 'w', encoding='utf-8') as f:
        f.write("# NagaAgent 3.0 环境变量配置\n")
        f.write("# 请勿将此文件提交到版本控制系统\n\n")
        
        if any(key.startswith('TWITTER_') for key in env_dict):
            f.write("# Twitter API 配置\n")
            for key in ['TWITTER_API_KEY', 'TWITTER_API_SECRET', 'TWITTER_ACCESS_TOKEN', 
                       'TWITTER_ACCESS_TOKEN_SECRET', 'TWITTER_BEARER_TOKEN']:
                if key in env_dict:
                    f.write(f"{key}={env_dict[key]}\n")
            f.write("\n")
        
        if any(key.startswith('NEO4J_') for key in env_dict):
            f.write("# Neo4j 数据库配置\n")
            for key in ['NEO4J_URI', 'NEO4J_USERNAME', 'NEO4J_PASSWORD']:
                if key in env_dict:
                    f.write(f"{key}={env_dict[key]}\n")
            f.write("\n")
    
    print("✅ 环境变量已保存到 .env 文件")

def check_dependencies():
    """检查依赖项安装状态"""
    print("\n📦 检查依赖项...")
    
    required_packages = [
        "opencv-python",
        "transformers", 
        "torch",
        "sentence-transformers",
        "tweepy",
        "py2neo",
        "SpeechRecognition",
        "sounddevice",
        "soundfile"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (缺失)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  发现 {len(missing_packages)} 个缺失的依赖项")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        
        install_now = input("\n是否现在自动安装? (y/N): ").lower().strip()
        if install_now == 'y':
            import subprocess
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
                print("✅ 依赖项安装完成")
            except subprocess.CalledProcessError as e:
                print(f"❌ 安装失败: {e}")
                return False
    
    return True

def configure_hardware_permissions():
    """配置硬件权限"""
    print("\n🎥 硬件权限配置")
    print("高级感知功能需要以下硬件权限:")
    print("📷 摄像头访问权限")
    print("🎤 麦克风访问权限")
    print("\n请确保:")
    print("1. 您的系统已连接摄像头和麦克风")
    print("2. Python有权限访问这些设备")
    print("3. 防火墙/杀毒软件允许访问")
    
    test_camera = input("\n是否测试摄像头? (y/N): ").lower().strip()
    if test_camera == 'y':
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print("✅ 摄像头测试成功")
                cap.release()
            else:
                print("❌ 摄像头访问失败")
        except Exception as e:
            print(f"❌ 摄像头测试错误: {e}")
    
    test_microphone = input("是否测试麦克风? (y/N): ").lower().strip()
    if test_microphone == 'y':
        try:
            import sounddevice as sd
            import numpy as np
            print("正在录制3秒音频...")
            recording = sd.rec(int(3 * 44100), samplerate=44100, channels=1)
            sd.wait()
            if np.max(np.abs(recording)) > 0.01:
                print("✅ 麦克风测试成功")
            else:
                print("⚠️  麦克风音量很低，请检查设置")
        except Exception as e:
            print(f"❌ 麦克风测试错误: {e}")

def configure_autonomous_level():
    """配置自主行为级别"""
    print("\n🤖 AI自主行为级别配置")
    print("请选择AI的自主行为级别:")
    print("1. restricted - 限制模式 (仅基础功能)")
    print("2. moderate - 适中模式 (推荐)")
    print("3. full - 完全自主 (高级用户)")
    
    config = load_config()
    current_level = config.get("emotional_ai", {}).get("autonomous_level", "full")
    print(f"当前级别: {current_level}")
    
    choice = input("请选择 (1/2/3) 或回车保持当前设置: ").strip()
    
    level_map = {"1": "restricted", "2": "moderate", "3": "full"}
    if choice in level_map:
        config["emotional_ai"]["autonomous_level"] = level_map[choice]
        
        # 根据级别调整其他参数
        if choice == "3":  # 完全自主
            config["emotional_ai"]["max_daily_posts"] = 10
            config["emotional_ai"]["sharing_probability"] = 0.25
        elif choice == "2":  # 适中
            config["emotional_ai"]["max_daily_posts"] = 5
            config["emotional_ai"]["sharing_probability"] = 0.15
        else:  # 限制
            config["emotional_ai"]["max_daily_posts"] = 2
            config["emotional_ai"]["sharing_probability"] = 0.05
        
        save_config(config)

def show_final_summary():
    """显示最终配置摘要"""
    print("\n" + "=" * 80)
    print("🎉 配置完成!")
    print("=" * 80)
    print("您已启用以下高级功能:")
    print("✅ 摄像头感知 (面部/表情/场景识别)")
    print("✅ 麦克风感知 (语音识别)")
    print("✅ 深度反思系统 (LLM驱动的哲学思考)")
    print("✅ 性格演化系统 (AI人格发展)")
    print("✅ 知识图谱构建 (记忆关联)")
    print("✅ 社交媒体集成 (Twitter自动发布)")
    
    print("\n⚠️  重要提醒:")
    print("1. 请确保您的API密钥配置正确")
    print("2. 首次运行可能需要下载ML模型，请耐心等待")
    print("3. 某些功能需要网络连接")
    print("4. AI的自主行为会消耗API额度，请注意监控")
    
    print("\n🚀 现在可以运行 'python main.py' 启动NagaAgent!")
    print("或者运行 'python test_emotional_ai_integration.py' 进行功能测试")

def main():
    """主函数"""
    print_header()
    
    # 检查依赖项
    if not check_dependencies():
        print("❌ 请先安装缺失的依赖项")
        return
    
    # 创建环境变量文件
    create_env_file()
    
    # 配置硬件权限
    configure_hardware_permissions()
    
    # 配置自主行为级别
    configure_autonomous_level()
    
    # 显示最终摘要
    show_final_summary()

if __name__ == "__main__":
    main()