import json

# All 5 new Emirates NBD cards with COMPLETE data
new_enbd_cards = [
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
            "education": 5.0,
            "airline_specific": "",
            "other_categories": "If min monthly spend of 5,000 AED not met, earn 1.5% Plus Points on all categories"
        },
        "rewards_conditions": {
            "min_monthly_spend_for_bonus": 5000,
            "bonus_categories": ["groceries", "utilities", "electronics", "education", "fuel"],
            "bonus_rate": "5% Plus Points",
            "standard_rate_if_not_met": "1.5% Plus Points"
        },
        "best_for": ["no_fee", "groceries", "utilities", "golf", "airport_lounge", "education"],
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
    },
    {
        "card_id": "ENBD_VISA_FLEXI",
        "name": "Emirates NBD Visa Flexi Credit Card",
        "bank": "Emirates NBD",
        "bank_code": "ENBD",
        "network": "Visa",
        "tier": "Signature/Premium",
        "card_variant": "Customizable Benefits",
        "annual_fee": 0,
        "min_salary": 0,
        "currency": "AED",
        "interest_rate": "",
        "estimated_annual_savings": 5640,
        "last_updated": "October 2025",
        "urls": {
            "primary_apply_url": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/visa-flexi",
            "card_details_url": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/visa-flexi",
            "bank_general_apply": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/apply"
        },
        "rewards": {
            "general": "",
            "groceries": 0,
            "fuel": 0,
            "dining": "Via SupperClub if selected",
            "online": 0,
            "travel": "Various travel benefits if selected",
            "airline_specific": "",
            "other_categories": "Benefits are customizable - choose your own"
        },
        "customizable_benefits": {
            "travel_benefits": {
                "choose": "3 out of 5",
                "options": [
                    {"id": "airport_lounge", "name": "Airport Lounge", "description": "Access over 1,000 lounges worldwide", "details": "2 complimentary lounge visits per year + 2 additional visits with every 20,000 AED spend in non-AED currency", "annual_cap": "6 additional visits per year", "savings": 800},
                    {"id": "airport_transfer", "name": "Airport Transfer", "description": "Complimentary Airport Transfers", "details": "2 complimentary airport transfers per year in UAE + 1 additional transfer with every 20,000 AED spend in non-AED currency", "annual_cap": "3 additional trips per year", "conditions": "Travel tickets must be purchased with the card. One-way transfer = one trip. Inter-Emirate transfers not applicable. Only valid within city limits.", "savings": 500},
                    {"id": "smart_delay", "name": "Smart Delay", "description": "Flight Delay Lounge Access", "details": "Complimentary airport lounge access for you and up to 4 registered guests in the event of a flight delay", "savings": 400},
                    {"id": "tax_claims", "name": "Tax Claims", "description": "Global Blue Membership", "details": "Scan digital membership barcode in store for automatic Tax Free Form filling. Track and manage transactions. Exclusive offers with brand and travel partners. Tax refund automatically to Visa credit card within 1-2 days.", "savings": 300},
                    {"id": "esim", "name": "eSIM", "description": "3GB eSIM Global Data Roaming Access", "details": "Access data whilst receiving OTPs from original SIM. High speed global connectivity. 3GB Global Roaming per calendar year. Valid for 21 days from first activation. Access to over 150 countries.", "savings": 140}
                ]
            },
            "lifestyle_benefits": {
                "choose": "2 out of 4",
                "options": [
                    {"id": "ten_concierge", "name": "TEN Concierge", "description": "Visa Premium Concierge", "details": "Restaurant advice and booking. Travel arrangements: booking flights, hotels, car rentals, hotel transfers, tourist advice.", "savings": 500},
                    {"id": "golf_privileges", "name": "Golf Privileges", "description": "Emirates NBD Golf Program", "details": "Complimentary golf at The Track Meydan, Address Montgomerie and 3 other courses", "savings": 1400},
                    {"id": "careem", "name": "Careem", "description": "Up to 1,200 AED in Careem credit per year", "details": "20% discount for 6 rides per quarter with a cap of 30 AED per ride", "savings": 1200},
                    {"id": "supperclub", "name": "SupperClub", "description": "12 months SupperClub Signature Premium Dining membership", "details": "Exclusive discounts at favorite venues. Buy 1, Get 1 offers, % discounts & more. Unlimited discounts for entire bookings (5 or 10 guests). New offers added every month.", "savings": 288.75}
                ]
            },
            "entertainment_benefits": {
                "choose": "1 out of 3",
                "options": [
                    {"id": "anghami", "name": "Anghami", "description": "6 Months Anghami Plus Subscription", "details": "Unlimited downloads and offline listening. Uninterrupted ad-free music on any device.", "savings": 110},
                    {"id": "vox", "name": "VOX", "description": "Discount on Theatre & 4DX", "details": "2 Theatre experiences for 200 AED. 20% discount on Theatre menu. 4DX experience with special effects at 100 AED for every 2 tickets purchased.", "savings": 1600},
                    {"id": "starzplay", "name": "Starzplay", "description": "3-month Starzplay Entertainment and Sports subscription", "details": "Hit movies, popular TV series, Arabic originals in full HD. Or watch LIVE sports: Cricket, UFC, Football, Rugby, wrestling and more.", "savings": 105}
                ]
            }
        },
        "best_for": ["customizable", "travel", "careem", "golf", "entertainment"],
        "eligibility": {
            "min_salary_aed": 0,
            "age_min": 21,
            "age_max": 65,
            "employment_type": ["salaried", "self_employed"],
            "nationality_restrictions": "UAE residents only"
        },
        "fees": {
            "annual_fee": 0,
            "annual_fee_conditions": "",
            "foreign_txn_fee": "",
            "late_payment_fee": "",
            "cash_advance_fee": ""
        },
        "benefits": {
            "airport_lounge": "Optional - choose from travel benefits",
            "travel_insurance": "",
            "concierge": "Optional - TEN Concierge if selected",
            "airport_pickup": "Optional - choose from travel benefits",
            "valet_parking": "",
            "other_benefits": [
                "Fully customizable benefit package",
                "Choose your own travel, lifestyle, and entertainment perks",
                "Flexibility to match card benefits to your lifestyle"
            ]
        },
        "restrictions": {
            "region_limitations": "Global",
            "category_caps": "Benefits have individual caps and conditions",
            "notes": "Benefits must be selected from available options. Some benefits have spend-based unlocking."
        },
        "notes": "Unique customizable credit card where you choose 3 travel benefits, 2 lifestyle benefits, and 1 entertainment benefit from a menu of options. Perfect for those who want to tailor their card to their specific needs."
    },
    {
        "card_id": "ENBD_INFINITE",
        "name": "Emirates NBD Infinite Credit Card",
        "bank": "Emirates NBD",
        "bank_code": "ENBD",
        "network": "Visa",
        "tier": "Infinite",
        "card_variant": "Premium",
        "annual_fee": 1500,
        "min_salary": 0,
        "currency": "AED",
        "interest_rate": "3.25% per month",
        "estimated_annual_savings": 11150,
        "last_updated": "July 2024",
        "urls": {
            "primary_apply_url": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/infinite",
            "card_details_url": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/infinite-credit-card",
            "bank_general_apply": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/apply"
        },
        "rewards": {
            "general": "2 Plus Points per 100 AED retail spend",
            "groceries": 2.0,
            "fuel": 2.0,
            "dining": 2.0,
            "online": 2.0,
            "travel": 2.0,
            "airline_specific": "",
            "other_categories": ""
        },
        "best_for": ["premium", "travel", "concierge", "airport_lounge", "golf", "valet_parking"],
        "eligibility": {
            "min_salary_aed": 0,
            "age_min": 21,
            "age_max": 65,
            "employment_type": ["salaried", "self_employed"],
            "nationality_restrictions": "UAE residents only"
        },
        "fees": {
            "annual_fee": 1500,
            "annual_fee_conditions": "Free for Life (Limited period offer)",
            "supplementary_card_fee": "",
            "foreign_txn_fee": "",
            "late_payment_fee": "",
            "cash_advance_fee": ""
        },
        "benefits": {
            "airport_lounge": "2 complimentary visits to 900+ airport lounges",
            "travel_insurance": "Multi-trip travel insurance included",
            "concierge": "Free concierge service",
            "airport_pickup": "Airport pick-up and drop service",
            "valet_parking": "Complimentary valet parking at malls in Abu Dhabi",
            "golf": "Complimentary golf across select golf courses in UAE",
            "courier": "Local courier service",
            "roadside_assistance": "Free roadside assistance",
            "dining_program": "Bon Appétit - Up to 30% discount on dining",
            "health_fitness": "LiveWell - Up to 50% discount on health & fitness",
            "entertainment": "GoodTimes - Up to 50% discount on entertainment & lifestyle",
            "digital_wallets": ["Apple Pay", "Google Pay", "Samsung Pay", "Garmin Pay"],
            "other_benefits": [
                "Visa Infinite privileges globally",
                "Premium lifestyle access"
            ]
        },
        "estimated_savings_breakdown": {
            "rewards_savings": {"annual_value": 3600, "assumption": "Retail spends of 15,000 AED per month"},
            "lounge_savings": {"annual_value": 2400, "assumption": "6 uses in a year"},
            "concierge_airport_savings": {"annual_value": 800, "assumption": "4 uses in a year (airport pick-up/drop)"},
            "courier_savings": {"annual_value": 400, "assumption": "4 uses in a year"},
            "golf_savings": {"annual_value": 1200, "assumption": "6 rounds of golf a year"},
            "valet_parking_savings": {"annual_value": 1200, "assumption": "4 uses in a month"},
            "roadside_assistance_savings": {"annual_value": 300, "assumption": "Service utilized once in a year"},
            "dining_savings": {"annual_value": 750, "assumption": "15% savings on annual dining spends of 5,000 AED at partner outlets"},
            "travel_insurance_savings": {"annual_value": 500, "assumption": "Annual value of multi-trip travel insurance"}
        },
        "restrictions": {
            "region_limitations": "Global",
            "category_caps": "",
            "notes": "Free for Life offer is for limited period only"
        },
        "notes": "Emirates NBD's flagship Visa Infinite card with comprehensive premium benefits including concierge, airport services, golf, valet parking, and travel insurance. Currently offered Free for Life as a limited-time promotion."
    },
    {
        "card_id": "ENBD_GO4IT_GOLD",
        "name": "Emirates NBD Go4it Gold Credit Card",
        "bank": "Emirates NBD",
        "bank_code": "ENBD",
        "network": "Visa",
        "tier": "Gold",
        "card_variant": "Nol-Integrated",
        "annual_fee": 0,
        "min_salary": 0,
        "currency": "AED",
        "interest_rate": "",
        "estimated_annual_savings": 2500,
        "last_updated": "July 2024",
        "urls": {
            "primary_apply_url": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/go4it-gold",
            "card_details_url": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/go4it-gold-credit-card",
            "bank_general_apply": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/apply"
        },
        "rewards": {
            "general": "Plus Points (Promotional rewards throughout the year)",
            "groceries": 0,
            "fuel": 0,
            "dining": "15% savings at partner outlets via Bon Appétit, LiveWell & GoodTimes",
            "online": 0,
            "travel": "10% discount on Holiday Packages",
            "airline_specific": "",
            "other_categories": ""
        },
        "unique_features": {
            "nol_integration": {
                "description": "Built-in Nol chip",
                "uses": ["RTA Parking Meters", "Metro (regular cabin)", "Bus", "Waterbus"]
            },
            "auto_topup": {
                "nol": "Nol Auto Top-up facility",
                "salik": "Salik Auto Top-up facility"
            }
        },
        "best_for": ["no_fee", "nol", "dubai_transport", "salik", "dubai_ferry"],
        "eligibility": {
            "min_salary_aed": 0,
            "age_min": 21,
            "age_max": 65,
            "employment_type": ["salaried", "self_employed"],
            "nationality_restrictions": "UAE residents only"
        },
        "fees": {
            "annual_fee": 0,
            "annual_fee_conditions": "",
            "supplementary_card_fee": "Complimentary (up to 5 cards)",
            "foreign_txn_fee": "",
            "late_payment_fee": "",
            "cash_advance_fee": ""
        },
        "benefits": {
            "airport_lounge": "",
            "travel_insurance": "",
            "concierge": "",
            "airport_pickup": "",
            "valet_parking": "",
            "dubai_ferry": "Free rides on Dubai Ferry (Economy Class)",
            "hotel_discounts": "Up to 25% discount on stays & 20% off at participating restaurants at hotels & resorts via Visa offers",
            "holiday_packages": "10% discount on Holiday Packages (Promotional offer)",
            "supplementary_cards": "Up to 5 Supplementary Cards free",
            "dining_program": "Bon Appétit - Up to 30% discount on dining",
            "health_fitness": "LiveWell - Up to 50% discount on health & fitness",
            "entertainment": "GoodTimes - Up to 50% discount on entertainment & lifestyle",
            "other_benefits": [
                "Built-in Nol chip for RTA payments",
                "Nol Auto Top-up",
                "Salik Auto Top-up"
            ]
        },
        "estimated_savings_breakdown": {
            "rewards_savings": {"annual_value": 300, "assumption": "Promotional rewards over the year"},
            "dining_lifestyle_savings": {"annual_value": 750, "assumption": "15% savings on dining spend of 5,000 AED p.a. at partner outlets"},
            "hotel_resort_savings": {"annual_value": 770, "assumption": "Up to 25% discount on stays & 20% off at participating restaurants"},
            "dubai_ferry_savings": {"annual_value": 200, "assumption": "4 rides in a year at regular price of 50 AED per ticket"},
            "holiday_package_savings": {"annual_value": 480, "assumption": "10% discount on tickets purchased worth 4,800 AED in a year"}
        },
        "restrictions": {
            "region_limitations": "UAE / Dubai focused",
            "category_caps": "",
            "notes": "Best suited for Dubai residents using public transport"
        },
        "notes": "Unique card with built-in Nol chip for seamless Dubai public transport payments. Ideal for Dubai residents who use Metro, Bus, and want auto top-up convenience for Nol and Salik."
    },
    {
        "card_id": "ENBD_MANCHESTER_UNITED",
        "name": "Emirates NBD Manchester United Credit Card",
        "bank": "Emirates NBD",
        "bank_code": "ENBD",
        "network": "Mastercard",
        "tier": "Titanium",
        "card_variant": "Co-branded Sports",
        "annual_fee": 0,
        "min_salary": 0,
        "currency": "AED",
        "interest_rate": "3.49% per month",
        "estimated_annual_savings": 2307,
        "last_updated": "May 2025",
        "urls": {
            "primary_apply_url": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/manchester-united",
            "card_details_url": "https://www.emiratesnbd.com/manutd",
            "bank_general_apply": "https://www.emiratesnbd.com/en/personal-banking/credit-cards/apply"
        },
        "rewards": {
            "general": "1 RED Point per 1 AED on all retail purchases",
            "groceries": 1.0,
            "fuel": 1.0,
            "dining": 5.0,
            "online": 1.0,
            "travel": 2.0,
            "airline_specific": "",
            "sports_stores": 10.0,
            "other_categories": ""
        },
        "rewards_structure": {
            "base_rate": "1 RED Point per 1 AED",
            "bonus_categories": [
                {"category": "International spends", "multiplier": "2X", "rate": "2 RED Points per 1 AED"},
                {"category": "Dining", "multiplier": "5X", "rate": "5 RED Points per 1 AED"},
                {"category": "Sports Good stores", "multiplier": "10X", "rate": "10 RED Points per 1 AED"}
            ]
        },
        "guaranteed_gifts": {
            "welcome_gift": {"item": "Guaranteed Home Jersey", "value": 400, "condition": "Activation and spend of 2,000 AED within 30 days of card issuance"},
            "red_box": {"item": "Guaranteed RED Box with official merchandise", "value": "Priceless", "condition": "Spend of 6,000 AED within 3 billing cycles"},
            "anniversary_gift": {"item": "Guaranteed Anniversary Gift - 'Money Can't Buy' gift", "value": "Priceless", "condition": "Spend of 250,000 AED in a calendar year"}
        },
        "priceless_rewards": {
            "description": "Offered to the Highest Spenders - Monthly, Quarterly and Yearly",
            "rewards": [
                "Guaranteed Team Signed Jersey",
                "50,000 RED Points",
                "Fully Paid Trip to watch Manchester United at Old Trafford ('Theatre of Dreams')"
            ]
        },
        "best_for": ["no_fee", "manchester_united", "sports", "dining", "airport_lounge"],
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
            "airport_lounge": "Unlimited complimentary lounge access in GCC",
            "travel_insurance": "",
            "concierge": "",
            "airport_pickup": "",
            "valet_parking": "",
            "dining_discounts": "15% savings at partner dining outlets",
            "manchester_united": [
                "Guaranteed Home Jersey",
                "Official merchandise gifts",
                "Chance to win signed memorabilia",
                "Chance to win trip to Old Trafford"
            ],
            "other_benefits": [
                "Exclusive Manchester United experiences",
                "RED Points rewards program"
            ]
        },
        "estimated_savings_breakdown": {
            "welcome_gift_value": {"annual_value": 400, "assumption": "Guaranteed Home Jersey with 2,000 AED spend in 30 days"},
            "rewards_value": {"annual_value": 307, "assumption": "Retail spends of 24,000 AED annually (General shopping 12,000 AED, international spends 2,400 AED, dining 7,200 AED, Sports Good Stores 2,400 AED)"},
            "dining_savings": {"annual_value": 1080, "assumption": "15% savings on annual dining spends of 7,200 AED at partner outlets"},
            "red_box_value": {"annual_value": "Priceless", "assumption": "Official merchandise with 6,000 AED spend in 3 months"},
            "priceless_rewards": {"annual_value": "Priceless", "assumption": "Team Signed Jersey, 50K RED Points, or Old Trafford trip for highest spenders"}
        },
        "restrictions": {
            "region_limitations": "Global, lounge access limited to GCC",
            "category_caps": "",
            "notes": "All gifts and rewards may be subject to minimum spend criteria. Match tickets offered as prizes are at discretion of Emirates NBD and subject to change."
        },
        "notes": "Ultimate card for Manchester United fans with guaranteed merchandise, 10X rewards at sports stores, and chances to win trips to Old Trafford. Free for life with unlimited GCC lounge access."
    }
]

# Save complete detailed data
with open('data/uae_cards_detailed.json', 'w') as f:
    json.dump(new_enbd_cards, f, indent=2)

print(f"✅ Created detailed cards file with {len(new_enbd_cards)} Emirates NBD cards")
print("All data fields preserved including:")
print("- Complete rewards structures")
print("- Customizable benefits (Visa Flexi)")
print("- Guaranteed gifts (Manchester United)")
print("- Estimated savings breakdowns")
print("- Eligibility criteria")
print("- All fees and restrictions")
