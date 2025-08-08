# 🚀 StarryNightAI系统 - GPU推理加速设置指南

## 📋 概述

本指南帮助您为StarryNightAI系统启用GPU推理加速，大幅提升模型推理性能。

## ✅ 已完成的配置

### 1. 依赖包更新
- ✅ **requirements.txt** 已更新，包含所有必需依赖：
  - **Web网站相关**: `bcrypt`, `sqlalchemy`, `python-jose`, `Jinja2`
  - **GPU推理相关**: `torch`, `torchvision`, `torchaudio`, `cupy-cuda12x`
  - **异步处理**: `asyncio-mqtt`, `aiofiles`
  - **数据库**: `alembic` (数据库迁移)
  - **WebSocket**: `python-socketio`

### 2. GPU推理模块
- ✅ **gpu_inference_config.py** - 统一GPU推理管理
  - 自动设备检测 (CUDA/MPS/CPU)
  - 混合精度训练支持
  - 内存管理和优化
  - 模型编译加速
  - 性能基准测试

### 3. 修复的问题
- ✅ AI网站JWT导入问题 (`jwt` → `python-jose`)
- ✅ 缺失的 `bcrypt`, `sqlalchemy` 等依赖
- ✅ GPU推理相关依赖配置

### 4. 自动化脚本
- ✅ **install_all_dependencies.py** - 一键安装所有依赖
- ✅ **system_health_check.py** - 系统健康检查
- ✅ **start_complete_fixed_system.py** - 完整系统启动

## 🎯 GPU推理优化特性

### 自动设备检测
```python
from gpu_inference_config import get_gpu_manager

manager = get_gpu_manager()
print(f"当前设备: {manager.device}")
```

### 模型优化加载
```python
from gpu_inference_config import load_model_optimized
from transformers import AutoModel

# 自动GPU优化的模型加载
model = load_model_optimized(AutoModel, "model_name")
```

### 推理管道创建
```python
from gpu_inference_config import create_inference_pipeline

# 创建GPU加速的推理管道
pipe = create_inference_pipeline("text-classification", "model_name")
```

## 📦 安装步骤

### 1. 自动安装（推荐）
```bash
python install_all_dependencies.py
```

### 2. 手动安装
```bash
# 基础依赖
pip install -r requirements.txt

# GPU版本PyTorch (CUDA 12.1)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CuPy GPU加速
pip install cupy-cuda12x

# 可选加速库
pip install albumentations accelerate bitsandbytes
```

## 🔍 系统检查

运行健康检查验证安装：
```bash
python system_health_check.py
```

预期输出示例：
```
✅ FastAPI Web框架 - 已安装
✅ PyTorch深度学习 - 已安装
✅ CUDA GPU支持 - 已启用
  📱 设备: NVIDIA GeForce RTX 4080
  💾 显存: 0.12GB / 2.50GB
✅ CuPy GPU加速 - 已安装
```

## 🚀 启动系统

### 启动完整系统
```bash
python start_complete_fixed_system.py
```

这将启动：
- 🌐 AI网站 (http://127.0.0.1:8080)
- 🤖 自主交互系统
- 🖥️ 主程序界面

### 单独启动组件
```bash
# 仅主程序
python main.py

# 仅AI网站
cd ai_website && python app.py
```

## ⚡ GPU性能优化建议

### 1. 硬件要求
- **GPU**: NVIDIA GPU with CUDA 12.1+ 支持
- **显存**: 建议 6GB+ 用于中等模型
- **驱动**: 最新NVIDIA驱动程序

### 2. 软件配置
- **CUDA**: 确保安装CUDA 12.1+
- **cuDNN**: 与CUDA版本匹配的cuDNN
- **PyTorch**: GPU版本 (通过脚本自动安装)

### 3. 性能调优
- 使用混合精度训练 (`torch.float16`)
- 启用模型编译 (`torch.compile`)
- 批处理推理以提高吞吐量
- 监控GPU内存使用

## 🛠️ 故障排除

### GPU未被检测
1. **检查CUDA安装**:
   ```bash
   nvidia-smi
   nvcc --version
   ```

2. **重新安装PyTorch GPU版本**:
   ```bash
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

3. **验证PyTorch GPU支持**:
   ```python
   import torch
   print(torch.cuda.is_available())
   print(torch.cuda.get_device_name())
   ```

### 内存不足错误
1. **降低批处理大小**
2. **启用梯度检查点**
3. **使用模型量化** (8bit/4bit)
4. **清理GPU缓存**: `torch.cuda.empty_cache()`

### 依赖冲突
1. **创建虚拟环境**:
   ```bash
   python -m venv gpu_env
   gpu_env\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

## 📊 性能基准

启用GPU推理后，预期性能提升：
- **文本嵌入**: 3-5x 加速
- **图像处理**: 5-10x 加速
- **模型推理**: 2-8x 加速（取决于模型大小）

## 🔗 相关文件

- `requirements.txt` - 完整依赖列表
- `gpu_inference_config.py` - GPU配置模块
- `gpu_optimization.py` - 现有GPU优化功能
- `install_all_dependencies.py` - 自动安装脚本
- `system_health_check.py` - 系统检查脚本
- `start_complete_fixed_system.py` - 完整系统启动

## 📞 支持

如遇问题，请：
1. 运行 `python system_health_check.py` 检查系统状态
2. 检查错误日志
3. 确认GPU驱动和CUDA版本兼容性

---

**🎉 恭喜！您的StarryNightAI系统现已支持GPU加速推理！**