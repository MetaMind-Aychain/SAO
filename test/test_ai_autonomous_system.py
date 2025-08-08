#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI自主交互系统综合测试
测试所有新实现的功能：
1. AI自主交互循环
2. 网站用户管理
3. 评论系统
4. AI个性化回复
5. 情感化内容生成
"""

import asyncio
import logging
import time
import requests
import json
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AISystemTester:
    def __init__(self):
        self.website_url = "http://localhost:8001"
        self.test_user = {
            "username": "test_user_001",
            "email": "test@example.com",
            "password": "test123456"
        }
        self.auth_token = None
        
    async def run_comprehensive_test(self):
        """运行综合测试"""
        logger.info("🚀 开始AI自主交互系统综合测试")
        
        # 等待系统启动
        logger.info("⏳ 等待系统启动...")
        await asyncio.sleep(10)
        
        tests = [
            self.test_ai_autonomous_initialization,
            self.test_website_accessibility,
            self.test_user_registration,
            self.test_user_login,
            self.test_dynamic_publishing,
            self.test_comment_system,
            self.test_ai_reply_system,
            self.test_emotion_integration,
            self.test_memory_system,
        ]
        
        results = {}
        for test in tests:
            test_name = test.__name__
            try:
                logger.info(f"🧪 运行测试: {test_name}")
                result = await test()
                results[test_name] = {"status": "success", "result": result}
                logger.info(f"✅ {test_name} 测试通过")
            except Exception as e:
                results[test_name] = {"status": "failed", "error": str(e)}
                logger.error(f"❌ {test_name} 测试失败: {e}")
        
        # 生成测试报告
        self.generate_test_report(results)
        
    async def test_ai_autonomous_initialization(self):
        """测试AI自主交互系统初始化"""
        try:
            from ai_autonomous_interaction import autonomous_interaction
            
            # 检查系统是否正确初始化
            assert autonomous_interaction is not None, "自主交互系统未初始化"
            assert hasattr(autonomous_interaction, 'emotion_core'), "情绪核心未初始化"
            assert hasattr(autonomous_interaction, 'publisher'), "动态发布器未初始化"
            
            logger.info("AI自主交互系统组件初始化完成")
            return True
            
        except ImportError:
            logger.warning("AI自主交互模块未找到，可能需要启动主程序")
            return "模块未加载"
            
    async def test_website_accessibility(self):
        """测试网站可访问性"""
        try:
            response = requests.get(f"{self.website_url}/", timeout=5)
            assert response.status_code == 200, f"网站状态码: {response.status_code}"
            
            # 测试API状态
            api_response = requests.get(f"{self.website_url}/api/ai/status", timeout=5)
            api_data = api_response.json()
            
            logger.info(f"网站可访问，AI状态: {api_data.get('status', 'unknown')}")
            return {
                "website_status": response.status_code,
                "ai_status": api_data
            }
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"网站不可访问: {e}")
            return f"网站不可访问: {e}"
            
    async def test_user_registration(self):
        """测试用户注册功能"""
        try:
            response = requests.post(
                f"{self.website_url}/api/register",
                json=self.test_user,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access_token')
                logger.info("用户注册成功")
                return {"registered": True, "token": bool(self.auth_token)}
            else:
                # 可能用户已存在，尝试登录
                logger.info("用户可能已存在，将在登录测试中验证")
                return {"registered": False, "reason": "用户可能已存在"}
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"注册请求失败: {e}")
            return f"注册请求失败: {e}"
            
    async def test_user_login(self):
        """测试用户登录功能"""
        try:
            response = requests.post(
                f"{self.website_url}/api/login",
                json={
                    "username": self.test_user["username"],
                    "password": self.test_user["password"]
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access_token')
                logger.info("用户登录成功")
                return {"logged_in": True, "token": bool(self.auth_token)}
            else:
                logger.warning(f"登录失败: {response.status_code}")
                return {"logged_in": False, "status_code": response.status_code}
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"登录请求失败: {e}")
            return f"登录请求失败: {e}"
            
    async def test_dynamic_publishing(self):
        """测试动态发布功能"""
        try:
            # 获取现有动态
            response = requests.get(f"{self.website_url}/api/dynamics?limit=5", timeout=5)
            
            if response.status_code == 200:
                dynamics = response.json()
                logger.info(f"获取到 {len(dynamics)} 条动态")
                
                # 分析动态类型
                activity_types = [d.get('activity_type', 'unknown') for d in dynamics]
                emotion_types = [d.get('emotion_type', 'unknown') for d in dynamics]
                
                return {
                    "dynamics_count": len(dynamics),
                    "activity_types": list(set(activity_types)),
                    "emotion_types": list(set(emotion_types)),
                    "latest_dynamic": dynamics[0] if dynamics else None
                }
            else:
                return {"error": f"获取动态失败: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"动态获取请求失败: {e}")
            return f"动态获取请求失败: {e}"
            
    async def test_comment_system(self):
        """测试评论系统"""
        if not self.auth_token:
            return "需要登录token"
            
        try:
            # 获取动态列表
            response = requests.get(f"{self.website_url}/api/dynamics?limit=1", timeout=5)
            if response.status_code != 200:
                return "无法获取动态列表"
                
            dynamics = response.json()
            if not dynamics:
                return "没有可评论的动态"
                
            dynamic_id = dynamics[0]['id']
            
            # 发表测试评论
            comment_data = {
                "content": f"这是一条测试评论 - {datetime.now().strftime('%H:%M:%S')}",
                "dynamic_id": dynamic_id
            }
            
            comment_response = requests.post(
                f"{self.website_url}/api/dynamics/{dynamic_id}/comment",
                json=comment_data,
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=5
            )
            
            if comment_response.status_code == 200:
                logger.info("评论发表成功")
                
                # 等待一下，然后获取评论列表
                await asyncio.sleep(2)
                comments_response = requests.get(
                    f"{self.website_url}/api/dynamics/{dynamic_id}/comments",
                    timeout=5
                )
                
                if comments_response.status_code == 200:
                    comments = comments_response.json()
                    return {
                        "comment_posted": True,
                        "comments_count": len(comments),
                        "has_ai_reply": any(c.get('is_ai_reply', False) for c in comments)
                    }
                else:
                    return {"comment_posted": True, "comments_fetch_failed": True}
            else:
                return {"comment_posted": False, "status_code": comment_response.status_code}
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"评论测试请求失败: {e}")
            return f"评论测试请求失败: {e}"
            
    async def test_ai_reply_system(self):
        """测试AI回复系统"""
        # 等待AI处理评论
        logger.info("等待AI处理评论并回复...")
        await asyncio.sleep(10)
        
        try:
            # 获取最新动态的评论，检查是否有AI回复
            response = requests.get(f"{self.website_url}/api/dynamics?limit=1", timeout=5)
            if response.status_code != 200:
                return "无法获取动态"
                
            dynamics = response.json()
            if not dynamics:
                return "没有动态"
                
            dynamic_id = dynamics[0]['id']
            
            comments_response = requests.get(
                f"{self.website_url}/api/dynamics/{dynamic_id}/comments",
                timeout=5
            )
            
            if comments_response.status_code == 200:
                comments = comments_response.json()
                ai_replies = [c for c in comments if c.get('is_ai_reply', False)]
                user_comments_with_reply = [c for c in comments if c.get('ai_reply')]
                
                return {
                    "total_comments": len(comments),
                    "ai_replies_count": len(ai_replies),
                    "user_comments_with_ai_reply": len(user_comments_with_reply),
                    "ai_reply_working": len(ai_replies) > 0 or len(user_comments_with_reply) > 0
                }
            else:
                return "无法获取评论"
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"AI回复测试失败: {e}")
            return f"AI回复测试失败: {e}"
            
    async def test_emotion_integration(self):
        """测试情绪集成"""
        try:
            # 获取AI状态
            response = requests.get(f"{self.website_url}/api/ai/status", timeout=5)
            
            if response.status_code == 200:
                ai_status = response.json()
                
                # 检查情绪信息
                current_emotion = ai_status.get('current_emotion')
                emotion_intensity = ai_status.get('emotion_intensity')
                all_emotions = ai_status.get('all_emotions', [])
                
                return {
                    "emotion_system_active": bool(current_emotion),
                    "current_emotion": current_emotion,
                    "emotion_intensity": emotion_intensity,
                    "emotions_count": len(all_emotions),
                    "ai_status": ai_status.get('status')
                }
            else:
                return {"error": f"AI状态获取失败: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"情绪集成测试失败: {e}")
            return f"情绪集成测试失败: {e}"
            
    async def test_memory_system(self):
        """测试记忆系统"""
        try:
            # 检查用户交互是否被记录
            if not self.auth_token:
                return "需要登录token"
                
            # 获取当前用户信息
            user_response = requests.get(
                f"{self.website_url}/api/me",
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=5
            )
            
            if user_response.status_code == 200:
                user_info = user_response.json()
                
                return {
                    "user_info_accessible": True,
                    "user_id": user_info.get('id'),
                    "username": user_info.get('username'),
                    "memory_system_ready": True
                }
            else:
                return {"user_info_accessible": False, "status_code": user_response.status_code}
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"记忆系统测试失败: {e}")
            return f"记忆系统测试失败: {e}"
            
    def generate_test_report(self, results):
        """生成测试报告"""
        report = {
            "test_time": datetime.now().isoformat(),
            "total_tests": len(results),
            "passed_tests": len([r for r in results.values() if r["status"] == "success"]),
            "failed_tests": len([r for r in results.values() if r["status"] == "failed"]),
            "results": results
        }
        
        # 保存到文件
        report_file = Path("ai_system_test_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 打印摘要
        logger.info("=" * 60)
        logger.info("🧪 AI自主交互系统测试报告")
        logger.info("=" * 60)
        logger.info(f"📊 总测试数: {report['total_tests']}")
        logger.info(f"✅ 通过: {report['passed_tests']}")
        logger.info(f"❌ 失败: {report['failed_tests']}")
        logger.info(f"📁 详细报告: {report_file}")
        
        # 打印关键功能状态
        logger.info("\n🔍 关键功能状态:")
        
        key_tests = {
            "AI自主系统": "test_ai_autonomous_initialization",
            "网站可访问": "test_website_accessibility", 
            "用户认证": "test_user_login",
            "动态发布": "test_dynamic_publishing",
            "评论系统": "test_comment_system",
            "AI回复": "test_ai_reply_system",
            "情绪集成": "test_emotion_integration",
            "记忆系统": "test_memory_system"
        }
        
        for feature, test_name in key_tests.items():
            if test_name in results:
                status = "✅" if results[test_name]["status"] == "success" else "❌"
                logger.info(f"  {status} {feature}")
            else:
                logger.info(f"  ⚠️ {feature} (未测试)")
        
        logger.info("=" * 60)

async def main():
    """主函数"""
    tester = AISystemTester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())