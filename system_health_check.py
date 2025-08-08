#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统健康检查脚本 - 验证所有组件是否就绪
"""

import sys
import importlib
import subprocess
from typing import Dict, List, Tuple

def check_module(module_name: str, display_name: str = None) -> Tuple[bool, str]:
    """检查单个模块"""
    display_name = display_name or module_name
    try:
        importlib.import_module(module_name)
        return True, f"✅ {display_name} - 已安装"
    except ImportError as e:
        return False, f"❌ {display_name} - 未安装 ({e})"

def check_gpu_support() -> Dict[str, any]:
    """检查GPU支持"""
    gpu_info = {
        "cuda_available": False,
        "cupy_available": False,
        "device_info": {}
    }
    
    try:
        import torch
        gpu_info["cuda_available"] = torch.cuda.is_available()
        if gpu_info["cuda_available"]:
            gpu_info["device_info"] = {
                "device_name": torch.cuda.get_device_name(),
                "device_count": torch.cuda.device_count(),
                "memory_allocated": f"{torch.cuda.memory_allocated() / 1024**3:.2f}GB",
                "memory_reserved": f"{torch.cuda.memory_reserved() / 1024**3:.2f}GB"
            }
    except Exception as e:
        gpu_info["torch_error"] = str(e)
    
    try:
        import cupy
        gpu_info["cupy_available"] = True
    except ImportError:
        gpu_info["cupy_available"] = False
    
    return gpu_info

def main():
    """主检查函数"""
    print("🔍 StarryNightAI系统 - 健康检查")
    print("=" * 60)
    
    # 核心依赖检查
    core_modules = [
        ("fastapi", "FastAPI Web框架"),
        ("uvicorn", "ASGI服务器"),
        ("sqlalchemy", "数据库ORM"),
        ("bcrypt", "密码加密"),
        ("jose", "JWT处理"),
        ("aiohttp", "异步HTTP客户端"),
        ("transformers", "Transformer模型"),
        ("sentence_transformers", "句子嵌入模型"),
        ("torch", "PyTorch深度学习"),
        ("opencv", "计算机视觉"),
        ("pygame", "音频播放"),
        ("PyQt5", "GUI框架"),
    ]
    
    print("\n📦 核心依赖检查:")
    all_core_good = True
    for module, name in core_modules:
        success, message = check_module(module, name)
        print(f"  {message}")
        if not success:
            all_core_good = False
    
    # 可选依赖检查
    optional_modules = [
        ("cupy", "CuPy GPU加速"),
        ("torchvision", "PyTorch视觉"),
        ("torchaudio", "PyTorch音频"),
        ("speechrecognition", "语音识别"),
        ("tweepy", "Twitter API"),
        ("py2neo", "Neo4j图数据库"),
        ("sounddevice", "音频设备"),
        ("playwright", "浏览器自动化"),
    ]
    
    print("\n🔧 可选依赖检查:")
    for module, name in optional_modules:
        success, message = check_module(module, name)
        print(f"  {message}")
    
    # GPU支持检查
    print("\n🎯 GPU支持检查:")
    gpu_info = check_gpu_support()
    
    if gpu_info["cuda_available"]:
        print("  ✅ CUDA GPU支持 - 已启用")
        device_info = gpu_info["device_info"]
        print(f"    📱 设备: {device_info.get('device_name', 'Unknown')}")
        print(f"    🔢 数量: {device_info.get('device_count', 0)}")
        print(f"    💾 显存: {device_info.get('memory_allocated', '0GB')} / {device_info.get('memory_reserved', '0GB')}")
    else:
        print("  ⚠️ CUDA GPU支持 - 未检测到或未启用")
    
    if gpu_info["cupy_available"]:
        print("  ✅ CuPy GPU加速 - 已安装")
    else:
        print("  ⚠️ CuPy GPU加速 - 未安装")
    
    # 配置文件检查
    print("\n📄 配置文件检查:")
    try:
        from config import config
        print("  ✅ config.json - 已加载")
        
        # 检查关键配置
        if config.api.api_key:
            print("  ✅ API密钥 - 已配置")
        else:
            print("  ⚠️ API密钥 - 未配置")
        
        if config.api_server.enabled:
            print("  ✅ API服务器 - 已启用")
        else:
            print("  ⚠️ API服务器 - 已禁用")
            
    except Exception as e:
        print(f"  ❌ 配置加载失败: {e}")
    
    # 总结
    print("\n" + "=" * 60)
    if all_core_good:
        print("🎉 系统检查完成!")
        print("\n📋 启动建议:")
        print("1. 运行主程序: python main.py")
        print("2. 运行完整系统: python start_complete_fixed_system.py")
        print("3. 访问AI网站: http://127.0.0.1:8080")
        
        if gpu_info["cuda_available"]:
            print("\n🚀 GPU加速已启用，推理性能将大幅提升!")
        else:
            print("\n💡 GPU优化建议:")
            print("- 安装NVIDIA GPU驱动和CUDA")
            print("- 重启应用以检测GPU")
    else:
        print("⚠️ 发现缺失依赖，请运行以下命令安装:")
        print("python install_all_dependencies.py")

if __name__ == "__main__":
    main()