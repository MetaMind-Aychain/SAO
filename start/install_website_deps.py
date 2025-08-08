#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装AI网站依赖
"""

import subprocess
import sys
import os

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🚀 安装StarryNightAI网站依赖...")
    
    # 网站依赖包
    packages = [
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0", 
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "python-jose[cryptography]>=3.3.0",
        "python-multipart>=0.0.6",
        "jinja2>=3.1.0",
        "bcrypt>=4.0.0",
        "websockets>=11.0.0"
    ]
    
    failed_packages = []
    
    for package in packages:
        print(f"📦 安装 {package}...")
        if install_package(package):
            print(f"✅ {package} 安装成功")
        else:
            print(f"❌ {package} 安装失败")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️ 以下包安装失败: {', '.join(failed_packages)}")
        print("请手动安装: pip install " + " ".join(failed_packages))
    else:
        print("\n🎉 所有依赖安装完成！")
        print("现在可以启动StarryNightAI网站了")

if __name__ == "__main__":
    main()