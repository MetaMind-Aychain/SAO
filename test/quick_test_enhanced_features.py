#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试增强AI功能 - 简化版本，避免长时间等待
"""

import asyncio
import sys
import time
from datetime import datetime

async def quick_test_enhanced_screen():
    """快速测试增强屏幕分析"""
    print("🖥️ 快速测试增强屏幕分析...")
    try:
        from enhanced_screen_analyzer import enhanced_screen_analyzer
        
        result = await asyncio.wait_for(
            enhanced_screen_analyzer.analyze_screen_content(), 
            timeout=10
        )
        
        if result and 'error' not in result:
            print(f"✅ 屏幕分析成功")
            activity = result.get('user_activity', {}).get('primary_activity', '未知')
            print(f"   用户活动: {activity}")
            return True
        else:
            print(f"❌ 屏幕分析失败: {result}")
            return False
            
    except asyncio.TimeoutError:
        print("⏰ 屏幕分析超时")
        return False
    except Exception as e:
        print(f"❌ 屏幕分析异常: {e}")
        return False

async def quick_test_enhanced_camera():
    """快速测试增强摄像头分析"""
    print("📷 快速测试增强摄像头分析...")
    try:
        from enhanced_camera_analyzer import enhanced_camera_analyzer
        
        result = await asyncio.wait_for(
            enhanced_camera_analyzer.analyze_camera_content(), 
            timeout=5
        )
        
        if result and 'error' not in result:
            print(f"✅ 摄像头分析成功")
            behavior = result.get('behavior_analysis', {}).get('primary_behavior', '未知')
            print(f"   主要行为: {behavior}")
            return True
        else:
            print(f"❌ 摄像头分析失败")
            return False
            
    except asyncio.TimeoutError:
        print("⏰ 摄像头分析超时")
        return False
    except Exception as e:
        print(f"❌ 摄像头分析异常: {e}")
        return False

async def quick_test_file_reading():
    """快速测试文件阅读"""
    print("📁 快速测试文件阅读...")
    try:
        from proactive_file_reader import proactive_file_reader
        
        result = await asyncio.wait_for(
            proactive_file_reader.discover_and_read_files(), 
            timeout=15
        )
        
        if result and 'error' not in result:
            print(f"✅ 文件阅读成功")
            count = result.get('read_count', 0)
            print(f"   阅读文件: {count}")
            return True
        else:
            print(f"❌ 文件阅读失败")
            return False
            
    except asyncio.TimeoutError:
        print("⏰ 文件阅读超时")
        return False
    except Exception as e:
        print(f"❌ 文件阅读异常: {e}")
        return False

async def quick_test_web_browsing():
    """快速测试网络浏览"""
    print("🌐 快速测试网络浏览...")
    try:
        from proactive_web_browser import proactive_web_browser
        
        result = await asyncio.wait_for(
            proactive_web_browser.browse_and_discover(), 
            timeout=10
        )
        
        if result and 'error' not in result:
            print(f"✅ 网络浏览成功")
            topic = result.get('search_topic', '未知')
            print(f"   搜索主题: {topic}")
            return True
        else:
            print(f"❌ 网络浏览失败")
            return False
            
    except asyncio.TimeoutError:
        print("⏰ 网络浏览超时")
        return False
    except Exception as e:
        print(f"❌ 网络浏览异常: {e}")
        return False

async def quick_test_emotion_core():
    """快速测试情绪核心"""
    print("🎭 快速测试情绪核心...")
    try:
        from emotional_ai_core import get_emotion_core, EmotionType
        from config import config
        
        emotion_core = get_emotion_core(config)
        
        # 测试基本方法
        if hasattr(emotion_core, 'should_explore') and hasattr(emotion_core, 'choose_exploration_action'):
            # 触发一些情绪
            emotion_core.add_emotion(EmotionType.CURIOUS, 0.8)
            
            should_explore = emotion_core.should_explore()
            action = emotion_core.choose_exploration_action() if should_explore else 'none'
            
            print(f"✅ 情绪核心正常")
            print(f"   应该探索: {should_explore}")
            print(f"   探索动作: {action}")
            return True
        else:
            print(f"❌ 情绪核心缺少方法")
            return False
            
    except Exception as e:
        print(f"❌ 情绪核心异常: {e}")
        return False

async def main():
    """主测试函数"""
    print("🚀 StarryNight AGENT 增强AI功能快速测试")
    print("=" * 50)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("情绪核心", quick_test_emotion_core),
        ("增强屏幕分析", quick_test_enhanced_screen),
        ("增强摄像头分析", quick_test_enhanced_camera),
        ("文件阅读", quick_test_file_reading),
        ("网络浏览", quick_test_web_browsing),
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
    print("\n" + "=" * 50)
    print("📊 快速测试结果:")
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 项测试通过")
    
    if passed >= len(results) * 0.8:
        print("🎉 大部分增强功能正常工作！")
        print("💡 新增功能已成功集成到StarryNight AGENT中")
    elif passed >= len(results) * 0.6:
        print("⚠️ 多数增强功能正常，少数需要调优")
    else:
        print("🔧 需要进一步优化部分功能")
    
    print("\n🌟 StarryNight的增强感知和互动能力测试完成！")
    
    return passed >= len(results) * 0.6

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