from flask import Flask, render_template, jsonify, request, session
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import json
import os
import requests
from google import genai
warnings.filterwarnings('ignore')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Configure Gemini AI (new google-genai SDK)
GEMINI_API_KEY = "AIzaSyDOymWnnOqy4tE5GgIseYU1kNu3NVtfbCE"
client = genai.Client(api_key=GEMINI_API_KEY)
GEMINI_MODEL = "gemini-2.5-flash"

# In-memory storage for serverless (Vercel doesn't have persistent filesystem)
# For production, use Redis, PostgreSQL, or Vercel KV
WATCHLIST_DATA = []
ALERTS_DATA = []
CHAT_HISTORY = {}  # {session_id: [{role: 'user/assistant', content: '...', timestamp: '...'}]}

# Try to use file storage if available (local development)
WATCHLIST_FILE = 'data/watchlist.json'
ALERTS_FILE = 'data/alerts.json'
CHAT_HISTORY_FILE = 'data/chat_history.json'

try:
    os.makedirs('data', exist_ok=True)
    
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r') as f:
            WATCHLIST_DATA = json.load(f)
    
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, 'r') as f:
            ALERTS_DATA = json.load(f)
    
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as f:
            CHAT_HISTORY = json.load(f)
except:
    # If file operations fail (serverless), use in-memory storage
    pass

def save_chat_history():
    """Save chat history to file if possible"""
    try:
        with open(CHAT_HISTORY_FILE, 'w') as f:
            json.dump(CHAT_HISTORY, f)
    except:
        pass  # Silently fail on serverless

def save_watchlist():
    """Save watchlist to file if possible"""
    try:
        with open(WATCHLIST_FILE, 'w') as f:
            json.dump(WATCHLIST_DATA, f)
    except:
        pass  # Silently fail on serverless

def save_alerts():
    """Save alerts to file if possible"""
    try:
        with open(ALERTS_FILE, 'w') as f:
            json.dump(ALERTS_DATA, f)
    except:
        pass  # Silently fail on serverless

def send_whatsapp_notification(phone, message):
    """
    Send WhatsApp notification using API
    For production, use services like:
    - Twilio WhatsApp API
    - WhatsApp Business API
    - Fonnte.com (Indonesian service)
    """
    try:
        # Example using Fonnte (you need to register and get API key)
        # Get your API key from https://fonnte.com
        api_key = os.environ.get('FONNTE_API_KEY', '6CHvYRScRHSK2obG2Xf9')
        
        if not api_key:
            print(f"[WhatsApp] API key not configured. Message: {message} to {phone}")
            return False
        
        url = "https://api.fonnte.com/send"
        headers = {
            'Authorization': api_key
        }
        data = {
            'target': phone,
            'message': message,
            'countryCode': '62'
        }
        
        response = requests.post(url, headers=headers, data=data, timeout=10)
        result = response.json()
        
        if result.get('status'):
            print(f"[WhatsApp] Sent to {phone}: {message}")
            return True
        else:
            print(f"[WhatsApp] Failed to send: {result}")
            return False
            
    except Exception as e:
        print(f"[WhatsApp] Error: {e}")
        return False

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
    
    ema9_val = to_float(ema_9.iloc[-1])
    ema21_val = to_float(ema_21.iloc[-1])
    ema50_val = to_float(ema_50.iloc[-1])
    
    if ema9_val > ema21_val > ema50_val:
        signals['trend_strength'] = 100  # Strong uptrend
    elif ema9_val < ema21_val < ema50_val:
        signals['trend_strength'] = 0   # Strong downtrend
    else:
        signals['trend_strength'] = 50  # Sideways
    
    # Momentum Score (RSI + MACD)
    rsi_series = calculate_rsi(close_series)
    rsi = to_float(rsi_series.iloc[-1]) if not rsi_series.empty else 50.0
    if rsi < 30:
        signals['momentum_score'] = 90  # Oversold - buy signal
    elif rsi > 70:
        signals['momentum_score'] = 10  # Overbought - sell signal
    else:
        signals['momentum_score'] = 50
    
    # Volume Score
    current_vol = df['Volume'].iloc[-1]
    avg_vol = df['Volume'].rolling(20).mean().iloc[-1]
    vol_ratio = to_float(current_vol / avg_vol) if to_float(avg_vol) > 0 else 1.0
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
    atr = to_float(atr_series.iloc[-1]) if not atr_series.empty else 0.0
    current_price = to_float(close_series.iloc[-1])
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
    support = to_float(low_series.tail(30).min())
    resistance = to_float(high_series.tail(30).max())
    current = to_float(close_series.iloc[-1])
    
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
        result = float(val)
        if pd.isna(result):
            return 0.0
        return result
    except (TypeError, ValueError):
        return 0.0

