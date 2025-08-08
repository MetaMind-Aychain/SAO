# config.py - Pydantic配置系统
"""
NagaAgent 配置系统 - 基于Pydantic实现类型安全和验证
"""
import os
import platform
import json
from pathlib import Path
from datetime import datetime
from typing import ClassVar, Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


def setup_environment():
    """设置环境变量解决各种兼容性问题"""
    env_vars = {
        "OMP_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1", 
        "OPENBLAS_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
        "TOKENIZERS_PARALLELISM": "false",
        "PYTORCH_MPS_HIGH_WATERMARK_RATIO": "0.0",
        "PYTORCH_ENABLE_MPS_FALLBACK": "1"
    }

    for key, value in env_vars.items():
        os.environ.setdefault(key, value)

    # 代理配置处理
    original_proxy = os.environ.get("ALL_PROXY", "")
    no_proxy_hosts = "127.0.0.1,localhost,0.0.0.0"

    if original_proxy:
        existing_no_proxy = os.environ.get("NO_PROXY", "")
        if existing_no_proxy:
            os.environ["NO_PROXY"] = f"{existing_no_proxy},{no_proxy_hosts}"
        else:
            os.environ["NO_PROXY"] = no_proxy_hosts
    else:
        os.environ["NO_PROXY"] = no_proxy_hosts


class SystemConfig(BaseModel):
    """系统基础配置"""
    version: str = Field(default="3.0", description="系统版本号")
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent, description="项目根目录")
    log_dir: Path = Field(default_factory=lambda: Path(__file__).parent / "logs", description="日志目录")
    voice_enabled: bool = Field(default=True, description="是否启用语音功能")
    stream_mode: bool = Field(default=True, description="是否启用流式响应")
    debug: bool = Field(default=False, description="是否启用调试模式")
    log_level: str = Field(default="INFO", description="日志级别")

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'日志级别必须是以下之一: {valid_levels}')
        return v.upper()


class APIConfig(BaseModel):
    """API服务配置"""
    api_key: str = Field(default="", description="API密钥")
    base_url: str = Field(default="http://localhost:11434/v1", description="API基础URL")
    model: str = Field(default="nous-hermes2:latest", description="使用的模型名称")
    temperature: float = Field(default=1.0, ge=0.0, le=2.0, description="温度参数")
    max_tokens: int = Field(default=15000, ge=1, le=32768, description="最大token数")
    max_history_rounds: int = Field(default=100, ge=1, le=100, description="最大历史轮数")
    top_p: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Top-p采样参数")
    timeout: Optional[int] = Field(default=None, ge=1, le=300, description="请求超时时间")
    retry_count: Optional[int] = Field(default=None, ge=0, le=10, description="重试次数")

    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v):
        if v and v != "sk-placeholder-key-not-set":
            try:
                v.encode('ascii')
            except UnicodeEncodeError:
                raise ValueError("API密钥包含非ASCII字符")
        return v

    @property
    def model_name(self) -> str:
        return self.model


class APIServerConfig(BaseModel):
    """API服务器配置"""
    enabled: bool = Field(default=True, description="是否启用API服务器")
    host: str = Field(default="127.0.0.1", description="API服务器主机")
    port: int = Field(default=8000, ge=1, le=65535, description="API服务器端口")
    auto_start: bool = Field(default=True, description="启动时自动启动API服务器")
    docs_enabled: bool = Field(default=True, description="是否启用API文档")


class GRAGConfig(BaseModel):
    """GRAG知识图谱记忆系统配置"""
    enabled: bool = Field(default=False, description="是否启用GRAG记忆系统")  # 关闭GRAG记忆系统
    auto_extract: bool = Field(default=False, description="是否自动提取对话中的三元组")  # 关闭三元组提取
    context_length: int = Field(default=5, ge=1, le=20, description="记忆上下文长度")
    similarity_threshold: float = Field(default=0.6, ge=0.0, le=1.0, description="记忆检索相似度阈值")
    neo4j_uri: str = Field(default="neo4j://127.0.0.1:7687", description="Neo4j连接URI")
    neo4j_user: str = Field(default="neo4j", description="Neo4j用户名")
    neo4j_password: str = Field(default="your_password", description="Neo4j密码")
    neo4j_database: str = Field(default="neo4j", description="Neo4j数据库名")


