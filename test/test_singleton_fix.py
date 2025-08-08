#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试单例修复是否有效
"""

import time
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_singleton():
    """测试单例模式"""
    logger.info("🧪 测试全局单例模式...")
    
    # 测试1：多次调用应该返回同一个实例
    from main import get_global_naga_instance
    
    instance1 = get_global_naga_instance()
    instance2 = get_global_naga_instance()
    
    if instance1 is instance2:
        logger.info("✅ 单例测试通过：多次调用返回同一实例")
    else:
        logger.error("❌ 单例测试失败：多次调用返回不同实例")
        return False
    
    # 测试2：多线程环境下的单例
    instances = []
    
    def get_instance():
        instance = get_global_naga_instance()
        instances.append(instance)
    
    threads = []
    for i in range(5):
        thread = threading.Thread(target=get_instance)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # 检查所有实例是否相同
    if all(inst is instances[0] for inst in instances):
        logger.info("✅ 多线程单例测试通过：所有线程获得同一实例")
    else:
        logger.error("❌ 多线程单例测试失败：线程获得不同实例")
        return False
    
    return True

def test_database_fields():
    """测试数据库字段修复"""
    logger.info("🧪 测试数据库字段修复...")
    
    try:
        # 尝试导入和初始化AI网站模块
        from ai_website.app import Base, engine, AIDynamic
        
        # 检查是否能正常创建表
        Base.metadata.create_all(bind=engine)
        logger.info("✅ 数据库表创建成功，字段修复有效")
        
        # 检查AIDynamic模型
        if hasattr(AIDynamic, 'extra_data'):
            logger.info("✅ AIDynamic.extra_data 字段存在")
        else:
            logger.error("❌ AIDynamic.extra_data 字段不存在")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ 数据库字段测试失败: {e}")
        return False

def main():
    """主测试函数"""
    logger.info("=" * 50)
    logger.info("🧪 开始修复验证测试")
    logger.info("=" * 50)
    
    test_results = []
    
    # 测试单例修复
    test_results.append(("单例模式", test_singleton()))
    
    # 测试数据库字段修复
    test_results.append(("数据库字段", test_database_fields()))
    
    # 输出结果
    logger.info("=" * 50)
    logger.info("📊 测试结果总结")
    logger.info("=" * 50)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        logger.info(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in test_results)
    
    if all_passed:
        logger.info("🎉 所有修复验证测试通过！")
    else:
        logger.error("⚠️ 部分测试失败，需要进一步检查")
    
    return all_passed

if __name__ == "__main__":
    main()