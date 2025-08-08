#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neo4j连接测试脚本
用于诊断Neo4j数据库连接问题
"""

import sys
import logging
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_neo4j_connection():
    """测试Neo4j连接"""
    print("🔍 Neo4j连接测试")
    print("=" * 50)
    
    # 检查配置
    if not hasattr(config, 'grag'):
        print("❌ GRAG配置不存在")
        return False
    
    if not config.grag.enabled:
        print("❌ GRAG功能未启用")
        return False
    
    print(f"📋 配置信息:")
    print(f"   URI: {config.grag.neo4j_uri}")
    print(f"   用户名: {config.grag.neo4j_user}")
    print(f"   密码: {'*' * len(config.grag.neo4j_password) if config.grag.neo4j_password else '未设置'}")
    
    # 尝试导入py2neo
    try:
        from py2neo import Graph
        print("✅ py2neo库导入成功")
    except ImportError:
        print("❌ py2neo库未安装")
        print("   请运行: pip install py2neo")
        return False
    
    # 尝试连接
    try:
        print("\n🔗 尝试连接Neo4j...")
        graph = Graph(
            config.grag.neo4j_uri,
            auth=(config.grag.neo4j_user, config.grag.neo4j_password)
        )
        
        # 测试连接
        result = graph.run("RETURN 1 as test").data()
        if result:
            print("✅ Neo4j连接成功!")
            print(f"   测试查询结果: {result}")
            return True
        else:
            print("❌ 连接成功但查询失败")
            return False
            
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")
        print("\n💡 可能的解决方案:")
        print("1. 确保Neo4j服务正在运行")
        print("2. 检查端口7687是否开放")
        print("3. 验证用户名和密码")
        print("4. 检查防火墙设置")
        print("5. 如果使用Docker，确保端口映射正确")
        return False

def show_neo4j_setup_guide():
    """显示Neo4j设置指南"""
    print("\n📖 Neo4j设置指南")
    print("=" * 50)
    print("1. 下载并安装Neo4j Desktop或Neo4j Community Edition")
    print("2. 启动Neo4j服务")
    print("3. 创建新数据库或使用默认数据库")
    print("4. 设置用户名和密码")
    print("5. 确保端口7687可访问")
    print("\n🔗 官方文档: https://neo4j.com/docs/")
    print("🐳 Docker方式: docker run -p 7474:7474 -p 7687:7687 neo4j:latest")

if __name__ == "__main__":
    success = test_neo4j_connection()
    
    if not success:
        show_neo4j_setup_guide()
        print("\n⚠️  注意: Neo4j连接失败不会影响其他功能")
        print("   记忆知识图谱将使用内存模式运行")
    
    print("\n✅ 测试完成") 