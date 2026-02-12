# Test Vercel Deployment
# Run this after deployment completes

import requests
import json

# Your actual Vercel URL
BASE_URL = "https://monitor-saham-nine.vercel.app"

def test_homepage():
    """Test if homepage loads"""
    print("🏠 Testing homepage...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ Homepage loads successfully!")
            return True
        else:
            print(f"❌ Homepage failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_stock_analysis():
    """Test stock analysis API"""
    print("\n📊 Testing stock analysis...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze-simple",
            json={"ticker": "BBCA.JK"},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                print(f"❌ API returned error: {data['error']}")
                return False
            print("✅ Stock analysis works!")
            print(f"   Ticker: {data.get('ticker')}")
            print(f"   Price: Rp {data.get('harga', {}).get('sekarang', 0):,.0f}")
            return True
        else:
            print(f"❌ API failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_watchlist():
    """Test watchlist API"""
    print("\n⭐ Testing watchlist...")
    try:
        response = requests.get(f"{BASE_URL}/api/watchlist")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Watchlist works! Items: {len(data.get('watchlist', []))}")
            return True
        else:
            print(f"❌ Watchlist failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_top_movers():
    """Test top movers API"""
    print("\n🔥 Testing top movers...")
    try:
        response = requests.get(f"{BASE_URL}/api/top-movers", timeout=30)
        if response.status_code == 200:
            data = response.json()
            gainers = len(data.get('gainers', []))
            losers = len(data.get('losers', []))
            print(f"✅ Top movers works! Gainers: {gainers}, Losers: {losers}")
            return True
        else:
            print(f"❌ Top movers failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("="*60)
    print("🧪 VERCEL DEPLOYMENT TEST")
    print("="*60)
    print(f"\nTesting URL: {BASE_URL}\n")
    
    results = []
    results.append(("Homepage", test_homepage()))
    results.append(("Stock Analysis", test_stock_analysis()))
    results.append(("Watchlist", test_watchlist()))
    results.append(("Top Movers", test_top_movers()))
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} : {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! Deployment successful!")
    else:
        print("\n⚠️  Some tests failed. Check Vercel logs for details.")
        print("   Dashboard: https://vercel.com/dashboard")

if __name__ == "__main__":
    main()
