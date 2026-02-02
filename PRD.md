# Product Requirements Document (PRD)
# UAE Credit Card Recommender

**Version:** 1.0  
**Date:** January 2025  
**Author:** Product Team  
**Status:** Implemented

---

## 1. Executive Summary

The UAE Credit Card Recommender is an intelligent recommendation system that helps UAE residents find the perfect credit card based on their financial profile, spending patterns, lifestyle preferences, and financial goals. The system uses AI-powered analysis, RAG (Retrieval Augmented Generation), and adaptive questionnaires to deliver personalized recommendations.

### Key Value Proposition
- **For Users:** Save hours of research by getting personalized credit card recommendations in minutes
- **For Banks:** Increase qualified lead generation through intelligent matching
- **Estimated User Savings:** 2,000 - 15,000 AED annually by choosing the optimal card

---

## 2. Problem Statement

### Current Pain Points
1. **Information Overload:** 35+ credit cards available in UAE with complex reward structures
2. **Hidden Value:** Users miss out on rewards because they don't know which card matches their spending
3. **Co-branded Confusion:** Cards like Amazon, Noon, Lulu offer high rewards but only at specific merchants
4. **Goal Mismatch:** Users often choose cards based on marketing rather than actual needs
5. **Time-Consuming Research:** Comparing cards manually takes 3-5 hours

### Target Users
- UAE residents with monthly salary 5,000 - 100,000+ AED
- Age: 25-55 years
- Tech-savvy professionals seeking to optimize finances
- Frequent shoppers, travelers, or lifestyle-focused individuals

---

## 3. Product Goals & Success Metrics

### Primary Goals
1. Deliver accurate, personalized credit card recommendations
2. Maximize user's potential rewards based on actual spending
3. Provide transparent value calculations

### Success Metrics
| Metric | Target | Current |
|--------|--------|---------|
| Recommendation Accuracy | >90% | 92% |
| User Conversion (Apply Click) | >15% | Tracking |
| Session Completion Rate | >70% | Tracking |
| Average Session Duration | 3-5 min | Tracking |
| User Satisfaction (NPS) | >50 | TBD |

---

## 4. User Personas

### Persona 1: The Optimizer (Primary)
- **Name:** Ahmed, 32
- **Salary:** 25,000 AED/month
- **Behavior:** Shops on Amazon (60%), Noon (30%), uses Careem daily
- **Goals:** Maximize cashback, no annual fee
- **Pain Point:** Doesn't know which card gives best rewards for his spending

### Persona 2: The Traveler
- **Name:** Sarah, 38
- **Salary:** 45,000 AED/month
- **Behavior:** Travels internationally 6x/year, prefers Emirates
- **Goals:** Earn miles, airport lounge access
- **Pain Point:** Confused between Emirates Skywards vs Etihad Guest cards

### Persona 3: The Budget-Conscious
- **Name:** Raj, 26
- **Salary:** 8,000 AED/month
- **Behavior:** Entry-level professional, careful with spending
- **Goals:** No annual fee, build credit history
- **Pain Point:** Limited options due to low salary requirement

---

## 5. Feature Specifications

### 5.1 Profile Collection

**Purpose:** Gather user's financial information for personalized recommendations

**Input Fields:**
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Monthly Salary | Number | Yes | Min: 1,000 AED |
| Spending Categories (12) | Number | No | Min: 0 |
| Financial Goals | Multi-select | No | Max: 4 priorities |
| Lifestyle Preferences | Multi-select | No | With usage % |

**Spending Categories:**
1. Groceries
2. International Travel
3. Local Transport (Careem, RTA, Metro)
4. Fuel
5. Online Shopping
6. Dining
7. Education
8. Remittances
9. Entertainment
10. Healthcare
11. Utilities/Bills
12. Miscellaneous

**Financial Goals:**
- ✈️ Travel Miles
- 💵 Cashback
- 🆓 No Annual Fee
- 🛫 Airport Lounge
- 🍽️ Dining Rewards
- ⭐ Premium Benefits
- ⛽ Fuel Savings
- 🛍️ Online Shopping


### 5.2 Adaptive Questionnaire

**Purpose:** Fill gaps in user profile with contextual questions

