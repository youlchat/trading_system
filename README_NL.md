# Cryptocurrency Handelsysteem

Een real-time monitoring systeem voor prijsverschillen en funding rates tussen Binance en OKX beurzen, met ondersteuning voor dynamische API-configuratie.

## Functies

- 🔄 **Real-time Data Monitoring**: Gelijktijdig K-line data, prijzen en funding rates ophalen van Binance en OKX
- 📊 **Prijsverschil Analyse**: Bereken prijsverschillen tussen beurzen en identificeer arbitrage mogelijkheden
- 💰 **Funding Rate Analyse**: Monitor funding rate verschillen en identificeer arbitrage richtingen (alleen contract paren)
- 📈 **Visualisatie Grafieken**: Gebruik Plotly om prijstrends en vergelijkingsgrafieken te maken
- ⚙️ **Dynamische API Configuratie**: Ondersteuning voor frontend dynamische API sleutel configuratie updates
- 🔄 **Auto-refresh**: Ondersteuning voor geplande automatische data vernieuwing
- 🎨 **Moderne UI**: Responsive design, mobiel-vriendelijk
- 📋 **Handelspaar Types**: Ondersteuning voor spot en contract handelsparen met automatische identificatie en adaptieve weergave

## Systeem Architectuur

- **Backend**: Flask + CCXT (Python)
- **Frontend**: HTML + JavaScript + Plotly
- **Data Bronnen**: Binance API + OKX API

## Installatie en Setup

### 1. Project Klonen

```bash
git clone <repository-url>
cd trading_system
```

### 2. Dependencies Installeren

```bash
pip install -r requirements.txt
```

### 3. Omgevingsvariabelen Configureren (Optioneel)

Maak een `.env` bestand aan:

```env
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET=your_binance_secret
OKX_API_KEY=your_okx_api_key
OKX_SECRET=your_okx_secret
OKX_PASSWORD=your_okx_password
```

### 4. Systeem Starten

```bash
# Backend service starten
python backend/app.py

# Of gebruik het startup script
./start.sh
```

### 5. Frontend Toegang

Open je browser en ga naar `http://localhost:5001` of open direct `frontend/index.html`

## Gebruiksgids

### 1. API Sleutels Configureren

In de frontend interface:
1. Voer Binance API sleutel en Secret in
2. Voer OKX API sleutel, Secret en Password in
3. Klik op "🔧 Update API Configuratie" knop

### 2. Handelspaar en Tijdsframe Selecteren

- Kies handelsparen om te monitoren:
  - **Spot Handelsparen** (bijv. `BTC/USDT`): Toon prijsvergelijking en spread analyse, geen funding rates
  - **Contract Handelsparen** (bijv. `BTC/USDT:USDT`): Toon prijsvergelijking, spread analyse en funding rate analyse
- Selecteer tijdsframe (1 minuut tot 1 dag)
- Klik op "🔄 Data Laden" om real-time data te krijgen

### 3. Analyse Resultaten Bekijken

Het systeem zal tonen:
- **Prijsvergelijking**: Real-time prijzen van beide beurzen en prijsverschillen
- **Funding Rate Vergelijking**: Funding rates en rate verschillen
- **Spread Analyse**: Prijsverschil percentage en arbitrage mogelijkheid beoordeling
- **Funding Rate Analyse**: Rate verschillen en arbitrage richting aanbevelingen

### 4. Auto-refresh

- Klik op "▶️ Start Auto-refresh" om 30-seconden interval automatische vernieuwing in te schakelen
- Klik op "⏹️ Stop Auto-refresh" om automatische vernieuwing te stoppen

## API Endpoints

### API Configuratie Bijwerken
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

### Beschikbare Handelsparen Ophalen
```
GET /api/symbols
```

### K-line Data Ophalen
```
GET /api/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=100
```

### Funding Rate Ophalen
```
GET /api/funding_rate?symbol=BTC/USDT
```

### Real-time Prijs Ophalen
```
GET /api/ticker?symbol=BTC/USDT
```

### Analyse Data Ophalen
```
GET /api/analysis?symbol=BTC/USDT
```

## Testen

Voer het test script uit om systeem functionaliteit te verifiëren:

```bash
python test_api_config.py
```

## Belangrijke Opmerkingen

1. **API Permissies**: Zorg ervoor dat API sleutels leesrechten hebben (geen handelsrechten vereist)
2. **Netwerk Verbinding**: Vereist stabiele netwerkverbinding om beurs APIs te benaderen
3. **Rate Limiting**: Systeem heeft rate limiting ingeschakeld om API restricties te voorkomen
4. **Data Nauwkeurigheid**: Spread analyse is alleen voor referentie, daadwerkelijke handel moet transactiekosten en andere factoren overwegen
5. **Handelspaar Types**: 
   - Spot handelsparen (bijv. `BTC/USDT`) hebben geen funding rates, tonen alleen spread analyse
   - Contract handelsparen (bijv. `BTC/USDT:USDT`) hebben funding rates, tonen complete spread en funding rate analyse
6. **Contract Formaat**: Verschillende beurzen kunnen verschillende contract formaten hebben, raad aan om `:USDT` formaat lineaire contracten te gebruiken

## Technologie Stack

- **Backend**: Python 3.7+, Flask, CCXT, Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Plotly.js
- **Data**: Binance API, OKX API

## Licentie

MIT Licentie

## Bijdragen

Welkom om Issues en Pull Requests in te dienen!

---

## Multi-language Versions

- [English Version](README_EN.md) - English documentation
- [Nederlandse Versie](README_NL.md) - Nederlandse documentatie (huidige)
- [中文版本](README.md) - 中文文档 