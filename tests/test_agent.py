import pytest
from app.rag_pipeline import get_cards_retriever, create_documents
from app.agent import CardAdvisor

def test_retriever_returns_documents():
    """Test that retriever returns relevant documents for travel query."""
    retriever = get_cards_retriever()
    docs = retriever.get_relevant_documents("travel miles airport lounge")
    
    assert len(docs) >= 1, "Should return at least 1 document"
    assert any("travel" in doc.page_content.lower() for doc in docs), "Should contain travel-related cards"

def test_documents_creation():
    """Test that documents are created correctly from JSON."""
    docs = create_documents()
    
    assert len(docs) >= 5, "Should have at least 5 cards"
    assert all(hasattr(doc, 'page_content') for doc in docs), "All docs should have page_content"
    assert all(hasattr(doc, 'metadata') for doc in docs), "All docs should have metadata"

def test_recommendation_structure():
    """Test that recommendations return valid structure."""
    advisor = CardAdvisor()
    
    sample_profile = {
        "salary": 15000,
        "spend": {
            "groceries": 2000,
            "international_travel": 3000,
            "fuel": 500,
            "online": 1000,
            "dining": 1500
        },
        "goals": ["travel", "miles"]
    }
    
    result = advisor.recommend(sample_profile)
    
    assert "recommendations" in result, "Should have recommendations key"
    recommendations = result["recommendations"]
    
    assert 1 <= len(recommendations) <= 3, "Should return 1-3 recommendations"
    
    for rec in recommendations:
        assert "card_name" in rec, "Should have card_name"
        assert "fit_score" in rec, "Should have fit_score"
        assert "reasons" in rec, "Should have reasons"
        assert 0 <= rec["fit_score"] <= 1, "Fit score should be between 0 and 1"
        assert isinstance(rec["reasons"], list), "Reasons should be a list"

def test_chat_turn():
    """Test that chat turn returns a response."""
    advisor = CardAdvisor()
    
    response = advisor.chat_turn("What cards have no annual fee?")
    
    assert isinstance(response, str), "Should return a string"
    assert len(response) > 0, "Response should not be empty"
