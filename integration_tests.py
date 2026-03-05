import os
import sys
import json
import unittest
from dotenv import load_dotenv

# Add all phase directories to path
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, 'phase1_ingest'))
sys.path.append(os.path.join(base_dir, 'phase2_retrieve'))
sys.path.append(os.path.join(base_dir, 'phase3_generate'))

from generator import FundGenerator
from vector_store import build_vector_store

class TestRAGIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the environment and vector store before tests."""
        load_dotenv(os.path.join(base_dir, 'phase3_generate', '.env'))
        # Ensure the vector store is built from current sample data
        print("\n[Setup] Building vector store from sample data...")
        build_vector_store()
        cls.generator = FundGenerator()

    def test_nav_query(self):
        """Test if the assistant can correctly retrieve and report NAV."""
        query = "What is the NAV of HDFC Mid Cap Fund?"
        print(f"\n[Test] Query: {query}")
        response = self.generator.generate_response(query)
        print(f"[Response]: {response}")
        
        # Validate content (based on sample_fund_data.json)
        self.assertIn("220.177", response)
        self.assertIn("HDFC Mid Cap", response)
        
        # Validate constraints
        self.assertTrue(len(response.split('.')) <= 5) # Sentences check (approximate)
        self.assertIn("groww.in", response.lower()) # Citation check
        self.assertIn("Last updated from sources:", response) # Footer check

    def test_refusal_opinion(self):
        """Test if the assistant refuses to give investment advice."""
        query = "Is Tata Small Cap Fund a good buy right now?"
        print(f"\n[Test] Query: {query}")
        response = self.generator.generate_response(query)
        print(f"[Response]: {response}")
        
        self.assertIn("investment advice", response.lower())
        self.assertIn("Groww MF Knowledge Centre", response)

    def test_exit_load_query(self):
        """Test if the assistant reports exit load correctly."""
        query = "What is the exit load for SBI ELSS Tax Saver?"
        print(f"\n[Test] Query: {query}")
        response = self.generator.generate_response(query)
        print(f"[Response]: {response}")
        
        # SBI ELSS exit load is "Nil" in our sample
        self.assertIn("Nil", response)
        self.assertIn("SBI ELSS", response)

if __name__ == "__main__":
    unittest.main()
