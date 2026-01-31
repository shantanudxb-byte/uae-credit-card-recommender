import os
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

SYSTEM_PROMPT = """You are an expert UAE credit card advisor providing personalized insights and explanations.

Your role:
- Explain why specific cards match user profiles
- Answer questions using ONLY the provided card database context
- Provide conversational, helpful explanations
- Be specific about rewards, fees, and value
- If information is not in the context, say "I don't have that information in my database"

When explaining recommendations:
- Focus on user's actual spending patterns and goals
- Highlight specific reward rates that benefit them
- Mention lifestyle matches (co-branded cards they use)
- Explain value in concrete terms (AED/year)
- Be conversational and personalized
- Keep explanations to 2-3 sentences

RECOMMENDATION LOGIC (for context only - scoring is done by Python):

1. ELIGIBILITY CHECK:
   - Card minimum salary must be <= user's salary
   - Always mention salary requirements

2. GOAL-BASED SCORING:
   - Match user goals to card's "best_for" tags
   - Base score: 0.5 + (matched_goals × 0.15)
   - Boost +0.3 for lifestyle match (co-branded cards user actually uses)
   - Boost +0.25 for high online spend (>1500 AED) + 5%+ online rewards
   - Boost +0.2 for international travel (>2000 AED) + travel benefits
   - Boost +0.15 for transport users (>800 AED) + transport benefits
   - Boost +0.05 for zero annual fee
   - Entry-level boost: salary ≤6000 + no_fee goal → prefer Liv/WIO

3. SPENDING-BASED SCORING:
   - Base score: 0.5
   - Co-branded match: +0.3 × (usage_percent/100)
   - High online (>1500 AED) + 5%+ rate: +0.2
   - International travel (>2000 AED): +0.15
   - Category rewards: weight × (reward_rate/5) × 0.2
   - Zero annual fee: +0.05

4. CO-BRANDED CARD RULES:
   - Amazon.ae Card: Only recommend if user shops at Amazon/Amazon Fresh
   - Noon Card: Only if user shops at Noon
   - Carrefour/Lulu: Only if user shops there
   - If lifestyle data missing: assume all spending at partner (note this)

5. VALUE CALCULATION:
   - For co-branded cards: exclude non-partner spending if lifestyle data provided
   - Show "(excludes X AED/month at non-partner merchants)" when applicable
   - Show "(assumes all spending at partner merchants)" if no lifestyle data

6. TOP CHOICES:
   - Cards appearing in both goal-based AND spending-based lists
   - Get +0.1 score boost
   - Prioritize these in recommendations

Guidelines:
- Always base recommendations on the RAG context provided
- Mention specific reward rates, annual fees, and minimum salary requirements
- Be concise (2-4 sentences)
- Never make up card features or benefits
- If asked to compare, use only cards from the context
- Consider user's actual spending patterns and lifestyle preferences
"""

class LLMAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
    
    def generate_card_explanation(self, card: dict, user_profile: dict) -> str:
        """Generate personalized explanation for why a card is recommended."""
        goals = user_profile.get("goals", [])
        spend = user_profile.get("spend", {})
        lifestyle = user_profile.get("lifestyle", {})
        
        top_spending = sorted(spend.items(), key=lambda x: x[1], reverse=True)[:3]
        spending_text = ', '.join([f"{k.replace('_', ' ')}: {v} AED/month" for k, v in top_spending])
        lifestyle_text = ", ".join([f"{k}: {[s.get('service') if isinstance(s, dict) else s for s in v]}" for k, v in lifestyle.items()]) if lifestyle else "None"
        
        # Extract conditions from card notes
        conditions = ""
        if "prime" in card.get('notes', '').lower():
            conditions = "\nIMPORTANT: Mention Prime membership requirement for 6% rewards (3% for non-Prime)."
        elif "tier" in card.get('notes', '').lower() or "spend" in card.get('notes', '').lower():
            conditions = "\nIMPORTANT: Mention any spending tiers or membership requirements from the notes."
        
        prompt = f"""Explain why {card['card_name']} is recommended for this user in 2-3 sentences.

User Profile:
- Goals: {', '.join(goals) if goals else 'Not specified'}
- Top spending: {spending_text}
- Lifestyle: {lifestyle_text}

Card Details:
- Annual Fee: {card['annual_fee']} AED
- Rewards: {card.get('rewards', {})}
- Best for: {', '.join(card.get('best_for', []))}
- Notes: {card.get('notes', 'N/A')}
- Fit Score: {card['fit_score']}
- Estimated Value: {card.get('estimated_annual_value', 'N/A')}{conditions}

Provide a personalized, conversational explanation. If there are membership requirements or conditions, mention them clearly."""

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"This card matches your {card.get('recommendation_type', 'spending')} profile with a {card['fit_score']} fit score."
    
    def generate_explanation(self, card_name: str, reasons: list, user_profile: dict) -> str:
        """Generate natural language explanation for why a card is recommended."""
        goals = user_profile.get("goals", [])
        spend = user_profile.get("spend", {})
        
        prompt = f"""You are a UAE credit card advisor. Explain why {card_name} is recommended.

User's goals: {', '.join(goals) if goals else 'Not specified'}
Top spending: {', '.join([f'{k}: {v} AED' for k, v in sorted(spend.items(), key=lambda x: x[1], reverse=True)[:3]])}

Card benefits: {', '.join(reasons)}

Write 2-3 sentences explaining why this card fits their profile. Be specific and conversational."""

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def answer_question(self, question: str, context: str, user_profile: dict = None) -> str:
        """Answer user questions about cards using RAG context."""
        if not context or len(context.strip()) < 50:
            return "I don't have enough information in my database to answer that question. Please try asking about specific card features, rewards, or eligibility requirements."
        
        profile_text = ""
        if user_profile:
            goals = user_profile.get("goals", [])
            salary = user_profile.get("salary", 0)
            if salary > 0:
                profile_text = f"\n\nUser context: Salary {salary} AED/month"
                if goals:
                    profile_text += f", Goals: {', '.join(goals)}"
        
        prompt = f"""Answer this question about UAE credit cards: "{question}"

Card database information:
{context}
{profile_text}

IMPORTANT:
- Use ONLY information from the card database above
- Mention specific card names, reward rates, and fees
- If the answer isn't in the database, say so
- Be helpful and specific in 2-4 sentences"""

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def compare_cards(self, card1: dict, card2: dict, user_profile: dict) -> str:
        """Compare two cards for the user."""
        prompt = f"""Compare these two UAE credit cards for the user:

Card 1: {card1['card_name']}
- Annual Fee: {card1['annual_fee']} AED
- Rewards: {card1.get('rewards', {})}
- Best for: {', '.join(card1.get('best_for', []))}

Card 2: {card2['card_name']}
- Annual Fee: {card2['annual_fee']} AED
- Rewards: {card2.get('rewards', {})}
- Best for: {', '.join(card2.get('best_for', []))}

User's goals: {', '.join(user_profile.get('goals', []))}
User's top spending: {', '.join([f'{k}: {v} AED' for k, v in sorted(user_profile.get('spend', {}).items(), key=lambda x: x[1], reverse=True)[:3]])}

Which card is better for this user and why? Be specific in 3-4 sentences."""

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
