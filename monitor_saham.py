import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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
    """ATR - Average True Range (Volatilitas)"""
    high_low = high - low
    high_close = (high - close.shift()).abs()
    low_close = (low - close.shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=window).mean()
    return atr

def calculate_support_resistance(df, window=20):
    """Support & Resistance Levels"""
    resistance = float(df['High'].rolling(window=window).max().iloc[-1])
    support = float(df['Low'].rolling(window=window).min().iloc[-1])
    return support, resistance

def analyze_volume(df):
    """Analisis Volume Trading"""
    avg_volume = float(df['Volume'].tail(20).mean())
    current_volume = float(df['Volume'].iloc[-1])
    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
    return volume_ratio

def calculate_ema(data, span):
    """EMA - Exponential Moving Average"""
    return data.ewm(span=span, adjust=False).mean()

def trend_analysis(df):
    """Analisis Trend dengan Multiple EMA"""
    ema_9 = float(calculate_ema(df['Close'], 9).iloc[-1])
    ema_21 = float(calculate_ema(df['Close'], 21).iloc[-1])
    ema_50 = float(calculate_ema(df['Close'], 50).iloc[-1])
    ema_200 = float(calculate_ema(df['Close'], 200).iloc[-1])
    
    current_price = float(df['Close'].iloc[-1])
    
    if current_price > ema_9 > ema_21 > ema_50:
        return "BULLISH KUAT 🚀", "green"
    elif current_price > ema_9 > ema_21:
        return "BULLISH 📈", "green"
    elif current_price < ema_9 < ema_21 < ema_50:
        return "BEARISH KUAT 📉", "red"
    elif current_price < ema_9 < ema_21:
        return "BEARISH 🔻", "red"
    else:
        return "SIDEWAYS ➡️", "yellow"

def momentum_score(df):
    """Skor Momentum (0-100)"""
    rsi = float(df['RSI'].iloc[-1])
    macd_hist = float(df['MACD_Hist'].iloc[-1])
    stoch_k = float(df['Stoch_K'].iloc[-1])
    
    score = 0
    # RSI scoring
    if 40 < rsi < 60:
        score += 20
    elif 30 < rsi < 70:
        score += 10
    
    # MACD scoring
    if macd_hist > 0:
        score += 30
    
    # Stochastic scoring
    if 20 < stoch_k < 80:
        score += 20
    elif stoch_k < 20:
        score += 30  # Oversold = opportunity
    
    # Volume scoring
    volume_ratio = analyze_volume(df)
    if volume_ratio > 1.5:
        score += 20
    elif volume_ratio > 1.0:
        score += 10
    
    return min(score, 100)

def get_signal(df):
    """Generate Trading Signal"""
    rsi = float(df['RSI'].iloc[-1])
    macd_line = float(df['MACD'].iloc[-1])
    signal_line = float(df['Signal'].iloc[-1])
    macd_hist = float(df['MACD_Hist'].iloc[-1])
    stoch_k = float(df['Stoch_K'].iloc[-1])
    stoch_d = float(df['Stoch_D'].iloc[-1])
    bb_upper = float(df['BB_Upper'].iloc[-1])
    bb_lower = float(df['BB_Lower'].iloc[-1])
    current_price = float(df['Close'].iloc[-1])
    
    buy_signals = 0
    sell_signals = 0
    
    # RSI Signal
    if rsi < 30:
        buy_signals += 2
    elif rsi > 70:
        sell_signals += 2
    
    # MACD Signal
    if macd_line > signal_line and macd_hist > 0:
        buy_signals += 2
    elif macd_line < signal_line and macd_hist < 0:
        sell_signals += 2
    
    # Stochastic Signal
    if stoch_k < 20 and stoch_k > stoch_d:
        buy_signals += 1
    elif stoch_k > 80 and stoch_k < stoch_d:
        sell_signals += 1
    
    # Bollinger Bands Signal
    if current_price < bb_lower:
        buy_signals += 1
    elif current_price > bb_upper:
        sell_signals += 1
    
    # Decision
    if buy_signals >= 3:
        return "🟢 STRONG BUY", "green"
    elif buy_signals >= 2:
        return "🟢 BUY", "green"
    elif sell_signals >= 3:
        return "🔴 STRONG SELL", "red"
    elif sell_signals >= 2:
        return "🔴 SELL", "red"
    else:
        return "🟡 HOLD", "yellow"