**Trigger Conditions:**
- Miscellaneous spending ≥ 1,000 AED (no breakdown provided)
- Local transport ≥ 500 AED (no service specified)
- Online shopping ≥ 1,000 AED (no platform specified)
- Groceries ≥ 800 AED (no store specified)

**Question Types:**
1. **Multi-select:** "Where do you shop for groceries?" (Lulu, Carrefour, Amazon Fresh, Noon Daily)
2. **Single-select:** "How often do you travel internationally?" (Monthly, Quarterly, Occasional, Rare)
3. **Custom input:** "What does miscellaneous spending include?" (with text field)

**UX Flow:**
```
Profile Submitted → Gap Detection → Show Modal (2-3 questions max) → Display Insights → Get Recommendations
```

**Design Requirements:**
- Modal overlay with progress bar
- Maximum 2-3 questions per session
- Skip option available
- Random insight shown while processing
- Smooth animations (slideIn/slideOut)

---

### 5.3 Recommendation Engine

**Algorithm Overview:**

#### Goal-Based Scoring
```
Base Score = 0.5
+ Matched Goals × 0.15
+ Lifestyle Match × 0.3 (weighted by usage %)
+ Spending Alignment × 0.3
+ Travel Reward Boost (5%+ rate: +0.2, 3%+ rate: +0.1)
+ No Fee Bonus × 0.05
```

#### Spending-Based Scoring
```
Base Score = 0.5
+ Σ(category_spend / total_spend × reward_rate / 5 × 0.2)
+ Co-brand Boost × 0.3 × usage_percent
+ High Online Spender Bonus (>1500 AED, 5%+ rate: +0.2)
+ International Traveler Bonus (>2000 AED: +0.15)
```

**Output Structure:**
- **Top Choices:** Cards appearing in both goal-based AND spending-based (score boosted +0.1)
- **Goal-Based Cards:** Top 5 cards matching user's prioritized goals
- **Spending-Based Cards:** Top 3 cards optimized for spending patterns

**Value Calculation Logic:**
```
For Co-branded Cards (Amazon, Noon, Lulu):
  WITH lifestyle data:
    - Only count spending at partner merchants
    - Show exclusion: "(excludes X AED/month at non-partner)"
  
  WITHOUT lifestyle data:
    - Assume all spending at partners
    - Show note: "(assumes all spending at partner merchants)"

Net Value = (Total Rewards × 12) - Annual Fee
```

---

### 5.4 Card Display & Interaction

**Card Information Displayed:**
- Card name with bank logo
- Match score (0-100%)
- Annual fee
- Minimum salary requirement
- Matched goals (badges)
- 4 key reasons for recommendation
- Estimated annual value with exclusions
- AI-generated explanation (top 3 cards only)
- Apply Now button (tracked)

**Visual Hierarchy:**
1. **Top Choices:** Gold border, "🏆 Perfect Match" badge
2. **Goal-Based:** Blue gradient background
3. **Spending-Based:** Green gradient background

**Interaction Tracking:**
- Card click → Analytics event
- Apply button click → Analytics event + external redirect

---

### 5.5 Interactive Chat

**Purpose:** Answer follow-up questions and compare cards

**Capabilities:**
- "What if my salary increases to 20K?"
- "Compare Emirates Skywards vs ADCB Traveller"
- "Show me cards with no annual fee"
- "Which card is best for Amazon shopping?"

**LLM Integration:**
- Model: Groq (llama-3.3-70b-versatile)
- Context: User profile + card database + RAG retrieval
- Guardrails: No hallucinations, RAG-enforced answers only
- Auto-detection: Prime membership, spending tiers from card notes

---

## 6. Technical Architecture

### 6.1 System Components

```
┌─────────────────┐
│  Frontend (JS)  │
│  - index.html   │
│  - analytics.js │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Flask API     │
│  - /recommend   │
│  - /questions   │
│  - /chat        │
│  - /track/*     │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌──────────────┐
│ Agent   │ │ RAG Pipeline │
│ Engine  │ │ (Chroma DB)  │
└─────────┘ └──────────────┘
    │
    ▼
┌─────────────────┐
│  LLM Agent      │
│  (Groq)         │
└─────────────────┘
```

### 6.2 Data Models

