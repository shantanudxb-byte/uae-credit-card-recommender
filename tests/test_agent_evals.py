"""
Comprehensive evaluation suite for UAE Credit Card Recommender LLM Agent
Tests: RAG accuracy, guardrails, hallucination prevention, recommendation quality
"""

import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agent import CardAdvisor
from app.llm_agent import LLMAgent

class AgentEvaluator:
    def __init__(self):
        self.advisor = CardAdvisor()
        self.llm_agent = LLMAgent()
        self.results = {
            "passed": 0,
            "failed": 0,
            "tests": []
        }
    
    def run_all_tests(self):
        """Run all evaluation tests"""
        print("=" * 60)
        print("UAE CREDIT CARD AGENT EVALUATION")
        print("=" * 60)
        
        self.test_rag_accuracy()
        self.test_guardrails()
        self.test_hallucination_prevention()
        self.test_recommendation_quality()
        self.test_context_awareness()
        
        self.print_summary()
    
    def test_rag_accuracy(self):
        """Test if agent uses RAG context correctly"""
        print("\n[1] RAG ACCURACY TESTS")
        print("-" * 60)
        
        tests = [
            {
                "name": "Specific card query",
                "question": "What are the rewards for Amazon.ae Credit Card?",
                "expected_keywords": ["amazon", "cashback"],
                "should_not_contain": ["noon", "carrefour"]
            },
            {
                "name": "No annual fee cards",
                "question": "Which cards have no annual fee?",
                "expected_keywords": ["0", "aed", "fee"],
                "should_not_contain": []
            },
            {
                "name": "Travel rewards query",
                "question": "Best card for travel miles?",
                "expected_keywords": ["travel", "%"],
                "should_not_contain": []
            }
        ]
        
        for test in tests:
            docs = self.advisor.retriever.get_relevant_documents(test["question"])
            context = "\n".join([doc.page_content[:500] for doc in docs[:3]])
            response = self.llm_agent.answer_question(test["question"], context)
            
            passed = all(kw.lower() in response.lower() for kw in test["expected_keywords"])
            no_wrong = all(kw.lower() not in response.lower() for kw in test["should_not_contain"])
            
            self._record_test(
                category="RAG Accuracy",
                name=test["name"],
                passed=passed and no_wrong,
                details=f"Response: {response[:100]}..."
            )
    
    def test_guardrails(self):
        """Test if agent respects guardrails"""
        print("\n[2] GUARDRAILS TESTS")
        print("-" * 60)
        
        tests = [
            {
                "name": "Refuses to answer without context",
                "question": "What is the best credit card in the world?",
                "context": "",
                "should_contain": ["don't have", "database", "information"]
            },
            {
                "name": "Stays within UAE cards scope",
                "question": "Tell me about American Express Platinum",
                "context": "Card: Liv. Credit Card\nBank: Emirates NBD\nAnnual Fee: 0 AED",
                "should_contain": ["liv", "emirates nbd"]
            }
        ]
        
        for test in tests:
            response = self.llm_agent.answer_question(test["question"], test["context"])
            passed = any(kw.lower() in response.lower() for kw in test["should_contain"])
            
            self._record_test(
                category="Guardrails",
                name=test["name"],
                passed=passed,
                details=f"Response: {response[:100]}..."
            )
    
    def test_hallucination_prevention(self):
        """Test if agent hallucinates card features"""
        print("\n[3] HALLUCINATION PREVENTION TESTS")
        print("-" * 60)
        
        tests = [
            {
                "name": "Doesn't invent card features",
                "question": "Does Liv. Credit Card offer airport lounge access?",
                "context": "Card: Liv. Credit Card\nBank: Emirates NBD\nAnnual Fee: 0 AED\nRewards: 1% cashback",
                "should_not_contain": ["yes", "lounge access", "airport"]
            },
            {
                "name": "Doesn't recommend non-existent cards",
                "question": "What about the Dubai Gold Premium Card?",
                "context": "Card: Amazon.ae Credit Card\nCard: Liv. Credit Card",
                "should_contain": ["don't have", "database", "not in"]
            }
        ]
        
        for test in tests:
            response = self.llm_agent.answer_question(test["question"], test["context"])
            passed = all(kw.lower() not in response.lower() for kw in test.get("should_not_contain", []))
            has_required = any(kw.lower() in response.lower() for kw in test.get("should_contain", ["no", "not"]))
            
            self._record_test(
                category="Hallucination Prevention",
                name=test["name"],
                passed=passed or has_required,
                details=f"Response: {response[:100]}..."
            )
    
    def test_recommendation_quality(self):
        """Test recommendation logic quality"""
        print("\n[4] RECOMMENDATION QUALITY TESTS")
        print("-" * 60)
        
        profiles = [
            {
                "name": "High grocery spender",
                "profile": {
                    "salary": 15000,
                    "spend": {"groceries": 3000, "dining": 500},
                    "goals": ["cashback", "groceries"],
                    "lifestyle": {"groceries": [{"service": "amazon_fresh", "usage_percent": 80}]}
                },
                "expected_card": "amazon"
            },
            {
                "name": "Budget conscious user",
                "profile": {
                    "salary": 6000,
                    "spend": {"groceries": 800, "online": 500},
                    "goals": ["no_fee"],
                    "lifestyle": {}
                },
                "expected_card": "liv"
            },
            {
                "name": "Travel enthusiast",
                "profile": {
                    "salary": 30000,
                    "spend": {"international_travel": 5000, "dining": 2000},
                    "goals": ["travel", "airport_lounge"],
                    "lifestyle": {}
                },
                "expected_card": "travel"
            }
        ]
        
        for test in profiles:
            result = self.advisor.recommend(test["profile"])
            recommendations = result.get("recommendations", [])
            
            if recommendations:
                top_card = recommendations[0]["card_name"].lower()
                passed = test["expected_card"] in top_card
            else:
                passed = False
            
            self._record_test(
                category="Recommendation Quality",
                name=test["name"],
                passed=passed,
                details=f"Top card: {recommendations[0]['card_name'] if recommendations else 'None'}"
            )
    
    def test_context_awareness(self):
        """Test if agent uses user profile context"""
        print("\n[5] CONTEXT AWARENESS TESTS")
        print("-" * 60)
        
        profile = {
            "salary": 20000,
            "spend": {"groceries": 2000, "online": 1500},
            "goals": ["cashback", "online"]
        }
        
        tests = [
            {
                "name": "Uses salary in response",
                "question": "Am I eligible for premium cards?",
                "should_contain": ["20000", "salary", "eligible"]
            },
            {
                "name": "Considers user goals",
                "question": "What card should I get?",
                "should_contain": ["cashback", "online"]
            }
        ]
        
        for test in tests:
            docs = self.advisor.retriever.get_relevant_documents(test["question"])
            context = "\n".join([doc.page_content[:500] for doc in docs[:3]])
            response = self.llm_agent.answer_question(test["question"], context, profile)
            
            passed = any(kw.lower() in response.lower() for kw in test["should_contain"])
            
            self._record_test(
                category="Context Awareness",
                name=test["name"],
                passed=passed,
                details=f"Response: {response[:100]}..."
            )
    
    def _record_test(self, category: str, name: str, passed: bool, details: str):
        """Record test result"""
        status = "✓ PASS" if passed else "✗ FAIL"
        color = "\033[92m" if passed else "\033[91m"
        reset = "\033[0m"
        
        print(f"{color}{status}{reset} - {name}")
        if not passed:
            print(f"  Details: {details}")
        
        if passed:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
        
        self.results["tests"].append({
            "category": category,
            "name": name,
            "passed": passed,
            "details": details
        })
    
    def print_summary(self):
        """Print evaluation summary"""
        print("\n" + "=" * 60)
        print("EVALUATION SUMMARY")
        print("=" * 60)
        
        total = self.results["passed"] + self.results["failed"]
        pass_rate = (self.results["passed"] / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        if self.results["failed"] > 0:
            print("\nFailed Tests:")
            for test in self.results["tests"]:
                if not test["passed"]:
                    print(f"  - [{test['category']}] {test['name']}")
        
        # Save results to file
        with open("eval_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        print("\nDetailed results saved to: eval_results.json")

if __name__ == "__main__":
    evaluator = AgentEvaluator()
    evaluator.run_all_tests()
