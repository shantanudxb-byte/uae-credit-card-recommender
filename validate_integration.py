#!/usr/bin/env python3
"""
Simple frontend-backend validation test
"""
import json
import os
import sys

def test_frontend_structure():
    """Test frontend HTML structure and API endpoints"""
    print("🌐 Testing frontend structure...")
    
    frontend_file = 'frontend/index.html'
    if not os.path.exists(frontend_file):
        print(f"❌ Frontend file missing: {frontend_file}")
        return False
    
    with open(frontend_file, 'r') as f:
        content = f.read()
    
    # Check for required elements
    required_elements = [
        'id="profileForm"',
        'id="salary"',
        'name="groceries"',
        'name="international_travel"',
        'data-goal="travel"',
        'id="submitBtn"',
        'id="results"',
        'id="chatInput"'
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing HTML elements: {missing_elements}")
        return False
    
    # Check API endpoints
    if 'localhost:5001/api/recommend' in content:
        print("✅ Correct recommendation API endpoint")
    else:
        print("❌ Wrong recommendation API endpoint")
        return False
    
    if 'localhost:5001/api/chat' in content:
        print("✅ Correct chat API endpoint")
    else:
        print("❌ Wrong chat API endpoint")
        return False
    
    # Check form submission logic
    if 'addEventListener(\'submit\'' in content:
        print("✅ Form submission handler present")
    else:
        print("❌ Form submission handler missing")
        return False
    
    print("✅ Frontend structure validation passed")
    return True

def test_backend_structure():
    """Test backend API structure"""
    print("\n🔧 Testing backend structure...")
    
    try:
        # Test imports
        from app.api import app
        from app.agent import CardAdvisor
        print("✅ Backend imports successful")
        
        # Test CardAdvisor initialization
        advisor = CardAdvisor()
        print("✅ CardAdvisor initializes successfully")
        
        # Test data files
        required_files = [
            'data/uae_cards.json',
            'app/agent.py',
            'app/rag_pipeline.py',
            'app/memory.py'
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path} exists")
            else:
                print(f"❌ {file_path} missing")
                return False
        
        # Test card data structure
        with open('data/uae_cards.json', 'r') as f:
            cards_data = json.load(f)
        
        if len(cards_data) > 0:
            print(f"✅ Card database has {len(cards_data)} cards")
            
            # Check first card structure
            first_card = cards_data[0]
            required_keys = ['name', 'bank', 'annual_fee', 'min_salary', 'rewards']
            missing_keys = [key for key in required_keys if key not in first_card]
            
            if missing_keys:
                print(f"❌ Card data missing keys: {missing_keys}")
                return False
            else:
                print("✅ Card data structure valid")
        else:
            print("❌ No cards in database")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Backend structure test failed: {e}")
        return False

def test_recommendation_logic():
    """Test the core recommendation logic"""
    print("\n🎯 Testing recommendation logic...")
    
    try:
        from app.agent import CardAdvisor
        
        advisor = CardAdvisor()
        
        # Test profile
        test_profile = {
            "salary": 15000,
            "spend": {
                "groceries": 2000,
                "international_travel": 3000,
                "fuel": 500,
                "online": 1000,
                "dining": 1500
            },
            "goals": ["travel", "airport_lounge"],
            "lifestyle": {}
        }
        
        # Get recommendations
        result = advisor.recommend(test_profile)
        
        # Validate result structure
        required_keys = ['recommendations', 'goal_based', 'spending_based', 'has_goals']
        missing_keys = [key for key in required_keys if key not in result]
        
        if missing_keys:
            print(f"❌ Result missing keys: {missing_keys}")
            return False
        
        recommendations = result.get('recommendations', [])
        if len(recommendations) > 0:
            print(f"✅ Generated {len(recommendations)} recommendations")
            
            # Check first recommendation structure
            first_rec = recommendations[0]
            rec_keys = ['card_name', 'bank', 'fit_score', 'reasons', 'estimated_annual_value']
            missing_rec_keys = [key for key in rec_keys if key not in first_rec]
            
            if missing_rec_keys:
                print(f"❌ Recommendation missing keys: {missing_rec_keys}")
                return False
            
            print(f"✅ Top recommendation: {first_rec['card_name']} (Score: {first_rec['fit_score']})")
            print("✅ Recommendation logic working")
            return True
        else:
            print("❌ No recommendations generated")
            return False
            
    except Exception as e:
        print(f"❌ Recommendation logic test failed: {e}")
        return False

def test_chat_logic():
    """Test the chat functionality"""
    print("\n💬 Testing chat logic...")
    
    try:
        from app.agent import CardAdvisor
        
        advisor = CardAdvisor()
        
        # Test chat responses
        test_messages = [
            "What cards have no annual fee?",
            "Show me travel cards"
        ]
        
        for message in test_messages:
            response = advisor.chat_turn(message)
            if response and len(response) > 10:
                print(f"✅ Chat response for '{message[:30]}...': {len(response)} chars")
            else:
                print(f"❌ No/invalid chat response for '{message}'")
                return False
        
        print("✅ Chat logic working")
        return True
        
    except Exception as e:
        print(f"❌ Chat logic test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🧪 Frontend-Backend Integration Validation\n")
    
    tests = [
        ("Frontend Structure", test_frontend_structure),
        ("Backend Structure", test_backend_structure), 
        ("Recommendation Logic", test_recommendation_logic),
        ("Chat Logic", test_chat_logic)
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Print summary
    print(f"\n📊 Validation Results:")
    print("=" * 50)
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<25}: {status}")
    
    all_passed = all(results.values())
    print("=" * 50)
    print(f"Overall Result: {'✅ ALL VALIDATIONS PASSED' if all_passed else '❌ SOME VALIDATIONS FAILED'}")
    
    if all_passed:
        print("\n🎉 Frontend-backend integration is properly configured!")
        print("\n📋 To run the application:")
        print("1. Start backend: python3 -m app.api")
        print("2. Open frontend: open frontend/index.html")
        print("3. Or use: python3 serve_frontend.py")
        print("\n✨ The form submission and chat should work correctly!")
    else:
        print("\n❌ Please fix the failing validations before testing")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())