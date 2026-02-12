# 🚀 Deploy StockPro AI ke Vercel

## 📋 Prerequisites

1. **Akun Vercel**
   - Buat akun di [vercel.com](https://vercel.com)
   - Install Vercel CLI: `npm install -g vercel`

2. **GitHub Repository (Opsional)**
   - Push code ke GitHub untuk auto-deployment

## 🔧 Setup Langkah demi Langkah

### Metode 1: Deploy via CLI (Tercepat)

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login ke Vercel
vercel login

# 3. Deploy dari folder project
cd D:\TRADING
vercel

# 4. Ikuti prompt:
#    - Set up and deploy? Y
#    - Which scope? [pilih account Anda]
#    - Link to existing project? N
#    - What's your project's name? stockpro-ai
#    - In which directory is your code located? ./
#    - Want to override settings? N

# 5. Deploy production
vercel --prod
```

### Metode 2: Deploy via GitHub (Recommended)

```bash
# 1. Create GitHub repository baru
# 2. Push code ke GitHub:

git init
git add .
git commit -m "Initial commit - StockPro AI"
git remote add origin https://github.com/USERNAME/stockpro-ai.git
git push -u origin main

# 3. Di Vercel Dashboard:
#    - Klik "New Project"
#    - Import dari GitHub
#    - Pilih repository stockpro-ai
#    - Framework Preset: Other
#    - Build Command: (kosongkan)
#    - Output Directory: (kosongkan)
#    - Install Command: pip install -r requirements.txt
#    - Klik Deploy
```

### Metode 3: Deploy via Vercel Dashboard

1. Zip folder `D:\TRADING` (exclude `.venv`, `__pycache__`)
2. Buka [vercel.com/new](https://vercel.com/new)
3. Drag & drop zip file
4. Deploy!

## ⚙️ Configuration

### Environment Variables (Jika Diperlukan)

Di Vercel Dashboard → Settings → Environment Variables:

```
FLASK_ENV=production
```

## 🔍 Troubleshooting

### Error: Module not found
```bash
# Pastikan requirements.txt lengkap
# Re-deploy dengan:
vercel --prod --force
```

### Error: Function timeout
```json
// Tambahkan di vercel.json:
{
  "functions": {
    "api/index.py": {
      "maxDuration": 30
    }
  }
}
```

### Error: Memory limit
```json
// Tambahkan di vercel.json:
{
  "functions": {
    "api/index.py": {
      "memory": 1024
    }
  }
}
```

## 📱 Custom Domain (Opsional)

1. Beli domain (Namecheap, GoDaddy, dll)
2. Di Vercel Dashboard → Settings → Domains
3. Add domain dan ikuti instruksi DNS

## 🎯 Testing

Setelah deploy, test URL:
```
https://stockpro-ai.vercel.app/commercial
```

## 🚀 Update/Redeploy

```bash
# Metode CLI
vercel --prod

# Metode GitHub (auto-deploy)
git add .
git commit -m "Update features"
git push
```

## 📊 Monitoring

- Lihat logs: Vercel Dashboard → Deployments → View Function Logs
- Analytics: Vercel Dashboard → Analytics
- Performance: Vercel Dashboard → Speed Insights

## 💰 Pricing

- **Hobby (Free)**: 
  - 100GB bandwidth/month
  - Unlimited deployments
  - Serverless Functions: 100 hours/month
  - Perfect untuk portfolio/demo

- **Pro ($20/month)**:
  - Unlimited bandwidth
  - Advanced analytics
  - Priority support

## ✅ Checklist Deploy

- [ ] File `vercel.json` ada
- [ ] File `requirements.txt` lengkap
- [ ] File `api/index.py` ada
- [ ] Test lokal: `python app_simple.py`
- [ ] Login Vercel CLI: `vercel login`
- [ ] Deploy: `vercel --prod`
- [ ] Test production URL
- [ ] Setup custom domain (optional)

## 🔗 Useful Links

- Vercel Docs: https://vercel.com/docs
- Python on Vercel: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- Flask on Vercel: https://vercel.com/guides/using-flask-with-vercel

---

**Need Help?** Contact support atau check Vercel Community forums.
