#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库数据
"""

import sys
import os
sys.path.append('..')

# 直接创建数据库连接，避免导入其他模块
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# 数据库设置
DATABASE_URL = "sqlite:///./ai_website.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 模型定义
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

def check_database():
    db = SessionLocal()
    try:
        print("=== 数据库状态检查 ===")
        
        # 检查各表的数据量
        dynamics_count = db.query(AIDynamic).count()
        print(f"动态数量: {dynamics_count}")
        
        dev_updates_count = db.query(DeveloperUpdate).count()
        print(f"开发日志数量: {dev_updates_count}")
        
        users_count = db.query(User).count()
        print(f"用户数量: {users_count}")
        
        comments_count = db.query(Comment).count()
        print(f"评论数量: {comments_count}")
        
        likes_count = db.query(Like).count()
        print(f"点赞数量: {likes_count}")
        
        print("\n=== 最近的动态 ===")
        latest_dynamics = db.query(AIDynamic).order_by(AIDynamic.created_at.desc()).limit(5).all()
        for d in latest_dynamics:
            print(f"ID: {d.id}, 内容: {d.content[:50]}..., 时间: {d.created_at}")
        
        print("\n=== 最近的开发日志 ===")
        latest_updates = db.query(DeveloperUpdate).order_by(DeveloperUpdate.created_at.desc()).limit(3).all()
        for u in latest_updates:
            print(f"ID: {u.id}, 标题: {u.title}, 时间: {u.created_at}")
            
    except Exception as e:
        print(f"检查数据库时出错: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database()