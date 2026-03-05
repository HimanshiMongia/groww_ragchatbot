import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Paths
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

class FundRetriever:
    def __init__(self):
        if not os.path.exists(DB_DIR):
            raise Exception("Vector store not found. Please run vector_store.py first.")
        
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(
            persist_directory=DB_DIR,
            embedding_function=self.embeddings
        )

    def retrieve(self, query, k=3):
        """
        Performs semantic search to find relevant fund data.
        """
        results = self.vectorstore.similarity_search(query, k=k)
        return results

if __name__ == "__main__":
    # Quick test
    try:
        retriever = FundRetriever()
        query = "What is the exit load for HDFC Mid Cap?"
        docs = retriever.retrieve(query)
        
        print(f"\nQuery: {query}")
        print("-" * 20)
        for i, doc in enumerate(docs):
            print(f"Result {i+1}:")
            print(doc.page_content)
            print(f"Source: {doc.metadata['url']}")
            print("-" * 10)
    except Exception as e:
        print(e)
        print("Tip: Make sure to run 'python phase2_retrieve/vector_store.py' first.")
