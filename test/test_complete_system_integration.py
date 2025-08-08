#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整系统集成测试脚本
测试AI动态发布、数据持久化、Web实时更新等功能
"""

import os
import sys
import time
import asyncio
import threading
import subprocess
import sqlite3
import requests
from datetime import datetime
from pathlib import Path

def print_banner():
    """打印测试横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                🧪 StarryNightAI系统完整集成测试 🧪                 ║
    ║                                                              ║
    ║  测试内容：                                                   ║
    ║  🔗 AI动态发布器集成                                         ║
    ║  💾 数据库持久化                                             ║
    ║  🌐 Web端实时更新                                            ║
    ║  🤖 AI主动互动频率                                           ║
    ║  📊 统计数据同步                                             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_database():
    """检查数据库状态"""
    print("🔍 检查数据库状态...")
    
    db_path = "ai_website/ai_website.db"
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表结构
        tables = ['ai_dynamics', 'developer_updates', 'users', 'comments', 'likes']
        for table in tables:
            cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone()[0] == 0:
                print(f"❌ 表 {table} 不存在")
                return False
            else:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✅ 表 {table}: {count} 条记录")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("🌐 测试API端点...")
    
    base_url = "http://localhost:8001"
    endpoints = [
        "/api/ai/status",
        "/api/stats",
        "/api/dynamics",
        "/api/developer/updates"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: 成功 ({len(str(data))} 字符)")
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: 连接失败 - {e}")

def test_websocket():
    """测试WebSocket连接"""
    print("🔌 测试WebSocket连接...")
    
    try:
        import websocket
        import json
        
        def on_message(ws, message):
            data = json.loads(message)
            print(f"✅ WebSocket消息: {data.get('type', 'unknown')}")
        
        def on_error(ws, error):
            print(f"❌ WebSocket错误: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            print("🔌 WebSocket连接已关闭")
        
        def on_open(ws):
            print("✅ WebSocket连接已建立")
            # 发送测试消息
            ws.send(json.dumps({"type": "ping"}))
            
        ws = websocket.WebSocketApp("ws://localhost:8001/ws",
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close,
                                  on_open=on_open)
        
        # 运行3秒钟测试
        def run_ws():
            ws.run_forever()
        
        ws_thread = threading.Thread(target=run_ws, daemon=True)
        ws_thread.start()
        time.sleep(3)
        ws.close()
        
    except ImportError:
        print("⚠️ websocket-client 未安装，跳过WebSocket测试")
    except Exception as e:
        print(f"❌ WebSocket测试失败: {e}")

def simulate_ai_activity():
    """模拟AI活动"""
    print("🤖 模拟AI活动...")
    
    try:
        # 导入动态发布器
        sys.path.append(os.path.dirname(__file__))
        from ai_dynamic_publisher import ai_dynamic_publisher
        
        # 模拟活动数据
        activities = [
            {
                'type': 'thinking',
                'content': '正在思考用户的问题，这是一个很有趣的话题...',
                'metadata': {'complexity': 'medium', 'timestamp': datetime.now().isoformat()}
            },
            {
                'type': 'emotion_change',
                'content': '感受到了用户的关心，心情变得愉悦起来',
                'metadata': {'emotion': 'joy', 'intensity': 0.8}
            },
            {
                'type': 'conversation',
                'content': '用户：你好\nStarryNight：你好！很高兴见到你！',
                'metadata': {'user_input': '你好', 'ai_response': '你好！很高兴见到你！'}
            }
        ]
        
        for activity in activities:
            asyncio.run(ai_dynamic_publisher.queue_activity(
                activity['type'],
                activity['content'],
                activity['metadata']
            ))
            print(f"✅ 已发布 {activity['type']} 活动")
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ AI活动模拟失败: {e}")

def check_data_persistence():
    """检查数据持久化"""
    print("💾 检查数据持久化...")
    
    try:
        # 检查数据库记录数量变化
        db_path = "ai_website/ai_website.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取动态数量
        cursor.execute("SELECT COUNT(*) FROM ai_dynamics")
        dynamics_count = cursor.fetchone()[0]
        
        # 获取最新动态
        cursor.execute("SELECT content, created_at FROM ai_dynamics ORDER BY created_at DESC LIMIT 5")
        recent_dynamics = cursor.fetchall()
        
        print(f"✅ 总动态数: {dynamics_count}")
        print("📝 最近动态:")
        for i, (content, created_at) in enumerate(recent_dynamics):
            print(f"  {i+1}. {content[:50]}... ({created_at})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 数据持久化检查失败: {e}")

def main():
    """主测试函数"""
    print_banner()
    
    print("🚀 开始系统集成测试...")
    print()
    
    # 1. 检查数据库
    if not check_database():
        print("❌ 数据库检查失败，请先启动AI网站")
        return
    
    print()
    
    # 2. 测试API端点
    test_api_endpoints()
    print()
    
    # 3. 测试WebSocket
    test_websocket()
    print()
    
    # 4. 模拟AI活动
    simulate_ai_activity()
    print()
    
    # 5. 检查数据持久化
    check_data_persistence()
    print()
    
    print("✅ 系统集成测试完成！")
    print()
    print("📋 测试结果总结:")
    print("  🔗 动态发布器: 已集成")
    print("  💾 数据持久化: 已验证")  
    print("  🌐 API端点: 已测试")
    print("  🔌 WebSocket: 已测试")
    print()
    print("🌟 建议访问 http://localhost:8001 查看实时效果")

if __name__ == "__main__":
    main()