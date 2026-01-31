# UAE Credit Card Recommender - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER (Customer)                                 │
│                    Browser: Chrome/Safari/Firefox                            │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (index.html)                                │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ 1. Profile Collection Form                                             │ │
│  │    - Salary input                                                      │ │
│  │    - 12 spending categories (groceries, travel, fuel, etc.)           │ │
│  │    - 8 goal tags (cashback, travel, no_fee, etc.)                     │ │
│  │    - 6 lifestyle categories with service selection                    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                 │                                            │
│                                 ▼                                            │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ 2. Questionnaire Modal (Conditional)                                   │ │
│  │    - Triggers if lifestyle is empty                                    │ │
│  │    - 2-3 contextual questions based on spending                        │ │
│  │    - Question types: multi-select, single-select, ranking              │ │
│  │    - Shows insight card while API processes                            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                 │                                            │
│                                 ▼                                            │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ 3. Results Display                                                     │ │
│  │    - Profile summary (4 stats)                                         │ │
│  │    - Top choices (goal + spending match)                               │ │
│  │    - Goal-based cards (up to 5)                                        │ │
│  │    - Spending-based cards (up to 3)                                    │ │
│  │    - Filter options (annual fee, reward type, etc.)                    │ │
│  │    - Chat interface for follow-up questions                            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ HTTP/JSON (Port 5001)
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BACKEND API (Flask)                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ API Endpoints (app/api.py)                                             │ │
│  │  • POST /api/generate-questions  → Question generation                 │ │
│  │  • POST /api/recommend           → Card recommendations                │ │
│  │  • POST /api/chat                → Follow-up Q&A                       │ │
│  │  • POST /api/filter              → Filter results                      │ │
│  │  • GET  /health                  → Health check                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐
│  Question Generator Module   │  │   Card Advisor Module        │
│  (app/question_generator.py) │  │   (app/agent.py)             │
│                              │  │                              │
│  • Analyze spending patterns │  │  • Load 35 UAE cards         │
│  • Detect unclear categories │  │  • Filter by salary          │
│  • Generate 2-3 questions    │  │  • Goal-based matching       │
│  • Enrich profile with       │  │  • Spending-based scoring    │
│    questionnaire answers     │  │  • Lifestyle co-brand boost  │
│                              │  │  • Generate reasons          │
└──────────────┬───────────────┘  └──────────┬───────────────────┘
               │                             │
               │                             ▼
               │                  ┌──────────────────────────────┐
               │                  │   RAG Pipeline Module        │
               │                  │   (app/rag_pipeline.py)      │
               │                  │                              │
               │                  │  • Chroma vector database    │
               │                  │  • OpenAI embeddings         │
               │                  │  • Semantic card search      │
               │                  │  • Retriever for chat        │
               │                  └──────────┬───────────────────┘
               │                             │
               └─────────────────────────────┼─────────────────────┐
                                             │                     │
                                             ▼                     ▼
                              ┌──────────────────────┐  ┌──────────────────────┐
                              │   Data Layer         │  │   Memory Module      │
                              │                      │  │   (app/memory.py)    │
                              │  • uae_cards.json    │  │                      │
                              │    (35 cards)        │  │  • Conversation      │
                              │  • card_service_     │  │    buffer memory     │
                              │    mapping.json      │  │  • Chat context      │
                              │  • card_apply_       │  │                      │
                              │    urls.json         │  │                      │
                              └──────────────────────┘  └──────────────────────┘
```

---

## Detailed Component Flow

### 1. **User Input Collection** (Frontend)

**Business Function**: Gather customer financial profile
**Technical Implementation**: HTML form with JavaScript

**Data Collected**:
- **Salary**: Monthly income (AED)
- **Spending**: 12 categories with amounts
  - Groceries, International Travel, Local Transport, Fuel
  - Online Shopping, Dining, Education, Remittances
  - Entertainment, Healthcare, Utilities, Miscellaneous
- **Goals**: Up to 8 selectable goals
  - Travel Miles, Cashback, No Annual Fee, Airport Lounge
  - Dining Rewards, Premium Benefits, Fuel Savings, Online Shopping
- **Lifestyle** (Optional): Service preferences with usage %
  - Groceries: Lulu, Carrefour, Amazon Fresh, Noon Daily
  - Online: Amazon.ae, Noon, Namshi
  - Fuel: ADNOC, ENOC, Emarat
  - Entertainment: VOX, Reel Cinemas, etc.
  - Airlines: Emirates, Etihad, FlyDubai

---

### 2. **Intelligent Questionnaire** (Frontend + Backend)

**Business Function**: Fill gaps in customer profile for better recommendations
**Technical Implementation**: Dynamic question generation based on spending patterns

**Trigger Condition**: `lifestyle` is empty

**Question Generation Logic** (`generate_questions()`):
```
IF miscellaneous >= 1000 AED → Ask what it includes
IF domestic_transport >= 500 AED → Ask transport type (Careem, Metro, etc.)
IF online >= 1000 AED → Ask shopping platforms
IF groceries >= 800 AED → Ask grocery stores
IF dining >= 1000 AED → Ask dining habits
IF fuel >= 400 AED → Ask fuel stations
IF entertainment >= 800 AED → Ask entertainment type
IF international_travel >= 1500 AED → Ask travel frequency