# === CONFIG ===
TICKER = "TLKM.JK"

try:
    print(f"{'='*60}")
    print(f"🔍 ANALISIS SAHAM ADVANCED - {TICKER}")
    print(f"{'='*60}")
    print(f"⏰ Waktu: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
    
    # Ambil data 6 bulan untuk analisis lebih akurat
    print("📊 Mengambil data historical...")
    df = yf.download(TICKER, period="6mo", interval="1d", progress=False)

    if df.empty:
        print("❌ Data tidak ditemukan. Cek koneksi atau simbol saham.")
    else:
        # === HITUNG SEMUA INDIKATOR ===
        df['RSI'] = calculate_rsi(df['Close'])
        df['MACD'], df['Signal'], df['MACD_Hist'] = calculate_macd(df['Close'])
        df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = calculate_bollinger_bands(df['Close'])
        df['Stoch_K'], df['Stoch_D'] = calculate_stochastic(df['High'], df['Low'], df['Close'])
        df['ATR'] = calculate_atr(df['High'], df['Low'], df['Close'])
        
        # Data terakhir
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        harga_terakhir = float(latest['Close'].iloc[0] if hasattr(latest['Close'], 'iloc') else latest['Close'])
        prev_close = float(prev['Close'].iloc[0] if hasattr(prev['Close'], 'iloc') else prev['Close'])
        perubahan = harga_terakhir - prev_close
        perubahan_persen = (perubahan / prev_close) * 100
        
        # Support & Resistance
        support, resistance = calculate_support_resistance(df)
        
        # Trend Analysis
        trend, trend_color = trend_analysis(df)
        
        # Momentum Score
        momentum = momentum_score(df)
        
        # Trading Signal
        signal, signal_color = get_signal(df)
        
        # Volume Analysis
        volume_ratio = analyze_volume(df)
        
        # === DISPLAY HASIL ===
        print(f"{'='*60}")
        print(f"📌 INFORMASI DASAR")
        print(f"{'='*60}")
        print(f"💰 Harga Terakhir    : Rp {harga_terakhir:,.0f}")
        print(f"📊 Perubahan         : Rp {perubahan:+,.0f} ({perubahan_persen:+.2f}%)")
        print(f"📈 Harga Tertinggi   : Rp {float(latest['High']):,.0f}")
        print(f"📉 Harga Terendah    : Rp {float(latest['Low']):,.0f}")
        print(f"🔊 Volume            : {int(latest['Volume']):,} ({volume_ratio:.2f}x rata-rata)")
        
        print(f"\n{'='*60}")
        print(f"🎯 SUPPORT & RESISTANCE")
        print(f"{'='*60}")
        print(f"⬆️  Resistance        : Rp {resistance:,.0f} ({((resistance-harga_terakhir)/harga_terakhir*100):+.2f}%)")
        print(f"⬇️  Support           : Rp {support:,.0f} ({((support-harga_terakhir)/harga_terakhir*100):+.2f}%)")
        
        print(f"\n{'='*60}")
        print(f"📊 INDIKATOR TEKNIKAL")
        print(f"{'='*60}")
        rsi_val = float(latest['RSI'].iloc[0] if hasattr(latest['RSI'], 'iloc') else latest['RSI'])
        print(f"RSI (14)             : {rsi_val:.2f} ", end="")
        if rsi_val < 30:
            print("⚠️ OVERSOLD - Peluang Beli!")
        elif rsi_val > 70:
            print("⚠️ OVERBOUGHT - Hati-hati!")
        else:
            print("✅ Normal")
        
        macd_val = float(latest['MACD'].iloc[0] if hasattr(latest['MACD'], 'iloc') else latest['MACD'])
        signal_val = float(latest['Signal'].iloc[0] if hasattr(latest['Signal'], 'iloc') else latest['Signal'])
        macd_hist_val = float(latest['MACD_Hist'].iloc[0] if hasattr(latest['MACD_Hist'], 'iloc') else latest['MACD_Hist'])
        print(f"MACD                 : {macd_val:.4f}")
        print(f"Signal Line          : {signal_val:.4f}")
        print(f"MACD Histogram       : {macd_hist_val:.4f} ", end="")
        if macd_hist_val > 0:
            print("🟢 Bullish")
        else:
            print("🔴 Bearish")
        
        stoch_k_val = float(latest['Stoch_K'].iloc[0] if hasattr(latest['Stoch_K'], 'iloc') else latest['Stoch_K'])
        stoch_d_val = float(latest['Stoch_D'].iloc[0] if hasattr(latest['Stoch_D'], 'iloc') else latest['Stoch_D'])
        print(f"Stochastic K         : {stoch_k_val:.2f}")
        print(f"Stochastic D         : {stoch_d_val:.2f}")
        
        bb_upper_val = float(latest['BB_Upper'].iloc[0] if hasattr(latest['BB_Upper'], 'iloc') else latest['BB_Upper'])
        bb_middle_val = float(latest['BB_Middle'].iloc[0] if hasattr(latest['BB_Middle'], 'iloc') else latest['BB_Middle'])
        bb_lower_val = float(latest['BB_Lower'].iloc[0] if hasattr(latest['BB_Lower'], 'iloc') else latest['BB_Lower'])
        print(f"Bollinger Upper      : Rp {bb_upper_val:,.0f}")
        print(f"Bollinger Middle     : Rp {bb_middle_val:,.0f}")
        print(f"Bollinger Lower      : Rp {bb_lower_val:,.0f}")
        
        atr_val = float(latest['ATR'].iloc[0] if hasattr(latest['ATR'], 'iloc') else latest['ATR'])
        print(f"ATR (Volatility)     : {atr_val:.2f}")
        
        print(f"\n{'='*60}")
        print(f"🎯 ANALISIS & REKOMENDASI")
        print(f"{'='*60}")
        print(f"📈 Trend             : {trend}")
        print(f"⚡ Momentum Score    : {momentum}/100 ", end="")
        if momentum >= 70:
            print("🔥 SANGAT KUAT!")
        elif momentum >= 50:
            print("💪 Kuat")
        elif momentum >= 30:
            print("😐 Sedang")
        else:
            print("😴 Lemah")
        
        print(f"\n🎯 SINYAL TRADING    : {signal}")
        
        print(f"\n{'='*60}")
        print(f"💡 INSIGHT")
        print(f"{'='*60}")
        
        # Generate insights
        insights = []
        
        rsi_check = float(latest['RSI'].iloc[0] if hasattr(latest['RSI'], 'iloc') else latest['RSI'])
        macd_hist_check = float(latest['MACD_Hist'].iloc[0] if hasattr(latest['MACD_Hist'], 'iloc') else latest['MACD_Hist'])
        stoch_k_check = float(latest['Stoch_K'].iloc[0] if hasattr(latest['Stoch_K'], 'iloc') else latest['Stoch_K'])
        bb_lower_check = float(latest['BB_Lower'].iloc[0] if hasattr(latest['BB_Lower'], 'iloc') else latest['BB_Lower'])
        
        if rsi_check < 30 and macd_hist_check > 0:
            insights.append("✅ RSI oversold dengan MACD bullish - Strong buy signal!")
        
        if harga_terakhir < bb_lower_check:
            insights.append("✅ Harga di bawah BB Lower - Potensi rebound!")
        
        if volume_ratio > 1.5:
            insights.append("⚠️ Volume tinggi - Perhatikan pergerakan harga!")
        
        if stoch_k_check < 20:
            insights.append("✅ Stochastic oversold - Peluang entry!")
        
        if abs(harga_terakhir - resistance) / harga_terakhir < 0.02:
            insights.append("⚠️ Mendekati resistance - Waspadai penolakan!")
        
        if abs(harga_terakhir - support) / harga_terakhir < 0.02:
            insights.append("⚠️ Mendekati support - Perhatikan breakdown!")
        
        if len(insights) == 0:
            insights.append("📊 Kondisi pasar normal, tunggu sinyal lebih jelas.")
        
        for insight in insights:
            print(insight)
        
        print(f"\n{'='*60}")
        print("✅ Analisis selesai!")
        print(f"{'='*60}")

except Exception as e:
    print(f"❌ Terjadi kesalahan: {e}")
    import traceback
    traceback.print_exc()