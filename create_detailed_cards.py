import json

# Load existing cards
with open('data/uae_cards.json', 'r') as f:
    existing_cards = json.load(f)

# New detailed Emirates NBD cards
new_cards_data = [
    {
        "card_id": "ENBD_DUO",
        "name": "Emirates NBD Duo Credit Card",
        "bank": "Emirates NBD",
        "bank_code": "ENBD",
        "network": ["Diners Club", "Mastercard"],
        "tier": "Platinum",
        "card_variant": "Dual Card Package",
        "annual_fee": 0,
        "min_salary": 0,
        "currency": "AED",
        "interest_rate": "3.49% per month",
        "estimated_annual_savings": 8156,
        "last_updated": "March 2025",
        "urls": {
            "primary_apply_url": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/duo",
            "card_details_url": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/duo",
            "bank_general_apply": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/apply"
        },
        "rewards": {
            "general": "0.5% Plus Points on all spends",
            "groceries": 5.0,
            "fuel": 5.0,
            "dining": 0.5,
            "online": 0.5,
            "travel": 0.5,
            "utilities": 5.0,
            "electronics": 5.0,
            "education": 5.0
        },
        "rewards_conditions": {
            "min_monthly_spend_for_bonus": 5000,
            "bonus_categories": ["groceries", "utilities", "electronics", "education", "fuel"],
            "bonus_rate": "5% Plus Points",
            "standard_rate_if_not_met": "1.5% Plus Points"
        },
        "best_for": ["no_fee", "groceries", "utilities", "golf", "airport_lounge"],
        "eligibility": {
            "min_salary_aed": 0,
            "age_min": 21,
            "age_max": 65,
            "employment_type": ["salaried", "self_employed"],
            "nationality_restrictions": "UAE residents only"
        },
        "fees": {
            "annual_fee": 0,
            "annual_fee_conditions": "Free for Life",
            "supplementary_card_fee": "",
            "foreign_txn_fee": "",
            "late_payment_fee": "",
            "cash_advance_fee": ""
        },
        "benefits": {
            "airport_lounge": "Unlimited access to 1,500+ airport lounges worldwide",
            "travel_insurance": "",
            "concierge": "",
            "airport_pickup": "",
            "valet_parking": "",
            "cinema": "Buy 1 Get 1 free on cinema tickets at Royal Cinemas",
            "golf": "Complimentary access to top golf courses across UAE",
            "dining_program": "Bon Appétit - Up to 30% discount on dining",
            "health_fitness": "LiveWell - Up to 50% discount on health & fitness",
            "entertainment": "GoodTimes - Up to 50% discount on entertainment & lifestyle",
            "other_benefits": [
                "Two cards in one package (Diners Club + Mastercard Platinum)",
                "Diners Club acceptance at exclusive merchants",
                "Mastercard Platinum benefits"
            ]
        },
        "estimated_savings_breakdown": {
            "rewards_savings": {"annual_value": 3000, "assumption": "Monthly spends: 2,000 AED grocery, 700 AED utilities, 500 AED fuel, 500 AED electronics, 1,220 AED education, 800 AED others"},
            "lounge_savings": {"annual_value": 800, "assumption": "4 usages per year for Primary and Supplementary Cards"},
            "cinema_savings": {"annual_value": 756, "assumption": "1 usage per month for two people"},
            "golf_savings": {"annual_value": 3600, "assumption": "6 rounds of golf per year"}
        },
        "restrictions": {
            "region_limitations": "Global",
            "category_caps": "5% categories require minimum 5,000 AED monthly spend",
            "notes": "Dual card package - both cards linked to same account"
        },
        "notes": "Unique dual-card offering combining Diners Club exclusivity with Mastercard Platinum acceptance. Excellent for high spenders on groceries, utilities, and education with unlimited lounge access."
    }
]

# Save to detailed file
with open('data/uae_cards_detailed.json', 'w') as f:
    json.dump(new_cards_data, f, indent=2)

print("Created detailed cards file with 1 card")
