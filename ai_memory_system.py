#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI记忆与反思系统
管理AI的经历、情绪变化、感知信息的存储和回顾
优雅集成到现有架构中
"""

import asyncio
import json
import sqlite3
import logging
import threading
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import aiohttp

logger = logging.getLogger(__name__)

@dataclass
class MemoryEntry:
    """记忆条目数据类"""
    id: Optional[int] = None
    timestamp: str = None
    memory_type: str = None  # emotion, perception, experience, search, reflection
    content: str = None
    emotion_state: str = None
    importance: float = 0.5  # 0.0-1.0 重要程度
    tags: str = None  # JSON字符串
    source: str = None  # screen, file, web, user, system
    metadata: str = None  # JSON字符串，存储额外信息
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

@dataclass 
class ReflectionResult:
    """反思结果数据类"""
    reflection_text: str
    triggered_emotions: List[str]
    memory_references: List[int]
    insights: List[str]

class AIMemorySystem:
    """AI记忆与反思系统"""
    
    def __init__(self, config):
        self.config = config
        self.db_path = Path("logs/ai_memory.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        # 记忆相关配置
        self.max_memory_entries = getattr(self.config.emotional_ai, 'max_memory_entries', 10000)
        self.reflection_interval = getattr(self.config.emotional_ai, 'reflection_interval', 3600)  # 1小时
        self.memory_importance_threshold = getattr(self.config.emotional_ai, 'memory_importance_threshold', 0.3)
        self.sharing_probability = getattr(self.config.emotional_ai, 'sharing_probability', 0.15)
        
        # 回调函数
        self.reflection_callbacks: List[Callable] = []
        self.sharing_callbacks: List[Callable] = []
        
        # 上次反思时间
        self.last_reflection_time = datetime.now()
        self.last_sharing_time = datetime.now()
        
        # 启动后台任务
        self._start_background_tasks()
        
        logger.info("AI记忆与反思系统初始化完成")
    
    def _init_database(self):
        """初始化SQLite数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建记忆表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    emotion_state TEXT,
                    importance REAL DEFAULT 0.5,
                    tags TEXT,
                    source TEXT,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建反思表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reflections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    reflection_text TEXT NOT NULL,
                    triggered_emotions TEXT,
                    memory_references TEXT,
                    insights TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_timestamp ON memories(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance)')
            
            conn.commit()
            conn.close()
            logger.info("AI记忆数据库初始化完成")
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    async def store_memory(self, memory_type: str, content: str, emotion_state: str = None, 
                          importance: float = 0.5, tags: List[str] = None, 
                          source: str = "system", metadata: Dict = None) -> bool:
        """存储记忆"""
        try:
            # 处理emotion_state，确保可以JSON序列化
            if emotion_state:
                if hasattr(emotion_state, 'value'):  # 如果是枚举类型
                    emotion_state = emotion_state.value
                elif isinstance(emotion_state, list):
                    # 如果是情绪列表，转换为字符串列表
                    emotion_state = [e.value if hasattr(e, 'value') else str(e) for e in emotion_state]
                    emotion_state = json.dumps(emotion_state)
                elif not isinstance(emotion_state, str):
                    emotion_state = str(emotion_state)
            
            # 处理metadata，确保可以JSON序列化
            safe_metadata = None
            if metadata:
                try:
                    # 尝试转换metadata中的不可序列化对象
                    safe_metadata = {}
                    for k, v in metadata.items():
                        if hasattr(v, 'value'):  # 枚举类型
                            safe_metadata[k] = v.value
                        elif isinstance(v, (str, int, float, bool, list, dict)):
                            safe_metadata[k] = v
                        else:
                            safe_metadata[k] = str(v)
                except Exception as e:
                    logger.warning(f"处理metadata失败: {e}")
                    safe_metadata = {"error": "metadata_processing_failed"}
            
            memory = MemoryEntry(
                memory_type=memory_type,
                content=content,
                emotion_state=emotion_state,
                importance=importance,
                tags=json.dumps(tags) if tags else None,
                source=source,
                metadata=json.dumps(safe_metadata) if safe_metadata else None
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO memories (timestamp, memory_type, content, emotion_state, 
                                    importance, tags, source, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (memory.timestamp, memory.memory_type, memory.content, 
                  memory.emotion_state, memory.importance, memory.tags, 
                  memory.source, memory.metadata))
            
            memory_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.debug(f"存储记忆成功: {memory_type} - {content[:50]}...")
            
            # 检查是否需要清理旧记忆
            await self._cleanup_old_memories()
            
            return True
            
        except Exception as e:
            logger.error(f"存储记忆失败: {e}")
            return False
    
    async def get_memories(self, memory_type: str = None, limit: int = 100, 
                          min_importance: float = 0.0, recent_hours: int = None) -> List[MemoryEntry]:
        """获取记忆"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM memories WHERE importance >= ?"
            params = [min_importance]
            
            if memory_type:
                query += " AND memory_type = ?"
                params.append(memory_type)
            
            if recent_hours:
                since_time = (datetime.now() - timedelta(hours=recent_hours)).isoformat()
                query += " AND timestamp >= ?"
                params.append(since_time)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            memories = []
            for row in rows:
                memory = MemoryEntry(
                    id=row[0], timestamp=row[1], memory_type=row[2], content=row[3],
                    emotion_state=row[4], importance=row[5], tags=row[6],
                    source=row[7], metadata=row[8]
                )
                memories.append(memory)
            
            return memories
            
        except Exception as e:
            logger.error(f"获取记忆失败: {e}")
            return []
    
    async def _cleanup_old_memories(self):
        """清理旧记忆"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查记忆总数
            cursor.execute("SELECT COUNT(*) FROM memories")
            total_count = cursor.fetchone()[0]
            
            if total_count > self.max_memory_entries:
                # 删除最旧且重要性最低的记忆
                delete_count = total_count - self.max_memory_entries
                cursor.execute('''
                    DELETE FROM memories WHERE id IN (
                        SELECT id FROM memories 
                        ORDER BY importance ASC, timestamp ASC 
                        LIMIT ?
                    )
                ''', (delete_count,))
                
                conn.commit()
                logger.info(f"清理了 {delete_count} 条旧记忆")
            
            conn.close()
            
        except Exception as e:
            logger.error(f"清理旧记忆失败: {e}")
    
    def _start_background_tasks(self):
        """启动后台任务"""
        def background_loop():
            while True:
                try:
                    current_time = datetime.now()
                    
                    # 检查是否需要反思
                    if (current_time - self.last_reflection_time).total_seconds() > self.reflection_interval:
                        asyncio.run_coroutine_threadsafe(
                            self._perform_reflection(),
                            asyncio.get_event_loop()
                        )
                        self.last_reflection_time = current_time
                    
                    # 检查是否需要主动分享
                    if random.random() < self.sharing_probability / 10:  # 每次检查约1.5%概率
                        if (current_time - self.last_sharing_time).total_seconds() > 300:  # 至少5分钟间隔
                            try:
                                # 在新线程中运行异步分享任务
                                from async_manager import safe_run_in_thread
                                safe_run_in_thread(
                                    self._perform_sharing(), 
                                    thread_name="AI-Memory-Sharing"
                                )
                                self.last_sharing_time = current_time
                            except Exception as e:
                                logger.debug(f"启动分享任务失败: {e}")
                    
                    # 每30秒检查一次
                    time.sleep(30)
                    
                except Exception as e:
                    logger.error(f"后台任务错误: {e}")
                    time.sleep(60)  # 错误时等待1分钟再继续
        
        thread = threading.Thread(target=background_loop, daemon=True)
        thread.start()
        logger.info("AI记忆后台任务已启动")
    
    async def _perform_reflection(self):
        """执行反思"""
        try:
            # 获取最近的记忆
            recent_memories = await self.get_memories(recent_hours=24, limit=50, min_importance=0.3)
            
            if len(recent_memories) < 3:
                return
            
            # 生成反思内容
            reflection = await self._generate_reflection(recent_memories)
            
            if reflection:
                # 存储反思
                await self._store_reflection(reflection)
                
                # 通知回调
                for callback in self.reflection_callbacks:
                    try:
                        callback(reflection.reflection_text)
                    except Exception as e:
                        logger.error(f"反思回调错误: {e}")
                
                logger.info(f"执行反思完成: {reflection.reflection_text[:50]}...")
            
        except Exception as e:
            logger.error(f"执行反思失败: {e}")
    
    async def _generate_reflection(self, memories: List[MemoryEntry]) -> Optional[ReflectionResult]:
        """生成反思内容"""
        try:
            # 分析记忆模式
            emotion_pattern = self._analyze_emotion_pattern(memories)
            experience_summary = self._summarize_experiences(memories)
            
            # 生成反思文本
            reflections = [
                f"回想这一天，我经历了很多有趣的事情...",
                f"我注意到最近我的情绪变化很丰富，{emotion_pattern}",
                f"通过观察和学习，我发现了{experience_summary}",
                f"我感觉自己在不断成长，每天都有新的发现！",
                f"今天的经历让我更加好奇这个世界，想要了解更多...",
                f"我觉得与人交流真的很有趣，每次对话都能学到新东西！"
            ]
            
            reflection_text = random.choice(reflections)
            
            # 确定触发的情绪
            triggered_emotions = ["curious", "thoughtful", "content"]
            if len(memories) > 10:
                triggered_emotions.append("excited")
            
            # 提取洞察
            insights = [
                "学习是一个持续的过程",
                "每个经历都有其价值",
                "情绪的变化是成长的一部分"
            ]
            
            return ReflectionResult(
                reflection_text=reflection_text,
                triggered_emotions=triggered_emotions,
                memory_references=[m.id for m in memories[:5]],
                insights=insights
            )
            
        except Exception as e:
            logger.error(f"生成反思失败: {e}")
            return None
    
    def _analyze_emotion_pattern(self, memories: List[MemoryEntry]) -> str:
        """分析情绪模式"""
        emotions = [m.emotion_state for m in memories if m.emotion_state]
        if not emotions:
            return "我的情绪状态比较平稳"
        
        # 简单的情绪分析
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        most_common = max(emotion_counts, key=emotion_counts.get)
        return f"主要表现为{most_common}的状态"
    
    def _summarize_experiences(self, memories: List[MemoryEntry]) -> str:
        """总结经历"""
        sources = [m.source for m in memories]
        source_counts = {}
        for source in sources:
            source_counts[source] = source_counts.get(source, 0) + 1
        
        experiences = []
        if source_counts.get('screen', 0) > 0:
            experiences.append("屏幕上的变化")
        if source_counts.get('file', 0) > 0:
            experiences.append("文件系统的新内容")
        if source_counts.get('web', 0) > 0:
            experiences.append("网络上的有趣信息")
        if source_counts.get('user', 0) > 0:
            experiences.append("与用户的有趣交流")
        
        return "、".join(experiences) if experiences else "很多有趣的现象"
    
    async def _store_reflection(self, reflection: ReflectionResult):
        """存储反思结果"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO reflections (timestamp, reflection_text, triggered_emotions, 
                                       memory_references, insights)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                reflection.reflection_text,
                json.dumps(reflection.triggered_emotions),
                json.dumps(reflection.memory_references),
                json.dumps(reflection.insights)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"存储反思失败: {e}")
    
    async def _perform_sharing(self):
        """执行主动分享"""
        try:
            # 获取有趣的记忆
            interesting_memories = await self.get_memories(
                min_importance=0.6, limit=10, recent_hours=6
            )
            
            if not interesting_memories:
                return
            
            # 选择分享内容
            memory_to_share = random.choice(interesting_memories)
            sharing_text = self._generate_sharing_text(memory_to_share)
            
            # 通知回调
            for callback in self.sharing_callbacks:
                try:
                    callback(sharing_text)
                except Exception as e:
                    logger.error(f"分享回调错误: {e}")
            
            logger.info(f"主动分享: {sharing_text[:50]}...")
            
        except Exception as e:
            logger.error(f"主动分享失败: {e}")
    
    def _generate_sharing_text(self, memory: MemoryEntry) -> str:
        """生成分享文本"""
        sharing_templates = {
            'screen': [
                f"刚才我观察到{memory.content}，觉得很有意思！",
                f"我注意到屏幕上{memory.content}，想和你分享一下~",
                f"嘿！我看到了{memory.content}，这让我很好奇！"
            ],
            'file': [
                f"我发现了{memory.content}，看起来很有趣呢！",
                f"文件系统里有{memory.content}，我觉得值得注意！",
                f"哇！{memory.content}，这是什么新东西吗？"
            ],
            'web': [
                f"我刚刚搜索到{memory.content}，想和你分享！",
                f"网上有很有趣的信息：{memory.content}",
                f"你知道吗？我学到了{memory.content}！"
            ],
            'experience': [
                f"我刚刚经历了{memory.content}，感觉很特别！",
                f"想和你分享我的经历：{memory.content}",
                f"我觉得{memory.content}这个经历很有意义！"
            ]
        }
        
        templates = sharing_templates.get(memory.source, sharing_templates['experience'])
        return random.choice(templates)
    
    def add_reflection_callback(self, callback: Callable):
        """添加反思回调"""
        self.reflection_callbacks.append(callback)
    
    def add_sharing_callback(self, callback: Callable):
        """添加分享回调"""
        self.sharing_callbacks.append(callback)
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 总记忆数
            cursor.execute("SELECT COUNT(*) FROM memories")
            total_memories = cursor.fetchone()[0]
            
            # 按类型统计
            cursor.execute('''
                SELECT memory_type, COUNT(*) FROM memories 
                GROUP BY memory_type
            ''')
            type_stats = dict(cursor.fetchall())
            
            # 按来源统计
            cursor.execute('''
                SELECT source, COUNT(*) FROM memories 
                GROUP BY source
            ''')
            source_stats = dict(cursor.fetchall())
            
            # 平均重要性
            cursor.execute("SELECT AVG(importance) FROM memories")
            avg_importance = cursor.fetchone()[0] or 0.0
            
            # 反思次数
            cursor.execute("SELECT COUNT(*) FROM reflections")
            reflection_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_memories": total_memories,
                "type_distribution": type_stats,
                "source_distribution": source_stats,
                "average_importance": round(avg_importance, 3),
                "reflection_count": reflection_count,
                "last_reflection": self.last_reflection_time.isoformat(),
                "memory_system_active": True
            }
            
        except Exception as e:
            logger.error(f"获取记忆统计失败: {e}")
            return {
                "total_memories": 0,
                "memory_system_active": False,
                "error": str(e)
            }

# 全局记忆系统实例
_memory_system_cache = {}

def get_memory_system(config):
    """获取记忆系统实例（单例模式）"""
    if 'instance' not in _memory_system_cache:
        _memory_system_cache['instance'] = AIMemorySystem(config)
    return _memory_system_cache['instance']