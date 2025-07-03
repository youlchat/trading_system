from flask import Flask, request, jsonify
from flask_cors import CORS
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

class TradingDataCollector:
    def __init__(self):
        # 默认从环境变量初始化，但可以被动态更新
        self.binance_config = {
            'apiKey': os.getenv('BINANCE_API_KEY', ''),
            'secret': os.getenv('BINANCE_SECRET', ''),
            'sandbox': False,
            'enableRateLimit': True
        }
        
        self.okx_config = {
            'apiKey': os.getenv('OKX_API_KEY', ''),
            'secret': os.getenv('OKX_SECRET', ''),
            'password': os.getenv('OKX_PASSWORD', ''),
            'sandbox': False,
            'enableRateLimit': True
        }
        
        # 初始化交易所实例
        self._init_exchanges()
    
    def _init_exchanges(self):
        """初始化交易所实例"""
        try:
            self.binance = ccxt.binance(self.binance_config)
            self.okx = ccxt.okx(self.okx_config)
        except Exception as e:
            print(f"初始化交易所失败: {e}")
            self.binance = None
            self.okx = None
    
    def update_api_config(self, binance_config=None, okx_config=None):
        """更新API配置"""
        if binance_config:
            self.binance_config.update(binance_config)
        
        if okx_config:
            self.okx_config.update(okx_config)
        
        # 重新初始化交易所实例
        self._init_exchanges()
        
        return {
            'success': True,
            'message': 'API配置已更新'
        }
    
    def get_available_symbols(self):
        """获取可用的交易对"""
        try:
            if not self.binance or not self.okx:
                return []
                
            binance_symbols = self.binance.load_markets()
            okx_symbols = self.okx.load_markets()
            
            # 获取共同的USDT交易对
            binance_usdt = [s for s in binance_symbols.keys() if '/USDT' in s]
            okx_usdt = [s for s in okx_symbols.keys() if '/USDT' in s]
            
            common_symbols = list(set(binance_usdt) & set(okx_usdt))
            return sorted(common_symbols)
        except Exception as e:
            print(f"获取交易对失败: {e}")
            return []
    
    def get_ohlcv_data(self, symbol, timeframe='1h', limit=100):
        """获取K线数据"""
        try:
            if not self.binance or not self.okx:
                return {'binance': [], 'okx': [], 'error': '交易所未初始化'}
            
            # 获取币安数据
            binance_ohlcv = self.binance.fetch_ohlcv(symbol, timeframe, limit=limit)
            binance_df = pd.DataFrame(binance_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            binance_df['timestamp'] = pd.to_datetime(binance_df['timestamp'], unit='ms')
            binance_df['exchange'] = 'Binance'
            
            # 获取欧易数据
            okx_ohlcv = self.okx.fetch_ohlcv(symbol, timeframe, limit=limit)
            okx_df = pd.DataFrame(okx_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            okx_df['timestamp'] = pd.to_datetime(okx_df['timestamp'], unit='ms')
            okx_df['exchange'] = 'OKX'
            
            return {
                'binance': binance_df.to_dict('records'),
                'okx': okx_df.to_dict('records')
            }
        except Exception as e:
            print(f"获取K线数据失败: {e}")
            return {'binance': [], 'okx': [], 'error': str(e)}
    
    def get_funding_rate(self, symbol):
        """获取资金费率"""
        try:
            if not self.binance or not self.okx:
                return {'binance': {}, 'okx': {}, 'error': '交易所未初始化'}
            
            # 检查是否为现货交易对（不包含:USDT等合约标识）
            is_spot = ':' not in symbol
            
            if is_spot:
                # 现货交易对没有资金费率，返回空数据
                return {
                    'binance': {
                        'funding_rate': 0,
                        'next_funding_time': 0,
                        'timestamp': 0,
                        'note': '现货交易对无资金费率'
                    },
                    'okx': {
                        'funding_rate': 0,
                        'next_funding_time': 0,
                        'timestamp': 0,
                        'note': '现货交易对无资金费率'
                    },
                    'is_spot': True
                }
            
            # 合约交易对获取资金费率
            try:
                # 币安资金费率
                binance_funding = self.binance.fetch_funding_rate(symbol)
                
                # 欧易资金费率
                okx_funding = self.okx.fetch_funding_rate(symbol)
                
                return {
                    'binance': {
                        'funding_rate': binance_funding.get('fundingRate', 0),
                        'next_funding_time': binance_funding.get('nextFundingTime', 0),
                        'timestamp': binance_funding.get('timestamp', 0)
                    },
                    'okx': {
                        'funding_rate': okx_funding.get('fundingRate', 0),
                        'next_funding_time': okx_funding.get('nextFundingTime', 0),
                        'timestamp': okx_funding.get('timestamp', 0)
                    },
                    'is_spot': False
                }
            except Exception as e:
                print(f"获取合约资金费率失败: {e}")
                return {
                    'binance': {},
                    'okx': {},
                    'error': f'获取资金费率失败: {str(e)}',
                    'is_spot': False
                }
                
        except Exception as e:
            print(f"获取资金费率失败: {e}")
            return {'binance': {}, 'okx': {}, 'error': str(e)}
    
    def get_ticker(self, symbol):
        """获取实时价格"""
        try:
            if not self.binance or not self.okx:
                return {'binance': {}, 'okx': {}, 'error': '交易所未初始化'}
            
            binance_ticker = self.binance.fetch_ticker(symbol)
            okx_ticker = self.okx.fetch_ticker(symbol)
            
            return {
                'binance': {
                    'bid': binance_ticker['bid'],
                    'ask': binance_ticker['ask'],
                    'last': binance_ticker['last'],
                    'volume': binance_ticker['baseVolume']
                },
                'okx': {
                    'bid': okx_ticker['bid'],
                    'ask': okx_ticker['ask'],
                    'last': okx_ticker['last'],
                    'volume': okx_ticker['baseVolume']
                }
            }
        except Exception as e:
            print(f"获取价格数据失败: {e}")
            return {'binance': {}, 'okx': {}, 'error': str(e)}

# 初始化数据收集器
collector = TradingDataCollector()

@app.route('/api/update_config', methods=['POST'])
def update_config():
    """更新API配置"""
    try:
        data = request.get_json()
        
        binance_config = {}
        okx_config = {}
        
        # 提取币安配置
        if data.get('binance_api_key'):
            binance_config['apiKey'] = data['binance_api_key']
        if data.get('binance_secret'):
            binance_config['secret'] = data['binance_secret']
        
        # 提取欧易配置
        if data.get('okx_api_key'):
            okx_config['apiKey'] = data['okx_api_key']
        if data.get('okx_secret'):
            okx_config['secret'] = data['okx_secret']
        if data.get('okx_password'):
            okx_config['password'] = data['okx_password']
        
        result = collector.update_api_config(binance_config, okx_config)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/symbols', methods=['GET'])
def get_symbols():
    """获取可用交易对"""
    symbols = collector.get_available_symbols()
    return jsonify({'symbols': symbols})

@app.route('/api/ohlcv', methods=['GET'])
def get_ohlcv():
    """获取K线数据"""
    symbol = request.args.get('symbol', 'BTC/USDT')
    timeframe = request.args.get('timeframe', '1h')
    limit = int(request.args.get('limit', 100))
    
    data = collector.get_ohlcv_data(symbol, timeframe, limit)
    return jsonify(data)

@app.route('/api/funding_rate', methods=['GET'])
def get_funding_rate():
    """获取资金费率"""
    symbol = request.args.get('symbol', 'BTC/USDT')
    data = collector.get_funding_rate(symbol)
    return jsonify(data)

@app.route('/api/ticker', methods=['GET'])
def get_ticker():
    """获取实时价格"""
    symbol = request.args.get('symbol', 'BTC/USDT')
    data = collector.get_ticker(symbol)
    return jsonify(data)

@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    """获取价差和资金费率差分析"""
    symbol = request.args.get('symbol', 'BTC/USDT')
    
    # 获取价格数据
    ticker_data = collector.get_ticker(symbol)
    
    # 获取资金费率
    funding_data = collector.get_funding_rate(symbol)
    
    # 检查是否有错误
    if 'error' in ticker_data:
        return jsonify({'error': '无法获取价格数据，请检查API配置'})
    
    if ticker_data['binance'] and ticker_data['okx']:
        # 计算价差
        price_diff = abs(ticker_data['binance']['last'] - ticker_data['okx']['last'])
        price_diff_percent = (price_diff / ticker_data['binance']['last']) * 100
        
        analysis = {
            'symbol': symbol,
            'price_analysis': {
                'binance_price': ticker_data['binance']['last'],
                'okx_price': ticker_data['okx']['last'],
                'price_difference': price_diff,
                'price_difference_percent': price_diff_percent
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # 检查是否为现货交易对
        if funding_data.get('is_spot', False):
            # 现货交易对只分析价差
            analysis['funding_analysis'] = {
                'note': '现货交易对无资金费率',
                'funding_difference': 0
            }
        elif 'error' in funding_data:
            # 资金费率获取失败
            analysis['funding_analysis'] = {
                'error': funding_data['error'],
                'funding_difference': 0
            }
        else:
            # 合约交易对分析资金费率
            funding_diff = abs(funding_data['binance'].get('funding_rate', 0) - funding_data['okx'].get('funding_rate', 0))
            analysis['funding_analysis'] = {
                'binance_funding': funding_data['binance'].get('funding_rate', 0),
                'okx_funding': funding_data['okx'].get('funding_rate', 0),
                'funding_difference': funding_diff
            }
    else:
        analysis = {'error': '无法获取数据'}
    
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 