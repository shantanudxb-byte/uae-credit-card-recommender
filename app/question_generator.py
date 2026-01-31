"""
Question generator for credit card recommendations
Analyzes spending patterns and generates contextual questions
"""

def generate_questions(salary, spend, lifestyle, goals=None):
    """Generate 2-3 contextual questions based on spending patterns"""
    
    questions = []
    
    # Check for unclear spending categories (even if lifestyle partially filled)
    unclear_categories = [
        ('miscellaneous', 1000),
        ('domestic_transport', 500),
        ('online', 1000),
        ('groceries', 800),
        ('dining', 1000),
        ('fuel', 400),
        ('entertainment', 800),
        ('international_travel', 1500)
    ]
    
    # Find categories with spending but no lifestyle data
    for category, threshold in unclear_categories:
        amount = spend.get(category, 0)
        if amount >= threshold:
            # Check if this category already has lifestyle data
            lifestyle_key = _get_lifestyle_key(category)
            if not lifestyle.get(lifestyle_key):
                q = _get_category_question(category, amount)
                if q and not any(existing['id'] == q['id'] for existing in questions):
                    questions.append(q)
                    if len(questions) >= 2:
                        break
    
    return {
        "should_ask": len(questions) > 0,
        "questions": questions[:2]  # Max 2 questions, no priority ranking
    }


def _get_lifestyle_key(category):
    """Map spending category to lifestyle key"""
    mapping = {
        'online': 'online_shopping',
        'groceries': 'groceries',
        'fuel': 'fuel_stations',
        'domestic_transport': 'transport',
        'dining': 'dining',
        'entertainment': 'entertainment',
        'international_travel': 'airlines'
    }
    return mapping.get(category)


def _get_priority_options(user_goals):
    """Generate priority options based on user's selected goals"""
    
    # All available options with their mappings
    all_options = {
        'cashback': {'value': 'cashback', 'label': 'Maximum cashback', 'icon': '💰'},
        'travel': {'value': 'travel_rewards', 'label': 'Travel miles & perks', 'icon': '🎫'},
        'travel_rewards': {'value': 'travel_rewards', 'label': 'Travel miles & perks', 'icon': '🎫'},
        'no_fee': {'value': 'no_fee', 'label': 'No annual fee', 'icon': '🆓'},
        'premium': {'value': 'premium', 'label': 'Premium benefits', 'icon': '⭐'},
        'dining': {'value': 'dining', 'label': 'Dining rewards', 'icon': '🍽️'},
        'online': {'value': 'online', 'label': 'Online shopping rewards', 'icon': '🛍️'},
        'fuel': {'value': 'fuel', 'label': 'Fuel savings', 'icon': '⛽'},
        'airport_lounge': {'value': 'airport_lounge', 'label': 'Airport lounge access', 'icon': '✈️'}
    }
    
    selected_options = []
    
    # First, add options matching user's goals
    for goal in user_goals:
        goal_lower = goal.lower()
        if goal_lower in all_options:
            selected_options.append(all_options[goal_lower])
    
    # Remove duplicates by value
    seen_values = set()
    unique_options = []
    for opt in selected_options:
        if opt['value'] not in seen_values:
            seen_values.add(opt['value'])
            unique_options.append(opt)
    
    # If less than 4 options, add common defaults
    default_order = ['cashback', 'travel_rewards', 'no_fee', 'premium']
    for default_key in default_order:
        if len(unique_options) >= 4:
            break
        default_opt = all_options.get(default_key)
        if default_opt and default_opt['value'] not in seen_values:
            unique_options.append(default_opt)
            seen_values.add(default_opt['value'])
    
    return unique_options[:4]


