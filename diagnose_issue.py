#!/usr/bin/env python3
"""Diagnose frontend loading issues"""

import requests
import time
import json

API_URL = "http://localhost:5001"

def test_health():
    """Test if API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        print(f"✓ API Health: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"✗ API Health Failed: {e}")
        return False

def test_recommend():
    """Test recommendation endpoint"""
    profile = {
        "salary": 15000,
        "spend": {
            "groceries": 2000,
            "online": 1500,
            "dining": 1000,
            "fuel": 500,
            "international_travel": 0,
            "domestic_transport": 0,
            "education": 0,
            "remittances": 0,
            "entertainment": 0,
            "healthcare": 0,
            "utilities": 0,
            "miscellaneous": 0
        },
        "goals": ["cashback", "online"],
        "lifestyle": {}
    }
    
    try:
        print("\n⏱️  Testing /api/recommend endpoint...")
        start = time.time()
        response = requests.post(f"{API_URL}/api/recommend", json=profile, timeout=30)
        elapsed = time.time() - start
        
        print(f"✓ Recommend: {response.status_code} - took {elapsed:.2f}s")
        if response.ok:
            data = response.json()
            print(f"  - Recommendations: {len(data.get('recommendations', []))}")
            print(f"  - Goal-based: {len(data.get('goal_based', []))}")
            print(f"  - Spending-based: {len(data.get('spending_based', []))}")
        else:
            print(f"  - Error: {response.text}")
        return True
    except Exception as e:
        print(f"✗ Recommend Failed: {e}")
        return False

def test_chat():
    """Test chat endpoint"""
    try:
        print("\n⏱️  Testing /api/chat endpoint...")
        start = time.time()
        response = requests.post(
            f"{API_URL}/api/chat",
            json={"message": "What cards have no annual fee?"},
            timeout=30
        )
        elapsed = time.time() - start
        
        print(f"✓ Chat: {response.status_code} - took {elapsed:.2f}s")
        if response.ok:
            data = response.json()
            print(f"  - Response length: {len(data.get('response', ''))}")
        else:
            print(f"  - Error: {response.text}")
        return True
    except Exception as e:
        print(f"✗ Chat Failed: {e}")
        return False

def test_generate_questions():
    """Test question generation endpoint"""
    try:
        print("\n⏱️  Testing /api/generate-questions endpoint...")
        start = time.time()
        response = requests.post(
            f"{API_URL}/api/generate-questions",
            json={
                "salary": 15000,
                "spend": {"miscellaneous": 2000, "online": 1500},
                "lifestyle": {}
            },
            timeout=10
        )
        elapsed = time.time() - start
        
        print(f"✓ Generate Questions: {response.status_code} - took {elapsed:.2f}s")
        if response.ok:
            data = response.json()
            print(f"  - Should ask: {data.get('should_ask')}")
            print(f"  - Questions: {len(data.get('questions', []))}")
        else:
            print(f"  - Error: {response.text}")
        return True
    except Exception as e:
        print(f"✗ Generate Questions Failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DIAGNOSING FRONTEND LOADING ISSUE")
    print("=" * 60)
    
    if not test_health():
        print("\n❌ API is not running! Start it with: python3 -m app.api")
        exit(1)
    
    test_recommend()
    test_chat()
    test_generate_questions()
    
    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)