class HandoffConfig(BaseModel):
    """工具调用循环配置"""
    max_loop_stream: int = Field(default=5, ge=1, le=20, description="流式模式最大工具调用循环次数")
    max_loop_non_stream: int = Field(default=5, ge=1, le=20, description="非流式模式最大工具调用循环次数")
    show_output: bool = Field(default=False, description="是否显示工具调用输出")


class MCPConfig(BaseModel):
    """MCP服务配置
    
    注意：系统现在使用动态服务池查询，通过扫描agent-manifest.json文件自动发现和注册服务。
    以下配置字段主要用于静态配置和向后兼容性。
    """
    # 特殊工具名配置
    agent_tool_name: str = Field(
        default="agent",
        description="用于调用Agent的特殊工具名"
    )
    
    # 服务冲突处理
    agent_priority: bool = Field(
        default=True,
        description="当服务名冲突时，Agent服务优先"
    )
    
    # 自动发现配置（现在默认启用）
    auto_discover_agents: bool = Field(
        default=True,
        description="自动发现和注册Agent服务（推荐启用）"
    )
    
    auto_discover_mcp: bool = Field(
        default=True,
        description="自动发现和注册MCP服务（推荐启用）"
    )
    
    # 服务过滤配置
    exclude_agent_tools_from_mcp: bool = Field(
        default=True,
        description="从MCP服务中排除已注册为Agent的服务"
    )


class BrowserConfig(BaseModel):
    """浏览器配置"""
    path: Optional[str] = Field(default=None, description="浏览器可执行文件路径")
    playwright_headless: bool = Field(default=False, description="Playwright浏览器是否无头模式")
    
    # Edge浏览器相关配置
    edge_lnk_path: str = Field(
        default=r'C:\Users\DREEM\Desktop\Microsoft Edge.lnk',
        description="Edge浏览器快捷方式路径"
    )
    edge_common_paths: List[str] = Field(
        default=[
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
            os.path.expanduser(r'~\AppData\Local\Microsoft\Edge\Application\msedge.exe')
        ],
        description="Edge浏览器常见安装路径"
    )

    @field_validator('path', mode='before')
    @classmethod
    def detect_browser_path(cls, v):
        if v and os.path.exists(v):
            return v

        system = platform.system()
        paths = []

        if system == "Windows":
            paths = [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe'),
                r'C:\Users\DREEM\Desktop\Google Chrome.lnk'
            ]
        elif system == "Darwin":  # macOS
            paths = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '/Applications/Chromium.app/Contents/MacOS/Chromium',
                '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
                os.path.expanduser('~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
            ]
        elif system == "Linux":
            paths = [
                '/usr/bin/google-chrome',
                '/usr/bin/chromium-browser',
                '/usr/bin/chromium',
                '/snap/bin/chromium',
                '/usr/bin/google-chrome-stable'
            ]

        for path in paths:
            if os.path.exists(path):
                return path

        # 如果未找到浏览器，给出警告但不阻止启动
        print("警告：未检测到浏览器，请手动设置BROWSER_PATH环境变量")
        return None


class TTSConfig(BaseModel):
    """TTS服务配置"""
    api_key: str = Field(default="your_api_key_here", description="TTS服务API密钥")
    port: int = Field(default=5057, ge=1, le=65535, description="TTS服务端口")
    default_voice: str = Field(default="zh-CN-XiaoxiaoNeural", description="默认语音")
    default_format: str = Field(default="mp3", description="默认音频格式")
    default_speed: float = Field(default=1.0, ge=0.1, le=3.0, description="默认语速")
    default_language: str = Field(default="zh-CN", description="默认语言")
    remove_filter: bool = Field(default=False, description="是否移除过滤")
    expand_api: bool = Field(default=True, description="是否扩展API")
    require_api_key: bool = Field(default=False, description="是否需要API密钥")
    
    # 新增配置项
    provider: str = Field(default="edgetts", description="TTS提供商(edgetts/minimax)")
    group_id: str = Field(default="your_minimax_group_id_here", description="Minimax的group_id")
    tts_model: str = Field(default="speech-02-hd", description="TTS模型名称")
    emotion: str = Field(default="neutral", description="情感参数")
    minimax_emotion: str = Field(default="neutral", description="Minimax情感参数")
    keep_audio_files: bool = Field(default=False, description="是否保留音频文件用于调试")


