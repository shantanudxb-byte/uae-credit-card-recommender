#!/usr/bin/env python3
"""
Automated frontend-backend integration test
"""
import requests
import json
import subprocess
import time
import os
import signal
import sys

class IntegrationTester:
    def __init__(self):
        self.api_process = None
        self.base_url = 'http://localhost:5001'
    
    def start_backend(self):
        """Start the backend API server"""
        print("🚀 Starting backend server...")
        try:
            self.api_process = subprocess.Popen(
                [sys.executable, '-m', 'app.api'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(4)  # Wait for server to start
            
            # Test health endpoint
            response = requests.get(f'{self.base_url}/health', timeout=5)
            if response.status_code == 200:
                print("✅ Backend server running on port 5001")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def test_recommendation_api(self):
        """Test the main recommendation endpoint"""
        print("\n📊 Testing /api/recommend endpoint...")
        
        # Sample profile data (matches frontend form structure)
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
            response = requests.post(
                f'{self.base_url}/api/recommend',
                json=profile,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Validate response structure
                required_keys = ['recommendations', 'goal_based', 'spending_based', 'has_goals']
                missing_keys = [key for key in required_keys if key not in result]
                
                if missing_keys:
                    print(f"❌ Missing keys in response: {missing_keys}")
                    return False
                
                recommendations = result.get('recommendations', [])
                if len(recommendations) > 0:
                    print(f"✅ Got {len(recommendations)} recommendations")
                    
                    # Validate first recommendation structure
                    first_card = recommendations[0]
                    card_keys = ['card_name', 'bank', 'fit_score', 'reasons', 'estimated_annual_value']
                    missing_card_keys = [key for key in card_keys if key not in first_card]
                    
                    if missing_card_keys:
                        print(f"❌ Missing card keys: {missing_card_keys}")
                        return False
                    
                    print(f"✅ Top recommendation: {first_card['card_name']} (Score: {first_card['fit_score']})")
                    print(f"✅ Response structure valid")
                    return True
                else:
                    print("❌ No recommendations returned")
                    return False
            else:
                print(f"❌ API error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Request timeout - backend may be slow")
            return False
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return False
    
    def test_chat_api(self):
        """Test the chat endpoint"""
        print("\n💬 Testing /api/chat endpoint...")
        
        test_messages = [
            "What cards have no annual fee?",
            "Show me travel cards",
            "Compare Emirates vs Etihad cards"
        ]
        
        for message in test_messages:
            try:
                response = requests.post(
                    f'{self.base_url}/api/chat',
                    json={"message": message},
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'response' in result and len(result['response']) > 10:
                        print(f"✅ Chat response for '{message[:30]}...': {len(result['response'])} chars")
                    else:
                        print(f"❌ Empty/invalid chat response for '{message}'")
                        return False
                else:
                    print(f"❌ Chat API error: {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ Chat request failed: {e}")
                return False
        
        return True
    
    def test_filter_api(self):
        """Test the filter endpoint"""
        print("\n🔍 Testing /api/filter endpoint...")
        
        # First get some recommendations
        profile = {"salary": 15000, "spend": {"groceries": 2000}, "goals": ["cashback"]}
        
        try:
            rec_response = requests.post(f'{self.base_url}/api/recommend', json=profile, timeout=10)
            if rec_response.status_code != 200:
                print("❌ Could not get recommendations for filter test")
                return False
            
            recommendations = rec_response.json().get('recommendations', [])
            if not recommendations:
                print("❌ No recommendations to filter")
                return False
            
            # Test filtering
            filter_data = {
                "recommendations": recommendations,
                "filter_type": "annual_fee", 
                "choice": "no annual fee preferred"
            }
            
            filter_response = requests.post(
                f'{self.base_url}/api/filter',
                json=filter_data,
                timeout=10
            )
            
            if filter_response.status_code == 200:
                filtered = filter_response.json().get('filtered_recommendations', [])
                print(f"✅ Filter API working - filtered to {len(filtered)} cards")
                return True
            else:
                print(f"❌ Filter API error: {filter_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Filter test failed: {e}")
            return False
    
    def test_frontend_files(self):
        """Test that frontend files exist and have correct API URLs"""
        print("\n📁 Testing frontend files...")
        
        frontend_file = 'frontend/index.html'
        if not os.path.exists(frontend_file):
            print(f"❌ Frontend file missing: {frontend_file}")
            return False
        
        # Check if frontend has correct API URLs
        with open(frontend_file, 'r') as f:
            content = f.read()
            
        if 'localhost:5001' in content:
            print("✅ Frontend configured for correct API port (5001)")
        else:
            print("❌ Frontend not configured for port 5001")
            return False
        
        if '/api/recommend' in content and '/api/chat' in content:
            print("✅ Frontend has correct API endpoints")
        else:
            print("❌ Frontend missing API endpoints")
            return False
        
        return True
    
    def run_all_tests(self):
        """Run comprehensive integration tests"""
        print("🧪 Starting Frontend-Backend Integration Tests\n")
        
        # Test frontend files first
        if not self.test_frontend_files():
            print("\n❌ Frontend file tests failed")
            return False
        
        # Start backend
        if not self.start_backend():
            print("\n❌ Backend startup failed")
            return False
        
        try:
            # Run API tests
            tests = [
                ("Recommendation API", self.test_recommendation_api),
                ("Chat API", self.test_chat_api),
                ("Filter API", self.test_filter_api)
            ]
            
            results = {}
            for test_name, test_func in tests:
                results[test_name] = test_func()
            
            # Print summary
            print(f"\n📊 Test Results Summary:")
            print("-" * 40)
            for test_name, passed in results.items():
                status = "✅ PASS" if passed else "❌ FAIL"
                print(f"{test_name:<20}: {status}")
            
            all_passed = all(results.values())
            print("-" * 40)
            print(f"Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
            
            if all_passed:
                print("\n🎉 Frontend-backend integration is working correctly!")
                print("💡 You can now:")
                print("   1. Open frontend/index.html in your browser")
                print("   2. Fill out the form and submit")
                print("   3. Get personalized card recommendations")
                print("   4. Use the chat feature for questions")
            
            return all_passed
            
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up processes"""
        if self.api_process:
            try:
                self.api_process.terminate()
                self.api_process.wait(timeout=5)
            except:
                self.api_process.kill()
            print("\n🧹 Backend server stopped")

def main():
    tester = IntegrationTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())