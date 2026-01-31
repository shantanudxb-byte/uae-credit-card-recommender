# Goal-Based vs Spending-Based Recommendations

## Overview
The recommendation system now splits recommendations into TWO distinct sections to help users understand different card options:

### 1. 🎯 Goal-Based Recommendations
**Purpose**: Help users achieve their selected goals, even if current spending doesn't align

**Example Scenario**:
- User Goal: "Travel Miles" + "Airport Lounge"
- Current Spending: Mostly groceries and dining (no travel spending)
- **Result**: System still recommends Emirates Skywards Card because it helps achieve the travel goals
- **Message**: "Perfect for earning air miles - 3.0% on travel bookings. Use this card for travel, airport_lounge to maximize benefits"

### 2. 💰 Spending-Based Recommendations
**Purpose**: Maximize rewards based on current spending patterns

**Example Scenario**:
- Current Spending: 3000 AED miscellaneous, 1000 AED groceries
- **Result**: System recommends WIO Mastercard (2% flat on everything)
- **Message**: "Flat 2.0% on all spending including miscellaneous (3000 AED/month)"

---

## Visual Design

### Section Headers
- **Goal-Based**: Purple gradient background with 🎯 icon
  - "Cards that help you achieve your selected goals"
  
- **Spending-Based**: Green gradient background with 💰 icon
  - "Cards optimized for your current spending patterns"

### Card Logos
Each card displays its official logo (50x50px) next to the card name for better brand recognition:
- Emirates Skywards Card
- Amazon.ae Credit Card
- Noon VIP Credit Card
- Liv Cashback Card
- WIO Mastercard
- SHARE Credit Card
- Mashreq Cashback Card

### Card Styling
- **Goal-Based Cards**: Purple left border with light purple gradient background
- **Spending-Based Cards**: Green left border with light green gradient background

---

## Logic Implementation

### Goal-Based Scoring
```python
def _get_goal_based_cards(user_profile):
    # Match cards to user goals regardless of spending
    # Score based on:
    # - Goal matches (0.15 per goal)
    # - Base score (0.5)
    # - No fee bonus (0.05)
```

**Key Features**:
- Ignores spending patterns
- Focuses purely on goal alignment
- Provides guidance on how to use the card for goals

### Spending-Based Scoring
```python
def _get_spending_based_cards(user_profile):
    # Match cards to spending patterns
    # Score based on:
    # - Lifestyle matches (co-branded, partner benefits)
    # - Category spending alignment
    # - Miscellaneous spending handling
    # - General rewards detection
```

**Key Features**:
- Analyzes actual spending
- Considers lifestyle preferences
- Handles miscellaneous spending intelligently
- Boosts general rewards cards when appropriate

---

## User Benefits

### 1. Clear Separation
Users can now see:
- Cards that help achieve future goals (aspirational)
- Cards that maximize current spending (practical)

### 2. Educational
Goal-based recommendations educate users:
- "Use this card for travel to maximize benefits"
- "Perfect for earning air miles even if you don't travel much now"

### 3. Flexibility
Users can choose based on:
- **Short-term**: Pick spending-based card for immediate rewards
- **Long-term**: Pick goal-based card to work towards goals

### 4. Visual Clarity
- Card logos for instant brand recognition
- Color-coded sections (purple = goals, green = spending)
- Clear explanations for each recommendation type

---

## Example Use Cases

### Case 1: Aspiring Traveler
**Profile**:
- Salary: 15,000 AED
- Spending: Groceries 2000, Dining 1500, Fuel 500
- Goals: Travel Miles, Airport Lounge

**Goal-Based Recommendations**:
1. Emirates Skywards Signature Card
   - "Perfect for earning air miles - 3.0% on travel bookings"
   - "Use this card for travel, airport_lounge to maximize benefits"

**Spending-Based Recommendations**:
1. Mashreq Cashback Card
   - "Earns 3.0% on groceries = 720 AED/year"
   - "Earns 3.5% on fuel = 210 AED/year"

**User Decision**: Can choose Emirates for future travel goals OR Mashreq for current spending rewards

---

### Case 2: Diverse Spender
**Profile**:
- Salary: 12,000 AED
- Spending: Miscellaneous 3000, Groceries 1000, Utilities 800
- Goals: Cashback

**Goal-Based Recommendations**:
1. WIO Mastercard
   - "Optimized for cashback rewards across categories"
   - "Flat 2.0% on all spending"

**Spending-Based Recommendations**:
1. WIO Mastercard (same card!)
   - "Flat 2.0% on all spending including miscellaneous (3000 AED/month)"
   - "Earns 2.0% on miscellaneous = 720 AED/year"

**User Decision**: Clear winner - WIO matches both goals AND spending

---

### Case 3: Amazon Shopper with Travel Goals
**Profile**:
- Salary: 10,000 AED
- Spending: Groceries 2000 (80% Amazon Fresh), Online 1500
- Goals: Travel Miles
- Lifestyle: Amazon Fresh 80%

**Goal-Based Recommendations**:
1. Emirates Skywards Signature Card
   - "Perfect for earning air miles - 3.0% on travel bookings"

**Spending-Based Recommendations**:
1. Amazon.ae Credit Card
   - "✓ 5% cashback on Amazon.ae including Amazon Fresh (80% of your spending)"
   - "Earns 5.0% on groceries = 1200 AED/year"

**User Decision**: 
- Pick Emirates if planning to travel soon
- Pick Amazon.ae for immediate high cashback on current spending

---

## Technical Details

### API Response Structure
```json
{
  "recommendations": [...],  // All unique cards (backward compatible)
  "goal_based": [...],       // Top 3 goal-matching cards
  "spending_based": [...],   // Top 3 spending-matching cards
  "has_goals": true          // Whether user selected any goals
}
```

### Frontend Display Logic
- If `has_goals = true` AND `goal_based` has cards → Show goal section
- Always show spending section
- Each section displays up to 3 cards
- Cards show appropriate icons and messaging based on type

---

## Future Enhancements

1. **Hybrid Recommendations**: Cards that score high in BOTH categories
2. **Goal Progress Tracking**: Show how much user needs to spend to reach goal
3. **Card Comparison**: Side-by-side comparison of goal vs spending cards
4. **Smart Suggestions**: "Consider using Card A for travel and Card B for daily spending"
5. **More Card Logos**: Add logos for all 15 cards in database
