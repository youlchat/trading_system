# Cryptocurrency Trading System

A real-time monitoring system for price differences and funding rates between Binance and OKX exchanges, supporting dynamic API configuration.

## Features

- 🔄 **Real-time Data Monitoring**: Simultaneously fetch K-line data, prices, and funding rates from Binance and OKX
- 📊 **Price Difference Analysis**: Calculate price differences between exchanges and identify arbitrage opportunities
- 💰 **Funding Rate Analysis**: Monitor funding rate differences and identify arbitrage directions (contract pairs only)
- 📈 **Visualization Charts**: Use Plotly to create price trends and comparison charts
- ⚙️ **Dynamic API Configuration**: Support frontend dynamic API key configuration updates
- 🔄 **Auto-refresh**: Support scheduled automatic data refresh
- 🎨 **Modern UI**: Responsive design, mobile-friendly
- 📋 **Trading Pair Types**: Support spot and contract trading pairs with automatic identification and adaptive display

## System Architecture

- **Backend**: Flask + CCXT (Python)
- **Frontend**: HTML + JavaScript + Plotly
- **Data Sources**: Binance API + OKX API

## Installation and Setup

### 1. Clone the Project

```bash
git clone <repository-url>
cd trading_system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables (Optional)

Create a `.env` file:

```env
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET=your_binance_secret
OKX_API_KEY=your_okx_api_key
OKX_SECRET=your_okx_secret
OKX_PASSWORD=your_okx_password
```

### 4. Start the System

```bash
# Start backend service
python backend/app.py

# Or use the startup script
./start.sh
```

### 5. Access Frontend

Open your browser and visit `http://localhost:5001` or directly open `frontend/index.html`

## Usage Guide

### 1. Configure API Keys

In the frontend interface:
1. Enter Binance API key and Secret
2. Enter OKX API key, Secret, and Password
3. Click "🔧 Update API Configuration" button

### 2. Select Trading Pair and Timeframe

- Choose trading pairs to monitor:
  - **Spot Trading Pairs** (e.g., `BTC/USDT`): Display price comparison and spread analysis, no funding rates
  - **Contract Trading Pairs** (e.g., `BTC/USDT:USDT`): Display price comparison, spread analysis, and funding rate analysis
- Select timeframe (1 minute to 1 day)
- Click "🔄 Load Data" to get real-time data

### 3. View Analysis Results

The system will display:
- **Price Comparison**: Real-time prices from both exchanges and price differences
- **Funding Rate Comparison**: Funding rates and rate differences
- **Spread Analysis**: Price difference percentage and arbitrage opportunity assessment
- **Funding Rate Analysis**: Rate differences and arbitrage direction recommendations

### 4. Auto-refresh

- Click "▶️ Start Auto-refresh" to enable 30-second interval automatic refresh
- Click "⏹️ Stop Auto-refresh" to stop automatic refresh

## API Endpoints

### Update API Configuration
```
POST /api/update_config
Content-Type: application/json

{
    "binance_api_key": "your_key",
    "binance_secret": "your_secret",
    "okx_api_key": "your_key",
    "okx_secret": "your_secret",
    "okx_password": "your_password"
}
```

### Get Available Trading Pairs
```
GET /api/symbols
```

### Get K-line Data
```
GET /api/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=100
```

### Get Funding Rate
```
GET /api/funding_rate?symbol=BTC/USDT
```

### Get Real-time Price
```
GET /api/ticker?symbol=BTC/USDT
```

### Get Analysis Data
```
GET /api/analysis?symbol=BTC/USDT
```

## Testing

Run the test script to verify system functionality:

```bash
python test_api_config.py
```

## Important Notes

1. **API Permissions**: Ensure API keys have read permissions (no trading permissions required)
2. **Network Connection**: Requires stable network connection to access exchange APIs
3. **Rate Limiting**: System has enabled rate limiting to avoid triggering API restrictions
4. **Data Accuracy**: Spread analysis is for reference only, actual trading should consider transaction fees and other factors
5. **Trading Pair Types**: 
   - Spot trading pairs (e.g., `BTC/USDT`) have no funding rates, only display spread analysis
   - Contract trading pairs (e.g., `BTC/USDT:USDT`) have funding rates, display complete spread and funding rate analysis
6. **Contract Format**: Different exchanges may have different contract formats, recommend using `:USDT` format linear contracts

## Technology Stack

- **Backend**: Python 3.7+, Flask, CCXT, Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Plotly.js
- **Data**: Binance API, OKX API

## License

MIT License

## Contributing

Welcome to submit Issues and Pull Requests!

---

## Multi-language Versions

- [English Version](README_EN.md) - English documentation (current)
- [Nederlandse Versie](README_NL.md) - Nederlandse documentatie
- [中文版本](README.md) - 中文文档 