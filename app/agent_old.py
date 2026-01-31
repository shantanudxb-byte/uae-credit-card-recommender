import json
import os
from app.rag_pipeline import get_cards_retriever
from app.memory import get_conversation_memory

class CardAdvisor:
    def __init__(self):
        self.retriever = get_cards_retriever()
        self.memory = get_conversation_memory()
        self.cards_data = self._load_cards()
        self.service_mapping = self._load_service_mapping()
        self.apply_urls = self._load_apply_urls()
    
    def _load_cards(self):
        """Load card data from JSON."""
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "uae_cards.json")
        with open(data_path, "r") as f:
            return json.load(f)
    
    def _load_service_mapping(self):
        """Load service-to-card mapping."""
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "card_service_mapping.json")
        try:
            with open(data_path, "r") as f:
                return json.load(f)
        except:
            return {"co_branded_cards": {}, "partner_benefits": {}}
    
    def _load_apply_urls(self):
        """Load card application URLs."""
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "card_apply_urls.json")
        try:
            with open(data_path, "r") as f:
                data = json.load(f)
                return data.get("cards", {})
        except:
            return {}
    
    def recommend(self, user_profile: dict) -> dict:
        """Generate recommendations split by goals and spending."""
        
        salary = user_profile.get("salary", 0)
        goals = user_profile.get("goals", [])
        
        # Get goal-based recommendations
        goal_cards = self._get_goal_based_cards(user_profile) if goals else []
        
        # Get premium goal cards (cards with fees that match premium goals)
        premium_goal_cards = self._get_premium_goal_cards(user_profile) if goals else []
        
        # Get spending-based recommendations
        spending_cards = self._get_spending_based_cards(user_profile)
        
        # Combine for backward compatibility
        all_recommendations = goal_cards + premium_goal_cards + spending_cards
        seen = set()
        unique_recommendations = []
        for card in all_recommendations:
            if card["card_name"] not in seen:
                seen.add(card["card_name"])
                unique_recommendations.append(card)
        
        return {
            "recommendations": unique_recommendations[:6],
            "goal_based": goal_cards[:3],
            "premium_goal_based": premium_goal_cards[:2],
            "spending_based": spending_cards[:3],
            "has_goals": len(goals) > 0
        }
    
    def _get_premium_goal_cards(self, user_profile: dict) -> list:
        """Get premium cards with fees that match goals like airport_lounge."""
        salary = user_profile.get("salary", 0)
        goals = user_profile.get("goals", [])
        
        # Premium goals that typically require fees
        premium_goals = ['airport_lounge', 'premium', 'travel']
        has_premium_goals = any(g in goals for g in premium_goals)
        
        if not has_premium_goals:
            return []
        
        scored_cards = []
        
        for card in self.cards_data:
            if card["min_salary"] > salary or card["annual_fee"] == 0:
                continue
            
            best_for = card.get("best_for", [])
            matched_goals = []
            
            for goal in goals:
                if goal in premium_goals and any(goal.lower() in bf.lower() for bf in best_for):
                    matched_goals.append(goal)
            
            if len(matched_goals) == 0:
                continue
            
            score = 0.5 + (len(matched_goals) * 0.15)
            reasons = self._generate_goal_reasons(card, matched_goals, card["annual_fee"])
            value = self._estimate_value(card, user_profile)
            
            scored_cards.append({
                "card_name": card["name"],
                "bank": card["bank"],
                "annual_fee": card["annual_fee"],
                "min_salary": card["min_salary"],
                "fit_score": round(min(score, 1.0), 2),
                "reasons": reasons,
                "estimated_annual_value": value,
                "recommendation_type": "premium_goal",
                "matched_goals": matched_goals,
                "total_goals": len(goals),
                "apply_url": self.apply_urls.get(card["name"], {}).get("apply_url", "")
            })
        
        scored_cards.sort(key=lambda x: (len(x["matched_goals"]), x["fit_score"]), reverse=True)
        return scored_cards[:2]
    
    def _get_goal_based_cards(self, user_profile: dict) -> list:
        """Get cards that match ANY user goals (not all required)."""
        salary = user_profile.get("salary", 0)
        goals = user_profile.get("goals", [])
        
        scored_cards = []
        has_no_fee_goal = "no_fee" in goals or "no annual fee" in [g.lower() for g in goals]
        
        for card in self.cards_data:
            if card["min_salary"] > salary:
                continue
            
            # Check which goals this card matches
            best_for = card.get("best_for", [])
            matched_goals = []
            
            for goal in goals:
                if any(goal.lower() in bf.lower() for bf in best_for):
                    matched_goals.append(goal)
            
            # Skip if no goals match
            if len(matched_goals) == 0:
                continue
            
            # If card has fee but user wants no_fee, only skip if no_fee is the ONLY matched goal
            if card["annual_fee"] > 0 and has_no_fee_goal:
                # Remove no_fee from matched goals since card has fee
                matched_goals = [g for g in matched_goals if g not in ["no_fee", "no annual fee"]]
                # If no other goals match, skip this card
                if len(matched_goals) == 0:
                    continue
            
            # Score based on number of goals matched
            score = 0.5 + (len(matched_goals) * 0.15)
            if card["annual_fee"] == 0:
                score += 0.05
            
            reasons = self._generate_goal_reasons(card, matched_goals, card["annual_fee"])
            value = self._estimate_value(card, user_profile)
            
            scored_cards.append({
                "card_name": card["name"],
                "bank": card["bank"],
                "annual_fee": card["annual_fee"],
                "min_salary": card["min_salary"],
                "fit_score": round(min(score, 1.0), 2),
                "reasons": reasons,
                "estimated_annual_value": value,
                "recommendation_type": "goal",
                "matched_goals": matched_goals,
                "total_goals": len(goals),
                "apply_url": self.apply_urls.get(card["name"], {}).get("apply_url", "")
            })
        
        scored_cards.sort(key=lambda x: (len(x["matched_goals"]), x["fit_score"]), reverse=True)
        return scored_cards[:3]
    
    def _get_spending_based_cards(self, user_profile: dict) -> list:
        """Get cards that match user spending patterns."""
        salary = user_profile.get("salary", 0)
        goals = user_profile.get("goals", [])
        
        scored_cards = []
        
        for card in self.cards_data:
            if card["min_salary"] > salary:
                continue
            
            if ("no_fee" in goals) and card["annual_fee"] > 0:
                continue
            
            score, matches = self._calculate_score_with_lifestyle(card, user_profile)
            reasons = self._generate_reasons_with_lifestyle(card, user_profile, matches)
            value = self._estimate_value(card, user_profile)
            
            scored_cards.append({
                "card_name": card["name"],
                "bank": card["bank"],
                "annual_fee": card["annual_fee"],
                "min_salary": card["min_salary"],
                "fit_score": round(score, 2),
                "reasons": reasons,
                "estimated_annual_value": value,
                "lifestyle_matches": matches,
                "recommendation_type": "spending",
                "apply_url": self.apply_urls.get(card["name"], {}).get("apply_url", "")
            })
        
        scored_cards.sort(key=lambda x: x["fit_score"], reverse=True)
        return scored_cards[:3]
    
    def _generate_goal_reasons(self, card: dict, matched_goals: list, annual_fee: int = 0) -> list:
        """Generate reasons focused on matched goals only."""
        reasons = []
        best_for = card.get("best_for", [])
        rewards = card.get("rewards", {})
        
        # Add reason for each matched goal
        for goal in matched_goals:
            if "travel" in goal.lower() or "miles" in goal.lower():
                travel_rate = rewards.get("travel", 0)
                reasons.append(f"✓ Matches your '{goal}' goal - {travel_rate}% on travel bookings")
            elif "cashback" in goal.lower():
                reasons.append(f"✓ Matches your '{goal}' goal - cashback rewards across categories")
            elif "dining" in goal.lower():
                dining_rate = rewards.get("dining", 0)
                reasons.append(f"✓ Matches your '{goal}' goal - {dining_rate}% on restaurants")
            elif "airport_lounge" in goal.lower():
                reasons.append(f"✓ Matches your '{goal}' goal - complimentary lounge access")
            elif "premium" in goal.lower():
                reasons.append(f"✓ Matches your '{goal}' goal - premium benefits & concierge")
            elif "fuel" in goal.lower():
                fuel_rate = rewards.get("fuel", 0)
                reasons.append(f"✓ Matches your '{goal}' goal - {fuel_rate}% on fuel")
            elif "online" in goal.lower():
                online_rate = rewards.get("online", 0)
                reasons.append(f"✓ Matches your '{goal}' goal - {online_rate}% on online shopping")
            elif "no_fee" in goal.lower():
                reasons.append(f"✓ Matches your '{goal}' goal - zero annual fee")
        
        # Add fee note if card has fee but matches other goals
        if annual_fee > 0 and len(matched_goals) > 0:
            reasons.append(f"Note: {annual_fee} AED annual fee, but offers premium benefits")
        
        # Add summary
        if len(matched_goals) > 1:
            reasons.append(f"Meets {len(matched_goals)} of your goals in one card")
        
        return reasons[:4]
    
    def _calculate_score_with_lifestyle(self, card: dict, profile: dict) -> tuple:
        """Calculate score including lifestyle service matches with usage percentages."""
        score = 0.5
        matches = []
        
        lifestyle = profile.get("lifestyle", {})
        co_branded = self.service_mapping.get("co_branded_cards", {})
        partner_benefits = self.service_mapping.get("partner_benefits", {})
        
        # Check co-branded matches with usage weighting
        for category, services in lifestyle.items():
            for service_data in services:
                # Handle both old format (string) and new format (dict with usage)
                if isinstance(service_data, dict):
                    service = service_data.get("service")
                    usage_percent = service_data.get("usage_percent", 50)
                else:
                    service = service_data
                    usage_percent = 50
                
                # Co-branded card match
                if service in co_branded:
                    if co_branded[service]["card_name"] == card["name"]:
                        # Higher usage = higher score boost
                        boost = 0.3 * (usage_percent / 100)
                        score += boost
                        matches.append({
                            "type": "co_branded",
                            "service": service,
                            "usage": usage_percent,
                            "benefit": co_branded[service]["benefit"]
                        })
                
                # Partner benefits
                if service in partner_benefits:
                    if card["name"] in partner_benefits[service]:
                        boost = 0.15 * (usage_percent / 100)
                        score += boost
                        matches.append({
                            "type": "partner",
                            "service": service,
                            "usage": usage_percent,
                            "benefit": f"Special benefits at {service}"
                        })
        
        # Check if Amazon is used for groceries (high usage)
        groceries = lifestyle.get("groceries", [])
        for service_data in groceries:
            if isinstance(service_data, dict):
                service = service_data.get("service")
                usage = service_data.get("usage_percent", 0)
                if service == "amazon_fresh" and usage >= 50:
                    # Boost Amazon.ae card for high Amazon Fresh usage
                    if card["name"] == "Amazon.ae Credit Card":
                        score += 0.2
                        matches.append({
                            "type": "high_usage",
                            "service": "amazon_fresh",
                            "usage": usage,
                            "benefit": f"You use Amazon Fresh {usage}% for groceries - 5% cashback applies!"
                        })
        
        # Spending-based scoring with miscellaneous handling
        spend = profile.get("spend", {})
        rewards = card.get("rewards", {})
        total_spend = sum(spend.values()) or 1
        misc_spend = spend.get("miscellaneous", 0)
        
        # Check if card has uniform rewards across categories (general rewards card)
        reward_values = list(rewards.values())
        is_general_rewards = len(set(reward_values)) == 1 and len(reward_values) >= 5
        
        # If miscellaneous is high (>30% of total) and card offers general rewards, boost score
        if misc_spend > 0 and misc_spend / total_spend > 0.3 and is_general_rewards:
            general_rate = reward_values[0] if reward_values else 0
            if general_rate >= 2.0:
                score += 0.25
                matches.append({
                    "type": "general_rewards",
                    "service": "miscellaneous",
                    "usage": int((misc_spend / total_spend) * 100),
                    "benefit": f"Flat {general_rate}% on all spending including miscellaneous ({int(misc_spend)} AED/month)"
                })
        
        # Category-specific scoring (skip miscellaneous and utilities/bills)
        for category, amount in spend.items():
            if amount > 0 and category not in ["miscellaneous", "utilities", "remittances"]:
                reward_rate = rewards.get(category, 0)
                if reward_rate > 0:
                    weight = amount / total_spend
                    score += weight * (reward_rate / 5) * 0.2
        
        # For miscellaneous, use general reward rate if available
        if misc_spend > 0:
            misc_reward = rewards.get("miscellaneous", 0)
            if misc_reward == 0 and is_general_rewards:
                misc_reward = reward_values[0]
            if misc_reward > 0:
                weight = misc_spend / total_spend
                score += weight * (misc_reward / 5) * 0.2
        
        # Goal matching
        goals = profile.get("goals", [])
        best_for = card.get("best_for", [])
        goal_matches = sum(1 for g in goals if any(g.lower() in bf.lower() for bf in best_for))
        score += min(goal_matches * 0.1, 0.15)
        
        # No fee bonus
        if card["annual_fee"] == 0:
            score += 0.05
        
        return min(score, 1.0), matches
    
    def _generate_reasons_with_lifestyle(self, card: dict, profile: dict, matches: list) -> list:
        """Generate reasons including lifestyle matches with usage info."""
        reasons = []
        
        # Add lifestyle matches first (most important)
        for match in matches[:2]:
            usage = match.get("usage", "")
            usage_text = f" ({usage}% of your spending)" if usage else ""
            if match["type"] == "co_branded":
                reasons.append(f"✓ {match['benefit']}{usage_text}")
            elif match["type"] == "high_usage":
                reasons.append(f"✓ {match['benefit']}")
            elif match["type"] == "general_rewards":
                reasons.append(f"✓ {match['benefit']}")
            else:
                reasons.append(f"✓ {match['benefit']}{usage_text}")
        
        # Add spending-based reasons
        spend = profile.get("spend", {})
        rewards = card.get("rewards", {})
        
        # Check if general rewards card
        reward_values = list(rewards.values())
        is_general_rewards = len(set(reward_values)) == 1 and len(reward_values) >= 5
        
        for category, amount in sorted(spend.items(), key=lambda x: x[1], reverse=True):
            if len(reasons) >= 4:
                break
            if category in rewards and rewards[category] > 0 and amount > 0:
                annual_reward = amount * 12 * rewards[category] / 100
                reasons.append(f"Earns {rewards[category]}% on {category} = {int(annual_reward)} AED/year")
            elif is_general_rewards and category in ["miscellaneous", "utilities", "remittances"] and amount > 0:
                general_rate = reward_values[0]
                annual_reward = amount * 12 * general_rate / 100
                reasons.append(f"Earns {general_rate}% on {category} = {int(annual_reward)} AED/year")
        
        # Annual fee info
        if card["annual_fee"] == 0 and len(reasons) < 4:
            reasons.append("Zero annual fee - no cost to hold")
        
        return reasons[:4]
    
    def _estimate_value(self, card: dict, profile: dict) -> str:
        """Estimate annual value."""
        spend = profile.get("spend", {})
        rewards = card.get("rewards", {})
        
        # Check if general rewards card
        reward_values = list(rewards.values())
        is_general_rewards = len(set(reward_values)) == 1 and len(reward_values) >= 5
        general_rate = reward_values[0] if is_general_rewards and reward_values else 0
        
        total_rewards = 0
        for category, amount in spend.items():
            if category in rewards:
                total_rewards += amount * 12 * rewards[category] / 100
            elif is_general_rewards and category in ["miscellaneous", "utilities", "remittances"]:
                # Apply general rate to categories not explicitly listed
                total_rewards += amount * 12 * general_rate / 100
        
        net_value = total_rewards - card["annual_fee"]
        
        if net_value > 0:
            return f"approx. {int(net_value)} AED net benefit annually"
        else:
            return f"approx. {int(total_rewards)} AED rewards (minus {card['annual_fee']} AED fee)"
    
    def chat_turn(self, user_message: str) -> str:
        """Handle follow-up questions."""
        docs = self.retriever.get_relevant_documents(user_message)
        context = "\n".join([doc.page_content[:500] for doc in docs[:3]])
        
        message_lower = user_message.lower()
        
        if "no fee" in message_lower:
            no_fee_cards = [c for c in self.cards_data if c["annual_fee"] == 0]
            response = "Cards with NO annual fee:\n"
            for card in no_fee_cards:
                response += f"• {card['name']} ({card['bank']}) - Min salary: {card['min_salary']} AED\n"
            return response
        
        if "travel" in message_lower or "miles" in message_lower:
            travel_cards = [c for c in self.cards_data if "travel" in c.get("best_for", [])]
            response = "Best cards for TRAVEL/MILES:\n"
            for card in travel_cards:
                response += f"• {card['name']} - {card['rewards'].get('travel', 0)}% on travel\n"
            return response
        
        return f"Based on your question:\n\n{context[:800]}"
