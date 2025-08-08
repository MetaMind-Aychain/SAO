#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPU优化模块 - 将CPU密集型计算迁移到GPU
"""

import logging
import numpy as np
from typing import Optional, Tuple, List, Dict, Any
import cv2

logger = logging.getLogger(__name__)

# 检查GPU可用性
GPU_AVAILABLE = False
CUPY_AVAILABLE = False
TORCH_GPU_AVAILABLE = False

try:
    import cupy as cp
    import cupyx.scipy.ndimage as cupy_ndimage
    CUPY_AVAILABLE = True
    logger.info("✅ CuPy已可用，启用GPU加速的图像处理")
except ImportError:
    logger.debug("CuPy不可用，将使用CPU进行图像处理")

try:
    import torch
    if torch.cuda.is_available():
        TORCH_GPU_AVAILABLE = True
        GPU_DEVICE = torch.device("cuda")
        logger.info(f"✅ PyTorch GPU已可用，设备: {torch.cuda.get_device_name()}")
    else:
        GPU_DEVICE = torch.device("cpu")
        logger.debug("PyTorch GPU不可用，将使用CPU")
except ImportError:
    logger.debug("PyTorch不可用")

GPU_AVAILABLE = CUPY_AVAILABLE or TORCH_GPU_AVAILABLE

class GPUImageProcessor:
    """GPU加速的图像处理器"""
    
    def __init__(self):
        self.use_gpu = GPU_AVAILABLE
        self.device = "cuda" if self.use_gpu else "cpu"
        logger.info(f"🎯 GPU图像处理器初始化 - 设备: {self.device}")
    
    def detect_motion_gpu(self, prev_frame: np.ndarray, curr_frame: np.ndarray, threshold: float = 30.0) -> Tuple[float, np.ndarray]:
        """GPU加速的运动检测"""
        try:
            if CUPY_AVAILABLE:
                return self._detect_motion_cupy(prev_frame, curr_frame, threshold)
            elif TORCH_GPU_AVAILABLE:
                return self._detect_motion_torch(prev_frame, curr_frame, threshold)
            else:
                return self._detect_motion_cpu(prev_frame, curr_frame, threshold)
        except Exception as e:
            logger.error(f"GPU运动检测失败，回退到CPU: {e}")
            return self._detect_motion_cpu(prev_frame, curr_frame, threshold)
    
    def _detect_motion_cupy(self, prev_frame: np.ndarray, curr_frame: np.ndarray, threshold: float) -> Tuple[float, np.ndarray]:
        """使用CuPy进行GPU运动检测"""
        # 转换为GPU数组
        prev_gpu = cp.asarray(prev_frame)
        curr_gpu = cp.asarray(curr_frame)
        
        # 转换为灰度
        if len(prev_gpu.shape) == 3:
            prev_gray = cp.mean(prev_gpu, axis=2).astype(cp.uint8)
            curr_gray = cp.mean(curr_gpu, axis=2).astype(cp.uint8)
        else:
            prev_gray = prev_gpu
            curr_gray = curr_gpu
        
        # 计算差异
        diff = cp.abs(curr_gray.astype(cp.float32) - prev_gray.astype(cp.float32))
        
        # 应用阈值
        motion_mask = diff > threshold
        
        # 计算运动强度
        motion_pixels = cp.sum(motion_mask)
        total_pixels = diff.size
        motion_ratio = float(motion_pixels / total_pixels)
        
        # 转回CPU用于返回
        motion_mask_cpu = cp.asnumpy(motion_mask).astype(np.uint8) * 255
        
        return motion_ratio, motion_mask_cpu
    
    def _detect_motion_torch(self, prev_frame: np.ndarray, curr_frame: np.ndarray, threshold: float) -> Tuple[float, np.ndarray]:
        """使用PyTorch进行GPU运动检测"""
        # 转换为PyTorch张量并移到GPU
        prev_tensor = torch.from_numpy(prev_frame).float().to(GPU_DEVICE)
        curr_tensor = torch.from_numpy(curr_frame).float().to(GPU_DEVICE)
        
        # 转换为灰度
        if len(prev_tensor.shape) == 3:
            prev_gray = torch.mean(prev_tensor, dim=2)
            curr_gray = torch.mean(curr_tensor, dim=2)
        else:
            prev_gray = prev_tensor
            curr_gray = curr_tensor
        
        # 计算差异
        diff = torch.abs(curr_gray - prev_gray)
        
        # 应用阈值
        motion_mask = diff > threshold
        
        # 计算运动强度
        motion_pixels = torch.sum(motion_mask)
        total_pixels = diff.numel()
        motion_ratio = float(motion_pixels / total_pixels)
        
        # 转回CPU
        motion_mask_cpu = motion_mask.cpu().numpy().astype(np.uint8) * 255
        
        return motion_ratio, motion_mask_cpu
    
    def _detect_motion_cpu(self, prev_frame: np.ndarray, curr_frame: np.ndarray, threshold: float) -> Tuple[float, np.ndarray]:
        """CPU运动检测（后备方案）"""
        # 转换为灰度
        if len(prev_frame.shape) == 3:
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        else:
            prev_gray = prev_frame
            curr_gray = curr_frame
        
        # 计算差异
        diff = cv2.absdiff(prev_gray, curr_gray)
        
        # 应用阈值
        _, motion_mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        
        # 计算运动强度
        motion_pixels = np.sum(motion_mask > 0)
        total_pixels = motion_mask.size
        motion_ratio = motion_pixels / total_pixels
        
        return motion_ratio, motion_mask
    
    def enhance_frame_gpu(self, frame: np.ndarray) -> np.ndarray:
        """GPU加速的帧增强"""
        try:
            if CUPY_AVAILABLE:
                return self._enhance_frame_cupy(frame)
            elif TORCH_GPU_AVAILABLE:
                return self._enhance_frame_torch(frame)
            else:
                return self._enhance_frame_cpu(frame)
        except Exception as e:
            logger.error(f"GPU帧增强失败，回退到CPU: {e}")
            return self._enhance_frame_cpu(frame)
    
    def _enhance_frame_cupy(self, frame: np.ndarray) -> np.ndarray:
        """使用CuPy进行GPU帧增强"""
        frame_gpu = cp.asarray(frame)
        
        # 对比度增强
        enhanced = cp.clip(frame_gpu * 1.2 + 10, 0, 255).astype(cp.uint8)
        
        # 高斯模糊降噪
        if len(enhanced.shape) == 3:
            for i in range(enhanced.shape[2]):
                enhanced[:, :, i] = cupy_ndimage.gaussian_filter(enhanced[:, :, i], sigma=0.5)
        else:
            enhanced = cupy_ndimage.gaussian_filter(enhanced, sigma=0.5)
        
        return cp.asnumpy(enhanced)
    
    def _enhance_frame_torch(self, frame: np.ndarray) -> np.ndarray:
        """使用PyTorch进行GPU帧增强"""
        frame_tensor = torch.from_numpy(frame).float().to(GPU_DEVICE)
        
        # 对比度增强
        enhanced = torch.clamp(frame_tensor * 1.2 + 10, 0, 255)
        
        # 简单降噪（移动平均）
        kernel = torch.ones(3, 3, device=GPU_DEVICE) / 9
        if len(enhanced.shape) == 3:
            enhanced = enhanced.permute(2, 0, 1)  # HWC -> CHW
            enhanced = torch.nn.functional.conv2d(enhanced.unsqueeze(0), kernel.unsqueeze(0).unsqueeze(0), padding=1)
            enhanced = enhanced.squeeze(0).permute(1, 2, 0)  # CHW -> HWC
        
        return enhanced.cpu().numpy().astype(np.uint8)
    
    def _enhance_frame_cpu(self, frame: np.ndarray) -> np.ndarray:
        """CPU帧增强（后备方案）"""
        # 对比度增强
        enhanced = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)
        
        # 高斯模糊降噪
        enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0.5)
        
        return enhanced

class GPUFaceDetector:
    """GPU加速的人脸检测器"""
    
    def __init__(self):
        self.use_gpu = TORCH_GPU_AVAILABLE
        self.device = GPU_DEVICE if self.use_gpu else "cpu"
        self.face_model = None
        self._init_face_detector()
    
    def _init_face_detector(self):
        """初始化人脸检测器"""
        try:
            if TORCH_GPU_AVAILABLE:
                # 尝试加载GPU加速的人脸检测模型
                import torchvision.transforms as transforms
                self.transform = transforms.Compose([
                    transforms.ToPILImage(),
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                ])
                logger.info("✅ GPU人脸检测器已初始化")
            else:
                logger.info("使用CPU人脸检测器")
        except Exception as e:
            logger.error(f"GPU人脸检测器初始化失败: {e}")
            self.use_gpu = False
    
    def detect_faces_gpu(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """GPU加速的人脸检测"""
        try:
            if self.use_gpu and TORCH_GPU_AVAILABLE:
                return self._detect_faces_torch(frame)
            else:
                return self._detect_faces_opencv(frame)
        except Exception as e:
            logger.error(f"GPU人脸检测失败，回退到OpenCV: {e}")
            return self._detect_faces_opencv(frame)
    
    def _detect_faces_torch(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """使用PyTorch进行GPU人脸检测"""
        # 这里可以集成更先进的GPU人脸检测模型
        # 为了简化，暂时使用OpenCV，但在GPU上进行预处理
        
        # GPU预处理
        frame_tensor = torch.from_numpy(frame).to(GPU_DEVICE)
        
        # 转换为灰度（在GPU上）
        if len(frame_tensor.shape) == 3:
            gray_tensor = torch.mean(frame_tensor.float(), dim=2).cpu().numpy().astype(np.uint8)
        else:
            gray_tensor = frame_tensor.cpu().numpy()
        
        # 使用OpenCV进行实际检测（这部分可以用专门的GPU模型替换）
        return self._detect_faces_opencv_gray(gray_tensor)
    
    def _detect_faces_opencv(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """使用OpenCV进行人脸检测"""
        try:
            # 加载人脸检测器
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # 转换为灰度
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame
            
            # 检测人脸
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # 格式化结果
            face_results = []
            for (x, y, w, h) in faces:
                face_results.append({
                    'bbox': [int(x), int(y), int(w), int(h)],
                    'confidence': 0.8,  # OpenCV不提供置信度
                    'center': [int(x + w/2), int(y + h/2)]
                })
            
            return face_results
            
        except Exception as e:
            logger.error(f"OpenCV人脸检测失败: {e}")
            return []
    
    def _detect_faces_opencv_gray(self, gray: np.ndarray) -> List[Dict[str, Any]]:
        """在已有灰度图上进行人脸检测"""
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            face_results = []
            for (x, y, w, h) in faces:
                face_results.append({
                    'bbox': [int(x), int(y), int(w), int(h)],
                    'confidence': 0.8,
                    'center': [int(x + w/2), int(y + h/2)]
                })
            
            return face_results
            
        except Exception as e:
            logger.error(f"灰度图人脸检测失败: {e}")
            return []

class GPUTextProcessor:
    """GPU加速的文本处理器"""
    
    def __init__(self):
        self.use_gpu = TORCH_GPU_AVAILABLE
        self.device = GPU_DEVICE if self.use_gpu else "cpu"
        self.embedder = None
        self._init_embedder()
    
    def _init_embedder(self):
        """初始化嵌入模型"""
        try:
            if TORCH_GPU_AVAILABLE:
                from sentence_transformers import SentenceTransformer
                self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device=self.device)
                logger.info(f"✅ GPU文本嵌入器已初始化 - 设备: {self.device}")
            else:
                logger.info("使用CPU文本处理器")
        except Exception as e:
            logger.error(f"GPU文本处理器初始化失败: {e}")
            self.use_gpu = False
    
    def get_text_embeddings_gpu(self, texts: List[str]) -> np.ndarray:
        """GPU加速的文本嵌入"""
        try:
            if self.use_gpu and self.embedder:
                embeddings = self.embedder.encode(texts, device=self.device, show_progress_bar=False)
                return embeddings
            else:
                # CPU后备方案
                return self._get_text_embeddings_cpu(texts)
        except Exception as e:
            logger.error(f"GPU文本嵌入失败，回退到CPU: {e}")
            return self._get_text_embeddings_cpu(texts)
    
    def _get_text_embeddings_cpu(self, texts: List[str]) -> np.ndarray:
        """CPU文本嵌入（后备方案）"""
        try:
            from sentence_transformers import SentenceTransformer
            embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device='cpu')
            return embedder.encode(texts, show_progress_bar=False)
        except Exception as e:
            logger.error(f"CPU文本嵌入也失败: {e}")
            # 返回随机嵌入作为最后的后备
            return np.random.random((len(texts), 384)).astype(np.float32)

# 全局GPU处理器实例
gpu_image_processor = GPUImageProcessor()
gpu_face_detector = GPUFaceDetector()
gpu_text_processor = GPUTextProcessor()

def get_gpu_status() -> Dict[str, Any]:
    """获取GPU状态信息"""
    status = {
        "gpu_available": GPU_AVAILABLE,
        "cupy_available": CUPY_AVAILABLE,
        "torch_gpu_available": TORCH_GPU_AVAILABLE,
        "device_info": {}
    }
    
    if TORCH_GPU_AVAILABLE:
        try:
            status["device_info"] = {
                "device_name": torch.cuda.get_device_name(),
                "device_count": torch.cuda.device_count(),
                "current_device": torch.cuda.current_device(),
                "memory_allocated": torch.cuda.memory_allocated() / 1024**3,  # GB
                "memory_reserved": torch.cuda.memory_reserved() / 1024**3,   # GB
            }
        except Exception as e:
            status["device_info"]["error"] = str(e)
    
    return status

def optimize_with_gpu():
    """输出GPU优化建议"""
    status = get_gpu_status()
    
    if not GPU_AVAILABLE:
        logger.warning("🔧 GPU优化建议:")
        logger.warning("  1. 安装CUDA和cuDNN以启用GPU加速")
        logger.warning("  2. 安装PyTorch GPU版本: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121")
        logger.warning("  3. 可选安装CuPy: pip install cupy-cuda12x")
        logger.warning("  4. 重启应用以应用GPU优化")
    else:
        logger.info("✅ GPU优化已启用!")
        if TORCH_GPU_AVAILABLE:
            info = status["device_info"]
            logger.info(f"  🎯 GPU设备: {info.get('device_name', 'Unknown')}")
            logger.info(f"  💾 显存使用: {info.get('memory_allocated', 0):.2f}GB / {info.get('memory_reserved', 0):.2f}GB")
        if CUPY_AVAILABLE:
            logger.info("  🚀 CuPy图像处理加速已启用")

# 导出主要接口
__all__ = [
    'gpu_image_processor',
    'gpu_face_detector', 
    'gpu_text_processor',
    'get_gpu_status',
    'optimize_with_gpu',
    'GPU_AVAILABLE'
]