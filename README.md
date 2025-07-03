<<<<<<< Updated upstream
<<<<<<< Updated upstream
 # 加密货币交易系统
=======
# 加密货币交易系统
>>>>>>> Stashed changes
=======
# 加密货币交易系统
>>>>>>> Stashed changes

一个实时监控币安和欧易交易所价差与资金费率的交易系统，支持动态API配置。

## 功能特性

- 🔄 **实时数据监控**: 同时获取币安和欧易的K线数据、价格和资金费率
- 📊 **价差分析**: 计算两个交易所之间的价格差异和套利机会
- 💰 **资金费率分析**: 监控资金费率差异，识别套利方向（仅合约交易对）
- 📈 **可视化图表**: 使用Plotly绘制价格走势和对比图表
- ⚙️ **动态API配置**: 支持前端动态更新API密钥配置
- 🔄 **自动刷新**: 支持定时自动刷新数据
- 🎨 **现代化UI**: 响应式设计，支持移动端
- 📋 **交易对类型**: 支持现货和合约交易对，自动识别并适配显示内容

## 系统架构

- **后端**: Flask + CCXT (Python)
- **前端**: HTML + JavaScript + Plotly
- **数据源**: 币安(Binance) + 欧易(OKX) API

## 安装和运行

### 1. 克隆项目

```bash
git clone <repository-url>
cd trading_system
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量（可选）

创建 `.env` 文件：

```env
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET=your_binance_secret
OKX_API_KEY=your_okx_api_key
OKX_SECRET=your_okx_secret
OKX_PASSWORD=your_okx_password
```

### 4. 启动系统

```bash
# 启动后端服务
python backend/app.py

# 或者使用启动脚本
./start.sh
```

### 5. 访问前端

打开浏览器访问 `http://localhost:5001` 或直接打开 `frontend/index.html`

## 使用方法

### 1. 配置API密钥

在前端界面中：
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
1. 输入币安API密钥和Secret
2. 输入欧易API密钥、Secret和Password
3. 点击"🔧 更新API配置"按钮

### 2. 选择交易对和时间周期

- 选择要监控的交易对：
  - **现货交易对**（如 `BTC/USDT`）：显示价格对比和价差分析，无资金费率
  - **合约交易对**（如 `BTC/USDT:USDT`）：显示价格对比、价差分析和资金费率分析
- 选择时间周期（1分钟到1天）
- 点击"🔄 加载数据"获取实时数据

### 3. 查看分析结果

系统会显示：
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
- **价格对比**: 两个交易所的实时价格和价差
- **资金费率对比**: 资金费率和费率差
- **价差分析**: 价差百分比和套利机会评估
- **资金费率分析**: 费率差和套利方向建议

### 4. 自动刷新

- 点击"▶️ 开始自动刷新"启动30秒间隔的自动刷新
- 点击"⏹️ 停止自动刷新"停止自动刷新

## API接口

### 更新API配置
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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

### 获取交易对
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
```
GET /api/symbols
```

### 获取K线数据
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
```
GET /api/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=100
```

### 获取资金费率
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
```
GET /api/funding_rate?symbol=BTC/USDT
```

### 获取实时价格
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
```
GET /api/ticker?symbol=BTC/USDT
```

### 获取分析数据
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
```
GET /api/analysis?symbol=BTC/USDT
```

## 测试

运行测试脚本验证系统功能：

```bash
python test_api_config.py
```

## 注意事项

1. **API权限**: 确保API密钥具有读取权限（不需要交易权限）
2. **网络连接**: 需要稳定的网络连接访问交易所API
3. **频率限制**: 系统已启用频率限制，避免触发API限制
4. **数据准确性**: 价差分析仅供参考，实际交易需考虑手续费等因素
<<<<<<< Updated upstream
<<<<<<< Updated upstream
5. **交易对类型**:
=======
5. **交易对类型**: 
>>>>>>> Stashed changes
=======
5. **交易对类型**: 
>>>>>>> Stashed changes
   - 现货交易对（如 `BTC/USDT`）没有资金费率，只显示价差分析
   - 合约交易对（如 `BTC/USDT:USDT`）有资金费率，显示完整的价差和资金费率分析
6. **合约格式**: 不同交易所的合约格式可能不同，建议使用 `:USDT` 格式的线性合约

## 技术栈

- **后端**: Python 3.7+, Flask, CCXT, Pandas, NumPy
- **前端**: HTML5, CSS3, JavaScript ES6+, Plotly.js
- **数据**: 币安API, 欧易API

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes

---

## 多语言版本 / Multi-language Versions

- [English Version](README_EN.md) - English documentation
- [Nederlandse Versie](README_NL.md) - Nederlandse documentatie
<<<<<<< Updated upstream
- [中文版本](README.md) - 中文文档（当前版本） 
>>>>>>> Stashed changes
=======
- [中文版本](README.md) - 中文文档（当前版本） 
>>>>>>> Stashed changes
