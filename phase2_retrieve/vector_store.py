import json
import os
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpointEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Paths
PHASE1_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "phase1_ingest")
DATA_FILE = os.path.join(PHASE1_DIR, "sample_fund_data.json")
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found. Please run Phase 1 ingest first.")
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def create_documents(data):
    documents = []
    for entry in data:
        # Create a descriptive text for embedding
        content = (
            f"Mutual Fund: {entry['fund_name']}. "
            f"Current NAV: {entry['nav']}. "
            f"Expense Ratio: {entry['expense_ratio']}. "
            f"Exit Load: {entry['exit_load']}. "
            f"Minimum SIP: {entry['min_sip']}. "
            f"Risk Level: {entry['risk']}. "
            f"One Year Return: {entry['one_year_return']}. "
            f"Lock-in Period: {entry['lock_in']}."
        )
        
        # Metadata for filtering
        metadata = {
            "fund_name": entry["fund_name"],
            "url": entry["url"],
            "risk": entry["risk"],
            "lock_in": entry["lock_in"],
            "last_updated": entry.get("last_updated", "N/A")
        }
        
        documents.append(Document(page_content=content, metadata=metadata))
    return documents

def build_vector_store():
    data = load_data()
    if not data:
        return
    
    documents = create_documents(data)
    
    # Initialize API-based embedding model for Vercel/serverless
    print("Initializing embedding model (HuggingFace API)...")
    # Note: Requires HUGGINGFACEHUB_API_TOKEN or GROQ_API_KEY if using Groq embeddings
    embeddings = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("GROQ_API_KEY") 
    )
    
    # Create Chroma DB
    print(f"Building Chroma DB at {DB_DIR}...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print("Vector store built successfully.")
    return vectorstore

if __name__ == "__main__":
    build_vector_store()
