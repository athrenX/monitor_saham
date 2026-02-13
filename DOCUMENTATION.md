# StockPro AI - Professional Stock Analysis Platform

## 📋 Dokumentasi Lengkap

### 🌟 Fitur Utama

#### 1. **Analisis Real-Time dengan AI** 🎯
- Data harga saham real-time dari Yahoo Finance
- Update otomatis setiap 30 detik
- Support untuk saham Indonesia (IDX) dan internasional (NYSE, NASDAQ)
- Format ticker: `BBCA.JK` (Indonesia), `AAPL` (US)

#### 2. **13 Indikator Teknikal Profesional** 📊
- **RSI (14)**: Relative Strength Index untuk mengukur overbought/oversold
- **MACD (12,26,9)**: Moving Average Convergence Divergence untuk trend
- **Bollinger Bands (20,2)**: Volatilitas dan support/resistance
- **Stochastic (14,3)**: Momentum oscillator
- **ATR (14)**: Average True Range untuk volatilitas
- **Moving Averages**: MA7, MA30, MA50
- **Exponential MA**: EMA9, EMA21, EMA50

#### 3. **AI Multi-Factor Scoring System** 🤖
Sistem scoring otomatis dengan 4 faktor weighted:
- **Trend Analysis (35%)**: Analisis arah pergerakan harga
- **Momentum Signals (30%)**: Kekuatan pergerakan
- **Volume Pattern (20%)**: Konfirmasi dengan volume
- **Volatility Check (15%)**: Risiko dan fluktuasi

**Rekomendasi AI:**
- **STRONG BUY** (90-100): Sinyal beli sangat kuat
- **BUY** (70-89): Sinyal beli
- **HOLD** (40-69): Tahan posisi
- **SELL** (20-39): Sinyal jual
- **STRONG SELL** (0-19): Sinyal jual kuat

#### 4. **Interactive Charts** 📈
- **Line Chart & Candlestick**: Toggle sesuai preferensi
- **Zoom & Pan**: Mouse wheel untuk zoom, Ctrl+Drag untuk pan
- **Zoom Buttons**: +/- untuk zoom in/out, Reset untuk default view
- **Click & Drag**: Pilih area untuk zoom spesifik
- **Responsive**: Otomatis menyesuaikan ukuran layar

#### 5. **Price Alert System** ⏰
- Set target harga dengan kondisi (above/below)
- Notifikasi otomatis via WhatsApp menggunakan Fonnte API
- Auto-check setiap 60 detik
- Welcome message saat membuat alert
- Detailed notification dengan price change percentage

**Cara Menggunakan:**
1. Klik tombol "Set Price Alert" setelah analisis
2. Pilih kondisi: Harga di atas/di bawah target
3. Masukkan target harga (Rp)
4. (Opsional) Masukkan nomor WhatsApp format: 628xxx
5. Klik "Simpan Alert"

#### 6. **Watchlist Management** 👀
- Simpan hingga unlimited saham favorit
- Real-time price updates setiap 30 detik
- Color-coded: hijau (naik), merah (turun)
- Quick analysis: klik ticker untuk analisis instant
- Modal picker dengan 15 saham populer Indonesia
- Search function untuk cari saham cepat
- Custom ticker input manual

**Saham Populer:**
- Banking: BBCA.JK, BBRI.JK, BMRI.JK, BBNI.JK
- Telco: TLKM.JK, ISAT.JK, EXCL.JK
- Consumer: ICBP.JK, INDF.JK, UNVR.JK
- Auto: ASII.JK
- Mining: ANTM.JK, INCO.JK
- Tech: GOTO.JK
- Energy: MEDC.JK

#### 7. **WhatsApp Integration** 📱
- Fonnte API integration
- Automatic welcome message
- Alert triggered notifications dengan detail:
  - Ticker saham
  - Target price vs Current price
  - Percentage change
  - Timestamp
  - Trading suggestions

