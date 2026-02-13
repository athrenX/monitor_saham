// Multi-language support for StockPro AI
const translations = {
    id: {
        // Navigation
        'app.title': 'StockPro AI',
        'app.tagline': 'Platform Analisis Saham Profesional',
        'nav.features': 'Fitur',
        'nav.documentation': 'Dokumentasi',
        'nav.language': 'Bahasa',
        'nav.theme': 'Tema',
        
        // Main Interface
        'hero.title': 'Analisis Saham Real-Time dengan AI',
        'hero.subtitle': 'Platform trading profesional dengan 13 indikator teknikal dan AI scoring',
        'input.ticker': 'Masukkan Ticker Saham',
        'input.placeholder': 'Contoh: BBCA.JK, BBRI.JK, AAPL',
        'btn.analyze': 'Analisis Sekarang',
        'btn.loading': 'Menganalisis...',
        
        // Analysis Section
        'analysis.inputPlaceholder': 'Masukkan kode saham (contoh: BBCA.JK)',
        'analysis.button': 'ANALISIS SEKARANG',
        
        // Watchlist
        'watchlist.title': 'Watchlist Saya',
        'watchlist.addButton': 'Tambah Saham',
        'watchlist.quickAdd': 'Tambah Saham Saat Ini',
        
        // Company Info
        'company.info': 'Informasi Perusahaan',
        'company.sector': 'Sektor',
        'company.industry': 'Industri',
        'company.employees': 'Karyawan',
        'company.market_cap': 'Market Cap',
        'company.website': 'Website',
        
        // Chart Controls
        'chart.title': 'Grafik Harga',
        'chart.candlestick': 'Candlestick',
        'chart.line': 'Line Chart',
        'chart.zoom_in': 'Perbesar',
        'chart.zoom_out': 'Perkecil',
        'chart.reset': 'Reset Zoom',
        
        // Technical Indicators
        'indicators.title': 'Indikator Teknikal',
        'indicators.rsi': 'RSI (14)',
        'indicators.macd': 'MACD',
        'indicators.bb': 'Bollinger Bands',
        'indicators.stoch': 'Stochastic',
        'indicators.atr': 'ATR (14)',
        'indicators.volume': 'Volume',
        
        // AI Analysis
        'ai.title': 'Analisis AI',
        'ai.score': 'Skor AI',
        'ai.recommendation': 'Rekomendasi',
        'ai.confidence': 'Confidence',
        'ai.strong_buy': 'BELI KUAT',
        'ai.buy': 'BELI',
        'ai.hold': 'TAHAN',
        'ai.sell': 'JUAL',
        'ai.strong_sell': 'JUAL KUAT',
        
        // Signals
        'signal.trend': 'Sinyal Trend',
        'signal.momentum': 'Sinyal Momentum',
        'signal.volume': 'Sinyal Volume',
        'signal.volatility': 'Sinyal Volatilitas',
        'signal.bullish': 'BULLISH',
        'signal.bearish': 'BEARISH',
        'signal.neutral': 'NETRAL',
        'signal.high': 'TINGGI',
        'signal.low': 'RENDAH',
        'signal.normal': 'NORMAL',
        
        // Watchlist
        'watchlist.title': 'Watchlist Saya',
        'watchlist.add': 'Tambah ke Watchlist',
        'watchlist.remove': 'Hapus dari Watchlist',
        'watchlist.empty': 'Belum ada saham di watchlist',
        'watchlist.loading': 'Memuat harga...',
        
        // Price Alert
        'alert.title': 'Set Price Alert',
        'alert.subtitle': 'Dapatkan notifikasi saat target harga tercapai',
        'alert.ticker': 'Ticker Saham',
        'alert.condition': 'Kondisi Alert',
        'alert.condition.above': '📈 Harga di atas target',
        'alert.condition.below': '📉 Harga di bawah target',
        'alert.target': 'Target Harga (Rp)',
        'alert.whatsapp': 'WhatsApp',
        'alert.whatsapp.optional': 'Opsional',
        'alert.whatsapp.format': 'Format: 628xxx (tanpa +). Kosongkan jika tidak perlu notifikasi WA.',
        'alert.btn.cancel': 'Batal',
        'alert.btn.save': 'Simpan Alert',
        'alert.success': 'Alert berhasil dibuat',
        'alert.error.price': 'Masukkan harga target yang valid',
        'alert.error.whatsapp': 'Format WhatsApp tidak valid. Gunakan: 628123456789',
        
        // Top Movers
        'movers.title': 'Top Movers',
        'movers.gainers': 'Top Gainers',
        'movers.losers': 'Top Losers',
        
        // News
        'news.title': 'Berita Terkini',
        'news.loading': 'Memuat berita...',
        'news.empty': 'Tidak ada berita tersedia',
        
        // Notifications
        'notif.success': 'Berhasil!',
        'notif.error': 'Terjadi Kesalahan',
        'notif.warning': 'Peringatan',
        'notif.info': 'Informasi',
        
        // Documentation
        'docs.title': 'Dokumentasi Fitur',
        'docs.subtitle': 'Panduan lengkap menggunakan StockPro AI',
        'docs.close': 'Tutup',
        
        // Features in Documentation
        'docs.feature1.title': '🎯 Analisis Real-Time',
        'docs.feature1.desc': 'Dapatkan data harga saham real-time dari Yahoo Finance dengan update otomatis setiap 30 detik.',
        
        'docs.feature2.title': '📊 13 Indikator Teknikal',
        'docs.feature2.desc': 'RSI, MACD, Bollinger Bands, Stochastic, ATR, Moving Averages (7, 30, 50), dan Exponential Moving Averages (9, 21, 50).',
        
        'docs.feature3.title': '🤖 AI Multi-Factor Scoring',
        'docs.feature3.desc': 'Sistem scoring otomatis dengan 4 faktor: Trend (35%), Momentum (30%), Volume (20%), dan Volatilitas (15%).',
        
        'docs.feature4.title': '📈 Interactive Charts',
        'docs.feature4.desc': 'Chart.js dengan zoom, pan, dan toggle antara line chart dan candlestick. Klik dan drag untuk zoom area tertentu.',
        
        'docs.feature5.title': '⏰ Price Alerts',
        'docs.feature5.desc': 'Set alert untuk harga target dengan notifikasi WhatsApp otomatis saat harga tercapai. Cek otomatis setiap 60 detik.',
        
        'docs.feature6.title': '👀 Watchlist',
        'docs.feature6.desc': 'Simpan saham favorit Anda dengan update harga real-time. Klik saham di watchlist untuk analisis cepat.',
        
        'docs.feature7.title': '📱 WhatsApp Integration',
        'docs.feature7.desc': 'Terima notifikasi langsung via WhatsApp menggunakan Fonnte API. Welcome message otomatis saat membuat alert.',
        
        'docs.feature8.title': '🌐 Multi-Language',
        'docs.feature8.desc': 'Bahasa Indonesia dan English. Ganti bahasa dengan klik tombol di navbar.',
        
        'docs.feature9.title': '🎨 Dark/Light Theme',
        'docs.feature9.desc': 'Toggle antara tema gelap dan terang sesuai preferensi Anda.',
        
        'docs.feature10.title': '📰 Market News',
        'docs.feature10.desc': 'Berita pasar terkini dan analisis fundamental untuk keputusan trading yang lebih baik.',
        
        'docs.usage.title': 'Cara Penggunaan',
        'docs.usage.step1': '1. Masukkan ticker saham (contoh: BBCA.JK untuk BCA, AAPL untuk Apple)',
        'docs.usage.step2': '2. Klik "Analisis Sekarang" untuk mendapatkan analisis lengkap',
        'docs.usage.step3': '3. Lihat grafik harga, indikator teknikal, dan rekomendasi AI',
        'docs.usage.step4': '4. Tambahkan ke watchlist untuk monitoring cepat',
        'docs.usage.step5': '5. Set price alert dengan WhatsApp untuk notifikasi otomatis',
        'docs.usage.step6': '6. Gunakan zoom dan pan pada chart untuk analisis detail',
        
        'docs.tips.title': 'Tips Profesional',
        'docs.tips.tip1': '💡 Gunakan multiple timeframe untuk konfirmasi sinyal',
        'docs.tips.tip2': '💡 Perhatikan volume saat harga breakout untuk validasi',
        'docs.tips.tip3': '💡 RSI > 70 = overbought, RSI < 30 = oversold',
        'docs.tips.tip4': '💡 MACD crossover di atas zero line = sinyal bullish kuat',
        'docs.tips.tip5': '💡 Harga menyentuh lower BB = potensi support',
        'docs.tips.tip6': '💡 ATR tinggi = volatilitas tinggi, gunakan stop loss lebih lebar',
    },
    
    en: {
        // Navigation
        'app.title': 'StockPro AI',
        'app.tagline': 'Professional Stock Analysis Platform',
        'nav.features': 'Features',
        'nav.documentation': 'Documentation',
        'nav.language': 'Language',
        'nav.theme': 'Theme',
        
        // Main Interface
        'hero.title': 'Real-Time Stock Analysis with AI',
        'hero.subtitle': 'Professional trading platform with 13 technical indicators and AI scoring',
        'input.ticker': 'Enter Stock Ticker',
        'input.placeholder': 'Example: BBCA.JK, BBRI.JK, AAPL',
        'btn.analyze': 'Analyze Now',
        'btn.loading': 'Analyzing...',
        
        // Analysis Section
        'analysis.inputPlaceholder': 'Enter stock ticker (example: BBCA.JK)',
        'analysis.button': 'ANALYZE NOW',
        
        // Watchlist
        'watchlist.title': 'My Watchlist',
        'watchlist.addButton': 'Add Stock',
        'watchlist.quickAdd': 'Add Current Stock',
        
        // Company Info
        'company.info': 'Company Information',
        'company.sector': 'Sector',
        'company.industry': 'Industry',
        'company.employees': 'Employees',
        'company.market_cap': 'Market Cap',
        'company.website': 'Website',
        
        // Chart Controls
        'chart.title': 'Price Chart',
        'chart.candlestick': 'Candlestick',
        'chart.line': 'Line Chart',
        'chart.zoom_in': 'Zoom In',
        'chart.zoom_out': 'Zoom Out',
        'chart.reset': 'Reset Zoom',
        
        // Technical Indicators
        'indicators.title': 'Technical Indicators',
        'indicators.rsi': 'RSI (14)',
        'indicators.macd': 'MACD',
        'indicators.bb': 'Bollinger Bands',
        'indicators.stoch': 'Stochastic',
        'indicators.atr': 'ATR (14)',
        'indicators.volume': 'Volume',
        
        // AI Analysis
        'ai.title': 'AI Analysis',
        'ai.score': 'AI Score',
        'ai.recommendation': 'Recommendation',
        'ai.confidence': 'Confidence',
        'ai.strong_buy': 'STRONG BUY',
        'ai.buy': 'BUY',
        'ai.hold': 'HOLD',
        'ai.sell': 'SELL',
        'ai.strong_sell': 'STRONG SELL',
        
        // Signals
        'signal.trend': 'Trend Signal',
        'signal.momentum': 'Momentum Signal',
        'signal.volume': 'Volume Signal',
        'signal.volatility': 'Volatility Signal',
        'signal.bullish': 'BULLISH',
        'signal.bearish': 'BEARISH',
        'signal.neutral': 'NEUTRAL',
        'signal.high': 'HIGH',
        'signal.low': 'LOW',
        'signal.normal': 'NORMAL',
        
        // Watchlist
        'watchlist.title': 'My Watchlist',
        'watchlist.add': 'Add to Watchlist',
        'watchlist.remove': 'Remove from Watchlist',
        'watchlist.empty': 'No stocks in watchlist yet',
        'watchlist.loading': 'Loading prices...',
        
        // Price Alert
        'alert.title': 'Set Price Alert',
        'alert.subtitle': 'Get notified when target price is reached',
        'alert.ticker': 'Stock Ticker',
        'alert.condition': 'Alert Condition',
        'alert.condition.above': '📈 Price above target',
        'alert.condition.below': '📉 Price below target',
        'alert.target': 'Target Price',
        'alert.whatsapp': 'WhatsApp',
        'alert.whatsapp.optional': 'Optional',
        'alert.whatsapp.format': 'Format: 628xxx (without +). Leave empty if no WA notification needed.',
        'alert.btn.cancel': 'Cancel',
        'alert.btn.save': 'Save Alert',
        'alert.success': 'Alert created successfully',
        'alert.error.price': 'Enter valid target price',
        'alert.error.whatsapp': 'Invalid WhatsApp format. Use: 628123456789',
        
        // Top Movers
        'movers.title': 'Top Movers',
        'movers.gainers': 'Top Gainers',
        'movers.losers': 'Top Losers',
        
        // News
        'news.title': 'Latest News',
        'news.loading': 'Loading news...',
        'news.empty': 'No news available',
        
        // Notifications
        'notif.success': 'Success!',
        'notif.error': 'Error Occurred',
        'notif.warning': 'Warning',
        'notif.info': 'Information',
        
        // Documentation
        'docs.title': 'Feature Documentation',
        'docs.subtitle': 'Complete guide to using StockPro AI',
        'docs.close': 'Close',
        
        // Features in Documentation
        'docs.feature1.title': '🎯 Real-Time Analysis',
        'docs.feature1.desc': 'Get real-time stock price data from Yahoo Finance with automatic updates every 30 seconds.',
        
        'docs.feature2.title': '📊 13 Technical Indicators',
        'docs.feature2.desc': 'RSI, MACD, Bollinger Bands, Stochastic, ATR, Moving Averages (7, 30, 50), and Exponential Moving Averages (9, 21, 50).',
        
        'docs.feature3.title': '🤖 AI Multi-Factor Scoring',
        'docs.feature3.desc': 'Automatic scoring system with 4 factors: Trend (35%), Momentum (30%), Volume (20%), and Volatility (15%).',
        
        'docs.feature4.title': '📈 Interactive Charts',
        'docs.feature4.desc': 'Chart.js with zoom, pan, and toggle between line chart and candlestick. Click and drag to zoom specific area.',
        
        'docs.feature5.title': '⏰ Price Alerts',
        'docs.feature5.desc': 'Set alerts for target prices with automatic WhatsApp notifications when price is reached. Auto-check every 60 seconds.',
        
        'docs.feature6.title': '👀 Watchlist',
        'docs.feature6.desc': 'Save your favorite stocks with real-time price updates. Click stocks in watchlist for quick analysis.',
        
        'docs.feature7.title': '📱 WhatsApp Integration',
        'docs.feature7.desc': 'Receive notifications directly via WhatsApp using Fonnte API. Automatic welcome message when creating alerts.',
        
        'docs.feature8.title': '🌐 Multi-Language',
        'docs.feature8.desc': 'Indonesian and English language support. Switch language by clicking button in navbar.',
        
        'docs.feature9.title': '🎨 Dark/Light Theme',
        'docs.feature9.desc': 'Toggle between dark and light themes according to your preference.',
        
        'docs.feature10.title': '📰 Market News',
        'docs.feature10.desc': 'Latest market news and fundamental analysis for better trading decisions.',
        
        'docs.usage.title': 'How to Use',
        'docs.usage.step1': '1. Enter stock ticker (example: BBCA.JK for BCA, AAPL for Apple)',
        'docs.usage.step2': '2. Click "Analyze Now" to get complete analysis',
        'docs.usage.step3': '3. View price chart, technical indicators, and AI recommendations',
        'docs.usage.step4': '4. Add to watchlist for quick monitoring',
        'docs.usage.step5': '5. Set price alert with WhatsApp for automatic notifications',
        'docs.usage.step6': '6. Use zoom and pan on chart for detailed analysis',
        
        'docs.tips.title': 'Professional Tips',
        'docs.tips.tip1': '💡 Use multiple timeframes to confirm signals',
        'docs.tips.tip2': '💡 Watch volume when price breaks out for validation',
        'docs.tips.tip3': '💡 RSI > 70 = overbought, RSI < 30 = oversold',
        'docs.tips.tip4': '💡 MACD crossover above zero line = strong bullish signal',
        'docs.tips.tip5': '💡 Price touching lower BB = potential support',
        'docs.tips.tip6': '💡 High ATR = high volatility, use wider stop loss',
    }
};

// Current language (default: Indonesian)
let currentLang = localStorage.getItem('stockpro_lang') || 'id';

// Translate function
function t(key) {
    return translations[currentLang][key] || key;
}

// Switch language
function switchLanguage(lang) {
    if (lang !== 'id' && lang !== 'en') return;
    currentLang = lang;
    localStorage.setItem('stockpro_lang', lang);
    updatePageLanguage();
    showNotification(
        lang === 'id' ? '✅ Bahasa diubah ke Indonesia' : '✅ Language changed to English',
        'success'
    );
}

// Update all text on page
function updatePageLanguage() {
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translation = t(key);
        
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            el.placeholder = translation;
        } else {
            el.textContent = translation;
        }
    });
    
    // Update elements with data-i18n-placeholder attribute
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        const translation = t(key);
        el.placeholder = translation;
    });
    
    // Update document title
    document.title = t('app.title') + ' - ' + t('app.tagline');
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', () => {
    updatePageLanguage();
});
