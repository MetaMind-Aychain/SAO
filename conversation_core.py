import logging
import os
# import asyncio # 日志与系统
from datetime import datetime # 时间
from mcpserver.mcp_manager import get_mcp_manager # 多功能管理
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX # handoff提示词
# from mcpserver.agent_playwright_master import ControllerAgent, BrowserAgent, ContentAgent # 导入浏览器相关类
from openai import OpenAI,AsyncOpenAI # LLM
# import difflib # 模糊匹配
import sys
import json
import traceback
import time # 时间戳打印
import re # 添加re模块导入
from typing import List, Dict # 修复List未导入
# 恢复树状思考系统导入
from thinking import TreeThinkingEngine # 树状思考引擎
from thinking.config import COMPLEX_KEYWORDS # 复杂关键词
from config import config
# 导入独立的工具调用模块
from apiserver.tool_call_utils import parse_tool_calls, execute_tool_calls, tool_call_loop
# 导入情绪AI核心
from emotional_ai_core import get_emotion_core

# 导入动态发布器
try:
    from ai_dynamic_publisher import (
        publish_thinking, 
        publish_manual_dynamic,
        ai_dynamic_publisher
    )
    DYNAMIC_PUBLISHER_AVAILABLE = True
except ImportError:
    DYNAMIC_PUBLISHER_AVAILABLE = False

# GRAG记忆系统导入
if config.grag.enabled:
    try:
        from summer_memory.memory_manager import memory_manager
    except Exception as e:
        logger = logging.getLogger("NagaConversation")
        logger.error(f"夏园记忆系统加载失败: {e}")
        memory_manager = None
else:
    memory_manager = None

def now():
    return time.strftime('%H:%M:%S:')+str(int(time.time()*1000)%10000) # 当前时间
_builtin_print=print
def print(*a, **k):
    return sys.stderr.write('[print] '+(' '.join(map(str,a)))+'\n')

# 配置日志 - 使用统一配置系统的日志级别
log_level = getattr(logging, config.system.log_level.upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)

# 特别设置httpcore和openai的日志级别，减少连接异常噪音
logging.getLogger("httpcore.connection").setLevel(logging.WARNING)
logging.getLogger("httpcore.http11").setLevel(logging.WARNING)  # 屏蔽HTTP请求DEBUG
logging.getLogger("httpx").setLevel(logging.WARNING)  # 屏蔽httpx DEBUG
logging.getLogger("openai._base_client").setLevel(logging.WARNING)
# 隐藏asyncio的DEBUG日志
logging.getLogger("asyncio").setLevel(logging.WARNING)
logger = logging.getLogger("NagaConversation")

# _MCP_HANDOFF_REGISTERED=False  # 已移除，不再需要
_TREE_THINKING_SUBSYSTEMS_INITIALIZED=False
_MCP_SERVICES_INITIALIZED=False
_QUICK_MODEL_MANAGER_INITIALIZED=False
_VOICE_ENABLED_LOGGED=False

