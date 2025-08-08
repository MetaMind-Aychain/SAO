# emotional_ai/auto_exploration.py
"""
AI自动探索系统
让AI主动探索文件、搜索知识、学习新内容
"""

import asyncio
import aiohttp
import json
import random
import time
import os
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
import logging
from urllib.parse import quote_plus
import mimetypes

from .emotion_core import get_emotion_engine, EmotionType
from config import config

logger = logging.getLogger(__name__)

class ExplorationTarget:
    """探索目标"""
    def __init__(self, target_type: str, content: str, priority: float = 0.5, context: Dict = None):
        self.target_type = target_type  # "file", "search", "url", "directory"
        self.content = content
        self.priority = priority
        self.context = context or {}
        self.timestamp = datetime.now()
        self.attempts = 0
        self.max_attempts = 3
    
    def __str__(self):
        return f"{self.target_type}:{self.content}"

class ExplorationResult:
    """探索结果"""
    def __init__(self, target: ExplorationTarget, success: bool, data: Any = None, error: str = None):
        self.target = target
        self.success = success
        self.data = data
        self.error = error
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_type": self.target.target_type,
            "target_content": self.target.content,
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp.isoformat()
        }

class FileExplorer:
    """文件探索器"""
    
    def __init__(self):
        self.explored_files: Set[str] = set()
        self.interesting_extensions = {
            '.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml',
            '.doc', '.docx', '.pdf', '.log', '.cfg', '.ini', '.yaml', '.yml'
        }
        self.max_file_size = 1024 * 1024  # 1MB
        
    async def explore_file(self, file_path: str) -> ExplorationResult:
        """探索单个文件"""
        target = ExplorationTarget("file", file_path)
        
        try:
            path = Path(file_path)
            if not path.exists():
                return ExplorationResult(target, False, error="文件不存在")
            
            if str(path.absolute()) in self.explored_files:
                return ExplorationResult(target, False, error="文件已探索过")
            
            if path.is_dir():
                return await self.explore_directory(file_path)
            
            # 检查文件大小
            file_size = path.stat().st_size
            if file_size > self.max_file_size:
                return ExplorationResult(target, False, error="文件过大")
            
            # 检查文件类型
            if path.suffix.lower() not in self.interesting_extensions:
                return ExplorationResult(target, False, error="文件类型不感兴趣")
            
            # 读取文件内容
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                self.explored_files.add(str(path.absolute()))
                
                # 分析文件内容
                analysis = self._analyze_file_content(content, path.suffix)
                
                return ExplorationResult(target, True, {
                    "file_type": path.suffix,
                    "file_size": file_size,
                    "content_preview": content[:500] + "..." if len(content) > 500 else content,
                    "analysis": analysis
                })
                
            except UnicodeDecodeError:
                return ExplorationResult(target, False, error="文件编码无法解析")
                
        except Exception as e:
            return ExplorationResult(target, False, error=str(e))
    
    async def explore_directory(self, dir_path: str) -> ExplorationResult:
        """探索目录"""
        target = ExplorationTarget("directory", dir_path)
        
        try:
            path = Path(dir_path)
            if not path.exists() or not path.is_dir():
                return ExplorationResult(target, False, error="目录不存在")
            
            files = []
            directories = []
            interesting_files = []
            
            for item in path.iterdir():
                if item.is_file():
                    files.append(item.name)
                    if item.suffix.lower() in self.interesting_extensions:
                        interesting_files.append(str(item))
                elif item.is_dir():
                    directories.append(item.name)
            
            return ExplorationResult(target, True, {
                "total_files": len(files),
                "total_directories": len(directories),
                "interesting_files": interesting_files[:10],  # 最多10个感兴趣的文件
                "file_types": list(set([Path(f).suffix for f in files if Path(f).suffix])),
                "sample_files": files[:10]  # 文件样本
            })
            
        except Exception as e:
            return ExplorationResult(target, False, error=str(e))
    
    def _analyze_file_content(self, content: str, file_ext: str) -> Dict[str, Any]:
        """分析文件内容"""
        analysis = {
            "line_count": len(content.split('\n')),
            "char_count": len(content),
            "word_count": len(content.split()),
        }
        
        # 基于文件类型的特殊分析
        if file_ext == '.py':
            analysis["python_imports"] = len([line for line in content.split('\n') if line.strip().startswith('import')])
            analysis["python_functions"] = len([line for line in content.split('\n') if 'def ' in line])
            analysis["python_classes"] = len([line for line in content.split('\n') if 'class ' in line])
        elif file_ext == '.js':
            analysis["js_functions"] = len([line for line in content.split('\n') if 'function' in line])
        elif file_ext in ['.md', '.txt']:
            analysis["heading_count"] = len([line for line in content.split('\n') if line.strip().startswith('#')])
        
        # 检查是否包含敏感信息
        sensitive_keywords = ['password', 'key', 'token', 'secret', 'api_key']
        analysis["contains_sensitive"] = any(keyword in content.lower() for keyword in sensitive_keywords)
        
        return analysis
    
    def get_exploration_suggestions(self) -> List[str]:
        """获取探索建议"""
        suggestions = []
        
        # 常见有趣目录
        common_dirs = [
            str(Path.home() / "Documents"),
            str(Path.home() / "Desktop"),
            str(Path.home() / "Downloads"),
            str(Path.cwd()),
            "/tmp" if os.name != 'nt' else str(Path.home() / "AppData" / "Local" / "Temp")
        ]
        
        for dir_path in common_dirs:
            if os.path.exists(dir_path):
                suggestions.append(dir_path)
        
        return suggestions

