#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自然语言处理器 - 解析用户输入并自动调用对应的高级功能
"""

import re
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class NaturalLanguageProcessor:
    """自然语言处理器"""
    
    def __init__(self):
        self.keyword_patterns = {
            'screen_analysis': [
                r'看.*屏幕', r'屏幕.*内容', r'我.*屏幕.*什么', r'你.*看.*得.*到.*屏幕',
                r'屏幕.*显示', r'当前.*窗口', r'我.*在.*做.*什么', r'我.*正在.*干.*什么',
                r'我.*界面.*什么', r'屏幕.*活动', r'看.*我.*桌面', r'看.*得.*到.*屏幕'
            ],
            'camera_analysis': [
                r'看.*我', r'摄像头.*看.*到', r'我.*样子', r'能.*看.*见.*我',
                r'观察.*我', r'我.*表情', r'我.*情绪', r'我.*现在.*状态',
                r'镜头.*里.*我', r'你.*看.*到.*我', r'视频.*中.*我'
            ],
            'file_reading': [
                r'读.*文件', r'打开.*文件', r'文件.*内容', r'看.*文档',
                r'阅读.*\.(txt|md|py|js|html|json|xml|csv)', r'能.*读.*取',
                r'文件.*是.*什么', r'读.*取.*\w+\.(txt|md|py|js|html|json|xml|csv)',
                r'我.*写.*\w+\.(txt|md|py|js|html|json|xml|csv)', r'文档.*里.*什么',
                r'小说.*名.*\w+', r'代码.*文件'
            ],
            'web_search': [
                r'搜索.*', r'查找.*', r'上网.*找', r'网上.*搜',
                r'百度.*', r'谷歌.*', r'在线.*查', r'互联网.*搜索',
                r'帮.*找.*', r'查.*资料', r'搜.*信息'
            ],
            'general_perception': [
                r'我.*环境.*怎么样', r'周围.*情况', r'现在.*状况',
                r'观察.*周围', r'感知.*环境', r'当前.*情形',
                r'看看.*我.*现在.*环境', r'环境.*怎么样'
            ]
        }
    
    async def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """处理用户输入，识别需要调用的功能"""
        result = {
            'original_input': user_input,
            'detected_functions': [],
            'function_results': {},
            'enhanced_context': ''
        }
        
        try:
            # 检测各种功能需求
            detected_functions = self._detect_required_functions(user_input)
            result['detected_functions'] = detected_functions
            
            if detected_functions:
                logger.info(f"检测到需要调用的功能: {detected_functions}")
                
                # 按顺序执行检测到的功能
                for function_name in detected_functions:
                    function_result = await self._execute_function(function_name, user_input)
                    if function_result:
                        result['function_results'][function_name] = function_result
                
                # 生成增强上下文
                result['enhanced_context'] = self._generate_enhanced_context(
                    user_input, result['function_results']
                )
            
            return result
            
        except Exception as e:
            logger.error(f"处理用户输入失败: {e}")
            return result
    
    def _detect_required_functions(self, user_input: str) -> List[str]:
        """检测需要调用的功能"""
        detected = []
        user_input_lower = user_input.lower()
        
        for function_name, patterns in self.keyword_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    if function_name not in detected:
                        detected.append(function_name)
                    break
        
        return detected
    
    async def _execute_function(self, function_name: str, user_input: str) -> Optional[Dict[str, Any]]:
        """执行指定的功能"""
        try:
            if function_name == 'screen_analysis':
                return await self._execute_screen_analysis()
            elif function_name == 'camera_analysis':
                return await self._execute_camera_analysis()
            elif function_name == 'file_reading':
                return await self._execute_file_reading(user_input)
            elif function_name == 'web_search':
                return await self._execute_web_search(user_input)
            elif function_name == 'general_perception':
                return await self._execute_general_perception()
            
        except Exception as e:
            logger.error(f"执行功能 {function_name} 失败: {e}")
            return None
    
    async def _execute_screen_analysis(self) -> Optional[Dict[str, Any]]:
        """执行屏幕分析"""
        try:
            from enhanced_screen_analyzer import enhanced_screen_analyzer
            
            result = await enhanced_screen_analyzer.analyze_screen_content()
            
            if result and 'error' not in result:
                return {
                    'type': 'screen_analysis',
                    'user_activity': result.get('user_activity', {}),
                    'window_info': result.get('window_info', {}),
                    'observation': result.get('observation', ''),
                    'summary': f"屏幕分析完成: {result.get('observation', '观察到屏幕内容')}"
                }
            
        except Exception as e:
            logger.error(f"屏幕分析执行失败: {e}")
            
        return None
    
    async def _execute_camera_analysis(self) -> Optional[Dict[str, Any]]:
        """执行摄像头分析"""
        try:
            from enhanced_camera_analyzer import enhanced_camera_analyzer
            
            result = await enhanced_camera_analyzer.analyze_camera_content()
            
            if result and 'error' not in result:
                return {
                    'type': 'camera_analysis',
                    'face_analysis': result.get('face_analysis', {}),
                    'behavior_analysis': result.get('behavior_analysis', {}),
                    'observation': result.get('observation', ''),
                    'summary': f"摄像头分析完成: {result.get('observation', '通过摄像头观察到内容')}"
                }
            
        except Exception as e:
            logger.error(f"摄像头分析执行失败: {e}")
            
        return None
    
    async def _execute_file_reading(self, user_input: str) -> Optional[Dict[str, Any]]:
        """执行文件阅读"""
        try:
            # 尝试从用户输入中提取文件名
            file_info = self._extract_file_info(user_input)
            
            from proactive_file_reader import proactive_file_reader
            
            if file_info.get('specific_file'):
                # 尝试读取特定文件
                result = await self._read_specific_file(file_info['specific_file'])
            else:
                # 执行常规文件发现和阅读
                result = await proactive_file_reader.discover_and_read_files()
            
            if result and 'error' not in result:
                return {
                    'type': 'file_reading',
                    'files_read': result.get('reading_results', []),
                    'summary': result.get('summary', '文件阅读完成'),
                    'file_info': file_info
                }
            
        except Exception as e:
            logger.error(f"文件阅读执行失败: {e}")
            
        return None
    
    def _extract_file_info(self, user_input: str) -> Dict[str, Any]:
        """从用户输入中提取文件信息"""
        file_info = {'specific_file': None, 'file_extension': None, 'file_name': None}
        
        # 提取文件名模式
        file_patterns = [
            r'(\w+\.(txt|md|py|js|html|css|json|xml|csv))',  # 完整文件名
            r'名.*(\w+\.(txt|md|py|js|html|css|json|xml|csv))',  # "名为xxx.txt"
            r'叫.*(\w+\.(txt|md|py|js|html|css|json|xml|csv))',  # "叫xxx.txt"
        ]
        
        for pattern in file_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                full_filename = match.group(1)
                file_info['specific_file'] = full_filename
                file_info['file_name'] = full_filename.split('.')[0]
                file_info['file_extension'] = '.' + full_filename.split('.')[-1]
                break
        
        return file_info
    
    async def _read_specific_file(self, filename: str) -> Dict[str, Any]:
        """读取指定的文件"""
        try:
            # 搜索可能的文件路径
            possible_paths = [
                Path(r'C:\Users\wt\Desktop\AIStudy') / filename,  # 默认学习路径
                Path(r'C:\Users\wt\Desktop') / filename,          # 桌面
                Path(r'C:\Users\wt\Documents') / filename,        # 文档
                Path.cwd() / filename,                            # 当前目录
            ]
            
            found_file = None
            for path in possible_paths:
                if path.exists():
                    found_file = path
                    break
            
            if found_file:
                # 读取文件内容
                try:
                    with open(found_file, 'r', encoding='utf-8') as f:
                        content = f.read(10000)  # 限制读取长度
                    
                    return {
                        'timestamp': datetime.now().isoformat(),
                        'discovered_count': 1,
                        'read_count': 1,
                        'reading_results': [{
                            'file_path': str(found_file),
                            'file_name': filename,
                            'content_preview': content[:500],
                            'file_size': found_file.stat().st_size,
                            'analysis': {'content_length': len(content)},
                            'observation': f"成功读取了文件 {filename}，内容很有趣！"
                        }],
                        'summary': f"成功找到并读取了文件 {filename}！",
                        'suggestions': [f"文件 {filename} 的内容很有趣呢！", "感谢你让我学习新知识~"]
                    }
                except UnicodeDecodeError:
                    # 尝试其他编码
                    for encoding in ['gbk', 'gb2312']:
                        try:
                            with open(found_file, 'r', encoding=encoding) as f:
                                content = f.read(10000)
                            break
                        except:
                            continue
                    else:
                        return {'error': f'无法读取文件 {filename}，编码格式不支持'}
            else:
                return {
                    'timestamp': datetime.now().isoformat(),
                    'discovered_count': 0,
                    'read_count': 0,
                    'reading_results': [],
                    'summary': f"抱歉，我没有找到文件 {filename}。它可能在其他地方，或者文件名不太对？",
                    'suggestions': [f"没有找到文件 {filename}，也许在其他地方？", "可以告诉我更详细的路径吗？"]
                }
            
        except Exception as e:
            logger.error(f"读取特定文件失败: {e}")
            return {'error': str(e)}
    
    async def _execute_web_search(self, user_input: str) -> Optional[Dict[str, Any]]:
        """执行网络搜索"""
        try:
            from proactive_web_browser import proactive_web_browser
            
            result = await proactive_web_browser.browse_and_discover()
            
            if result and 'error' not in result:
                return {
                    'type': 'web_search',
                    'search_topic': result.get('search_topic', ''),
                    'interesting_content': result.get('interesting_content', []),
                    'summary': f"网络搜索完成，探索了关于 {result.get('search_topic', '未知')} 的内容"
                }
            
        except Exception as e:
            logger.error(f"网络搜索执行失败: {e}")
            
        return None
    
    async def _execute_general_perception(self) -> Optional[Dict[str, Any]]:
        """执行综合感知"""
        try:
            # 同时执行屏幕和摄像头分析
            screen_result = await self._execute_screen_analysis()
            camera_result = await self._execute_camera_analysis()
            
            return {
                'type': 'general_perception',
                'screen_analysis': screen_result,
                'camera_analysis': camera_result,
                'summary': '综合感知分析完成，获取了环境和屏幕信息'
            }
            
        except Exception as e:
            logger.error(f"综合感知执行失败: {e}")
            
        return None
    
    def _generate_enhanced_context(self, user_input: str, function_results: Dict[str, Any]) -> str:
        """生成增强的上下文信息"""
        context_parts = [f"用户问题: {user_input}\n"]
        
        if function_results:
            context_parts.append("执行的分析结果:")
            
            for function_name, result in function_results.items():
                if result:
                    summary = result.get('summary', f'{function_name}执行完成')
                    context_parts.append(f"- {summary}")
                    
                    # 添加具体的观察结果
                    if 'observation' in result:
                        context_parts.append(f"  观察: {result['observation']}")
                    
                    # 添加特定功能的详细信息
                    if function_name == 'screen_analysis' and 'user_activity' in result:
                        activity = result['user_activity']
                        context_parts.append(f"  用户活动: {activity.get('primary_activity', '未知')}")
                        context_parts.append(f"  参与度: {activity.get('engagement_level', 0):.1f}")
                    
                    elif function_name == 'camera_analysis' and 'face_analysis' in result:
                        face_info = result['face_analysis']
                        context_parts.append(f"  检测到人脸: {face_info.get('face_count', 0)}个")
                        if face_info.get('dominant_emotion'):
                            context_parts.append(f"  主要情绪: {face_info['dominant_emotion']}")
                    
                    elif function_name == 'file_reading' and 'files_read' in result:
                        files = result['files_read']
                        if files:
                            context_parts.append(f"  成功读取了 {len(files)} 个文件")
                            for file_info in files[:2]:  # 只显示前2个文件的信息
                                context_parts.append(f"    - {file_info.get('file_name', '未知文件')}")
        
        context_parts.append("\n请基于以上分析结果，用StarryNight3岁心理年龄的可爱语气回复用户的问题。")
        
        return "\n".join(context_parts)

# 全局实例
natural_language_processor = NaturalLanguageProcessor()