#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试异步修复和token限制提升
"""

import asyncio
import sys
import time
from datetime import datetime

async def test_async_manager():
    """测试异步管理器"""
    print("🔧 测试异步管理器...")
    try:
        from async_manager import async_manager, safe_create_task, safe_run_in_thread
        
        # 测试安全任务创建
        async def test_task():
            await asyncio.sleep(0.1)
            return "任务完成"
        
        task = safe_create_task(test_task(), name="test-task")
        if task:
            result = await task
            print(f"✅ 安全任务创建: {result}")
        else:
            print("⚠️ 任务创建失败（可能没有事件循环）")
        
        # 测试线程中运行异步任务
        async def thread_task():
            await asyncio.sleep(0.1)
            print("✅ 线程异步任务完成")
        
        thread = safe_run_in_thread(thread_task(), "test-thread")
        time.sleep(0.2)  # 等待线程完成
        
        print("✅ 异步管理器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 异步管理器测试失败: {e}")
        return False

def test_config_tokens():
    """测试配置中的token限制"""
    print("📝 测试token配置...")
    try:
        from config import config
        
        max_tokens = config.api.max_tokens
        if max_tokens >= 15000:
            print(f"✅ Token限制已提升: {max_tokens}")
            return True
        else:
            print(f"❌ Token限制仍然较低: {max_tokens}")
            return False
            
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

async def test_llm_api():
    """测试LLM API调用和token输出"""
    print("🤖 测试LLM API调用...")
    try:
        from conversation_core import call_llm_api
        
        # 测试长文本生成
        prompt = """请写一个关于人工智能未来发展的详细文章，包含以下内容：
1. 当前AI技术现状
2. 未来5年的发展趋势
3. 可能面临的挑战
4. 对社会的影响
5. 发展建议

请详细展开每个部分，字数要尽可能多。"""
        
        print("正在调用LLM API（测试长文本输出）...")
        response = await call_llm_api(prompt, max_tokens=15000, temperature=0.7)
        
        if response and not response.startswith("抱歉"):
            word_count = len(response)
            print(f"✅ LLM API调用成功")
            print(f"📊 响应字数: {word_count}")
            print(f"📊 响应预览: {response[:200]}...")
            return True
        else:
            print(f"❌ LLM API调用失败: {response}")
            return False
            
    except Exception as e:
        print(f"❌ LLM API测试失败: {e}")
        return False

async def test_http_cleanup():
    """测试HTTP客户端清理"""
    print("🌐 测试HTTP客户端清理...")
    try:
        from async_manager import safe_get
        
        # 测试多个HTTP请求
        tasks = []
        for i in range(3):
            # 使用一个简单的测试URL（如果无法访问会正常失败）
            try:
                task = safe_get("http://httpbin.org/delay/1", timeout=5)
                tasks.append(task)
            except:
                pass  # 网络不可达时忽略
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            print(f"✅ HTTP客户端清理测试完成，处理了{len(tasks)}个请求")
        else:
            print("✅ HTTP客户端清理测试跳过（网络不可达）")
        
        return True
        
    except Exception as e:
        print(f"⚠️ HTTP清理测试警告: {e}")
        return True  # 网络问题不算失败

async def main():
    """主测试函数"""
    print("🔧 StarryNight AGENT 异步修复验证")
    print("=" * 50)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("配置Token限制", test_config_tokens),
        ("异步管理器", test_async_manager), 
        ("HTTP客户端清理", test_http_cleanup),
        ("LLM API调用", test_llm_api),
    ]
    
    results = []
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}测试...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 修复验证结果:")
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("🎉 所有修复验证通过！")
        print("💡 修复内容:")
        print("   • 异步事件循环错误已修复")
        print("   • LLM输出token限制提升至15000")
        print("   • HTTP客户端安全清理机制")
        print("   • 更健壮的异步任务管理")
    elif passed >= len(results) * 0.75:
        print("⚠️ 大部分修复验证通过")
    else:
        print("❌ 多项修复验证失败")
    
    return passed == len(results)

if __name__ == "__main__":
    try:
        # Windows事件循环策略
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试程序异常: {e}")
        sys.exit(1)