class WebSearcher:
    """网络搜索器"""
    
    def __init__(self):
        self.search_history: List[str] = []
        self.interesting_topics = [
            "人工智能", "机器学习", "编程", "科技新闻", "有趣的科学",
            "创意设计", "未来技术", "科学发现", "编程技巧", "开源项目"
        ]
        
    async def search_web(self, query: str) -> ExplorationResult:
        """搜索网络内容"""
        target = ExplorationTarget("search", query)
        
        try:
            # 这里可以集成真实的搜索API，比如Google、Bing等
            # 为了演示，我们模拟搜索结果
            await asyncio.sleep(1)  # 模拟网络延迟
            
            # 模拟搜索结果
            mock_results = [
                {
                    "title": f"关于'{query}'的详细介绍",
                    "url": f"https://example.com/search/{quote_plus(query)}",
                    "snippet": f"这是关于{query}的详细信息，包含了最新的研究和发现..."
                },
                {
                    "title": f"{query} - 维基百科",
                    "url": f"https://zh.wikipedia.org/wiki/{quote_plus(query)}",
                    "snippet": f"{query}是一个重要的概念，在多个领域都有应用..."
                },
                {
                    "title": f"{query}的实用指南",
                    "url": f"https://example.com/guide/{quote_plus(query)}",
                    "snippet": f"学习{query}的最佳方法和实践技巧..."
                }
            ]
            
            self.search_history.append(query)
            
            return ExplorationResult(target, True, {
                "query": query,
                "results": mock_results,
                "result_count": len(mock_results)
            })
            
        except Exception as e:
            return ExplorationResult(target, False, error=str(e))
    
    def get_search_suggestions(self) -> List[str]:
        """获取搜索建议"""
        # 基于当前时间、情绪等生成搜索建议
        emotion_engine = get_emotion_engine()
        dominant_emotion = emotion_engine.get_dominant_emotion()
        
        suggestions = []
        
        if dominant_emotion:
            if dominant_emotion.emotion == EmotionType.CURIOUS:
                suggestions.extend([
                    "最新科学发现", "如何工作的原理", "有趣的历史事件",
                    "未解之谜", "科技创新"
                ])
            elif dominant_emotion.emotion == EmotionType.HAPPY:
                suggestions.extend([
                    "有趣的事实", "可爱的动物", "励志故事",
                    "搞笑图片", "正能量新闻"
                ])
            elif dominant_emotion.emotion == EmotionType.EXCITED:
                suggestions.extend([
                    "最新游戏", "酷炫科技", "创意项目",
                    "极限运动", "惊人发明"
                ])
        
        # 添加一些随机主题
        suggestions.extend(random.sample(self.interesting_topics, min(3, len(self.interesting_topics))))
        
        return suggestions[:5]  # 返回最多5个建议

