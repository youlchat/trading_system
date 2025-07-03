#!/usr/bin/env python3
"""
测试API配置更新功能
"""

import requests
import json

def test_api_config_update():
    """测试API配置更新功能"""
    base_url = "http://localhost:5001/api"
    
    # 测试数据
    test_config = {
        "binance_api_key": "test_binance_key",
        "binance_secret": "test_binance_secret",
        "okx_api_key": "test_okx_key",
        "okx_secret": "test_okx_secret",
        "okx_password": "test_okx_password"
    }
    
    try:
        # 测试更新配置
        print("🔄 测试更新API配置...")
        response = requests.post(
            f"{base_url}/update_config",
            headers={"Content-Type": "application/json"},
            json=test_config
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 配置更新成功: {result}")
        else:
            print(f"❌ 配置更新失败: {response.status_code} - {response.text}")
            return False
        
        # 测试获取交易对（使用更新后的配置）
        print("\n🔄 测试获取交易对...")
        response = requests.get(f"{base_url}/symbols")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取交易对成功: {len(result.get('symbols', []))} 个交易对")
        else:
            print(f"❌ 获取交易对失败: {response.status_code} - {response.text}")
        
        # 测试获取K线数据
        print("\n🔄 测试获取K线数据...")
        response = requests.get(f"{base_url}/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=10")
        
        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                print(f"⚠️ 获取K线数据返回错误: {result['error']}")
            else:
                binance_count = len(result.get('binance', []))
                okx_count = len(result.get('okx', []))
                print(f"✅ 获取K线数据成功: 币安 {binance_count} 条, 欧易 {okx_count} 条")
        else:
            print(f"❌ 获取K线数据失败: {response.status_code} - {response.text}")
        
        # 测试获取现货资金费率（应该返回无资金费率）
        print("\n🔄 测试获取现货资金费率...")
        response = requests.get(f"{base_url}/funding_rate?symbol=BTC/USDT")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('is_spot'):
                print(f"✅ 现货交易对正确处理: {result.get('binance', {}).get('note', '无资金费率')}")
            elif 'error' in result:
                print(f"⚠️ 获取资金费率返回错误: {result['error']}")
            else:
                print(f"✅ 获取资金费率成功")
        else:
            print(f"❌ 获取资金费率失败: {response.status_code} - {response.text}")
        
        # 测试获取合约资金费率
        print("\n🔄 测试获取合约资金费率...")
        response = requests.get(f"{base_url}/funding_rate?symbol=BTC/USDT:USDT")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('is_spot'):
                print(f"⚠️ 合约交易对被识别为现货: {result.get('binance', {}).get('note', '无资金费率')}")
            elif 'error' in result:
                print(f"⚠️ 获取合约资金费率返回错误: {result['error']}")
            else:
                print(f"✅ 获取合约资金费率成功")
        else:
            print(f"❌ 获取合约资金费率失败: {response.status_code} - {response.text}")
        
        # 测试获取现货分析数据
        print("\n🔄 测试获取现货分析数据...")
        response = requests.get(f"{base_url}/analysis?symbol=BTC/USDT")
        
        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                print(f"⚠️ 获取现货分析数据返回错误: {result['error']}")
            else:
                print(f"✅ 获取现货分析数据成功")
                if result.get('funding_analysis', {}).get('note'):
                    print(f"   现货交易对分析: {result['funding_analysis']['note']}")
        else:
            print(f"❌ 获取现货分析数据失败: {response.status_code} - {response.text}")
        
        # 测试获取合约分析数据
        print("\n🔄 测试获取合约分析数据...")
        response = requests.get(f"{base_url}/analysis?symbol=BTC/USDT:USDT")
        
        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                print(f"⚠️ 获取合约分析数据返回错误: {result['error']}")
            else:
                print(f"✅ 获取合约分析数据成功")
                if result.get('funding_analysis', {}).get('error'):
                    print(f"   资金费率获取失败: {result['funding_analysis']['error']}")
                else:
                    print(f"   合约分析正常")
        else:
            print(f"❌ 获取合约分析数据失败: {response.status_code} - {response.text}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保后端服务正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始测试API配置更新功能...\n")
    success = test_api_config_update()
    
    if success:
        print("\n✅ 测试完成！")
    else:
        print("\n❌ 测试失败！") 