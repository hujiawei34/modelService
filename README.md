# Qwen Model Service

提供基于 Qwen 语言模型的 Web 服务，支持聊天对话和流式响应。

## 功能特性

- 🚀 基于 FastAPI 的高性能 Web 服务
- 🤖 支持 Qwen2.5 和 Qwen3 模型
- 💬 支持普通聊天和流式聊天
- 🔄 自动模型加载和管理
- 📊 完整的 API 文档
- 🔍 健康检查接口

## 项目结构

```
modelService/
├── src/py/
│   ├── model_service/          # 核心服务模块
│   │   ├── server.py          # FastAPI 服务器
│   │   ├── api_routes.py      # API 路由
│   │   ├── model_manager.py   # 模型管理器
│   │   ├── client.py          # 客户端工具
│   │   └── start_service.py   # 启动脚本
│   ├── prepare/               # 模型准备工具
│   └── utils/                 # 工具函数
├── models/                    # 模型文件目录
├── doc/                       # 文档
└── requirements.txt           # 依赖包
```

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 模型准备

确保在 `models/` 目录下有可用的 Qwen 模型文件。

### 3. 启动服务

```bash
# 使用启动脚本
python src/py/model_service/start_service.py

# 或者自定义参数
python src/py/model_service/start_service.py --host 0.0.0.0 --port 19100 --reload
```

### 4. 访问服务

- 服务地址: http://localhost:19100
- API 文档: http://localhost:19100/docs
- 健康检查: http://localhost:19100/health

## API 接口

### 普通聊天
```bash
POST /api/v1/chat
Content-Type: application/json

{
  "message": "你好，请介绍一下你自己",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

### 流式聊天
```bash
POST /api/v1/chat/stream
Content-Type: application/json

{
  "message": "写一个 Python 函数来计算斐波那契数列",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

## 启动参数

| 参数 | 默认值 | 描述 |
|------|--------|------|
| --host | 0.0.0.0 | 服务器主机地址 |
| --port | 19100 | 服务器端口 |
| --workers | 1 | 工作进程数 |
| --reload | False | 启用热重载（开发模式） |
| --log-level | info | 日志级别 |

## 开发模式

```bash
# 启用热重载和调试模式
python src/py/model_service/start_service.py --reload --log-level debug
```

## 部署

### Docker 部署
```bash
# 构建镜像
docker build -t qwen-model-service .

# 运行容器
docker run -p 19100:19100 qwen-model-service
```

### 生产环境
```bash
# 使用多进程运行
python src/py/model_service/start_service.py --workers 4 --log-level warning
```

## 故障排除

1. **模型加载失败**: 检查模型文件路径和格式
2. **端口被占用**: 使用 `--port` 参数指定其他端口
3. **内存不足**: 减少 workers 数量或使用更小的模型

## 许可证

本项目使用 MIT 许可证。