**Setup WhatsApp:**
1. Register di fonnte.com
2. Dapatkan API token
3. Connect WhatsApp device via QR code
4. Masukkan nomor format: 628123456789 (tanpa +62)

#### 8. **Multi-Language Support** 🌐
- **Bahasa Indonesia**: Default language
- **English**: Full translation
- Toggle via navbar button
- Auto-save preference ke localStorage
- All UI elements translated including:
  - Navigation
  - Indicators
  - AI recommendations
  - Notifications
  - Documentation

#### 9. **Dark/Light Theme** 🎨
- **Dark Mode**: Eye-friendly untuk trading malam
- **Light Mode**: Clear untuk siang hari
- Toggle via navbar
- Smooth transition animations
- Persistent preference

#### 10. **Top Movers** 🚀
- Top Gainers: Saham dengan kenaikan tertinggi
- Top Losers: Saham dengan penurunan tertinggi
- Real-time data
- Quick access untuk analisis

#### 11. **Market News** 📰
- Latest market news
- Fundamental analysis
- Economic indicators
- Company announcements

---

### 📖 Panduan Penggunaan

#### Langkah 1: Analisis Saham
```
1. Masukkan ticker saham di input field
   Contoh: BBCA.JK (Bank BCA), AAPL (Apple Inc.)
   
2. Klik tombol "Analisis Sekarang"
   
3. Tunggu proses analisis (3-5 detik)
   
4. Hasil muncul:
   - Company Info
   - Price Chart
   - Technical Indicators
   - AI Recommendation
   - Signals Analysis
```

#### Langkah 2: Membaca Indikator

**RSI (Relative Strength Index):**
- **> 70**: Overbought (jenuh beli) - potensi koreksi
- **30-70**: Normal range
- **< 30**: Oversold (jenuh jual) - potensi rebound

**MACD:**
- **Crossover di atas zero**: Bullish signal
- **Crossover di bawah zero**: Bearish signal
- **Histogram positif**: Momentum naik
- **Histogram negatif**: Momentum turun

**Bollinger Bands:**
- **Harga di upper band**: Overbought
- **Harga di lower band**: Oversold/support
- **Squeeze (bands sempit)**: Volatilitas rendah, siap breakout
- **Expansion (bands lebar)**: Volatilitas tinggi

**Stochastic:**
- **> 80**: Overbought
- **< 20**: Oversold
- **%K cross %D**: Signal entry/exit

#### Langkah 3: Interpretasi AI Score

**Score Breakdown:**
- **90-100**: Extremely Bullish - Strong Buy signal
- **80-89**: Very Bullish - Buy signal dengan confidence tinggi
- **70-79**: Bullish - Buy signal moderate
- **60-69**: Slightly Bullish - Hold atau accumulate
- **50-59**: Neutral - Wait and see
- **40-49**: Slightly Bearish - Reduce position
- **30-39**: Bearish - Sell signal moderate
- **20-29**: Very Bearish - Sell signal dengan confidence tinggi
- **0-19**: Extremely Bearish - Strong Sell signal

#### Langkah 4: Menggunakan Chart

**Zoom In/Out:**
- Mouse wheel: scroll up/down
- Buttons: klik +/- di header chart
- Touch: pinch gesture di mobile

**Pan/Move:**
- Ctrl + Drag (desktop)
- Two-finger drag (mobile)

**Select Area:**
- Click dan drag tanpa Ctrl untuk zoom area spesifik

**Reset:**
- Klik tombol "Reset Zoom"

#### Langkah 5: Set Price Alert

**Contoh Scenario:**
```
Saham: BBCA.JK
Harga saat ini: Rp 6,500
Target: Rp 7,000 (naik 7.7%)

Setup:
1. Pilih kondisi: "Harga di atas"
2. Target: 7000
3. WhatsApp: 628123456789
4. Simpan

Result:
- Alert created ✅
- Welcome message dikirim ke WA
- Auto-check dimulai
- Notifikasi dikirim saat harga >= 7000
```

