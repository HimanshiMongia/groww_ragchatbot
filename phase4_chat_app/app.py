import streamlit as st
import os
import sys
import time
from datetime import datetime

# Add Phase 3 to path to import generator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'phase3_generate')))
from generator import FundGenerator

# Page config
st.set_page_config(page_title="Groww - Investment Assistant", page_icon="📈", layout="centered")

# Custom CSS for Groww aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F9FAFB;
    }
    
    .stApp {
        background-color: #F9FAFB;
    }

    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }

    .suggestion-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border: 1px solid #E5E7EB;
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
        transition: all 0.2s;
    }

    .suggestion-card:hover {
        border-color: #00D09C;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .groww-button {
        background-color: #00D09C;
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 600;
        border: none;
        display: inline-block;
        margin-bottom: 2rem;
        box-shadow: 0 4px 14px 0 rgba(0, 208, 156, 0.39);
    }

    .footer-text {
        text-align: center;
        color: #9CA3AF;
        font-size: 0.85rem;
        margin-top: 2rem;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Input area styling */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid #E5E7EB !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "generator" not in st.session_state:
    with st.spinner("Initializing AI Assistant..."):
        st.session_state.generator = FundGenerator()

# UI Layout
st.image("https://groww.in/groww-logo-270.png", width=120)

st.markdown('<div class="main-header">Hi! I\'m here to help with your investment questions</div>', unsafe_allow_html=True)

# Initial screen shown only when no messages
if not st.session_state.messages:
    st.markdown('<div class="groww-button">+ What do you want to learn today?</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="color: #6B7280; font-weight: 600; margin-bottom: 1rem;">Suggested Questions</div>', unsafe_allow_html=True)
    
    suggestions = [
        "What is the current NAV of HDFC Mid Cap Fund?",
        "What is the exit load for Tata Small Cap Fund?",
        "What is the risk level of SBI ELSS Tax Saver?",
        "What is the 1-year return of Kotak Multicap Fund?"
    ]
    
    for sug in suggestions:
        if st.button(sug, key=sug, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": sug})
            st.rerun()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Ask about mutual funds..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # For real-time feel, we generate then stream
            response = st.session_state.generator.generate_response(prompt)
            
            # Simulate streaming
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"I encountered an error while processing your request: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

st.markdown('<div class="footer-text">Facts-only. No investment advice.</div>', unsafe_allow_html=True)
