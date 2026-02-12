# 🚀 Deploy MarketPulse Pro ke Vercel

Panduan lengkap deploy aplikasi AI Stock Analysis ke Vercel.

---

## 📋 Prerequisites

✅ **Sudah Selesai:**
- ✅ Git repository initialized
- ✅ File vercel.json configured
- ✅ requirements.txt ready
- ✅ .gitignore configured
- ✅ All code committed

⏳ **Yang Perlu Dilakukan:**
1. Buat akun GitHub (jika belum punya)
2. Push code ke GitHub
3. Buat akun Vercel
4. Deploy dari Vercel dashboard

---

## 🔥 **METHOD 1: Deploy via Vercel Dashboard (RECOMMENDED)**

### Step 1: Push ke GitHub

1. **Buka GitHub** → https://github.com/new
   
2. **Create Repository:**
   - Repository name: `marketpulse-pro` (atau nama lain)
   - Description: `AI-Powered Stock Analysis Platform`
   - Public atau Private (bebas)
   - ❌ JANGAN centang "Add README" atau ".gitignore"
   - Klik **Create repository**

3. **Copy URL repository** (contoh: `https://github.com/username/marketpulse-pro.git`)

4. **Push code ke GitHub:**

Jalankan command ini di terminal PowerShell:

```powershell
# Masuk ke folder project
cd D:\TRADING

# Add remote GitHub
git remote add origin https://github.com/YOUR_USERNAME/marketpulse-pro.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** Ganti `YOUR_USERNAME` dengan username GitHub Anda!

### Step 2: Deploy ke Vercel

1. **Buka Vercel** → https://vercel.com

2. **Sign Up / Login:**
   - Klik "Sign Up"
   - Pilih **"Continue with GitHub"**
   - Authorize Vercel

3. **Import Project:**
   - Klik "Add New..." → "Project"
   - Pilih "Import Git Repository"
   - Cari dan pilih repository `marketpulse-pro`
   - Klik "Import"

4. **Configure Project:**
   - **Project Name:** marketpulse-pro (atau sesuai keinginan)
   - **Framework Preset:** Other
   - **Root Directory:** ./
   - **Build Command:** (kosongkan)
   - **Output Directory:** (kosongkan)
   - **Install Command:** `pip install -r requirements.txt`

5. **Environment Variables (Optional):**
   Klik "Add" jika mau set env vars:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   ```

6. **Deploy:**
   - Klik **"Deploy"**
   - Tunggu 2-3 menit
   - ✅ **DONE!**

7. **Get Your URL:**
   - URL format: `https://marketpulse-pro.vercel.app`
   - atau custom domain: `https://marketpulse-pro-yourusername.vercel.app`

---

## ⚡ **METHOD 2: Deploy via Vercel CLI**

### Step 1: Install Node.js & Vercel CLI

1. **Download Node.js:**
   - https://nodejs.org (LTS version)
   - Install dengan default settings

2. **Install Vercel CLI:**
```powershell
npm install -g vercel
```

3. **Verify Installation:**
```powershell
vercel --version
```

### Step 2: Login & Deploy

```powershell
# Login ke Vercel
vercel login

# Deploy (first time)
cd D:\TRADING
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (pilih account Anda)
# - Link to existing project? N
# - Project name? marketpulse-pro
# - In which directory? ./
# - Override settings? N

# Deploy to Production
vercel --prod
```

---

## 🔧 Troubleshooting

### Error: "Build Failed"
**Solusi:**
- Pastikan `requirements.txt` ada
- Cek Python version (Vercel support Python 3.9)
- Verifikasi semua dependencies terinstall

### Error: "Function Timeout"
**Penyebab:** Vercel free tier = 10 detik execution limit
**Solusi:**
- Reduce data fetching (gunakan cache)
- Optimize indicator calculations
- Upgrade ke Vercel Pro ($20/month)

### Error: "Module Not Found"
**Solusi:**
```powershell
# Update requirements.txt
pip freeze > requirements.txt

# Commit & push
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Watchlist/Alerts Not Persisting
**Penyebab:** Vercel serverless = no persistent filesystem
**Solusi:**
- Gunakan Vercel KV Database (Redis)
- Atau gunakan Supabase (PostgreSQL)
- Atau Firebase Realtime Database

---

## 📊 Post-Deployment

### Update Code (Git Push Auto-Deploy)

```powershell
# Make changes to code
# Then commit and push

git add .
git commit -m "Update feature X"
git push

# Vercel akan auto-deploy!
```

### Set Custom Domain

1. **Vercel Dashboard:**
   - Pilih project
   - Tab "Settings" → "Domains"
   - Add domain: `yourdomain.com`

2. **Update DNS:**
   - Add CNAME record: `cname.vercel-dns.com`

### Monitor Analytics

- **Vercel Dashboard → Analytics**
- View:
  - Page views
  - Unique visitors
  - Function invocations
  - Error rates

---

## 🎯 Vercel Limits (Free Tier)

| Feature | Free Tier | Pro Tier |
|---------|-----------|----------|
| Bandwidth | 100GB/month | 1TB/month |
| Invocations | 100K/month | Unlimited |
| Build Time | 6000 minutes | 24000 minutes |
| Function Duration | 10s | 60s |
| Concurrent Builds | 1 | 12 |

---

## 💡 Tips Optimization

### 1. Cache Data
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_stock_data(ticker):
    # Cached for faster response
    return yf.download(ticker)
```

### 2. Reduce Dependencies
```python
# Only import what you need
from flask import Flask, jsonify
```

### 3. Use CDN for Static Files
- Upload Chart.js, Tailwind ke CDN
- Reduce bundle size

### 4. Enable Compression
```python
from flask_compress import Compress
Compress(app)
```

---

## 🚀 Alternative Hosting

Jika Vercel tidak cocok:

### Railway.app
- ✅ Longer execution time (30 mins)
- ✅ Persistent filesystem
- ✅ PostgreSQL included
- 💰 $5/month

### Render.com
- ✅ Free tier generous
- ✅ Auto-deploy from GitHub
- ✅ Background workers
- ⚠️ Slower cold starts

### PythonAnywhere
- ✅ Specifically for Python
- ✅ Easy deployment
- ✅ MySQL included
- 💰 $5/month

---

## ✅ Checklist Deploy

- [ ] Git repository created
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Project imported to Vercel
- [ ] Deployment successful
- [ ] Test live URL
- [ ] All features working
- [ ] Watchlist persists (atau setup database)
- [ ] Alerts working
- [ ] Top movers loading
- [ ] Chart rendering
- [ ] Mobile responsive

---

## 📞 Support

**Jika stuck:**
1. Check Vercel deployment logs
2. Test locally dulu (`python app_simple.py`)
3. Google error message
4. Ask ChatGPT/Claude
5. Email: angwynren@gmail.com

---

## 🎉 Congratulations!

Aplikasi Anda sudah LIVE dan bisa diakses di internet!

**Share URL Anda:**
- https://marketpulse-pro.vercel.app
- Social media: LinkedIn, Twitter, Instagram
- Portfolio: Tambahkan ke CV/Resume

**Next Steps:**
- [ ] Add custom domain
- [ ] Setup analytics (Google Analytics)
- [ ] Add more features
- [ ] Get user feedback
- [ ] Monetize (premium features, ads)

---

Made with ❤️ by Athala Angyn Renaldi
