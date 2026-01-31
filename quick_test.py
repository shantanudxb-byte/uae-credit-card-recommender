#!/usr/bin/env python3
"""Quick test script to validate project structure and data."""

import json
import os

def test_project_structure():
    """Test that all required files exist."""
    print("🔍 Testing Project Structure...")
    
    required_files = [
        'data/uae_cards.json',
        'app/__init__.py',
        'app/config.py',
        'app/rag_pipeline.py',
        'app/memory.py',
        'app/agent.py',
        'app/cli.py',
        'app/api.py',
        'tests/test_agent.py',
        'frontend/index.html',
        'requirements.txt',
        '.env.example',
        'README.md'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing {len(missing)} files")
        return False
    else:
        print("\n✅ All files present")
        return True

def test_card_data():
    """Test that card data is valid."""
    print("\n🔍 Testing Card Data...")
    
    with open('data/uae_cards.json', 'r') as f:
        cards = json.load(f)
    
    print(f"  ✓ Found {len(cards)} cards")
    
    required_fields = ['name', 'bank', 'annual_fee', 'min_salary', 'rewards', 'best_for', 'notes']
    
    for i, card in enumerate(cards, 1):
        missing_fields = [field for field in required_fields if field not in card]
        if missing_fields:
            print(f"  ✗ Card {i} missing fields: {missing_fields}")
            return False
        print(f"  ✓ Card {i}: {card['name']} ({card['bank']})")
    
    print("\n✅ All card data valid")
    return True

def test_frontend():
    """Test frontend file."""
    print("\n🔍 Testing Frontend...")
    
    with open('frontend/index.html', 'r') as f:
        content = f.read()
    
    checks = [
        ('Form element', '<form id="profileForm"' in content),
        ('Salary input', 'id="salary"' in content),
        ('Spending inputs', 'name="groceries"' in content),
        ('Goals section', 'goals-section' in content),
        ('Results display', 'id="results"' in content),
        ('API call', 'fetch(' in content)
    ]
    
    for check_name, result in checks:
        if result:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name} - MISSING")
            return False
    
    print("\n✅ Frontend structure valid")
    return True

def main():
    print("="*60)
    print("UAE CREDIT CARD ADVISOR - QUICK TEST")
    print("="*60 + "\n")
    
    results = []
    results.append(test_project_structure())
    results.append(test_card_data())
    results.append(test_frontend())
    
    print("\n" + "="*60)
    if all(results):
        print("✅ ALL TESTS PASSED - Ready to install dependencies!")
        print("="*60)
        print("\nNext steps:")
        print("1. pip3 install -r requirements.txt")
        print("2. cp .env.example .env")
        print("3. Add your OPENAI_API_KEY to .env")
        print("4. python3 -m app.cli")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("="*60)
        return 1

if __name__ == '__main__':
    exit(main())
