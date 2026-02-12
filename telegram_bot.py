import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import yfinance as yf
import pandas as pd
from datetime import datetime

# TOKEN BOT TELEGRAM
TELEGRAM_TOKEN = "8220118835:AAF_K9yGUgkPNyQxCFNHVAbelkzlC6t29ro"

# === FUNGSI ANALISIS ===
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_moving_average(data, window):
    return data.rolling(window=window).mean()

def to_float(val):
    if hasattr(val, 'values'):
        return float(val.values[0])
    return float(val)

def analyze_stock_telegram(ticker):
    """Analisis saham untuk Telegram Bot"""
    try:
        df = yf.download(ticker, period="3mo", interval="1d", progress=False)
        
        if df.empty:
            return None
        
        df['MA7'] = calculate_moving_average(df['Close'], 7)
        df['MA30'] = calculate_moving_average(df['Close'], 30)
        df['RSI'] = calculate_rsi(df['Close'])
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        harga_sekarang = to_float(latest['Close'])
        harga_kemarin = to_float(prev['Close'])
        perubahan = harga_sekarang - harga_kemarin
        perubahan_persen = (perubahan / harga_kemarin) * 100
        
        harga_tertinggi_30d = to_float(df['High'].tail(30).max())
        harga_terendah_30d = to_float(df['Low'].tail(30).min())
        
        ma7 = to_float(latest['MA7'])
        ma30 = to_float(latest['MA30'])
        rsi = to_float(latest['RSI'])
        
        volume_sekarang = to_float(latest['Volume'])
        volume_rata = to_float(df['Volume'].tail(20).mean())
        volume_ratio = volume_sekarang / volume_rata if volume_rata > 0 else 0
        
        # Analisis
        range_30d = harga_tertinggi_30d - harga_terendah_30d
        posisi_harga_pct = ((harga_sekarang - harga_terendah_30d) / range_30d * 100) if range_30d > 0 else 50
        
        # Posisi Harga
        if posisi_harga_pct < 30:
            posisi = "🟢 MURAH"
            posisi_desc = "Harga mendekati terendah 30 hari"
        elif posisi_harga_pct > 70:
            posisi = "🔴 MAHAL"
            posisi_desc = "Harga mendekati tertinggi 30 hari"
        else:
            posisi = "🟡 NORMAL"
            posisi_desc = "Harga di tengah-tengah range"
        
        # Trend
        if harga_sekarang > ma7 > ma30:
            trend = "📈 NAIK KUAT"
        elif harga_sekarang > ma30:
            trend = "📊 NAIK"
        elif harga_sekarang < ma7 < ma30:
            trend = "📉 TURUN KUAT"
        else:
            trend = "➡️ SIDEWAYS"
        
        # Momentum RSI
        if rsi < 30:
            momentum = "🎯 OVERSOLD (Peluang Beli)"
            rsi_status = "Terlalu banyak yang jual"
        elif rsi > 70:
            momentum = "⚠️ OVERBOUGHT (Hati-hati)"
            rsi_status = "Terlalu banyak yang beli"
        else:
            momentum = "✅ NETRAL"
            rsi_status = "Kondisi normal"
        
        # Volume
        if volume_ratio > 1.5:
            volume_status = "🔥 SANGAT RAMAI"
        elif volume_ratio > 1.0:
            volume_status = "📊 RAMAI"
        else:
            volume_status = "😴 SEPI"
        
        # Rekomendasi
        score_beli = 0
        score_jual = 0
        
        if posisi_harga_pct < 30:
            score_beli += 2
        elif posisi_harga_pct > 70:
            score_jual += 2
        
        if harga_sekarang > ma7 > ma30:
            score_beli += 2
        elif harga_sekarang < ma7 < ma30:
            score_jual += 2
        
        if rsi < 30:
            score_beli += 3
        elif rsi > 70:
            score_jual += 3
        
        if score_beli >= 4:
            rekomendasi = "🟢 BELI"
            rekomendasi_desc = "Kondisi bagus untuk membeli"
        elif score_jual >= 4:
            rekomendasi = "🔴 JUAL"
            rekomendasi_desc = "Sebaiknya jual atau tunggu"
        elif score_beli > score_jual:
            rekomendasi = "🟡 PERTIMBANGKAN BELI"
            rekomendasi_desc = "Ada sinyal positif, riset lebih lanjut"
        else:
            rekomendasi = "⚪ TUNGGU DULU"
            rekomendasi_desc = "Belum ada sinyal jelas"
        
        # Nama perusahaan
        try:
            stock_info = yf.Ticker(ticker)
            info = stock_info.info
            nama = info.get('longName', info.get('shortName', ticker))
        except:
            nama = ticker
        
        return {
            'ticker': ticker,
            'nama': nama,
            'harga': harga_sekarang,
            'perubahan': perubahan,
            'perubahan_persen': perubahan_persen,
            'tertinggi_30d': harga_tertinggi_30d,
            'terendah_30d': harga_terendah_30d,
            'volume': int(volume_sekarang),
            'volume_status': volume_status,
            'posisi': posisi,
            'posisi_desc': posisi_desc,
            'posisi_pct': posisi_harga_pct,
            'trend': trend,
            'momentum': momentum,
            'rsi': rsi,
            'rsi_status': rsi_status,
            'rekomendasi': rekomendasi,
            'rekomendasi_desc': rekomendasi_desc
        }
    except Exception as e:
        return None

