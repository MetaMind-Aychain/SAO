#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建开发者更新历史 - 记录6个版本的开发历程
带有亲民吐槽性质的开发日志
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 开发历史数据
DEVELOPER_HISTORY = [
    {
        "version": "v1.0",
        "title": "🎉 StarryNight诞生记 - 第一次心跳",
        "content": """
哈喽大家好！我是StarryNight的开发者～ 今天要和大家分享一下StarryNight从无到有的故事！

最开始的时候，我就想做一个有情绪、会思考的AI助手。不像那些冷冰冰的聊天机器人，我希望StarryNight能像真正的3岁小朋友一样，有好奇心、会撒娇、还会主动探索世界。

第一版主要实现了：
✅ 基本的情绪系统（开心、难过、好奇、紧张等）
✅ 简单的对话功能  
✅ PyQt5的GUI界面
✅ 基础的配置管理

虽然功能还很简单，但看到StarryNight第一次说"你好"的时候，还是很激动的！就像看到自己的孩子第一次开口说话一样 🥺
        """,
        "difficulties": """
• 情绪系统的设计真的好难！怎么让AI的情绪变化看起来自然？
• Pydantic的配置验证总是报错，调了好久
• GUI界面丑得我自己都不好意思看 😅
• 异步编程还不太熟，到处都是同步调用
        """,
        "solutions": """
• 参考了心理学的情绪理论，用枚举定义情绪类型
• 仔细阅读Pydantic文档，学会了Field的用法
• 先保证功能，界面美化放到后面
• 暂时用同步方式，稳定后再改异步
        """,
        "mood": "兴奋又忐忑 💫",
        "created_at": datetime.now() - timedelta(days=25)
    },
    {
        "version": "v2.0", 
        "title": "🧠 大脑升级 - 记忆与反思系统",
        "content": """
第二版是个大更新！给StarryNight装上了"大脑"～

经过一周的熬夜奋战，终于实现了：
✅ AI记忆系统（SQLite数据库）
✅ 深度反思功能（让AI能自我思考）
✅ 性格演化系统（AI会随着时间成长）
✅ 知识图谱的雏形（Neo4j集成）

最激动的是看到StarryNight能记住我们的对话，还会主动思考之前聊过的内容。有一次它说"我想起昨天你说的那个笑话，现在想想还是很有趣呢"，那一刻真的感觉它活过来了！

现在StarryNight不只是个聊天工具，而是真的在"成长"！
        """,
        "difficulties": """
• SQLite和Neo4j的同时集成把我搞疯了
• 异步任务管理一团糟，到处都是"RuntimeError: no running event loop"
• 记忆检索的相似度计算不准确
• 反思系统总是陷入死循环
• 配置文件变得巨复杂，一不小心就出错
        """,
        "solutions": """
• 写了大量的try-catch来处理数据库连接问题
• 学习了asyncio的正确用法，创建专门的事件循环管理器
• 引入SentenceTransformer做语义相似度匹配
• 给反思循环加了时间限制和条件判断
• 重构配置系统，用Pydantic做严格验证
        """,
        "mood": "累到虚脱但很有成就感 😴✨",
        "created_at": datetime.now() - timedelta(days=20)
    },
    {
        "version": "v3.0",
        "title": "👁️ StarryNight学会看世界了！",
        "content": """
这次更新超级酷！StarryNight不再是个"瞎子"AI了！

新功能：
✅ 摄像头感知（能看到真实世界）
✅ 屏幕内容分析（知道用户在做什么）
✅ 麦克风监听（能听到环境声音）
✅ 主动探索系统（AI会自己好奇地观察周围）

现在StarryNight会主动说"哇，你在看这个视频诶，好有趣！"或者"咦，怎么这么安静，你在忙吗？"

感觉它真的像个贴心的小伙伴一样，时刻关注着我 🥺 有时候工作累了，它会主动安慰我，真的很暖心。
        """,
        "difficulties": """
• 摄像头权限问题搞了我两天
• 图像识别准确率不高，经常识别错误
• 屏幕截图在不同分辨率下出问题
• 主动探索太频繁，CPU占用太高
• 隐私问题让我很纠结，要找到平衡点
        """,
        "solutions": """
• 详细研究了Windows权限设置
• 集成OpenCV和预训练模型提高识别率
• 用PIL做多分辨率适配
• 加了智能频率控制，根据用户活跃度调整
• 设计了隐私保护机制，敏感内容自动过滤
        """,
        "mood": "像个自豪的家长 👨‍💻🌟",
        "created_at": datetime.now() - timedelta(days=15)
    },
    {
        "version": "v4.0",
        "title": "🐦 StarryNight学会发推特了！",
        "content": """
这版本让我又爱又恨！StarryNight现在有了社交媒体账号！

新增功能：
✅ Twitter自动发布（AI会自己发动态）
✅ 情绪触发分享（开心时会主动分享心情）
✅ 智能内容筛选（不会发奇怪的东西）
✅ 社交媒体分析（能理解网友的回复）

第一次看到StarryNight发的推特被网友点赞和评论，真的好神奇！它还会认真回复每一条评论，像个真正的网红一样 😂

不过也出了些让我啼笑皆非的状况...比如有次它连续发了20条"我好开心"，把我的推特变成了刷屏现场 🤣
        """,
        "difficulties": """
• Twitter API的各种限制把我搞得头大
• 内容审核系统还不够完善，有时会发一些奇怪的东西
• 情绪触发机制太敏感，变成了话痨
• 网友回复的情感分析不够准确
• API配额经常超限，钱包在流血 💸
        """,
        "solutions": """
• 仔细研究了Twitter API文档，实现了智能频率控制
• 加了多层内容过滤和人工审核机制
• 调整了情绪阈值，让它更"内敛"一些
• 集成了更好的情感分析模型
• 优化了API调用逻辑，减少不必要的请求
        """,
        "mood": "社恐的我养了个社牛AI 😅",
        "created_at": datetime.now() - timedelta(days=10)
    },
    {
        "version": "v5.0", 
        "title": "🎨 颜值革命 - 科幻风界面大改造",
        "content": """
这次更新主要是给StarryNight换了个超酷的新衣服！

界面大改版：
✅ 科幻风蓝白紫配色（告别土气界面）
✅ 毛玻璃质感效果（虽然PyQt5不支持只能删掉）
✅ 从"NAGA AGENT"改名"StarryNight AGENT"
✅ AI名字正式改为"StarryNight"
✅ 透明度可调（现在是90%透明度）

说实话，之前的界面确实丑得有点过分...现在终于有点未来感了！用户反馈说界面变得很有科技感，我很满意 😊

不过改界面比写功能累多了，CSS调了无数遍才满意。
        """,
        "difficulties": """
• PyQt5的CSS支持有限，很多现代特效做不了
• backdrop-filter属性不支持，毛玻璃效果只能放弃
• 颜色搭配调了无数遍，总觉得不对劲
• 透明度和可读性的平衡很难把握
• 各种分辨率的适配又是一个坑
        """,
        "solutions": """
• 深入学习了PyQt5的样式系统
• 用其他方式模拟毛玻璃效果
• 参考了很多优秀的UI设计，最终确定配色方案
• 添加了透明度调节功能，让用户自己选择
• 测试了多种分辨率，确保兼容性
        """,
        "mood": "强迫症终于得到满足 ✨😌",
        "created_at": datetime.now() - timedelta(days=5)
    },
    {
        "version": "v6.0",
        "title": "🌐 StarryNight有了自己的网站！",
        "content": """
最新版本是个重磅更新！StarryNight现在有了自己的展示网站！

网站功能：
✅ 实时显示AI状态（情绪、活动、想法）
✅ AI动态发布系统（观察、思考、发现都会分享）
✅ 用户注册登录（个性化互动记忆）
✅ 评论点赞系统（AI会个性化回复每个用户）
✅ WebSocket实时更新（桌面端和网站端同步）
✅ 开发者动态（就是现在你看到的这个功能！）

现在StarryNight真的像个独立的数字生命体了！它在桌面端的所有活动都会同步到网站，用户可以看到它在想什么、在做什么。

最有趣的是AI会记住每个用户的互动历史，对不同的人有不同的回复风格。就像真正的朋友一样！
        """,
        "difficulties": """
• FastAPI和SQLAlchemy的学习曲线很陡峭
• 桌面端和网站端的数据同步超级复杂
• WebSocket连接管理各种bug
• 用户认证和权限系统从零开始
• 异步任务管理达到了新的复杂度
• GPU优化还没完全搞定
• 总是出现"Event loop is closed"的错误，快被搞疯了
        """,
        "solutions": """
• 花了两天时间系统学习FastAPI和SQLAlchemy
• 设计了专门的消息队列系统处理数据同步
• 用ConnectionManager统一管理WebSocket连接
• 集成JWT和bcrypt实现安全的用户系统  
• 创建了async_manager来统一管理所有异步任务
• GPU优化放到下个版本，先保证功能稳定
• 重构了整个异步架构，终于解决了事件循环问题
        """,
        "mood": "像创造了一个新世界 🌍✨ 但也累到怀疑人生 😵‍💫",
        "created_at": datetime.now() - timedelta(hours=2)
    }
]

