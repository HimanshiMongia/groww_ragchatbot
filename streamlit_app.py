import streamlit as st
import os
import sys
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
        background-color: #0F1115;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    /* Strictly target chat message content for font size */
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] div,
    .stMarkdown p,
    .stMarkdown div {
        font-size: 15px !important;
        font-weight: 400 !important;
        line-height: 1.5 !important;
    }
    .stChatMessage {
        background-color: #1C2028 !important;
        border-radius: 10px;
        padding: 5px 15px;
        margin-bottom: 5px;
    }
    .stButton button {
        background-color: #00D09C;
        color: white;
        border-radius: 5px;
        border: none;
        font-size: 14px !important;
    }
    .stTextInput input {
        background-color: #1C2028;
        color: white;
        border: 1px solid #2E3440;
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
        st.markdown(message["content"])

# Suggested Questions (Show only if no messages)
if not st.session_state.messages:
    st.markdown("### Suggested Questions")
    suggestions = [
        "What is the NAV of HDFC Mid Cap?",
        "What is the exit load for Tata Small Cap?",
        "What is the risk level of SBI ELSS?"
    ]
    
    for suggestion in suggestions:
        if st.button(f"🔍 {suggestion}", key=suggestion):
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
