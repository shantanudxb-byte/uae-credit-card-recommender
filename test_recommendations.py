#!/usr/bin/env python3

import json
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from agent import CardAdvisor

def run_evaluation():
    print("=== CREDIT CARD RECOMMENDATION EVALUATION ===\n")
    
    advisor = CardAdvisor()
    
    test_cases = [
        {
            "id": 1,
            "name": "High ADNOC Spender",
            "profile": {
                "salary": 8000,
                "spend": {"fuel": 1200, "groceries": 1500, "dining": 800},
                "goals": ["fuel", "adnoc"]
            },
            "expected_contains": "ADNOC"
        },
        {
            "id": 2,
            "name": "Fitness Enthusiast",
            "profile": {
                "salary": 12000,
                "spend": {"groceries": 2000, "dining": 1000, "online": 800},
                "goals": ["fitness", "gym"]
            },
            "expected_contains": "Active"
        },
        {
            "id": 3,
            "name": "Budget Lounge Seeker",
            "profile": {
                "salary": 6000,
                "spend": {"travel": 500, "dining": 800, "online": 1200},
                "goals": ["airport_lounge", "no_fee"]
            },
            "expected_contains": "Indulge"
        },
        {
            "id": 4,
            "name": "Amazon Heavy User",
            "profile": {
                "salary": 18000,
                "spend": {"online": 3000, "groceries": 2500, "dining": 1200},
                "goals": ["amazon", "online"]
            },
            "expected_contains": "Amazon"
        },
        {
            "id": 5,
            "name": "Streaming User",
            "profile": {
                "salary": 7000,
                "spend": {"online": 800, "dining": 600, "groceries": 1200},
                "goals": ["streaming", "digital"]
            },
            "expected_contains": "Z Card"
        },
        {
            "id": 6,
            "name": "Fashion Shopper",
            "profile": {
                "salary": 9000,
                "spend": {"online": 2000, "dining": 1500, "groceries": 1800},
                "goals": ["fashion", "cashback"]
            },
            "expected_contains": "Cashback"
        },
        {
            "id": 7,
            "name": "Etihad Flyer",
            "profile": {
                "salary": 15000,
                "spend": {"travel": 4000, "dining": 2000, "groceries": 1500},
                "goals": ["etihad", "miles"]
            },
            "expected_contains": "Etihad"
        },
        {
            "id": 8,
            "name": "Man City Fan",
            "profile": {
                "salary": 8000,
                "spend": {"dining": 1000, "online": 800, "travel": 1200},
                "goals": ["manchester_city", "sports"]
            },
            "expected_contains": "Manchester City"
        },
        {
            "id": 9,
            "name": "High Earner",
            "profile": {
                "salary": 60000,
                "spend": {"travel": 8000, "dining": 3000, "groceries": 2000},
                "goals": ["premium", "luxury"]
            },
            "expected_contains": "Elite"
        },
        {
            "id": 10,
            "name": "Grocery Shopper",
            "profile": {
                "salary": 12000,
                "spend": {"groceries": 3000, "online": 1500, "dining": 1200},
                "goals": ["groceries", "cashback"]
            },
            "expected_contains": "Cashback"
        },
        {
            "id": 11,
            "name": "Entry Level",
            "profile": {
                "salary": 5500,
                "spend": {"groceries": 800, "online": 600, "dining": 400},
                "goals": ["no_fee"]
            },
            "expected_contains": "Liv"
        },
        {
            "id": 12,
            "name": "International Spender",
            "profile": {
                "salary": 20000,
                "spend": {"travel": 5000, "online": 2000, "dining": 1800},
                "goals": ["travel", "international"]
            },
            "expected_contains": "Amazon"
        },
        {
            "id": 13,
            "name": "Online Shopper",
            "profile": {
                "salary": 8000,
                "spend": {"online": 2500, "groceries": 1200, "dining": 800},
                "goals": ["online"]
            },
            "expected_contains": "online"
        },
        {
            "id": 14,
            "name": "Balanced Spender",
            "profile": {
                "salary": 6000,
                "spend": {"groceries": 2000, "fuel": 600, "dining": 500},
                "goals": ["groceries"]
            },
            "expected_contains": "groceries"
        },
        {
            "id": 15,
            "name": "Dining Enthusiast",
            "profile": {
                "salary": 35000,
                "spend": {"dining": 4000, "travel": 3000, "online": 2000},
                "goals": ["dining", "premium"]
            },
            "expected_contains": "dining"
        },
        {
            "id": 16,
            "name": "Parent with Kids",
            "profile": {
                "salary": 25000,
                "spend": {"groceries": 2000, "fuel": 800, "dining": 1200},
                "goals": ["education", "family"]
            },
            "expected_contains": "GEMS"
        },
        {
            "id": 17,
            "name": "Entertainment Lover",
            "profile": {
                "salary": 12000,
                "spend": {"dining": 1500, "online": 2500, "groceries": 1200},
                "goals": ["entertainment"]
            },
            "expected_contains": "entertainment"
        },
        {
            "id": 18,
            "name": "Low Salary",
            "profile": {
                "salary": 3000,
                "spend": {"groceries": 600, "online": 400, "dining": 300},
                "goals": ["no_salary"]
            },
            "expected_contains": "WIO"
        },
        {
            "id": 19,
            "name": "Travel Focused",
            "profile": {
                "salary": 12000,
                "spend": {"travel": 2000, "fuel": 800, "dining": 1000},
                "goals": ["travel", "miles"]
            },
            "expected_contains": "travel"
        },
        {
            "id": 20,
            "name": "All-Rounder",
            "profile": {
                "salary": 15000,
                "spend": {"groceries": 1500, "fuel": 800, "dining": 1200, "online": 1000, "travel": 1500},
                "goals": ["cashback"]
            },
            "expected_contains": "cashback"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        print(f"🧪 TEST {test['id']}: {test['name']}")
        print(f"   Salary: {test['profile']['salary']} AED")
        print(f"   Spending: {test['profile']['spend']}")
        print(f"   Goals: {test['profile']['goals']}")
        print(f"   Expected to contain: {test['expected_contains']}")
        
        try:
            # Get recommendations
            result = advisor.recommend(test['profile'])
            recommendations = result.get('recommendations', [])
            
            if recommendations and len(recommendations) > 0:
                top_card = recommendations[0]['card_name']
                print(f"   Got: {top_card}")
                
                # Check if expected term is in the top recommendation
                if test['expected_contains'].lower() in top_card.lower():
                    print(f"   ✅ PASS - Contains '{test['expected_contains']}'")
                    passed += 1
                else:
                    # Check if it's in top 3
                    top_3_names = [r['card_name'] for r in recommendations[:3]]
                    found_in_top_3 = any(test['expected_contains'].lower() in name.lower() for name in top_3_names)
                    
                    if found_in_top_3:
                        print(f"   ⚠️  PARTIAL - Found '{test['expected_contains']}' in top 3")
                        passed += 0.5
                    else:
                        print(f"   ❌ FAIL - '{test['expected_contains']}' not in top 3")
                        failed += 1
                    
                # Show top 3 recommendations
                print(f"   Top 3: {[r['card_name'] for r in recommendations[:3]]}")
                print(f"   Scores: {[r['fit_score'] for r in recommendations[:3]]}")
            else:
                print(f"   ❌ FAIL - No recommendations returned")
                failed += 1
                
        except Exception as e:
            print(f"   ❌ ERROR - {str(e)}")
            failed += 1
            
        print()
    
    total_tests = len(test_cases)
    pass_rate = (passed / total_tests) * 100
    
    print("=== EVALUATION SUMMARY ===")
    print(f"✅ Passed: {passed}/{total_tests} ({pass_rate:.1f}%)")
    print(f"❌ Failed: {failed}/{total_tests} ({(failed/total_tests)*100:.1f}%)")
    
    if pass_rate >= 70:  # 70% pass rate
        print("🎉 EVALUATION PASSED - Recommendation logic is working well!")
    else:
        print("⚠️  EVALUATION NEEDS IMPROVEMENT - Consider adjusting recommendation logic")

if __name__ == "__main__":
    run_evaluation()