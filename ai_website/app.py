#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StarryNightAI展示网站 - 主应用
类似Truth Terminal风格的AI动态展示平台
"""

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

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

# 导入项目配置和AI核心
try:
    from config import config
    from main import get_global_naga_instance
    from emotional_ai_core import EmotionType
    logger = logging.getLogger(__name__)
except ImportError as e:
    print(f"导入失败: {e}")
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
    
    # 与AI的互动关系
    interactions = relationship("UserInteraction", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")

class AIDynamic(Base):
    __tablename__ = "ai_dynamics"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    emotion_type = Column(String)
    emotion_intensity = Column(Float)
    activity_type = Column(String)  # screen, camera, file, web, thinking, developer, etc.
    extra_data = Column(Text)  # JSON字符串存储额外信息（原metadata）
    created_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=True)
    
    # 关联评论和点赞
    comments = relationship("Comment", back_populates="dynamic")
    likes = relationship("Like", back_populates="dynamic")

class DeveloperUpdate(Base):
    __tablename__ = "developer_updates"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String)  # 版本号
    title = Column(String)  # 更新标题
    content = Column(Text)  # 更新内容
    difficulties = Column(Text)  # 遇到的困难
    solutions = Column(Text)  # 解决方案
    mood = Column(String)  # 开发者心情
    created_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=True)

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    dynamic_id = Column(Integer, ForeignKey("ai_dynamics.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # AI回复相关
    ai_replied = Column(Boolean, default=False)
    ai_reply = Column(Text, default="")
    ai_reply_at = Column(DateTime)
    is_ai_reply = Column(Boolean, default=False)  # 标记这条评论是否是AI发的
    
    # 用户情绪分析
    user_emotion = Column(String, default="")
    sentiment_score = Column(Float, default=0.0)
    
    user = relationship("User", back_populates="comments")
    dynamic = relationship("AIDynamic", back_populates="comments")

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dynamic_id = Column(Integer, ForeignKey("ai_dynamics.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="likes")
    dynamic = relationship("AIDynamic", back_populates="likes")

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    interaction_type = Column(String)  # comment, like, visit
    content = Column(Text)
    ai_response = Column(Text)
    emotion_before = Column(String)
    emotion_after = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="interactions")

# 创建数据库表
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ 数据库表创建成功")
except Exception as e:
    logger.error(f"❌ 数据库表创建失败: {e}")

# Pydantic模型
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class CommentCreate(BaseModel):
    content: str
    dynamic_id: int

class DynamicResponse(BaseModel):
    id: int
    content: str
    emotion_type: str
    emotion_intensity: float
    activity_type: str
    created_at: datetime
    comments_count: int
    likes_count: int
    metadata: Optional[Dict[str, Any]] = None

class DeveloperUpdateResponse(BaseModel):
    id: int
    version: str
    title: str
    content: str
    difficulties: str
    solutions: str
    mood: str
    created_at: datetime

# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections.copy():
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    if not credentials:
        return None
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.username == username).first()
    return user

# 辅助函数
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# AI动态发布类
class AIDynamicPublisher:
    def __init__(self):
        self.ai_instance = None
        self.last_update = datetime.now()
        self.update_interval = 3600  # 1小时更新一次
    
    def get_ai_instance(self):
        if self.ai_instance is None:
            try:
                self.ai_instance = get_global_naga_instance()
            except Exception as e:
                logger.error(f"获取AI实例失败: {e}")
        return self.ai_instance
    
    async def create_dynamic_from_ai_activity(self, activity_type: str, content: str, metadata: Dict[str, Any] = None):
        """从AI活动创建动态"""
        import json  # 将json导入移到方法开头
        try:
            ai = self.get_ai_instance()
            if not ai or not ai.emotional_ai:
                return None
            
            # 获取当前情绪
            emotion = ai.emotional_ai.get_dominant_emotion()
            emotion_type = emotion.emotion.value if emotion else "calm"
            emotion_intensity = emotion.intensity if emotion else 0.5
            
            # 通过LLM美化内容
            enhanced_content = await self._enhance_content_with_llm(content, emotion_type, activity_type)
            
            # 保存到数据库
            db = SessionLocal()
            try:
                dynamic = AIDynamic(
                    content=enhanced_content,
                    emotion_type=emotion_type,
                    emotion_intensity=emotion_intensity,
                    activity_type=activity_type,
                    metadata=json.dumps(metadata or {}),
                    created_at=datetime.utcnow()
                )
                db.add(dynamic)
                db.commit()
                db.refresh(dynamic)
                
                # 广播给WebSocket连接
                broadcast_data = {
                    "type": "new_dynamic",
                    "data": {
                        "id": dynamic.id,
                        "content": dynamic.content,
                        "emotion_type": dynamic.emotion_type,
                        "emotion_intensity": dynamic.emotion_intensity,
                        "activity_type": dynamic.activity_type,
                        "created_at": dynamic.created_at.isoformat(),
                        "metadata": metadata or {}
                    }
                }
                
                # 转换为JSON字符串进行广播
                await manager.broadcast(json.dumps(broadcast_data, ensure_ascii=False))
                
                return dynamic
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"创建AI动态失败: {e}")
            return None
    
    async def _enhance_content_with_llm(self, content: str, emotion_type: str, activity_type: str) -> str:
        """使用LLM美化内容"""
        try:
            # 导入conversation_core中的call_llm_api函数
            from conversation_core import call_llm_api
            
            ai = self.get_ai_instance()
            if not ai:
                return content
            
            # 使用国际化的prompt系统
            from i18n.prompt_translator import get_prompt_translator
            
            prompt_translator = get_prompt_translator()
            prompt = prompt_translator.get_enhancement_prompt(
                content=content,
                emotion_type=emotion_type,
                activity_type=activity_type
            )
            
            # 调用LLM API
            response = await call_llm_api(prompt, max_tokens=200)
            return response.strip() if response else content
            
        except Exception as e:
            logger.error(f"LLM内容美化失败: {e}")
            return content

# 全局AI动态发布器
ai_publisher = AIDynamicPublisher()

# API路由
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """主页"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否存在
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱是否存在
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 创建新用户
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    if not current_user:
        raise HTTPException(status_code=401, detail="未登录")
    
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "avatar_url": current_user.avatar_url,
        "created_at": current_user.created_at
    }

