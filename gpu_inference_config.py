#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPU推理配置模块 - 统一管理所有模型的GPU配置
"""

import logging
import torch
import os
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class GPUConfig:
    """GPU配置类"""
    device: str = "auto"  # "auto", "cpu", "cuda", "mps"
    mixed_precision: bool = True  # 混合精度训练
    memory_fraction: float = 0.8  # GPU显存使用比例
    cache_dir: str = "./models_cache"  # 模型缓存目录
    batch_size: int = 8  # 批处理大小
    max_length: int = 512  # 最大序列长度

class GPUInferenceManager:
    """GPU推理管理器"""
    
    def __init__(self, config: Optional[GPUConfig] = None):
        self.config = config or GPUConfig()
        self.device = self._detect_device()
        self.models_cache = {}
        
        # 设置GPU内存管理
        self._setup_gpu_memory()
        
        logger.info(f"🎯 GPU推理管理器初始化完成 - 设备: {self.device}")
    
    def _detect_device(self) -> str:
        """自动检测最佳设备"""
        if self.config.device != "auto":
            return self.config.device
        
        # 检查CUDA
        if torch.cuda.is_available():
            device = f"cuda:{torch.cuda.current_device()}"
            logger.info(f"✅ 检测到CUDA设备: {torch.cuda.get_device_name()}")
            return device
        
        # 检查Apple Silicon MPS
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            logger.info("✅ 检测到Apple MPS设备")
            return "mps"
        
        # 回退到CPU
        logger.info("⚠️ 未检测到GPU，使用CPU")
        return "cpu"
    
    def _setup_gpu_memory(self):
        """设置GPU内存管理"""
        if "cuda" in self.device:
            try:
                # 设置显存分配策略
                torch.cuda.set_per_process_memory_fraction(self.config.memory_fraction)
                torch.cuda.empty_cache()
                
                # 启用cudnn基准测试以优化性能
                torch.backends.cudnn.benchmark = True
                torch.backends.cudnn.deterministic = False
                
                logger.info(f"📊 GPU显存配置: {self.config.memory_fraction*100}%")
                
            except Exception as e:
                logger.warning(f"GPU内存配置失败: {e}")
    
    def get_model_device_map(self, model_name: str) -> Dict[str, Any]:
        """获取模型设备映射配置"""
        if "cuda" not in self.device:
            return {"": self.device}
        
        # 检查可用GPU数量
        gpu_count = torch.cuda.device_count()
        if gpu_count > 1:
            # 多GPU配置
            return {
                "transformer.word_embeddings": 0,
                "transformer.word_embeddings_layernorm": 0,
                "lm_head": "cpu",  # 将输出层放在CPU上节省显存
                "transformer.h": {i: i % gpu_count for i in range(24)}  # 假设24层
            }
        else:
            # 单GPU配置
            return {"": 0}
    
    def get_model_kwargs(self, model_name: str) -> Dict[str, Any]:
        """获取模型加载的关键字参数"""
        kwargs = {
            "cache_dir": self.config.cache_dir,
            "torch_dtype": torch.float16 if "cuda" in self.device else torch.float32,
            "device_map": self.get_model_device_map(model_name),
            "trust_remote_code": True,
        }
        
        # GPU特定配置
        if "cuda" in self.device:
            kwargs.update({
                "load_in_8bit": False,  # 可选：8位量化
                "load_in_4bit": False,  # 可选：4位量化
                "low_cpu_mem_usage": True,
                "use_cache": True,
            })
        
        return kwargs
    
    def optimize_model(self, model, model_name: str = "unknown"):
        """优化模型以提高推理速度"""
        try:
            # 移动模型到正确设备
            if hasattr(model, 'to'):
                model = model.to(self.device)
            
            # 设置评估模式
            if hasattr(model, 'eval'):
                model.eval()
            
            # 禁用梯度计算
            if hasattr(model, 'requires_grad_'):
                for param in model.parameters():
                    param.requires_grad_(False)
            
            # 编译模型（PyTorch 2.0+）
            if hasattr(torch, 'compile') and "cuda" in self.device:
                try:
                    model = torch.compile(model)
                    logger.info(f"✅ 模型 {model_name} 已编译优化")
                except Exception as e:
                    logger.debug(f"模型编译失败（正常，继续使用原模型）: {e}")
            
            logger.info(f"🚀 模型 {model_name} 已优化 - 设备: {self.device}")
            return model
            
        except Exception as e:
            logger.error(f"模型优化失败: {e}")
            return model
    
    def create_pipeline(self, task: str, model: str, **kwargs):
        """创建优化的推理管道"""
        try:
            from transformers import pipeline
            
            # 合并配置
            pipeline_kwargs = {
                "device": 0 if "cuda" in self.device else -1,
                "torch_dtype": torch.float16 if "cuda" in self.device else torch.float32,
                **kwargs
            }
            
            # 创建管道
            pipe = pipeline(
                task=task,
                model=model,
                **pipeline_kwargs
            )
            
            logger.info(f"✅ 创建 {task} 管道成功 - 模型: {model}")
            return pipe
            
        except Exception as e:
            logger.error(f"创建管道失败: {e}")
            raise
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取GPU内存使用统计"""
        stats = {"device": self.device}
        
        if "cuda" in self.device:
            try:
                stats.update({
                    "allocated_gb": torch.cuda.memory_allocated() / 1024**3,
                    "reserved_gb": torch.cuda.memory_reserved() / 1024**3,
                    "max_allocated_gb": torch.cuda.max_memory_allocated() / 1024**3,
                    "device_name": torch.cuda.get_device_name(),
                    "device_count": torch.cuda.device_count(),
                })
            except Exception as e:
                stats["error"] = str(e)
        
        return stats
    
    def clear_cache(self):
        """清理GPU缓存"""
        if "cuda" in self.device:
            torch.cuda.empty_cache()
            logger.info("🧹 GPU缓存已清理")
    
    def benchmark_model(self, model, input_data, iterations: int = 10):
        """对模型进行性能基准测试"""
        import time
        
        # 预热
        for _ in range(3):
            with torch.no_grad():
                _ = model(input_data)
        
        # 基准测试
        torch.cuda.synchronize() if "cuda" in self.device else None
        start_time = time.time()
        
        for _ in range(iterations):
            with torch.no_grad():
                _ = model(input_data)
        
        torch.cuda.synchronize() if "cuda" in self.device else None
        end_time = time.time()
        
        avg_time = (end_time - start_time) / iterations
        logger.info(f"📊 模型平均推理时间: {avg_time:.4f}秒")
        
        return avg_time

