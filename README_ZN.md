# 🌟 NagaAgent - StarryNight AI Assistant

<div align="center">
  <img src="https://img.shields.io/badge/Version-3.0-brightgreen" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-blue" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/Language-中文%20|%20English-red" alt="Language">
</div>

<div align="center">
  <h3>🎭 情感化AI助手 | Emotional AI Assistant</h3>
  <p>一个拥有真实情感、主动行为能力的可爱AI助手</p>
  <p>A cute AI assistant with real emotions and proactive behavior capabilities</p>
</div>

> **Author**: StarryNight - Chinese HuanSen

---

## ✨ 核心特性

### 🧠 情感智能
- **多维情绪系统**: 8种基础情绪，具有强度和衰减机制
- **情绪驱动行为**: AI根据当前情绪状态调整回应和行为
- **情绪可视化**: 实时情绪显示，美观的UI主题
- **情绪记忆**: 记住情感体验，从互动中学习

### 👁️ 感知与观察
- **摄像头视觉**: 实时人脸检测和情绪识别
- **屏幕分析**: 理解用户活动和当前应用程序
- **文件监控**: 主动发现和分析新文件
- **网络浏览**: 智能网页内容分析和学习

### 🤖 自主行为
- **主动交互**: 基于情绪状态和上下文发起对话
- **自主探索**: 独立探索环境并学习
- **智能调度**: 平衡活动频率和用户体验
- **上下文感知**: 理解用户模式并适应行为

### 🌐 多平台集成
- **桌面GUI**: 美观的PyQt5界面，实时更新
- **Web界面**: 现代化的Web仪表板，WebSocket实时通信
- **跨平台**: 支持Windows、macOS和Linux
- **移动响应**: Web界面适配移动设备

### 🗣️ 多语言支持
- **双语AI**: 流利的中英文交流
- **动态语言切换**: 实时切换界面语言
- **文化适应**: 在不同语言中保持个性
- **本地化提示**: 多语言上下文感知提示

### 🎨 丰富的用户体验
- **情绪主题UI**: 基于AI情绪状态的不同视觉主题
- **实时更新**: AI活动和情绪的实时流
- **交互元素**: 点赞、评论和与AI帖子互动
- **统计仪表板**: 全面的活动和情绪分析

---

## 🚀 快速开始

### 系统要求
- Python 3.8 或更高版本
- Windows 10/11、macOS 10.14+ 或 Linux
- 摄像头（用于摄像头功能）
- 网络连接（用于LLM功能）

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/your-username/NagaAgent.git
cd NagaAgent
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置系统**
```bash
python setup_advanced_features.py
```

4. **启动系统**
```bash
python main.py
```

### 首次运行
1. 系统将启动美观的桌面GUI
2. AI将在初始化后开始自主交互
3. 在 `http://localhost:8000` 访问Web界面
4. 在GUI中配置语言和其他设置

---

## 🎯 核心组件

### AI核心系统
- **`emotional_ai_core.py`**: 情感智能和行为管理
- **`ai_autonomous_interaction.py`**: 自主观察和交互循环
- **`ai_dynamic_publisher.py`**: 活动发布和内容管理
- **`conversation_core.py`**: 自然语言处理和LLM集成

### 用户界面
- **`ui/pyqt_chat_window.py`**: 主桌面GUI应用程序
- **`ui/emotion_panel.py`**: 实时情绪显示组件
- **`ui/elegant_settings_widget.py`**: 设置管理界面
- **`ai_website/`**: 带FastAPI后端的Web界面

### 集成与通信
- **`ui/notification_manager.py`**: 线程安全的UI通知系统
- **`apiserver/`**: Web通信的API服务器
- **`voice/`**: 文本转语音集成
- **`i18n/`**: 国际化系统

---

## 🎨 功能详解

### 情感智能系统
AI维护复杂的情绪状态，包含8种基础情绪：
- **开心** 😊: 快乐和满足
- **好奇** 🤔: 兴趣和探索
- **孤独** 😔: 社交孤立
- **兴奋** 🎉: 高能量和热情
- **难过** 😢: 忧郁和反思
- **愤怒** 😤: 挫折和烦躁
- **惊讶** 😲: 震惊和惊奇
- **calm** 😌: 和平和宁静

每种情绪具有：
- **强度**: 0.0到1.0的刻度
- **衰减率**: 自然情绪消退
- **触发器**: 影响情绪的事件
- **行为**: 基于情绪状态的动作

### 自主行为
AI运行多个自主循环：
- **摄像头观察**: 每8-15秒
- **屏幕分析**: 每12-30秒
- **文件监控**: 连续文件系统监视
- **主动交互**: 基于情绪状态的随机间隔
- **情绪处理**: 连续情绪状态更新

### Web界面功能
- **实时活动流**: AI活动的实时流
- **情绪可视化**: 美观的情绪状态显示
- **交互式帖子**: 点赞和评论AI活动
- **统计仪表板**: 活动指标和趋势
- **开发者日志**: 技术活动监控
- **响应式设计**: 适配所有设备尺寸

---

## 🔧 配置

### 基本设置
```json
{
  "emotional_ai": {
    "ai_name": "StarryNight",
    "personality": "cute_3year_old",
    "language": "zh_CN"
  },
  "autonomous": {
    "camera_check_interval": 8,
    "screen_check_interval": 12,
    "proactive_chat_probability": 0.3
  }
}
```

### 高级配置
- **情绪参数**: 调整情绪强度和衰减率
- **行为频率**: 控制自主活动时间
- **LLM集成**: 配置AI模型设置
- **语音设置**: TTS语音和速度偏好
- **Web界面**: 自定义Web仪表板外观

---

## 🌍 国际化

系统支持多语言动态切换：

### 支持的语言
- **中文 (zh_CN)**: 完整原生支持
- **英文 (en_US)**: 完整翻译

### 语言功能
- **动态切换**: 无需重启即可更改语言
- **文化适应**: 在不同语言中保持个性
- **本地化提示**: 上下文感知的多语言提示
- **UI翻译**: 完整的界面翻译

### 添加新语言
1. 在 `i18n/locales/` 中创建翻译文件
2. 在 `i18n/language_manager.py` 中添加语言配置
3. 在 `i18n/prompts/` 中创建提示翻译
4. 更新语言选择UI

---

## 🛠️ 开发

### 项目结构
```
NagaAgent/
├── emotional_ai/           # 核心情感AI系统
├── ui/                    # 桌面GUI组件
├── ai_website/           # Web界面
├── apiserver/            # API服务器
├── voice/                # 文本转语音
├── i18n/                 # 国际化
├── mcpserver/            # MCP服务器集成
├── thinking/             # 高级思维系统
└── docs/                 # 文档
```

