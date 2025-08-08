#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试增强AI功能 - 验证所有新增的感知和互动能力
"""

import asyncio
import sys
import time
from datetime import datetime

async def test_enhanced_screen_analysis():
    """测试增强屏幕分析"""
    print("🖥️ 测试增强屏幕分析...")
    try:
        from enhanced_screen_analyzer import enhanced_screen_analyzer
        
        result = await enhanced_screen_analyzer.analyze_screen_content()
        
        if result and 'error' not in result:
            print(f"✅ 屏幕分析成功")
            print(f"   用户活动: {result.get('user_activity', {}).get('primary_activity', '未知')}")
            print(f"   参与度: {result.get('user_activity', {}).get('engagement_level', 0):.1f}")
            print(f"   观察: {result.get('observation', '无')[:100]}...")
            return True
        else:
            print(f"❌ 屏幕分析失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 屏幕分析异常: {e}")
        return False

async def test_enhanced_camera_analysis():
    """测试增强摄像头分析"""
    print("📷 测试增强摄像头分析...")
    try:
        from enhanced_camera_analyzer import enhanced_camera_analyzer
        
        result = await enhanced_camera_analyzer.analyze_camera_content()
        
        if result and 'error' not in result:
            print(f"✅ 摄像头分析成功")
            face_count = result.get('face_analysis', {}).get('face_count', 0)
            primary_behavior = result.get('behavior_analysis', {}).get('primary_behavior', '未知')
            print(f"   检测到人脸: {face_count}")
            print(f"   主要行为: {primary_behavior}")
            print(f"   观察: {result.get('observation', '无')[:100]}...")
            return True
        else:
            print(f"❌ 摄像头分析失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 摄像头分析异常: {e}")
        return False

async def test_proactive_file_reading():
    """测试主动文件阅读"""
    print("📁 测试主动文件阅读...")
    try:
        from proactive_file_reader import proactive_file_reader
        
        result = await proactive_file_reader.discover_and_read_files()
        
        if result and 'error' not in result:
            print(f"✅ 文件阅读成功")
            print(f"   发现文件: {result.get('discovered_count', 0)}")
            print(f"   阅读文件: {result.get('read_count', 0)}")
            print(f"   总结: {result.get('summary', '无')[:100]}...")
            return True
        else:
            print(f"❌ 文件阅读失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 文件阅读异常: {e}")
        return False

async def test_proactive_web_browsing():
    """测试主动网络浏览"""
    print("🌐 测试主动网络浏览...")
    try:
        from proactive_web_browser import proactive_web_browser
        
        result = await proactive_web_browser.browse_and_discover()
        
        if result and 'error' not in result:
            print(f"✅ 网络浏览成功")
            print(f"   搜索主题: {result.get('search_topic', '未知')}")
            print(f"   浏览页面: {result.get('pages_browsed', 0)}")
            print(f"   有趣内容: {result.get('interesting_count', 0)}")
            sharing_content = result.get('sharing_content', [])
            if sharing_content:
                print(f"   分享内容: {sharing_content[0][:100]}...")
            return True
        else:
            print(f"❌ 网络浏览失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 网络浏览异常: {e}")
        return False

async def test_emotional_core_integration():
    """测试情绪核心集成"""
    print("🎭 测试情绪核心集成...")
    try:
        from emotional_ai_core import get_emotion_core
        from config import config
        
        emotion_core = get_emotion_core(config)
        
        # 测试探索方法
        if hasattr(emotion_core, 'should_explore') and hasattr(emotion_core, 'choose_exploration_action'):
            should_explore = emotion_core.should_explore()
            action = emotion_core.choose_exploration_action() if should_explore else 'none'
            print(f"✅ 情绪核心方法正常")
            print(f"   应该探索: {should_explore}")
            print(f"   探索动作: {action}")
            return True
        else:
            print(f"❌ 情绪核心缺少必要方法")
            return False
            
    except Exception as e:
        print(f"❌ 情绪核心测试异常: {e}")
        return False

async def test_proactive_behavior_triggers():
    """测试主动行为触发器"""
    print("🤖 测试主动行为触发器...")
    try:
        from emotional_ai_core import get_emotion_core
        from config import config
        
        emotion_core = get_emotion_core(config)
        
        # 导入情绪类型
        from emotional_ai_core import EmotionType
        
        # 测试不同的触发条件
        test_scenarios = [
            ("用户长时间未互动", lambda: emotion_core.add_emotion(EmotionType.LONELY, 0.7)),
            ("用户在看视频", lambda: emotion_core.add_emotion(EmotionType.CURIOUS, 0.6)),
            ("检测到人脸", lambda: emotion_core.add_emotion(EmotionType.EXCITED, 0.8)),
            ("发现有趣内容", lambda: emotion_core.add_emotion(EmotionType.HAPPY, 0.7))
        ]
        
        triggered_behaviors = 0
        for scenario, trigger_func in test_scenarios:
            try:
                # 模拟触发条件
                trigger_func()
                
                # 检查是否应该探索
                if emotion_core.should_explore():
                    action = emotion_core.choose_exploration_action()
                    triggered_behaviors += 1
                    print(f"   {scenario} → 触发行为: {action}")
                
            except Exception as e:
                print(f"   {scenario} → 错误: {e}")
        
        if triggered_behaviors > 0:
            print(f"✅ 主动行为触发器正常，触发了{triggered_behaviors}个行为")
            return True
        else:
            print(f"⚠️ 主动行为触发器未触发任何行为")
            return False
            
    except Exception as e:
        print(f"❌ 主动行为测试异常: {e}")
        return False

async def test_interaction_suggestions():
    """测试互动建议系统"""
    print("💬 测试互动建议系统...")
    try:
        # 测试各种分析器的互动建议
        suggestions_count = 0
        
        # 屏幕分析建议
        try:
            from enhanced_screen_analyzer import enhanced_screen_analyzer
            result = await enhanced_screen_analyzer.analyze_screen_content()
            suggestions = result.get('interaction_suggestion', [])
            if suggestions:
                suggestions_count += len(suggestions)
                print(f"   屏幕分析建议: {len(suggestions)}条")
        except:
            pass
        
        # 摄像头分析建议
        try:
            from enhanced_camera_analyzer import enhanced_camera_analyzer
            result = await enhanced_camera_analyzer.analyze_camera_content()
            suggestions = result.get('interaction_suggestion', [])
            if suggestions:
                suggestions_count += len(suggestions)
                print(f"   摄像头分析建议: {len(suggestions)}条")
        except:
            pass
        
        # 文件阅读建议
        try:
            from proactive_file_reader import proactive_file_reader
            result = await proactive_file_reader.discover_and_read_files()
            suggestions = result.get('suggestions', [])
            if suggestions:
                suggestions_count += len(suggestions)
                print(f"   文件阅读建议: {len(suggestions)}条")
        except:
            pass
        
        if suggestions_count > 0:
            print(f"✅ 互动建议系统正常，生成了{suggestions_count}条建议")
            return True
        else:
            print(f"⚠️ 互动建议系统未生成建议")
            return False
            
    except Exception as e:
        print(f"❌ 互动建议测试异常: {e}")
        return False

async def main():
    """主测试函数"""
    print("🚀 StarryNight AGENT 增强AI功能测试")
    print("=" * 60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("情绪核心集成", test_emotional_core_integration),
        ("主动行为触发器", test_proactive_behavior_triggers),
        ("增强屏幕分析", test_enhanced_screen_analysis),
        ("增强摄像头分析", test_enhanced_camera_analysis),
        ("主动文件阅读", test_proactive_file_reading),
        ("主动网络浏览", test_proactive_web_browsing),
        ("互动建议系统", test_interaction_suggestions),
    ]
    
    results = []
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}测试...")
        try:
            result = await asyncio.wait_for(test_func(), timeout=30)
            results.append((test_name, result))
            if result:
                passed += 1
        except asyncio.TimeoutError:
            print(f"⏰ {test_name}测试超时")
            results.append((test_name, False))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 增强AI功能测试结果:")
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("🎉 所有增强功能测试通过！")
        print("💡 新增功能:")
        print("   • 🖥️ 深度屏幕内容分析和用户行为推断")
        print("   • 📷 增强摄像头人物和行为识别")
        print("   • 📁 主动文件发现、阅读和分析")
        print("   • 🌐 智能网络浏览和内容分享")
        print("   • 🤖 丰富的主动互动触发条件")
        print("   • 💬 智能化的互动建议系统")
        print("   • 🎭 基于情绪状态的行为选择")
    elif passed >= len(results) * 0.7:
        print("⚠️ 大部分增强功能正常工作")
        print("💡 建议检查失败的功能模块")
    else:
        print("❌ 多项增强功能存在问题")
        print("🔧 需要进一步调试和修复")
    
    print("\n🌟 StarryNight现在拥有更强大的感知和互动能力！")
    
    return passed >= len(results) * 0.7

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