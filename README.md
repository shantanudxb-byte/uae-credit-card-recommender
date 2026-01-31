# 💳 UAE Credit Card Recommender

An intelligent credit card recommendation system for UAE residents that uses AI, RAG (Retrieval Augmented Generation), and adaptive questionnaires to find the perfect credit card match based on your financial profile.

## ✨ Features

- 🎯 **Smart Goal-Based Matching** - Prioritize up to 4 goals (cashback, travel miles, no fees, etc.)
- 💰 **Spending Pattern Analysis** - Analyzes 12 spending categories to find optimal rewards
- 🏪 **Lifestyle Integration** - Considers where you actually shop (Amazon, Noon, Lulu, etc.)
- 🤖 **Adaptive Questionnaire** - Asks 2-3 contextual questions only when needed
- 📊 **Accurate Value Estimation** - Calculates rewards based on actual merchant usage
- 🔍 **35+ UAE Credit Cards** - Comprehensive database with real card data
- 💬 **Interactive Chat** - Ask follow-up questions and compare cards
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile

## 🏗️ Architecture

```
Frontend (HTML/JS) → Flask API → CardAdvisor Engine
                                      ↓
                          ┌───────────┴───────────┐
                          ↓                       ↓
                  Question Generator      RAG Pipeline (Chroma)
                          ↓                       ↓
                  Profile Enrichment      Semantic Search
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key (for embeddings)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/shantanudxb-byte/uae-credit-card-recommender.git
cd uae-credit-card-recommender
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. Start the backend:
```bash
python -m app.api
```

5. Open the frontend:
```bash
cd frontend
python -m http.server 8000
```

6. Visit `http://localhost:8000` in your browser

## 📖 How It Works

### 1. Profile Collection
- Enter salary and monthly spending across 12 categories
- Select and prioritize up to 4 financial goals
- Optionally specify lifestyle preferences (stores, services)

### 2. Intelligent Questionnaire
- System detects gaps in your profile
- Asks 2-3 contextual questions (e.g., "Where do you shop for groceries?")
- Only triggers when lifestyle data is missing

### 3. Smart Recommendations
- **Goal-Based Cards**: Match your prioritized goals
- **Spending-Based Cards**: Optimize for your spending patterns
- **Top Choices**: Cards that excel in both categories

### 4. Accurate Value Calculation
- For co-branded cards (Amazon, Noon, Lulu): Only counts spending at partner merchants
- Shows exclusions: "(excludes X AED/month at non-partner merchants)"
- Without lifestyle data: Assumes all spending at partners

## 🎯 Example Use Case

**Profile:**
- Salary: 30,000 AED/month
- Top spending: Groceries (2,000), Online (1,500), Dining (1,200)
- Goals: Cashback (Priority 1), No Fee (Priority 2)
- Lifestyle: Shops at Amazon Fresh (70%), Noon (30%)

**Result:**
- Amazon.ae Credit Card: 6% cashback on Amazon Fresh groceries
- Estimated value: 1,440 AED/year (excludes 600 AED/month at Carrefour)

## 📊 Technology Stack

- **Backend**: Flask, Python 3.9
- **AI/ML**: LangChain, OpenAI Embeddings, Chroma Vector DB
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Data**: 35 UAE credit cards with real reward rates

## 🗂️ Project Structure

```
├── app/
│   ├── api.py                 # Flask API endpoints
│   ├── agent.py               # Card recommendation engine
│   ├── question_generator.py  # Adaptive questionnaire logic
│   ├── rag_pipeline.py        # Vector DB and semantic search
│   └── memory.py              # Conversation memory
├── data/
│   ├── uae_cards.json         # 35 credit cards database
│   ├── card_service_mapping.json  # Co-brand partnerships
│   └── card_apply_urls.json   # Application links
├── frontend/
│   └── index.html             # Single-page application
├── tests/
│   └── test_e2e_questionnaire.py
└── ARCHITECTURE.md            # Detailed system design
```

## 🔑 Key Algorithms

### Goal-Based Scoring
```python
score = 0.5 + (matched_goals * 0.15)
+ lifestyle_boost (0.3 per match)
+ spending_alignment (0.3 for high-value categories)
```

### Spending-Based Scoring
```python
score = 0.5 + Σ(category_spend / total_spend * reward_rate / 5 * 0.2)
+ co_brand_boost (0.3 * usage_percent)
```

## 📝 API Endpoints

- `POST /api/recommend` - Get card recommendations
- `POST /api/generate-questions` - Generate adaptive questions
- `POST /api/chat` - Chat with advisor
- `POST /api/filter` - Filter recommendations
- `GET /health` - Health check

## 🎨 Features in Detail

### Adaptive Questionnaire
- Triggers only when lifestyle data is missing
- Asks about unclear spending categories (miscellaneous ≥1000 AED, transport ≥500 AED, etc.)
- Supports multi-select, single-select, and custom text input
- Shows random insights while processing

### Value Calculation Logic
- **With lifestyle data**: Excludes non-partner spending for co-branded cards
- **Without lifestyle data**: Assumes all spending at partners (noted)
- Accounts for annual fees and calculates net benefit

### Goal Prioritization
- Click once to set priority (gold badge with number 1-4)
- Click again to deselect
- Top 4 priorities get higher weight in recommendations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🙏 Acknowledgments

- Credit card data sourced from official UAE bank websites
- Built with LangChain and OpenAI
- Inspired by the need for transparent, user-friendly financial tools

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**⭐ If you find this project helpful, please give it a star!**