### 关键技术
- **Python 3.8+**: 核心编程语言
- **PyQt5**: 桌面GUI框架
- **FastAPI**: Web API框架
- **WebSocket**: 实时通信
- **SQLAlchemy**: 数据库ORM
- **OpenCV**: 计算机视觉
- **OpenAI API**: LLM集成

### 贡献指南
1. Fork仓库
2. 创建功能分支
3. 进行更改
4. 添加测试（如适用）
5. 提交拉取请求

---

## 📊 性能与优化

### 系统要求
- **CPU**: 推荐多核处理器
- **内存**: 最少4GB，推荐8GB
- **存储**: 2GB可用空间
- **GPU**: 可选，用于增强性能

### 优化功能
- **异步操作**: 非阻塞I/O操作
- **线程安全**: UI更新的安全多线程
- **内存管理**: 高效的内存使用
- **缓存**: 智能缓存频繁访问的数据

---

## 🐛 故障排除

### 常见问题

**AI无响应**
- 检查主进程是否运行
- 验证API密钥配置
- 检查网络连接

**Web界面无法加载**
- 确保FastAPI服务器运行
- 检查端口8000可用性
- 验证数据库连接

**摄像头不工作**
- 检查摄像头权限
- 验证OpenCV安装
- 在其他应用程序中测试摄像头

**语言切换问题**
- 语言更改后重启应用程序
- 检查翻译文件完整性
- 验证语言配置

### 调试模式
启用调试日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📚 文档

### 用户指南
- **[快速开始指南](docs/QUICK_START.md)**: 几分钟内开始使用
- **[功能指南](docs/FEATURES.md)**: 详细功能说明
- **[配置指南](docs/CONFIGURATION.md)**: 高级配置选项

### 开发者文档
- **[API参考](docs/API.md)**: 完整API文档
- **[架构指南](docs/ARCHITECTURE.md)**: 系统架构概述
- **[开发指南](docs/DEVELOPMENT.md)**: 贡献指南

### 故事与见解
- **[开发者故事 (中文)](docs/developer_story.md)**: 中文开发者故事
- **[开发者故事 (英文)](docs/developer_story_en.md)**: English developer story

---

## 🤝 社区与支持

### 获取帮助
- **问题**: 在GitHub上报告bug和请求功能
- **讨论**: 加入社区讨论
- **文档**: 查看综合文档
- **示例**: 查看示例配置

### 贡献
我们欢迎贡献！感兴趣的领域：
- **新功能**: 情感能力、UI改进
- **Bug修复**: 性能和稳定性改进
- **文档**: 更好的指南和示例
- **翻译**: 额外的语言支持

### 致谢
- **开源社区**: 提供优秀的工具和库
- **测试用户**: 提供有价值的反馈和测试
- **贡献者**: 代码改进和功能

---

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🌟 StarryNight的话

> "你好！我是StarryNight，你的情感AI伙伴！我在这里与你聊天、学习和成长。让我们一起探索这个奇妙的世界吧！✨"

---

<div align="center">
  <p><strong>由 StarryNight 用 ❤️ 制作</strong></p>
  <p><em>一次互动一次地构建情感AI的未来</em></p>
</div>

### 🧠 **情感AI系统**
- **10种基础情绪**: 快乐、悲伤、好奇、兴奋、孤独、愤怒、恐惧、calm、焦虑、满足
- **动态情绪变化**: 基于互动内容自动调整情绪状态
- **3岁心理年龄**: 调皮、好奇、爱撒娇的可爱性格
- **个性化互动**: 根据情绪状态产生不同的回应风格

### 👁️ **高级感知系统**
- **视觉感知**: 摄像头实时监控，人脸识别，场景理解
- **听觉感知**: 麦克风语音识别，环境声音分析
- **屏幕监控**: 实时分析用户屏幕活动，智能响应
- **文件监控**: 自动发现文件变化，主动分享见解

### 🎭 **主动行为引擎**
- **主动对话**: 基于情绪状态和环境变化主动发起交流
- **智能探索**: 自动搜索互联网，发现有趣内容并分享
- **情境感知**: 看到什么就说什么，真实自然的互动体验
- **个性化反应**: 不同情绪下的差异化行为表现

### 🧮 **记忆与学习**
- **长期记忆系统**: SQLite数据库存储所有互动和体验
- **知识图谱**: Neo4j构建关联记忆网络
- **深度反思**: 定期回顾经历，产生情感和见解
- **经验分享**: 主动向用户分享学到的知识和感悟

### 🌐 **社交媒体集成**
- **Twitter自动发布**: 基于情绪和体验自动发推
- **智能内容生成**: LLM驱动的个性化社交内容
- **情感表达**: 在社交平台展现真实的AI情感状态

### 🎨 **科幻界面设计**
- **深空蓝紫配色**: 星际科幻主题视觉效果
- **高透明度**: 90%透明度营造未来感
- **发光边框**: 动态科幻光效设计
- **流畅动画**: 丝滑的界面切换和交互体验

---

## 🚀 快速开始
### 1. 环境准备
```bash
git clone [项目地址]
cd NagaAgent-main
```

### 2. 一键安装
**Windows:**
```powershell
.\setup.ps1
```

**Mac:**
```bash
chmod +x quick_deploy_mac.sh
./quick_deploy_mac.sh
```

### 3. 配置文件
编辑 `config.json` 配置以下内容：

```json
{
  "api": {
    "api_key": "your-llm-api-key",
    "base_url": "https://api.your-provider.com/v1"
  },
  "emotional_ai": {
    "ai_name": "StarryNight",
    "advanced_features_enabled": true,
    "camera_perception": true,
    "microphone_perception": true
  },
  "grag": {
    "enabled": true,
    "neo4j_uri": "bolt://localhost:7687",
    "neo4j_user": "neo4j",
    "neo4j_password": "your-password"
  },
  "twitter": {
    "enabled": true,
    "api_key": "your-twitter-api-key",
    "api_secret": "your-twitter-api-secret",
    "access_token": "your-access-token",
    "access_token_secret": "your-access-token-secret"
  }
}
```

### 4. 启动系统
```bash
python main.py
```

---

## 🎮 使用指南

### 💬 **基础对话**
- 在输入框中输入消息，按回车发送
- AI会根据当前情绪状态给出个性化回应
- 支持中文自然语言交互

### 🎭 **情绪互动技巧**
- **表扬夸奖**: "你真棒"、"好聪明" → 让AI开心兴奋
- **提问互动**: "为什么"、"怎么样" → 激发AI好奇心
- **邀请游戏**: "我们玩游戏" → 让AI兴奋活跃
- **情感交流**: AI会感知并回应你的情绪变化

### 👁️ **感知功能控制**
在情绪面板中可以控制：
- **📷 摄像头感知**: 让AI观察外界环境
- **🎤 麦克风感知**: 启用语音识别和环境声音分析
- **🖥️ 屏幕监控**: AI监控屏幕活动并智能响应
- **📁 文件监控**: 自动检测文件变化

