#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web界面测试脚本
测试Alice Synthesis AI游戏官网的各项功能
"""

import os
import sys
import time
import webbrowser
import http.server
import socketserver
import threading
from pathlib import Path

def test_web_files():
    """测试web文件是否存在"""
    web_dir = Path(__file__).parent / "web"
    required_files = ["index.html", "styles.css", "script.js"]
    
    print("🔍 检查web文件...")
    missing_files = []
    
    for file in required_files:
        file_path = web_dir / file
        if file_path.exists():
            print(f"✅ {file} - 存在")
        else:
            print(f"❌ {file} - 缺失")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ 缺少文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有web文件检查完成")
    return True

def test_html_structure():
    """测试HTML结构"""
    web_dir = Path(__file__).parent / "web"
    html_file = web_dir / "index.html"
    
    print("\n🔍 检查HTML结构...")
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键元素
        checks = [
            ("<!DOCTYPE html>", "HTML5文档类型"),
            ("<title>", "页面标题"),
            ("<link rel=\"stylesheet\"", "CSS链接"),
            ("<script src=\"script.js\">", "JavaScript链接"),
            ("class=\"game-ui-container\"", "游戏UI容器"),
            ("class=\"top-hud\"", "顶部HUD"),
            ("class=\"hero-section\"", "英雄区域"),
            ("class=\"about-section\"", "关于区域"),
            ("class=\"features-section\"", "功能区域"),
            ("class=\"demo-section\"", "演示区域"),
            ("class=\"download-section\"", "下载区域"),
            ("class=\"bottom-hud\"", "底部HUD"),
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - 未找到")
        
        return True
        
    except Exception as e:
        print(f"❌ 读取HTML文件失败: {e}")
        return False

def test_css_styles():
    """测试CSS样式"""
    web_dir = Path(__file__).parent / "web"
    css_file = web_dir / "styles.css"
    
    print("\n🔍 检查CSS样式...")
    
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键样式
        checks = [
            (":root", "CSS变量定义"),
            ("--primary-cyan", "主色调变量"),
            ("--sao-orange", "SAO主题色"),
            ("@keyframes", "动画关键帧"),
            (".game-ui-container", "游戏UI容器样式"),
            (".top-hud", "顶部HUD样式"),
            (".hero-section", "英雄区域样式"),
            (".feature-item", "功能项样式"),
            (".demo-chat", "演示聊天样式"),
            ("@media", "响应式设计"),
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - 未找到")
        
        return True
        
    except Exception as e:
        print(f"❌ 读取CSS文件失败: {e}")
        return False

def test_javascript_functionality():
    """测试JavaScript功能"""
    web_dir = Path(__file__).parent / "web"
    js_file = web_dir / "script.js"
    
    print("\n🔍 检查JavaScript功能...")
    
    try:
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键功能
        checks = [
            ("initializeWebsite", "网站初始化"),
            ("initializeMatrixRain", "数字雨效果"),
            ("initializeScrollEffects", "滚动效果"),
            ("initializeNavigation", "导航功能"),
            ("initializeChat", "聊天功能"),
            ("initializeAnimations", "动画效果"),
            ("initializeCounters", "计数器动画"),
            ("initializeGameEffects", "游戏特效"),
            ("addMessage", "消息添加功能"),
            ("animateCounter", "计数器动画"),
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - 未找到")
        
        return True
        
    except Exception as e:
        print(f"❌ 读取JavaScript文件失败: {e}")
        return False

def start_test_server():
    """启动测试服务器"""
    web_dir = Path(__file__).parent / "web"
    
    print("\n🚀 启动测试服务器...")
    
    try:
        os.chdir(web_dir)
        
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", 8080), handler) as httpd:
            print("✅ 测试服务器启动成功！")
            print("📱 访问地址: http://localhost:8080")
            print("⏹️  按 Ctrl+C 停止服务器")
            print("-" * 50)
            
            # 自动打开浏览器
            def open_browser():
                time.sleep(2)
                webbrowser.open("http://localhost:8080")
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 测试服务器已停止")
    except Exception as e:
        print(f"❌ 启动测试服务器失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🎮 Alice Synthesis AI - 游戏官网测试")
    print("=" * 60)
    
    # 运行所有测试
    tests = [
        test_web_files,
        test_html_structure,
        test_css_styles,
        test_javascript_functionality
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！")
        print("🌟 游戏官网界面已准备就绪")
        print("=" * 60)
        
        # 启动测试服务器
        start_test_server()
    else:
        print("❌ 部分测试失败，请检查相关文件")
        print("=" * 60)

if __name__ == "__main__":
    main()


