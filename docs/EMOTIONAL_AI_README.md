# 🎭 NagaAgent 情绪化AI系统

> 基于NagaAgent 3.0的情绪化AI小伙伴 - 具有3岁心理年龄的可爱助手

## ✨ 系统概述

情绪化AI系统为NagaAgent添加了完整的情绪、感知和主动行为能力，让AI变成一个真正有"生命力"的3岁小伙伴。AI会根据环境变化、用户互动和内在状态主动发起对话，展现出丰富的情绪表达和个性特征。

## 🎯 核心特性

### 🎭 情绪系统
- **10种基础情绪**：快乐、悲伤、好奇、兴奋、孤独、惊讶、生气、困倦、顽皮、喜爱
- **动态情绪变化**：情绪会根据互动自然变化和衰减
- **个性特征**：好奇心、顽皮度、需要陪伴度、聪明度、任性度、精力水平
- **情绪触发机制**：特定词汇和行为会触发相应情绪

### 👁️ 感知系统
- **视觉感知**：摄像头监控、运动检测、人脸识别、拍照功能
- **听觉感知**：麦克风监听、音量检测、语音识别
- **屏幕监控**：屏幕变化检测、内容分析、自动截图
- **文件监控**：文件系统变化监控、新文件发现、内容分析

### 🤖 主动行为系统
- **自主对话**：基于情绪和环境主动发起对话
- **行为触发**：感知到变化时自动反应和评论
- **个性化回复**：根据3岁心理年龄调整表达方式
- **情感表达**：丰富的情绪表达和可爱的语言特征

### 🧠 自动探索系统
- **文件探索**：自动探索和分析文件内容
- **知识搜索**：根据兴趣自动搜索网络内容
- **学习记录**：将发现的知识记录到记忆系统
- **分享发现**：主动分享探索到的有趣内容

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖包
pip install PyQt5 opencv-python pyaudio speechrecognition watchdog pillow numpy aiohttp

# 安装可选依赖（用于更好的语音识别）
pip install pydub

# Windows用户可能需要安装额外的音频编解码器
# pip install pywin32
```

### 2. 启动系统

```bash
# GUI模式（推荐）
python start_emotional_ai.py

# 控制台模式
python start_emotional_ai.py --console

