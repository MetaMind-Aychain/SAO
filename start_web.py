#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alice Synthesis AI Web界面启动器
启动本地web服务器来展示项目
"""

import os
import sys
import webbrowser
import http.server
import socketserver
import threading
import time
from pathlib import Path

def start_web_server(port=8080):
    """启动web服务器"""
    web_dir = Path(__file__).parent / "web"
    
    if not web_dir.exists():
        print("❌ web目录不存在！")
        return False
    
    os.chdir(web_dir)
    
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🚀 Alice Synthesis AI Web服务器启动成功！")
            print(f"📱 访问地址: http://localhost:{port}")
            print(f"📁 服务目录: {web_dir.absolute()}")
            print(f"⏹️  按 Ctrl+C 停止服务器")
            print("-" * 50)
            
            # 自动打开浏览器
            def open_browser():
                time.sleep(1)
                webbrowser.open(f"http://localhost:{port}")
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ 端口 {port} 已被占用，尝试使用端口 {port + 1}")
            return start_web_server(port + 1)
        else:
            print(f"❌ 启动服务器失败: {e}")
            return False
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
        return True

def main():
    """主函数"""
    print("=" * 60)
    print("🎮 Alice Synthesis AI - 刀剑神域数字世界")
    print("=" * 60)
    print("🌟 欢迎来到爱丽丝的AI世界！")
    print("💫 体验前所未有的数字世界陪伴体验")
    print("=" * 60)
    
    # 检查web文件
    web_files = ["index.html", "styles.css", "script.js"]
    web_dir = Path(__file__).parent / "web"
    
    missing_files = []
    for file in web_files:
        if not (web_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少以下文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有web文件检查完成")
    print()
    
    # 启动服务器
    try:
        start_web_server()
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

if __name__ == "__main__":
    main()


