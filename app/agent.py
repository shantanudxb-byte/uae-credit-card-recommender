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
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "uae_cards.json")
        with open(data_path, "r") as f:
            return json.load(f)
    
    def _load_service_mapping(self):
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "card_service_mapping.json")
        try:
            with open(data_path, "r") as f:
                return json.load(f)
        except:
            return {"co_branded_cards": {}, "partner_benefits": {}}
    
    def _load_apply_urls(self):
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "card_apply_urls.json")
        try:
            with open(data_path, "r") as f:
                data = json.load(f)
                return data.get("cards", {})
        except:
            return {}
    
    def recommend(self, user_profile: dict) -> dict:
        salary = user_profile.get("salary", 0)
        goals = user_profile.get("goals", [])
        
        goal_cards = self._get_goal_based_cards(user_profile) if goals else []
        spending_cards = self._get_spending_based_cards(user_profile)
        
        # Find cards that appear in both lists (top choices)
        goal_card_names = {card["card_name"] for card in goal_cards}
        spending_card_names = {card["card_name"] for card in spending_cards}
        top_choice_names = goal_card_names.intersection(spending_card_names)
        
        # Mark top choices and boost their scores
        top_choices = []
        for card in goal_cards + spending_cards:
            if card["card_name"] in top_choice_names:
                card["is_top_choice"] = True
                card["fit_score"] = min(card["fit_score"] + 0.1, 1.0)  # Boost score
                if card["card_name"] not in [c["card_name"] for c in top_choices]:
                    top_choices.append(card)
        
        # Remove duplicates and create unified list
        all_recommendations = goal_cards + spending_cards
        seen = set()
        unique_recommendations = []
        for card in all_recommendations:
            if card["card_name"] not in seen:
                seen.add(card["card_name"])
                unique_recommendations.append(card)
        
        # Sort by top choice status and score
        unique_recommendations.sort(key=lambda x: (x.get("is_top_choice", False), x["fit_score"]), reverse=True)
        
        # Generate follow-up questions if too many recommendations
        follow_up_questions = self._generate_follow_up_questions(unique_recommendations, user_profile)
        
        return {
            "recommendations": unique_recommendations[:6],
            "goal_based": goal_cards[:5],
            "spending_based": spending_cards[:3],
            "top_choices": top_choices,
            "has_goals": len(goals) > 0,
            "follow_up_questions": follow_up_questions
        }
    
    def _get_goal_based_cards(self, user_profile: dict) -> list:
        salary = user_profile.get("salary", 0)
        goals = user_profile.get("goals", [])
        lifestyle = user_profile.get("lifestyle", {})
        spend = user_profile.get("spend", {})
        
        # Deduplicate goals
        goals = list(set(goals))
        
        scored_cards = []
        co_branded = self.service_mapping.get("co_branded_cards", {})
        
        for card in self.cards_data:
            if card["min_salary"] > salary:
                continue
            
            best_for = card.get("best_for", [])
            matched_goals = []
            
            for goal in goals:
                if any(goal.lower() in bf.lower() for bf in best_for):
                    if goal not in matched_goals:  # Prevent duplicates
                        matched_goals.append(goal)
            
            if len(matched_goals) == 0:
                continue
            
            score = 0.5 + (len(matched_goals) * 0.15)
            
            # Enhanced scoring adjustments
            if card["annual_fee"] == 0:
                score += 0.05
            
            # Boost for international spenders
            international_travel = spend.get("international_travel", 0)
            if international_travel > 2000 and "international" in goals:
                if "Amazon" in card["name"] or card["rewards"].get("international", 0) > 2:
                    score += 0.2
            
            # Boost for domestic transport users
            domestic_transport = spend.get("domestic_transport", 0)
            if domestic_transport > 800 and any(g in goals for g in ["transport", "careem", "nol"]):
                transport_benefits = any(tag in best_for for tag in ["careem", "transport", "nol", "salik"])
                if transport_benefits:
                    score += 0.15
            
            # Boost for online shoppers
            online_spend = spend.get("online", 0)
            if online_spend > 1500 and "online" in goals:
                online_rate = card["rewards"].get("online", 0)
                if online_rate >= 5:
                    score += 0.25
                elif online_rate >= 3:
                    score += 0.15
            
            # Boost for entertainment seekers
            if "entertainment" in goals:
                if any(tag in best_for for tag in ["entertainment", "cinema", "vox", "dubai_mall"]):
                    score += 0.2
            
            # Premium card boost for high earners
            if salary >= 50000 and any(g in goals for g in ["premium", "luxury"]):
                if card["annual_fee"] > 1000 or any(tag in best_for for tag in ["premium", "elite", "signature"]):
                    score += 0.25
            
            # Strong boost for goal+spending alignment
            if "online" in goals:
                online_spend = spend.get("online", 0)
                online_rate = card["rewards"].get("online", 0)
                if online_spend > 2000 and online_rate >= 5:
                    score += 0.3
            
            if "dining" in goals:
                dining_spend = spend.get("dining", 0)
                dining_rate = card["rewards"].get("dining", 0)
                if dining_spend > 3000 and dining_rate >= 3:
                    score += 0.3
            
            # Entry-level card boost for low salary
            if salary <= 6000 and "no_fee" in goals:
                if "Liv" in card["name"] or card["min_salary"] <= 5000:
                    score += 0.15
            lifestyle_match_name = None
            for category, services in lifestyle.items():
                for service_data in services:
                    if isinstance(service_data, dict):
                        service = service_data.get("service")
                        usage_percent = service_data.get("usage_percent", 50)
                    else:
                        service = service_data
                        usage_percent = 50
                    
                    if service in co_branded and co_branded[service]["card_name"] == card["name"]:
                        score += 0.3 * (usage_percent / 100)  # Boost for lifestyle match
                        lifestyle_match_name = service.replace("_", " ").title()
            
            reasons = self._generate_goal_reasons(card, matched_goals, card["annual_fee"], lifestyle_match_name)
            value = self._estimate_value(card, user_profile)
            
            scored_cards.append({
                "card_name": card["name"],
                "bank": card["bank"],
                "annual_fee": card["annual_fee"],
                "min_salary": card["min_salary"],
                "rewards": card.get("rewards", {}),
                "best_for": card.get("best_for", []),
                "fit_score": round(min(score, 1.0), 2),
                "reasons": reasons,
                "estimated_annual_value": value,
                "recommendation_type": "goal",
                "matched_goals": matched_goals,
                "total_goals": len(goals),
                "apply_url": self.apply_urls.get(card["name"], {}).get("apply_url", "")
            })
        
        scored_cards.sort(key=lambda x: (len(x["matched_goals"]), x["fit_score"]), reverse=True)
        return scored_cards[:5]  # Return top 5 instead of 3 to show more goal matches
    
    def _get_spending_based_cards(self, user_profile: dict) -> list:
        salary = user_profile.get("salary", 0)
        
        scored_cards = []
        
        for card in self.cards_data:
            if card["min_salary"] > salary:
                continue
            
            score, matches = self._calculate_score_with_lifestyle(card, user_profile)
            reasons = self._generate_reasons_with_lifestyle(card, user_profile, matches)
            value = self._estimate_value(card, user_profile)
            
            scored_cards.append({
                "card_name": card["name"],
                "bank": card["bank"],
                "annual_fee": card["annual_fee"],
                "min_salary": card["min_salary"],
                "rewards": card.get("rewards", {}),
                "best_for": card.get("best_for", []),
                "fit_score": round(score, 2),
                "reasons": reasons,
                "estimated_annual_value": value,
                "lifestyle_matches": matches,
                "recommendation_type": "spending",
                "apply_url": self.apply_urls.get(card["name"], {}).get("apply_url", "")
            })
        
        scored_cards.sort(key=lambda x: x["fit_score"], reverse=True)
        return scored_cards[:3]
    
    def _generate_goal_reasons(self, card: dict, matched_goals: list, annual_fee: int = 0, lifestyle_match: str = None) -> list:
        reasons = []
        rewards = card.get("rewards", {})
        
        # Add lifestyle match first if present
        if lifestyle_match:
            reasons.append(f"Perfect for {lifestyle_match} users")
        
        for goal in matched_goals:
            if "travel" in goal.lower() or "miles" in goal.lower():
                travel_rate = rewards.get("travel", 0)
                reasons.append(f"Matches '{goal}' - {travel_rate}% on travel")
            elif "cashback" in goal.lower():
                reasons.append(f"Matches '{goal}' - cashback rewards")
            elif "dining" in goal.lower():
                dining_rate = rewards.get("dining", 0)
                reasons.append(f"Matches '{goal}' - {dining_rate}% on dining")
            elif "airport_lounge" in goal.lower():
                reasons.append(f"Matches '{goal}' - lounge access")
            elif "premium" in goal.lower():
                reasons.append(f"Matches '{goal}' - premium benefits")
            elif "fuel" in goal.lower():
                fuel_rate = rewards.get("fuel", 0)
                reasons.append(f"Matches '{goal}' - {fuel_rate}% on fuel")
            elif "online" in goal.lower():
                online_rate = rewards.get("online", 0)
                reasons.append(f"Matches '{goal}' - {online_rate}% online")
            elif "no_fee" in goal.lower():
                reasons.append(f"Matches '{goal}' - zero annual fee")
        
        if annual_fee > 0:
            reasons.append(f"Annual fee: {annual_fee} AED")
        
        if len(matched_goals) > 1:
            reasons.append(f"Meets {len(matched_goals)} of your goals")
        
        return reasons[:4]
    
    def _calculate_score_with_lifestyle(self, card: dict, profile: dict) -> tuple:
        score = 0.5
        matches = []
        
        lifestyle = profile.get("lifestyle", {})
        co_branded = self.service_mapping.get("co_branded_cards", {})
        partner_benefits = self.service_mapping.get("partner_benefits", {})
        spend = profile.get("spend", {})
        goals = profile.get("goals", [])
        salary = profile.get("salary", 0)
        
        for category, services in lifestyle.items():
            for service_data in services:
                if isinstance(service_data, dict):
                    service = service_data.get("service")
                    usage_percent = service_data.get("usage_percent", 50)
                else:
                    service = service_data
                    usage_percent = 50
                
                if service in co_branded:
                    if co_branded[service]["card_name"] == card["name"]:
                        boost = 0.3 * (usage_percent / 100)
                        score += boost
                        matches.append({
                            "type": "co_branded",
                            "service": service,
                            "usage": usage_percent,
                            "benefit": co_branded[service]["benefit"]
                        })
                
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
        
        # Enhanced scoring adjustments
        online_spend = spend.get("online", 0)
        international_travel = spend.get("international_travel", 0)
        domestic_transport = spend.get("domestic_transport", 0)  # ride-hailing, metro, etc
        total_spend = sum(spend.values()) or 1
        
        # Boost for high online spenders
        if online_spend > 1500:
            online_rate = card["rewards"].get("online", 0)
            if online_rate >= 5:
                score += 0.2
                matches.append({
                    "type": "high_online",
                    "service": "online_shopping",
                    "usage": int((online_spend / total_spend) * 100),
                    "benefit": f"{online_rate}% on online spending ({online_spend} AED/month)"
                })
        
        # Boost for international travelers (flights, hotels, foreign spending)
        if international_travel > 2000:
            intl_rate = card["rewards"].get("international", card["rewards"].get("travel", 0))
            if intl_rate >= 2.5 or "Amazon" in card["name"]:
                score += 0.15
                matches.append({
                    "type": "international_travel",
                    "service": "international_travel",
                    "usage": int((international_travel / total_spend) * 100),
                    "benefit": f"Enhanced rewards on international travel & foreign spending"
                })
        
        # Boost for domestic transport users (Careem, RTA, etc)
        if domestic_transport > 800:
            transport_benefits = any(tag in card.get("best_for", []) for tag in ["careem", "transport", "nol", "salik"])
            if transport_benefits:
                score += 0.1
                matches.append({
                    "type": "domestic_transport",
                    "service": "ride_hailing_transport",
                    "usage": int((domestic_transport / total_spend) * 100),
                    "benefit": f"Benefits for ride-hailing and local transport"
                })
        
        # Entry-level card boost
        if salary <= 6000 and card["annual_fee"] == 0 and card["min_salary"] <= 5000:
            if "Liv" in card["name"] or "WIO" in card["name"]:
                score += 0.1
        
        # Entertainment boost
        entertainment_spend = spend.get("dining", 0) + spend.get("online", 0)
        if entertainment_spend > 2000:
            best_for = card.get("best_for", [])
            if any(tag in best_for for tag in ["entertainment", "cinema", "vox", "dubai_mall", "namshi"]):
                score += 0.1
        
        groceries = lifestyle.get("groceries", [])
        for service_data in groceries:
            if isinstance(service_data, dict):
                service = service_data.get("service")
                usage = service_data.get("usage_percent", 0)
                if service == "amazon_fresh" and usage >= 50:
                    if card["name"] == "Amazon.ae Credit Card":
                        score += 0.2
                        matches.append({
                            "type": "high_usage",
                            "service": "amazon_fresh",
                            "usage": usage,
                            "benefit": f"You use Amazon Fresh {usage}% for groceries - 6% cashback applies!"
                        })
        
        rewards = card.get("rewards", {})
        misc_spend = spend.get("miscellaneous", 0)
        
        reward_values = list(rewards.values())
        is_general_rewards = len(set(reward_values)) == 1 and len(reward_values) >= 5
        
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
        
        for category, amount in spend.items():
            if amount > 0 and category not in ["miscellaneous", "utilities", "remittances"]:
                reward_rate = rewards.get(category, 0)
                if reward_rate > 0:
                    weight = amount / total_spend
                    score += weight * (reward_rate / 5) * 0.2
        
        if misc_spend > 0:
            misc_reward = rewards.get("miscellaneous", 0)
            if misc_reward == 0 and is_general_rewards:
                misc_reward = reward_values[0]
            if misc_reward > 0:
                weight = misc_spend / total_spend
                score += weight * (misc_reward / 5) * 0.2
        
        best_for = card.get("best_for", [])
        goal_matches = sum(1 for g in goals if any(g.lower() in bf.lower() for bf in best_for))
        score += min(goal_matches * 0.1, 0.15)
        
        if card["annual_fee"] == 0:
            score += 0.05
        
        return min(score, 1.0), matches
        
    def _generate_follow_up_questions(self, recommendations: list, profile: dict) -> list:
        """Generate follow-up questions to help users filter recommendations."""
        if len(recommendations) <= 3:
            return []
        
        questions = []
        spend = profile.get("spend", {})
        goals = profile.get("goals", [])
        
        # Question about annual fee preference
        free_cards = [r for r in recommendations if r["annual_fee"] == 0]
        paid_cards = [r for r in recommendations if r["annual_fee"] > 0]
        if len(free_cards) >= 2 and len(paid_cards) >= 2:
            questions.append({
                "question": "Do you prefer cards with no annual fee, or are you open to paying a fee for better benefits?",
                "options": ["No annual fee preferred", "Open to annual fees for better rewards"],
                "filter_type": "annual_fee"
            })
        
        # Question about spending focus
        high_spends = [(k, v) for k, v in spend.items() if v > 1000]
        if len(high_spends) >= 2:
            top_category = max(high_spends, key=lambda x: x[1])[0]
            questions.append({
                "question": f"Your highest spending is on {top_category.replace('_', ' ')} ({high_spends[0][1]} AED/month). Do you want a card optimized for this category?",
                "options": [f"Yes, optimize for {top_category.replace('_', ' ')}", "No, I want balanced rewards"],
                "filter_type": "spending_focus",
                "category": top_category
            })
        
        # Question about lifestyle preferences
        lifestyle_cards = [r for r in recommendations if any(tag in r.get("best_for", []) for tag in ["amazon", "noon", "carrefour", "lulu", "adnoc"])]
        if len(lifestyle_cards) >= 2:
            questions.append({
                "question": "Do you frequently shop at specific stores (Amazon, Noon, Carrefour, Lulu) or fuel at ADNOC?",
                "options": ["Yes, I'm loyal to specific brands", "No, I shop everywhere"],
                "filter_type": "brand_loyalty"
            })
        
        # Question about premium vs basic benefits
        premium_cards = [r for r in recommendations if r["annual_fee"] > 500]
        if len(premium_cards) >= 2:
            questions.append({
                "question": "Are premium benefits like airport lounge access, concierge, and travel insurance important to you?",
                "options": ["Yes, premium benefits matter", "No, just good rewards"],
                "filter_type": "premium_benefits"
            })
        
        return questions[:2]  # Return max 2 questions to avoid overwhelming
    
    def filter_recommendations(self, recommendations: list, filter_type: str, choice: str, **kwargs) -> list:
        """Filter recommendations based on user's follow-up answers."""
        filtered = []
        
        if filter_type == "annual_fee":
            if "no annual fee" in choice.lower():
                filtered = [r for r in recommendations if r["annual_fee"] == 0]
            else:
                filtered = [r for r in recommendations if r["annual_fee"] > 0]
        
        elif filter_type == "spending_focus":
            category = kwargs.get("category")
            if "yes" in choice.lower() and category:
                filtered = [r for r in recommendations if r.get("rewards", {}).get(category, 0) >= 2.0]
            else:
                filtered = [r for r in recommendations if len([v for v in r.get("rewards", {}).values() if v >= 2.0]) >= 3]
        
        elif filter_type == "brand_loyalty":
            if "yes" in choice.lower():
                filtered = [r for r in recommendations if any(tag in r.get("best_for", []) for tag in ["amazon", "noon", "carrefour", "lulu", "adnoc"])]
            else:
                filtered = [r for r in recommendations if not any(tag in r.get("best_for", []) for tag in ["amazon", "noon", "carrefour", "lulu", "adnoc"])]
        
        elif filter_type == "premium_benefits":
            if "yes" in choice.lower():
                filtered = [r for r in recommendations if r["annual_fee"] > 500 or any(tag in r.get("best_for", []) for tag in ["premium", "airport_lounge", "concierge"])]
            else:
                filtered = [r for r in recommendations if r["annual_fee"] <= 500]
        
        # If filter is too strict, return top 3 from original
        if len(filtered) == 0:
            return recommendations[:3]
        
        return filtered
    
    def _generate_reasons_with_lifestyle(self, card: dict, profile: dict, matches: list) -> list:
        reasons = []
        
        for match in matches[:2]:
            usage = match.get("usage", "")
            usage_text = f" ({usage}% of your spending)" if usage else ""
            if match["type"] == "co_branded":
                reasons.append(f"{match['benefit']}{usage_text}")
            elif match["type"] == "high_usage":
                reasons.append(f"{match['benefit']}")
            elif match["type"] == "general_rewards":
                reasons.append(f"{match['benefit']}")
            else:
                reasons.append(f"{match['benefit']}{usage_text}")
        
        spend = profile.get("spend", {})
        rewards = card.get("rewards", {})
        
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
        
        if card["annual_fee"] == 0 and len(reasons) < 4:
            reasons.append("Zero annual fee - no cost to hold")
        
        return reasons[:4]
    
    def _estimate_value(self, card: dict, profile: dict) -> str:
        spend = profile.get("spend", {})
        lifestyle = profile.get("lifestyle", {})
        rewards = card.get("rewards", {})
        
        reward_values = list(rewards.values())
        is_general_rewards = len(set(reward_values)) == 1 and len(reward_values) >= 5
        general_rate = reward_values[0] if is_general_rewards and reward_values else 0
        
        co_branded = self.service_mapping.get("co_branded_cards", {})
        card_co_brand_service = None
        for service, info in co_branded.items():
            if info["card_name"] == card["name"]:
                card_co_brand_service = service
                break
        
        total_rewards = 0
        excluded_spend = 0
        has_lifestyle_data = len(lifestyle) > 0
        
        for category, amount in spend.items():
            category_lifestyle = lifestyle.get(self._get_lifestyle_category_key(category), [])
            
            # Only apply exclusion logic if user provided lifestyle data for this category
            if category_lifestyle and card_co_brand_service:
                user_services = [s.get("service") if isinstance(s, dict) else s for s in category_lifestyle]
                
                # Exclude spend if card is co-branded but user doesn't use that service
                if card_co_brand_service not in user_services:
                    excluded_spend += amount
                    continue
            
            if category in rewards:
                total_rewards += amount * 12 * rewards[category] / 100
            elif is_general_rewards and category in ["miscellaneous", "utilities", "remittances"]:
                total_rewards += amount * 12 * general_rate / 100
        
        net_value = total_rewards - card["annual_fee"]
        
        exclusion_note = ""
        if excluded_spend > 0 and has_lifestyle_data:
            exclusion_note = f" (excludes {int(excluded_spend)} AED/month at non-partner merchants)"
        elif not has_lifestyle_data and card_co_brand_service:
            exclusion_note = " (assumes all spending at partner merchants)"
        
        if net_value > 0:
            return f"approx. {int(net_value)} AED net benefit annually{exclusion_note}"
        else:
            return f"approx. {int(total_rewards)} AED rewards (minus {card['annual_fee']} AED fee){exclusion_note}"
    
    def _get_lifestyle_category_key(self, spend_category: str) -> str:
        mapping = {
            "groceries": "groceries",
            "online": "online_shopping",
            "fuel": "fuel_stations",
            "entertainment": "entertainment",
            "international_travel": "airlines"
        }
        return mapping.get(spend_category, "")
    
    def chat_turn(self, user_message: str) -> str:
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