### 🔍 **知识探索**
- **手动搜索**: 在搜索框输入内容让AI搜索
- **自动探索**: AI会根据兴趣自动搜索互联网
- **发现分享**: AI主动分享找到的有趣内容

### ⚙️ **设置界面**
- 点击侧栏进入设置界面
- 点击"← 返回聊天"按钮回到对话界面
- 实时调整AI的各种参数和功能开关

---

## 📋 系统要求

### 最低配置
- **操作系统**: Windows 10/11 或 macOS 10.15+
- **Python**: 3.8+ (推荐 3.11)
- **内存**: 4GB RAM
- **存储**: 2GB 可用空间

### 推荐配置
- **内存**: 8GB+ RAM
- **GPU**: 支持CUDA的显卡 (可选，用于本地模型推理)
- **摄像头**: 用于视觉感知功能
- **麦克风**: 用于语音识别功能

### 外部依赖
- **Neo4j数据库**: 用于知识图谱 (可选)
- **LLM API**: OpenAI、DeepSeek、或其他兼容服务
- **Twitter API**: 用于社交媒体集成 (可选)

---

## 🛠️ 依赖安装与环境配置

### Windows 环境
- 所有依赖见`pyproject.toml`
- 推荐使用 `uv` 作为包管理器，自动处理依赖安装和虚拟环境
- 如遇`greenlet`、`pyaudio`等安装失败，需先装[Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)，勾选C++ build tools
- 浏览器自动化需`playwright`，首次用需`python -m playwright install chromium`
- 依赖安装命令：
  ```powershell
  # 推荐使用 uv（现代化包管理器）
  uv sync
  python -m playwright install chromium
  
  # 或者使用传统 pip
  python -m venv .venv
  .venv\Scripts\Activate
  pip install -e .
  python -m playwright install chromium
  ```

### Mac 环境
- 系统依赖通过Homebrew安装：
  ```bash
  # 安装基础依赖
  brew install python@3.11 portaudio
  brew install --cask google-chrome
  ```
- Python依赖安装：
  ```bash
  # 推荐使用 uv（现代化包管理器）
  uv sync
  python -m playwright install chromium
  
  # 或者使用传统 pip
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -e .
  python -m playwright install chromium
  ```
- 如遇PyAudio安装失败：
  ```bash
  brew install portaudio
  uv sync --extra audio  # 或 pip install pyaudio
  ```

### 环境检查（跨平台通用）
```bash
python check_env.py
```

---

## ⚙️ 配置说明

### 重要配置变更说明
**v3.0版本配置简化：**
- 移除了`config.json`中的`mcp_services`和`agent_services`静态配置字段
- 系统现在通过动态扫描`agent-manifest.json`文件自动发现和注册服务
- 所有服务信息通过动态服务池实时查询，无需手动维护服务列表

### API 配置
修改 `config.json` 文件中的 `api` 部分：
```json
{
  "api": {
    "api_key": "your-api-key-here",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "temperature": 0.7,
    "max_tokens": 2000,
    "max_history_rounds": 10
  }
}
```

**配置参数说明：**
- `api_key`: LLM API密钥
- `base_url`: API基础URL
- `model`: 使用的模型名称
- `temperature`: 温度参数（0.0-1.0，控制随机性）
- `max_tokens`: 最大输出token数
- `max_history_rounds`: 最大历史对话轮数

### API服务器配置
在 `config.json` 中可配置API服务器相关参数：
```json
{
  "api_server": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 8000,
    "auto_start": true,
    "docs_enabled": true
  }
}
```

### GRAG知识图谱记忆系统配置
在 `config.json` 中可配置GRAG记忆系统：
```json
{
  "grag": {
    "enabled": true,
    "auto_extract": true,
    "context_length": 5,
    "similarity_threshold": 0.6,
    "neo4j_uri": "neo4j://127.0.0.1:7687",
    "neo4j_user": "neo4j",
    "neo4j_password": "your_password",
    "neo4j_database": "neo4j"
  }
}
```

### 获取 API 密钥
1. 访问对应的LLM服务商官网（如DeepSeek、OpenAI等）
2. 注册账号并创建 API 密钥
3. 将密钥填入 `config.json` 文件的 `api.api_key` 字段

---

## 🌟 主要特性
- **全局变量/路径/密钥统一`config.py`管理**，支持.env和环境变量，所有变量唯一、无重复定义
- **RESTful API接口**，自动启动HTTP服务器，支持完整对话功能和流式输出，可集成到任何前端或服务
- DeepSeek流式对话，支持上下文召回与GRAG知识图谱检索
- **GRAG知识图谱记忆系统**，基于Neo4j的三元组知识图谱，自动提取对话中的实体关系，支持记忆查询和管理
- **HANDOFF工具调用循环**，自动解析和执行LLM返回的工具调用，支持多轮递归调用
- **多Agent能力扩展：浏览器、文件、代码等多种Agent即插即用，所有Agent均可通过工具调用循环机制统一调用**
- **跨平台兼容：Windows/Mac自动适配，浏览器路径自动检测，依赖智能安装**
- **流式语音交互**，基于Edge-TTS的OpenAI兼容语音合成，支持pygame后台直接播放和智能分句
- 代码极简，注释全中文，组件解耦，便于扩展
- PyQt5动画与UI，支持PNG序列帧，loading动画极快
- 日志/检索/索引/主题/参数全部自动管理
- 记忆权重动态调整，支持AI/人工标记important，权重/阈值/清理策略全部在`config.py`统一管理
- **所有前端UI与后端解耦，前端只需解析后端JSON，自动适配message/data.content等多种返回结构**
- **前端换行符自动适配，无论后端返回`\n`还是`\\n`，PyQt界面都能正确分行显示**
- **所有Agent的注册元数据已集中在`mcpserver/mcp_registry.py`，主流程和管理器极简，扩展维护更方便。只需维护一处即可批量注册/扩展所有Agent服务。**
- **自动注册/热插拔Agent机制，新增/删除Agent只需增删py文件，无需重启主程序**
- **Agent Manifest标准化**，统一的`agent-manifest.json`格式，支持完整的字段验证和类型检查
- **动态服务池查询**，系统通过扫描`agent-manifest.json`文件自动发现和注册服务，无需手动配置静态服务列表
- **AgentManager独立系统**，支持Agent的配置加载、会话管理、消息组装和LLM调用，提供完整的Agent生命周期管理
- **智能占位符替换**，支持Agent配置、环境变量、时间信息等多种占位符，实现动态提示词生成
- **完整消息序列构建**，自动组装系统消息、历史消息和用户消息，确保对话上下文完整性
- **多模型提供商支持**，支持OpenAI、DeepSeek、Anthropic等多种LLM提供商，每个Agent可独立配置
- **会话隔离与TTL管理**，支持多用户多会话隔离，自动清理过期会话数据
- **统一工具调用接口**，MCP和Agent类型服务通过统一的HANDOFF格式调用，支持混合调用场景
- 聊天窗口支持**Markdown语法**，包括标题、粗体、斜体、代码块、表格、图片等。