def _get_category_question(category, amount):
    """Generate question based on spending category"""
    
    questions_map = {
        'miscellaneous': {
            'id': 'misc_breakdown',
            'text': f'You have {int(amount):,} AED/month in miscellaneous spending',
            'context': 'What does this mostly include?',
            'type': 'multi',
            'allow_custom': True,
            'options': [
                {'value': 'shopping', 'label': 'Shopping & retail', 'icon': '🛍️'},
                {'value': 'subscriptions', 'label': 'Subscriptions & memberships', 'icon': '📱'},
                {'value': 'personal_care', 'label': 'Personal care & wellness', 'icon': '💆'},
                {'value': 'gifts', 'label': 'Gifts & donations', 'icon': '🎁'},
                {'value': 'other', 'label': 'Other (specify below)', 'icon': '💳'}
            ]
        },
        'domestic_transport': {
            'id': 'transport_type',
            'text': f'You spend {int(amount):,} AED/month on local transport',
            'context': 'How do you usually commute?',
            'type': 'multi',
            'options': [
                {'value': 'careem', 'label': 'Careem', 'icon': '🚗'},
                {'value': 'uber', 'label': 'Uber', 'icon': '🚕'},
                {'value': 'metro', 'label': 'Metro & public transport', 'icon': '🚇'},
                {'value': 'taxi', 'label': 'Regular taxis', 'icon': '🚖'},
                {'value': 'parking', 'label': 'Parking & tolls', 'icon': '🅿️'}
            ]
        },
        'online': {
            'id': 'online_shopping',
            'text': f'We noticed significant online shopping expenses ({int(amount):,} AED/month)',
            'context': 'Where do you shop most frequently?',
            'type': 'multi',
            'options': [
                {'value': 'amazon', 'label': 'Amazon.ae', 'icon': '📦'},
                {'value': 'noon', 'label': 'Noon', 'icon': '🛍️'},
                {'value': 'international', 'label': 'International sites', 'icon': '🌍'},
                {'value': 'namshi', 'label': 'Namshi & fashion', 'icon': '👗'}
            ]
        },
        'international_travel': {
            'id': 'travel_frequency',
            'text': f'You spend {int(amount):,} AED/month on international travel',
            'context': 'How often do you travel internationally?',
            'type': 'single',
            'options': [
                {'value': 'monthly', 'label': 'Monthly or more', 'icon': '✈️'},
                {'value': 'quarterly', 'label': 'Every 2-3 months', 'icon': '🗓️'},
                {'value': 'occasional', 'label': 'Few times a year', 'icon': '🏖️'},
                {'value': 'rare', 'label': 'Rarely', 'icon': '🏠'}
            ]
        },
        'groceries': {
            'id': 'grocery_shopping',
            'text': f'You spend {int(amount):,} AED/month on groceries',
            'context': 'Where do you usually shop for groceries?',
            'type': 'multi',
            'options': [
                {'value': 'lulu', 'label': 'Lulu Hypermarket', 'icon': '🛒'},
                {'value': 'carrefour', 'label': 'Carrefour', 'icon': '🏪'},
                {'value': 'amazon_fresh', 'label': 'Amazon Fresh', 'icon': '📦'},
                {'value': 'spinneys', 'label': 'Spinneys & premium stores', 'icon': '🏬'}
            ]
        },
        'dining': {
            'id': 'dining_habits',
            'text': f'You spend {int(amount):,} AED/month on dining',
            'context': 'How do you usually dine?',
            'type': 'multi',
            'options': [
                {'value': 'restaurants', 'label': 'Restaurants & cafes', 'icon': '🍽️'},
                {'value': 'delivery', 'label': 'Food delivery apps', 'icon': '🚚'},
                {'value': 'talabat', 'label': 'Talabat', 'icon': '🍔'},
                {'value': 'zomato', 'label': 'Zomato', 'icon': '🍕'}
            ]
        },
        'fuel': {
            'id': 'fuel_stations',
            'text': f'You spend {int(amount):,} AED/month on fuel',
            'context': 'Which fuel stations do you use?',
            'type': 'multi',
            'options': [
                {'value': 'adnoc', 'label': 'ADNOC', 'icon': '⛽'},
                {'value': 'enoc', 'label': 'ENOC', 'icon': '⛽'},
                {'value': 'emarat', 'label': 'Emarat', 'icon': '⛽'},
                {'value': 'any', 'label': 'Any station', 'icon': '🚗'}
            ]
        },
        'entertainment': {
            'id': 'entertainment_type',
            'text': f'You spend {int(amount):,} AED/month on entertainment',
            'context': 'What type of entertainment do you prefer?',
            'type': 'multi',
            'options': [
                {'value': 'cinema', 'label': 'Movies & cinema', 'icon': '🎬'},
                {'value': 'events', 'label': 'Events & concerts', 'icon': '🎭'},
                {'value': 'shopping', 'label': 'Shopping malls', 'icon': '🛍️'},
                {'value': 'activities', 'label': 'Activities & parks', 'icon': '🎢'}
            ]
        }
    }
    
    return questions_map.get(category)


def enrich_profile_with_answers(profile, questionnaire_answers):
    """Convert questionnaire answers to lifestyle data"""
    
    if not questionnaire_answers:
        return profile
    
    lifestyle = profile.get('lifestyle', {})
    
    # Map answers to lifestyle categories
    for question_id, answer in questionnaire_answers.items():
        # Skip custom text fields (handled separately)
        if question_id.endswith('_custom'):
            continue
            
        if question_id == 'online_shopping':
            lifestyle['online_shopping'] = [
                {'service': svc, 'usage_percent': 50} 
                for svc in (answer if isinstance(answer, list) else [answer])
            ]
        elif question_id == 'grocery_shopping':
            lifestyle['groceries'] = [
                {'service': svc, 'usage_percent': 50}
                for svc in (answer if isinstance(answer, list) else [answer])
            ]
        elif question_id == 'fuel_stations':
            lifestyle['fuel_stations'] = [
                {'service': svc, 'usage_percent': 50}
                for svc in (answer if isinstance(answer, list) else [answer])
            ]
        elif question_id == 'transport_type':
            # Map transport types to lifestyle
            transport_services = answer if isinstance(answer, list) else [answer]
            lifestyle['transport'] = [
                {'service': svc, 'usage_percent': 50}
                for svc in transport_services
            ]
            profile['transport_preference'] = transport_services
        elif question_id == 'misc_breakdown':
            misc_categories = answer if isinstance(answer, list) else [answer]
            profile['misc_categories'] = misc_categories
            
            # Add custom text if provided
            custom_key = question_id + '_custom'
            if custom_key in questionnaire_answers:
                profile['misc_details'] = questionnaire_answers[custom_key]
        elif question_id == 'dining_habits':
            dining_services = answer if isinstance(answer, list) else [answer]
            lifestyle['dining'] = [
                {'service': svc, 'usage_percent': 50}
                for svc in dining_services
            ]
            profile['dining_preference'] = dining_services
        elif question_id == 'entertainment_type':
            entertainment_services = answer if isinstance(answer, list) else [answer]
            lifestyle['entertainment'] = [
                {'service': svc, 'usage_percent': 50}
                for svc in entertainment_services
            ]
        elif question_id == 'travel_frequency':
            profile['travel_frequency'] = answer
        elif question_id == 'priority':
            # Convert ranking to goals with weights
            if isinstance(answer, dict):
                sorted_priorities = sorted(answer.items(), key=lambda x: x[1])
                profile['goals'] = profile.get('goals', []) + [p[0] for p in sorted_priorities[:2]]
    
    profile['lifestyle'] = lifestyle
    return profile