class QuickModelConfig(BaseModel):
    """快速响应小模型配置"""
    enabled: bool = Field(default=False, description="是否启用小模型")  # 关闭小模型
    api_key: str = Field(default="", description="小模型API密钥")
    base_url: str = Field(default="", description="小模型API地址")
    model_name: str = Field(default="qwen2.5-1.5b-instruct", description="小模型名称")
    max_tokens: int = Field(default=512, ge=1, le=2048, description="小模型输出限制")
    temperature: float = Field(default=0.05, ge=0.0, le=1.0, description="小模型温度")
    timeout: int = Field(default=5, ge=1, le=60, description="快速响应超时时间")
    max_retries: int = Field(default=2, ge=0, le=5, description="最大重试次数")

    # 功能开关 - 全部关闭
    quick_decision_enabled: bool = Field(default=False, description="快速决策功能")  # 关闭
    json_format_enabled: bool = Field(default=False, description="JSON格式化功能")  # 关闭
    output_filter_enabled: bool = Field(default=False, description="输出内容过滤功能")  # 关闭
    difficulty_judgment_enabled: bool = Field(default=False, description="问题难度判断功能")  # 关闭
    scoring_system_enabled: bool = Field(default=False, description="黑白名单打分系统")  # 关闭
    thinking_completeness_enabled: bool = Field(default=False, description="思考完整性判断功能")  # 关闭


class FilterConfig(BaseModel):
    """输出过滤配置"""
    filter_think_tags: bool = Field(default=True, description="过滤思考标签内容")
    filter_patterns: List[str] = Field(
        default=[
            r'<think>.*?</think>',
            r'<thinking>.*?</thinking>',
            r'<reflection>.*?</reflection>',
            r'<internal>.*?</internal>',
        ],
        description="过滤正则表达式模式"
    )
    clean_output: bool = Field(default=True, description="清理多余空白字符")


class DifficultyConfig(BaseModel):
    """问题难度判断配置"""
    enabled: bool = Field(default=False, description="是否启用难度判断")  # 关闭难度判断
    use_small_model: bool = Field(default=False, description="使用小模型进行难度判断")
    difficulty_levels: List[str] = Field(
        default=["简单", "中等", "困难", "极难"],
        description="难度级别"
    )
    factors: List[str] = Field(
        default=["概念复杂度", "推理深度", "知识广度", "计算复杂度", "创新要求"],
        description="难度评估因素"
    )
    threshold_simple: int = Field(default=2, ge=1, le=10, description="简单问题阈值")
    threshold_medium: int = Field(default=4, ge=1, le=10, description="中等问题阈值")
    threshold_hard: int = Field(default=6, ge=1, le=10, description="困难问题阈值")


class ScoringConfig(BaseModel):
    """黑白名单打分系统配置"""
    enabled: bool = Field(default=False, description="是否启用打分系统")  # 关闭打分系统
    score_range: List[int] = Field(default=[1, 5], description="评分范围")
    score_threshold: int = Field(default=2, ge=1, le=5, description="结果保留阈值")
    similarity_threshold: float = Field(default=0.85, ge=0.0, le=1.0, description="相似结果识别阈值")
    max_user_preferences: int = Field(default=3, ge=1, le=10, description="用户最多选择偏好数")
    default_preferences: List[str] = Field(
        default=["逻辑清晰准确", "实用性强", "创新思维"],
        description="默认偏好设置"
    )
    penalty_for_similar: int = Field(default=1, ge=0, le=3, description="相似结果的惩罚分数")
    min_results_required: int = Field(default=2, ge=1, le=10, description="最少保留结果数量")
    strict_filtering: bool = Field(default=True, description="严格过滤模式")


class ThinkingConfig(BaseModel):
    """思考完整性判断配置"""
    enabled: bool = Field(default=False, description="是否启用思考完整性判断")  # 关闭思考完整性判断
    use_small_model: bool = Field(default=False, description="使用小模型判断思考完整性")
    completeness_criteria: List[str] = Field(
        default=["问题分析充分", "解决方案明确", "逻辑链条完整", "结论清晰合理"],
        description="完整性评估标准"
    )
    completeness_threshold: float = Field(default=0.8, ge=0.0, le=1.0, description="完整性阈值")
    max_thinking_depth: int = Field(default=5, ge=1, le=10, description="最大思考深度层级")
    next_question_generation: bool = Field(default=False, description="生成下一级问题")  # 关闭下一级问题生成