# === TELEGRAM BOT HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /start"""
    welcome_message = """
🤖 <b>Selamat Datang di Stock Analysis Bot!</b>

Bot ini membantu Anda menganalisis saham dengan mudah menggunakan data real-time dari Yahoo Finance.

<b>📋 Cara Pakai:</b>
• Kirim kode saham (contoh: BBCA.JK, TLKM.JK)
• Atau gunakan command /analisis [KODE]

<b>🇮🇩 Saham Indonesia:</b>
• BBCA.JK - Bank BCA
• BBRI.JK - Bank BRI
• TLKM.JK - Telkom Indonesia
• GOTO.JK - GoTo Gojek Tokopedia
• ASII.JK - Astra International

<b>🇺🇸 Saham Amerika:</b>
• AAPL - Apple
• TSLA - Tesla
• GOOGL - Google
• MSFT - Microsoft

<b>📊 Commands:</b>
/start - Tampilkan menu ini
/analisis [KODE] - Analisis saham
/help - Bantuan

<b>Powered by Yahoo Finance 📈</b>
    """
    
    keyboard = [
        [InlineKeyboardButton("📊 Contoh: BBCA.JK", callback_data="example_BBCA.JK")],
        [InlineKeyboardButton("📈 Contoh: TLKM.JK", callback_data="example_TLKM.JK")],
        [InlineKeyboardButton("🌐 Buka Web App", url="http://localhost:5001")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /help"""
    help_text = """
<b>📚 PANDUAN PENGGUNAAN</b>

<b>1. Analisis Saham</b>
Kirim kode saham langsung atau gunakan:
<code>/analisis BBCA.JK</code>

<b>2. Format Kode Saham</b>
• Indonesia: Tambahkan .JK (BBCA.JK)
• Amerika: Langsung kode (AAPL)
• Crypto: Tambahkan -USD (BTC-USD)

<b>3. Penjelasan Istilah</b>
• <b>OVERSOLD</b>: Banyak yang jual, potensi naik
• <b>OVERBOUGHT</b>: Banyak yang beli, potensi turun
• <b>RSI</b>: Indikator kekuatan beli/jual (0-100)
• <b>Trend</b>: Arah pergerakan harga

<b>4. Rekomendasi</b>
🟢 BELI - Kondisi bagus
🟡 PERTIMBANGKAN - Riset lagi
🔴 JUAL - Sebaiknya jual
⚪ TUNGGU - Belum jelas

⚠️ <i>Disclaimer: Bukan saran investasi!</i>
    """
    await update.message.reply_text(help_text, parse_mode='HTML')

async def analisis_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /analisis"""
    if not context.args:
        await update.message.reply_text(
            "⚠️ Masukkan kode saham!\n\nContoh:\n<code>/analisis BBCA.JK</code>",
            parse_mode='HTML'
        )
        return
    
    ticker = context.args[0].upper()
    await process_stock_analysis(update, ticker)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk pesan text (kode saham)"""
    ticker = update.message.text.upper().strip()
    
    # Cek apakah seperti kode saham
    if len(ticker) > 1 and len(ticker) < 20:
        await process_stock_analysis(update, ticker)
    else:
        await update.message.reply_text(
            "🤔 Kirim kode saham yang valid\n\nContoh: BBCA.JK, TLKM.JK, AAPL"
        )

async def process_stock_analysis(update: Update, ticker: str):
    """Proses analisis saham"""
    # Kirim pesan loading
    loading_msg = await update.message.reply_text(
        f"⏳ Menganalisis {ticker}...\nTunggu sebentar ya!"
    )
    
    # Analisis
    result = analyze_stock_telegram(ticker)
    
    if not result:
        await loading_msg.edit_text(
            f"❌ Tidak dapat menganalisis {ticker}\n\n"
            "Pastikan kode saham benar:\n"
            "• Indonesia: BBCA.JK, TLKM.JK\n"
            "• Amerika: AAPL, TSLA, MSFT"
        )
        return
    
    # Format hasil
    message = f"""
📊 <b>ANALISIS SAHAM</b>

<b>{result['nama']}</b>
Kode: <code>{result['ticker']}</code>

━━━━━━━━━━━━━━━━━━━━
💰 <b>HARGA SAHAM</b>

Harga Sekarang: <b>Rp {result['harga']:,.0f}</b>
Perubahan: <code>{'+' if result['perubahan'] >= 0 else ''}{result['perubahan']:,.0f} ({result['perubahan_persen']:+.2f}%)</code>

Tertinggi 30 hari: Rp {result['tertinggi_30d']:,.0f}
Terendah 30 hari: Rp {result['terendah_30d']:,.0f}

━━━━━━━━━━━━━━━━━━━━
📊 <b>ANALISIS</b>

<b>Posisi Harga:</b> {result['posisi']}
{result['posisi_desc']} ({result['posisi_pct']:.1f}%)

<b>Trend:</b> {result['trend']}

<b>Momentum:</b> {result['momentum']}
RSI: {result['rsi']:.1f} - {result['rsi_status']}

<b>Volume Trading:</b> {result['volume_status']}
{result['volume']:,} lembar

━━━━━━━━━━━━━━━━━━━━
🎯 <b>REKOMENDASI</b>

{result['rekomendasi']}
<i>{result['rekomendasi_desc']}</i>

━━━━━━━━━━━━━━━━━━━━
⏰ {datetime.now().strftime('%d %b %Y, %H:%M')}

⚠️ <i>Disclaimer: Analisis ini hanya referensi.
Bukan saran investasi. DYOR!</i>
    """
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{ticker}")],
        [InlineKeyboardButton("📈 Lihat di Web", url="http://localhost:5001")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await loading_msg.edit_text(
        message,
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk inline button"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith("example_"):
        ticker = data.replace("example_", "")
        await query.message.reply_text(f"Menganalisis {ticker}...")
        await process_stock_analysis(update, ticker)
    
    elif data.startswith("refresh_"):
        ticker = data.replace("refresh_", "")
        await query.message.edit_text(f"⏳ Menganalisis ulang {ticker}...")
        await process_stock_analysis(update, ticker)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk error"""
    print(f"Error: {context.error}")

def main():
    """Main function untuk menjalankan bot"""
    print("🤖 Starting Telegram Stock Analysis Bot...")
    print(f"📱 Bot: @athal_saham_monitor_bot")
    print("=" * 50)
    
    # Buat application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analisis", analisis_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # Jalankan bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
