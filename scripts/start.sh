#!/bin/bash

# Qwen Model Service Start Script
# 服务启动脚本

set -e

# 默认参数
HOST="0.0.0.0"
PORT="19100"
WORKERS="1"
LOG_LEVEL="info"
RELOAD="false"

# 帮助信息
show_help() {
    cat << EOF
Qwen Model Service 启动脚本

用法: $0 [选项]

选项:
    -h, --help          显示帮助信息
    -H, --host HOST     服务器主机地址 (默认: 0.0.0.0)
    -p, --port PORT     服务器端口 (默认: 19100)
    -w, --workers NUM   工作进程数 (默认: 1)
    -l, --log-level LVL 日志级别 (默认: info)
    -r, --reload        启用热重载 (开发模式)
    -d, --daemon        后台运行
    -s, --stop          停止服务

示例:
    $0                                # 使用默认参数启动
    $0 -p 8080 -w 4                 # 指定端口和进程数
    $0 -r -l debug                  # 开发模式启动
    $0 -d                           # 后台运行
    $0 -s                           # 停止服务

EOF
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -H|--host)
            HOST="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -w|--workers)
            WORKERS="$2"
            shift 2
            ;;
        -l|--log-level)
            LOG_LEVEL="$2"
            shift 2
            ;;
        -r|--reload)
            RELOAD="true"
            shift
            ;;
        -d|--daemon)
            DAEMON="true"
            shift
            ;;
        -s|--stop)
            STOP="true"
            shift
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 停止服务
if [ "$STOP" = "true" ]; then
    echo "正在停止服务..."
    pkill -f "model_service.start_service" || echo "服务未运行"
    exit 0
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "错误: 未找到虚拟环境，请先运行 scripts/setup.sh"
    exit 1
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 创建日志目录
mkdir -p logs

# 构建启动命令
CMD="python src/py/model_service/start_service.py"
CMD="$CMD --host $HOST --port $PORT --workers $WORKERS --log-level $LOG_LEVEL"

if [ "$RELOAD" = "true" ]; then
    CMD="$CMD --reload"
fi

# 启动服务
echo "======================================"
echo "Qwen Model Service 启动中..."
echo "======================================"
echo "主机地址: $HOST"
echo "端口号: $PORT"
echo "工作进程数: $WORKERS"
echo "日志级别: $LOG_LEVEL"
echo "热重载: $RELOAD"
echo "======================================"

if [ "$DAEMON" = "true" ]; then
    echo "后台模式启动..."
    nohup $CMD > logs/service.log 2>&1 &
    echo "服务已在后台启动，PID: $!"
    echo "日志文件: logs/service.log"
    echo "停止服务: $0 -s"
else
    echo "前台模式启动..."
    exec $CMD
fi