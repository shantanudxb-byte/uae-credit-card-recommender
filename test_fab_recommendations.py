#!/usr/bin/env python3

import json

# Load cards data
with open('data/uae_cards.json', 'r') as f:
    cards = json.load(f)

# Create card lookup
fab_cards = {card['name']: card for card in cards if card['bank'] == 'FAB'}

print("=== FAB CARDS VALIDATION ===\n")

# Test cases based on recommendation logic
test_cases = [
    {
        'name': 'ADNOC Fuel User',
        'card_expected': 'FAB ADNOC Rewards Credit Card',
        'logic': 'fuel_station === "adnoc" && salary >= 5000',
        'expected_benefits': '15% ADNOC cashback'
    },
    {
        'name': 'Fitness Enthusiast', 
        'card_expected': 'FAB Rewards Active Credit Card',
        'logic': 'fitness_active === true && salary >= 5000',
        'expected_benefits': 'Free access to 25+ gyms'
    },
    {
        'name': 'Subscription User',
        'card_expected': 'FAB Z Card', 
        'logic': 'subscriptions.includes("netflix") || subscriptions.includes("spotify")',
        'expected_benefits': 'Free Careem Plus + noon One + 20% streaming'
    },
    {
        'name': 'Lounge Seeker (Budget)',
        'card_expected': 'FAB Rewards Indulge Card',
        'logic': 'userProfile.wants_lounge && salary >= 5000',
        'expected_benefits': 'FREE worldwide lounge access on FREE card'
    },
    {
        'name': 'Etihad Flyer',
        'card_expected': 'Etihad Guest Platinum Card',
        'logic': 'airline === "etihad" && salary >= 8000', 
        'expected_benefits': 'Entry-level Etihad card'
    },
    {
        'name': 'Fashion Shopper',
        'card_expected': 'FAB Cashback Credit Card',
        'logic': 'shopping_habits.includes("fashion")',
        'expected_benefits': '5% on fashion + 5% dining + 5% groceries'
    },
    {
        'name': 'Man City Fan',
        'card_expected': 'Manchester City Titanium Credit Card',
        'logic': 'userProfile.sports_team === "manchester_city"',
        'expected_benefits': 'Win trips to Etihad Stadium + FREE lounge'
    }
]

# Validate each test case
for test in test_cases:
    print(f"🧪 TEST: {test['name']}")
    print(f"   Logic: {test['logic']}")
    print(f"   Expected Card: {test['card_expected']}")
    
    if test['card_expected'] in fab_cards:
        card = fab_cards[test['card_expected']]
        print(f"   ✅ Card Found: {card['name']}")
        print(f"   💰 Annual Fee: {card['annual_fee']} AED")
        print(f"   💵 Min Salary: {card['min_salary']} AED")
        print(f"   🎯 Best For: {', '.join(card['best_for'])}")
        print(f"   📝 Notes: {card['notes'][:100]}...")
        
        # Validate specific logic
        if test['name'] == 'ADNOC Fuel User':
            fuel_reward = card['rewards'].get('fuel', 0)
            if fuel_reward >= 15:
                print(f"   ✅ Fuel reward: {fuel_reward}% (matches 15% expectation)")
            else:
                print(f"   ❌ Fuel reward: {fuel_reward}% (expected 15%+)")
                
        elif test['name'] == 'Lounge Seeker (Budget)':
            if card['annual_fee'] == 0 and 'airport_lounge' in card['best_for']:
                print(f"   ✅ Free card with lounge access confirmed")
            else:
                print(f"   ❌ Not free or missing lounge benefit")
                
        elif test['name'] == 'Fashion Shopper':
            fashion_reward = card['rewards'].get('fashion', 0)
            dining_reward = card['rewards'].get('dining', 0)
            if fashion_reward >= 5 and dining_reward >= 5:
                print(f"   ✅ Fashion: {fashion_reward}%, Dining: {dining_reward}%")
            else:
                print(f"   ❌ Fashion: {fashion_reward}%, Dining: {dining_reward}% (expected 5%+)")
                
    else:
        print(f"   ❌ Card NOT FOUND in dataset!")
        print(f"   Available FAB cards: {list(fab_cards.keys())}")
    
    print()

# Check for missing cards referenced in logic
print("=== MISSING CARDS CHECK ===")
referenced_cards = [
    'FAB_ADNOC_REWARDS', 'FAB_BLUE_AL_FUTTAIM', 'FAB_GEMS_WORLD',
    'FAB_REWARDS_ACTIVE', 'FAB_Z_CARD', 'FAB_REWARDS_INDULGE', 
    'FAB_ETIHAD_PLATINUM', 'FAB_CASHBACK_UPDATED', 'FAB_MANCHESTER_CITY',
    'FAB_SHARE_SIGNATURE'
]

card_name_mapping = {
    'FAB_ADNOC_REWARDS': 'FAB ADNOC Rewards Credit Card',
    'FAB_BLUE_AL_FUTTAIM': 'BLUE Al-Futtaim Platinum', 
    'FAB_GEMS_WORLD': 'GEMS World Credit Card',
    'FAB_REWARDS_ACTIVE': 'FAB Rewards Active Credit Card',
    'FAB_Z_CARD': 'FAB Z Card',
    'FAB_REWARDS_INDULGE': 'FAB Rewards Indulge Card',
    'FAB_ETIHAD_PLATINUM': 'Etihad Guest Platinum Card',
    'FAB_CASHBACK_UPDATED': 'FAB Cashback Credit Card', 
    'FAB_MANCHESTER_CITY': 'Manchester City Titanium Credit Card',
    'FAB_SHARE_SIGNATURE': 'FAB SHARE Signature'
}

for card_id in referenced_cards:
    expected_name = card_name_mapping.get(card_id, card_id)
    if expected_name in fab_cards:
        print(f"✅ {card_id} -> {expected_name}")
    else:
        print(f"❌ {card_id} -> {expected_name} (NOT FOUND)")

print(f"\n📊 Total FAB cards in dataset: {len(fab_cards)}")
print("FAB cards available:", list(fab_cards.keys()))