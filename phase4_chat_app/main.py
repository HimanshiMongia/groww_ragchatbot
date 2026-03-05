import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# Add Phase 3 to path to import generator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'phase3_generate')))
from generator import FundGenerator

app = FastAPI(title="Groww Chatbot API")

# Initialize the generator
generator = FundGenerator()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

# Serve standard static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/status")
async def get_status():
    return {
        "status": "online",
        "funds_loaded": len(generator.retriever.documents),
        "data_file_exists": os.path.exists(generator.retriever.data_file_path),
        "last_updated_sample": generator.retriever.documents[0].metadata.get("last_updated") if generator.retriever.documents else "None"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        res = generator.generate_response(req.query)
        return ChatResponse(response=res)
    except Exception as e:
        return ChatResponse(response=f"Error processing your request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    host = "0.0.0.0" if os.getenv("PORT") else "127.0.0.1"
    # Pass 'app' directly to avoid module path issues when running from root
    uvicorn.run(app, host=host, port=port)
