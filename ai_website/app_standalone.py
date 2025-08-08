#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StarryNightAI展示网站 - 独立运行版本
不依赖主AI系统，用于展示现有数据
"""

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import bcrypt
from jose import jwt, JWTError

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI应用初始化
app = FastAPI(
    title="StarryNightAI展示平台",
    description="展示AI的情绪、学习、探索和互动",
    version="1.0.0"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件和模板
STATIC_DIR = Path(__file__).parent / "static"
TEMPLATES_DIR = Path(__file__).parent / "templates"
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# 数据库设置
DATABASE_URL = "sqlite:///./ai_website.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT配置
SECRET_KEY = "StarryNight_agent_secret_key_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30天

# 数据库模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    avatar_url = Column(String, default="")

class AIDynamic(Base):
    __tablename__ = "ai_dynamics"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    emotion_type = Column(String)
    emotion_intensity = Column(Float)
    activity_type = Column(String)
    extra_data = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=True)

class DeveloperUpdate(Base):
    __tablename__ = "developer_updates"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String)
    title = Column(String)
    content = Column(Text)
    difficulties = Column(Text)
    solutions = Column(Text)
    mood = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=True)

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    dynamic_id = Column(Integer, ForeignKey("ai_dynamics.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    ai_replied = Column(Boolean, default=False)
    ai_reply = Column(Text, default="")
    ai_reply_at = Column(DateTime)
    is_ai_reply = Column(Boolean, default=False)
    user_emotion = Column(String, default="")
    sentiment_score = Column(Float, default=0.0)

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dynamic_id = Column(Integer, ForeignKey("ai_dynamics.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic模型
class DynamicResponse(BaseModel):
    id: int
    content: str
    emotion_type: str
    emotion_intensity: float
    activity_type: str
    created_at: datetime
    comments_count: int = 0
    likes_count: int = 0
    metadata: Dict[str, Any] = {}

class DeveloperUpdateResponse(BaseModel):
    id: int
    version: str
    title: str
    content: str
    difficulties: Optional[str] = None
    solutions: Optional[str] = None
    mood: str
    created_at: datetime

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 模拟AI状态（独立版本）
class MockAIStatus:
    def __init__(self):
        self.status = "online"
        self.current_emotion = "好奇"
        self.emotion_intensity = 0.7
        
    def get_status(self):
        return {
            "status": self.status,
            "name": "StarryNight",
            "age": "3岁",
            "personality": "好奇、活泼、善学的AI助手",
            "current_emotion": self.current_emotion,
            "emotion_intensity": self.emotion_intensity,
            "all_emotions": [
                {"type": "好奇", "intensity": 0.7},
                {"type": "快乐", "intensity": 0.6},
                {"type": "calm", "intensity": 0.5}
            ],
            "current_activity": "正在展示我的动态给大家看～",
            "memory_info": {
                "total_memories": 128,
                "recent_learning": "刚刚学习了web开发相关知识"
            },
            "uptime": "2小时15分钟",
            "capabilities": [
                "🎭 情绪感知与表达",
                "💭 记忆学习与反思", 
                "👁️ 视觉感知（摄像头）",
                "🎤 语音交互",
                "🌐 网络探索",
                "📝 文件读取学习",
                "🤖 自主互动"
            ],
            "last_activity": datetime.now().isoformat(),
            "version": "3.0",
            "mood_description": "对世界充满好奇，想要探索更多未知的事物"
        }

mock_ai = MockAIStatus()

# API路由
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    """主页"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/ai/status")
async def get_ai_status():
    """获取AI状态"""
    return mock_ai.get_status()

@app.get("/api/dynamics", response_model=List[DynamicResponse])
async def get_dynamics(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """获取AI动态列表"""
    dynamics = db.query(AIDynamic).filter(AIDynamic.is_published == True)\
                .order_by(AIDynamic.created_at.desc())\
                .offset(skip).limit(limit).all()
    
    result = []
    for dynamic in dynamics:
        comments_count = db.query(Comment).filter(Comment.dynamic_id == dynamic.id).count()
        likes_count = db.query(Like).filter(Like.dynamic_id == dynamic.id).count()
        
        extra_data = {}
        try:
            if dynamic.extra_data:
                extra_data = json.loads(dynamic.extra_data)
        except:
            pass
        
        result.append(DynamicResponse(
            id=dynamic.id,
            content=dynamic.content,
            emotion_type=dynamic.emotion_type,
            emotion_intensity=dynamic.emotion_intensity,
            activity_type=dynamic.activity_type,
            created_at=dynamic.created_at,
            comments_count=comments_count,
            likes_count=likes_count,
            metadata=extra_data
        ))
    
    return result

@app.get("/api/developer/updates", response_model=List[DeveloperUpdateResponse])
async def get_developer_updates(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """获取开发者更新日志"""
    updates = db.query(DeveloperUpdate).filter(DeveloperUpdate.is_published == True)\
                .order_by(DeveloperUpdate.created_at.desc())\
                .offset(skip).limit(limit).all()
    
    return [DeveloperUpdateResponse(
        id=update.id,
        version=update.version,
        title=update.title,
        content=update.content,
        difficulties=update.difficulties,
        solutions=update.solutions,
        mood=update.mood,
        created_at=update.created_at
    ) for update in updates]

@app.get("/api/stats")
async def get_ai_statistics(db: Session = Depends(get_db)):
    """获取AI活动统计数据"""
    try:
        # 动态统计
        total_dynamics = db.query(AIDynamic).count()
        published_dynamics = db.query(AIDynamic).filter(AIDynamic.is_published == True).count()
        
        # 最近7天的动态
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_dynamics = db.query(AIDynamic).filter(
            AIDynamic.created_at >= seven_days_ago
        ).count()
        
        # 评论统计
        total_comments = db.query(Comment).count()
        
        # 点赞统计  
        total_likes = db.query(Like).count()
        
        # 用户统计
        total_users = db.query(User).count()
        
        # 开发者更新统计
        developer_updates = db.query(DeveloperUpdate).count()
        
        # 最新活动时间
        latest_dynamic = db.query(AIDynamic)\
            .order_by(AIDynamic.created_at.desc())\
            .first()
        
        return {
            "overview": {
                "total_dynamics": total_dynamics,
                "published_dynamics": published_dynamics,
                "recent_dynamics": recent_dynamics,
                "total_comments": total_comments,
                "total_likes": total_likes,
                "total_users": total_users,
                "developer_updates": developer_updates
            },
            "ai_status": {
                "status": "online",
                "current_emotion": mock_ai.current_emotion,
                "last_activity": latest_dynamic.created_at.isoformat() if latest_dynamic else None
            },
            "engagement": {
                "avg_comments_per_dynamic": round(total_comments / max(published_dynamics, 1), 2),
                "avg_likes_per_dynamic": round(total_likes / max(published_dynamics, 1), 2),
                "user_engagement_rate": round((total_comments + total_likes) / max(total_users, 1), 2)
            }
        }
        
    except Exception as e:
        logger.error(f"获取统计数据失败: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🌟 启动StarryNightAI展示网站（独立版本）")
    print("📊 URL: http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)