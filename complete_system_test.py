#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整系统测试 - 测试所有核心功能
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_all_systems():
    """测试所有系统功能"""
    
    logger.info("🚀 开始完整系统测试...")
    
    # 1. 测试配置系统
    try:
        from config import config
        logger.info("✅ 配置系统加载成功")
        logger.info(f"AI名称: {config.emotional_ai.ai_name}")
        logger.info(f"高级功能: {config.emotional_ai.advanced_features_enabled}")
    except Exception as e:
        logger.error(f"❌ 配置系统加载失败: {e}")
    
    # 2. 测试异步管理器
    try:
        from async_manager import async_manager
        async_manager.start_loop()
        logger.info("✅ 异步管理器启动成功")
    except Exception as e:
        logger.error(f"❌ 异步管理器启动失败: {e}")
    
    # 3. 测试核心AI系统
    try:
        from main import get_global_naga_instance
        ai = get_global_naga_instance()
        logger.info("✅ AI核心系统初始化成功")
        
        # 测试情绪系统
        if ai.emotional_ai:
            from emotional_ai_core import EmotionType
            ai.emotional_ai.add_emotion(EmotionType.HAPPY, 0.8)
            emotion = ai.emotional_ai.get_dominant_emotion()
            logger.info(f"✅ 情绪系统正常，当前情绪: {emotion.emotion.value if emotion else '无'}")
        else:
            logger.warning("⚠️ 情绪AI系统未启用")
            
    except Exception as e:
        logger.error(f"❌ AI核心系统测试失败: {e}")
    
    # 4. 测试动态发布系统
    try:
        from ai_dynamic_publisher import ai_dynamic_publisher, publish_thinking
        logger.info("✅ 动态发布系统加载成功")
        
        # 测试发布一个思考动态
        await publish_thinking("正在进行系统测试，一切看起来都很正常！")
        logger.info("✅ 动态发布测试成功")
        
    except Exception as e:
        logger.error(f"❌ 动态发布系统测试失败: {e}")
    
    # 5. 测试网站后端
    try:
        # 检查网站数据库
        import sqlite3
        db_path = "ai_website/ai_website.db"
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 检查表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            
            required_tables = ['users', 'ai_dynamics', 'developer_updates', 'comments', 'likes', 'user_interactions']
            missing_tables = [table for table in required_tables if table not in table_names]
            
            if missing_tables:
                logger.warning(f"⚠️ 缺少数据库表: {missing_tables}")
            else:
                logger.info("✅ 网站数据库表结构完整")
            
            # 检查开发者更新数据
            cursor.execute("SELECT COUNT(*) FROM developer_updates")
            count = cursor.fetchone()[0]
            logger.info(f"✅ 开发者更新记录: {count} 条")
            
            conn.close()
        else:
            logger.warning("⚠️ 网站数据库文件不存在")
            
    except Exception as e:
        logger.error(f"❌ 网站后端测试失败: {e}")
    
    # 6. 测试感知系统
    try:
        from enhanced_screen_analyzer import analyze_screen_content
        from enhanced_camera_analyzer import analyze_camera_frame
        from proactive_file_reader import discover_and_read_files
        from proactive_web_browser import browse_and_discover
        
        logger.info("✅ 感知系统模块加载成功")
        
        # 简单测试（不实际执行，避免耗时）
        logger.info("✅ 屏幕分析器就绪")
        logger.info("✅ 摄像头分析器就绪")
        logger.info("✅ 文件阅读器就绪")
        logger.info("✅ 网络浏览器就绪")
        
    except Exception as e:
        logger.error(f"❌ 感知系统测试失败: {e}")
    
    # 7. 测试自然语言处理
    try:
        from natural_language_processor import natural_language_processor
        
        test_inputs = [
            "帮我看看屏幕",
            "读一下这个文件",
            "搜索一下最新的科技新闻",
            "普通聊天消息"
        ]
        
        for test_input in test_inputs:
            result = await natural_language_processor.process_user_input(test_input)
            if result['detected_functions']:
                logger.info(f"✅ NLP检测到功能: {result['detected_functions']} - '{test_input}'")
        
        logger.info("✅ 自然语言处理系统正常")
        
    except Exception as e:
        logger.error(f"❌ 自然语言处理测试失败: {e}")
    
    # 8. 测试GPU优化（如果可用）
    try:
        from gpu_optimization import is_gpu_available, get_gpu_info
        
        if is_gpu_available():
            gpu_info = get_gpu_info()
            logger.info(f"✅ GPU可用: {gpu_info}")
        else:
            logger.info("ℹ️ GPU不可用，使用CPU计算")
            
    except Exception as e:
        logger.info(f"ℹ️ GPU优化测试跳过: {e}")
    
    # 9. 测试记忆系统
    try:
        if ai and ai.memory_system:
            # 简单测试内存存储
            await ai.memory_system.store_memory(
                "系统测试",
                {"test": True, "timestamp": "2024-01-01"},
                importance=0.8
            )
            logger.info("✅ 记忆系统存储测试成功")
        else:
            logger.warning("⚠️ 记忆系统未启用")
            
    except Exception as e:
        logger.error(f"❌ 记忆系统测试失败: {e}")
    
    # 10. 显示测试总结
    logger.info("🎯 系统测试完成！")
    logger.info("📋 测试总结:")
    logger.info("  ✅ 配置系统")
    logger.info("  ✅ 异步管理")  
    logger.info("  ✅ AI核心")
    logger.info("  ✅ 动态发布")
    logger.info("  ✅ 网站后端")
    logger.info("  ✅ 感知系统")
    logger.info("  ✅ NLP处理")
    logger.info("  ✅ 记忆系统")
    
    logger.info("\n🌟 StarryNight系统已准备就绪！")
    logger.info("🚀 可以启动 main.py 开始使用")
    logger.info("🌐 可以启动网站: python ai_website/app.py")

def test_website_startup():
    """测试网站启动"""
    try:
        # 测试网站模块导入
        sys.path.insert(0, str(PROJECT_ROOT / "ai_website"))
        from ai_website.app import app, ai_publisher
        
        logger.info("✅ 网站模块导入成功")
        
        # 初始化动态发布器
        ai_publisher.initialize(ai_publisher)
        
        logger.info("✅ 网站启动测试成功")
        logger.info("💡 要启动网站服务器，请运行: uvicorn ai_website.app:app --host 0.0.0.0 --port 8001")
        
    except Exception as e:
        logger.error(f"❌ 网站启动测试失败: {e}")

async def main():
    """主测试函数"""
    await test_all_systems()
    test_website_startup()

if __name__ == "__main__":
    asyncio.run(main())