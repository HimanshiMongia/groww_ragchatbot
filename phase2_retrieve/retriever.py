import os
import json
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

# Paths
# Use more robust path resolution for serverless environments
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
DATA_FILE = os.path.join(BASE_DIR, "phase1_ingest", "sample_fund_data.json")

class FundRetriever:
    def __init__(self):
        if not os.path.exists(DATA_FILE):
            raise Exception(f"Data file not found at {DATA_FILE}. Please run scraper first.")
        
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.documents = []
        for entry in data:
            content = (
                f"Mutual Fund: {entry['fund_name']}. "
                f"Current NAV: {entry['nav']}. "
                f"Expense Ratio: {entry['expense_ratio']}. "
                f"Exit Load: {entry['exit_load']}. "
                f"Minimum SIP: {entry['min_sip']}. "
                f"Risk Level: {entry['risk']}. "
                f"One Year Return: {entry['one_year_return']}. "
                f"Lock-in Period: {entry['lock_in']}."
            ).lower()
            metadata = {
                "fund_name": entry["fund_name"],
                "url": entry["url"],
                "last_updated": entry.get("last_updated", "N/A")
            }
            self.documents.append(Document(page_content=content, metadata=metadata))
        
        # Initialize BM25 retriever (Keyword-based)
        self.retriever = BM25Retriever.from_documents(self.documents)

    def retrieve(self, query, k=4):
        """
        Performs keyword-based search to find relevant fund data.
        """
        # Lowercase query for better BM25 matching
        query = query.lower()
        self.retriever.k = k
        results = self.retriever.invoke(query)
        return results

if __name__ == "__main__":
    # Quick test
    try:
        retriever = FundRetriever()
        query = "What is the NAV of HDFC Mid Cap?"
        docs = retriever.retrieve(query)
        
        print(f"\nQuery: {query}")
        print("-" * 20)
        for i, doc in enumerate(docs):
            print(f"Result {i+1}:")
            print(doc.page_content)
            print(f"Source: {doc.metadata['url']}")
            print("-" * 10)
    except Exception as e:
        print(f"Error: {e}")
