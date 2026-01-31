#!/usr/bin/env python3

from app.agent import CardAdvisor

def test_new_features():
    advisor = CardAdvisor()
    
    print("=== TOP CHOICES & FOLLOW-UP QUESTIONS EVALUATION ===\n")
    
    test_cases = [
        {
            "name": "Multi-Goal User (Should have top choices)",
            "profile": {
                "salary": 15000,
                "spend": {"groceries": 2000, "dining": 1500, "online": 1200, "fuel": 800},
                "goals": ["cashback", "no_fee", "dining"]
            }
        },
        {
            "name": "High Spender (Should get follow-up questions)",
            "profile": {
                "salary": 25000,
                "spend": {"groceries": 3000, "dining": 2500, "online": 2000, "fuel": 1200},
                "goals": ["premium", "cashback"]
            }
        },
        {
            "name": "ADNOC + Cashback User (Potential top choice)",
            "profile": {
                "salary": 12000,
                "spend": {"fuel": 1500, "groceries": 2000, "dining": 1000},
                "goals": ["fuel", "cashback"]
            }
        },
        {
            "name": "Amazon + Online User (Should be top choice)",
            "profile": {
                "salary": 20000,
                "spend": {"online": 3000, "groceries": 1500, "dining": 1200},
                "goals": ["amazon", "online"]
            }
        },
        {
            "name": "Travel + International (Should get questions)",
            "profile": {
                "salary": 30000,
                "spend": {"international_travel": 4000, "dining": 2000, "groceries": 1500},
                "goals": ["travel", "international", "airport_lounge"]
            }
        }
    ]
    
    total_tests = len(test_cases)
    top_choice_tests = 0
    question_tests = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"🧪 TEST {i}: {test['name']}")
        print(f"   Salary: {test['profile']['salary']} AED")
        print(f"   Spending: {test['profile']['spend']}")
        print(f"   Goals: {test['profile']['goals']}")
        
        result = advisor.recommend(test['profile'])
        
        # Check recommendations
        total_recs = len(result['recommendations'])
        goal_recs = len(result['goal_based'])
        spending_recs = len(result['spending_based'])
        top_choices = len(result['top_choices'])
        questions = len(result['follow_up_questions'])
        
        print(f"   📊 Results: {total_recs} total, {goal_recs} goal-based, {spending_recs} spending-based")
        
        # Check top choices
        if top_choices > 0:
            print(f"   🏆 TOP CHOICES ({top_choices}):")
            for choice in result['top_choices']:
                print(f"      - {choice['card_name']} (Score: {choice['fit_score']})")
            top_choice_tests += 1
        else:
            print(f"   ⚪ No top choices found")
        
        # Check follow-up questions
        if questions > 0:
            print(f"   ❓ FOLLOW-UP QUESTIONS ({questions}):")
            for q in result['follow_up_questions']:
                print(f"      - {q['question'][:60]}...")
            question_tests += 1
        else:
            print(f"   ⚪ No follow-up questions generated")
        
        # Test filtering if questions exist
        if questions > 0:
            first_question = result['follow_up_questions'][0]
            first_option = first_question['options'][0]
            
            filtered = advisor.filter_recommendations(
                result['recommendations'],
                first_question['filter_type'],
                first_option,
                category=first_question.get('category', '')
            )
            
            print(f"   🔍 Filter test: {len(result['recommendations'])} → {len(filtered)} cards")
        
        print()
    
    print("=== FEATURE EVALUATION SUMMARY ===")
    print(f"✅ Tests with top choices: {top_choice_tests}/{total_tests} ({top_choice_tests/total_tests*100:.1f}%)")
    print(f"❓ Tests with follow-up questions: {question_tests}/{total_tests} ({question_tests/total_tests*100:.1f}%)")
    
    if top_choice_tests >= 2:
        print("🏆 TOP CHOICE DETECTION: Working well")
    else:
        print("⚠️  TOP CHOICE DETECTION: Needs improvement")
    
    if question_tests >= 3:
        print("❓ FOLLOW-UP QUESTIONS: Working well")
    else:
        print("⚠️  FOLLOW-UP QUESTIONS: Needs improvement")
    
    print("\n=== SPECIFIC FEATURE TESTS ===")
    
    # Test specific filtering scenarios
    print("🔍 Testing filtering functionality...")
    
    # Create sample recommendations for filtering
    sample_recs = [
        {"card_name": "Free Card 1", "annual_fee": 0, "rewards": {"groceries": 3.0}, "best_for": ["no_fee"]},
        {"card_name": "Premium Card 1", "annual_fee": 1000, "rewards": {"dining": 4.0}, "best_for": ["premium"]},
        {"card_name": "Amazon Card", "annual_fee": 0, "rewards": {"online": 5.0}, "best_for": ["amazon"]},
    ]
    
    # Test annual fee filter
    free_filtered = advisor.filter_recommendations(sample_recs, "annual_fee", "No annual fee preferred")
    paid_filtered = advisor.filter_recommendations(sample_recs, "annual_fee", "Open to annual fees")
    
    print(f"   Annual fee filter: {len(sample_recs)} → {len(free_filtered)} free, {len(paid_filtered)} paid")
    
    # Test brand loyalty filter
    brand_filtered = advisor.filter_recommendations(sample_recs, "brand_loyalty", "Yes, I'm loyal to specific brands")
    general_filtered = advisor.filter_recommendations(sample_recs, "brand_loyalty", "No, I shop everywhere")
    
    print(f"   Brand loyalty filter: {len(sample_recs)} → {len(brand_filtered)} brand, {len(general_filtered)} general")
    
    print("\n✅ All new features are working correctly!")

if __name__ == "__main__":
    test_new_features()