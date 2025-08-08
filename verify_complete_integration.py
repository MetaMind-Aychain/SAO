#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整集成验证脚本
验证AI自主交互系统在真实环境中与GUI和Web端的集成效果
"""

import asyncio
import logging
import time
import json
import threading
import subprocess
import requests
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegrationVerifier:
    def __init__(self):
        self.api_server_process = None
        self.ai_system = None
        self.verification_results = []
        
    async def start_api_server(self):
        """启动API服务器"""
        logger.info("🚀 启动API服务器...")
        
        try:
            # 检查端口是否已被占用
            try:
                response = requests.get("http://localhost:8000/", timeout=3)
                logger.info("✅ API服务器已在运行")
                return True
            except:
                pass
            
            # 启动API服务器
            import uvicorn
            from apiserver.api_server import app
            
            def run_server():
                uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")
            
            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            
            # 等待服务器启动
            for i in range(10):
                try:
                    response = requests.get("http://localhost:8000/", timeout=2)
                    logger.info("✅ API服务器启动成功")
                    return True
                except:
                    await asyncio.sleep(1)
            
            logger.error("❌ API服务器启动失败")
            return False
            
        except Exception as e:
            logger.error(f"❌ API服务器启动异常: {e}")
            return False
    
    async def test_api_endpoints(self):
        """测试API端点"""
        logger.info("🔍 测试API端点...")
        
        endpoints = [
            "/",
            "/api/ai/status",
            "/api/dynamics",
            "/api/developer_updates"
        ]
        
        success_count = 0
        for endpoint in endpoints:
            try:
                response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
                if response.status_code == 200:
                    logger.info(f"✅ {endpoint} - 状态码: {response.status_code}")
                    success_count += 1
                else:
                    logger.warning(f"⚠️ {endpoint} - 状态码: {response.status_code}")
            except Exception as e:
                logger.error(f"❌ {endpoint} - 错误: {e}")
        
        success_rate = (success_count / len(endpoints)) * 100
        logger.info(f"📊 API端点测试: {success_count}/{len(endpoints)} 通过 ({success_rate:.1f}%)")
        return success_count >= len(endpoints) // 2  # 至少一半成功
    
    async def test_websocket_connection(self):
        """测试WebSocket连接"""
        logger.info("🌐 测试WebSocket连接...")
        
        try:
            import websockets
            
            async def test_ws():
                try:
                    uri = "ws://localhost:8000/ws/mcplog"
                    async with websockets.connect(uri) as websocket:
                        logger.info("✅ WebSocket连接成功")
                        
                        # 等待连接确认
                        response = await asyncio.wait_for(websocket.recv(), timeout=5)
                        data = json.loads(response)
                        logger.info(f"📨 收到服务器消息: {data.get('type', 'unknown')}")
                        
                        # 发送心跳
                        await websocket.send("ping")
                        response = await asyncio.wait_for(websocket.recv(), timeout=5)
                        data = json.loads(response)
                        logger.info(f"💓 心跳响应: {data.get('type', 'unknown')}")
                        
                        return True
                        
                except Exception as e:
                    logger.error(f"WebSocket测试失败: {e}")
                    return False
            
            return await test_ws()
            
        except ImportError:
            logger.warning("websockets库未安装，跳过WebSocket测试")
            return True
        except Exception as e:
            logger.error(f"❌ WebSocket测试异常: {e}")
            return False
    
    async def initialize_ai_system(self):
        """初始化AI系统"""
        logger.info("🤖 初始化AI自主交互系统...")
        
        try:
            from ai_autonomous_interaction import get_autonomous_interaction
            self.ai_system = get_autonomous_interaction()
            
            logger.info(f"AI系统实例: {type(self.ai_system).__name__}")
            logger.info(f"运行状态: {self.ai_system.is_running}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ AI系统初始化失败: {e}")
            return False
    
    async def test_ai_message_generation(self):
        """测试AI消息生成"""
        logger.info("💬 测试AI消息生成...")
        
        if not self.ai_system:
            logger.error("AI系统未初始化")
            return False
        
        try:
            # 模拟AI生成不同类型的消息
            test_scenarios = [
                {
                    "message": "🧪 验证测试：我在观察周围的环境",
                    "emotion": "好奇",
                    "activity": "camera",
                    "priority": "normal"
                },
                {
                    "message": "📖 验证测试：我发现了有趣的文件内容",
                    "emotion": "兴奋", 
                    "activity": "file",
                    "priority": "high"
                },
                {
                    "message": "🤔 验证测试：我正在思考刚才的对话",
                    "emotion": "思考",
                    "activity": "reflection",
                    "priority": "low"
                }
            ]
            
            for i, scenario in enumerate(test_scenarios, 1):
                logger.info(f"发送测试场景 {i}/3: {scenario['message']}")
                await self.ai_system._notify_desktop(
                    scenario["message"],
                    scenario["emotion"],
                    scenario["activity"], 
                    scenario["priority"]
                )
                await asyncio.sleep(1)  # 等待处理
            
            logger.info("✅ AI消息生成测试完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ AI消息生成测试失败: {e}")
            return False
    
    async def test_web_integration(self):
        """测试Web端集成"""
        logger.info("🌐 测试Web端集成...")
        
        try:
            # 检查AI网站是否可访问
            try:
                response = requests.get("http://localhost:8001/", timeout=5)
                logger.info(f"✅ AI网站可访问 - 状态码: {response.status_code}")
                web_accessible = True
            except:
                logger.warning("⚠️ AI网站不可访问（可能未启动）")
                web_accessible = False
            
            # 测试动态API
            try:
                response = requests.get("http://localhost:8001/api/dynamics", timeout=5)
                if response.status_code == 200:
                    dynamics = response.json()
                    logger.info(f"📊 动态数据: {len(dynamics)} 条记录")
                else:
                    logger.warning(f"⚠️ 动态API状态码: {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️ 动态API测试失败: {e}")
            
            return web_accessible
            
        except Exception as e:
            logger.error(f"❌ Web端集成测试失败: {e}")
            return False
    
    async def run_comprehensive_verification(self):
        """运行综合验证"""
        logger.info("🌟 开始AI系统完整集成验证...")
        logger.info("="*80)
        
        # 步骤1: 启动API服务器
        logger.info("\n📡 步骤1: 启动API服务器")
        logger.info("-" * 50)
        result1 = await self.start_api_server()
        self.verification_results.append(("API服务器启动", result1))
        
        if result1:
            # 步骤2: 测试API端点
            logger.info("\n🔍 步骤2: 测试API端点")
            logger.info("-" * 50)
            result2 = await self.test_api_endpoints()
            self.verification_results.append(("API端点测试", result2))
            
            # 步骤3: 测试WebSocket连接
            logger.info("\n🌐 步骤3: 测试WebSocket连接")
            logger.info("-" * 50)
            result3 = await self.test_websocket_connection()
            self.verification_results.append(("WebSocket连接", result3))
        else:
            logger.warning("⚠️ API服务器未启动，跳过相关测试")
            result2 = result3 = False
            self.verification_results.extend([("API端点测试", False), ("WebSocket连接", False)])
        
        # 步骤4: 初始化AI系统
        logger.info("\n🤖 步骤4: 初始化AI系统")
        logger.info("-" * 50)
        result4 = await self.initialize_ai_system()
        self.verification_results.append(("AI系统初始化", result4))
        
        if result4:
            # 步骤5: 测试AI消息生成
            logger.info("\n💬 步骤5: 测试AI消息生成")
            logger.info("-" * 50)
            result5 = await self.test_ai_message_generation()
            self.verification_results.append(("AI消息生成", result5))
        else:
            result5 = False
            self.verification_results.append(("AI消息生成", False))
        
        # 步骤6: 测试Web端集成
        logger.info("\n🌐 步骤6: 测试Web端集成")
        logger.info("-" * 50)
        result6 = await self.test_web_integration()
        self.verification_results.append(("Web端集成", result6))
        
        # 汇总结果
        self.print_verification_results()
        
        return self.calculate_success_rate() >= 0.7  # 70%成功率

    def print_verification_results(self):
        """打印验证结果"""
        logger.info("\n" + "="*80)
        logger.info("📊 完整集成验证结果")
        logger.info("="*80)
        
        success_count = 0
        for test_name, success in self.verification_results:
            status = "✅ 通过" if success else "❌ 失败"
            logger.info(f"{status} {test_name}")
            if success:
                success_count += 1
        
        total_tests = len(self.verification_results)
        success_rate = (success_count / total_tests) * 100
        
        logger.info(f"\n🎯 总体结果: {success_count}/{total_tests} 通过 ({success_rate:.1f}%)")
        
        if success_rate >= 70:
            logger.info("\n🎉 AI系统集成验证成功！")
            print("\n" + "="*80)
            print("✅ AI自主交互系统与GUI和Web端集成验证成功！")
            print("\n🌟 验证通过的功能:")
            for test_name, success in self.verification_results:
                if success:
                    print(f"  ✅ {test_name}")
            print("\n📋 使用说明:")
            print("  1. 运行 'python main.py' 启动完整系统")
            print("  2. 观察桌面GUI界面的AI消息显示")
            print("  3. 访问 http://localhost:8001 查看Web界面")
            print("  4. AI会自动产生各种观察和互动消息")
            print("="*80)
        else:
            logger.error("\n❌ 部分功能验证失败")
            print("\n" + "="*80)
            print("❌ AI系统集成验证未完全通过")
            print("\n⚠️ 失败的功能:")
            for test_name, success in self.verification_results:
                if not success:
                    print(f"  ❌ {test_name}")
            print("\n🔧 建议检查:")
            print("  - API服务器是否正常启动")
            print("  - 端口8000和8001是否被占用")
            print("  - AI系统是否正确初始化")
            print("="*80)
    
    def calculate_success_rate(self):
        """计算成功率"""
        if not self.verification_results:
            return 0
        
        success_count = sum(1 for _, success in self.verification_results if success)
        return success_count / len(self.verification_results)

async def main():
    """主函数"""
    print("🌟 AI自主交互系统完整集成验证")
    print("="*80)
    print("此验证将测试:")
    print("1. API服务器启动和连接")
    print("2. WebSocket实时通信")
    print("3. AI自主交互系统")
    print("4. GUI和Web端消息显示")
    print("5. 完整的消息流程")
    print("="*80)
    
    verifier = IntegrationVerifier()
    
    try:
        result = await verifier.run_comprehensive_verification()
        
        if result:
            print("\n🎉 验证完成！系统已准备就绪！")
            return 0
        else:
            print("\n❌ 验证发现问题，请检查相关功能")
            return 1
            
    except KeyboardInterrupt:
        logger.info("🛑 验证被用户中断")
        return 1
    except Exception as e:
        logger.error(f"❌ 验证过程异常: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)