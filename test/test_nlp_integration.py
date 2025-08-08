#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试自然语言处理集成功能
"""

import asyncio
import sys
from datetime import datetime

# 测试用例
test_cases = [
    {
        "input": "你看得到我的屏幕吗？",
        "expected_functions": ["screen_analysis"],
        "description": "屏幕分析触发测试"
    },
    {
        "input": "能看见我吗？我现在什么表情？",
        "expected_functions": ["camera_analysis"],
        "description": "摄像头分析触发测试"
    },
    {
        "input": "我写了一本小说，名为story.txt，你能读取吗？",
        "expected_functions": ["file_reading"],
        "description": "特定文件读取测试"
    },
    {
        "input": "帮我搜索一下人工智能的最新进展",
        "expected_functions": ["web_search"],
        "description": "网络搜索触发测试"
    },
    {
        "input": "看看我现在的环境怎么样",
        "expected_functions": ["general_perception"],
        "description": "综合感知触发测试"
    },
    {
        "input": "今天天气不错",
        "expected_functions": [],
        "description": "普通对话无功能触发测试"
    }
]

async def test_nlp_function_detection():
    """测试自然语言处理功能检测"""
    print("🧠 测试自然语言处理功能检测...")
    
    try:
        from natural_language_processor import natural_language_processor
        
        passed = 0
        total = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n测试 {i}/{total}: {test_case['description']}")
            print(f"输入: \"{test_case['input']}\"")
            
            try:
                # 只测试功能检测，不实际执行
                detected_functions = natural_language_processor._detect_required_functions(test_case['input'])
                expected = test_case['expected_functions']
                
                print(f"检测到的功能: {detected_functions}")
                print(f"期望的功能: {expected}")
                
                # 检查是否匹配
                if set(detected_functions) == set(expected):
                    print("✅ 检测正确")
                    passed += 1
                else:
                    print("❌ 检测错误")
                    
            except Exception as e:
                print(f"❌ 测试异常: {e}")
        
        print(f"\n🎯 功能检测测试结果: {passed}/{total} 通过")
        return passed == total
        
    except Exception as e:
        print(f"❌ 自然语言处理器导入失败: {e}")
        return False

async def test_nlp_full_processing():
    """测试完整的自然语言处理流程"""
    print("\n🔄 测试完整的自然语言处理流程...")
    
    try:
        from natural_language_processor import natural_language_processor
        
        # 选择一个简单的测试用例
        test_input = "你看得到我的屏幕吗？"
        print(f"测试输入: \"{test_input}\"")
        
        # 执行完整处理（带超时）
        result = await asyncio.wait_for(
            natural_language_processor.process_user_input(test_input),
            timeout=30
        )
        
        print("✅ 处理完成")
        print(f"检测到的功能: {result.get('detected_functions', [])}")
        print(f"功能结果数量: {len(result.get('function_results', {}))}")
        
        if result.get('enhanced_context'):
            print("✅ 生成了增强上下文")
            print(f"上下文长度: {len(result['enhanced_context'])} 字符")
        else:
            print("⚠️ 未生成增强上下文")
        
        return True
        
    except asyncio.TimeoutError:
        print("⏰ 处理超时")
        return False
    except Exception as e:
        print(f"❌ 处理异常: {e}")
        return False

async def test_file_path_extraction():
    """测试文件路径提取功能"""
    print("\n📁 测试文件路径提取功能...")
    
    try:
        from natural_language_processor import natural_language_processor
        
        file_test_cases = [
            "我写了一个文件叫test.txt",
            "能读取story.md吗？",
            "文件名为config.json的内容是什么",
            "没有文件名的普通句子"
        ]
        
        passed = 0
        for test_input in file_test_cases:
            print(f"测试: \"{test_input}\"")
            
            file_info = natural_language_processor._extract_file_info(test_input)
            print(f"提取结果: {file_info}")
            
            # 简单验证
            if "test.txt" in test_input and file_info.get('specific_file') == 'test.txt':
                passed += 1
                print("✅ 提取正确")
            elif "story.md" in test_input and file_info.get('specific_file') == 'story.md':
                passed += 1
                print("✅ 提取正确")
            elif "config.json" in test_input and file_info.get('specific_file') == 'config.json':
                passed += 1
                print("✅ 提取正确")
            elif "没有文件名" in test_input and not file_info.get('specific_file'):
                passed += 1
                print("✅ 正确识别无文件名")
            else:
                print("❌ 提取错误")
        
        print(f"\n🎯 文件路径提取测试: {passed}/{len(file_test_cases)} 通过")
        return passed == len(file_test_cases)
        
    except Exception as e:
        print(f"❌ 文件路径提取测试失败: {e}")
        return False

async def test_emotion_based_file_reading():
    """测试基于情绪的文件阅读"""
    print("\n😊 测试基于情绪的文件阅读...")
    
    try:
        from proactive_file_reader import proactive_file_reader
        
        # 测试正常情绪
        print("测试正常情绪强度 (0.3)...")
        normal_result = await asyncio.wait_for(
            proactive_file_reader.discover_and_read_files(0.3),
            timeout=15
        )
        print(f"✅ 正常模式完成，发现 {normal_result.get('discovered_count', 0)} 个文件")
        
        # 测试激烈情绪
        print("\n测试激烈情绪强度 (0.8)...")
        intense_result = await asyncio.wait_for(
            proactive_file_reader.discover_and_read_files(0.8),
            timeout=15
        )
        print(f"✅ 激烈模式完成，发现 {intense_result.get('discovered_count', 0)} 个文件")
        
        return True
        
    except asyncio.TimeoutError:
        print("⏰ 情绪文件阅读测试超时")
        return False
    except Exception as e:
        print(f"❌ 情绪文件阅读测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🚀 StarryNight AGENT 自然语言处理集成测试")
    print("=" * 60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("自然语言功能检测", test_nlp_function_detection),
        ("完整NLP处理流程", test_nlp_full_processing),
        ("文件路径提取", test_file_path_extraction),
        ("基于情绪的文件阅读", test_emotion_based_file_reading),
    ]
    
    results = []
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}测试...")
        try:
            result = await test_func()
            results.append((test_name, result))
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 自然语言处理集成测试结果:")
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("🎉 所有自然语言处理功能测试通过！")
        print("💡 新功能已成功集成:")
        print("   • 🧠 智能关键词检测和功能调用")
        print("   • 📁 智能文件路径识别和读取")
        print("   • 😊 基于情绪强度的文件探索策略")
        print("   • 🔄 无缝集成到对话流程中")
        print("   • 🎭 增强的上下文生成")
    elif passed >= len(results) * 0.75:
        print("⚠️ 大部分自然语言处理功能正常")
    else:
        print("🔧 需要进一步调优自然语言处理功能")
    
    print("\n🌟 StarryNight现在能更智能地理解和响应用户的自然语言请求！")
    
    return passed >= len(results) * 0.75

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