**User Profile:**
```json
{
  "salary": 30000,
  "spend": {
    "groceries": 2000,
    "online": 1500,
    "dining": 1200
  },
  "goals": ["cashback", "no_fee"],
  "goal_priorities": {"cashback": 1, "no_fee": 2},
  "lifestyle": {
    "groceries": [{"service": "amazon_fresh", "usage_percent": 70}],
    "online_shopping": [{"service": "amazon_ae", "usage_percent": 60}]
  }
}
```

**Card Data:**
```json
{
  "name": "Amazon.ae Credit Card",
  "bank": "Emirates Islamic Bank",
  "annual_fee": 0,
  "min_salary": 15000,
  "rewards": {
    "groceries": 6.0,
    "online": 6.0,
    "international": 2.5,
    "domestic": 2.0
  },
  "rewards_prime": {"amazon_spend": 6.0},
  "rewards_non_prime": {"amazon_spend": 3.0},
  "best_for": ["amazon", "online", "groceries", "prime_members"]
}
```

### 6.3 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/recommend` | POST | Get card recommendations |
| `/api/generate-questions` | POST | Generate adaptive questions |
| `/api/chat` | POST | Chat with AI advisor |
| `/api/track/card-click` | POST | Track card interaction |
| `/api/track/apply-click` | POST | Track apply button click |
| `/api/analytics/metrics` | GET | Get analytics dashboard data |
| `/health` | GET | Health check |

---

## 7. Analytics & Tracking

### 7.1 User Journey Funnel

```
Initiated (Profile Started)
    ↓
Profile Completed
    ↓
Recommendations Shown
    ↓
Card Clicked
    ↓
Applied (Apply Button Clicked)
```

### 7.2 Tracked Events

**Session Events:**
- Session ID generation
- Profile submission
- Questionnaire completion
- Recommendations displayed

**Interaction Events:**
- Card click (card name, position)
- Apply button click (card name, position, URL)
- Chat message sent

### 7.3 Analytics Dashboard

**Metrics Displayed:**
- Total sessions
- Conversion rate (applied / total)
- Average recommendations per session
- Total apply clicks
- Top recommended cards (with click rate)
- Salary distribution
- Spending category breakdown
- Recent sessions table

**Technology:** Flask-based dashboard (port 8501)

---

## 8. Security & Compliance

### 8.1 Security Measures

**Input Validation:**
- SQL injection prevention (parameterized queries)
- Prompt injection detection and blocking
- Data type validation (salary, spending amounts)
- Range validation (salary ≥ 1000 AED)

**Output Safety:**
- No PII exposure in logs
- Sanitized error messages
- No credential leakage

**Test Coverage:** 23/23 security tests passing (100%)

### 8.2 Data Privacy

- No personal data stored beyond session
- Session IDs are UUIDs (non-identifiable)
- No credit card information collected
- Analytics data anonymized

---

## 9. User Experience (UX) Specifications

### 9.1 Design Principles

1. **Simplicity:** One-page application, minimal clicks
2. **Transparency:** Show why each card is recommended
3. **Visual Hierarchy:** Color-coded sections (gold for top choices)
4. **Progressive Disclosure:** Optional lifestyle fields, adaptive questions
5. **Mobile-First:** Responsive design for all screen sizes

### 9.2 Color Palette

- **Primary:** #667eea (Purple gradient)
- **Secondary:** #764ba2 (Deep purple)
- **Success:** #10b981 (Green)
- **Warning:** #FFD700 (Gold)
- **Background:** #f9fafb (Light gray)

### 9.3 Key Interactions

**Goal Selection:**
- Click once → Select (blue border)
- Click again → Set priority (gold badge with number 1-4)
- Click third time → Deselect

**Lifestyle Services:**
- Click → Modal opens for usage percentage
- Slider: 10% - 100% in 10% increments
- Re-click → Edit usage percentage

**Card Results:**
- Hover → Slight lift animation
- Click → Track analytics event
- Apply button → Track + redirect to bank


---

## 10. UI Mockups & Wireframes

### 10.1 Profile Collection Screen

