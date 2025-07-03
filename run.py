#!/usr/bin/env python3
"""
交易系统启动脚本
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import ccxt
        import flask
        import pandas
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def create_env_file():
    """创建环境变量文件"""
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 创建 .env 文件...")
        with open(env_file, 'w') as f:
            f.write("""# 币安API配置
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_SECRET=your_binance_secret_here

# 欧易API配置
OKX_API_KEY=your_okx_api_key_here
OKX_SECRET=your_okx_secret_here
OKX_PASSWORD=your_okx_password_here
""")
        print("✅ .env 文件已创建，请配置您的API密钥")

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    backend_dir = Path('backend')
    if not backend_dir.exists():
        print("❌ backend 目录不存在")
        return False
    
    os.chdir(backend_dir)
    
    try:
        # 启动Flask应用
        from app import app
        print("✅ 后端服务启动成功")
        print("🌐 服务地址: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ 后端服务启动失败: {e}")
        return False

def open_frontend():
    """打开前端页面"""
    frontend_file = Path('frontend/index.html')
    if frontend_file.exists():
        print("🌐 打开前端页面...")
        webbrowser.open(f'file://{frontend_file.absolute()}')
    else:
        print("❌ 前端文件不存在")

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 加密货币交易系统")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 创建环境变量文件
    create_env_file()
    
    # 启动后端服务
    start_backend()

if __name__ == '__main__':
    main() 