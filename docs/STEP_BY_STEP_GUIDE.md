
# 🚀 分步启用高级功能指南

## 第一步：确保基础功能运行
运行 `python main.py` 确保以下功能正常：
- ✅ 基础情绪系统
- ✅ 记忆存储
- ✅ 语音播放
- ✅ 主动对话

## 第二步：配置API（如果需要深度反思）
在 config.json 中配置：
```json
{
  "api": {
    "api_key": "your_openai_api_key_here",
    "base_url": "https://api.openai.com/v1",
    "model_name": "gpt-3.5-turbo"
  }
}
```

## 第三步：在GUI中逐步启用功能
1. 启动程序：`python main.py`
2. 点击设置 → "🎭 情绪AI系统"
3. 逐一启用功能：
   - ✅ 深度反思功能
   - ✅ 性格演化
   - ✅ 知识图谱构建（如果有Neo4j）
   - ✅ 摄像头感知（如果需要）
   - ✅ 麦克风感知（如果需要）

## 第四步：测试高级功能
每启用一个功能后，观察：
- 控制台日志是否有错误
- AI行为是否正常
- 内存使用是否合理

## 第五步：配置可选服务（进阶）
### Neo4j图数据库：
```bash
docker run -d --name nagaai-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest
```

### Twitter API：
创建 .env 文件：
```
TWITTER_CONSUMER_KEY=your_key
TWITTER_CONSUMER_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret
```

## ⚠️ 重要提醒
- 一次只启用一个新功能
- 出现问题立即禁用该功能
- 使用"🚨 紧急停止"按钮控制自主行为
- 定期检查日志和内存使用

## 🆘 如果还有问题
1. 查看 `TROUBLESHOOTING_GUIDE.md`
2. 运行 `python offline_mode_setup.py` 降级到离线模式
3. 检查依赖：`python setup_advanced_features.py`