```
┌─────────────────────────────────────────────────────────┐
│  💳 UAE Credit Card Advisor                             │
│  Find the perfect credit card tailored to your lifestyle│
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📊 Financial Profile                                    │
│  ┌────────────────────────────────────────────────┐    │
│  │ Monthly Salary (AED)                           │    │
│  │ [        30000        ]                        │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  💰 Monthly Spending                                     │
│  ┌──────────┬──────────┬──────────┬──────────┐        │
│  │🛒 Groceries│✈️ Travel │🚗 Transport│⛽ Fuel  │        │
│  │[  2000  ] │[ 1000  ] │[  800   ] │[   0  ] │        │
│  └──────────┴──────────┴──────────┴──────────┘        │
│  ┌──────────┬──────────┬──────────┬──────────┐        │
│  │🛍️ Online │🍽️ Dining │🎓 Education│💸 Remit │        │
│  │[ 1500  ] │[ 1200  ] │[   0   ] │[   0  ] │        │
│  └──────────┴──────────┴──────────┴──────────┘        │
│                                                          │
│  🎯 Your Goals & Priorities                              │
│  Click to select. Click again to set priority (1-4)     │
│  ┌─────────┬─────────┬─────────┬─────────┐            │
│  │✈️ Travel│💵 Cashback│🆓 No Fee│🛫 Lounge│            │
│  │  Miles  │    ①    │         │         │            │
│  └─────────┴─────────┴─────────┴─────────┘            │
│                                                          │
│  🏪 Your Lifestyle (Optional)                            │
│  🛒 Groceries:                                           │
│  [Lulu] [Carrefour] [Amazon Fresh 70%] [Noon Daily]    │
│                                                          │
│  🛍️ Online Shopping:                                     │
│  [Amazon.ae 60%] [Noon 30%] [Namshi] [+ Add Other]     │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │      Get My Recommendations                    │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### 10.2 Adaptive Questionnaire Modal

```
┌─────────────────────────────────────────────────────────┐
│  🎯 Help Us Personalize Your Recommendations            │
│  Answer 2 quick questions for better card matches       │
│  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 33%       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  You spend 1,500 AED/month on online shopping           │
│  Where do you shop most frequently?                     │
│  (Select all that apply)                                │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │ 📦 Amazon.ae                              ✓    │    │
│  └────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────┐    │
│  │ 🛍️ Noon                                   ✓    │    │
│  └────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────┐    │
│  │ 🌍 International sites                         │    │
│  └────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────┐    │
│  │ 👗 Namshi & fashion                            │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  💡 Skip if unsure - we'll still give great recommendations│
│                                                          │
│  [Skip]                              [← Back] [Next →]  │
└─────────────────────────────────────────────────────────┘
```

### 10.3 Recommendations Results

```
┌─────────────────────────────────────────────────────────┐
│  📋 Your Profile Summary                                 │
│  ┌──────────┬──────────┬──────────┬──────────┐        │
│  │  30,000  │  15,300  │    2     │    6     │        │
│  │  Salary  │  Spend   │  Goals   │  Cards   │        │
│  └──────────┴──────────┴──────────┴──────────┘        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🏆 Perfect Matches                                      │
│  Cards that match both your goals AND spending patterns  │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │ 🏆 Perfect Match                               │    │
│  │ ┌──┐ Amazon.ae Credit Card                     │    │
│  │ │AM│ Emirates Islamic Bank                     │    │
│  │ └──┘                                            │    │
│  │ 💵 Cashback  🛍️ Online                          │    │
│  │ Match Score: 95%                                │    │
│  │                                                  │    │
│  │ Annual Fee: FREE    Min. Salary: 15,000 AED    │    │
│  │                                                  │    │
│  │ 🏆 Perfect for your goals AND spending:         │    │
│  │ ✓ 6% cashback on Amazon.ae (1,500 AED/month)   │    │
│  │ ✓ You use Amazon Fresh 70% for groceries       │    │
│  │ ✓ 2.5% on international spending                │    │
│  │ ✓ Zero annual fee matches your goals           │    │
│  │                                                  │    │
│  │ 💰 Estimated Value: 1,440 AED net benefit       │    │
│  │    (excludes 600 AED/month at Carrefour)       │    │
│  │                                                  │    │
│  │ [→ Apply Now]                                   │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────┬──────────────────────┐       │
│  │ 🎯 Goal-Based        │ 💰 Spending-Based    │       │
│  │ Achieve your goals   │ Match your spending  │       │
│  ├──────────────────────┼──────────────────────┤       │
│  │ [Card 1]             │ [Card 1]             │       │
│  │ [Card 2]             │ [Card 2]             │       │
│  │ [Card 3]             │ [Card 3]             │       │
│  └──────────────────────┴──────────────────────┘       │
│                                                          │
│  💬 Have Questions? Chat with Our Advisor               │
│  ┌────────────────────────────────────────────────┐    │
│  │ 👋 Hi! I'm here to help you find the perfect   │    │
│  │    credit card. Feel free to ask me anything   │    │
│  │    like:                                        │    │
│  │    • "What if my salary increases to 20K?"     │    │
│  │    • "Compare Emirates Skywards vs ADCB"       │    │
│  │    • "Show me cards with no annual fee"        │    │
│  └────────────────────────────────────────────────┘    │
│  [Type your question here...            ] [Send]       │
│                                                          │
│  [Start New Search]                                     │
└─────────────────────────────────────────────────────────┘
```

### 10.4 Analytics Dashboard

```
┌─────────────────────────────────────────────────────────┐
│  💳 Credit Card Recommender Analytics                   │
│  [🔄 Refresh]                                           │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┬──────────┬──────────┬──────────┐        │
│  │   156    │   18%    │   5.2    │    28    │        │
│  │ Sessions │Conversion│Avg Cards │  Applies │        │
│  └──────────┴──────────┴──────────┴──────────┘        │
│                                                          │
│  Top Recommended Cards                                   │
│  ┌────────────────────────────────────────────────┐    │
│  │ Amazon.ae Credit Card        ████████ 45       │    │
│  │ Liv Cashback Card            ██████ 32         │    │
│  │ FAB Cashback                 ████ 28           │    │
│  │ Emirates Skywards            ███ 24            │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Recent Sessions                                         │
│  ┌────────┬────────┬──────────┬───────┬────────┐      │
│  │Session │ Salary │  Goals   │ Cards │Applied │      │
│  ├────────┼────────┼──────────┼───────┼────────┤      │
│  │ a3f2...│ 30,000 │ Cashback │   6   │   ✅   │      │
│  │ b8d1...│ 15,000 │ Travel   │   5   │   ❌   │      │
│  │ c4e9...│ 45,000 │ Premium  │   4   │   ✅   │      │
│  └────────┴────────┴──────────┴───────┴────────┘      │
└─────────────────────────────────────────────────────────┘
```

---

## 11. Edge Cases & Error Handling

### 11.1 Input Validation

| Scenario | Handling |
|----------|----------|
| Salary < 1,000 AED | Show error: "Minimum salary 1,000 AED required" |
| All spending = 0 | Proceed with goal-based recommendations only |
| No goals selected | Show spending-based recommendations only |
| Total lifestyle usage > 100% | Alert: "Total usage cannot exceed 100%" |

### 11.2 No Results Scenarios

**Case 1: Salary too low for any card**
- Show message: "No cards match your salary requirement"
- Suggest: "Consider cards with lower minimum salary"

**Case 2: Conflicting goals**
- Example: "Premium benefits" + "No annual fee"
- Show: Best compromise cards with explanation

**Case 3: No co-branded match**
- Fall back to general rewards cards
- Explain: "No specific cards for your stores, showing best general rewards"

### 11.3 API Failures

| Error | User Message | Fallback |
|-------|--------------|----------|
| Backend down | "Service temporarily unavailable" | Retry button |
| LLM timeout | "Chat unavailable, try again" | Show recommendations only |
| Database error | "Unable to load cards" | Cache previous results |

---

## 12. Performance Requirements

### 12.1 Response Times

| Operation | Target | Current |
|-----------|--------|---------|
| Profile submission | < 2s | ~1.5s |
| Question generation | < 1s | ~0.8s |
| Recommendations | < 3s | ~2.2s |
| Chat response | < 5s | ~3.5s |
| Analytics dashboard | < 2s | ~1.2s |

### 12.2 Scalability

- **Concurrent users:** Support 100+ simultaneous sessions
- **Database:** SQLite (current), migrate to PostgreSQL for production
- **Caching:** Implement Redis for card data (future)

---

## 13. Testing & Quality Assurance

### 13.1 Test Coverage

| Test Type | Coverage | Status |
|-----------|----------|--------|
| Security Tests | 23/23 | ✅ 100% |
| Agent Evaluation | 12/12 | ✅ 92% accuracy |
| Integration Tests | 8/8 | ✅ Pass |
| E2E Tests | 5/5 | ✅ Pass |

### 13.2 Key Test Scenarios

1. **High earner (50K+):** Should recommend premium cards
2. **Budget user (5-8K):** Should recommend no-fee cards
3. **Amazon shopper (70% usage):** Should recommend Amazon.ae card as top choice
4. **Frequent traveler:** Should recommend Emirates/Etihad cards
5. **Miscellaneous spender:** Should trigger questionnaire

---

## 14. Deployment & Operations

### 14.1 Environment Setup

**Backend:**
```bash
python -m app.api  # Port 5001
```

**Frontend:**
```bash
cd frontend && python -m http.server 8000
```

**Analytics Dashboard:**
```bash
python dashboard_simple.py  # Port 8501
```

### 14.2 Environment Variables

```
OPENAI_API_KEY=<key>      # For embeddings (RAG)
GROQ_API_KEY=<key>        # For LLM chat
```

### 14.3 Dependencies

**Core:**
- Flask 2.3+
- LangChain 0.1+
- Chroma 0.4+
- Groq 0.4+

**Analytics:**
- SQLite3 (built-in)

---

## 15. Future Roadmap

### Phase 2 (Q2 2025)
- [ ] User accounts & saved profiles
- [ ] Email recommendations
- [ ] Card comparison tool (side-by-side)
- [ ] Mobile app (iOS/Android)

### Phase 3 (Q3 2025)
- [ ] Real-time card offers integration
- [ ] Spending tracker integration (link bank account)
- [ ] Personalized alerts (new cards, better offers)
- [ ] Referral program

### Phase 4 (Q4 2025)
- [ ] Multi-card portfolio optimization
- [ ] Credit score integration
- [ ] Loan & mortgage recommendations
- [ ] B2B white-label solution for banks

---

## 16. Success Stories (Projected)

### Example 1: Ahmed's Savings
- **Before:** Using random bank card, earning 200 AED/year
- **After:** Switched to Amazon.ae card, earning 1,440 AED/year
- **Savings:** 1,240 AED/year (620% increase)

### Example 2: Sarah's Travel Perks
- **Before:** No lounge access, paying 150 AED per visit
- **After:** Emirates Skywards Signature, free lounge + 3,600 miles/year
- **Value:** 2,400 AED in benefits

### Example 3: Raj's Credit Building
- **Before:** Rejected for premium cards
- **After:** Approved for Liv Cashback (5K salary), earning 540 AED/year
- **Impact:** Building credit history + rewards

---

## 17. Appendix

### 17.1 Card Database Summary

- **Total Cards:** 35
- **Banks:** FAB, Emirates NBD, ADCB, Mashreq, RAKBank, Emirates Islamic, WIO, MAF Finance
- **Categories:** Travel, Cashback, Co-branded, Premium, No-fee, Lifestyle
- **Data Sources:** Official bank websites (updated Jan 2025)

### 17.2 Glossary

- **RAG:** Retrieval Augmented Generation (AI technique)
- **Co-branded Card:** Card partnered with specific merchant (Amazon, Noon, Lulu)
- **Fit Score:** 0-100% match between user profile and card benefits
- **Net Value:** Annual rewards minus annual fee
- **Lifestyle Match:** User's preferred merchants align with card partnerships

### 17.3 References

- AWS Pricing Calculator: https://calculator.aws
- UAE Central Bank Regulations: https://centralbank.ae
- Card Application URLs: See `data/card_apply_urls.json`

---

**Document Version History:**
- v1.0 (Jan 2025): Initial PRD based on implemented solution
- Future updates: Track in Git commits

**Approval:**
- [ ] Product Manager
- [ ] Engineering Lead
- [ ] Design Lead
- [ ] Stakeholders

---

*End of Product Requirements Document*
