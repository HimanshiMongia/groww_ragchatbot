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
    }
    .stChatMessage {
        background-color: #1C2028 !important;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .stButton button {
        background-color: #00D09C;
        color: white;
        border-radius: 5px;
        border: none;
    }
    .stTextInput input {
        background-color: #1C2028;
        color: white;
        border: 1px solid #2E3440;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Groww Fund Assistant")
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

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ex: What is the NAV of HDFC Mid Cap?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        if retriever and generator:
            with st.spinner("Thinking..."):
                try:
                    # The generator already uses the retriever internally or we can pass it
                    # Here we use the generator's internal recall logic which uses retrieval
                    response = generator.generate_response(prompt)
                    st.markdown(response)
                    # Add assistant response to history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error generating response: {e}")
        else:
            st.error("Tools not initialized properly. Please check your data and API keys.")

# Sidebar with Info
with st.sidebar:
    st.image("https://groww.in/logo-groww.png", width=100)
    st.subheader("Settings")
    st.info("This assistant uses Groww's real-time fund data and Groq LLM.")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