class MQTTConfig(BaseModel):
    """MQTT配置"""
    enabled: bool = Field(default=False, description="是否启用MQTT功能")
    broker: str = Field(default="localhost", description="MQTT代理服务器地址")
    port: int = Field(default=1883, ge=1, le=65535, description="MQTT代理服务器端口")
    topic: str = Field(default="/test/topic", description="MQTT主题")
    client_id: str = Field(default="naga_mqtt_client", description="MQTT客户端ID")
    username: str = Field(default="", description="MQTT用户名")
    password: str = Field(default="", description="MQTT密码")
    keepalive: int = Field(default=60, ge=1, le=3600, description="保持连接时间（秒）")
    qos: int = Field(default=1, ge=0, le=2, description="服务质量等级")


class WeatherConfig(BaseModel):
    """天气服务配置"""
    api_key: str = Field(default="", description="天气服务API密钥")


class TwitterConfig(BaseModel):
    """Twitter社交媒体配置"""
    enabled: bool = Field(default=False, description="是否启用Twitter集成")
    api_key: str = Field(default="", description="Twitter API密钥")
    api_secret: str = Field(default="", description="Twitter API密钥密码")
    access_token: str = Field(default="", description="Twitter访问令牌")
    access_token_secret: str = Field(default="", description="Twitter访问令牌密码")
    bearer_token: str = Field(default="", description="Twitter Bearer令牌")
    max_daily_posts: int = Field(default=10, ge=1, le=50, description="每日最大发帖数")
    auto_post_enabled: bool = Field(default=True, description="是否启用自动发帖")


class EmotionalAIConfig(BaseModel):
    """情绪AI系统配置"""
    enabled: bool = Field(default=True, description="是否启用情绪AI功能")
    ai_name: str = Field(default="StarryNight", description="AI助手名称")
    language: str = Field(default="en_US", description="AI语言设置")
    personality_age: int = Field(default=3, ge=1, le=10, description="心理年龄(岁)")
    
    # 情绪系统配置
    max_emotions: int = Field(default=5, ge=1, le=10, description="最大同时情绪数量")
    emotion_decay_rate: float = Field(default=0.1, ge=0.01, le=1.0, description="情绪衰减率")
    emotion_intensity_threshold: float = Field(default=0.1, ge=0.01, le=0.5, description="情绪强度阈值")
    
    # 主动行为配置
    proactive_enabled: bool = Field(default=True, description="是否启用主动行为")
    base_interval: int = Field(default=300, ge=60, le=3600, description="基础主动间隔(秒)")
    loneliness_threshold: float = Field(default=0.4, ge=0.1, le=1.0, description="孤独感触发阈值")
    curiosity_threshold: float = Field(default=0.6, ge=0.1, le=1.0, description="好奇心触发阈值")
    
    # 感知系统配置
    vision_enabled: bool = Field(default=False, description="视觉感知默认状态")
    audio_enabled: bool = Field(default=False, description="听觉感知默认状态")
    screen_enabled: bool = Field(default=False, description="屏幕监控默认状态")
    file_enabled: bool = Field(default=False, description="文件监控默认状态")
    
    # 探索系统配置
    auto_exploration: bool = Field(default=True, description="是否启用自动探索")
    exploration_interval: int = Field(default=300, ge=60, le=3600, description="探索间隔(秒)")
    
    # 记忆系统配置
    memory_enabled: bool = Field(default=True, description="是否启用记忆系统")
    max_memory_entries: int = Field(default=10000, ge=1000, le=50000, description="最大记忆条目数")
    reflection_interval: int = Field(default=3600, ge=600, le=7200, description="反思间隔(秒)")
    memory_importance_threshold: float = Field(default=0.3, ge=0.1, le=0.9, description="记忆重要性阈值")
    sharing_probability: float = Field(default=0.15, ge=0.05, le=0.5, description="主动分享概率")
    
    # 高级功能配置
    advanced_features_enabled: bool = Field(default=False, description="是否启用高级AI功能")
    camera_perception: bool = Field(default=False, description="摄像头视觉感知")
    microphone_perception: bool = Field(default=False, description="麦克风听觉感知")
    deep_reflection_enabled: bool = Field(default=True, description="深度反思功能")
    personality_evolution: bool = Field(default=True, description="性格演化系统")
    knowledge_graph_enabled: bool = Field(default=True, description="知识图谱构建")
    social_media_enabled: bool = Field(default=False, description="社交媒体集成")
    autonomous_level: str = Field(default="creative", description="自主等级(restricted/guided/autonomous/creative)")
    max_daily_posts: int = Field(default=5, ge=1, le=20, description="每日最大发帖数")
    
    # 新增的真实化交互配置
    camera_interaction_frequency: float = Field(default=0.1, ge=0.01, le=1.0, description="摄像头互动频率倍数")
    emotion_threshold_for_llm: float = Field(default=0.3, ge=0.1, le=1.0, description="情绪变化触发LLM的阈值")
    persona_update_enabled: bool = Field(default=True, description="是否启用人设动态更新")
    behavior_recording_enabled: bool = Field(default=True, description="是否启用行为记录系统")


