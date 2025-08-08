# 🔧 故障排除指南

## 常见问题及解决方案

### 1. 🤖 表情识别模型加载失败

**问题**:
```
表情识别模型加载失败: We couldn't connect to 'https://huggingface.co'
```

**原因**: 无法连接到Hugging Face下载ML模型

**解决方案**:

#### 选项A: 离线模式 (推荐)
```bash
python offline_mode_setup.py
```

#### 选项B: 配置代理
```bash
export HF_ENDPOINT=https://hf-mirror.com  # 使用镜像
```

#### 选项C: 手动下载模型
```bash
# 下载到本地
git lfs clone https://huggingface.co/trpakov/vit-face-expression
```

#### 选项D: 禁用表情识别
在 `config.json` 中设置:
```json
{
  "emotional_ai": {
    "camera_perception": false
  }
}
```

### 2. 🗃️ Neo4j连接问题

**问题**:
```
记忆知识图谱加载失败: cannot access local variable 'NEO4J_AVAILABLE'
```

**解决方案**:

#### 快速修复
```bash
python setup_advanced_features.py
# 选择 Neo4j 配置选项
```

#### 手动配置
1. **Docker部署** (推荐):
```bash
docker run -d \
  --name nagaai-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest
```

2. **更新配置**:
```json
{
  "grag": {
    "enabled": true,
    "neo4j_uri": "neo4j://localhost:7687",
    "neo4j_user": "neo4j",
    "neo4j_password": "your_password"
  }
}
```

#### 禁用图数据库
```json
{
  "grag": {
    "enabled": false
  },
  "emotional_ai": {
    "knowledge_graph_enabled": false
  }
}
```

### 3. 🐦 Twitter API配置

**问题**:
```
Twitter凭证未配置
```

**解决方案**:

#### 获取Twitter API密钥
1. 访问 https://developer.twitter.com/
2. 创建应用获取密钥
3. 运行配置助手:
```bash
python setup_advanced_features.py
```

#### 手动配置环境变量
创建 `.env` 文件:
```
TWITTER_CONSUMER_KEY=your_consumer_key
TWITTER_CONSUMER_SECRET=your_consumer_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

#### 禁用Twitter功能
```json
{
  "emotional_ai": {
    "social_media_enabled": false
  }
}
```

### 4. 🔑 OpenAI API配置

**问题**:
```
请在 config.json 文件中设置正确的 api.api_key 值
```

**解决方案**:

#### 配置OpenAI API
```json
{
  "api": {
    "api_key": "your_api_key_here",
    "base_url": "https://api.openai.com/v1",
    "model_name": "gpt-3.5-turbo"
  }
}
```

#### 使用其他API提供商
```json
{
  "api": {
    "api_key": "your_api_key",
    "base_url": "https://api.deepseek.com/v1",
    "model_name": "deepseek-chat"
  }
}
```

### 5. 📦 依赖安装问题

**问题**: 缺少某些Python包

**解决方案**:

#### 检查并安装依赖
```bash
python setup_advanced_features.py
# 会自动检查并安装缺失的依赖
```

#### 手动安装核心依赖
```bash
# 基础依赖
pip install opencv-python>=4.8.0
pip install SpeechRecognition>=3.10.0
pip install sounddevice>=0.4.6

# ML依赖 (可选)
pip install transformers>=4.30.0
pip install torch>=2.0.0
pip install sentence-transformers>=2.2.0

# 社交媒体 (可选)
pip install tweepy>=4.14.0

# 图数据库 (可选)
pip install py2neo>=2021.2.3
```

### 6. 🎥 摄像头/麦克风权限问题

**问题**: 无法访问摄像头或麦克风

**解决方案**:

#### Windows
1. 设置 → 隐私 → 摄像头/麦克风
2. 允许应用访问摄像头/麦克风
3. 允许桌面应用访问

#### Linux
```bash
# 检查权限
ls -l /dev/video0
ls -l /dev/audio*

# 添加用户到相关组
sudo usermod -a -G video $USER
sudo usermod -a -G audio $USER
```

#### macOS
系统偏好设置 → 安全性与隐私 → 摄像头/麦克风

### 7. 🚀 性能优化

**问题**: 运行缓慢或内存不足

**解决方案**:

#### 减少功能负载
```json
{
  "emotional_ai": {
    "camera_perception": false,
    "microphone_perception": false,
    "knowledge_graph_enabled": false,
    "max_memory_entries": 5000
  }
}
```

#### 调整刷新频率
```json
{
  "emotional_ai": {
    "reflection_interval": 7200,
    "exploration_interval": 600
  }
}
```

## 🛠️ 快速诊断工具

### 运行系统检查
```bash
python setup_advanced_features.py
```

### 测试基础功能
```bash
python test_emotional_ai_integration.py
```

### 启用离线模式
```bash
python offline_mode_setup.py
```

## 🆘 获取帮助

### 查看日志
检查 `logs/` 目录下的日志文件

### 系统信息
运行测试脚本查看系统状态

### 渐进式启用
建议按以下顺序启用功能:
1. 基础情绪系统 ✅
2. 记忆系统 ✅
3. 性格演化 ✅
4. 深度反思 (需要API)
5. 知识图谱 (需要Neo4j)
6. 社交媒体 (需要Twitter API)
7. 高级感知 (需要硬件权限)

## 🔄 重置到默认状态

如果遇到无法解决的问题，可以重置配置:

```bash
# 备份当前配置
cp config.json config.json.backup

# 恢复默认配置
cp config.json.example config.json

# 或运行离线模式设置
python offline_mode_setup.py
```

记住：**渐进式启用功能，确保每个阶段都稳定运行后再添加新功能！**