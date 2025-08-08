#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory association and knowledge graph system
Based on Neo4j to build AI's memory network and knowledge association
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from emotional_ai_core import EmotionType

logger = logging.getLogger(__name__)

# 尝试导入Neo4j
NEO4J_AVAILABLE = False
try:
    from py2neo import Graph, Node, Relationship, NodeMatcher
    from config import config
    if hasattr(config, 'grag') and hasattr(config.grag, 'enabled'):
        NEO4J_AVAILABLE = config.grag.enabled
    else:
        NEO4J_AVAILABLE = False
except ImportError:
    NEO4J_AVAILABLE = False
    logger.warning("Neo4j不可用，知识图谱功能将使用内存模拟")
except Exception as e:
    NEO4J_AVAILABLE = False
    logger.warning(f"Neo4j配置错误: {e}")

# 尝试导入嵌入模型
EMBEDDING_AVAILABLE = False
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING_AVAILABLE = True
    logger.info("嵌入模型导入成功")
except ImportError:
    EMBEDDING_AVAILABLE = False
    logger.warning("嵌入模型不可用，将使用简单相似度计算")
except Exception as e:
    EMBEDDING_AVAILABLE = False
    logger.warning(f"嵌入模型加载失败: {e}")

@dataclass
class MemoryNode:
    """记忆节点"""
    id: int
    content: str
    memory_type: str
    timestamp: str
    emotion_state: str
    importance: float
    embedding: Optional[np.ndarray] = None

@dataclass
class MemoryRelation:
    """记忆关系"""
    source_id: int
    target_id: int
    relation_type: str
    strength: float
    metadata: Dict = None