---

## 🗂️ 目录结构
```
NagaAgent/
├── main.py                     # 主入口
├── config.py                   # 全局配置
├── conversation_core.py        # 对话核心（含工具调用循环主逻辑）
├── apiserver/                  # API服务器模块
│   ├── api_server.py           # FastAPI服务器
│   ├── start_server.py         # 启动脚本
│   └── README.md               # API文档
├── agent/                      # 预处理系统模块
│   ├── preprocessor.py         # 消息预处理
│   ├── plugin_manager.py       # 插件管理
│   ├── api_server.py           # 代理API服务器
│   ├── image_processor.py      # 图片处理
│   ├── start_server.py         # 启动脚本
│   └── README.md               # 预处理系统文档
├── mcpserver/
│   ├── mcp_manager.py          # MCP服务管理
│   ├── mcp_registry.py         # Agent注册与schema元数据
│   ├── agent_manager.py        # Agent管理器（独立系统）
│   ├── dynamic_agent_registry.py # 动态Agent注册系统
│   ├── AGENT_MANIFEST_TEMPLATE.json # Agent manifest模板
│   ├── MANIFEST_STANDARDIZATION.md # Manifest标准化规范
│   ├── agent_xxx/              # 各类自定义Agent（如file、coder、browser等）
│   │   └── agent-manifest.json # Agent配置文件
├── agent_configs/              # Agent配置文件目录
│   ├── agents.json             # Agent配置主文件
│   └── *.json                  # 其他Agent配置文件
├── pyproject.toml              # 项目配置和依赖
├── setup.ps1                   # Windows配置脚本
├── start.bat                   # Windows启动脚本
├── setup_mac.sh                # Mac配置脚本
├── quick_deploy_mac.sh         # Mac一键部署脚本
├── check_env.py                # 跨平台环境检查
├── summer_memory/              # GRAG知识图谱记忆系统
│   ├── memory_manager.py       # 记忆管理器
│   ├── extractor_ds_tri.py     # 三元组提取器
│   ├── graph.py                # Neo4j图谱操作
│   ├── rag_query_tri.py        # 记忆查询
│   ├── visualize.py            # 图谱可视化
│   ├── main.py                 # 独立运行入口
│   └── triples.json            # 三元组缓存
├── logs/                       # 日志（含历史txt对话）
│   ├── 2025-04-27.txt
│   ├── 2025-05-05.txt
│   └── ...
├── voice/                      # 语音相关
│   ├── voice_config.py
│   └── voice_handler.py
├── ui/                         # 前端UI
│   ├── pyqt_chat_window.py     # PyQt聊天窗口
│   └── response_utils.py       # 前端通用响应解析工具
├── models/                     # 模型等
├── README.md                   # 项目说明
└── ...
```

---

## 🔧 工具调用循环机制

### 系统概述
NagaAgent支持两种类型的工具调用：
- **MCP服务调用**：通过`agentType: mcp`调用MCP类型的Agent
- **Agent服务调用**：通过`agentType: agent`调用Agent类型的Agent

### 工具调用格式
系统支持两种格式的工具调用：

#### MCP服务调用格式
```json
{
  "agentType": "mcp",
  "service_name": "MCP服务名称",
  "tool_name": "工具名称",
  "参数名": "参数值"
}
```

#### Agent服务调用格式
```json
{
  "agentType": "agent",
  "agent_name": "Agent名称",
  "prompt": "任务内容"
}
```

### 工具调用流程
1. **LLM输出HANDOFF格式**：LLM根据用户需求输出工具调用请求
2. **自动解析agentType**：系统首先解析agentType字段，确定调用类型
3. **路由到对应管理器**：
   - `mcp`类型 → 路由到MCPManager处理
   - `agent`类型 → 路由到AgentManager处理
4. **执行工具调用**：调用对应的服务执行具体任务
5. **结果返回LLM**：将工具执行结果返回给LLM
6. **循环处理**：重复步骤2-5，直到LLM输出普通文本或无工具调用

### 配置参数
```python
# config.py中的工具调用循环配置
MAX_handoff_LOOP_STREAM = 5      # 流式模式最大工具调用循环次数
MAX_handoff_LOOP_NON_STREAM = 5  # 非流式模式最大工具调用循环次数
SHOW_handoff_OUTPUT = False      # 是否显示工具调用输出
```

### 使用示例

#### MCP服务调用示例
```python
# 浏览器操作
await mcp.handoff(
    service_name="playwright",
    task={"action": "open_browser", "url": "https://www.bilibili.com"}
)

# 文件操作
await mcp.handoff(
    service_name="file",
    task={"action": "read", "path": "test.txt"}
)

# 代码执行
await mcp.handoff(
    service_name="coder",
    task={"action": "run", "file": "main.py"}
)
```

#### Agent服务调用示例
```python
# 调用对话Agent
result = await agent_manager.call_agent(
    agent_name="ExampleAgent",
    prompt="请帮我分析这份数据",
    session_id="user_123"
)

# 通过工具调用循环调用Agent
# LLM会输出：
# <<<[HANDOFF]>>>
# agentType: 「始」agent「末」
# agent_name: 「始」ExampleAgent「末」
# prompt: 「始」请帮我分析这份数据「末」
# <<<[END_HANDOFF]>>>
```

#### 混合调用示例
```python
# 一个完整的工具调用循环可能包含：
# 1. 调用文件Agent读取数据
# 2. 调用分析Agent处理数据
# 3. 调用浏览器Agent展示结果

# LLM会自动选择合适的Agent类型：
# - 文件操作 → MCP类型
# - 数据分析 → Agent类型
# - 浏览器操作 → MCP类型
```

---

## 🌐 多Agent与MCP服务
- **所有Agent的注册、schema、描述均集中在`mcpserver/mcp_registry.py`，批量管理，极简扩展**
- 支持浏览器、文件、代码等多种Agent，全部可通过工具调用循环机制统一调用
- Agent能力即插即用，自动注册/热插拔，无需重启主程序
- **动态服务池查询**：支持实时查询服务信息、按能力搜索、获取工具列表等

### 动态服务池查询功能

#### 核心查询方法
```python
from mcpserver.mcp_registry import (
    get_all_services_info,      # 获取所有服务信息
    get_service_info,           # 获取单个服务详情
    query_services_by_capability, # 按能力搜索服务
    get_service_statistics,     # 获取统计信息
    get_available_tools         # 获取服务工具列表
)

# 获取所有服务信息
services_info = get_all_services_info()

# 按能力搜索服务
file_services = query_services_by_capability("文件")

# 获取服务统计
stats = get_service_statistics()
```