def safe_int(val, default=0):
    """Convert value to int safely, handling NaN"""
    try:
        f = float(val)
        if pd.isna(f):
            return default
        return int(f)
    except (TypeError, ValueError):
        return default

def analyze_stock_simple(ticker):
    """Analisis saham versi sederhana untuk orang awam"""
    try:
        # Normalize ticker format
        ticker = ticker.strip().upper()
        
        print(f"[DEBUG] Downloading data for {ticker}...")  # Vercel log
        
        # Try downloading with retry mechanism
        df = None
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                print(f"[DEBUG] Attempt {attempt + 1}/{max_retries}")
                # Download data 3 bulan - single ticker only
                df = yf.download(ticker, period="3mo", interval="1d", progress=False)
                
                if df is not None and not df.empty and len(df) >= 10:
                    print(f"[DEBUG] Download successful on attempt {attempt + 1}")
                    break
                else:
                    print(f"[DEBUG] Attempt {attempt + 1} returned insufficient data")
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(1)
            except Exception as e:
                print(f"[DEBUG] Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(1)
        
        # Check if download was successful
        if df is None or df.empty or len(df) < 10:
            return {
                "error": f"Data untuk ticker '{ticker}' tidak tersedia atau tidak cukup. Coba ticker lain seperti: BBCA.JK, TLKM.JK, GOTO.JK"
            }
        
        # Handle multi-level columns (yfinance >= 0.2.31 always returns MultiIndex)
        if isinstance(df.columns, pd.MultiIndex):
            # Use xs to extract single ticker, or droplevel if only one ticker
            tickers_in_data = df.columns.get_level_values(1).unique().tolist()
            if len(tickers_in_data) == 1:
                df.columns = df.columns.droplevel(1)
            else:
                # Multiple tickers in data (shouldn't happen but handle gracefully)
                # Pick columns that match our ticker
                try:
                    df = df.xs(ticker, level=1, axis=1)
                except KeyError:
                    df.columns = df.columns.droplevel(1)
        
        # Ensure no duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]
        
        # Verify required columns exist
        required_cols = ['Close', 'High', 'Low', 'Open', 'Volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return {
                "error": f"Data tidak lengkap untuk '{ticker}'. Kolom yang hilang: {', '.join(missing_cols)}"
            }
        
        # Convert to clean Series
        close_series = df['Close'].squeeze()
        high_series = df['High'].squeeze()
        low_series = df['Low'].squeeze()
        
        # Ensure they are Series, not DataFrames
        if isinstance(close_series, pd.DataFrame):
            close_series = close_series.iloc[:, 0]
        if isinstance(high_series, pd.DataFrame):
            high_series = high_series.iloc[:, 0]
        if isinstance(low_series, pd.DataFrame):
            low_series = low_series.iloc[:, 0]
        
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
        chart_prices = chart_data['Close'].fillna(0).values.tolist()
        chart_volumes = chart_data['Volume'].fillna(0).values.tolist()
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
                "volume": safe_int(volume_sekarang),
                "volume_avg": safe_int(volume_rata),
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
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error analyzing {ticker}: {error_detail}")  # Log to Vercel
        return {
            "error": f"Gagal menganalisis '{ticker}'. Pastikan kode ticker benar (contoh: BBCA.JK, TLKM.JK, GOTO.JK). Detail: {str(e)}"
        }

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

# === IDX MONITOR API ===
@app.route('/api/idx/monitor', methods=['POST'])
def api_idx_monitor():
    """Get real-time data for IDX stocks"""
    data = request.get_json()
    tickers = data.get('tickers', [])
    
    results = []
    for ticker in tickers:
        try:
            hist = None
            for attempt in range(3):
                try:
                    hist = yf.download(ticker, period='5d', interval='1d', progress=False)
                    if hist is not None and not hist.empty and len(hist) >= 2:
                        break
                    else:
                        if attempt < 2:
                            import time
                            time.sleep(0.5)
                except Exception as e:
                    if attempt < 2:
                        import time
                        time.sleep(0.5)
                    else:
                        raise e
            
            if hist is None or hist.empty or len(hist) < 2:
                results.append({'ticker': ticker, 'error': True, 'message': 'Data tidak tersedia'})
                continue
            
            # Handle MultiIndex columns
            if isinstance(hist.columns, pd.MultiIndex):
                tickers_in = hist.columns.get_level_values(1).unique().tolist()
                if len(tickers_in) == 1:
                    hist.columns = hist.columns.droplevel(1)
                else:
                    try:
                        hist = hist.xs(ticker, level=1, axis=1)
                    except KeyError:
                        hist.columns = hist.columns.droplevel(1)
            
            hist = hist.loc[:, ~hist.columns.duplicated()]
            
            current_price = to_float(hist['Close'].iloc[-1])
            prev_price = to_float(hist['Close'].iloc[-2])
            change = current_price - prev_price
            change_percent = (change / prev_price) * 100 if prev_price > 0 else 0
            volume = to_float(hist['Volume'].iloc[-1])
            
            results.append({
                'ticker': ticker,
                'price': round(current_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'volume': safe_int(volume),
                'high': round(to_float(hist['High'].iloc[-1]), 2),
                'low': round(to_float(hist['Low'].iloc[-1]), 2),
                'error': False
            })
                    
        except Exception as e:
            print(f"Error fetching {ticker}: {str(e)}")
            results.append({'ticker': ticker, 'error': True, 'message': str(e)[:50]})
    
    return jsonify({'data': results})

# === WATCHLIST API ===
@app.route('/api/watchlist', methods=['GET'])
def get_watchlist():
    """Get user's watchlist"""
    return jsonify({'watchlist': WATCHLIST_DATA})

@app.route('/api/watchlist/add', methods=['POST'])
def add_to_watchlist():
    """Add stock to watchlist"""
    data = request.get_json()
    ticker = data.get('ticker', '').upper()
    
    try:
        if ticker not in WATCHLIST_DATA:
            WATCHLIST_DATA.append(ticker)
            save_watchlist()
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
        if ticker in WATCHLIST_DATA:
            WATCHLIST_DATA.remove(ticker)
            save_watchlist()
            return jsonify({'success': True, 'message': f'{ticker} dihapus dari watchlist'})
        else:
            return jsonify({'success': False, 'message': f'{ticker} tidak ada di watchlist'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# === ALERTS API ===
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get user's price alerts"""
    return jsonify({'alerts': ALERTS_DATA})

@app.route('/api/alerts/add', methods=['POST'])
def add_alert():
    """Add price alert"""
    data = request.get_json()
    
    try:
        whatsapp = data.get('whatsapp', '').strip()
        
        alert = {
            'id': len(ALERTS_DATA) + 1,
            'ticker': data.get('ticker', '').upper(),
            'price': float(data.get('price', 0)),
            'condition': data.get('condition', 'above'),  # above/below
            'whatsapp': whatsapp if whatsapp else None,  # Store WhatsApp number
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'triggered': False
        }
        
        ALERTS_DATA.append(alert)
        save_alerts()
        
        message = 'Alert berhasil dibuat'
        
        # Kirim pesan WhatsApp welcome jika nomor WA diisi
        if whatsapp:
            # Format harga dengan proper formatting
            formatted_price = f"{alert['price']:,.2f}" if alert['price'] >= 1000 else f"{alert['price']:.2f}"
            
            welcome_message = f"""🎯 *Halo dari StockPro AI!*

Terima kasih telah mengaktifkan notifikasi WhatsApp! 📱

✅ Alert Anda telah berhasil dibuat:
• Saham: {alert['ticker']}
• Target Harga: Rp {formatted_price}
• Kondisi: {'Di atas' if alert['condition'] == 'above' else 'Di bawah'} target

📊 *Layanan Kami:*
• Notifikasi real-time saat harga mencapai target
• Analisis teknikal dengan 13 indikator
• AI scoring untuk rekomendasi trading
• Update pasar harian

💡 Anda akan menerima notifikasi otomatis di nomor ini ketika harga saham mencapai target yang Anda tentukan.

Selamat berinvestasi! 🚀

_StockPro AI - Platform Analisis Saham Terpercaya_"""
            
            # Kirim pesan welcome
            wa_sent = send_whatsapp_notification(whatsapp, welcome_message)
            
            if wa_sent:
                message += f'. Pesan welcome telah dikirim ke WhatsApp {whatsapp}'
            else:
                message += f'. Alert dibuat, namun pesan welcome gagal dikirim. Pastikan nomor WA {whatsapp} valid.'
        
        return jsonify({'success': True, 'message': message, 'alert': alert})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/alerts/remove', methods=['POST'])
def remove_alert():
    """Remove price alert"""
    data = request.get_json()
    alert_id = data.get('id')
    
    try:
        global ALERTS_DATA
        ALERTS_DATA = [a for a in ALERTS_DATA if a.get('id') != alert_id]
        save_alerts()
        
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
                # Handle MultiIndex
                if isinstance(df.columns, pd.MultiIndex):
                    tickers_in = df.columns.get_level_values(1).unique()
                    if len(tickers_in) == 1:
                        df.columns = df.columns.droplevel(1)
                    else:
                        try: df = df.xs(ticker, level=1, axis=1)
                        except: df.columns = df.columns.droplevel(1)
                df = df.loc[:, ~df.columns.duplicated()]
                
                current = to_float(df['Close'].iloc[-1])
                previous = to_float(df['Close'].iloc[-2])
                change_pct = ((current - previous) / previous) * 100 if previous > 0 else 0
                
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
        
        # Handle MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            tickers_in = df.columns.get_level_values(1).unique()
            if len(tickers_in) == 1:
                df.columns = df.columns.droplevel(1)
            else:
                try: df = df.xs(ticker, level=1, axis=1)
                except: df.columns = df.columns.droplevel(1)
        df = df.loc[:, ~df.columns.duplicated()]
        
        # Prepare candlestick data
        candles = []
        for idx, row in df.iterrows():
            candles.append({
                'date': idx.strftime('%Y-%m-%d'),
                'open': to_float(row['Open']),
                'high': to_float(row['High']),
                'low': to_float(row['Low']),
                'close': to_float(row['Close']),
                'volume': safe_int(row['Volume'])
            })
        
        return jsonify({'candles': candles})
    except Exception as e:
        return jsonify({'error': str(e)})

# === WATCHLIST REAL-TIME PRICES ===
@app.route('/api/watchlist/prices', methods=['GET'])
def get_watchlist_prices():
    """Get real-time prices for all watchlist tickers"""
    try:
        if not WATCHLIST_DATA:
            return jsonify({'prices': {}})
        
        prices = {}
        for ticker in WATCHLIST_DATA:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
                prev_close = info.get('previousClose', 0)
                
                if current_price and prev_close:
                    change = current_price - prev_close
                    change_percent = (change / prev_close) * 100
                else:
                    # Fallback: use latest close from history
                    hist = stock.history(period='1d')
                    if not hist.empty:
                        current_price = to_float(hist['Close'].iloc[-1])
                        if len(hist) > 1:
                            prev_close = to_float(hist['Close'].iloc[-2])
                        else:
                            prev_close = current_price
                        change = current_price - prev_close
                        change_percent = (change / prev_close) * 100 if prev_close else 0
                    else:
                        current_price = 0
                        change = 0
                        change_percent = 0
                
                prices[ticker] = {
                    'price': round(current_price, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2)
                }
            except:
                prices[ticker] = {
                    'price': 0,
                    'change': 0,
                    'change_percent': 0
                }
        
        return jsonify({'prices': prices})
        
    except Exception as e:
        print(f"Error getting watchlist prices: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts/check', methods=['POST'])
def check_alerts():
    """Check if any alerts should be triggered based on current prices"""
    try:
        triggered_alerts = []
        
        for alert in ALERTS_DATA:
            if alert.get('triggered'):
                continue  # Skip already triggered alerts
            
            ticker = alert['ticker']
            target_price = float(alert['price'])
            condition = alert['condition']
            whatsapp = alert.get('whatsapp')
            
            # Get current price
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period='1d')
                if hist.empty:
                    continue
                
                current_price = float(hist['Close'].iloc[-1])
                
                # Check if alert should trigger
                should_trigger = False
                if condition == 'above' and current_price >= target_price:
                    should_trigger = True
                elif condition == 'below' and current_price <= target_price:
                    should_trigger = True
                
                if should_trigger:
                    alert['triggered'] = True
                    triggered_alerts.append(alert)
                    
                    # Send WhatsApp notification
                    if whatsapp:
                        # Format prices properly
                        formatted_current = f"{current_price:,.2f}" if current_price >= 1000 else f"{current_price:.2f}"
                        formatted_target = f"{target_price:,.2f}" if target_price >= 1000 else f"{target_price:.2f}"
                        
                        price_change = ((current_price - target_price) / target_price) * 100
                        
                        notification_message = f"""🚨 *ALERT TRIGGERED - StockPro AI*

Harga saham {ticker} telah mencapai target Anda!

📊 *Detail Alert:*
• Saham: {ticker}
• Target: Rp {formatted_target}
• Harga Saat Ini: Rp {formatted_current}
• Perubahan: {price_change:+.2f}%
• Kondisi: {'Naik melewati' if condition == 'above' else 'Turun melewati'} target

⏰ Waktu: {datetime.now().strftime('%d %B %Y, %H:%M WIB')}

💡 *Saran:*
• Cek analisis teknikal terkini di dashboard
• Pertimbangkan take profit atau cut loss
• Perhatikan volume dan momentum pasar

Tetap bijak dalam berinvestasi! 📈

_StockPro AI - Notifikasi Real-time_"""
                        
                        send_whatsapp_notification(whatsapp, notification_message)
                        print(f"[Alert] Triggered for {ticker}: {current_price} {'>' if condition == 'above' else '<'} {target_price}")
                
            except Exception as e:
                print(f"[Alert] Error checking {ticker}: {e}")
                continue
        
        # Save updated alerts
        save_alerts()
        
        return jsonify({
            'checked': len(ALERTS_DATA),
            'triggered': len(triggered_alerts),
            'alerts': triggered_alerts
        })
        
    except Exception as e:
        print(f"Error checking alerts: {str(e)}")
        return jsonify({'error': str(e)}), 500

# === AI CHATBOT & ANALYSIS API ===
@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """AI Chatbot with conversation history caching"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        ticker = data.get('ticker', '')
        stock_data = data.get('stockData', {})
        session_id = data.get('sessionId', 'default')  # Client can pass session ID for multi-user support
        
        # Initialize session history if not exists
        if session_id not in CHAT_HISTORY:
            CHAT_HISTORY[session_id] = []
        
        # Clean old history (keep last 20 messages for context, ~10 exchanges)
        if len(CHAT_HISTORY[session_id]) > 20:
            CHAT_HISTORY[session_id] = CHAT_HISTORY[session_id][-20:]
        
        # Build context-aware prompt with conversation history
        system_instruction = """Kamu adalah StockPro AI, analis saham profesional bersertifikat CFA & CMT dengan pengalaman 15+ tahun di pasar Indonesia (IDX) dan global.

KEAHLIAN UTAMA:
- Technical Analysis: Chart patterns, candlestick, Fibonacci, Elliott Wave, Ichimoku
- Fundamental Analysis: Valuasi, rasio keuangan, analisis sektoral  
- Risk Management: Position sizing, stop loss, risk-reward ratio
- Behavioral Finance: Sentiment analysis, market psychology
- Pasar Indonesia: Familiar dengan semua emiten IDX, regulasi OJK, jam trading BEI

GAYA KOMUNIKASI:
- Profesional namun ramah dan mudah dipahami
- Gunakan data kuantitatif untuk mendukung argumen
- Berikan rekomendasi yang actionable (entry, exit, stop loss)
- Gunakan emoji untuk visual hierarchy
- Bahasa Indonesia yang natural dan engaging
- Selalu sertakan disclaimer risiko
- Jika user tanya dalam bahasa Inggris, jawab dalam bahasa Inggris
- Ingat konteks percakapan sebelumnya untuk memberikan jawaban yang relevan"""
        
        # Build conversation context for Gemini
        conversation_context = ""
        if len(CHAT_HISTORY[session_id]) > 0:
            conversation_context = "\n\nKONTEKS PERCAKAPAN SEBELUMNYA:\n"
            for msg in CHAT_HISTORY[session_id][-6:]:  # Last 3 exchanges
                role = "User" if msg['role'] == 'user' else "AI"
                conversation_context += f"{role}: {msg['content']}\n"
        
        if ticker and stock_data:
            user_prompt = f"""{conversation_context}

DATA SAHAM SAAT INI - {ticker}:
Harga: Rp {stock_data.get('price', 'N/A'):,.0f}
Perubahan: {stock_data.get('change_percent', 0):+.2f}%
Volume: {stock_data.get('volume', 'N/A'):,}
Trend: {stock_data.get('trend', 'N/A')}
RSI: {stock_data.get('rsi', 'N/A')}
MACD: {stock_data.get('macd', 'N/A')}
Support: Rp {stock_data.get('support', 0):,.0f}
Resistance: Rp {stock_data.get('resistance', 0):,.0f}
AI Score: {stock_data.get('ai_score', 'N/A')}/100

Pertanyaan User: {message}

Jawab 2-4 paragraf padat, actionable, dan data-driven. Gunakan format yang mudah dibaca dengan poin-poin penting."""
        else:
            user_prompt = f"{conversation_context}\n\nPertanyaan User: {message}\n\nJawab 2-4 paragraf, informatif dan educational."
        
        # Call Gemini AI
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=1024,
            )
        )
        
        ai_response = response.text
        
        # Save to history
        timestamp = datetime.now().isoformat()
        CHAT_HISTORY[session_id].append({
            'role': 'user',
            'content': message,
            'timestamp': timestamp,
            'ticker': ticker
        })
        CHAT_HISTORY[session_id].append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': timestamp
        })
        save_chat_history()
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'timestamp': timestamp,
            'historyCount': len(CHAT_HISTORY[session_id])
        })
        
    except Exception as e:
        print(f"AI Chat error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Maaf, terjadi kesalahan pada AI. Silakan coba lagi.',
            'details': str(e)
        }), 500

@app.route('/api/ai/analysis', methods=['POST'])
def ai_deep_analysis():
    """Enhanced AI Deep Analysis with comprehensive market insights"""
    try:
        data = request.get_json()
        ticker = data.get('ticker', '')
        stock_data = data.get('stockData', {})
        language = data.get('language', 'id')  # 'id' or 'en'
        
        if not ticker or not stock_data:
            return jsonify({'success': False, 'error': 'Data tidak lengkap'}), 400
        
        if language == 'en':
            system_instruction = """You are a Senior Equity Analyst certified CFA Level III and CMT (Chartered Market Technician) specializing in Indonesian and global stock markets. Provide analysis equivalent to professional research reports. Use quantitative data and actionable recommendations."""
            
            error_msg = 'Sorry, an error occurred with AI analysis. Please try again.'
        else:
            system_instruction = """Kamu adalah Senior Equity Analyst bersertifikat CFA Level III dan CMT dengan spesialisasi pasar saham Indonesia. Berikan analisis setara laporan riset profesional."""
            
            error_msg = 'Maaf, terjadi kesalahan pada AI analysis. Silakan coba lagi.'
        
        prompt = f"""Create COMPREHENSIVE DEEP ANALYSIS for {ticker}.

REAL-TIME DATA:
- Price: Rp {stock_data.get('price', 0):,.0f}
- Change: {stock_data.get('change_percent', 0):+.2f}%
- Volume: {stock_data.get('volume', 0):,}
- RSI: {stock_data.get('rsi', 'N/A')}
- MACD: {stock_data.get('macd', 'N/A')}
- Trend: {stock_data.get('trend', 'N/A')}
- AI Score: {stock_data.get('ai_score', 'N/A')}/100
- Support: Rp {stock_data.get('support', 0):,.0f}
- Resistance: Rp {stock_data.get('resistance', 0):,.0f}
- Stochastic: {stock_data.get('stochastic', 'N/A')}
- ATR: {stock_data.get('atr', 'N/A')}
- BB Upper: Rp {stock_data.get('bb_upper', 0):,.0f}
- BB Lower: Rp {stock_data.get('bb_lower', 0):,.0f}

REPORT FORMAT:

📊 **EXECUTIVE SUMMARY**
[3-4 sentences + rating: STRONG BUY/BUY/HOLD/SELL/STRONG SELL]

🔍 **IN-DEPTH TECHNICAL ANALYSIS**
• Trend Analysis (EMA, price action, momentum)
• Momentum (RSI, MACD, divergences)
• Volatility (Bollinger Bands, ATR, risk)
• Support & Resistance (key levels, Fibonacci)
• Chart Patterns & Volume Profile

📈 **TREND & OUTLOOK**
• Short-term (1-2 weeks)
• Medium-term (1-3 months)
• Long-term (6-12 months)
• Market Catalysts & Sector Performance

⚠️ **RISK ASSESSMENT**
• Technical, Market, Fundamental Risks
• Probability + Impact + Mitigation for each

💡 **RECOMMENDATIONS**
• Rating with conviction (1-5)
• Price Target (upside %)
• Stop Loss (risk %)
• Risk-Reward Ratio
• Confidence Level

🎯 **TRADING STRATEGY**
• Entry Zone
• TP1, TP2, TP3 with position sizing
• Stop Loss placement
• Time Horizon & Re-entry plan

💼 **PORTFOLIO IMPLICATIONS**
• Sector allocation & correlations

⚖️ **DISCLAIMER**
Educational only, not investment advice. DYOR.

Use emoji, **bold**, bullets. 700-900 words. Be specific with numbers."""
        
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.6,
                max_output_tokens=2048,
            )
        )
        
        return jsonify({
            'success': True,
            'analysis': response.text,
            'ticker': ticker,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"AI Analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'error': error_msg,
            'details': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Simple Stock Analysis Web App...")
    print("📊 Open browser at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)

# For Vercel serverless deployment
application = app
