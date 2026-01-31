from app.agent import CardAdvisor
from app.rag_pipeline import setup_vectorstore
import os

def collect_user_profile():
    """Collect user information via CLI."""
    print("\n" + "="*60)
    print("🏦 UAE Credit Card Recommendation Agent")
    print("="*60 + "\n")
    
    # Salary
    while True:
        try:
            salary = int(input("💰 Your monthly salary (AED): "))
            if salary > 0:
                break
            print("Please enter a valid salary.")
        except ValueError:
            print("Please enter a number.")
    
    # Spending
    print("\n📊 Monthly spending by category (AED):")
    spend = {}
    categories = ["groceries", "international_travel", "domestic_transport", "fuel", "online", "dining"]
    
    for cat in categories:
        display_name = cat.replace("_", " ").title()
        if cat == "international_travel":
            display_name = "International Travel (flights, hotels)"
        elif cat == "domestic_transport":
            display_name = "Local Transport (Careem, RTA, metro)"
            
        while True:
            try:
                amount = int(input(f"  {display_name}: "))
                if amount >= 0:
                    spend[cat] = amount
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a number.")
    
    # Goals
    print("\n🎯 Your goals (e.g., 'travel miles', 'cashback', 'no fees'):")
    goals_input = input("  Enter goals (comma-separated): ")
    goals = [g.strip() for g in goals_input.split(",") if g.strip()]
    
    return {
        "salary": salary,
        "spend": spend,
        "goals": goals
    }

def display_recommendations(result: dict):
    """Display recommendations in a formatted way."""
    print("\n" + "="*60)
    print("✨ TOP 3 RECOMMENDED CARDS FOR YOU")
    print("="*60 + "\n")
    
    recommendations = result.get("recommendations", [])
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['card_name']}")
        print(f"   Fit Score: {rec['fit_score']:.0%}")
        print(f"   Why this card:")
        for reason in rec['reasons']:
            print(f"     • {reason}")
        print(f"   Estimated Value: {rec['estimated_annual_value']}")
        print()

def main():
    """Main CLI loop."""
    
    # Initialize vector store if needed
    if not os.path.exists("./.chroma_db"):
        print("🔧 Setting up vector database (first time only)...")
        setup_vectorstore()
        print()
    
    # Initialize advisor
    advisor = CardAdvisor()
    
    # Collect profile
    profile = collect_user_profile()
    
    # Get recommendations
    print("\n🔍 Analyzing cards for your profile...")
    result = advisor.recommend(profile)
    
    # Display results
    display_recommendations(result)
    
    # Follow-up loop
    print("="*60)
    print("💬 Ask follow-up questions or type 'exit' to quit")
    print("="*60 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "quit", "q"]:
            print("\n👋 Thank you for using UAE Card Advisor!\n")
            break
        
        if not user_input:
            continue
        
        response = advisor.chat_turn(user_input)
        print(f"\nAdvisor: {response}\n")

if __name__ == "__main__":
    main()
