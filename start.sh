#!/bin/bash

# 交易系统启动脚本

echo "🚀 启动加密货币交易系统..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install -r requirements.txt

# 创建环境变量文件
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量文件..."
    cp env_example.txt .env
    echo "⚠️  请编辑 .env 文件配置您的API密钥"
fi

# 启动后端服务
echo "🚀 启动后端服务..."
cd backend
python app.py &
BACKEND_PID=$!

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 5

# 打开前端页面
echo "🌐 打开前端页面..."
if command -v open &> /dev/null; then
    open ../frontend/index.html
elif command -v xdg-open &> /dev/null; then
    xdg-open ../frontend/index.html
else
    echo "📱 请手动打开 frontend/index.html"
fi

echo "✅ 系统启动完成！"
echo "🌐 后端服务: http://localhost:5000"
echo "📱 前端页面: frontend/index.html"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap "echo '🛑 停止服务...'; kill $BACKEND_PID; exit" INT
wait 