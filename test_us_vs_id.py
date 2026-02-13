import requests

URL = "https://monitor-saham-nine.vercel.app/api/analyze-simple"

# Test with US stock first
print("Testing with US stock (AAPL)...")
response = requests.post(URL, json={"ticker": "AAPL"}, timeout=30)
print(f"Status: {response.status_code}")
data = response.json()

if 'error' in data:
    print(f"❌ Error: {data['error']}")
else:
    print(f"✅ Success!")
    print(f"   Ticker: {data.get('ticker')}")
    print(f"   Price: ${data.get('harga', {}).get('sekarang', 0):,.2f}")
 
print("\n" + "="*60 + "\n")

# Test with Indonesian stock
print("Testing with Indonesian stock (BBCA.JK)...")
response = requests.post(URL, json={"ticker": "BBCA.JK"}, timeout=30)
print(f"Status: {response.status_code}")
data = response.json()

if 'error' in data:
    print(f"❌ Error: {data['error']}")
else:
    print(f"✅ Success!")
    print(f"   Ticker: {data.get('ticker')}")
    print(f"   Price: Rp {data.get('harga', {}).get('sekarang', 0):,.0f}")
