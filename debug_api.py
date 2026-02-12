import requests
import json

URL = "https://monitor-saham-nine.vercel.app/api/analyze-simple"

print("Testing API with different tickers...\n")

tickers = ["BBCA.JK", "TLKM.JK", "GOTO.JK", "BBRI.JK"]

for ticker in tickers:
    print(f"Testing: {ticker}")
    try:
        response = requests.post(
            URL,
            json={"ticker": ticker},
            timeout=30
        )
        print(f"Status: {response.status_code}")
        
        data = response.json()
        if 'error' in data:
            print(f"❌ Error: {data['error']}")
        else:
            print(f"✅ Success! Price: Rp {data.get('harga', {}).get('sekarang', 0):,.0f}")
        
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print("-" * 60)
