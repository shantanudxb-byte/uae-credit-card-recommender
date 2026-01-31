#!/usr/bin/env python3
"""
E2E Test for Questionnaire Flow
Tests: Question generation → User answers → Profile enrichment → Recommendations
"""
import sys
import json

def test_question_generation():
    """Test 1: Question generation for unclear categories"""
    print("\n🧪 Test 1: Question Generation")
    print("-" * 50)
    
    from app.question_generator import generate_questions
    
    # Test Case 1: High miscellaneous spending
    profile1 = {
        'salary': 15000,
        'spend': {'miscellaneous': 2000, 'groceries': 500},
        'lifestyle': {}
    }
    
    result1 = generate_questions(profile1['salary'], profile1['spend'], profile1['lifestyle'])
    
    if result1['should_ask']:
        print(f"✅ Generated {len(result1['questions'])} questions")
        print(f"   Q1: {result1['questions'][0]['id']} (type: {result1['questions'][0]['type']})")
        if len(result1['questions']) > 1:
            print(f"   Q2: {result1['questions'][1]['id']} (type: {result1['questions'][1]['type']})")
        if len(result1['questions']) > 2:
            print(f"   Q3: {result1['questions'][2]['id']} (type: {result1['questions'][2]['type']})")
        
        # Check for custom input support
        misc_q = next((q for q in result1['questions'] if q['id'] == 'misc_breakdown'), None)
        if misc_q and misc_q.get('allow_custom'):
            print("✅ Miscellaneous question supports custom input")
        else:
            print("❌ Miscellaneous question missing custom input support")
            return False
    else:
        print("❌ Should have generated questions for unclear spending")
        return False
    
    # Test Case 2: Domestic transport spending
    profile2 = {
        'salary': 12000,
        'spend': {'domestic_transport': 800, 'online': 1500},
        'lifestyle': {}
    }
    
    result2 = generate_questions(profile2['salary'], profile2['spend'], profile2['lifestyle'])
    
    if result2['should_ask']:
        has_transport = any(q['id'] == 'transport_type' for q in result2['questions'])
        has_online = any(q['id'] == 'online_shopping' for q in result2['questions'])
        
        if has_transport and has_online:
            print("✅ Generated questions for transport and online spending")
        else:
            print(f"❌ Missing expected questions (transport: {has_transport}, online: {has_online})")
            return False
    
    # Test Case 3: Skip if lifestyle already provided
    profile3 = {
        'salary': 15000,
        'spend': {'miscellaneous': 2000},
        'lifestyle': {'groceries': [{'service': 'lulu', 'usage_percent': 50}]}
    }
    
    result3 = generate_questions(profile3['salary'], profile3['spend'], profile3['lifestyle'])
    
    if not result3['should_ask']:
        print("✅ Correctly skipped questions when lifestyle provided")
    else:
        print("❌ Should skip questions when lifestyle already exists")
        return False
    
    return True


def test_profile_enrichment():
    """Test 2: Profile enrichment with questionnaire answers"""
    print("\n🧪 Test 2: Profile Enrichment")
    print("-" * 50)
    
    from app.question_generator import enrich_profile_with_answers
    
    # Test Case 1: Multi-select answers
    profile = {
        'salary': 15000,
        'spend': {'miscellaneous': 2000, 'online': 1500},
        'goals': [],
        'lifestyle': {}
    }
    
    answers = {
        'misc_breakdown': ['shopping', 'subscriptions', 'other'],
        'misc_breakdown_custom': 'Pet care, gym membership',
        'online_shopping': ['amazon', 'noon'],
        'priority': {'cashback': 1, 'travel_rewards': 2, 'no_fee': 3, 'premium': 4}
    }
    
    enriched = enrich_profile_with_answers(profile, answers)
    
    # Validate enrichment
    if 'misc_categories' in enriched:
        print(f"✅ Misc categories stored: {enriched['misc_categories']}")
    else:
        print("❌ Misc categories not stored")
        return False
    
    if 'misc_details' in enriched:
        print(f"✅ Custom misc details stored: {enriched['misc_details']}")
    else:
        print("❌ Custom misc details not stored")
        return False
    
    if 'online_shopping' in enriched['lifestyle']:
        print(f"✅ Online shopping lifestyle added: {len(enriched['lifestyle']['online_shopping'])} services")
    else:
        print("❌ Online shopping lifestyle not added")
        return False
    
    if len(enriched['goals']) >= 2:
        print(f"✅ Goals added from priority ranking: {enriched['goals']}")
    else:
        print("❌ Goals not added from priority ranking")
        return False
    
    # Test Case 2: Transport type
    profile2 = {
        'salary': 12000,
        'spend': {'domestic_transport': 800},
        'goals': [],
        'lifestyle': {}
    }
    
    answers2 = {
        'transport_type': ['careem', 'metro'],
        'priority': {'no_fee': 1, 'cashback': 2}
    }
    
    enriched2 = enrich_profile_with_answers(profile2, answers2)
    
    if 'transport_preference' in enriched2:
        print(f"✅ Transport preference stored: {enriched2['transport_preference']}")
    else:
        print("❌ Transport preference not stored")
        return False
    
    return True