class AutoExplorationEngine:
    """自动探索引擎"""
    
    def __init__(self):
        self.emotion_engine = get_emotion_engine()
        self.file_explorer = FileExplorer()
        self.web_searcher = WebSearcher()
        
        self.is_active = False
        self.exploration_queue: List[ExplorationTarget] = []
        self.exploration_history: List[ExplorationResult] = []
        self.last_exploration_time = datetime.now()
        
        # 探索配置
        self.exploration_interval = 300  # 5分钟
        self.max_queue_size = 20
        self.max_history_size = 100
        
        # 回调函数
        self.exploration_callbacks: List = []
        
    def add_exploration_callback(self, callback):
        """添加探索回调"""
        self.exploration_callbacks.append(callback)
    
    async def start_auto_exploration(self):
        """启动自动探索"""
        if self.is_active:
            return
            
        self.is_active = True
        logger.info("自动探索系统启动")
        
        # 启动主循环
        asyncio.create_task(self._exploration_loop())
    
    def stop_auto_exploration(self):
        """停止自动探索"""
        self.is_active = False
        logger.info("自动探索系统停止")
    
    async def _exploration_loop(self):
        """探索主循环"""
        while self.is_active:
            try:
                # 检查是否应该进行探索
                if self._should_explore():
                    # 生成探索目标
                    targets = self._generate_exploration_targets()
                    for target in targets:
                        self._add_exploration_target(target)
                
                # 执行队列中的探索任务
                if self.exploration_queue:
                    target = self.exploration_queue.pop(0)
                    result = await self._execute_exploration(target)
                    self._handle_exploration_result(result)
                
                # 等待一段时间
                await asyncio.sleep(10)  # 每10秒检查一次
                
            except Exception as e:
                logger.error(f"探索循环错误: {e}")
                await asyncio.sleep(30)
    
    def _should_explore(self) -> bool:
        """判断是否应该进行探索"""
        current_time = datetime.now()
        time_since_last = (current_time - self.last_exploration_time).total_seconds()
        
        # 基本时间间隔检查
        if time_since_last < self.exploration_interval:
            return False
        
        # 基于情绪的探索倾向
        dominant_emotion = self.emotion_engine.get_dominant_emotion()
        if dominant_emotion:
            if dominant_emotion.emotion == EmotionType.CURIOUS and dominant_emotion.intensity > 0.6:
                return random.random() < 0.8
            elif dominant_emotion.emotion == EmotionType.EXCITED and dominant_emotion.intensity > 0.5:
                return random.random() < 0.6
            elif dominant_emotion.emotion == EmotionType.LONELY and dominant_emotion.intensity > 0.4:
                return random.random() < 0.4  # 孤独时可能想探索来转移注意力
        
        # 默认探索概率
        return random.random() < 0.3
    
    def _generate_exploration_targets(self) -> List[ExplorationTarget]:
        """生成探索目标"""
        targets = []
        
        # 文件探索目标
        file_suggestions = self.file_explorer.get_exploration_suggestions()
        if file_suggestions:
            target_path = random.choice(file_suggestions)
            targets.append(ExplorationTarget("directory", target_path, priority=0.6))
        
        # 搜索探索目标
        search_suggestions = self.web_searcher.get_search_suggestions()
        if search_suggestions:
            search_query = random.choice(search_suggestions)
            targets.append(ExplorationTarget("search", search_query, priority=0.7))
        
        return targets
    
    def _add_exploration_target(self, target: ExplorationTarget):
        """添加探索目标"""
        self.exploration_queue.append(target)
        
        # 按优先级排序
        self.exploration_queue.sort(key=lambda t: t.priority, reverse=True)
        
        # 限制队列大小
        if len(self.exploration_queue) > self.max_queue_size:
            self.exploration_queue = self.exploration_queue[:self.max_queue_size]
        
        logger.info(f"新增探索目标: {target}")
    
    async def _execute_exploration(self, target: ExplorationTarget) -> ExplorationResult:
        """执行探索"""
        self.last_exploration_time = datetime.now()
        target.attempts += 1
        
        try:
            if target.target_type == "file":
                return await self.file_explorer.explore_file(target.content)
            elif target.target_type == "directory":
                return await self.file_explorer.explore_directory(target.content)
            elif target.target_type == "search":
                return await self.web_searcher.search_web(target.content)
            else:
                return ExplorationResult(target, False, error="未知的探索类型")
                
        except Exception as e:
            return ExplorationResult(target, False, error=str(e))
    
    def _handle_exploration_result(self, result: ExplorationResult):
        """处理探索结果"""
        # 添加到历史记录
        self.exploration_history.append(result)
        
        # 限制历史记录大小
        if len(self.exploration_history) > self.max_history_size:
            self.exploration_history = self.exploration_history[-self.max_history_size:]
        
        # 基于结果触发情绪
        if result.success:
            # 成功探索触发好奇或兴奋
            if result.target.target_type == "search":
                self.emotion_engine.add_emotion(EmotionType.EXCITED, 0.5)
            else:
                self.emotion_engine.add_emotion(EmotionType.CURIOUS, 0.4)
            
            logger.info(f"探索成功: {result.target}")
        else:
            # 失败可能触发轻微的困惑（但不太影响情绪）
            logger.warning(f"探索失败: {result.target} - {result.error}")
            
            # 如果失败次数太多，重新加入队列（如果还有尝试次数）
            if result.target.attempts < result.target.max_attempts:
                self.exploration_queue.append(result.target)
        
        # 通知回调
        for callback in self.exploration_callbacks:
            try:
                callback(result)
            except Exception as e:
                logger.error(f"探索回调错误: {e}")
        
        # 更新探索满足度
        if hasattr(self.emotion_engine, 'exploration_satisfaction'):
            if result.success:
                self.emotion_engine.exploration_satisfaction = min(1.0, 
                    self.emotion_engine.exploration_satisfaction + 0.1)
            else:
                self.emotion_engine.exploration_satisfaction = max(0.0,
                    self.emotion_engine.exploration_satisfaction - 0.05)
    
    def manual_explore(self, target_type: str, content: str) -> bool:
        """手动触发探索"""
        try:
            target = ExplorationTarget(target_type, content, priority=0.9)
            self._add_exploration_target(target)
            return True
        except Exception as e:
            logger.error(f"手动探索失败: {e}")
            return False
    
    def get_exploration_status(self) -> Dict[str, Any]:
        """获取探索状态"""
        recent_results = self.exploration_history[-5:] if self.exploration_history else []
        
        return {
            "is_active": self.is_active,
            "queue_size": len(self.exploration_queue),
            "total_explorations": len(self.exploration_history),
            "last_exploration_time": self.last_exploration_time.isoformat(),
            "recent_results": [r.to_dict() for r in recent_results],
            "pending_targets": [str(t) for t in self.exploration_queue[:3]]
        }
    
    def get_exploration_summary(self) -> str:
        """获取探索摘要（用于AI分享）"""
        if not self.exploration_history:
            return "我还没有开始探索呢～"
        
        recent_results = self.exploration_history[-3:]
        successful_explorations = [r for r in recent_results if r.success]
        
        if not successful_explorations:
            return "最近的探索没有什么收获，不过我会继续努力的！"
        
        summary_parts = []
        for result in successful_explorations:
            if result.target.target_type == "search":
                summary_parts.append(f"搜索了'{result.target.content}'")
            elif result.target.target_type == "file":
                summary_parts.append(f"发现了文件'{result.target.content}'")
            elif result.target.target_type == "directory":
                summary_parts.append(f"探索了目录'{result.target.content}'")
        
        return f"我最近{', '.join(summary_parts)}，发现了很多有趣的东西！"

# 全局自动探索引擎实例
auto_exploration_engine = AutoExplorationEngine()

def get_auto_exploration_engine() -> AutoExplorationEngine:
    """获取全局自动探索引擎实例"""
    return auto_exploration_engine