class NagaConversation: # 对话主类
    def __init__(self):
        self.mcp = get_mcp_manager()
        self.messages = []
        self.dev_mode = False
        
        # 检测演示模式
        self.demo_mode = os.getenv("NAGAAGENT_DEMO_MODE") == "1" or config.api.api_key == "demo-mode"
        
        if self.demo_mode:
            logger.info("🎭 演示模式已启用 - 使用预设响应")
            self.client = None
            self.async_client = None
            # 导入演示对话模块
            try:
                from demo_conversation import get_demo_response
                self.demo_response_func = get_demo_response
            except ImportError:
                logger.warning("演示对话模块未找到，使用内置响应")
                self.demo_response_func = self._builtin_demo_response
        else:
            self.client = OpenAI(api_key=config.api.api_key, base_url=config.api.base_url.rstrip('/') + '/')
            self.async_client = AsyncOpenAI(api_key=config.api.api_key, base_url=config.api.base_url.rstrip('/') + '/')
        
        # 初始化MCP服务系统
        self._init_mcp_services()
        
        # 初始化GRAG记忆系统（只在首次初始化时显示日志）
        self.memory_manager = memory_manager
        if self.memory_manager and not hasattr(self.__class__, '_memory_initialized'):
            logger.info("夏园记忆系统已初始化")
            self.__class__._memory_initialized = True
        
        # 初始化语音处理系统
        self.voice = None
        if config.system.voice_enabled:
            try:
                # 语音功能已迁移到voice_integration.py，由ui/enhanced_worker.py调用
                # 不再需要在这里初始化VoiceHandler
                # 使用全局变量避免重复输出日志
                global _VOICE_ENABLED_LOGGED
                if not _VOICE_ENABLED_LOGGED:
                    logger.info("语音功能已启用，由UI层管理")
                    _VOICE_ENABLED_LOGGED = True
            except Exception as e:
                logger.warning(f"语音系统初始化失败: {e}")
                self.voice = None
        
        # 恢复树状思考系统
        self.tree_thinking = None
        # 集成树状思考系统（参考handoff的全局变量保护机制）
        global _TREE_THINKING_SUBSYSTEMS_INITIALIZED
        if not _TREE_THINKING_SUBSYSTEMS_INITIALIZED:
            try:
                self.tree_thinking = TreeThinkingEngine(api_client=self, memory_manager=self.memory_manager)
                print("[TreeThinkingEngine] ✅ 树状外置思考系统初始化成功")
                _TREE_THINKING_SUBSYSTEMS_INITIALIZED = True
            except Exception as e:
                logger.warning(f"树状思考系统初始化失败: {e}")
                self.tree_thinking = None
        else:
            # 如果子系统已经初始化过，创建新实例但不重新初始化子系统（静默处理）
            try:
                self.tree_thinking = TreeThinkingEngine(api_client=self, memory_manager=self.memory_manager)
            except Exception as e:
                logger.warning(f"树状思考系统实例创建失败: {e}")
                self.tree_thinking = None
        
        # 初始化快速模型管理器（用于异步思考判断）
        self.quick_model_manager = None
        # 集成快速模型管理器（参考树状思考的全局变量保护机制）
        global _QUICK_MODEL_MANAGER_INITIALIZED
        if not _QUICK_MODEL_MANAGER_INITIALIZED:
            try:
                from thinking.quick_model_manager import QuickModelManager
                self.quick_model_manager = QuickModelManager()
                logger.info("快速模型管理器初始化成功")
                _QUICK_MODEL_MANAGER_INITIALIZED = True
            except Exception as e:
                logger.debug(f"快速模型管理器初始化失败: {e}")
                self.quick_model_manager = None
        else:
            # 如果已经初始化过，创建新实例但不重新初始化（静默处理）
            try:
                from thinking.quick_model_manager import QuickModelManager
                self.quick_model_manager = QuickModelManager()
            except Exception as e:
                logger.debug(f"快速模型管理器实例创建失败: {e}")
                self.quick_model_manager = None
        
        # 初始化情绪AI系统
        self.emotional_ai = None
        if config.emotional_ai.enabled:
            try:
                self.emotional_ai = get_emotion_core(config)
                
                # 添加主动对话回调
                def handle_proactive_message(message):
                    """处理主动对话消息"""
                    try:
                        # 这里可以发送到UI或记录日志
                        emotion_display = self.emotional_ai.get_emotion_display()
                        logger.info(f"[{config.emotional_ai.ai_name}] {message} [{emotion_display}]")
                        
                        # 如果有UI回调，可以在这里调用
                        if hasattr(self, '_ui_callback') and self._ui_callback:
                            self._ui_callback(f"🤖 {config.emotional_ai.ai_name}: {message}")
                    except Exception as e:
                        logger.error(f"处理主动消息失败: {e}")
                
                self.emotional_ai.add_proactive_callback(handle_proactive_message)
                logger.info(f"情绪AI系统已初始化 - {config.emotional_ai.ai_name} ({config.emotional_ai.personality_age}岁)")
            except Exception as e:
                logger.warning(f"情绪AI系统初始化失败: {e}")
                self.emotional_ai = None
    
    def _builtin_demo_response(self, user_input: str, emotion_state=None) -> str:
        """内置演示响应"""
        import random
        
        responses = {
            "你好": ["你好呀！我是StarryNight！😊", "嗨～很高兴见到你！"],
            "再见": ["再见～记得常来陪我哦！", "拜拜！我会想你的！"],
            "你真棒": ["谢谢夸奖！我好开心！😊", "嘻嘻，你也很棒呀！"],
            "为什么": ["这是个好问题！🤔", "让我想想...为什么呢？"],
            "游戏": ["我们玩什么游戏呢？🤩", "游戏！我最喜欢了！"],
            "test": ["演示模式运行正常！✅", "测试成功～我在这里呢！"]
        }
        
        # 关键词匹配
        for keyword, resp_list in responses.items():
            if keyword in user_input:
                return random.choice(resp_list)
        
        # 默认响应
        default_responses = [
            "我在这里呢！有什么可以帮你的吗？",
            "让我想想怎么回答...",
            "嗯嗯，我听着呢～",
            "这个话题真有趣！",
            "我正在学习中...✨"
        ]
        
        return random.choice(default_responses)

    def set_ui_callback(self, callback):
        """设置UI回调函数"""
        self._ui_callback = callback
    
    def get_emotional_status(self):
        """获取情绪状态"""
        if self.emotional_ai:
            return self.emotional_ai.get_emotion_status()
        return None
    
    def _init_mcp_services(self):
        """初始化MCP服务系统（只在首次初始化时输出日志，后续静默）"""
        global _MCP_SERVICES_INITIALIZED
        if _MCP_SERVICES_INITIALIZED:
            # 静默跳过，不输出任何日志
            return
        try:
            # 自动注册所有MCP服务和handoff
            self.mcp.auto_register_services()
            logger.info("MCP服务系统初始化完成")
            _MCP_SERVICES_INITIALIZED = True
        except Exception as e:
            logger.error(f"MCP服务系统初始化失败: {e}")

    def save_log(self, u, a):  # 保存对话日志
        if self.dev_mode:
            return  # 开发者模式不写日志
        d = datetime.now().strftime('%Y-%m-%d')
        t = datetime.now().strftime('%H:%M:%S')
        
        # 确保日志目录存在
        log_dir = config.system.log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            logger.info(f"已创建日志目录: {log_dir}")
        
        f = os.path.join(log_dir, f'{d}.txt')
        with open(f, 'a', encoding='utf-8') as w:
            w.write('-'*50 + f'\n时间: {d} {t}\n用户: {u}\nStarryNight: {a}\n\n')

    async def _call_llm(self, messages: List[Dict]) -> Dict:
        """调用LLM API"""
        try:
            resp = await self.async_client.chat.completions.create(
                model=config.api.model, 
                messages=messages, 
                temperature=config.api.temperature, 
                max_tokens=config.api.max_tokens, 
                stream=False  # 工具调用循环中不使用流式
            )
            return {
                'content': resp.choices[0].message.content,
                'status': 'success'
            }
        except RuntimeError as e:
            if "handler is closed" in str(e):
                logger.debug(f"忽略连接关闭异常: {e}")
                # 重新创建客户端并重试
                self.async_client = AsyncOpenAI(api_key=config.api.api_key, base_url=config.api.base_url.rstrip('/') + '/')
                resp = await self.async_client.chat.completions.create(
                    model=config.api.model, 
                    messages=messages, 
                    temperature=config.api.temperature, 
                    max_tokens=config.api.max_tokens, 
                    stream=False
                )
                return {
                    'content': resp.choices[0].message.content,
                    'status': 'success'
                }
            else:
                raise
        except Exception as e:
            logger.error(f"LLM API调用失败: {e}")
            return {
                'content': f"API调用失败: {str(e)}",
                'status': 'error'
            }

    # 工具调用循环相关方法
    def handle_llm_response(self, a, mcp):
        # 只保留普通文本流式输出逻辑 #
        async def text_stream():
            for line in a.splitlines():
                yield ("StarryNight", line)
        return text_stream()

    def _format_services_for_prompt(self, available_services: dict) -> str:
        """格式化可用服务列表为prompt字符串，MCP服务和Agent服务分开，包含具体调用格式"""
        mcp_services = available_services.get("mcp_services", [])
        agent_services = available_services.get("agent_services", [])
        
        # 获取本地城市信息和当前时间
        local_city = "未知城市"
        current_time = ""
        try:
            # 从WeatherTimeAgent获取本地城市信息
            from mcpserver.agent_weather_time.agent_weather_time import WeatherTimeTool
            weather_tool = WeatherTimeTool()
            local_city = getattr(weather_tool, '_local_city', '未知城市') or '未知城市'
            
            # 获取当前时间
            from datetime import datetime
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"[DEBUG] 获取本地信息失败: {e}")
        
        # 格式化MCP服务列表，包含具体调用格式
        mcp_list = []
        for service in mcp_services:
            name = service.get("name", "")
            description = service.get("description", "")
            display_name = service.get("display_name", name)
            tools = service.get("available_tools", [])
            
            # 展示name+displayName
            if description:
                mcp_list.append(f"- {name}: {description}")
            else:
                mcp_list.append(f"- {name}")
            
            # 为每个工具显示具体调用格式
            if tools:
                for tool in tools:
                    tool_name = tool.get('name', '')
                    tool_desc = tool.get('description', '')
                    tool_example = tool.get('example', '')
                    
                    if tool_name and tool_example:
                        # 解析示例JSON，提取参数
                        try:
                            import json
                            example_data = json.loads(tool_example)
                            params = []
                            for key, value in example_data.items():
                                if key != 'tool_name':
                                    # 特殊处理city参数，注入本地城市信息
                                    if key == 'city' and name == 'WeatherTimeAgent':
                                        params.append(f"{key}: {local_city}")
                                    else:
                                        params.append(f"{key}: {value}")
                            
                            # 构建调用格式
                            format_str = f"  {tool_name}: ｛\n"
                            format_str += f"    \"agentType\": \"mcp\",\n"
                            format_str += f"    \"service_name\": \"{name}\",\n"
                            format_str += f"    \"tool_name\": \"{tool_name}\",\n"
                            for param in params:
                                # 将中文参数名转换为英文
                                param_key, param_value = param.split(': ', 1)
                                if param_key == 'city' and name == 'WeatherTimeAgent':
                                    format_str += f"    \"{param_key}\": \"{local_city}\",\n"
                                else:
                                    format_str += f"    \"{param_key}\": \"{param_value}\",\n"
                            format_str += f"  ｝\n"
                            
                            mcp_list.append(format_str)
                        except:
                            # 如果JSON解析失败，使用简单格式
                            mcp_list.append(f"  {tool_name}: 使用tool_name参数调用")
        
        # 格式化Agent服务列表
        agent_list = []
        
        # 1. 添加handoff服务
        for service in agent_services:
            name = service.get("name", "")
            description = service.get("description", "")
            tool_name = service.get("tool_name", "agent")
            display_name = service.get("display_name", name)
            # 展示name+displayName
            if description:
                agent_list.append(f"- {name}(工具名: {tool_name}): {description}")
            else:
                agent_list.append(f"- {name}(工具名: {tool_name})")
        
        # 2. 直接从AgentManager获取已注册的Agent
        try:
            from mcpserver.agent_manager import get_agent_manager
            agent_manager = get_agent_manager()
            agent_manager_agents = agent_manager.get_available_agents()
            
            for agent in agent_manager_agents:
                name = agent.get("name", "")
                base_name = agent.get("base_name", "")
                description = agent.get("description", "")
                
                # 展示格式：base_name: 描述
                if description:
                    agent_list.append(f"- {base_name}: {description}")
                else:
                    agent_list.append(f"- {base_name}")
                    
        except Exception as e:
            # 如果AgentManager不可用，静默处理
            pass
        
        # 添加本地信息说明
        local_info = f"\n\n【当前环境信息】\n- 本地城市: {local_city}\n- 当前时间: {current_time}\n\n【使用说明】\n- 天气/时间查询时，请使用上述本地城市信息作为city参数\n- 所有时间相关查询都基于当前系统时间"
        
        # 返回格式化的服务列表
        result = {
            "available_mcp_services": "\n".join(mcp_list) + local_info if mcp_list else "无" + local_info,
            "available_agent_services": "\n".join(agent_list) if agent_list else "无"
        }
        
        return result

    async def process(self, u, is_voice_input=False):  # 添加is_voice_input参数
        try:
            # 演示模式处理
            if self.demo_mode:
                # 获取当前情绪状态
                emotion_state = None
                if self.emotional_ai:
                    try:
                        emotions = self.emotional_ai.current_emotions
                        if emotions:
                            emotion_state = emotions[0].emotion.value
                    except:
                        pass
                
                # 生成演示响应
                response = self.demo_response_func(u, emotion_state)
                
                # 情绪AI处理
                if self.emotional_ai:
                    try:
                        self.emotional_ai.process_interaction(u, response)
                    except Exception as e:
                        logger.error(f"演示模式情绪AI处理失败: {e}")
                
                yield ("StarryNight", response)
                return
            
            # 自然语言处理 - 检测并执行高级功能
            enhanced_context = ""
            try:
                from natural_language_processor import natural_language_processor
                
                nlp_result = await natural_language_processor.process_user_input(u)
                if nlp_result['detected_functions']:
                    logger.info(f"检测到高级功能调用: {nlp_result['detected_functions']}")
                    enhanced_context = nlp_result['enhanced_context']
                    
                    # 如果检测到功能调用，使用增强的上下文
                    if enhanced_context:
                        u = enhanced_context
                        
            except Exception as e:
                logger.debug(f"自然语言处理失败: {e}")
            
            # 开发者模式优先判断
            if u.strip() == "#devmode":
                self.dev_mode = True
                yield ("StarryNight", "已进入开发者模式")
                return

            # 只在语音输入时显示处理提示
            if is_voice_input:
                print(f"开始处理用户输入：{now()}")  # 语音转文本结束，开始处理
            
            # 完全禁用GRAG记忆查询
            # GRAG记忆查询
            # memory_context = ""
            # if self.memory_manager:
            #     try:
            #         memory_result = await self.memory_manager.query_memory(u)
            #         if memory_result:
            #             # memory_context = f"\n[记忆检索结果]: {memory_result}\n"
            #             logger.info("从GRAG记忆中检索到相关信息")
            #     except Exception as e:
            #         logger.error(f"GRAG记忆查询失败: {e}")
            
            # 获取人设提示词
            persona_prompt = ""
            try:
                from persona_management_system import get_persona_prompt, get_persona_manager, record_ai_behavior
                
                # 检查是否需要更新人设
                persona_manager = get_persona_manager()
                if hasattr(persona_manager, 'should_update_llm_persona') and persona_manager.should_update_llm_persona():
                    persona_prompt = get_persona_prompt(f"用户说: {u}")
                    
                    # 记录人设更新行为
                    record_ai_behavior(
                        "persona_update",
                        "更新LLM人设信息以适应当前情绪和状态",
                        emotional_impact=0.2
                    )
                    logger.info("已更新LLM人设提示词")
                else:
                    # 使用简化人设，避免过度冗余
                    persona_prompt = "You are StarryNight, a cute AI assistant with the mental age of 3. You'll stay lively and adorable!，Respond naturally based on the current mood."
                
            except Exception as e:
                logger.error(f"获取人设提示词失败: {e}")
                persona_prompt = "You are StarryNight, a cute AI assistant with the mental age of 3. You'll stay lively and adorable!"
            
            # 结合人设和原有系统提示词
            enhanced_system_prompt = f"{persona_prompt}\n\n{RECOMMENDED_PROMPT_PREFIX}\n{config.prompts.naga_system_prompt}"
            
            # 获取过滤后的服务列表
            available_services = self.mcp.get_available_services_filtered()
            services_text = self._format_services_for_prompt(available_services)
            
            # 安全地格式化系统提示词
            try:
                formatted_prompt = enhanced_system_prompt.format(**services_text)
            except KeyError as e:
                logger.warning(f"系统提示词格式化失败: {e}, 使用默认提示词")
                formatted_prompt = enhanced_system_prompt.replace("{available_mcp_services}", services_text.get("available_mcp_services", "无")).replace("{available_agent_services}", services_text.get("available_agent_services", "无"))
            except Exception as e:
                logger.error(f"系统提示词格式化异常: {e}, 使用基础提示词")
                formatted_prompt = "You are StarryNight, a helpful AI assistant."
            
            sysmsg = {"role": "system", "content": formatted_prompt}
            msgs = [sysmsg] if sysmsg else []
            msgs += self.messages[-20:] + [{"role": "user", "content": u}]

            print(f"GTP请求发送：{now()}")  # AI请求前
            
            # 非线性思考判断：启动后台异步判断任务
            thinking_task = None
            if hasattr(self, 'tree_thinking') and self.tree_thinking and getattr(self.tree_thinking, 'is_enabled', False):
                # 启动异步思考判断任务
                import asyncio
                thinking_task = asyncio.create_task(self._async_thinking_judgment(u))
            
            # 普通模式：走工具调用循环（不等待思考树判断）
            try:
                result = await tool_call_loop(msgs, self.mcp, self._call_llm, is_streaming=True)
                final_content = result['content']
                recursion_depth = result['recursion_depth']
                
                if recursion_depth > 0:
                    print(f"工具调用循环完成，共执行 {recursion_depth} 轮")
                
                # 流式输出最终结果
                for line in final_content.splitlines():
                    yield ("StarryNight", line)
                
                # 情绪AI处理
                if self.emotional_ai:
                    try:
                        # 处理用户交互，更新情绪状态
                        self.emotional_ai.process_interaction(u, final_content)
                        
                        # 根据情绪修改回复（可选，保持原有回复的完整性）
                        # final_content = self.emotional_ai.get_personality_modifier(final_content)
                    except Exception as e:
                        logger.error(f"情绪AI处理失败: {e}")
                
                # 保存对话历史
                self.messages += [{"role": "user", "content": u}, {"role": "assistant", "content": final_content}]
                self.save_log(u, final_content)
                
                # GRAG记忆存储（开发者模式不写入）
                if self.memory_manager and not self.dev_mode:
                    try:
                        await self.memory_manager.add_conversation_memory(u, final_content)
                    except Exception as e:
                        logger.error(f"GRAG记忆存储失败: {e}")
                
                # 动态发布器 - 发布对话动态
                if DYNAMIC_PUBLISHER_AVAILABLE and not self.dev_mode:
                    try:
                        # 构建对话摘要
                        conversation_summary = f"用户：{u[:50]}{'...' if len(u) > 50 else ''}\nStarryNight：{final_content[:100]}{'...' if len(final_content) > 100 else ''}"
                        
                        # 异步发布对话动态
                        await ai_dynamic_publisher.queue_activity(
                            'conversation',
                            conversation_summary,
                            {
                                'user_input': u,
                                'ai_response': final_content,
                                'recursion_depth': recursion_depth,
                                'timestamp': datetime.now().isoformat(),
                                'input_method': 'voice' if is_voice_input else 'text'
                            }
                        )
                        logger.debug("对话动态已加入发布队列")
                    except Exception as e:
                        logger.error(f"对话动态发布失败: {e}")
                
                # 检查异步思考判断结果，如果建议深度思考则提示用户
                if thinking_task and not thinking_task.done():
                    # 等待思考判断完成（最多等待3秒）
                    try:
                        await asyncio.wait_for(thinking_task, timeout=3.0)
                        if thinking_task.result():
                            yield ("StarryNight", "\n💡 这个问题较为复杂，下面我会更详细地解释这个流程...")
                            # 启动深度思考
                            try:
                                thinking_result = await self.tree_thinking.think_deeply(u)
                                if thinking_result and "answer" in thinking_result:
                                    # 直接使用thinking系统的结果，避免重复处理
                                    yield ("StarryNight", f"\n{thinking_result['answer']}")
                                    
                                    # 更新对话历史
                                    final_thinking_answer = thinking_result['answer']
                                    self.messages[-1] = {"role": "assistant", "content": final_content + "\n\n" + final_thinking_answer}
                                    self.save_log(u, final_content + "\n\n" + final_thinking_answer)
                                    
                                    # GRAG记忆存储（开发者模式不写入）
                                    if self.memory_manager and not self.dev_mode:
                                        try:
                                            await self.memory_manager.add_conversation_memory(u, final_content + "\n\n" + final_thinking_answer)
                                        except Exception as e:
                                            logger.error(f"GRAG记忆存储失败: {e}")
                            except Exception as e:
                                logger.error(f"深度思考处理失败: {e}")
                                yield ("StarryNight", f"🌳 深度思考系统出错: {str(e)}")
                    except asyncio.TimeoutError:
                        # 超时取消任务
                        thinking_task.cancel()
                    except Exception as e:
                        logger.debug(f"思考判断任务异常: {e}")
                
            except Exception as e:
                print(f"工具调用循环失败: {e}")
                yield ("StarryNight", f"[MCP异常]: {e}")
                return

            return
        except Exception as e:
            import sys
            import traceback
            traceback.print_exc(file=sys.stderr)
            yield ("StarryNight", f"[MCP异常]: {e}")
            return

    async def get_response(self, prompt: str, temperature: float = 0.7) -> str:
        """为树状思考系统等提供API调用接口""" # 统一接口
        try:
            response = await self.async_client.chat.completions.create(
                model=config.api.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=config.api.max_tokens
            )
            return response.choices[0].message.content
        except RuntimeError as e:
            if "handler is closed" in str(e):
                logger.debug(f"忽略连接关闭异常，重新创建客户端: {e}")
                # 重新创建客户端并重试
                self.async_client = AsyncOpenAI(api_key=config.api.api_key, base_url=config.api.base_url.rstrip('/') + '/')
                response = await self.async_client.chat.completions.create(
                    model=config.api.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=config.api.max_tokens
                )
                return response.choices[0].message.content
            else:
                logger.error(f"API调用失败: {e}")
                return f"API调用出错: {str(e)}"
        except Exception as e:
            logger.error(f"API调用失败: {e}")
            return f"API调用出错: {str(e)}"

    async def _async_thinking_judgment(self, question: str) -> bool:
        """异步判断问题是否需要深度思考
        
        Args:
            question: 用户问题
            
        Returns:
            bool: 是否需要深度思考
        """
        try:
            if not self.tree_thinking:
                return False
            
            # 使用thinking文件夹中现成的难度判断器
            difficulty_assessment = await self.tree_thinking.difficulty_judge.assess_difficulty(question)
            difficulty = difficulty_assessment.get("difficulty", 3)
            
            # 根据难度判断是否需要深度思考
            # 难度4-5（复杂/极难）建议深度思考
            should_think_deeply = difficulty >= 4
            
            logger.info(f"难度判断：{difficulty}/5，建议深度思考：{should_think_deeply}")
            return should_think_deeply
                   
        except Exception as e:
            logger.debug(f"异步思考判断失败: {e}")
            return False

async def process_user_message(s,msg):
    if config.system.voice_enabled and not msg: #无文本输入时启动语音识别
        async for text in s.voice.stt_stream():
            if text:
                msg=text
                break
        return await s.process(msg, is_voice_input=True)  # 语音输入
    return await s.process(msg, is_voice_input=False)  # 文字输入

# 全局LLM API调用函数，供其他模块使用
async def call_llm_api(prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
    """
    全局LLM API调用函数
    
    Args:
        prompt: 提示词
        max_tokens: 最大token数
        temperature: 温度参数
        
    Returns:
        str: LLM响应文本
    """
    client = None
    try:
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(
            api_key=config.api.api_key,
            base_url=config.api.base_url.rstrip('/') + '/'
        )
        
        response = await client.chat.completions.create(
            model=config.api.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        result = response.choices[0].message.content.strip()
        return result
        
    except Exception as e:
        logger.error(f"LLM API调用失败: {e}")
        return f"抱歉，我现在无法思考这个问题：{e}"
    finally:
        # 确保客户端正确关闭
        if client is not None:
            try:
                await client.close()
            except Exception as e:
                logger.debug(f"关闭LLM客户端时出现异常: {e}")
                pass