# 全局GPU推理管理器实例
gpu_manager = GPUInferenceManager()

def get_gpu_manager() -> GPUInferenceManager:
    """获取全局GPU管理器实例"""
    return gpu_manager

def configure_gpu_inference(device: str = "auto", memory_fraction: float = 0.8):
    """配置GPU推理设置"""
    global gpu_manager
    config = GPUConfig(device=device, memory_fraction=memory_fraction)
    gpu_manager = GPUInferenceManager(config)
    return gpu_manager

# 便捷函数
def load_model_optimized(model_class, model_name: str, **kwargs):
    """加载并优化模型"""
    manager = get_gpu_manager()
    
    # 合并配置
    model_kwargs = manager.get_model_kwargs(model_name)
    model_kwargs.update(kwargs)
    
    # 加载模型
    model = model_class.from_pretrained(model_name, **model_kwargs)
    
    # 优化模型
    model = manager.optimize_model(model, model_name)
    
    return model

def create_inference_pipeline(task: str, model_name: str, **kwargs):
    """创建推理管道"""
    manager = get_gpu_manager()
    return manager.create_pipeline(task, model_name, **kwargs)

# 导出主要接口
__all__ = [
    'GPUConfig',
    'GPUInferenceManager', 
    'gpu_manager',
    'get_gpu_manager',
    'configure_gpu_inference',
    'load_model_optimized',
    'create_inference_pipeline'
]