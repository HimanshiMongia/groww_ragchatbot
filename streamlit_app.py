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

st.markdown("""
<style>
.product-context {
    background-color: #ffffff;
    padding: 16px 24px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    border-left: 5px solid #00D09C;
    margin-bottom: 12px;
    box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.05);
}

.product-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 4px;
    line-height: 1.2;
}

.product-desc {
    font-size: 0.9rem;
    color: #4b5563;
    font-weight: 500;
    margin-bottom: 12px;
}

.badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.badge {
    background-color: #E6F8F3;
    color: #00D09C;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    border: 1px solid #bbf7d0;
}
</style>

<div class="product-context">
<div class="product-title">AI Investment Assistant: Balancing Helpfulness & Safety</div>
<div class="product-desc">A controlled assistant that explores mutual funds while avoiding unsafe financial advice.</div>

<div class="badge-container">
<span class="badge">Facts Only</span>
<span class="badge">No Advisory Opinions</span>
<span class="badge">Sourced Data</span>
<span class="badge">Helpful & Safe</span>
</div>
</div>
""", unsafe_allow_html=True)

st.divider()

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

# Session State for History and Suggestions
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_suggestions" not in st.session_state:
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
    st.session_state.current_suggestions = random.sample(question_pool, 3)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Generate Assistant Response (if last message is from user)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                user_query = st.session_state.messages[-1]["content"]
                if retriever and generator:
                    response = generator.generate_response(user_query)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Refresh suggestions for the next turn
                    question_pool = [
                        "What is the NAV of HDFC Mid Cap?", "What is the exit load for Tata Small Cap?",
                        "What is the risk level of SBI ELSS?", "What is the minimum SIP for Kotak Multicap?",
                        "Does HDFC Flexi Cap have a lock-in period?", "What is the 1-year return for Motilal Oswal Large and Midcap?",
                        "What is the expense ratio of ICICI Prudential Retirement Fund?", "What is the risk category for Bajaj Finserv Nifty 50?",
                        "What is the current NAV of SBI ELSS Tax Saver?", "What is the exit load for HDFC Flexi Cap?"
                    ]
                    st.session_state.current_suggestions = random.sample(question_pool, 3)
                    st.rerun()
                else:
                    st.error("Tools not ready.")
            except Exception as e:
                st.error(f"Error generating response: {e}")

# Only show suggestions and input if the assistant is not currently thinking (last msg != user)
if not st.session_state.messages or st.session_state.messages[-1]["role"] == "assistant":
    # Suggested Questions Block
    st.markdown("#### Suggested Questions")
    cols = st.columns(len(st.session_state.current_suggestions))
    for idx, suggestion in enumerate(st.session_state.current_suggestions):
        with cols[idx]:
            if st.button(f"{suggestion}", key=f"sug_{suggestion}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                st.rerun()

    # User Input
    if prompt := st.chat_input("Ex: What is the NAV of HDFC Mid Cap?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

# Sidebar with Info
with st.sidebar:
    st.image("https://groww.in/logo-groww.png", width=100)
    st.subheader("Settings")
    st.info("This assistant uses Groww's real-time fund data and Groq LLM.")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        # Reset suggestions on clear
        question_pool = ["What is the NAV of HDFC Mid Cap?", "What is the exit load for Tata Small Cap?", "What is the risk level of SBI ELSS?", "What is the minimum SIP for Kotak Multicap?", "Does HDFC Flexi Cap have a lock-in period?", "What is the 1-year return for Motilal Oswal Large and Midcap?", "What is the expense ratio of ICICI Prudential Retirement Fund?", "What is the risk category for Bajaj Finserv Nifty 50?", "What is the current NAV of SBI ELSS Tax Saver?", "What is the exit load for HDFC Flexi Cap?"]
        st.session_state.current_suggestions = random.sample(question_pool, 3)
        st.rerun()
