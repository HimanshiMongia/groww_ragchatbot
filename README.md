An AI-powered investment assistant that provides factual information about mutual funds using Retrieval-Augmented Generation (RAG). The chatbot is designed to look and feel like the Groww app while ensuring data accuracy and compliance with investment advice restrictions.

### 🔗 Deployed Chatbot
**[https://growwragchatbot-git.streamlit.app/](https://growwragchatbot-git.streamlit.app/)**

---

### ⚠️ Disclaimer
This assistant provides factual information about mutual funds using official public sources. 
**It does NOT provide investment advice.** 
Please consult a financial advisor before making investment decisions.

---

## 🚀 Setup Instructions

### Prerequisites
- **Python 3.10+** (tested on 3.13)
- **Groq API Key**: Required for the LLM (Llama 3.3).

### Installation
1. **Clone the repository**:
   ```powershell
   git clone https://github.com/HimanshiMongia/groww_ragchatbot.git
   cd groww_ragchatbot
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment.
   ```powershell
   py -m pip install -r phase4_chat_app/requirements.txt
   ```
   
3. **Configure Environment Variables**:
   Create a `.env` file in `phase3_generate/` and add your Groq API key:
   ```text
   GROQ_API_KEY=your_key_here
   ```

### Running the Application (FastAPI)
Navigate to the chat app directory and start the server:
```powershell
cd phase4_chat_app
py -m uvicorn main:app --host 127.0.0.1 --port 8501 --reload
```
Open [http://127.0.0.1:8501](http://127.0.0.1:8501) in your browser.

---

## 🎯 Scope

### Covered AMCs
The chatbot currently indexes data from the following Asset Management Companies:
- **HDFC** Mutual Fund
- **Tata** Mutual Fund
- **SBI** Mutual Fund
- **Kotak** Mutual Fund
- **Motilal Oswal** Mutual Fund
- **ICICI Prudential** Mutual Fund
- **Bajaj Finserv** Mutual Fund

### Supported Schemes
The assistant provides details for various scheme types, including:
- **Equity**: Mid Cap, Large & Midcap, Flexi Cap, Multicap, Small Cap.
- **ELSS**: Tax Saver funds (with information on the 3-year lock-in).
- **Index Funds**: Nifty 50 Index funds.
- **Retirement Funds**: Pure Equity Plans.

---

## 📊 Data & Sources
The assistant relies on public data from official fund pages. 
- **Source URLs**: A complete list of tracked funds and their original URLs can be found in [source_urls.csv](source_urls.csv).
- **Update Frequency**: Data is refreshed daily via automated GitHub Actions.

---

## ⚠️ Known Limitations

1. **Facts-Only Assistant**: The agent is strictly constrained to prevent investment advice. It cannot answer questions like "Should I buy X?" or "Is Y a good investment?".
2. **Static Knowledge Base**: The RAG system uses a pre-scraped JSON database (`sample_fund_data.json`). Data is current as per the last scrape and may not reflect real-time NAV changes without running the scraper again.
3. **Limited Scheme Coverage**: While many popular funds are indexed, the coverage is restricted to the specific URLs defined in the ingestion phase.
4. **Performance Comparisons**: The assistant avoids performing real-time performance calculations or cross-fund comparisons unless the data is explicitly present in the retrieved context.
5. **No PII/Sensitive Data**: The application does not store or process personal financial data (PAN, account numbers, etc.).

---

## 🛠 Project Structure
- `phase1_ingest`: Data scraping and ingestion logic (Playwright + BeautifulSoup).
- `phase2_retrieve`: Vector database management (ChromaDB + HuggingFace Embeddings).
- `phase3_generate`: LLM response generation (LangChain + Groq).
- `phase4_chat_app`: FastAPI web application and Groww-themed UI.
- `phase5_scheduler`: Placeholder for automated update scheduling.
- `source_urls.csv`: Official public URLs for all indexed mutual funds.
- `sample_qa.md`: Example queries and assistant response documentation.
