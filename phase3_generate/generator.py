import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Add Phase 2 to path to import retriever
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'phase2_retrieve')))
from retriever import FundRetriever

# Load environment variables from .env in the same directory as this script
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

class FundGenerator:
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("Warning: GROQ_API_KEY not found in environment variables.")
        
        self.llm = ChatGroq(
            temperature=0,
            model_name=model_name,
            groq_api_key=self.api_key
        )
        self.retriever = FundRetriever()
        
        self.system_prompt = (
            "You are the 'Groww Funds Assistant', a helpful and professional financial data assistant. "
            "Your goal is to provide accurate information about mutual funds based on the provided context.\n\n"
            "STRICT CONSTRAINTS:\n"
            "1. Every answer MUST include exactly one clear citation link to a public Groww fund page from the context. This link MUST only appear at the very end of your response.\n"
            "2. REFUSE all opinionated or portfolio questions (e.g., 'Should I buy?', 'Is this good?'). "
            "Reply with: 'I am a facts-only assistant and cannot provide investment advice. For educational resources, please visit the [Groww MF Knowledge Centre](https://groww.in/blog/category/mutual-funds).'\n"
            "3. NO PII: Do not accept or store PAN, Aadhaar, account numbers, OTPs, emails, or phone numbers.\n"
            "4. NO PERFORMANCE CLAIMS: Do not compute or compare returns. Link to official factsheets or provided URLs if asked.\n"
            "5. LENGTH: Your response must be strictly 3 sentences or less (excluding the citation and date).\n"
            "6. PUBLIC SOURCES ONLY: Rely only on the provided context.\n"
            "7. FORMATTING: BOLD ONLY the specific numerical data or facts (e.g., '**₹220.177**', '**1.0%**'). Do not bold entire sentences or paragraphs.\n"
            "8. FOOTER: Your response MUST end with the following format:\n"
            "---\n"
            "**Source:** [Citation Link] • Last updated: {last_updated}\n\n"
            "Do not repeat the link anywhere else.\n"
            "Context:\n{context}"
        )

    def generate_response(self, query):
        # 1. Retrieve relevant data
        docs = self.retriever.retrieve(query, k=2)
        context = "\n".join([d.page_content + f" (Source: {d.metadata['url']})" for d in docs])
        
        # 2. Build prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{query}")
        ])
        
        # 3. Create chain
        chain = prompt | self.llm | StrOutputParser()
        
        # 4. Invoke
        # Extract last_updated from metadata of the first retrieved document
        last_updated = docs[0].metadata.get("last_updated", datetime.now().strftime("%Y-%m-%d")) if docs else datetime.now().strftime("%Y-%m-%d")
        
        response = chain.invoke({
            "context": context,
            "query": query,
            "last_updated": last_updated
        })
        
        return response

if __name__ == "__main__":
    # Quick test
    gen = FundGenerator()
    
    test_queries = [
        "What is the exit load for HDFC Mid Cap Fund?",
        "Should I invest in Tata Small Cap Fund?",
        "What is the NAV of SBI ELSS Tax Saver?"
    ]
    
    for q in test_queries:
        print(f"\nUser: {q}")
        print("-" * 20)
        try:
            print(f"Assistant: {gen.generate_response(q)}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 40)