def test_recommendation_with_questionnaire():
    """Test 3: Full recommendation flow with questionnaire data"""
    print("\n🧪 Test 3: Recommendations with Questionnaire Data")
    print("-" * 50)
    
    from app.agent import CardAdvisor
    from app.question_generator import enrich_profile_with_answers
    
    advisor = CardAdvisor()
    
    # Profile with questionnaire answers
    base_profile = {
        'salary': 15000,
        'spend': {
            'miscellaneous': 2000,
            'online': 1500,
            'groceries': 1000,
            'dining': 800
        },
        'goals': [],
        'lifestyle': {}
    }
    
    questionnaire_answers = {
        'misc_breakdown': ['shopping', 'subscriptions'],
        'misc_breakdown_custom': 'Gym membership, pet care',
        'online_shopping': ['amazon', 'noon'],
        'priority': {'cashback': 1, 'no_fee': 2, 'travel_rewards': 3, 'premium': 4}
    }
    
    # Enrich profile
    enriched_profile = enrich_profile_with_answers(base_profile, questionnaire_answers)
    
    # Get recommendations
    result = advisor.recommend(enriched_profile)
    
    if 'recommendations' in result and len(result['recommendations']) > 0:
        print(f"✅ Generated {len(result['recommendations'])} recommendations")
        print(f"   Top card: {result['recommendations'][0]['card_name']}")
        print(f"   Fit score: {result['recommendations'][0]['fit_score']}")
        
        # Check if goals were added from priority
        if len(enriched_profile['goals']) >= 2:
            print(f"✅ Goals from priority: {enriched_profile['goals']}")
        
        # Check if lifestyle was enriched
        if enriched_profile['lifestyle']:
            print(f"✅ Lifestyle enriched with {len(enriched_profile['lifestyle'])} categories")
        
        return True
    else:
        print("❌ No recommendations generated")
        return False


def test_api_endpoints():
    """Test 4: API endpoints"""
    print("\n🧪 Test 4: API Endpoints")
    print("-" * 50)
    
    import requests
    import subprocess
    import time
    
    # Start API server
    print("Starting API server...")
    api_process = subprocess.Popen(
        [sys.executable, '-m', 'app.api'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(4)
    
    try:
        # Test generate-questions endpoint
        profile = {
            'salary': 15000,
            'spend': {'miscellaneous': 2000, 'online': 1500},
            'lifestyle': {}
        }
        
        response = requests.post(
            'http://localhost:5001/api/generate-questions',
            json=profile,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['should_ask'] and len(data['questions']) > 0:
                print(f"✅ /api/generate-questions working ({len(data['questions'])} questions)")
            else:
                print("❌ /api/generate-questions returned no questions")
                return False
        else:
            print(f"❌ /api/generate-questions failed: {response.status_code}")
            return False
        
        # Test recommend endpoint with questionnaire answers
        full_profile = {
            'salary': 15000,
            'spend': {'miscellaneous': 2000, 'online': 1500},
            'goals': [],
            'lifestyle': {},
            'questionnaire_answers': {
                'misc_breakdown': ['shopping', 'subscriptions'],
                'online_shopping': ['amazon'],
                'priority': {'cashback': 1, 'no_fee': 2}
            }
        }
        
        response2 = requests.post(
            'http://localhost:5001/api/recommend',
            json=full_profile,
            timeout=15
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            if 'recommendations' in data2 and len(data2['recommendations']) > 0:
                print(f"✅ /api/recommend working with questionnaire data ({len(data2['recommendations'])} cards)")
                return True
            else:
                print("❌ /api/recommend returned no recommendations")
                return False
        else:
            print(f"❌ /api/recommend failed: {response2.status_code}")
            return False
            
    finally:
        api_process.terminate()
        api_process.wait(timeout=5)
        print("API server stopped")


def main():
    print("=" * 60)
    print("🚀 E2E Questionnaire Flow Tests")
    print("=" * 60)
    
    tests = [
        ("Question Generation", test_question_generation),
        ("Profile Enrichment", test_profile_enrichment),
        ("Recommendations with Questionnaire", test_recommendation_with_questionnaire),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<40}: {status}")
    
    all_passed = all(results.values())
    print("=" * 60)
    print(f"Overall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎉 E2E flow is working correctly!")
        print("\n📋 Ready to test in browser:")
        print("1. python3 -m app.api")
        print("2. open frontend/index.html")
        print("3. Fill form with miscellaneous/transport spending")
        print("4. Answer questionnaire questions")
        print("5. Get personalized recommendations")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