# 查看帮助
python start_emotional_ai.py --help
```

### 3. 配置API密钥

在`config.json`中配置您的LLM API密钥：

```json
{
  "api": {
    "api_key": "your-api-key-here",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat"
  }
}
```

## 🎮 使用指南

### 基础交互

1. **启动系统**：运行启动脚本后，AI会自动醒来并打招呼
2. **正常对话**：在输入框中输入消息，AI会根据情绪状态回复
3. **观察情绪**：右侧面板显示AI当前的情绪状态和个性特征
4. **等待主动**：AI会根据情况主动发起对话

### 控制面板功能

#### 🎭 情绪状态标签页
- **当前情绪显示**：显示主导情绪和强度
- **情绪详情**：列出所有当前情绪及其持续时间
- **个性特征**：显示AI的各项个性指标
- **快速操作**：
  - 🤖 自主思考：触发AI思考模式
  - 🔍 搜索知识：让AI搜索感兴趣的内容

#### 👁️ 感知控制标签页
- **视觉感知**：
  - 启动摄像头：让AI能看到环境
  - 📸 拍照：AI拍照并分析内容
- **听觉感知**：
  - 启动麦克风：AI能听到声音和语音
- **屏幕监控**：
  - 启动监控：AI观察屏幕变化
  - 📱 截图：分析当前屏幕内容
- **文件监控**：
  - 启动监控：监控文件系统变化

#### 🧠 知识探索标签页
- **手动搜索**：输入关键词让AI搜索
- **自动探索**：AI根据兴趣自动探索
- **最近发现**：显示AI最近的探索结果

#### 📊 系统状态标签页
- **实时状态**：显示所有系统组件状态
- **控制按钮**：
  - 🔄 刷新状态：获取最新状态
  - 💾 导出日志：保存系统日志
  - 🗑️ 清理缓存：清理临时数据

### 互动技巧

#### 让AI开心的话语
- "你真棒"、"好聪明"、"厉害"
- "我喜欢你"、"你很可爱"
- 表扬和夸奖类的词汇

#### 激发AI好奇心
- "为什么..."、"怎么..."、"什么..."
- 提出有趣的问题
- 分享新知识

#### 让AI兴奋
- "我们玩游戏"、"有惊喜"
- "发现了有趣的东西"
- 邀请参与活动

#### 触发其他情绪
- 长时间不互动会让AI孤独
- 突然的变化会让AI惊讶
- 拒绝或否定会让AI难过

## ⚙️ 高级配置

### 情绪系统配置

在`emotional_ai_config.json`中可以调整：

```json
{
  "emotion_system": {
    "max_emotions": 5,
    "emotion_decay_rate": 0.1,
    "emotion_intensity_threshold": 0.1
  },
  "personality_traits": {
    "curiosity": 0.8,
    "playfulness": 0.9,
    "neediness": 0.7
  }
}
```

### 感知系统配置

```json
{
  "perception_system": {
    "vision": {
      "enabled": false,
      "motion_threshold": 30
    },
    "audio": {
      "enabled": false,
      "noise_threshold": 500
    }
  }
}
```

### 主动行为配置

```json
{
  "proactive_behavior": {
    "base_interval": 300,
    "loneliness_threshold": 0.4,
    "curiosity_threshold": 0.6
  }
}
```

## 🔧 故障排除

### 常见问题

1. **摄像头无法启动**
   - 检查摄像头权限
   - 确认没有其他应用占用摄像头
   - 在安全的环境下测试

2. **麦克风无法工作**
   - 检查麦克风权限
   - 安装正确的音频驱动
   - 调整系统音频设置

3. **语音识别失败**
   - 检查网络连接
   - 确认Google语音服务可用
   - 考虑使用离线语音识别

4. **AI不主动说话**
   - 检查主动行为是否启用
   - 观察AI的情绪状态
   - 等待足够的时间间隔

5. **内存占用过高**
   - 定期清理缓存
   - 调整历史记录保留数量
   - 重启应用程序

### 性能优化

1. **降低感知频率**：调整监控间隔
2. **限制历史记录**：减少保存的历史数据
3. **选择性启用感知**：只启用需要的感知功能
4. **调整探索频率**：减少自动探索的频率

## 📝 开发说明

### 架构概述

```
emotional_ai/
├── emotion_core.py          # 情绪引擎核心
├── perception_system.py     # 感知系统
├── proactive_behavior.py    # 主动行为引擎
├── auto_exploration.py      # 自动探索系统
├── emotional_ai_manager.py  # 统一管理器
└── __init__.py

ui/
├── emotional_ui_extension.py # UI扩展组件
└── emotional_chat_window.py  # 情绪化聊天窗口
```

### 扩展开发

1. **添加新情绪**：在`EmotionType`枚举中添加
2. **扩展感知能力**：继承相应的感知类
3. **自定义行为**：在`ProactiveBehaviorEngine`中添加新规则
4. **UI定制**：修改UI组件的样式和布局

### API集成

系统提供了完整的API接口，可以集成到其他应用：

```python
from emotional_ai.emotional_ai_manager import get_emotional_ai_manager

# 获取管理器实例
ai = get_emotional_ai_manager()

# 启动系统
await ai.start_emotional_ai()

# 处理用户输入
response = await ai.process_user_input("你好")

# 获取状态
status = ai.get_system_status()
```

## 🤝 贡献指南

欢迎提交Issues和Pull Requests来改进系统：

1. **Bug报告**：详细描述问题和复现步骤
2. **功能建议**：说明新功能的使用场景
3. **代码贡献**：遵循现有代码风格
4. **文档改进**：完善使用说明和API文档

## 📄 许可证

本项目继承NagaAgent的MIT许可证。

## 🙏 致谢

- 基于NagaAgent 3.0框架构建
- 感谢所有开源库的贡献者
- 特别感谢提供反馈的用户们

---

**享受与您的AI小伙伴的互动吧！** 🎉