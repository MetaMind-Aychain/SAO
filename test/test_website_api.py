#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI网站API接口
"""

import asyncio
import aiohttp
import json

async def test_api_endpoints():
    """测试各个API端点"""
    
    base_url = "http://127.0.0.1:8080"
    
    endpoints = [
        "/",
        "/api/ai/status", 
        "/api/dynamics",
        "/api/developer/updates"
    ]
    
    print("🔍 测试AI网站API接口...")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            try:
                print(f"\n📡 测试: {url}")
                
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    status = response.status
                    
                    if status == 200:
                        print(f"  ✅ 状态: {status} OK")
                        
                        if endpoint != "/":  # 首页是HTML，其他是JSON
                            try:
                                data = await response.json()
                                if isinstance(data, list):
                                    print(f"  📊 数据: 列表，{len(data)} 项")
                                elif isinstance(data, dict):
                                    print(f"  📊 数据: 对象，{len(data)} 字段")
                                else:
                                    print(f"  📊 数据: {type(data)}")
                            except Exception as e:
                                print(f"  ⚠️ JSON解析失败: {e}")
                        else:
                            content = await response.text()
                            print(f"  📊 HTML长度: {len(content)} 字符")
                    else:
                        print(f"  ❌ 状态: {status}")
                        text = await response.text()
                        print(f"  错误: {text[:200]}")
                        
            except aiohttp.ClientError as e:
                print(f"  ❌ 连接错误: {e}")
            except asyncio.TimeoutError:
                print(f"  ❌ 超时")
            except Exception as e:
                print(f"  ❌ 其他错误: {e}")

async def test_database_connection():
    """测试数据库连接"""
    print("\n" + "=" * 50)
    print("🗄️ 测试数据库连接...")
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from ai_website.app import engine, Base
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("  ✅ 数据库连接成功，表已创建")
        
        # 测试基本查询
        from ai_website.app import SessionLocal
        db = SessionLocal()
        try:
            # 这里可以添加一些基本的数据库操作测试
            print("  ✅ 数据库会话创建成功")
        finally:
            db.close()
            
    except Exception as e:
        print(f"  ❌ 数据库连接失败: {e}")

def main():
    """主函数"""
    print("🌐 AI网站测试工具")
    print("检查网站是否正常运行...")
    
    # 首先测试数据库
    asyncio.run(test_database_connection())
    
    # 然后测试API
    asyncio.run(test_api_endpoints())
    
    print("\n" + "=" * 50)
    print("💡 如果所有测试都通过，说明网站后端正常运行")
    print("💡 如果测试失败，请确保：")
    print("   1. 网站已启动: python ai_website/app.py")
    print("   2. 端口8080未被占用")
    print("   3. 防火墙没有阻止连接")

if __name__ == "__main__":
    main()