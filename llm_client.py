from openai import OpenAI
from typing import Tuple, List, Dict
import time
import re
from config import API_CONFIGS, API_REQUEST_INTERVAL, GPT_REQUEST_INTERVAL, GPT_MODEL_PATTERNS

class LLMClient:
    def __init__(self, api_config: dict):
        """初始化LLM客户端"""
        self.client = OpenAI(
            api_key=api_config['api_key'],
            base_url=api_config['base_url']
        )
        self.model = api_config['model']
        self.last_request_time = 0  # 上次请求时间戳
        
    def is_gemini_model(self) -> bool:
        """检查当前模型是否为Gemini模型"""
        return self.model.startswith("gemini-")
    
    def is_doubao_model(self) -> bool:
        """检查当前模型是否为豆包模型"""
        return "doubao" in self.model.lower()
    
    def is_gpt_model(self) -> bool:
        """检查当前模型是否为GPT模型"""
        model_lower = self.model.lower()
        return any(pattern.lower() in model_lower for pattern in GPT_MODEL_PATTERNS)
    
    def chat(self, messages: List[Dict[str, str]], delay: int = None) -> Tuple[str, str]:
        """与LLM交互
        
        Args:
            messages: 消息列表
            delay: 调用API前等待的时间（秒），如果为None则根据模型类型自动决定
        
        Returns:
            tuple: (content, reasoning_content)
        """
        try:
            # 根据模型类型决定是否需要延迟
            if delay is None:
                if self.is_gpt_model():
                    delay = GPT_REQUEST_INTERVAL
                    print(f"检测到GPT模型，等待{delay}秒防止上游负载饱和...")
                    time.sleep(delay)
                else:
                    print(f"非GPT模型，无需等待延迟")
                    delay = 0
            else:
                print(f"准备调用API，等待{delay}秒防止上游负载饱和...")
                time.sleep(delay)
            
            # 检查距离上次请求的时间间隔
            current_time = time.time()
            elapsed_time = current_time - self.last_request_time
            
            # 如果距离上次请求时间不足设定的间隔，则额外等待
            if elapsed_time < API_REQUEST_INTERVAL and self.last_request_time > 0:
                wait_time = API_REQUEST_INTERVAL - elapsed_time
                print(f"额外等待API请求间隔: {wait_time:.1f}秒...")
                time.sleep(wait_time)
            
            print(f"LLM请求: {messages}")
            # 强制使用配置文件中指定的模型名称，避免被环境变量或默认值覆盖
            model_name = self.model
            print(f"使用模型: {model_name}")
            
            # 判断是否使用流式响应（本游戏场景下使用非流式响应）
            use_stream = False
            
            # 确保使用正确的模型
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                n=1,  # 确保只返回一个结果，与Gemini API兼容
                stream=use_stream  # 是否使用流式响应
            )
            
            # 更新上次请求时间
            self.last_request_time = time.time()
            
            # 处理流式响应
            if use_stream:
                full_content = ""
                for chunk in response:
                    if not chunk.choices:
                        continue
                    delta_content = chunk.choices[0].delta.content
                    if delta_content:
                        full_content += delta_content
                print(f"LLM推理内容: {full_content}")
                return full_content, ""
            # 处理非流式响应
            elif response.choices:
                message = response.choices[0].message
                content = message.content if message.content else ""
                reasoning_content = getattr(message, "reasoning_content", "")
                print(f"LLM推理内容: {content}")
                return content, reasoning_content
            
            return "", ""
                
        except Exception as e:
            print(f"LLM调用出错: {str(e)}")
            return "", ""