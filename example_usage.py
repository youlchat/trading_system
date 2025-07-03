#!/usr/bin/env python3
"""
使用示例：如何通过API更新配置并获取数据
"""

import requests
import json
import time

def example_usage():
    """使用示例"""
    base_url = "http://localhost:5001/api"
    
    print("🚀 加密货币交易系统 - API使用示例\n")
    
    # 1. 更新API配置
    print("1️⃣ 更新API配置...")
    config_data = {
        "binance_api_key": "your_binance_api_key_here",
        "binance_secret": "your_binance_secret_here",
        "okx_api_key": "your_okx_api_key_here",
        "okx_secret": "your_okx_secret_here",
        "okx_password": "your_okx_password_here"
    }
    
    try:
        response = requests.post(
            f"{base_url}/update_config",
            headers={"Content-Type": "application/json"},
            json=config_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result.get('message', '配置更新成功')}")
        else:
            print(f"❌ 配置更新失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return
    
    # 2. 获取可用交易对
    print("\n2️⃣ 获取可用交易对...")
    try:
        response = requests.get(f"{base_url}/symbols")
        if response.status_code == 200:
            symbols = response.json().get('symbols', [])
            print(f"✅ 找到 {len(symbols)} 个交易对")
            if symbols:
                print(f"   前5个: {symbols[:5]}")
        else:
            print(f"❌ 获取交易对失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取交易对失败: {e}")
    
    # 3. 获取K线数据
    print("\n3️⃣ 获取BTC/USDT的K线数据...")
    try:
        response = requests.get(f"{base_url}/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=5")
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                print(f"⚠️ {data['error']}")
            else:
                binance_count = len(data.get('binance', []))
                okx_count = len(data.get('okx', []))
                print(f"✅ 获取成功: 币安 {binance_count} 条, 欧易 {okx_count} 条")
                
                # 显示最新价格
                if data.get('binance') and data.get('okx'):
                    binance_latest = data['binance'][-1]
                    okx_latest = data['okx'][-1]
                    print(f"   币安最新价格: ${binance_latest['close']:.2f}")
                    print(f"   欧易最新价格: ${okx_latest['close']:.2f}")
        else:
            print(f"❌ 获取K线数据失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取K线数据失败: {e}")
    
    # 4. 获取资金费率
    print("\n4️⃣ 获取BTC/USDT的资金费率...")
    try:
        response = requests.get(f"{base_url}/funding_rate?symbol=BTC/USDT")
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                print(f"⚠️ {data['error']}")
            else:
                binance_rate = data.get('binance', {}).get('funding_rate', 0)
                okx_rate = data.get('okx', {}).get('funding_rate', 0)
                print(f"✅ 获取成功:")
                print(f"   币安资金费率: {binance_rate:.6f}")
                print(f"   欧易资金费率: {okx_rate:.6f}")
        else:
            print(f"❌ 获取资金费率失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取资金费率失败: {e}")
    
    # 5. 获取分析数据
    print("\n5️⃣ 获取价差和资金费率分析...")
    try:
        response = requests.get(f"{base_url}/analysis?symbol=BTC/USDT")
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                print(f"⚠️ {data['error']}")
            else:
                price_analysis = data.get('price_analysis', {})
                funding_analysis = data.get('funding_analysis', {})
                
                print(f"✅ 分析结果:")
                print(f"   价差: ${price_analysis.get('price_difference', 0):.2f}")
                print(f"   价差百分比: {price_analysis.get('price_difference_percent', 0):.4f}%")
                print(f"   资金费率差: {funding_analysis.get('funding_difference', 0):.6f}")
                
                # 套利建议
                if price_analysis.get('price_difference_percent', 0) > 0.1:
                    print("   💡 价差套利机会: 高")
                else:
                    print("   💡 价差套利机会: 低")
                    
                if funding_analysis.get('funding_difference', 0) > 0.001:
                    print("   💡 资金费率套利机会: 高")
                else:
                    print("   💡 资金费率套利机会: 低")
        else:
            print(f"❌ 获取分析数据失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取分析数据失败: {e}")
    
    print("\n🎉 示例完成！")

if __name__ == "__main__":
    example_usage() 