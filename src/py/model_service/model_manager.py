"""
Qwen3 模型管理器

负责模型的加载、管理和推理
"""

import os
import sys
import torch
import threading
import contextlib
from pathlib import Path
from modelscope import AutoModelForCausalLM, AutoTokenizer
from transformers import TextIteratorStreamer
from utils.log_util import default_logger as logger

try:
    import pynvml
    PYNVML_AVAILABLE = True
except ImportError:
    PYNVML_AVAILABLE = False
    logger.warning("pynvml 不可用，将使用简单的 GPU 选择策略")


def get_best_gpu():
    """选择可用内存最多的 GPU 设备"""
    if not torch.cuda.is_available():
        return None
    
    best_gpu = 0
    max_free_memory = 0
    
    if PYNVML_AVAILABLE:
        try:
            pynvml.nvmlInit()
            for i in range(torch.cuda.device_count()):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
                
                total_memory = meminfo.total
                used_memory = meminfo.used
                free_memory = meminfo.free
                
                logger.info(f"GPU {i}: 总内存 {total_memory / 1024**3:.2f} GB, 已用 {used_memory / 1024**3:.2f} GB, 可用 {free_memory / 1024**3:.2f} GB")
                
                if free_memory > max_free_memory:
                    max_free_memory = free_memory
                    best_gpu = i
            
            logger.info(f"选择 GPU {best_gpu} (可用内存: {max_free_memory / 1024**3:.2f} GB)")
            return best_gpu
            
        except Exception as e:
            logger.error(f"使用 pynvml 检测 GPU 时出错: {e}")
            # 回退到简单策略
    
    # 简单策略：使用固定 GPU 3
    logger.info("使用简单的 GPU 选择策略，固定选择 GPU 3")
    return 3


class LogCapture:
    """捕获标准输出和错误输出到日志"""
    
    def __init__(self, logger):
        self.logger = logger
        self.stdout_buffer = []
        self.stderr_buffer = []
    
    def write(self, text):
        if text.strip():
            self.logger.info(f"[ModelScope] {text.strip()}")
    
    def flush(self):
        pass


@contextlib.contextmanager
def capture_model_logs():
    """上下文管理器：捕获模型加载过程的输出"""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    log_capture = LogCapture(logger)
    
    try:
        # 重定向输出到日志
        sys.stdout = log_capture
        sys.stderr = log_capture
        yield
    finally:
        # 恢复原始输出
        sys.stdout = old_stdout
        sys.stderr = old_stderr


class ModelManager:
    """模型管理器，负责加载和管理 Qwen3 模型"""
    
    def __init__(self, model_name="Qwen/Qwen3-8B"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = None
        self.is_loaded = False
        self._load_lock = threading.Lock()
        
    def _get_model_path(self):
        """获取模型路径，优先使用项目本地 models 目录"""
        # 获取项目根目录
        project_root = Path(__file__).parent.parent.parent.parent
        local_model_path = project_root / "models" / self.model_name
        
        # 检查本地模型是否存在
        if local_model_path.exists() and (local_model_path / "config.json").exists():
            logger.info(f"使用本地模型: {local_model_path}")
            return str(local_model_path)
        else:
            logger.info(f"本地模型不存在 ({local_model_path})，将从 ModelScope 下载: {self.model_name}")
            return self.model_name

    def load_model(self):
        """加载模型"""
        with self._load_lock:
            if self.is_loaded:
                return
            
            logger.info(f"开始加载模型: {self.model_name}")
            
            # 获取模型路径
            model_path = self._get_model_path()
            
            # 配置模型参数
            model_kwargs = {
                "trust_remote_code": True,
            }
            
            # 自动选择内存最多的 GPU
            best_gpu = get_best_gpu()
            if best_gpu is not None:
                model_kwargs.update({
                    "torch_dtype": torch.float16,
                    "device_map": {"": best_gpu},
                })
                self.device = f"cuda:{best_gpu}"
            else:
                logger.warning("未检测到 CUDA 设备，使用 CPU")
                model_kwargs.update({"torch_dtype": torch.float32})
                self.device = "cpu"
            
            # 加载 tokenizer 和模型
            logger.info(f"加载 tokenizer: {model_path}")
            with capture_model_logs():
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_path, 
                    trust_remote_code=True
                )
            
            logger.info(f"加载模型: {model_path}")
            with capture_model_logs():
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path, 
                    **model_kwargs
                )
            
            self.is_loaded = True
            logger.info(f"模型加载完成，设备: {self.device}")
    
    def generate_response(self, user_input, history=None):
        """生成普通响应"""
        if not self.is_loaded:
            raise RuntimeError("模型未加载，请先调用 load_model()")
        
        if history is None:
            history = []
        
        messages = history + [{"role": "user", "content": user_input}]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(text, return_tensors="pt")
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            result = self.model.generate(**inputs, max_new_tokens=32768)
            response_ids = result[0][len(inputs["input_ids"][0]):].tolist()
            response = self.tokenizer.decode(response_ids, skip_special_tokens=True)
        
        return response
    
    def generate_response_stream(self, user_input, history=None):
        """生成流式响应"""
        if not self.is_loaded:
            raise RuntimeError("模型未加载，请先调用 load_model()")
        
        if history is None:
            history = []
        
        messages = history + [{"role": "user", "content": user_input}]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(text, return_tensors="pt")
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        
        # 使用流式生成
        streamer = TextIteratorStreamer(
            self.tokenizer, 
            skip_prompt=True, 
            skip_special_tokens=True
        )
        generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=32768)
        
        thread = threading.Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        
        for new_text in streamer:
            yield new_text
        
        thread.join()
    
    def get_model_info(self):
        """获取模型信息"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "is_loaded": self.is_loaded,
            "model_size": self.model.num_parameters() if self.is_loaded else None,
        }
    
    def health_check(self):
        """健康检查"""
        if not self.is_loaded:
            return False, "模型未加载"
        
        try:
            # 简单测试推理
            test_response = self.generate_response("测试", history=[])
            return True, "模型正常"
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return False, f"模型异常: {str(e)}"


# 全局模型管理器实例
model_manager = ModelManager()