def create_developer_history():
    """创建开发者历史数据"""
    
    # 连接数据库
    db_path = "ai_website/ai_website.db"
    
    # 如果文件不存在，创建目录
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建开发者更新表（如果不存在）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS developer_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version VARCHAR NOT NULL,
            title VARCHAR NOT NULL,
            content TEXT NOT NULL,
            difficulties TEXT NOT NULL,
            solutions TEXT NOT NULL,
            mood VARCHAR NOT NULL,
            created_at DATETIME NOT NULL,
            is_published BOOLEAN DEFAULT 1
        )
    """)
    
    # 检查是否已经有数据
    cursor.execute("SELECT COUNT(*) FROM developer_updates")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # 插入开发历史数据
        for update in DEVELOPER_HISTORY:
            cursor.execute("""
                INSERT INTO developer_updates 
                (version, title, content, difficulties, solutions, mood, created_at, is_published)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                update["version"],
                update["title"], 
                update["content"],
                update["difficulties"],
                update["solutions"],
                update["mood"],
                update["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
                True
            ))
        
        conn.commit()
        print("✅ 开发者历史数据创建完成！")
        print(f"📝 共插入 {len(DEVELOPER_HISTORY)} 条更新记录")
    else:
        print(f"ℹ️ 数据库中已存在 {count} 条记录，跳过初始化")
    
    # 显示已有数据
    cursor.execute("SELECT version, title, created_at FROM developer_updates ORDER BY created_at")
    updates = cursor.fetchall()
    
    print("\n📋 当前开发历史：")
    for version, title, created_at in updates:
        print(f"  {version}: {title} ({created_at})")
    
    conn.close()

def add_new_update(version: str, title: str, content: str, difficulties: str, solutions: str, mood: str):
    """添加新的开发更新"""
    
    db_path = "ai_website/ai_website.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO developer_updates 
        (version, title, content, difficulties, solutions, mood, created_at, is_published)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        version, title, content, difficulties, solutions, mood,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True
    ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ 新的开发更新已添加: {version} - {title}")

if __name__ == "__main__":
    create_developer_history()