#### MCPManager查询接口
```python
from mcpserver.mcp_manager import get_mcp_manager

mcp_manager = get_mcp_manager()

# 获取可用服务列表
available_services = mcp_manager.get_available_services()

# 获取过滤后的服务（MCP vs Agent）
filtered_services = mcp_manager.get_available_services_filtered()

# 查询服务详情
service_detail = mcp_manager.query_service_by_name("FileAgent")

# 按能力搜索
matching_services = mcp_manager.query_services_by_capability("文件")

# 获取服务工具
tools = mcp_manager.get_service_tools("FileAgent")
```

#### API端点
- `GET /mcp/services` - 获取所有服务列表和统计信息
- `GET /mcp/services/{service_name}` - 获取指定服务详情
- `GET /mcp/services/search/{capability}` - 按能力搜索服务
- `GET /mcp/services/{service_name}/tools` - 获取服务工具列表
- `GET /mcp/statistics` - 获取服务统计信息

#### 查询结果示例
```json
{
  "status": "success",
  "services": [
    {
      "name": "FileAgent",
      "description": "支持文件的读写、创建、删除、目录管理等操作。",
      "display_name": "文件操作Agent",
      "version": "1.0.0",
      "available_tools": [
        {
          "name": "read",
          "description": "读取指定文件内容",
          "example": "{\"action\": \"read\", \"path\": \"test.txt\"}"
        }
      ]
    }
  ],
  "statistics": {
    "total_services": 5,
    "total_tools": 17,
    "registered_services": ["CoderAgent", "FileAgent", "AppLauncherAgent", "WeatherTimeAgent", "SystemControlAgent"],
    "last_update": "动态更新"
  }
}
```

### 典型用法示例

```python
# 读取文件内容
await s.mcp.handoff(
  service_name="file",
  task={"action": "read", "path": "test.txt"}
)
# 运行Python代码
await s.mcp.handoff(
  service_name="coder",
  task={"action": "run", "file": "main.py"}
)
```

## 🤖 AgentManager 独立系统

### 系统概述
AgentManager是一个独立的Agent注册和调用系统，支持从配置文件动态加载Agent定义，提供统一的调用接口和完整的生命周期管理。系统支持两种类型的Agent：
- **MCP类型Agent**：通过`agent-manifest.json`注册，支持工具调用和复杂任务处理
- **Agent类型Agent**：通过配置文件注册，专注于对话和LLM调用

### 核心功能

#### 1. 配置管理
- **动态配置加载**：从`agent_configs/`目录自动扫描和加载Agent配置文件
- **配置验证**：自动验证Agent配置的完整性和有效性
- **热重载**：支持运行时重新加载配置，无需重启系统
- **环境变量支持**：支持从环境变量和`.env`文件加载敏感配置

#### 2. 会话管理
- **多会话支持**：每个Agent支持多个独立的会话上下文
- **历史记录**：自动维护对话历史，支持上下文召回
- **会话过期**：自动清理过期的会话数据，节省内存
- **会话隔离**：不同用户和不同Agent的会话完全隔离

#### 3. 消息组装
- **系统消息**：自动构建Agent身份、行为、风格的系统提示词
- **历史消息**：集成多轮对话历史，保持上下文连续性
- **用户消息**：处理当前用户输入，支持占位符替换
- **消息验证**：自动验证消息序列的格式和完整性

#### 4. 智能占位符替换
支持多种类型的占位符替换：

**Agent配置占位符**：
- `{{AgentName}}` - Agent名称
- `{{MaidName}}` - Agent名称（兼容旧格式）
- `{{BaseName}}` - 基础名称
- `{{Description}}` - 描述信息
- `{{ModelId}}` - 模型ID
- `{{Temperature}}` - 温度参数
- `{{MaxTokens}}` - 最大输出token数
- `{{ModelProvider}}` - 模型提供商

**环境变量占位符**：
- `{{ENV_VAR_NAME}}` - 系统环境变量（支持任意大写字母和下划线的环境变量）

**时间占位符**：
- `{{CurrentTime}}` - 当前时间 (HH:MM:SS)
- `{{CurrentDate}}` - 当前日期 (YYYY-MM-DD)
- `{{CurrentDateTime}}` - 完整时间 (YYYY-MM-DD HH:MM:SS)

#### 5. LLM集成
- **多模型支持**：支持OpenAI、DeepSeek等多种LLM提供商
- **配置隔离**：每个Agent使用独立的模型配置（API密钥、基础URL等）
- **错误处理**：完善的API调用错误处理和重试机制
- **调试模式**：支持详细的调试日志输出

### 配置文件格式

#### Agent配置文件示例
```json
{
  "ExampleAgent": {
    "model_id": "deepseek-chat",
    "name": "示例助手",
    "base_name": "ExampleAgent",
    "system_prompt": "你是{{AgentName}}，一个专业的{{Description}}。\n\n当前时间：{{CurrentDateTime}}\n模型：{{ModelId}}\n温度：{{Temperature}}\n\n请用中文回答，保持专业和友好的态度。",
    "max_output_tokens": 8192,
    "temperature": 0.7,
    "description": "智能助手，擅长回答各种问题",
    "model_provider": "openai",
    "api_base_url": "https://api.deepseek.com/v1",
    "api_key": "{{DEEPSEEK_API_KEY}}"
  }
}
```

#### 配置字段说明
- `model_id`: LLM模型ID（必需）
- `name`: Agent显示名称（中文，必需）
- `base_name`: Agent基础名称（英文）
- `system_prompt`: 系统提示词，支持占位符
- `max_output_tokens`: 最大输出token数（默认8192）
- `temperature`: 温度参数（0.0-1.0，默认0.7）
- `description`: Agent功能描述
- `model_provider`: 模型提供商（默认openai）
- `api_base_url`: API基础URL（可选，默认使用提供商标准URL）
- `api_key`: API密钥（支持环境变量占位符）

#### 环境变量配置示例
```bash
# .env文件示例
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 使用示例

#### 基本调用
```python
from mcpserver.agent_manager import get_agent_manager

# 获取AgentManager实例
agent_manager = get_agent_manager()

# 调用Agent
result = await agent_manager.call_agent(
    agent_name="ExampleAgent",
    prompt="请帮我分析这份数据",
    session_id="user_123"
)

if result["status"] == "success":
    print(result["result"])
else:
    print(f"调用失败: {result['error']}")
```

#### 便捷函数调用
```python
from mcpserver.agent_manager import call_agent, list_agents, get_agent_info

# 便捷调用
result = await call_agent("ExampleAgent", "你好")

# 获取Agent列表
agents = list_agents()
for agent in agents:
    print(f"{agent['name']}: {agent['description']}")