ALWAYS add priority ranking question (cashback vs miles vs no_fee vs premium)
```

**Question Types**:
- **Multi-select**: Select all that apply (e.g., "Where do you shop?")
- **Single-select**: Choose one option (e.g., "Travel frequency?")
- **Ranking**: Rank priorities 1-4 (e.g., "What matters most?")

**Profile Enrichment** (`enrich_profile_with_answers()`):
- Converts answers to `lifestyle` data structure
- Adds goals from priority ranking (top 2)
- Stores custom text for miscellaneous breakdown
- Sets 50% usage_percent for all services

---

### 3. **Card Recommendation Engine** (Backend)

**Business Function**: Match customer profile to best credit cards
**Technical Implementation**: Multi-factor scoring algorithm

#### 3.1 **Goal-Based Matching** (`_get_goal_based_cards()`)

**Logic**:
```
FOR each card in database:
  IF card.min_salary > user.salary → SKIP
  
  matched_goals = []
  FOR each user_goal:
    IF goal in card.best_for → ADD to matched_goals
  
  IF no matched_goals → SKIP
  
  base_score = 0.5 + (matched_goals_count × 0.15)
  
  BOOST score IF:
    - No annual fee (+0.05)
    - High international travel + international rewards (+0.2)
    - High transport spend + transport benefits (+0.15)
    - High online spend + high online rewards (+0.25)
    - Entertainment goals + entertainment tags (+0.2)
    - High salary + premium card (+0.25)
    - Goal + spending alignment (+0.3)
    - Lifestyle co-brand match (+0.3 × usage%)
  
  RETURN top 5 cards sorted by (matched_goals_count, fit_score)
```

**Output**: Up to 5 cards with matched goals highlighted

#### 3.2 **Spending-Based Matching** (`_get_spending_based_cards()`)

**Logic**:
```
FOR each card in database:
  IF card.min_salary > user.salary → SKIP
  
  base_score = 0.5
  
  FOR each lifestyle service:
    IF co-branded card match → score += 0.3 × usage%
    IF partner benefits → score += 0.15 × usage%
  
  IF online_spend > 1500 AND online_rate >= 5% → score += 0.2
  IF international_travel > 2000 → score += 0.15
  IF domestic_transport > 800 AND transport_benefits → score += 0.1
  IF miscellaneous > 30% AND general_rewards → score += 0.25
  
  FOR each spending category:
    score += (amount/total_spend) × (reward_rate/5) × 0.2
  
  IF goals match card.best_for → score += 0.1 per match
  IF no annual fee → score += 0.05
  
  RETURN top 3 cards sorted by fit_score
```

**Output**: Up to 3 cards optimized for spending patterns

#### 3.3 **Top Choices Identification**

**Logic**:
```
top_choices = goal_based_cards ∩ spending_based_cards
FOR each top_choice:
  fit_score += 0.1 (boost)
  is_top_choice = true
```

**Output**: Cards appearing in both lists (perfect matches)

---

### 4. **RAG Pipeline** (Backend)

**Business Function**: Enable semantic search and chat functionality
**Technical Implementation**: Vector database + LLM

**Components**:
- **Vector Store**: Chroma DB (local persistence at `./.chroma_db`)
- **Embeddings**: OpenAI `text-embedding-ada-002`
- **LLM**: OpenAI `gpt-4o-mini`
- **Documents**: 35 UAE credit cards with metadata

**Usage**:
- **Chat**: Retrieve relevant cards for user questions
- **Semantic Search**: Find cards similar to user goals

---

### 5. **Results Display** (Frontend)

**Business Function**: Present recommendations with explanations
**Technical Implementation**: Dynamic HTML rendering

**Display Sections**:

1. **Profile Summary** (4 stats)
   - Monthly Salary
   - Total Monthly Spend
   - Goals Selected
   - Cards Recommended

2. **Top Choices** (if any)
   - 🏆 Perfect Match badge
   - Cards matching both goals AND spending
   - Horizontal grid layout

3. **Goal-Based Cards** (if goals selected)
   - 🎯 Goal badges showing matched goals
   - Match score (X/Y goals)
   - Reasons focused on goal achievement

4. **Spending-Based Cards**
   - 💰 Spending optimization focus
   - Lifestyle match highlights
   - Annual value estimates

**Card Details Shown**:
- Card name + bank
- Annual fee
- Minimum salary
- Match score (0-100%)
- 3-4 reasons why it matches
- Estimated annual value
- Apply button (if URL available)

---

### 6. **Interactive Filters** (Frontend)

**Business Function**: Refine recommendations based on preferences
**Technical Implementation**: Client-side filtering with fallback

**Filter Options**:
- **Annual Fee**: No fee / Low fee / Any fee
- **Reward Type**: Cashback / Miles / Mixed
- **Spending Focus**: Travel / Dining / Groceries / Online / Fuel
- **Premium Benefits**: Yes / No

**Fallback Logic**: If filter returns 0 cards → show top 3 from original

---

### 7. **Chat Interface** (Frontend + Backend)

**Business Function**: Answer follow-up questions
**Technical Implementation**: RAG-based Q&A

**Capabilities**:
- "What if my salary is 20K?"
- "Compare Emirates Skywards vs ADCB Traveller"
- "Show me cards with no annual fee"
- Context-aware responses using conversation memory

---

## Data Flow Diagram

```
User Input
    ↓
