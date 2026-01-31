#!/usr/bin/env python3
"""
Quick test script to verify the API is working
"""
import requests
import json

def test_api():
    # Test data
    profile = {
        "salary": 15000,
        "spend": {
            "groceries": 2000,
            "international_travel": 3000,
            "domestic_transport": 500,
            "fuel": 500,
            "online": 1000,
            "dining": 1500,
            "education": 0,
            "remittances": 0,
            "entertainment": 800,
            "healthcare": 300,
            "utilities": 400,
            "miscellaneous": 500
        },
        "goals": ["travel", "airport_lounge"],
        "lifestyle": {
            "groceries": [{"service": "lulu", "usage_percent": 60}],
            "online_shopping": [{"service": "amazon_ae", "usage_percent": 80}]
        }
    }
    
    try:
        # Test recommendations endpoint
        print("Testing /api/recommend endpoint...")
        response = requests.post(
            'http://localhost:5001/api/recommend',
            json=profile,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Got {len(result.get('recommendations', []))} recommendations")
            
            # Print first recommendation for verification
            if result.get('recommendations'):
                first_card = result['recommendations'][0]
                print(f"Top recommendation: {first_card['card_name']} (Score: {first_card['fit_score']})")
            
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the API server is running:")
        print("   python -m app.api")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat():
    try:
        print("\nTesting /api/chat endpoint...")
        response = requests.post(
            'http://localhost:5001/api/chat',
            json={"message": "What cards have no annual fee?"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat working! Response: {result.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ Chat error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing UAE Credit Card API...")
    
    if test_api():
        test_chat()
        print("\n✅ API tests completed successfully!")
        print("\n🌐 You can now open frontend/index.html in your browser")
    else:
        print("\n❌ API tests failed. Please start the server first:")
        print("   python -m app.api")