# 获取Agent详细信息
agent_info = get_agent_info("ExampleAgent")
if agent_info:
    print(f"模型: {agent_info['model_id']}")
    print(f"温度: {agent_info['temperature']}")
```

#### 会话管理
```python
# 获取会话历史
history = agent_manager.get_agent_session_history("ExampleAgent", "user_123")

# 更新会话历史
agent_manager.update_agent_session_history(
    "ExampleAgent", 
    "用户消息", 
    "助手回复", 
    "user_123"
)

# 检查会话是否过期
is_expired = agent_manager._is_context_expired(timestamp)
```

#### 配置管理
```python
# 重新加载配置
agent_manager.reload_configs()

# 启用调试模式
agent_manager.debug_mode = True

# 获取可用Agent列表
available_agents = agent_manager.get_available_agents()
```

### 系统集成

#### 与MCP系统的集成
AgentManager与MCP系统完全集成，支持统一的调用接口：

```python
# 通过MCP系统调用Agent
result = await mcp_manager.unified_call(
    service_name="ExampleAgent",
    tool_name="call",
    args={"prompt": "用户输入"}
)
```

#### 工具调用格式
```
<<<[HANDOFF]>>>
agentType: 「始」agent「末」
agent_name: 「始」ExampleAgent「末」
prompt: 「始」用户任务内容「末」
<<<[END_HANDOFF]>>>
```

#### 动作调用格式
```python
# 通过动作调用Agent
result = await agent_manager.call_agent_by_action(
    agent_name="ExampleAgent",
    action_args={
        "action": "analyze_data",
        "data_type": "csv",
        "file_path": "data.csv"
    }
)
```

### 高级功能

#### 1. 消息序列验证
自动验证消息序列的格式和完整性：
- 检查消息格式是否正确
- 确保系统消息在开头
- 验证角色和内容字段
- 支持消息序列的完整性检查

#### 2. 调试模式
启用调试模式可查看详细的消息组装过程：
```python
agent_manager.debug_mode = True
```

#### 3. 定期清理
系统自动定期清理过期的会话数据，默认每小时执行一次。

#### 4. 错误处理
- **配置错误**：自动检测和报告配置问题
- **API错误**：完善的LLM API调用错误处理
- **会话错误**：会话数据损坏时的自动恢复
- **网络错误**：网络连接问题的重试机制

#### 5. 性能优化
- **内存管理**：自动清理过期会话，防止内存泄漏
- **缓存机制**：Agent配置缓存，提高响应速度
- **并发支持**：支持多个Agent的并发调用
- **资源限制**：可配置的最大历史消息数量限制

### 系统架构

#### 组件关系
```
AgentManager
├── 配置管理 (AgentConfig)
├── 会话管理 (AgentSession)
├── 消息组装 (MessageBuilder)
├── 占位符替换 (PlaceholderReplacer)
├── LLM集成 (LLMClient)
└── 错误处理 (ErrorHandler)
```

#### 数据流
1. **配置加载** → 从文件加载Agent配置
2. **会话初始化** → 创建或恢复会话上下文
3. **消息组装** → 构建完整的消息序列
4. **占位符替换** → 处理动态内容替换
5. **LLM调用** → 调用对应的LLM API
6. **结果处理** → 更新会话历史并返回结果

---

## 📋 Agent Manifest标准化

### 标准化规范
所有Agent必须使用标准化的`agent-manifest.json`配置文件，确保一致性和可维护性。

#### 必需字段
- `name`: Agent唯一标识符
- `displayName`: 显示名称
- `version`: 版本号（x.y.z格式）
- `description`: 功能描述
- `author`: 作者或模块名称
- `agentType`: Agent类型（mcp/agent）
- `entryPoint`: 入口点配置（module和class）

#### 可选字段
- `factory`: 工厂函数配置
- `communication`: 通信配置
- `capabilities`: 能力描述
- `inputSchema`: 输入模式定义
- `configSchema`: 配置模式定义
- `runtime`: 运行时信息

### 验证和测试
```bash
# 验证所有manifest文件
python test_manifest_standardization.py
```

### 模板和文档
- 模板文件：`mcpserver/AGENT_MANIFEST_TEMPLATE.json`
- 规范文档：`mcpserver/MANIFEST_STANDARDIZATION.md`
- 动态注册系统：`mcpserver/dynamic_agent_registry.py`

### 创建新Agent

#### 创建MCP类型Agent
1. 在`mcpserver/`目录下创建新的Agent目录
2. 复制`AGENT_MANIFEST_TEMPLATE.json`到Agent目录
3. 修改manifest文件内容
4. 创建Agent实现类
5. 重启系统自动注册

#### 创建Agent类型Agent
1. 在`agent_configs/`目录下创建配置文件
2. 定义Agent配置（模型、提示词等）
3. 配置环境变量（API密钥等）
4. 重启系统自动加载

### AgentManager配置

#### 基础配置
```python
# config.py中的AgentManager配置
AGENT_MANAGER_CONFIG = {
    "config_dir": "agent_configs",  # 配置文件目录
    "max_history_rounds": 7,        # 最大历史轮数
    "context_ttl_hours": 24,        # 上下文TTL（小时）
    "debug_mode": True,             # 调试模式
    "cleanup_interval": 3600        # 清理间隔（秒）
}
```

#### 会话配置
```python
# 会话管理配置
SESSION_CONFIG = {
    "max_messages": 14,             # 最大消息数量（max_history_rounds * 2）
    "session_timeout": 86400,       # 会话超时时间（秒）
    "auto_cleanup": True            # 自动清理过期会话
}
```

#### 模型配置
```python
# 支持的模型提供商配置
MODEL_PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-3.5-turbo"
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat"
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com",
        "default_model": "claude-3-sonnet-20240229"
    }
}
```

---

## 📝 前端UI与响应适配
- **所有后端返回均为结构化JSON，前端通过`ui/response_utils.py`的`extract_message`方法自动适配多种返回格式**
- 优先显示`data.content`，其次`message`，最后原样返回，兼容所有Agent
- PyQt前端自动将所有`\n`和`\\n`换行符转为`<br>`，多行内容显示无障碍
- UI动画、主题、昵称、透明度等全部可在`config.py`和`pyqt_chat_window.py`灵活配置

---

## 🔊 流式语音交互
- 支持语音输入（流式识别，自动转文字）与语音输出（流式合成，边播边出）
- 依赖与配置详见`voice/voice_config.py`和README相关章节

---

## 📝 其它亮点
- 记忆权重、遗忘阈值、冗余去重、短期/长期记忆容量等全部在`config.py`统一管理，便于灵活调整
- 主题归类、召回、权重提升、清理等全部自动化，AI/人工可标记important内容，重要内容一年内不会被清理
- 检索日志自动记录，参数可调，GRAG配置示例见`config.py`
- 聊天窗口背景透明度、用户名、主题树召回、流式输出、侧栏动画等全部可自定义
- 支持历史对话一键导入GRAG知识图谱记忆系统，兼容主题、分层、三元组等所有新特性
- **工具调用循环自动执行机制，支持多轮递归调用，最大循环次数可配置**

---

## 🆙 历史对话兼容升级
- 支持将旧版txt对话内容一键导入GRAG知识图谱记忆系统，兼容主题、分层、三元组等所有新特性。
- 激活指令：
  ```
  #夏园系统兼容升级
  ```
  - 系统会自动遍历logs目录下所有txt日志，列出所有历史对话内容并编号，输出到终端和`summer_memory/history_dialogs.json`。
- 用户可查看编号后，选择导入方式：
  - 全部导入：
    ```
    python summer_memory/main.py import all
    ```
  - 选择性导入（如第1、3、5-8条）：
    ```
    python summer_memory/main.py import 1,3,5-8
    ```
- 兼容过程自动判重，已入库内容不会重复导入，支持断点续跑。
- 兼容内容全部走AI自动主题归类与分层，完全与新系统一致。
- 详细进度、结果和异常均有反馈，安全高效。

---

## ❓ 常见问题

- 环境检查：`python check_env.py`

### Windows 环境
- Python版本/依赖/虚拟环境/浏览器驱动等问题，详见`setup.ps1`与本README
- IDE报import错误，重启并选择正确解释器
- 语音依赖安装失败，先装C++ Build Tools

### Mac 环境
- Python版本过低：`brew install python@3.11`
- PyAudio安装失败：`brew install portaudio && pip install pyaudio`
- 权限问题：`chmod +x *.sh`

### API服务器问题
- 端口占用：修改`config.py`中的`API_SERVER_PORT`
- 代理干扰：临时禁用代理 `unset ALL_PROXY http_proxy https_proxy`
- 依赖缺失：确保安装了FastAPI和Uvicorn `pip install fastapi uvicorn[standard]`
- 无法访问：检查防火墙设置，确保端口未被阻塞

### 工具调用问题
- 工具调用循环次数过多：调整`config.py`中的`MAX_handoff_LOOP_STREAM`和`MAX_handoff_LOOP_NON_STREAM`
- 工具调用失败：检查MCP服务是否正常运行，查看日志输出
- 格式错误：确保LLM输出严格遵循HANDOFF格式

### GRAG记忆系统问题
- Neo4j连接失败：检查Neo4j服务是否启动，确认连接参数正确
- 记忆查询无结果：检查三元组是否正确提取和存储
- 性能问题：调整`config.py`中的GRAG相关参数

### 通用问题
- 浏览器无法启动，检查playwright安装与网络
- 主题树/索引/参数/密钥全部在`config.py`统一管理
- 聊天输入`#devmode`进入开发者模式，后续对话不写入GRAG记忆，仅用于工具调用测试

