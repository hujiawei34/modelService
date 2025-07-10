#!/bin/bash

# Qwen Model Service Setup Script
# 自动化环境搭建脚本

set -e

echo "======================================"
echo "Qwen Model Service 环境搭建脚本"
echo "======================================"

# 检查 Python 版本
echo "检查 Python 版本..."
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "错误: 需要 Python $required_version 或更高版本，当前版本: $python_version"
    exit 1
fi

echo "Python 版本检查通过: $python_version"

# 创建虚拟环境
echo "创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "虚拟环境创建成功"
else
    echo "虚拟环境已存在"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "安装项目依赖..."
pip install -r requirements.txt

# 安装项目本身（开发模式）
echo "安装项目（开发模式）..."
pip install -e .

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p logs
mkdir -p data
mkdir -p output

# 设置权限
echo "设置脚本权限..."
chmod +x scripts/*.sh

echo "======================================"
echo "环境搭建完成！"
echo "======================================"
echo "使用方法:"
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 启动服务: python src/py/model_service/start_service.py"
echo "3. 或使用命令: qwen-service"
echo "4. 访问文档: http://localhost:19100/docs"
echo "======================================"