[Check Lifestyle]
    ↓
Empty? → YES → Generate Questions → Show Modal → Collect Answers → Enrich Profile
    ↓                                                                      ↓
   NO ←──────────────────────────────────────────────────────────────────┘
    ↓
Send to /api/recommend
    ↓
[Question Generator] → Enrich profile with questionnaire_answers
    ↓
[Card Advisor]
    ↓
Filter by salary
    ↓
    ├─→ Goal-Based Matching → Score & Rank → Top 5 Goal Cards
    │
    └─→ Spending-Based Matching → Score & Rank → Top 3 Spending Cards
    ↓
Identify Top Choices (intersection)
    ↓
Return JSON response
    ↓
Frontend renders results
    ↓
User applies filters OR asks chat questions
    ↓
[Optional] /api/filter OR /api/chat
    ↓
Updated results displayed
```

---

## Technology Stack

### Frontend
- **HTML5/CSS3**: UI structure and styling
- **Vanilla JavaScript**: Form handling, modal logic, API calls
- **Fetch API**: HTTP requests to backend

### Backend
- **Python 3.9+**: Core language
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin requests
- **LangChain**: RAG framework
- **OpenAI API**: Embeddings + LLM
- **Chroma**: Vector database

### Data
- **JSON files**: Card database, mappings, URLs
- **Vector embeddings**: Semantic search index

---

## Key Business Rules

1. **Salary Eligibility**: Cards with `min_salary > user.salary` are excluded
2. **Goal Matching**: At least 1 goal must match to appear in goal-based
3. **Scoring Range**: 0.0 to 1.0 (displayed as 0-100%)
4. **Top Choices**: Must appear in both goal-based AND spending-based
5. **Questionnaire**: Only triggers if lifestyle is empty
6. **Filter Fallback**: Always return at least 3 cards
7. **Lifestyle Boost**: Co-branded cards get 30% × usage% score boost

---

## Performance Metrics

- **API Response Time**: < 100ms (typical)
- **Question Generation**: < 10ms
- **Card Recommendations**: < 50ms
- **Chat Response**: < 500ms (LLM dependent)
- **Frontend Render**: < 100ms

---

## Security & Privacy

- **No Data Storage**: All data in-memory only
- **No User Tracking**: No cookies or analytics
- **API Key Security**: OpenAI key in `.env` (not committed)
- **CORS Enabled**: Allows frontend-backend communication
- **Input Validation**: Salary, spending amounts validated

---

## Extensibility Points

1. **Add More Cards**: Update `uae_cards.json` → Rebuild vector DB
2. **New Questions**: Add to `question_generator.py`
3. **Custom Scoring**: Modify `_calculate_score_with_lifestyle()`
4. **New Filters**: Add to frontend + backend filter logic
5. **LLM Model**: Change `OPENAI_MODEL_NAME` in `.env`
6. **Embeddings**: Swap OpenAI for local models (e.g., Sentence Transformers)

---

## Error Handling

- **Backend Down**: Frontend shows error message
- **Invalid Input**: API returns 400 with error details
- **No Cards Match**: Shows "No matching cards" message
- **Filter Too Strict**: Falls back to top 3 cards
- **Chat Failure**: Shows "trouble connecting" message

---

## Future Enhancements

1. **User Accounts**: Save profiles and preferences
2. **Application Tracking**: Track card applications
3. **Comparison Tool**: Side-by-side card comparison
4. **Personalized Insights**: ML-based spending analysis
5. **Multi-language**: Arabic support
6. **Mobile App**: Native iOS/Android apps
7. **Bank Integration**: Real-time eligibility checks
8. **Reward Calculator**: Precise annual value estimates
