from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)

# === FUNGSI INDIKATOR TEKNIKAL ===
def calculate_rsi(data, window=14):
    """RSI - Relative Strength Index"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data, fast=12, slow=26, signal=9):
    """MACD - Moving Average Convergence Divergence"""
    ema_fast = data.ewm(span=fast, adjust=False).mean()
    ema_slow = data.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(data, window=20, num_std=2):
    """Bollinger Bands"""
    sma = data.rolling(window=window).mean()
    std = data.rolling(window=window).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return upper_band, sma, lower_band

def calculate_stochastic(high, low, close, window=14):
    """Stochastic Oscillator"""
    lowest_low = low.rolling(window=window).min()
    highest_high = high.rolling(window=window).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=3).mean()
    return k, d

def calculate_atr(high, low, close, window=14):
    """ATR - Average True Range"""
    high_low = high - low
    high_close = (high - close.shift()).abs()
    low_close = (low - close.shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=window).mean()
    return atr

def calculate_support_resistance(df, window=20):
    """Support & Resistance Levels"""
    resistance = df['High'].rolling(window=window).max().iloc[-1]
    if hasattr(resistance, 'values'):
        resistance = float(resistance.values[0])
    else:
        resistance = float(resistance)
    
    support = df['Low'].rolling(window=window).min().iloc[-1]
    if hasattr(support, 'values'):
        support = float(support.values[0])
    else:
        support = float(support)
    
    return support, resistance

def analyze_volume(df):
    """Analisis Volume Trading"""
    avg_volume = df['Volume'].tail(20).mean()
    if hasattr(avg_volume, 'values'):
        avg_volume = float(avg_volume.values[0])
    else:
        avg_volume = float(avg_volume)
    
    current_volume = df['Volume'].iloc[-1]
    if hasattr(current_volume, 'values'):
        current_volume = float(current_volume.values[0])
    else:
        current_volume = float(current_volume)
    
    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
    return volume_ratio

def calculate_ema(data, span):
    """EMA - Exponential Moving Average"""
    return data.ewm(span=span, adjust=False).mean()

def trend_analysis(df):
    """Analisis Trend dengan Multiple EMA"""
    def to_float(val):
        if hasattr(val, 'values'):
            return float(val.values[0])
        return float(val)
    
    ema_9 = to_float(calculate_ema(df['Close'], 9).iloc[-1])
    ema_21 = to_float(calculate_ema(df['Close'], 21).iloc[-1])
    ema_50 = to_float(calculate_ema(df['Close'], 50).iloc[-1])
    ema_200 = to_float(calculate_ema(df['Close'], 200).iloc[-1])
    
    current_price = to_float(df['Close'].iloc[-1])
    
    if current_price > ema_9 > ema_21 > ema_50:
        return "BULLISH KUAT 🚀", "success"
    elif current_price > ema_9 > ema_21:
        return "BULLISH 📈", "success"
    elif current_price < ema_9 < ema_21 < ema_50:
        return "BEARISH KUAT 📉", "danger"
    elif current_price < ema_9 < ema_21:
        return "BEARISH 🔻", "danger"
    else:
        return "SIDEWAYS ➡️", "warning"

def momentum_score(df):
    """Skor Momentum (0-100)"""
    def to_float(val):
        if hasattr(val, 'values'):
            return float(val.values[0])
        return float(val)
    
    rsi = to_float(df['RSI'].iloc[-1])
    macd_hist = to_float(df['MACD_Hist'].iloc[-1])
    stoch_k = to_float(df['Stoch_K'].iloc[-1])
    
    score = 0
    if 40 < rsi < 60:
        score += 20
    elif 30 < rsi < 70:
        score += 10
    
    if macd_hist > 0:
        score += 30
    
    if 20 < stoch_k < 80:
        score += 20
    elif stoch_k < 20:
        score += 30
    
    volume_ratio = analyze_volume(df)
    if volume_ratio > 1.5:
        score += 20
    elif volume_ratio > 1.0:
        score += 10
    
    return min(score, 100)

def get_signal(df):
    """Generate Trading Signal"""
    def to_float(val):
        if hasattr(val, 'values'):
            return float(val.values[0])
        return float(val)
    
    rsi = to_float(df['RSI'].iloc[-1])
    macd_line = to_float(df['MACD'].iloc[-1])
    signal_line = to_float(df['Signal'].iloc[-1])
    macd_hist = to_float(df['MACD_Hist'].iloc[-1])
    stoch_k = to_float(df['Stoch_K'].iloc[-1])
    stoch_d = to_float(df['Stoch_D'].iloc[-1])
    bb_upper = to_float(df['BB_Upper'].iloc[-1])
    bb_lower = to_float(df['BB_Lower'].iloc[-1])
    current_price = to_float(df['Close'].iloc[-1])
    
    buy_signals = 0
    sell_signals = 0
    
    if rsi < 30:
        buy_signals += 2
    elif rsi > 70:
        sell_signals += 2
    
    if macd_line > signal_line and macd_hist > 0:
        buy_signals += 2
    elif macd_line < signal_line and macd_hist < 0:
        sell_signals += 2
    
    if stoch_k < 20 and stoch_k > stoch_d:
        buy_signals += 1
    elif stoch_k > 80 and stoch_k < stoch_d:
        sell_signals += 1
    
    if current_price < bb_lower:
        buy_signals += 1
    elif current_price > bb_upper:
        sell_signals += 1
    
    if buy_signals >= 3:
        return "🟢 STRONG BUY", "success"
    elif buy_signals >= 2:
        return "🟢 BUY", "success"
    elif sell_signals >= 3:
        return "🔴 STRONG SELL", "danger"
    elif sell_signals >= 2:
        return "🔴 SELL", "danger"
    else:
        return "🟡 HOLD", "warning"

def analyze_stock(ticker):
    """Analisis saham lengkap"""
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        if df.empty:
            return {"error": "Data tidak ditemukan. Cek simbol saham."}
        
        # Hitung semua indikator
        df['RSI'] = calculate_rsi(df['Close'])
        df['MACD'], df['Signal'], df['MACD_Hist'] = calculate_macd(df['Close'])
        df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = calculate_bollinger_bands(df['Close'])
        df['Stoch_K'], df['Stoch_D'] = calculate_stochastic(df['High'], df['Low'], df['Close'])
        df['ATR'] = calculate_atr(df['High'], df['Low'], df['Close'])
        
        # Data terakhir
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Helper function untuk konversi
        def to_float(val):
            return float(val.iloc[0] if hasattr(val, 'iloc') else val)
        
        harga_terakhir = to_float(latest['Close'])
        prev_close = to_float(prev['Close'])
        perubahan = harga_terakhir - prev_close
        perubahan_persen = (perubahan / prev_close) * 100
        
        support, resistance = calculate_support_resistance(df)
        trend, trend_color = trend_analysis(df)
        momentum = momentum_score(df)
        signal, signal_color = get_signal(df)
        volume_ratio = analyze_volume(df)
        
        # Indicators
        rsi_val = to_float(latest['RSI'])
        macd_val = to_float(latest['MACD'])
        signal_val = to_float(latest['Signal'])
        macd_hist_val = to_float(latest['MACD_Hist'])
        stoch_k_val = to_float(latest['Stoch_K'])
        stoch_d_val = to_float(latest['Stoch_D'])
        bb_upper_val = to_float(latest['BB_Upper'])
        bb_middle_val = to_float(latest['BB_Middle'])
        bb_lower_val = to_float(latest['BB_Lower'])
        atr_val = to_float(latest['ATR'])
        
        # Generate insights
        insights = []
        
        if rsi_val < 30 and macd_hist_val > 0:
            insights.append("✅ RSI oversold dengan MACD bullish - Strong buy signal!")
        
        if harga_terakhir < bb_lower_val:
            insights.append("✅ Harga di bawah BB Lower - Potensi rebound!")
        
        if volume_ratio > 1.5:
            insights.append("⚠️ Volume tinggi - Perhatikan pergerakan harga!")
        
        if stoch_k_val < 20:
            insights.append("✅ Stochastic oversold - Peluang entry!")
        
        if abs(harga_terakhir - resistance) / harga_terakhir < 0.02:
            insights.append("⚠️ Mendekati resistance - Waspadai penolakan!")
        
        if abs(harga_terakhir - support) / harga_terakhir < 0.02:
            insights.append("⚠️ Mendekati support - Perhatikan breakdown!")
        
        if len(insights) == 0:
            insights.append("📊 Kondisi pasar normal, tunggu sinyal lebih jelas.")
        
        # Chart data (last 60 days)
        chart_data = df.tail(60)
        chart_dates = [d.strftime('%Y-%m-%d') for d in chart_data.index]
        chart_prices = chart_data['Close'].values.tolist()
        chart_volumes = chart_data['Volume'].values.tolist()
        
        # RSI Chart
        rsi_values = chart_data['RSI'].values.tolist()
        
        # MACD Chart
        macd_values = chart_data['MACD'].values.tolist()
        signal_values = chart_data['Signal'].values.tolist()
        
        return {
            "success": True,
            "ticker": ticker,
            "timestamp": datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            "basic": {
                "price": harga_terakhir,
                "change": perubahan,
                "change_percent": perubahan_persen,
                "high": to_float(latest['High']),
                "low": to_float(latest['Low']),
                "volume": int(to_float(latest['Volume'])),
                "volume_ratio": volume_ratio
            },
            "support_resistance": {
                "resistance": resistance,
                "support": support,
                "resistance_pct": ((resistance - harga_terakhir) / harga_terakhir * 100),
                "support_pct": ((support - harga_terakhir) / harga_terakhir * 100)
            },
            "indicators": {
                "rsi": rsi_val,
                "rsi_status": "OVERSOLD" if rsi_val < 30 else "OVERBOUGHT" if rsi_val > 70 else "NORMAL",
                "macd": macd_val,
                "signal": signal_val,
                "macd_hist": macd_hist_val,
                "macd_status": "BULLISH" if macd_hist_val > 0 else "BEARISH",
                "stoch_k": stoch_k_val,
                "stoch_d": stoch_d_val,
                "bb_upper": bb_upper_val,
                "bb_middle": bb_middle_val,
                "bb_lower": bb_lower_val,
                "atr": atr_val
            },
            "analysis": {
                "trend": trend,
                "trend_color": trend_color,
                "momentum": momentum,
                "momentum_status": "SANGAT KUAT" if momentum >= 70 else "KUAT" if momentum >= 50 else "SEDANG" if momentum >= 30 else "LEMAH",
                "signal": signal,
                "signal_color": signal_color
            },
            "insights": insights,
            "charts": {
                "dates": chart_dates,
                "prices": chart_prices,
                "volumes": chart_volumes,
                "rsi": rsi_values,
                "macd": macd_values,
                "macd_signal": signal_values
            }
        }
    
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json()
    ticker = data.get('ticker', 'TLKM.JK')
    result = analyze_stock(ticker)
    return jsonify(result)

if __name__ == '__main__':
    print("🚀 Starting Stock Analysis Web App...")
    print("📊 Open browser at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
