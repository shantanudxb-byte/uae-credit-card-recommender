from flask import Flask, request, jsonify
from flask_cors import CORS
from app.agent import CardAdvisor
from app.question_generator import generate_questions, enrich_profile_with_answers

app = Flask(__name__)
CORS(app)

advisor = CardAdvisor()

@app.route('/api/generate-questions', methods=['POST'])
def generate_questions_endpoint():
    """Generate contextual questions based on spending patterns"""
    try:
        data = request.json
        
        if not data or 'salary' not in data or 'spend' not in data:
            return jsonify({'error': 'Invalid input'}), 400
        
        # Handle goals as object or array
        goals = data.get('goals', [])
        if isinstance(goals, dict):
            goals = [k for k, v in goals.items() if v]
        
        # Map camelCase goal names to snake_case
        goal_mapping = {
            'travelMiles': 'travel',
            'noAnnualFee': 'no_fee',
            'airportLounge': 'airport_lounge',
            'diningRewards': 'dining',
            'premiumBenefits': 'premium',
            'fuelSavings': 'fuel',
            'onlineShopping': 'online'
        }
        goals = [goal_mapping.get(g, g) for g in goals]
        
        result = generate_questions(
            data.get('salary'),
            data.get('spend', {}),
            data.get('lifestyle', {}),
            goals
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """API endpoint to get card recommendations."""
    try:
        data = request.json
        
        # Validate input
        if not data or 'salary' not in data:
            return jsonify({'error': 'Invalid input'}), 400
        
        # Handle goals as object or array
        goals = data.get('goals', [])
        if isinstance(goals, dict):
            # Convert {"cashback": true, "no_fee": true} to ["cashback", "no_fee"]
            goals = [k for k, v in goals.items() if v]
        
        # Map camelCase goal names to snake_case
        goal_mapping = {
            'travelMiles': 'travel',
            'noAnnualFee': 'no_fee',
            'airportLounge': 'airport_lounge',
            'diningRewards': 'dining',
            'premiumBenefits': 'premium',
            'fuelSavings': 'fuel',
            'onlineShopping': 'online'
        }
        goals = [goal_mapping.get(g, g) for g in goals]
        
        profile = {
            'salary': data.get('salary'),
            'spend': data.get('spend', {}),
            'goals': goals,
            'lifestyle': data.get('lifestyle', {})
        }
        
        # Enrich profile with questionnaire answers if provided
        questionnaire_answers = data.get('questionnaire_answers')
        if questionnaire_answers:
            print(f"[DEBUG] Questionnaire answers received: {questionnaire_answers}")
            profile = enrich_profile_with_answers(profile, questionnaire_answers)
            print(f"[DEBUG] Enriched profile - Goals: {profile.get('goals')}, Lifestyle: {list(profile.get('lifestyle', {}).keys())}")
        
        # Get recommendations
        result = advisor.recommend(profile)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/filter', methods=['POST'])
def filter_recommendations():
    """API endpoint to filter recommendations based on follow-up answers."""
    try:
        data = request.json
        
        recommendations = data.get('recommendations', [])
        filter_type = data.get('filter_type', '')
        choice = data.get('choice', '')
        category = data.get('category', '')
        
        if not recommendations or not filter_type or not choice:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Filter recommendations
        filtered = advisor.filter_recommendations(recommendations, filter_type, choice, category=category)
        
        return jsonify({'filtered_recommendations': filtered}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for follow-up questions."""
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message required'}), 400
        
        response = advisor.chat_turn(message)
        
        return jsonify({'response': response}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    import sys
    port = 5001  # Default to 5001
    if len(sys.argv) > 1 and sys.argv[1] == '--port' and len(sys.argv) > 2:
        port = int(sys.argv[2])
    app.run(debug=True, port=port)