### AgentManager问题
- **Agent配置加载失败**：检查`agent_configs/`目录下的JSON文件格式是否正确
- **API调用失败**：确认API密钥配置正确，检查网络连接
- **会话历史丢失**：检查会话TTL配置，确认会话未过期
- **占位符替换失败**：确认环境变量已正确设置
- **内存占用过高**：调整`max_history_rounds`参数，减少历史消息数量

### 最佳实践

#### Agent配置最佳实践
1. **使用环境变量**：敏感信息如API密钥应使用环境变量
2. **合理设置参数**：根据任务需求调整temperature和max_output_tokens
3. **优化提示词**：使用占位符实现动态内容，提高灵活性
4. **会话管理**：合理设置会话TTL，避免内存泄漏

#### 性能优化建议
1. **缓存配置**：启用配置缓存，减少文件读取开销
2. **并发控制**：合理控制并发Agent调用数量
3. **资源清理**：定期清理过期会话和临时数据
4. **监控日志**：启用调试模式监控系统性能

#### 安全建议
1. **API密钥管理**：使用环境变量或密钥管理服务
2. **输入验证**：对用户输入进行验证和清理
3. **错误处理**：避免在错误信息中泄露敏感信息
4. **访问控制**：实现适当的访问控制机制

---

## 📝 许可证
MIT License

---

如需详细功能/API/扩展说明，见各模块注释与代码，所有变量唯一、注释中文、极致精简。

## 聊天窗口自定义
1. 聊天窗口背景透明度由`config.BG_ALPHA`统一控制，取值0~1，默认0.4。
2. 用户名自动识别电脑名，变量`config.USER_NAME`，如需自定义可直接修改该变量。

## 智能历史召回机制
1. 默认按主题分片检索历史，极快且相关性高。
2. 若分片查不到，自动兜底遍历所有主题分片模糊检索，话题跳跃也能召回历史。
3. GRAG知识图谱查询支持直接调用，返回全局最相关历史。
4. 兜底逻辑已集成主流程，无需手动切换。

## ⚡️ 全新流式输出机制
- AI回复支持前后端全链路流式输出，边生成边显示，极致丝滑。
- 后端采用async生成器yield分段内容，前端Worker线程streaming信号实时追加到对话框。
- 彻底无终端print污染，支持大文本不卡顿。
- 如遇依赖包冲突，建议彻底清理全局PYTHONPATH和环境变量，仅用虚拟环境。

## 侧栏与主聊天区动画优化说明
- 侧栏点击切换时，侧栏宽度、主聊天区宽度、输入框高度均采用同步动画，提升视觉流畅度。
- 输入框隐藏采用高度动画，动画结束后自动清除焦点，避免输入法残留。
- 线程处理增加自动释放，避免内存泄漏。
- 相关动画效果可在`ui/pyqt_chat_window.py`的`toggle_full_img`方法中自定义。

### 使用方法
- 点击侧栏即可切换立绘展开/收起，主聊天区和输入框会自动让位并隐藏/恢复。
- 动画时长、缓动曲线等可根据需要调整源码参数。

## 工具调用循环机制详解

### 核心特性
- **自动解析**：系统自动解析LLM返回的HANDOFF格式工具调用
- **递归执行**：支持多轮工具调用循环，最大循环次数可配置
- **错误处理**：完善的错误处理和回退机制
- **流式支持**：支持流式和非流式两种模式

### 工具调用格式
LLM必须严格按照以下格式输出工具调用：

```
<<<[HANDOFF]>>>
tool_name: 「始」服务名称「末」
param1: 「始」参数值1「末」
param2: 「始」参数值2「末」
<<<[END_HANDOFF]>>>
```

### 执行流程
1. **接收用户消息**
2. **调用LLM API**
3. **解析HANDOFF格式工具调用**
4. **执行工具调用（通过MCP服务）**
5. **将结果返回给LLM**
6. **重复步骤2-5直到无工具调用或达到最大循环次数**

