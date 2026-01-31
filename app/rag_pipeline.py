import json
import os
import re
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import CHROMA_DB_PATH

def strip_rtf(text):
    """Remove RTF formatting and extract plain text."""
    # Remove RTF header and control words
    text = re.sub(r'\{\\rtf1.*?\\f0\\fs24 \\cf0 ', '', text, flags=re.DOTALL)
    text = re.sub(r'\\[a-z]+\d*\s?', '', text)
    text = re.sub(r'[{}]', '', text)
    text = text.replace('\\\n', '\n').replace('\\', '')
    return text.strip()

def load_cards_data():
    """Load UAE credit cards from JSON file."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "uae_cards.json")
    with open(data_path, "r") as f:
        return json.load(f)

def load_rtf_files():
    """Load additional data from RTF files."""
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    rtf_files = [
        "UAE_credit_cards.rtf",
        "ae_banks_credit_card_urls.rtf", 
        "uae_banks_list.md.rtf"
    ]
    
    documents = []
    for filename in rtf_files:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = strip_rtf(f.read())
                if content:
                    documents.append(Document(
                        page_content=content,
                        metadata={"source": filename, "type": "reference"}
                    ))
    return documents

def create_documents():
    """Convert all data sources into LangChain Documents."""
    documents = []
    
    # Load structured JSON cards
    cards = load_cards_data()
    for card in cards:
        content = f"""
Card: {card['name']}
Bank: {card['bank']}
Annual Fee: {card['annual_fee']} AED
Minimum Salary: {card['min_salary']} AED
Rewards: Groceries {card['rewards']['groceries']}%, Travel {card['rewards']['travel']}%, Fuel {card['rewards']['fuel']}%, Online {card['rewards']['online']}%, Dining {card['rewards']['dining']}%
Best For: {', '.join(card['best_for'])}
Details: {card['notes']}
"""
        doc = Document(
            page_content=content,
            metadata={
                "name": card["name"],
                "bank": card["bank"],
                "annual_fee": card["annual_fee"],
                "min_salary": card["min_salary"],
                "best_for": ", ".join(card["best_for"]),  # Convert list to string
                "source": "uae_cards.json",
                "type": "card"
            }
        )
        documents.append(doc)
    
    # Load RTF files with additional card data
    rtf_docs = load_rtf_files()
    documents.extend(rtf_docs)
    
    return documents

def get_embeddings():
    """Get HuggingFace embeddings (free, no API key needed)."""
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

def setup_vectorstore():
    """Initialize and populate Chroma vector store with all data sources."""
    documents = create_documents()
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", ", ", " "]
    )
    splits = text_splitter.split_documents(documents)
    
    # Create embeddings (FREE - HuggingFace)
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    
    print(f"✓ Vector store created with {len(splits)} document chunks at {CHROMA_DB_PATH}")
    print(f"  - Sources: uae_cards.json + 3 RTF files")
    return vectorstore

def get_cards_retriever():
    """Get retriever for card recommendations."""
    embeddings = get_embeddings()
    
    # Load existing vector store or create new one
    if os.path.exists(CHROMA_DB_PATH):
        vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings
        )
    else:
        vectorstore = setup_vectorstore()
    
    # Retrieve more documents since we have more data sources
    return vectorstore.as_retriever(search_kwargs={"k": 10})