---

### 💡 Tips Trading Profesional

#### 1. **Confirmation Strategy**
- Jangan trade berdasarkan 1 indikator saja
- Gunakan minimal 3 indikator untuk konfirmasi
- Perhatikan volume saat breakout
- Check multiple timeframes (5m, 15m, 1h, 1d)

#### 2. **Risk Management**
- **Never invest lebih dari 5% portfolio di 1 saham**
- Set stop loss 2-3% di bawah entry
- Target profit minimum 2:1 risk-reward ratio
- Use position sizing calculator

#### 3. **Entry Timing**
- **Bullish Entry**: RSI > 50, MACD crossover, price > MA20
- **Breakout Entry**: Volume spike + close above resistance
- **Pullback Entry**: Price touch MA support + RSI < 50

#### 4. **Exit Strategy**
- **Take Profit**: Partial sell di resistance level
- **Stop Loss**: Strict 2-3% cut loss
- **Trailing Stop**: Move stop loss naik seiring profit
- **Time Stop**: Exit jika tidak ada movement 3-5 hari

#### 5. **Volume Analysis**
```
High Volume + Green Candle = Strong Buying
High Volume + Red Candle = Strong Selling
Low Volume + Movement = Weak signal (skip)
Volume Spike + Breakout = Valid breakout
```

#### 6. **Candlestick Patterns**
**Bullish:**
- Hammer di support
- Bullish Engulfing
- Morning Star
- Three White Soldiers

**Bearish:**
- Shooting Star di resistance
- Bearish Engulfing
- Evening Star
- Three Black Crows

#### 7. **Market Conditions**
- **Trending Market**: Follow trend, use MA crossovers
- **Ranging Market**: Buy support, sell resistance
- **High Volatility**: Widen stop loss, reduce size
- **Low Volatility**: Prepare untuk breakout

---

### 🔧 Technical Specifications

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Chart.js 4.4.0 with zoom plugin
- Bootstrap Icons 1.11.0
- Tailwind CSS (CDN)
- Google Fonts (Inter, JetBrains Mono)

**Backend:**
- Python 3.11+
- Flask 3.0.0
- yfinance 0.2.36
- pandas 2.2.0, numpy 1.26.3

**APIs:**
- Yahoo Finance API (via yfinance)
- Fonnte WhatsApp API

**Performance:**
- Page load: < 2s
- Chart render: < 1s
- Analysis API: 2-5s
- Real-time updates: 30s interval
- Alert check: 60s interval

**Browser Support:**
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

---

### 🐛 Troubleshooting

#### Problem: "Ticker not found"
**Solution:**
- Check ticker format: `BBCA.JK` (Indonesia), `AAPL` (US)
- Verify ticker exists di Yahoo Finance
- Try alternative ticker symbol

#### Problem: WhatsApp notification tidak diterima
**Solution:**
1. Check Fonnte device status (must be "connected")
2. Verify phone number format: 628xxx (no spaces, no +)
3. Scan QR code di Fonnte dashboard
4. Check token validity (expires 16 March 2026)

#### Problem: Chart tidak muncul
**Solution:**
- Hard refresh: Ctrl+Shift+R
- Clear browser cache
- Check internet connection
- Disable browser extensions (AdBlock)

#### Problem: Harga tidak update
**Solution:**
- Market mungkin tutup (check trading hours)
- Refresh browser
- Check internet connection

---

### 📞 Support & Contact

**Developer:** StockPro AI Team
**Version:** 2.0.0 Professional
**Last Update:** February 2026

**Disclaimer:**
Platform ini untuk educational purposes. Trading saham memiliki risiko. 
Lakukan analisis mandiri dan konsultasi dengan financial advisor sebelum 
mengambil keputusan investasi. Past performance tidak guarantee future results.

---

**Made with ❤️ for Indonesian Traders**