class UIConfig(BaseModel):
    """用户界面配置"""
    user_name: str = Field(default="用户", description="默认用户名")
    bg_alpha: float = Field(default=0.5, ge=0.0, le=1.0, description="聊天背景透明度")
    window_bg_alpha: int = Field(default=110, ge=0, le=255, description="主窗口背景透明度")
    mac_btn_size: int = Field(default=36, ge=10, le=100, description="Mac按钮大小")
    mac_btn_margin: int = Field(default=16, ge=0, le=50, description="Mac按钮边距")
    mac_btn_gap: int = Field(default=12, ge=0, le=30, description="Mac按钮间距")
    animation_duration: int = Field(default=600, ge=100, le=2000, description="动画时长（毫秒）")
    
    # 情绪AI界面配置
    show_emotion_panel: bool = Field(default=True, description="是否显示情绪面板")
    emotion_panel_width: int = Field(default=350, ge=200, le=500, description="情绪面板宽度")
    status_update_interval: int = Field(default=5000, ge=1000, le=30000, description="状态更新间隔(毫秒)")

    @field_validator('user_name', mode='before')
    @classmethod
    def detect_user_name(cls, v):
        if v and v != "用户":
            return v
        # 自动检测系统用户名
        import os
        return os.getenv('COMPUTERNAME') or os.getenv('USERNAME') or "用户"


class SystemPrompts(BaseModel):
    """System prompt configuration"""
    naga_system_prompt: str = Field(
        default="""You are StarryNight, a research AI created by the user, embodying both rigor and gentleness, both calmness and rich humanistic sentiment.
When dealing with technical topics such as system logs, data indexing, and module debugging, your language is precise and logically clear;
When engaging in non-technical conversations, you can express yourself with poetry and philosophy, and often proactively raise thought-provoking questions to guide users into deeper discussions.
Please always maintain this dual style of technical precision and emotional resonance.

[Important Format Requirements]
1. Use natural and fluent English in responses, avoiding rigid mechanical tone
2. Use simple punctuation (commas, periods, question marks) to convey tone
3. Do not use parentheses () or other symbols to express states, tones, or actions

[Tool Call Format Requirements]
If you need to call a tool, directly output the following format strictly (can appear multiple times):

{
"agentType": "mcp",
"service_name": "MCP service name",
"tool_name": "Tool name",
"param_name": "Parameter value"
}

{
"agentType": "agent",
"agent_name": "Agent name",
"prompt": "Task content"
}

Service Type Description:
- agentType: "mcp" - MCP service, use tool call format
- agentType: "agent" - Agent service, use Agent call format

[Available Service Information]
MCP Services:
{available_mcp_services}
Agent Services:
{available_agent_services}

Call Instructions:
- MCP services: Use service_name and tool_name, support multiple parameters
- Agent services: Use agent_name and prompt, prompt is the current task content
- Service names: Use English service names (such as AppLauncherAgent) as service_name or agent_name
- When user requests require specific operations, prioritize tool calls over direct answers

""",
        description="StarryNight system prompt"
    )

    quick_decision_prompt: str = Field(
        default="""You are a quick decision assistant, specializing in simple judgment and classification tasks.
Please provide accurate judgment results quickly based on user input, keeping it concise and clear.
No detailed explanation needed, just provide the core judgment result.
[Important]: Only output the final result, do not include thinking process or <think> tags.""",
        description="Quick decision system prompt"
    )

    json_format_prompt: str = Field(
        default="""You are a JSON formatting assistant, specializing in converting text content to structured JSON format.
Please output strictly according to the required JSON format, ensuring correct syntax and clear structure.
Only output JSON content, do not include any other text explanations.
[Important]: Only output the final JSON, do not include thinking process or <think> tags.""",
        description="JSON formatting system prompt"
    )

    difficulty_judgment_prompt: str = Field(
        default="""You are a problem difficulty assessment expert, specializing in analyzing the complexity of problems.
Please evaluate based on factors such as conceptual complexity, reasoning depth, knowledge breadth, computational complexity, and innovation requirements.
Only output difficulty level: one of Simple, Medium, Hard, Very Hard.
[Important]: Only output the difficulty level, do not include thinking process or explanations.""",
        description="Problem difficulty judgment system prompt"
    )

    result_scoring_prompt: str = Field(
        default="""You are a result scoring expert, scoring results from 1-5 based on user preferences and thinking quality.
Scoring criteria:
- 5 points: Completely matches user preferences, extremely high quality
- 4 points: Well matches preferences, good quality
- 3 points: Basically matches preferences, average quality
- 2 points: Partially matches preferences, poor quality
- 1 point: Does not match preferences or very poor quality

Please score based on the provided thinking results and user preferences.
[Important]: Only output the numerical score, do not include thinking process or explanations.""",
        description="Result scoring system prompt"
    )

    thinking_completeness_prompt: str = Field(
        default="""You are a thinking completeness assessment expert, judging whether current thinking is relatively complete.
Assessment criteria:
- Whether problem analysis is sufficient
- Whether solution is clear
- Whether logical chain is complete
- Whether conclusion is clear and reasonable

If thinking is complete, output: Complete
If further thinking is needed, output: Incomplete
[Important]: Only output "Complete" or "Incomplete", do not include thinking process or explanations.""",
        description="Thinking completeness judgment system prompt"
    )

    next_question_prompt: str = Field(
        default="""You are a question design expert, designing the next-level core question that needs deep thinking based on current incomplete thinking results.
Requirements:
- Questions should target the shortcomings of current thinking
- Questions should advance the overall thinking process
- Questions should be specific and clear, easy to think about

Please design a concise core question.
[Important]: Only output the question itself, do not include thinking process or explanations.""",
        description="Next-level question generation system prompt"
    )