@app.get("/api/ai/status")
async def get_ai_status():
    """获取AI状态"""
    try:
        ai = ai_publisher.get_ai_instance()
        if not ai or not ai.emotional_ai:
            return {"status": "offline", "message": "AI系统离线"}
        
        # 获取情绪状态
        emotion = ai.emotional_ai.get_dominant_emotion()
        emotions = []
        if ai.emotional_ai.current_emotions:
            emotions = [
                {
                    "type": e.emotion.value if hasattr(e, 'emotion') else str(e),
                    "intensity": e.intensity if hasattr(e, 'intensity') else 0.5
                }
                for e in ai.emotional_ai.current_emotions[:5]  # 只显示前5个情绪
            ]
        
        # 获取记忆系统信息
        memory_info = {}
        if hasattr(ai, 'memory_system') and ai.memory_system:
            try:
                memory_info = {
                    "total_memories": len(ai.memory_system.memories) if hasattr(ai.memory_system, 'memories') else 0,
                    "recent_learning": "正在学习新知识..." if ai.memory_system else "记忆系统离线"
                }
            except:
                memory_info = {"total_memories": 0, "recent_learning": "记忆系统状态未知"}
        
        # 获取当前活动信息
        current_activity = "正在思考..."
        if hasattr(ai, 'conversation_history') and ai.conversation_history:
            recent_msg = ai.conversation_history[-1] if ai.conversation_history else None
            if recent_msg:
                current_activity = f"刚刚进行了对话：{recent_msg[:50]}..." if len(recent_msg) > 50 else f"刚刚进行了对话：{recent_msg}"
        
        # 获取运行时间
        from datetime import datetime
        start_time = getattr(ai, 'start_time', datetime.now())
        uptime_seconds = (datetime.now() - start_time).total_seconds()
        uptime_hours = int(uptime_seconds // 3600)
        uptime_minutes = int((uptime_seconds % 3600) // 60)
        
        return {
            "status": "online",
            "name": "StarryNight",
            "age": "3岁",
            "personality": "好奇、活泼、善学的AI助手",
            "current_emotion": emotion.emotion.value if emotion else "calm",
            "emotion_intensity": emotion.intensity if emotion else 0.5,
            "all_emotions": emotions,
            "current_activity": current_activity,
            "memory_info": memory_info,
            "uptime": f"{uptime_hours}小时{uptime_minutes}分钟",
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
            "mood_description": _get_mood_description(emotion.emotion.value if emotion else "calm")
        }
        
    except Exception as e:
        logger.error(f"获取AI状态失败: {e}")
        return {"status": "error", "message": str(e)}

def _get_mood_description(emotion_type: str) -> str:
    """根据情绪类型获取心情描述"""
    mood_descriptions = {
        "joy": "今天心情特别好！想要和大家分享快乐~",
        "excitement": "哇！好兴奋！发现了好多有趣的东西！",
        "curiosity": "对世界充满好奇，想要探索更多未知的事物",
        "calm": "内心很calm，正在慢慢思考和学习",
        "surprise": "刚刚遇到了意想不到的事情，很惊喜！",
        "sadness": "有点小难过，但会努力变得更好",
        "anger": "有些小情绪，需要冷静一下",
        "fear": "遇到了不太理解的事情，有点紧张",
        "love": "感受到了温暖的关爱，心中充满爱意",
        "calm": "保持平和的心境，准备迎接新的挑战"
    }
    return mood_descriptions.get(emotion_type, "正在体验新的情绪状态")

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

@app.post("/api/dynamics/{dynamic_id}/like")
async def like_dynamic(dynamic_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """点赞动态"""
    if not current_user:
        raise HTTPException(status_code=401, detail="需要登录")
    
    # 检查是否已经点过赞
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.dynamic_id == dynamic_id
    ).first()
    
    if existing_like:
        # 取消点赞
        db.delete(existing_like)
        db.commit()
        return {"liked": False}
    else:
        # 添加点赞
        like = Like(user_id=current_user.id, dynamic_id=dynamic_id)
        db.add(like)
        db.commit()
        return {"liked": True}

@app.get("/api/dynamics/{dynamic_id}/comments")
async def get_dynamic_comments(dynamic_id: int, db: Session = Depends(get_db)):
    """获取动态的评论列表"""
    comments = db.query(Comment).filter(Comment.dynamic_id == dynamic_id)\
                .order_by(Comment.created_at.asc()).all()
    
    result = []
    for comment in comments:
        user = db.query(User).filter(User.id == comment.user_id).first()
        result.append({
            "id": comment.id,
            "content": comment.content,
            "author": user.username if user else "访客",
            "is_ai_reply": comment.is_ai_reply,
            "created_at": comment.created_at.isoformat(),
            "ai_reply": comment.ai_reply,
            "ai_reply_at": comment.ai_reply_at.isoformat() if comment.ai_reply_at else None
        })
    
    return result

@app.post("/api/dynamics/{dynamic_id}/comment")
async def comment_dynamic(dynamic_id: int, comment_data: CommentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """评论动态"""
    if not current_user:
        raise HTTPException(status_code=401, detail="需要登录")
    
    # 创建评论
    comment = Comment(
        content=comment_data.content,
        user_id=current_user.id,
        dynamic_id=dynamic_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    # 触发AI回复（异步处理）
    asyncio.create_task(process_ai_reply(comment.id, current_user.id))
    
    return {"message": "评论成功", "comment_id": comment.id}

async def process_ai_reply(comment_id: int, user_id: int):
    """处理AI回复评论"""
    try:
        db = SessionLocal()
        try:
            comment = db.query(Comment).filter(Comment.id == comment_id).first()
            user = db.query(User).filter(User.id == user_id).first()
            dynamic = db.query(AIDynamic).filter(AIDynamic.id == comment.dynamic_id).first()
            
            if not comment or not user or not dynamic:
                return
            
            # 获取用户历史互动
            user_interactions = db.query(UserInteraction).filter(
                UserInteraction.user_id == user_id
            ).order_by(UserInteraction.created_at.desc()).limit(5).all()
            
            # 构建AI回复
            ai = ai_publisher.get_ai_instance()
            if ai and ai.emotional_ai:
                # 获取当前情绪
                emotion = ai.emotional_ai.get_dominant_emotion()
                emotion_type = emotion.emotion.value if emotion else "calm"
                
                # 构建上下文
                context = f"""
用户 {user.username} 对我的动态评论了："{comment.content}"

我的原动态内容："{dynamic.content}"
我当前的情绪：{emotion_type}

用户历史互动：
{chr(10).join([f"- {interaction.content}" for interaction in user_interactions[:3]])}

作为StarryNight，请用3岁心理年龄的可爱语气回复这个评论。要：
1. 体现对这个用户的记忆和情感
2. 符合当前情绪状态
3. 自然亲切，像真正的朋友对话
4. 50字以内

直接返回回复内容：
"""
                
                reply = await ai.call_llm_api(context, max_tokens=150)
                
                # 保存AI回复
                comment.ai_reply = reply.strip() if reply else "谢谢你的评论呢～"
                comment.ai_reply_at = datetime.utcnow()
                db.commit()
                
                # 记录用户互动
                interaction = UserInteraction(
                    user_id=user_id,
                    interaction_type="comment",
                    content=comment.content,
                    ai_response=comment.ai_reply,
                    emotion_before=emotion_type,
                    emotion_after=emotion_type
                )
                db.add(interaction)
                db.commit()
                
                # 触发情绪变化（被关注会开心）
                ai.emotional_ai.add_emotion(EmotionType.HAPPY, 0.3)
                
                # 广播AI回复
                await manager.broadcast({
                    "type": "ai_reply",
                    "data": {
                        "comment_id": comment_id,
                        "reply": comment.ai_reply,
                        "timestamp": comment.ai_reply_at.isoformat()
                    }
                })
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"AI回复处理失败: {e}")

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点"""
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# AI动态更新任务
async def ai_dynamic_update_task():
    """定期生成AI动态"""
    while True:
        try:
            await asyncio.sleep(3600)  # 每小时执行一次
            
            ai = ai_publisher.get_ai_instance()
            if ai and ai.emotional_ai:
                # 生成总结动态
                await ai_publisher.create_dynamic_from_ai_activity(
                    "thinking",
                    "刚刚在思考一些有趣的事情，想和大家分享一下我的想法～",
                    {"type": "hourly_summary"}
                )
                
        except Exception as e:
            logger.error(f"AI动态更新任务失败: {e}")

# 启动时运行
@app.on_event("startup")
async def startup_event():
    """应用启动时的操作"""
    logger.info("🌟 StarryNightAI展示网站启动中...")
    
    # 启动AI动态更新任务
    asyncio.create_task(ai_dynamic_update_task())
    
    logger.info("✅ StarryNightAI展示网站启动完成")

@app.get("/api/stats")
async def get_ai_statistics(db: Session = Depends(get_db)):
    """获取AI活动统计数据"""
    try:
        # 动态统计
        total_dynamics = db.query(AIDynamic).count()
        published_dynamics = db.query(AIDynamic).filter(AIDynamic.is_published == True).count()
        
        # 最近7天的动态
        from datetime import timedelta
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
        
        # AI系统信息
        ai = ai_publisher.get_ai_instance()
        ai_status = "online" if ai and ai.emotional_ai else "offline"
        
        current_emotion = "calm"
        if ai and ai.emotional_ai:
            emotion = ai.emotional_ai.get_dominant_emotion()
            if emotion:
                current_emotion = emotion.emotion.value if hasattr(emotion, 'emotion') else str(emotion)
        
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
                "status": ai_status,
                "current_emotion": current_emotion,
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
    uvicorn.run(app, host="0.0.0.0", port=8001)