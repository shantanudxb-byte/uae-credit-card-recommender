# Fine-Tuning Guide for Credit Card Recommendations

## Location: app/agent.py

### 1. MAIN RECOMMENDATION PROMPT (Line 29-56)
**What it does:** Controls how the LLM analyzes and ranks cards

**Current prompt issues you might see:**
- Not prioritizing spending categories correctly
- Ignoring annual fees
- Wrong fit scores
- Generic reasons

**How to fix:**

```python
# REPLACE the prompt template (line 29) with more specific instructions:

prompt = ChatPromptTemplate.from_template("""
You are a UAE credit card expert. Analyze cards and recommend TOP 3 based on user profile.

User Profile:
- Salary: {salary} AED/month
- Monthly Spending: {spending}
- Goals: {goals}

Available Cards:
{cards}

SCORING RULES (strictly follow):
1. ELIMINATE cards where min_salary > user salary
2. CALCULATE reward value: (spending_amount × reward_rate) for each category
3. SUBTRACT annual_fee from total rewards
4. BONUS points if card matches user goals
5. Fit score = (total_value / max_possible_value)

Return TOP 3 as JSON:
{{
  "recommendations": [
    {{
      "card_name": "exact card name from data",
      "fit_score": 0.0-1.0,
      "reasons": ["specific reason with numbers", "another specific reason"],
      "estimated_annual_value": "X AED in rewards/cashback annually"
    }}
  ]
}}

IMPORTANT:
- Use ACTUAL reward rates from card data
- Calculate REAL annual value based on spending
- Prioritize cards with highest net benefit (rewards - fees)
- Give specific numbers in reasons (e.g., "Earn 3% on 2000 AED groceries = 720 AED/year")
""")
```

### 2. QUERY BUILDER (Line 127-147)
**What it does:** Builds search query to retrieve relevant cards from vector DB

**Current issues:**
- May retrieve irrelevant cards
- Not weighting spending categories properly

**How to fix:**

```python
def _build_query(self, profile: dict) -> str:
    """Build search query from user profile."""
    parts = []
    
    # Add ALL spending categories with amounts (not just top 2)
    spend = profile.get("spend", {})
    for category, amount in spend.items():
        if amount > 0:
            parts.append(f"{category} spending {amount} AED")
    
    # Add goals with emphasis
    goals = profile.get("goals", [])
    if goals:
        parts.append(f"MUST HAVE: {', '.join(goals)}")
    
    # More granular salary context
    salary = profile.get("salary", 0)
    if salary < 8000:
        parts.append("REQUIRED: zero annual fee, low minimum salary")
    elif salary < 15000:
        parts.append("prefer low annual fee under 500 AED")
    elif salary < 30000:
        parts.append("can afford moderate annual fees")
    else:
        parts.append("premium cards with high rewards acceptable")
    
    return ". ".join(parts)
```

### 3. LLM TEMPERATURE (Line 13)
**What it does:** Controls randomness in LLM responses

```python
# Current: temperature=0.3 (more consistent but may miss nuances)

# For MORE CREATIVE recommendations:
temperature=0.7

# For MORE CONSISTENT recommendations:
temperature=0.1

# RECOMMENDED for financial advice:
temperature=0.2
```

### 4. RETRIEVER SETTINGS
**Location:** app/rag_pipeline.py (Line 67)

```python
# Current: retrieves top 5 cards
return vectorstore.as_retriever(search_kwargs={"k": 5})

# To retrieve MORE cards (better coverage):
return vectorstore.as_retriever(search_kwargs={"k": 7})

# To retrieve FEWER cards (faster, more focused):
return vectorstore.as_retriever(search_kwargs={"k": 3})
```

### 5. ADD CUSTOM SCORING LOGIC
**Location:** app/agent.py (add new method)

```python
def _calculate_card_value(self, card_data: dict, user_profile: dict) -> float:
    """Calculate actual monetary value of card for user."""
    spend = user_profile.get("spend", {})
    
    # Calculate rewards
    total_rewards = 0
    for category, amount in spend.items():
        reward_rate = card_data.get("rewards", {}).get(category, 0)
        total_rewards += (amount * 12 * reward_rate / 100)  # Annual
    
    # Subtract annual fee
    annual_fee = card_data.get("annual_fee", 0)
    net_value = total_rewards - annual_fee
    
    return net_value

# Then use this in recommend() method to pre-filter or re-rank cards
```

## QUICK FIXES FOR COMMON ISSUES:

### Issue: "Cards don't match my spending"
**Fix:** Modify prompt to emphasize spending categories more
Add: "PRIORITY: Match highest spending categories first"

### Issue: "Recommending cards I can't afford"
**Fix:** Add salary filter before LLM
```python
# In recommend() method, after retrieving docs:
eligible_docs = [doc for doc in docs 
                 if doc.metadata.get("min_salary", 0) <= user_profile["salary"]]
```

### Issue: "Fit scores don't make sense"
**Fix:** Add explicit scoring formula in prompt
```python
"Fit score formula: 
- Start with 0.5
- Add 0.1 for each matching goal (max +0.3)
- Add 0.2 if highest spending category matches best reward
- Subtract 0.1 if annual fee > 1000 AED
- Result must be between 0.0 and 1.0"
```

### Issue: "Reasons are too generic"
**Fix:** Require specific numbers in prompt
```python
"Each reason MUST include:
- Specific reward rate (e.g., '3% on travel')
- Actual spending amount (e.g., 'your 2000 AED monthly groceries')
- Calculated value (e.g., '= 720 AED annually')"
```

## TESTING YOUR CHANGES:

1. Edit app/agent.py
2. Restart the API: `python3 -m app.api`
3. Test with frontend or CLI
4. Check if recommendations improve

## RECOMMENDED TUNING ORDER:

1. Start with prompt (biggest impact)
2. Adjust query builder (better retrieval)
3. Fine-tune temperature (consistency)
4. Add custom scoring (advanced)