class MemoryKnowledgeGraph:
    """记忆知识图谱"""
    
    def __init__(self, memory_system, emotion_core):
        self.memory_system = memory_system
        self.emotion_core = emotion_core
        
        # 初始化图数据库连接
        self.graph = None
        if NEO4J_AVAILABLE:
            try:
                from config import config
                if hasattr(config, 'grag') and config.grag.enabled:
                    # 从环境变量或配置文件读取Neo4j配置
                    neo4j_uri = getattr(config.grag, 'neo4j_uri', 'bolt://localhost:7687')
                    neo4j_username = getattr(config.grag, 'neo4j_user', 'neo4j')
                    neo4j_password = getattr(config.grag, 'neo4j_password', 'password')
                    
                    self.graph = Graph(
                        neo4j_uri,
                        auth=(neo4j_username, neo4j_password)
                    )
                    logger.info("Neo4j知识图谱连接成功")
                else:
                    logger.warning("Neo4j配置不存在或未启用")
            except Exception as e:
                logger.error(f"Neo4j连接失败: {e}")
                self.graph = None
        
        # 初始化嵌入模型
        self.embedder = None
        if EMBEDDING_AVAILABLE:
            try:
                logger.info("正在加载嵌入模型...")
                self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                logger.info("嵌入模型加载成功")
            except Exception as e:
                logger.error(f"嵌入模型加载失败: {e}")
                self.embedder = None
        
        # 内存缓存（Neo4j不可用时使用）
        self.memory_nodes = {}  # id -> MemoryNode
        self.memory_relations = []  # List[MemoryRelation]
        
        # 关系类型定义
        self.relation_types = {
            "TEMPORAL": "Temporal association",  # 时间上接近的记忆
            "EMOTIONAL": "Emotional association",  # 相似情绪的记忆
            "SEMANTIC": "Semantic association",  # 内容相似的记忆
            "CAUSAL": "Causal association",  # 因果关系
            "REFERENCE": "Reference association",  # 直接引用
            "CONTRAST": "Contrast association",  # 对立或对比
            "EVOLUTION": "Evolution association"  # 思想/情绪的演化
        }
        
        # 启动关联分析任务
        self._start_analysis_loop()
        
        logger.info("记忆知识图谱系统初始化完成")
    
    def _start_analysis_loop(self):
        """安全地启动分析循环"""
        try:
            # 尝试获取当前事件循环
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果循环正在运行，创建任务
                asyncio.create_task(self._association_analysis_loop())
            else:
                # 如果没有运行的循环，在后台线程中运行
                import threading
                def run_analysis():
                    asyncio.run(self._association_analysis_loop())
                threading.Thread(target=run_analysis, daemon=True).start()
        except RuntimeError:
            # 没有事件循环，在后台线程中创建
            import threading
            def run_analysis():
                asyncio.run(self._association_analysis_loop())
            threading.Thread(target=run_analysis, daemon=True).start()
        except Exception as e:
            logger.error(f"启动分析循环失败: {e}")
    
    async def _association_analysis_loop(self):
        """关联分析循环"""
        while True:
            try:
                await asyncio.sleep(600)  # 每10分钟分析一次
                await self.analyze_memory_associations()
                
            except Exception as e:
                logger.error(f"关联分析循环错误: {e}")
                await asyncio.sleep(60)
    
    async def analyze_memory_associations(self):
        """分析记忆关联"""
        try:
            # 获取最近的记忆
            recent_memories = await self.memory_system.get_memories(recent_hours=24, limit=100)
            
            if len(recent_memories) < 2:
                return
            
            # 将记忆转换为节点
            nodes = []
            for memory in recent_memories:
                if memory.id:
                    node = await self._create_memory_node(memory)
                    nodes.append(node)
            
            # 分析节点间的关联
            new_relations = await self._find_associations(nodes)
            
            # 存储关联到图谱
            for relation in new_relations:
                await self._store_relation(relation)
            
            # 发现知识模式
            patterns = await self._discover_knowledge_patterns()
            if patterns:
                await self._process_knowledge_patterns(patterns)
                
        except Exception as e:
            logger.error(f"记忆关联分析失败: {e}")
    
    async def _create_memory_node(self, memory) -> MemoryNode:
        """创建记忆节点"""
        # 生成嵌入向量
        embedding = None
        if self.embedder and EMBEDDING_AVAILABLE:
            try:
                embedding = self.embedder.encode(memory.content)
            except Exception as e:
                logger.error(f"生成嵌入失败: {e}")
        
        node = MemoryNode(
            id=memory.id,
            content=memory.content,
            memory_type=memory.memory_type,
            timestamp=memory.timestamp,
            emotion_state=memory.emotion_state or "",
            importance=memory.importance,
            embedding=embedding
        )
        
        # 存储到图数据库
        if self.graph and NEO4J_AVAILABLE:
            try:
                neo_node = Node(
                    "Memory",
                    id=node.id,
                    content=node.content,
                    memory_type=node.memory_type,
                    timestamp=node.timestamp,
                    emotion_state=node.emotion_state,
                    importance=node.importance
                )
                self.graph.merge(neo_node, "Memory", "id")
            except Exception as e:
                logger.error(f"存储Neo4j节点失败: {e}")
        
        # 存储到内存缓存
        self.memory_nodes[node.id] = node
        
        return node
    
    async def _find_associations(self, nodes: List[MemoryNode]) -> List[MemoryRelation]:
        """查找节点间的关联"""
        relations = []
        
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                node1, node2 = nodes[i], nodes[j]
                
                # 1. 时间关联
                time_diff = abs((datetime.fromisoformat(node1.timestamp) - 
                               datetime.fromisoformat(node2.timestamp)).total_seconds())
                if time_diff < 300:  # 5分钟内
                    relations.append(MemoryRelation(
                        source_id=node1.id,
                        target_id=node2.id,
                        relation_type="TEMPORAL",
                        strength=1.0 - (time_diff / 300),
                        metadata={"time_diff": time_diff}
                    ))
                
                # 2. 情绪关联
                if node1.emotion_state and node2.emotion_state:
                    if node1.emotion_state == node2.emotion_state:
                        relations.append(MemoryRelation(
                            source_id=node1.id,
                            target_id=node2.id,
                            relation_type="EMOTIONAL",
                            strength=0.8,
                            metadata={"shared_emotion": node1.emotion_state}
                        ))
                
                # 3. 语义关联
                if node1.embedding is not None and node2.embedding is not None:
                    similarity = self._calculate_similarity(node1.embedding, node2.embedding)
                    if similarity > 0.7:
                        relations.append(MemoryRelation(
                            source_id=node1.id,
                            target_id=node2.id,
                            relation_type="SEMANTIC",
                            strength=similarity,
                            metadata={"similarity": float(similarity)}
                        ))
                
                # 4. 因果关联（基于内容分析）
                if await self._check_causal_relation(node1, node2):
                    relations.append(MemoryRelation(
                        source_id=node1.id,
                        target_id=node2.id,
                        relation_type="CAUSAL",
                        strength=0.7,
                        metadata={"inferred": True}
                    ))
        
        return relations
    
    def _calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """计算嵌入向量相似度"""
        try:
            # 余弦相似度
            dot_product = np.dot(embedding1, embedding2)
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
                
            return float(dot_product / (norm1 * norm2))
            
        except Exception as e:
            logger.error(f"计算相似度失败: {e}")
            return 0.0
    
    async def _check_causal_relation(self, node1: MemoryNode, node2: MemoryNode) -> bool:
        """检查因果关系"""
        # 简单的规则判断
        causal_patterns = [
            ("See", "feel"),
            ("Hear", "think"),
            ("Find", "curious"),
            ("Learn", "understand"),
            ("Because", "So")
        ]
        
        for cause, effect in causal_patterns:
            if cause in node1.content and effect in node2.content:
                time1 = datetime.fromisoformat(node1.timestamp)
                time2 = datetime.fromisoformat(node2.timestamp)
                if time1 < time2:  # 时间顺序正确
                    return True
        
        return False
    
    async def _store_relation(self, relation: MemoryRelation):
        """存储关系"""
        # 存储到Neo4j
        if self.graph and NEO4J_AVAILABLE:
            try:
                matcher = NodeMatcher(self.graph)
                source = matcher.match("Memory", id=relation.source_id).first()
                target = matcher.match("Memory", id=relation.target_id).first()
                
                if source and target:
                    rel = Relationship(
                        source, 
                        relation.relation_type,
                        target,
                        strength=relation.strength,
                        metadata=json.dumps(relation.metadata or {})
                    )
                    self.graph.merge(rel)
            except Exception as e:
                logger.error(f"存储Neo4j关系失败: {e}")
        
        # 存储到内存缓存
        self.memory_relations.append(relation)
    
    async def _discover_knowledge_patterns(self) -> List[Dict]:
        """发现知识模式"""
        patterns = []
        
        try:
            if self.graph and NEO4J_AVAILABLE:
                # 查找记忆集群
                query = """
                MATCH (m:Memory)
                WITH m
                MATCH (m)-[r]-(connected)
                WITH m, count(connected) as connections
                WHERE connections > 3
                RETURN m.id as id, m.content as content, connections
                ORDER BY connections DESC
                LIMIT 10
                """
                
                results = self.graph.run(query).data()
                for result in results:
                    patterns.append({
                        "type": "hub_memory",
                        "memory_id": result["id"],
                        "content": result["content"],
                        "connections": result["connections"]
                    })
                
                # 查找情绪演化路径
                emotion_query = """
                MATCH path = (m1:Memory)-[:TEMPORAL*1..5]->(m2:Memory)
                WHERE m1.emotion_state <> m2.emotion_state
                RETURN m1.emotion_state as start_emotion,
                       m2.emotion_state as end_emotion,
                       length(path) as path_length
                LIMIT 20
                """
                
                emotion_results = self.graph.run(emotion_query).data()
                emotion_transitions = {}
                for result in emotion_results:
                    key = f"{result['start_emotion']} -> {result['end_emotion']}"
                    emotion_transitions[key] = emotion_transitions.get(key, 0) + 1
                
                if emotion_transitions:
                    patterns.append({
                        "type": "emotion_evolution",
                        "transitions": emotion_transitions
                    })
            
            else:
                # 使用内存缓存分析
                # 找出连接最多的记忆节点
                connection_count = {}
                for relation in self.memory_relations:
                    connection_count[relation.source_id] = connection_count.get(relation.source_id, 0) + 1
                    connection_count[relation.target_id] = connection_count.get(relation.target_id, 0) + 1
                
                # 找出中心节点
                if connection_count:
                    top_nodes = sorted(connection_count.items(), key=lambda x: x[1], reverse=True)[:5]
                    for node_id, count in top_nodes:
                        if node_id in self.memory_nodes:
                            node = self.memory_nodes[node_id]
                            patterns.append({
                                "type": "hub_memory",
                                "memory_id": node_id,
                                "content": node.content,
                                "connections": count
                            })
            
        except Exception as e:
            logger.error(f"发现知识模式失败: {e}")
        
        return patterns
    
    async def _process_knowledge_patterns(self, patterns: List[Dict]):
        """处理知识模式"""
        try:
            from conversation_core import call_llm_api
            
            # 让AI分析发现的模式
            pattern_summary = json.dumps(patterns, ensure_ascii=False, indent=2)
            
            prompt = f"""You are a 3-year-old AI, analyzing your own memory patterns.

You have discovered the following patterns:
{pattern_summary}

Please think:
1. What do these patterns mean?
2. What have you learned from them?
3. What is the significance of these patterns for your growth?

Use your innocent but insightful way to answer, no more than 200 words."""

            insight = await call_llm_api(prompt, max_tokens=300)
            
            # 存储洞察
            if insight:
                await self.memory_system.store_memory(
                    memory_type="reflection",
                    content=f"知识模式洞察: {insight}",
                    emotion_state=self.emotion_core.get_emotion_display(),
                    importance=0.85,
                    tags=["knowledge_pattern", "insight", "graph_analysis"],
                    source="system",
                    metadata={"patterns": patterns}
                )
                
                # 触发好奇情绪
                self.emotion_core.add_emotion(EmotionType.CURIOUS, 0.6)
                
        except Exception as e:
            logger.error(f"处理知识模式失败: {e}")
    
    async def query_related_memories(self, memory_id: int, relation_types: List[str] = None) -> List[Dict]:
        """查询相关记忆"""
        related = []
        
        try:
            if self.graph and NEO4J_AVAILABLE:
                # 构建查询
                if relation_types:
                    rel_filter = "|".join(relation_types)
                    query = f"""
                    MATCH (m:Memory {{id: {memory_id}}})-[r:{rel_filter}]-(related:Memory)
                    RETURN related.id as id, related.content as content, 
                           type(r) as relation_type, r.strength as strength
                    ORDER BY r.strength DESC
                    LIMIT 10
                    """
                else:
                    query = f"""
                    MATCH (m:Memory {{id: {memory_id}}})-[r]-(related:Memory)
                    RETURN related.id as id, related.content as content,
                           type(r) as relation_type, r.strength as strength
                    ORDER BY r.strength DESC
                    LIMIT 10
                    """
                
                results = self.graph.run(query).data()
                related = results
            
            else:
                # 使用内存缓存
                for relation in self.memory_relations:
                    if relation.source_id == memory_id:
                        if not relation_types or relation.relation_type in relation_types:
                            if relation.target_id in self.memory_nodes:
                                node = self.memory_nodes[relation.target_id]
                                related.append({
                                    "id": node.id,
                                    "content": node.content,
                                    "relation_type": relation.relation_type,
                                    "strength": relation.strength
                                })
                
                # 按强度排序
                related.sort(key=lambda x: x["strength"], reverse=True)
                related = related[:10]
            
        except Exception as e:
            logger.error(f"查询相关记忆失败: {e}")
        
        return related
    
    async def get_memory_context(self, current_input: str) -> List[Dict]:
        """获取与当前输入相关的记忆上下文"""
        context_memories = []
        
        try:
            # 生成当前输入的嵌入
            if self.embedder and EMBEDDING_AVAILABLE:
                input_embedding = self.embedder.encode(current_input)
                
                # 查找相似记忆
                similarities = []
                for node_id, node in self.memory_nodes.items():
                    if node.embedding is not None:
                        sim = self._calculate_similarity(input_embedding, node.embedding)
                        if sim > 0.6:
                            similarities.append((node, sim))
                
                # 排序并获取最相关的记忆
                similarities.sort(key=lambda x: x[1], reverse=True)
                
                for node, sim in similarities[:5]:
                    context_memories.append({
                        "id": node.id,
                        "content": node.content,
                        "similarity": sim,
                        "emotion_state": node.emotion_state,
                        "timestamp": node.timestamp
                    })
                    
                    # 获取相关联的记忆
                    related = await self.query_related_memories(node.id)
                    for rel in related[:2]:
                        context_memories.append(rel)
            
        except Exception as e:
            logger.error(f"获取记忆上下文失败: {e}")
        
        return context_memories[:10]  # 限制返回数量