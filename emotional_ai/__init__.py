# emotional_ai/__init__.py
"""
情绪化AI系统 - 主模块
集成情绪、感知、主动行为和自动探索功能
"""

from .emotion_core import get_emotion_engine, EmotionEngine, EmotionType
from .perception_system import get_perception_manager, PerceptionManager, PerceptionEvent
from .proactive_behavior import get_proactive_engine, ProactiveBehaviorEngine, BehaviorType
from .auto_exploration import get_auto_exploration_engine, AutoExplorationEngine

__all__ = [
    'get_emotion_engine',
    'EmotionEngine', 
    'EmotionType',
    'get_perception_manager',
    'PerceptionManager',
    'PerceptionEvent',
    'get_proactive_engine',
    'ProactiveBehaviorEngine',
    'BehaviorType',
    'get_auto_exploration_engine',
    'AutoExplorationEngine'
]