#!/usr/bin/env python3
"""
交易系统测试脚本
"""

import requests
import json
import time
from datetime import datetime

def test_api_endpoints():
    """测试API端点"""
    base_url = "http://localhost:5000/api"
    
    print("🧪 开始测试API端点...")
    
    # 测试获取交易对列表
    try:
        response = requests.get(f"{base_url}/symbols")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取交易对成功: {len(data.get('symbols', []))} 个交易对")
        else:
            print(f"❌ 获取交易对失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取交易对异常: {e}")
    
    # 测试获取K线数据
    try:
        response = requests.get(f"{base_url}/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=10")
        if response.status_code == 200:
            data = response.json()
            binance_count = len(data.get('binance', []))
            okx_count = len(data.get('okx', []))
            print(f"✅ 获取K线数据成功: 币安{binance_count}条, 欧易{okx_count}条")
        else:
            print(f"❌ 获取K线数据失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取K线数据异常: {e}")
    
    # 测试获取资金费率
    try:
        response = requests.get(f"{base_url}/funding_rate?symbol=BTC/USDT")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取资金费率成功")
            if data.get('binance'):
                print(f"   币安资金费率: {data['binance'].get('funding_rate', 'N/A')}")
            if data.get('okx'):
                print(f"   欧易资金费率: {data['okx'].get('funding_rate', 'N/A')}")
        else:
            print(f"❌ 获取资金费率失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取资金费率异常: {e}")
    
    # 测试获取分析数据
    try:
        response = requests.get(f"{base_url}/analysis?symbol=BTC/USDT")
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                print(f"✅ 获取分析数据成功")
                price_diff = data.get('price_analysis', {}).get('price_difference_percent', 0)
                funding_diff = data.get('funding_analysis', {}).get('funding_difference', 0)
                print(f"   价差百分比: {price_diff:.4f}%")
                print(f"   资金费率差: {funding_diff:.6f}")
            else:
                print(f"❌ 分析数据错误: {data['error']}")
        else:
            print(f"❌ 获取分析数据失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取分析数据异常: {e}")

def test_data_consistency():
    """测试数据一致性"""
    print("\n🔍 测试数据一致性...")
    
    base_url = "http://localhost:5000/api"
    
    # 测试多个交易对
    symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
    
    for symbol in symbols:
        try:
            # 获取价格数据
            ticker_response = requests.get(f"{base_url}/ticker?symbol={symbol}")
            funding_response = requests.get(f"{base_url}/funding_rate?symbol={symbol}")
            
            if ticker_response.status_code == 200 and funding_response.status_code == 200:
                ticker_data = ticker_response.json()
                funding_data = funding_response.json()
                
                print(f"✅ {symbol}:")
                if ticker_data.get('binance') and ticker_data.get('okx'):
                    binance_price = ticker_data['binance']['last']
                    okx_price = ticker_data['okx']['last']
                    price_diff = abs(binance_price - okx_price)
                    print(f"   价格: 币安${binance_price:.2f}, 欧易${okx_price:.2f}, 价差${price_diff:.2f}")
                
                if funding_data.get('binance') and funding_data.get('okx'):
                    binance_funding = funding_data['binance'].get('funding_rate', 0)
                    okx_funding = funding_data['okx'].get('funding_rate', 0)
                    funding_diff = abs(binance_funding - okx_funding)
                    print(f"   资金费率: 币安{binance_funding:.6f}, 欧易{okx_funding:.6f}, 费率差{funding_diff:.6f}")
            
        except Exception as e:
            print(f"❌ {symbol} 测试失败: {e}")

def test_performance():
    """测试性能"""
    print("\n⚡ 测试性能...")
    
    base_url = "http://localhost:5000/api"
    start_time = time.time()
    
    # 测试连续请求
    for i in range(5):
        try:
            response = requests.get(f"{base_url}/ticker?symbol=BTC/USDT")
            if response.status_code == 200:
                print(f"✅ 请求 {i+1}: 成功 ({time.time() - start_time:.2f}s)")
            else:
                print(f"❌ 请求 {i+1}: 失败")
        except Exception as e:
            print(f"❌ 请求 {i+1}: 异常 - {e}")
        
        time.sleep(1)  # 避免请求过于频繁
    
    total_time = time.time() - start_time
    print(f"📊 总耗时: {total_time:.2f}秒")

def main():
    """主测试函数"""
    print("=" * 50)
    print("🧪 交易系统测试")
    print("=" * 50)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 等待后端服务启动
    print("⏳ 等待后端服务启动...")
    time.sleep(3)
    
    # 测试API端点
    test_api_endpoints()
    
    # 测试数据一致性
    test_data_consistency()
    
    # 测试性能
    test_performance()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")
    print("=" * 50)

if __name__ == '__main__':
    main() 