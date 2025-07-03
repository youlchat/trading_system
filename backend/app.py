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
        self.binance = ccxt.binance({
            'apiKey': os.getenv('BINANCE_API_KEY', ''),
            'secret': os.getenv('BINANCE_SECRET', ''),
            'sandbox': False,
            'enableRateLimit': True
        })
        
        self.okx = ccxt.okx({
            'apiKey': os.getenv('OKX_API_KEY', ''),
            'secret': os.getenv('OKX_SECRET', ''),
            'password': os.getenv('OKX_PASSWORD', ''),
            'sandbox': False,
            'enableRateLimit': True
        })
    
    def get_available_symbols(self):
        """获取可用的交易对"""
        try:
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
            return {'binance': [], 'okx': []}
    
    def get_funding_rate(self, symbol):
        """获取资金费率"""
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
                }
            }
        except Exception as e:
            print(f"获取资金费率失败: {e}")
            return {'binance': {}, 'okx': {}}
    
    def get_ticker(self, symbol):
        """获取实时价格"""
        try:
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
            return {'binance': {}, 'okx': {}}

# 初始化数据收集器
collector = TradingDataCollector()

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
    
    if ticker_data['binance'] and ticker_data['okx']:
        # 计算价差
        price_diff = abs(ticker_data['binance']['last'] - ticker_data['okx']['last'])
        price_diff_percent = (price_diff / ticker_data['binance']['last']) * 100
        
        # 计算资金费率差
        funding_diff = abs(funding_data['binance'].get('funding_rate', 0) - funding_data['okx'].get('funding_rate', 0))
        
        analysis = {
            'symbol': symbol,
            'price_analysis': {
                'binance_price': ticker_data['binance']['last'],
                'okx_price': ticker_data['okx']['last'],
                'price_difference': price_diff,
                'price_difference_percent': price_diff_percent
            },
            'funding_analysis': {
                'binance_funding': funding_data['binance'].get('funding_rate', 0),
                'okx_funding': funding_data['okx'].get('funding_rate', 0),
                'funding_difference': funding_diff
            },
            'timestamp': datetime.now().isoformat()
        }
    else:
        analysis = {'error': '无法获取数据'}
    
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 