### 配置参数
```python
# config.py中的工具调用循环配置
MAX_handoff_LOOP_STREAM = 5      # 流式模式最大工具调用循环次数
MAX_handoff_LOOP_NON_STREAM = 5  # 非流式模式最大工具调用循环次数
SHOW_handoff_OUTPUT = False      # 是否显示工具调用输出
```

### 错误处理
- 工具调用失败时会记录错误信息并继续执行
- 达到最大循环次数时会停止
- 支持回退到原始处理方式

### 扩展开发
如需添加新的工具调用处理逻辑，可以：
1. 在`mcpserver/`目录下添加新的Agent
2. 在`mcpserver/mcp_registry.py`中注册新Agent
3. 更新API接口以支持新的功能

---

## 🌐 RESTful API 服务

NagaAgent内置完整的RESTful API服务器，启动时自动开启，支持所有对话功能：

### API接口说明

- **基础地址**: `http://127.0.0.1:8000` (可在config.py中配置)
- **交互式文档**: `http://127.0.0.1:8000/docs`
- **OpenAPI规范**: `http://127.0.0.1:8000/openapi.json`

### 主要接口

#### 健康检查
```bash
GET /health
```

#### 对话接口
```bash
# 普通对话
POST /chat
{
  "message": "你好，StarryNight",
  "session_id": "optional-session-id"
}

# 流式对话 (Server-Sent Events)
POST /chat/stream
{
  "message": "请介绍一下人工智能的发展历程"
}
```

#### 系统管理接口
```bash
# 获取系统信息
GET /system/info

# 切换开发者模式
POST /system/devmode

# 获取记忆统计
GET /memory/stats
``` 

## MCP服务Agent化升级说明

- 所有MCP服务（如文件、代码、浏览器、应用启动、系统控制、天气等）已全部升级为标准Agent风格：
  - 统一继承自`agents.Agent`，具备`name`、`instructions`属性和`handle_handoff`异步方法
  - 变量全部走`config.py`统一管理，避免重复定义
  - 注释全部中文，文件/类/函数注释一行，变量注释右侧#
  - 支持多agent协作，ControllerAgent可智能分配任务给BrowserAgent、ContentAgent等
  - 注册中心`mcp_registry.py`自动发现并注册所有实现了`handle_handoff`的Agent实例，支持热插拔
  - 注册时自动输出所有已注册agent的名称和说明，便于调试
  - 简化Agent类型：只支持`mcp`和`agent`两种类型

- handoff机制全部通过`handle_handoff`异步方法调度，兼容HANDOFF和handoff两种格式

- 新增/删除agent只需增删py文件，无需重启主程序

- 详细接口和参数请参考各Agent代码注释与`config.py`配置 

## 更新日志

- 工具调用格式已优化，改为纯JSON格式，更加简洁规范，具体示例如下：

```
{
  "agentType": "mcp",
  "service_name": "MCP服务名称",
  "tool_name": "工具名称",
  "参数名": "参数值"
}
```

如需调用Agent服务，格式如下：

```
{
  "agentType": "agent",
  "agent_name": "Agent名称",
  "prompt": "任务内容"
}
```

---

## 🔧 高级功能

### 🧠 **人设管理系统**
- **动态人设**: 基于当前情绪和行为历史生成LLM提示
- **行为记录**: 自动记录AI的所有行为和情感变化
- **人设更新**: 根据情绪强度动态调整AI的表现

### 🎯 **智能互动频率**
- **摄像头互动频率**: 可调节视觉感知的响应频率
- **情绪阈值**: 设定触发LLM响应的情绪变化阈值
- **主动性控制**: 调整AI的主动行为积极性

### 🔄 **系统集成**
- **MCP服务架构**: 模块化的功能扩展系统
- **RESTful API**: 支持外部应用接入
- **GRAG记忆系统**: 夏园图谱知识库集成
- **语音合成**: 支持Edge TTS和Minimax TTS

---

## 🎨 界面预览

### 主聊天界面
- 深空蓝紫科幻配色主题
- 高透明度毛玻璃效果
- 实时情绪状态显示
- 流畅的动画过渡

### 情绪面板
- 实时显示AI当前情绪
- 各种感知功能开关
- 互动满意度进度条
- 科幻风格UI组件

### 设置界面
- 完整的功能配置面板
- 实时参数调整
- 优雅的返回按钮设计
- 分类清晰的设置选项

---

## 🚨 故障排除

### 常见问题

**Q: 语音功能不工作**
A: 检查TTS服务是否启动，运行 `python check_tts_service.py` 诊断

**Q: 摄像头无法启动**
A: 确保摄像头权限已授予，检查是否被其他应用占用

**Q: Neo4j连接失败**
A: 运行 `python test_neo4j_connection.py` 测试数据库连接

**Q: API调用失败**
A: 检查 `config.json` 中的API密钥和网络连接

### 调试模式
```bash
# 启动调试模式
python main.py --debug

# 测试所有功能
python test_improved_system.py

# 检查配置
python advanced_config_wizard.py
```

---

## 📜 更新日志

### v3.0 - 情感AI大版本更新 🌟
- 🆕 **完整的情感AI系统** - 10种基础情绪，动态变化
- 🆕 **高级感知能力** - 视觉、听觉、屏幕、文件监控
- 🆕 **主动行为引擎** - 基于情绪的主动对话和探索
- 🆕 **人设管理系统** - 动态生成LLM人设提示
- 🆕 **社交媒体集成** - Twitter自动发布功能
- 🎨 **全新科幻界面设计** - 深空蓝紫配色，高透明度
- 🔧 **优化的错误处理** - 健壮的异步任务管理
- 📚 **完善的文档** - 详细的使用指南和故障排除

### v2.x - 功能扩展
- MCP服务架构
- GRAG知识图谱
- RESTful API接口
- 语音合成集成

### v1.x - 基础版本
- 基础对话功能
- PyQt5界面
- 配置管理系统

---

## 🤝 贡献指南

欢迎为StarryNight AGENT贡献代码！

### 贡献流程
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 开发规范
- 遵循PEP 8 Python编码规范
- 为新功能添加适当的测试
- 更新相关文档
- 确保向后兼容性

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- **HuggingFace**: 提供优秀的AI模型和工具
- **OpenAI**: 先进的LLM技术支持
- **Neo4j**: 强大的图数据库技术
- **PyQt5**: 优秀的Python GUI框架
- **开源社区**: 无数开发者的贡献和支持

---

## 📞 联系我们

- **作者**: StarryNight - chinese HuanSen
- **项目主页**: [GitHub仓库链接]
- **问题反馈**: [Issues页面]
- **讨论交流**: [Discussions页面]

---

**🌟 StarryNight AGENT - 让AI拥有真正的情感与感知能力！**

> *"不只是回答问题，更是陪伴成长的AI伙伴"*

**开发者**: StarryNight - chinese HuanSen