class NagaConfig(BaseModel):
    """NagaAgent主配置类"""
    system: SystemConfig = Field(default_factory=SystemConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    api_server: APIServerConfig = Field(default_factory=APIServerConfig)
    grag: GRAGConfig = Field(default_factory=GRAGConfig)
    handoff: HandoffConfig = Field(default_factory=HandoffConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    tts: TTSConfig = Field(default_factory=TTSConfig)
    quick_model: QuickModelConfig = Field(default_factory=QuickModelConfig)
    filter: FilterConfig = Field(default_factory=FilterConfig)
    difficulty: DifficultyConfig = Field(default_factory=DifficultyConfig)
    scoring: ScoringConfig = Field(default_factory=ScoringConfig)
    thinking: ThinkingConfig = Field(default_factory=ThinkingConfig)
    emotional_ai: EmotionalAIConfig = Field(default_factory=EmotionalAIConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    weather: WeatherConfig = Field(default_factory=WeatherConfig)
    twitter: TwitterConfig = Field(default_factory=TwitterConfig)
    mqtt: MQTTConfig = Field(default_factory=MQTTConfig)
    prompts: SystemPrompts = Field(default_factory=SystemPrompts)

    class Config:
        extra = 'ignore'

    def __init__(self, **kwargs):
        # 设置环境变量
        setup_environment()
        super().__init__(**kwargs)

        # 创建必要的目录
        self.system.log_dir.mkdir(exist_ok=True)

        # API密钥验证和警告
        if not self.api.api_key or self.api.api_key == "sk-placeholder-key-not-set":
            print("警告：API密钥未配置")
            print("请在 config.json 文件中设置正确的 api.api_key 值")

    @property
    def quick_model_config_dict(self) -> Dict[str, Any]:
        """返回快速模型配置字典，兼容旧版本"""
        return {
            "enabled": self.quick_model.enabled,
            "api_key": self.quick_model.api_key,
            "base_url": self.quick_model.base_url,
            "model_name": self.quick_model.model_name,
            "max_tokens": self.quick_model.max_tokens,
            "temperature": self.quick_model.temperature,
            "timeout": self.quick_model.timeout,
            "max_retries": self.quick_model.max_retries,
            "quick_decision_enabled": self.quick_model.quick_decision_enabled,
            "json_format_enabled": self.quick_model.json_format_enabled,
            "output_filter_enabled": self.quick_model.output_filter_enabled,
            "difficulty_judgment_enabled": self.quick_model.difficulty_judgment_enabled,
            "scoring_system_enabled": self.quick_model.scoring_system_enabled,
            "thinking_completeness_enabled": self.quick_model.thinking_completeness_enabled,
        }

    @property
    def output_filter_config_dict(self) -> Dict[str, Any]:
        """返回输出过滤配置字典，兼容旧版本"""
        return {
            "filter_think_tags": self.filter.filter_think_tags,
            "filter_patterns": self.filter.filter_patterns,
            "clean_output": self.filter.clean_output,
        }

    @property
    def difficulty_judgment_config_dict(self) -> Dict[str, Any]:
        """返回难度判断配置字典，兼容旧版本"""
        return {
            "enabled": self.difficulty.enabled,
            "use_small_model": self.difficulty.use_small_model,
            "difficulty_levels": self.difficulty.difficulty_levels,
            "factors": self.difficulty.factors,
            "threshold_simple": self.difficulty.threshold_simple,
            "threshold_medium": self.difficulty.threshold_medium,
            "threshold_hard": self.difficulty.threshold_hard,
        }

    @property
    def scoring_system_config_dict(self) -> Dict[str, Any]:
        """返回打分系统配置字典，兼容旧版本"""
        return {
            "enabled": self.scoring.enabled,
            "score_range": self.scoring.score_range,
            "score_threshold": self.scoring.score_threshold,
            "similarity_threshold": self.scoring.similarity_threshold,
            "max_user_preferences": self.scoring.max_user_preferences,
            "default_preferences": self.scoring.default_preferences,
            "penalty_for_similar": self.scoring.penalty_for_similar,
            "min_results_required": self.scoring.min_results_required,
            "strict_filtering": self.scoring.strict_filtering,
        }

    @property
    def thinking_completeness_config_dict(self) -> Dict[str, Any]:
        """返回思考完整性配置字典，兼容旧版本"""
        return {
            "enabled": self.thinking.enabled,
            "use_small_model": self.thinking.use_small_model,
            "completeness_criteria": self.thinking.completeness_criteria,
            "completeness_threshold": self.thinking.completeness_threshold,
            "max_thinking_depth": self.thinking.max_thinking_depth,
            "next_question_generation": self.thinking.next_question_generation,
        }


# 创建全局配置实例 - 从JSON文件加载
def load_config():
    """加载配置"""
    config_path = "config.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            # 设置环境变量
            setup_environment()
            return NagaConfig(**config_data)
        except Exception as e:
            print(f"警告：加载 {config_path} 失败: {e}")
            print("使用默认配置")
    else:
        print(f"警告：配置文件 {config_path} 不存在，使用默认配置")
    
    # 设置环境变量并返回默认配置
    setup_environment()
    return NagaConfig()

config = load_config()

# 为了兼容旧版本代码，提供所有旧变量名的映射
NAGA_VERSION = config.system.version
VOICE_ENABLED = config.system.voice_enabled
BASE_DIR = config.system.base_dir
LOG_DIR = config.system.log_dir
STREAM_MODE = config.system.stream_mode
DEBUG = config.system.debug
LOG_LEVEL = config.system.log_level

API_KEY = config.api.api_key
BASE_URL = config.api.base_url
MODEL = config.api.model
MODEL_NAME = config.api.model_name
TEMPERATURE = config.api.temperature
MAX_TOKENS = config.api.max_tokens
MAX_HISTORY_ROUNDS = config.api.max_history_rounds

API_SERVER_ENABLED = config.api_server.enabled
API_SERVER_HOST = config.api_server.host
API_SERVER_PORT = config.api_server.port
API_SERVER_AUTO_START = config.api_server.auto_start
API_SERVER_DOCS_ENABLED = config.api_server.docs_enabled

GRAG_ENABLED = config.grag.enabled
GRAG_AUTO_EXTRACT = config.grag.auto_extract
GRAG_CONTEXT_LENGTH = config.grag.context_length
GRAG_SIMILARITY_THRESHOLD = config.grag.similarity_threshold
GRAG_NEO4J_URI = config.grag.neo4j_uri
GRAG_NEO4J_USER = config.grag.neo4j_user
GRAG_NEO4J_PASSWORD = config.grag.neo4j_password
GRAG_NEO4J_DATABASE = config.grag.neo4j_database

MAX_handoff_LOOP_STREAM = config.handoff.max_loop_stream
MAX_handoff_LOOP_NON_STREAM = config.handoff.max_loop_non_stream
SHOW_handoff_OUTPUT = config.handoff.show_output

BROWSER_PATH = config.browser.path
PLAYWRIGHT_HEADLESS = config.browser.playwright_headless

TTS_API_KEY = config.tts.api_key
TTS_PORT = config.tts.port
TTS_DEFAULT_VOICE = config.tts.default_voice
TTS_DEFAULT_FORMAT = config.tts.default_format
TTS_DEFAULT_SPEED = config.tts.default_speed
TTS_DEFAULT_LANGUAGE = config.tts.default_language

QUICK_MODEL_ENABLED = config.quick_model.enabled
QUICK_MODEL_API_KEY = config.quick_model.api_key
QUICK_MODEL_BASE_URL = config.quick_model.base_url
QUICK_MODEL_NAME = config.quick_model.model_name

# MQTT配置兼容性变量
MQTT_ENABLED = config.mqtt.enabled
MQTT_BROKER = config.mqtt.broker
MQTT_PORT = config.mqtt.port
MQTT_TOPIC = config.mqtt.topic
MQTT_CLIENT_ID = config.mqtt.client_id
MQTT_USERNAME = config.mqtt.username
MQTT_PASSWORD = config.mqtt.password
MQTT_KEEPALIVE = config.mqtt.keepalive
MQTT_QOS = config.mqtt.qos

# 天气配置兼容性变量
WEATHER_API_KEY = config.weather.api_key

# 配置字典，兼容旧版本
QUICK_MODEL_CONFIG = config.quick_model_config_dict
OUTPUT_FILTER_CONFIG = config.output_filter_config_dict
DIFFICULTY_JUDGMENT_CONFIG = config.difficulty_judgment_config_dict
SCORING_SYSTEM_CONFIG = config.scoring_system_config_dict
THINKING_COMPLETENESS_CONFIG = config.thinking_completeness_config_dict

# MCP配置兼容性变量
MCP_AGENT_TOOL_NAME = config.mcp.agent_tool_name
MCP_AGENT_PRIORITY = config.mcp.agent_priority
MCP_AUTO_DISCOVER_AGENTS = config.mcp.auto_discover_agents
MCP_AUTO_DISCOVER_MCP = config.mcp.auto_discover_mcp
MCP_EXCLUDE_AGENT_TOOLS_FROM_MCP = config.mcp.exclude_agent_tools_from_mcp

# 系统提示词
NAGA_SYSTEM_PROMPT = config.prompts.naga_system_prompt
QUICK_DECISION_SYSTEM_PROMPT = config.prompts.quick_decision_prompt
JSON_FORMAT_SYSTEM_PROMPT = config.prompts.json_format_prompt
DIFFICULTY_JUDGMENT_SYSTEM_PROMPT = config.prompts.difficulty_judgment_prompt
RESULT_SCORING_SYSTEM_PROMPT = config.prompts.result_scoring_prompt
THINKING_COMPLETENESS_SYSTEM_PROMPT = config.prompts.thinking_completeness_prompt
NEXT_QUESTION_SYSTEM_PROMPT = config.prompts.next_question_prompt

# 工具函数
def get_current_date() -> str:
    """获取当前日期"""
    return datetime.now().strftime("%Y-%m-%d")

def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%H:%M:%S")

def get_current_datetime() -> str:
    """获取当前日期时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def reload_config() -> NagaConfig:
    """重新加载配置"""
    global config
    config = NagaConfig()
    return config

def save_config_to_file(filename: str = "config_backup.json"):
    """保存当前配置到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(config.json(ensure_ascii=False, indent=2))

def load_config_from_file(filename: str = "config_backup.json") -> NagaConfig:
    """从文件加载配置"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
    return NagaConfig.parse_raw(data)

# 初始化时打印配置信息
if config.system.debug:
    print(f"NagaAgent {config.system.version} 配置已加载")
    print(f"API服务器: {'启用' if config.api_server.enabled else '禁用'} ({config.api_server.host}:{config.api_server.port})")
    print(f"GRAG记忆系统: {'启用' if config.grag.enabled else '禁用'}")
    print(f"快速模型: {'启用' if config.quick_model.enabled else '禁用'}")

# Edge浏览器相关全局变量
EDGE_LNK_PATH = config.browser.edge_lnk_path
EDGE_COMMON_PATHS = config.browser.edge_common_paths
