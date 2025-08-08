#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级功能配置助手
帮助用户配置Twitter、Neo4j等高级功能
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """检查依赖安装情况"""
    print("🔍 检查高级功能依赖...")
    
    dependencies = {
        "opencv-python": "摄像头视觉感知",
        "SpeechRecognition": "麦克风语音识别",
        "sounddevice": "音频设备访问",
        "soundfile": "音频文件处理",
        "transformers": "机器学习模型",
        "torch": "深度学习框架",
        "sentence-transformers": "文本嵌入",
        "tweepy": "Twitter API",
        "py2neo": "Neo4j图数据库"
    }
    
    missing = []
    installed = []
    
    for package, description in dependencies.items():
        try:
            __import__(package.replace('-', '_'))
            installed.append(f"✅ {package} - {description}")
        except ImportError:
            missing.append(f"❌ {package} - {description}")
    
    print("\n已安装的依赖:")
    for item in installed:
        print(f"  {item}")
    
    if missing:
        print("\n缺失的依赖:")
        for item in missing:
            print(f"  {item}")
        
        print("\n📦 安装缺失依赖:")
        print("pip install opencv-python SpeechRecognition sounddevice soundfile")
        print("pip install transformers torch sentence-transformers")
        print("pip install tweepy py2neo")
        
        install = input("\n是否现在安装缺失的依赖? (y/n): ").lower()
        if install == 'y':
            missing_packages = [item.split(' - ')[0][2:] for item in missing]
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
                print("✅ 依赖安装完成!")
            except subprocess.CalledProcessError as e:
                print(f"❌ 安装失败: {e}")
    else:
        print("\n🎉 所有依赖已安装!")

def setup_twitter():
    """配置Twitter API"""
    print("\n🐦 配置Twitter API")
    print("1. 访问 https://developer.twitter.com/")
    print("2. 创建应用并获取API密钥")
    print("3. 在下面输入您的API凭证:")
    
    credentials = {}
    
    print("\n请输入Twitter API凭证 (按回车跳过):")
    credentials['TWITTER_CONSUMER_KEY'] = input("Consumer Key: ").strip()
    credentials['TWITTER_CONSUMER_SECRET'] = input("Consumer Secret: ").strip()
    credentials['TWITTER_ACCESS_TOKEN'] = input("Access Token: ").strip()
    credentials['TWITTER_ACCESS_TOKEN_SECRET'] = input("Access Token Secret: ").strip()
    
    # 检查是否所有凭证都已输入
    if all(credentials.values()):
        # 写入.env文件
        env_file = Path(".env")
        with open(env_file, "w", encoding="utf-8") as f:
            for key, value in credentials.items():
                f.write(f"{key}={value}\n")
        
        # 也设置环境变量
        for key, value in credentials.items():
            os.environ[key] = value
        
        print("✅ Twitter API配置已保存到.env文件")
        
        # 测试连接
        try:
            import tweepy
            auth = tweepy.OAuthHandler(credentials['TWITTER_CONSUMER_KEY'], 
                                     credentials['TWITTER_CONSUMER_SECRET'])
            auth.set_access_token(credentials['TWITTER_ACCESS_TOKEN'], 
                                credentials['TWITTER_ACCESS_TOKEN_SECRET'])
            api = tweepy.API(auth)
            api.verify_credentials()
            print("✅ Twitter API连接测试成功!")
        except Exception as e:
            print(f"❌ Twitter API测试失败: {e}")
    else:
        print("⚠️ Twitter配置跳过")

def setup_neo4j():
    """配置Neo4j数据库"""
    print("\n🗃️ 配置Neo4j图数据库")
    print("选择配置方式:")
    print("1. Docker快速部署 (推荐)")
    print("2. 手动配置连接")
    print("3. 跳过")
    
    choice = input("选择 (1/2/3): ").strip()
    
    if choice == "1":
        print("\n🐳 Docker部署Neo4j:")
        password = input("设置Neo4j密码: ").strip() or "nagaai123"
        
        docker_cmd = f"""docker run -d \\
  --name nagaai-neo4j \\
  -p 7474:7474 -p 7687:7687 \\
  -e NEO4J_AUTH=neo4j/{password} \\
  -v nagaai-neo4j-data:/data \\
  neo4j:latest"""
        
        print(f"\n执行以下命令部署Neo4j:")
        print(docker_cmd)
        
        deploy = input("\n是否现在部署? (y/n): ").lower()
        if deploy == 'y':
            try:
                subprocess.run(["docker", "run", "-d", 
                              "--name", "nagaai-neo4j",
                              "-p", "7474:7474", "-p", "7687:7687",
                              "-e", f"NEO4J_AUTH=neo4j/{password}",
                              "-v", "nagaai-neo4j-data:/data",
                              "neo4j:latest"], check=True)
                print("✅ Neo4j部署成功!")
                print("🌐 访问 http://localhost:7474 管理数据库")
                
                # 更新配置
                update_config_neo4j("neo4j://localhost:7687", "neo4j", password)
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Docker部署失败: {e}")
                print("请确保Docker已安装并运行")
            except FileNotFoundError:
                print("❌ 未找到Docker，请先安装Docker")
    
    elif choice == "2":
        print("\n手动配置Neo4j连接:")
        uri = input("Neo4j URI (默认: neo4j://localhost:7687): ").strip() or "neo4j://localhost:7687"
        user = input("用户名 (默认: neo4j): ").strip() or "neo4j"
        password = input("密码: ").strip()
        
        if password:
            update_config_neo4j(uri, user, password)
            print("✅ Neo4j配置已更新")
        else:
            print("⚠️ 密码为空，配置跳过")
    else:
        print("⚠️ Neo4j配置跳过")

