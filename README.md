# 🚀 MarketPulse Pro - AI Stock Analysis Platform

Platform analisis saham dengan AI yang super gacor! Menampilkan 13 indikator teknikal, multi-factor scoring, pattern recognition, dan fitur-fitur premium.

## ✨ Fitur Unggulan

### 📊 Analisis Teknikal Lengkap
- **13 Indikator**: RSI, MACD, Bollinger Bands, Stochastic, ATR, MA (7/30/50), EMA (9/21/50)
- **AI Multi-Factor Scoring**: 4 faktor weighted analysis (Trend, Momentum, Volume, Volatility)
- **Pattern Recognition**: ML-like prediction dengan confidence score
- **Support & Resistance**: Auto-calculated dengan target prices

### 🎯 Fitur Premium
- ⭐ **Watchlist**: Save favorite stocks dengan quick access
- 🔔 **Price Alerts**: Set target harga dengan notifikasi
- 📊 **Candlestick Chart**: Toggle antara line chart dan candlestick
- 🔥 **Top Movers**: Real-time top gainers & losers
- 📈 **Real-time Ticker Tape**: Live price updates untuk 7 saham populer

### 🎨 User Experience
- 🌓 Dark/Light theme toggle
- 📱 Fully responsive design (mobile-friendly)
- ⚡ Auto-refresh setiap 30 detik
- 🎭 Professional animations & transitions
- 💎 Modern gradient UI design

## 🛠️ Tech Stack

- **Backend**: Python Flask 3.0
- **Data Source**: Yahoo Finance API (yfinance)
- **Analysis**: Pandas, NumPy
- **Frontend**: Vanilla JavaScript, Chart.js
- **Styling**: Tailwind CSS, Bootstrap Icons
- **Hosting**: Vercel Serverless

## 📦 Installation

### Local Development

1. Clone repository:
```bash
git clone <your-repo-url>
cd TRADING
```

2. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run application:
```bash
python app_simple.py
```

5. Open browser:
```
http://localhost:5001
```

## 🚀 Deploy ke Vercel

### Prerequisites
- Akun Vercel (https://vercel.com)
- Git installed
- Vercel CLI (optional)

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push ke GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Login ke Vercel**:
   - Buka https://vercel.com
   - Sign up/Login dengan GitHub

3. **Import Project**:
   - Klik "Add New Project"
   - Pilih repository Anda
   - Vercel akan auto-detect konfigurasi

4. **Deploy**:
   - Klik "Deploy"
   - Wait for build (2-3 minutes)
   - Get your live URL!

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Login**:
```bash
vercel login
```

3. **Deploy**:
```bash
vercel
```

4. **Follow prompts**:
   - Set up and deploy? Y
   - Which scope? (your account)
   - Link to existing project? N
   - Project name? (enter name)
   - Directory? ./
   - Override settings? N

5. **Production Deploy**:
```bash
vercel --prod
```

## 📝 Configuration

### Environment Variables (Optional)
Jika butuh custom configuration, tambahkan di Vercel Dashboard:

```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

### vercel.json
File sudah dikonfigurasi untuk Python Flask:
- Auto-routing ke app_simple.py
- Python runtime optimization
- Static file handling

## 📱 API Endpoints

### Stock Analysis
```
POST /api/analyze-simple
Body: { "ticker": "BBCA.JK" }
```

### Watchlist
```
GET /api/watchlist
POST /api/watchlist/add
POST /api/watchlist/remove
```

### Price Alerts
```
GET /api/alerts
POST /api/alerts/add
POST /api/alerts/remove
```

### Top Movers
```
GET /api/top-movers
```

### Candlestick Data
```
POST /api/candlestick
Body: { "ticker": "BBCA.JK", "period": "1mo" }
```

## 🎯 Supported Tickers

### Indonesia (IDX)
- BBCA.JK, BBRI.JK, BMRI.JK (Banking)
- TLKM.JK (Telecom)
- ASII.JK (Automotive)
- GOTO.JK (Tech)
- UNVR.JK, ICBP.JK, INDF.JK (Consumer)
- KLBF.JK (Healthcare)

### US Markets
- AAPL, MSFT, GOOGL (Tech)
- TSLA (EV)
- AMZN (E-commerce)
- Dan ribuan ticker lainnya

## 🤝 Contributing

Created by **Athala Angyn Renaldi**
Email: angwynren@gmail.com

## 📄 License

MIT License - feel free to use for your projects!

## 🐛 Known Issues

- Vercel free tier has 10s execution limit
- Some tickers might have delayed data
- Historical data limited by Yahoo Finance API

## 🔮 Future Features

- [ ] Portfolio tracking dengan P&L
- [ ] News sentiment analysis
- [ ] Backtesting strategies
- [ ] Social features (comments, sharing)
- [ ] More technical indicators (Fibonacci, Ichimoku)
- [ ] Email notifications untuk alerts
- [ ] Multi-timeframe analysis

## 📞 Support

Jika ada masalah atau pertanyaan:
- Email: angwynren@gmail.com
- Issues: GitHub Issues
- Telegram: @athal_saham_monitor_bot

---

Made with ❤️ by Athala Angyn Renaldi
