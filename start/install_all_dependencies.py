#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键安装所有依赖的脚本
"""

import subprocess
import sys
import platform

def run_command(command, description=""):
    """执行命令并显示结果"""
    print(f"\n{'='*50}")
    if description:
        print(f"🔧 {description}")
    print(f"执行命令: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ 执行成功")
        if result.stdout:
            print("输出:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 执行失败: {e}")
        if e.stderr:
            print("错误:", e.stderr)
        return False

def install_basic_requirements():
    """安装基础依赖"""
    print("🚀 开始安装基础依赖...")
    
    # 升级pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "升级pip")
    
    # 安装基础依赖
    run_command(f"{sys.executable} -m pip install -r requirements.txt", "安装requirements.txt中的依赖")

def install_gpu_dependencies():
    """安装GPU相关依赖"""
    print("\n🎯 安装GPU推理加速依赖...")
    
    # 检查操作系统
    system = platform.system().lower()
    
    if "windows" in system or "linux" in system:
        # 安装GPU版本的PyTorch
        pytorch_cmd = f"{sys.executable} -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121"
        if run_command(pytorch_cmd, "安装GPU版本PyTorch（CUDA 12.1）"):
            print("✅ GPU版本PyTorch安装成功")
        else:
            print("⚠️ GPU版本PyTorch安装失败，将安装CPU版本")
            cpu_pytorch_cmd = f"{sys.executable} -m pip install torch torchvision torchaudio"
            run_command(cpu_pytorch_cmd, "安装CPU版本PyTorch")
    else:
        # macOS或其他系统
        run_command(f"{sys.executable} -m pip install torch torchvision torchaudio", "安装PyTorch（CPU版本）")

def install_optional_dependencies():
    """安装可选依赖"""
    print("\n🔧 安装可选依赖...")
    
    optional_packages = [
        "cupy-cuda12x",  # CuPy GPU加速
        "albumentations",  # 图像增强
        "accelerate",  # HuggingFace加速库
        "bitsandbytes",  # 量化支持
    ]
    
    for package in optional_packages:
        print(f"\n尝试安装 {package}...")
        success = run_command(f"{sys.executable} -m pip install {package}", f"安装{package}")
        if success:
            print(f"✅ {package} 安装成功")
        else:
            print(f"⚠️ {package} 安装失败（可能不兼容当前系统）")

def check_installation():
    """检查安装结果"""
    print("\n🔍 检查关键依赖安装情况...")
    
    critical_packages = [
        "fastapi", "uvicorn", "sqlalchemy", "bcrypt", 
        "jose", "torch", "transformers", "sentence_transformers"
    ]
    
    all_good = True
    for package in critical_packages:
        try:
            __import__(package)
            print(f"✅ {package} - 已安装")
        except ImportError:
            print(f"❌ {package} - 未安装")
            all_good = False
    
    return all_good

def main():
    """主函数"""
    print("🎊 StarryNightAI系统 - 依赖安装脚本")
    print("=" * 60)
    
    # 安装基础依赖
    install_basic_requirements()
    
    # 安装GPU依赖
    install_gpu_dependencies()
    
    # 安装可选依赖
    install_optional_dependencies()
    
    # 检查安装结果
    print("\n" + "=" * 60)
    if check_installation():
        print("🎉 所有关键依赖安装完成！")
        print("\n📋 后续步骤:")
        print("1. 配置config.json中的API密钥")
        print("2. 运行 python main.py 启动主程序")
        print("3. 运行 python start_complete_fixed_system.py 启动完整系统")
        print("\n💡 GPU优化提示:")
        print("- 如果有NVIDIA GPU，确保已安装CUDA驱动")
        print("- 重启程序以启用GPU加速")
    else:
        print("⚠️ 部分依赖安装失败，请检查错误信息")
        print("💡 建议:")
        print("1. 检查网络连接")
        print("2. 更新pip: python -m pip install --upgrade pip")
        print("3. 手动安装失败的包")

if __name__ == "__main__":
    main()