def update_config_neo4j(uri, user, password):
    """更新config.json中的Neo4j配置"""
    config_file = Path("config.json")
    
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        if "grag" not in config:
            config["grag"] = {}
        
        config["grag"].update({
            "enabled": True,
            "neo4j_uri": uri,
            "neo4j_user": user,
            "neo4j_password": password,
            "neo4j_database": "neo4j"
        })
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

def configure_openai_api():
    """配置OpenAI API"""
    print("\n🤖 配置OpenAI API")
    
    config_file = Path("config.json")
    if not config_file.exists():
        print("❌ config.json文件不存在")
        return
    
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    current_key = config.get("api", {}).get("api_key", "")
    if current_key and current_key.strip() and current_key != " ":
        print(f"✅ API密钥已配置: {current_key[:10]}...{current_key[-10:]}")
        return
    
    print("请配置OpenAI兼容的API:")
    api_key = input("API密钥: ").strip()
    base_url = input("API端点 (默认OpenAI): ").strip() or "https://api.openai.com/v1"
    model = input("模型名称 (默认gpt-3.5-turbo): ").strip() or "gpt-3.5-turbo"
    
    if api_key:
        if "api" not in config:
            config["api"] = {}
        
        config["api"].update({
            "api_key": api_key,
            "base_url": base_url,
            "model_name": model
        })
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ OpenAI API配置已更新")
    else:
        print("⚠️ API密钥为空，配置跳过")

def enable_advanced_features():
    """启用高级功能"""
    print("\n🚀 启用高级功能")
    
    config_file = Path("config.json")
    if not config_file.exists():
        print("❌ config.json文件不存在")
        return
    
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 确保emotional_ai配置存在
    if "emotional_ai" not in config:
        config["emotional_ai"] = {}
    
    # 推荐的安全配置
    recommended_config = {
        "advanced_features_enabled": True,
        "camera_perception": False,  # 默认关闭摄像头
        "microphone_perception": False,  # 默认关闭麦克风
        "deep_reflection_enabled": True,
        "personality_evolution": True,
        "knowledge_graph_enabled": True,
        "social_media_enabled": False,  # 默认关闭社交媒体
        "autonomous_level": "creative",  # 从引导级别开始
        "max_daily_posts": 3
    }
    
    print("推荐的安全配置:")
    for key, value in recommended_config.items():
        print(f"  {key}: {value}")
    
    apply = input("\n应用推荐配置? (y/n): ").lower()
    if apply == 'y':
        config["emotional_ai"].update(recommended_config)
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ 高级功能配置已应用")
        print("\n⚠️ 安全提醒:")
        print("- 摄像头和麦克风默认关闭，可在GUI中手动启用")
        print("- 社交媒体默认关闭，需要配置Twitter后启用")
        print("- 自主等级设为'guided'，可逐步提升")
    else:
        print("⚠️ 配置跳过")

def main():
    """主函数"""
    print("🌟 NagaAgent高级功能配置助手")
    print("=" * 50)
    
    # 1. 检查依赖
    check_dependencies()
    
    # 2. 配置OpenAI API
    configure_openai_api()
    
    # 3. 配置Twitter (可选)
    setup_twitter()
    
    # 4. 配置Neo4j (可选)
    setup_neo4j()
    
    # 5. 启用高级功能
    enable_advanced_features()
    
    print("\n🎉 配置完成!")
    print("\n📖 使用指南:")
    print("1. 运行 python main.py 启动主程序")
    print("2. 在GUI设置中微调各项参数")
    print("3. 查看 ADVANCED_AI_FEATURES_GUIDE.md 了解详细功能")
    print("\n⚠️ 注意: 首次运行可能需要下载ML模型，请保持网络连接")

if __name__ == "__main__":
    main()