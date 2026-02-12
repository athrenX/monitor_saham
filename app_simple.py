from flask import Flask, render_template, jsonify, request, session
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import json
import os
warnings.filterwarnings('ignore')

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Persistent storage files
WATCHLIST_FILE = 'data/watchlist.json'
ALERTS_FILE = 'data/alerts.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize data files if they don't exist
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(ALERTS_FILE):
    with open(ALERTS_FILE, 'w') as f:
        json.dump([], f)

# === AI-POWERED ANALYSIS FUNCTIONS ===
def calculate_advanced_signals(df, close_series, high_series, low_series):
    """Advanced multi-indicator signal generation"""
    signals = {
        'trend_strength': 0,
        'momentum_score': 0,
        'volume_score': 0,
        'volatility_score': 0,
        'overall_score': 0
    }
    
    # Trend Strength (EMA crossovers)
    ema_9 = close_series.ewm(span=9).mean()
    ema_21 = close_series.ewm(span=21).mean()
    ema_50 = close_series.ewm(span=50).mean()
    
    ema9_val = float(ema_9.iloc[-1])
    ema21_val = float(ema_21.iloc[-1])
    ema50_val = float(ema_50.iloc[-1])
    
    if ema9_val > ema21_val > ema50_val:
        signals['trend_strength'] = 100  # Strong uptrend
    elif ema9_val < ema21_val < ema50_val:
        signals['trend_strength'] = 0   # Strong downtrend
    else:
        signals['trend_strength'] = 50  # Sideways
    
    # Momentum Score (RSI + MACD)
    rsi_series = calculate_rsi(close_series)
    rsi = float(rsi_series.iloc[-1]) if not rsi_series.empty else 50.0
    if rsi < 30:
        signals['momentum_score'] = 90  # Oversold - buy signal
    elif rsi > 70:
        signals['momentum_score'] = 10  # Overbought - sell signal
    else:
        signals['momentum_score'] = 50
    
    # Volume Score
    current_vol = df['Volume'].iloc[-1]
    avg_vol = df['Volume'].rolling(20).mean().iloc[-1]
    vol_ratio = float(current_vol / avg_vol) if avg_vol > 0 else 1.0
    if vol_ratio > 1.5:
        signals['volume_score'] = 80  # High volume
    elif vol_ratio > 1.0:
        signals['volume_score'] = 60
    else:
        signals['volume_score'] = 30
    
    # Volatility Score (ATR-based)
    high_low = high_series - low_series
    high_close = np.abs(high_series - close_series.shift())
    low_close = np.abs(low_series - close_series.shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr_series = true_range.rolling(14).mean()
    atr = float(atr_series.iloc[-1]) if not atr_series.empty else 0.0
    current_price = float(close_series.iloc[-1])
    atr_pct = (atr / current_price) * 100 if current_price > 0 else 0.0
    
    if atr_pct < 2:
        signals['volatility_score'] = 70  # Low volatility - stable
    elif atr_pct > 5:
        signals['volatility_score'] = 30  # High volatility - risky
    else:
        signals['volatility_score'] = 50
    
    # Overall Score (weighted average)
    signals['overall_score'] = int(
        signals['trend_strength'] * 0.35 +
        signals['momentum_score'] * 0.30 +
        signals['volume_score'] * 0.20 +
        signals['volatility_score'] * 0.15
    )
    
    return signals

def predict_next_move(df, close_series, high_series, low_series):
    """Simple ML-like prediction based on pattern recognition"""
    # Get recent price changes
    returns = close_series.pct_change().tail(10)
    avg_return = returns.mean()
    volatility = returns.std()
    
    # Calculate support/resistance
    support = float(low_series.tail(30).min())
    resistance = float(high_series.tail(30).max())
    current = float(close_series.iloc[-1])
    
    # Position in range
    range_position = (current - support) / (resistance - support) if resistance > support else 0.5
    
    # Prediction logic
    if avg_return > 0.01 and range_position < 0.4:
        prediction = "NAIK"
        confidence = min(85, int(70 + (0.4 - range_position) * 100))
    elif avg_return < -0.01 and range_position > 0.6:
        prediction = "TURUN"
        confidence = min(85, int(70 + (range_position - 0.6) * 100))
    else:
        prediction = "SIDEWAYS"
        confidence = 60
    
    return {
        'direction': prediction,
        'confidence': confidence,
        'support': support,
        'resistance': resistance,
        'target_up': resistance * 1.02,
        'target_down': support * 0.98
    }

# === FUNGSI INDIKATOR (Enhanced) ===
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_moving_average(data, window):
    return data.rolling(window=window).mean()

def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD indicator"""
    ema_fast = data.ewm(span=fast).mean()
    ema_slow = data.ewm(span=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(data, window=20, num_std=2):
    """Calculate Bollinger Bands"""
    sma = data.rolling(window=window).mean()
    std = data.rolling(window=window).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return upper_band, sma, lower_band

def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    """Calculate Stochastic Oscillator"""
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d = k.rolling(window=d_period).mean()
    return k, d

def calculate_atr(high, low, close, period=14):
    """Calculate Average True Range"""
    high_low = high - low
    high_close = np.abs(high - close.shift())
    low_close = np.abs(low - close.shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(period).mean()
    return atr

def to_float(val):
    """Convert pandas value to float safely"""
    # If it's a Series, get the first value
    if hasattr(val, 'iloc'):
        val = val.iloc[0] if len(val) > 0 else 0.0
    # If it's a numpy array, get the first element
    if hasattr(val, 'values'):
        val = val.values[0] if len(val.values) > 0 else 0.0
    # Convert to float
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0

def analyze_stock_simple(ticker):
    """Analisis saham versi sederhana untuk orang awam"""
    try:
        # Download data 3 bulan
        df = yf.download(ticker, period="3mo", interval="1d", progress=False)
        
        if df.empty:
            return {"error": "Kode saham tidak ditemukan. Pastikan kode benar (contoh: BBCA.JK untuk saham Indonesia)"}
        
        # Ensure we're working with Series, not DataFrame
        # If multi-level columns exist, flatten them
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # Get Close price as Series
        close_series = df['Close'].squeeze() if hasattr(df['Close'], 'squeeze') else df['Close']
        high_series = df['High'].squeeze() if hasattr(df['High'], 'squeeze') else df['High']
        low_series = df['Low'].squeeze() if hasattr(df['Low'], 'squeeze') else df['Low']
        
        # Hitung indikator sederhana
        df['MA7'] = calculate_moving_average(close_series, 7)   # Rata-rata 1 minggu
        df['MA30'] = calculate_moving_average(close_series, 30) # Rata-rata 1 bulan
        df['MA50'] = calculate_moving_average(close_series, 50) # Rata-rata 50 hari
        df['RSI'] = calculate_rsi(close_series)
        
        # Advanced indicators
        df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = calculate_macd(close_series)
        df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = calculate_bollinger_bands(close_series)
        df['Stoch_K'], df['Stoch_D'] = calculate_stochastic(high_series, low_series, close_series)
        df['ATR'] = calculate_atr(high_series, low_series, close_series)
        
        # EMA for trend analysis
        df['EMA9'] = close_series.ewm(span=9).mean()
        df['EMA21'] = close_series.ewm(span=21).mean()
        df['EMA50'] = close_series.ewm(span=50).mean()
        
        # Data terkini
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        harga_sekarang = to_float(latest['Close'])
        harga_kemarin = to_float(prev['Close'])
        perubahan = harga_sekarang - harga_kemarin
        perubahan_persen = (perubahan / harga_kemarin) * 100
        
        # Harga tertinggi dan terendah 30 hari terakhir
        harga_tertinggi_30d = to_float(df['High'].tail(30).max())
        harga_terendah_30d = to_float(df['Low'].tail(30).min())
        
        # Rata-rata harga
        ma7 = to_float(latest['MA7'])
        ma30 = to_float(latest['MA30'])
        ma50 = to_float(latest['MA50'])
        rsi = to_float(latest['RSI'])
        
        # Advanced indicators
        macd = to_float(latest['MACD'])
        macd_signal = to_float(latest['MACD_Signal'])
        macd_hist = to_float(latest['MACD_Hist'])
        bb_upper = to_float(latest['BB_Upper'])
        bb_lower = to_float(latest['BB_Lower'])
        bb_middle = to_float(latest['BB_Middle'])
        stoch_k = to_float(latest['Stoch_K'])
        stoch_d = to_float(latest['Stoch_D'])
        atr = to_float(latest['ATR'])
        
        # EMA values
        ema9 = to_float(latest['EMA9'])
        ema21 = to_float(latest['EMA21'])
        ema50 = to_float(latest['EMA50'])
        
        # Volume
        volume_sekarang = to_float(latest['Volume'])
        volume_rata = to_float(df['Volume'].tail(20).mean())
        volume_ratio = volume_sekarang / volume_rata if volume_rata > 0 else 0
        
        # === ANALISIS SEDERHANA ===
        
        # 1. Posisi Harga (Murah/Mahal relatif)
        range_30d = harga_tertinggi_30d - harga_terendah_30d
        posisi_harga_pct = ((harga_sekarang - harga_terendah_30d) / range_30d * 100) if range_30d > 0 else 50
        
        if posisi_harga_pct < 30:
            posisi_harga = "MURAH"
            posisi_warna = "success"
            posisi_emoji = "🟢"
            posisi_desc = "Harga saat ini mendekati harga terendah 30 hari terakhir. Bisa jadi peluang beli!"
        elif posisi_harga_pct > 70:
            posisi_harga = "MAHAL"
            posisi_warna = "danger"
            posisi_emoji = "🔴"
            posisi_desc = "Harga saat ini mendekati harga tertinggi 30 hari terakhir. Hati-hati membeli di posisi ini."
        else:
            posisi_harga = "NORMAL"
            posisi_warna = "warning"
            posisi_emoji = "🟡"
            posisi_desc = "Harga berada di tengah-tengah range 30 hari terakhir."
        
        # 2. Trend (Naik/Turun)
        if harga_sekarang > ma7 > ma30:
            trend = "NAIK KUAT"
            trend_warna = "success"
            trend_emoji = "📈"
            trend_desc = "Harga di atas rata-rata 1 minggu dan 1 bulan. Trend sedang bagus!"
        elif harga_sekarang > ma30:
            trend = "NAIK"
            trend_warna = "info"
            trend_emoji = "📊"
            trend_desc = "Harga di atas rata-rata 1 bulan. Trend masih positif."
        elif harga_sekarang < ma7 < ma30:
            trend = "TURUN KUAT"
            trend_warna = "danger"
            trend_emoji = "📉"
            trend_desc = "Harga di bawah rata-rata 1 minggu dan 1 bulan. Trend sedang lemah."
        else:
            trend = "SIDEWAYS"
            trend_warna = "secondary"
            trend_emoji = "➡️"
            trend_desc = "Harga bergerak mendatar, belum ada trend jelas."
        
        # 3. Momentum (Kekuatan Beli/Jual)
        if rsi < 30:
            momentum = "OVERSOLD - Banyak yang Jual"
            momentum_warna = "success"
            momentum_emoji = "🎯"
            momentum_desc = "Sudah terlalu banyak yang jual. Biasanya akan rebound (naik lagi)."
            momentum_score = 80
        elif rsi > 70:
            momentum = "OVERBOUGHT - Banyak yang Beli"
            momentum_warna = "danger"
            momentum_emoji = "⚠️"
            momentum_desc = "Sudah terlalu banyak yang beli. Hati-hati kemungkinan koreksi (turun)."
            momentum_score = 20
        else:
            momentum = "NETRAL"
            momentum_warna = "info"
            momentum_emoji = "✅"
            momentum_desc = "Kondisi normal, tidak terlalu ramai beli atau jual."
            momentum_score = 50
        
        # 4. Volume Trading
        if volume_ratio > 1.5:
            volume_status = "SANGAT RAMAI"
            volume_desc = "Volume perdagangan jauh di atas normal. Ada aktivitas besar!"
            volume_emoji = "🔥"
        elif volume_ratio > 1.0:
            volume_status = "RAMAI"
            volume_desc = "Volume perdagangan di atas rata-rata."
            volume_emoji = "📊"
        else:
            volume_status = "SEPI"
            volume_desc = "Volume perdagangan di bawah rata-rata."
            volume_emoji = "😴"
        
        # 5. AI-POWERED REKOMENDASI
        ai_signals = calculate_advanced_signals(df, close_series, high_series, low_series)
        prediction = predict_next_move(df, close_series, high_series, low_series)
        
        score_beli = 0
        score_jual = 0
        alasan = []
        
        # AI Overall Score Analysis
        if ai_signals['overall_score'] >= 70:
            score_beli += 3
            alasan.append(f"🤖 AI Score: {ai_signals['overall_score']}/100 - Signal BELI kuat")
        elif ai_signals['overall_score'] <= 30:
            score_jual += 3
            alasan.append(f"🤖 AI Score: {ai_signals['overall_score']}/100 - Signal JUAL kuat")
        
        # Prediction Analysis
        if prediction['direction'] == 'NAIK' and prediction['confidence'] > 70:
            score_beli += 2
            alasan.append(f"📈 AI Prediksi NAIK (Confidence: {prediction['confidence']}%)")
        elif prediction['direction'] == 'TURUN' and prediction['confidence'] > 70:
            score_jual += 2
            alasan.append(f"📉 AI Prediksi TURUN (Confidence: {prediction['confidence']}%)")
        
        # Cek dari posisi harga
        if posisi_harga_pct < 30:
            score_beli += 2
            alasan.append("✅ Harga sedang murah (dekat posisi terendah)")
        elif posisi_harga_pct > 70:
            score_jual += 2
            alasan.append("⚠️ Harga sudah mahal (dekat posisi tertinggi)")
        
        # Cek dari trend
        if harga_sekarang > ma7 > ma30:
            score_beli += 2
            alasan.append("✅ Trend naik kuat")
        elif harga_sekarang < ma7 < ma30:
            score_jual += 2
            alasan.append("⚠️ Trend turun kuat")
        
        # Cek dari RSI
        if rsi < 30:
            score_beli += 3
            alasan.append("✅ RSI oversold (peluang rebound)")
        elif rsi > 70:
            score_jual += 3
            alasan.append("⚠️ RSI overbought (risiko koreksi)")
        
        # Cek perubahan harga
        if perubahan_persen > 2:
            alasan.append(f"📈 Naik {perubahan_persen:.2f}% hari ini")
        elif perubahan_persen < -2:
            alasan.append(f"📉 Turun {perubahan_persen:.2f}% hari ini")
        
        # Support & Resistance from prediction
        alasan.append(f"📍 Support: Rp {prediction['support']:,.0f} | Resistance: Rp {prediction['resistance']:,.0f}")
        
        # Tentukan rekomendasi (Enhanced dengan AI)
        total_score = score_beli - score_jual
        
        if total_score >= 5 or (score_beli >= 4 and ai_signals['overall_score'] >= 65):
            rekomendasi = "STRONG BUY 🚀"
            rekomendasi_emoji = "🟢"
            rekomendasi_warna = "success"
            rekomendasi_desc = "AI dan semua indikator menunjukkan BELI KUAT! Peluang bagus untuk entry."
        elif score_beli >= 4:
            rekomendasi = "BELI"
            rekomendasi_emoji = "🟢"
            rekomendasi_warna = "success"
            rekomendasi_desc = "Kondisi bagus untuk membeli. Banyak indikator positif!"
        elif total_score <= -5 or (score_jual >= 4 and ai_signals['overall_score'] <= 35):
            rekomendasi = "STRONG SELL 🔻"
            rekomendasi_emoji = "🔴"
            rekomendasi_warna = "danger"
            rekomendasi_desc = "AI dan indikator menunjukkan JUAL KUAT! Pertimbangkan cut loss atau take profit."
        elif score_jual >= 4:
            rekomendasi = "JUAL"
            rekomendasi_emoji = "🔴"
            rekomendasi_warna = "danger"
            rekomendasi_desc = "Sebaiknya jual atau tunggu dulu. Banyak sinyal negatif."
        elif score_beli > score_jual:
            rekomendasi = "PERTIMBANGKAN BELI"
            rekomendasi_emoji = "🟡"
            rekomendasi_warna = "warning"
            rekomendasi_desc = "Ada beberapa sinyal positif, tapi belum kuat. Lakukan riset lebih lanjut."
        else:
            rekomendasi = "TUNGGU DULU / HOLD"
            rekomendasi_emoji = "⚪"
            rekomendasi_warna = "secondary"
            rekomendasi_desc = "Belum ada sinyal jelas. Lebih baik tunggu momentum yang lebih bagus."
        
        if len(alasan) == 0:
            alasan.append("📊 Kondisi pasar normal, tidak ada sinyal khusus.")
        
        # Chart data
        chart_data = df.tail(60)
        chart_dates = [d.strftime('%d %b') for d in chart_data.index]
        chart_prices = chart_data['Close'].values.tolist()
        chart_volumes = chart_data['Volume'].values.tolist()
        chart_ma7 = chart_data['MA7'].fillna(0).values.tolist()
        chart_ma30 = chart_data['MA30'].fillna(0).values.tolist()
        
        # Info perusahaan
        try:
            stock_info = yf.Ticker(ticker)
            info = stock_info.info
            nama_perusahaan = info.get('longName', info.get('shortName', ticker))
        except:
            nama_perusahaan = ticker
        
        return {
            "success": True,
            "ticker": ticker,
            "nama_perusahaan": nama_perusahaan,
            "timestamp": datetime.now().strftime('%d %B %Y, %H:%M'),
            "harga": {
                "sekarang": harga_sekarang,
                "kemarin": harga_kemarin,
                "perubahan": perubahan,
                "perubahan_persen": perubahan_persen,
                "tertinggi_30d": harga_tertinggi_30d,
                "terendah_30d": harga_terendah_30d,
                "volume": int(volume_sekarang),
                "volume_avg": int(volume_rata),
                "volume_status": volume_status,
                "volume_desc": volume_desc,
                "volume_emoji": volume_emoji
            },
            "ai_signals": {
                "overall_score": ai_signals['overall_score'],
                "trend_strength": ai_signals['trend_strength'],
                "momentum_score": ai_signals['momentum_score'],
                "volume_score": ai_signals['volume_score'],
                "volatility_score": ai_signals['volatility_score']
            },
            "prediction": prediction,
            "indikator": {
                "rsi": rsi,
                "macd": macd,
                "macd_signal": macd_signal,
                "macd_hist": macd_hist,
                "bb_upper": bb_upper,
                "bb_middle": bb_middle,
                "bb_lower": bb_lower,
                "stoch_k": stoch_k,
                "stoch_d": stoch_d,
                "atr": atr,
                "ema9": ema9,
                "ema21": ema21,
                "ema50": ema50
            },
            "analisis": {
                "posisi_harga": posisi_harga,
                "posisi_warna": posisi_warna,
                "posisi_emoji": posisi_emoji,
                "posisi_desc": posisi_desc,
                "posisi_pct": posisi_harga_pct,
                
                "trend": trend,
                "trend_warna": trend_warna,
                "trend_emoji": trend_emoji,
                "trend_desc": trend_desc,
                
                "momentum": momentum,
                "momentum_warna": momentum_warna,
                "momentum_emoji": momentum_emoji,
                "momentum_desc": momentum_desc,
                "momentum_score": momentum_score,
                "rsi_value": rsi,
                
                "rekomendasi": rekomendasi,
                "rekomendasi_emoji": rekomendasi_emoji,
                "rekomendasi_warna": rekomendasi_warna,
                "rekomendasi_desc": rekomendasi_desc,
                "alasan": alasan
            },
            "chart": {
                "dates": chart_dates,
                "prices": chart_prices,
                "volumes": chart_volumes,
                "ma7": chart_ma7,
                "ma30": chart_ma30
            }
        }
    
    except Exception as e:
        return {"error": f"Terjadi kesalahan: {str(e)}"}

@app.route('/')
def index():
    return render_template('commercial.html')

@app.route('/commercial')
def commercial():
    return render_template('commercial.html')

@app.route('/api/analyze-simple', methods=['POST'])
def api_analyze_simple():
    data = request.get_json()
    ticker = data.get('ticker', 'TLKM.JK')
    result = analyze_stock_simple(ticker)
    return jsonify(result)

# === WATCHLIST API ===
@app.route('/api/watchlist', methods=['GET'])
def get_watchlist():
    """Get user's watchlist"""
    try:
        with open(WATCHLIST_FILE, 'r') as f:
            watchlist = json.load(f)
        return jsonify({'watchlist': watchlist})
    except:
        return jsonify({'watchlist': []})

@app.route('/api/watchlist/add', methods=['POST'])
def add_to_watchlist():
    """Add stock to watchlist"""
    data = request.get_json()
    ticker = data.get('ticker', '').upper()
    
    try:
        with open(WATCHLIST_FILE, 'r') as f:
            watchlist = json.load(f)
        
        if ticker not in watchlist:
            watchlist.append(ticker)
            with open(WATCHLIST_FILE, 'w') as f:
                json.dump(watchlist, f)
            return jsonify({'success': True, 'message': f'{ticker} ditambahkan ke watchlist'})
        else:
            return jsonify({'success': False, 'message': f'{ticker} sudah ada di watchlist'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/watchlist/remove', methods=['POST'])
def remove_from_watchlist():
    """Remove stock from watchlist"""
    data = request.get_json()
    ticker = data.get('ticker', '').upper()
    
    try:
        with open(WATCHLIST_FILE, 'r') as f:
            watchlist = json.load(f)
        
        if ticker in watchlist:
            watchlist.remove(ticker)
            with open(WATCHLIST_FILE, 'w') as f:
                json.dump(watchlist, f)
            return jsonify({'success': True, 'message': f'{ticker} dihapus dari watchlist'})
        else:
            return jsonify({'success': False, 'message': f'{ticker} tidak ada di watchlist'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# === ALERTS API ===
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get user's price alerts"""
    try:
        with open(ALERTS_FILE, 'r') as f:
            alerts = json.load(f)
        return jsonify({'alerts': alerts})
    except:
        return jsonify({'alerts': []})

@app.route('/api/alerts/add', methods=['POST'])
def add_alert():
    """Add price alert"""
    data = request.get_json()
    
    try:
        with open(ALERTS_FILE, 'r') as f:
            alerts = json.load(f)
        
        alert = {
            'id': len(alerts) + 1,
            'ticker': data.get('ticker', '').upper(),
            'price': float(data.get('price', 0)),
            'condition': data.get('condition', 'above'),  # above/below
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        alerts.append(alert)
        
        with open(ALERTS_FILE, 'w') as f:
            json.dump(alerts, f)
        
        return jsonify({'success': True, 'message': 'Alert berhasil dibuat', 'alert': alert})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/alerts/remove', methods=['POST'])
def remove_alert():
    """Remove price alert"""
    data = request.get_json()
    alert_id = data.get('id')
    
    try:
        with open(ALERTS_FILE, 'r') as f:
            alerts = json.load(f)
        
        alerts = [a for a in alerts if a.get('id') != alert_id]
        
        with open(ALERTS_FILE, 'w') as f:
            json.dump(alerts, f)
        
        return jsonify({'success': True, 'message': 'Alert dihapus'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# === TOP MOVERS API ===
@app.route('/api/top-movers', methods=['GET'])
def get_top_movers():
    """Get top gainers and losers"""
    tickers = ['BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'TLKM.JK', 'ASII.JK', 
               'UNVR.JK', 'ICBP.JK', 'INDF.JK', 'KLBF.JK', 'GOTO.JK']
    
    movers = []
    
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="5d", interval="1d", progress=False)
            if not df.empty and len(df) >= 2:
                close_series = df['Close'].squeeze() if hasattr(df['Close'], 'squeeze') else df['Close']
                current = float(close_series.iloc[-1])
                previous = float(close_series.iloc[-2])
                change_pct = ((current - previous) / previous) * 100
                
                movers.append({
                    'ticker': ticker,
                    'price': current,
                    'change': change_pct
                })
        except:
            continue
    
    # Sort by change percentage
    movers.sort(key=lambda x: x['change'], reverse=True)
    
    gainers = movers[:5]  # Top 5 gainers
    losers = sorted(movers, key=lambda x: x['change'])[:5]  # Top 5 losers
    
    return jsonify({
        'gainers': gainers,
        'losers': losers
    })

# === CANDLESTICK DATA API ===
@app.route('/api/candlestick', methods=['POST'])
def get_candlestick():
    """Get candlestick chart data"""
    data = request.get_json()
    ticker = data.get('ticker', 'TLKM.JK')
    period = data.get('period', '1mo')  # 1d, 5d, 1mo, 3mo, 6mo, 1y
    
    try:
        df = yf.download(ticker, period=period, interval='1d', progress=False)
        
        if df.empty:
            return jsonify({'error': 'No data available'})
        
        # Prepare candlestick data
        candles = []
        for idx, row in df.iterrows():
            candles.append({
                'date': idx.strftime('%Y-%m-%d'),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume'])
            })
        
        return jsonify({'candles': candles})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🚀 Starting Simple Stock Analysis Web App...")
    print("📊 Open browser at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)

# For Vercel serverless deployment
application = app
