import streamlit as st
import os
import sys
import random
from datetime import datetime

# Add phase directories to path
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, 'phase2_retrieve'))
sys.path.append(os.path.join(base_dir, 'phase3_generate'))

from retriever import FundRetriever
from generator import FundGenerator

# Page Configuration
st.set_page_config(
    page_title="Groww Fund Assistant",
    page_icon="📈",
    layout="centered"
)

# Custom CSS for Groww aesthetics
st.markdown("""
    <style>
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    /* Force every single element inside a chat message to 15px */
    [data-testid="stChatMessageContent"],
    [data-testid="stChatMessageContent"] * {
        font-size: 15px !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
    }
    /* Ensure bold text stays bold but correct size */
    [data-testid="stChatMessageContent"] strong,
    [data-testid="stChatMessageContent"] b {
        font-weight: 700 !important;
    }
    /* Smaller size for Source and Last Updated */
    .source-footer, .source-footer * {
        font-size: 12px !important;
        opacity: 0.8;
    }
    /* Adaptive chat message background */
    .stChatMessage {
        border-radius: 10px;
        padding: 5px 15px;
        margin-bottom: 5px;
        border: 1px solid rgba(128, 128, 128, 0.1);
    }
    .stButton button {
        background-color: #00D09C !important;
        color: white !important;
        border-radius: 5px;
        border: none;
        font-size: 14px !important;
    }
    /* Allow text input to follow theme */
    .stTextInput input {
        border-radius: 5px;
        font-size: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Groww Fund Assistant")
st.write("Welcome! I'm here to help you with mutual fund data.")
st.info("💡 **Facts-only. No investment advice.**")
st.markdown("Ask me anything about Mutual Funds from Groww!")

# Initialize Retriever and Generator
@st.cache_resource
def get_tools():
    try:
        retriever = FundRetriever()
        generator = FundGenerator()
        return retriever, generator
    except Exception as e:
        st.error(f"Error initializing tools: {e}")
        return None, None

retriever, generator = get_tools()

# Session State for History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to process message
def process_query(query_text):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": query_text})
    
    # Generate and add assistant response
    if retriever and generator:
        try:
            response = generator.generate_response(query_text)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
    else:
        st.session_state.messages.append({"role": "assistant", "content": "Tools not ready."})

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Suggested Questions
st.markdown("### Suggested Questions")
question_pool = [
    "What is the NAV of HDFC Mid Cap?",
    "What is the exit load for Tata Small Cap?",
    "What is the risk level of SBI ELSS?",
    "What is the minimum SIP for Kotak Multicap?",
    "Does HDFC Flexi Cap have a lock-in period?",
    "What is the 1-year return for Motilal Oswal Large and Midcap?",
    "What is the expense ratio of ICICI Prudential Retirement Fund?",
    "What is the risk category for Bajaj Finserv Nifty 50?",
    "What is the current NAV of SBI ELSS Tax Saver?",
    "What is the exit load for HDFC Flexi Cap?"
]

# Randomly pick 3 unique questions for this interaction
current_suggestions = random.sample(question_pool, 3)

for suggestion in current_suggestions:
    if st.button(f"🔍 {suggestion}", key=f"sug_{suggestion}"):
        process_query(suggestion)
        st.rerun()

# User Input
if prompt := st.chat_input("Ex: What is the NAV of HDFC Mid Cap?"):
    process_query(prompt)
    st.rerun()

# Sidebar with Info
with st.sidebar:
    st.image("https://groww.in/logo-groww.png", width=100)
    st.subheader("Settings")
    st.info("This assistant uses Groww's real-time fund data and Groq LLM.")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
