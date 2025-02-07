




import logging
import os
import re
import anthropic
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from dotenv import load_dotenv
from starlette.responses import StreamingResponse
from services.corrector import correct_turkish_text
from services.summarizer import summarize_text, should_summarize
from services.naturalizer import TurkishTextNaturalizer

# ✅ Load environment variables
load_dotenv()

# ✅ Logging Configuration
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Ensure JSON responses are UTF-8 encoded
@app.middleware("http")
async def force_utf8_middleware(request: Request, call_next):
    response = await call_next(request)
    
    if isinstance(response, StreamingResponse):
        return response  

    body = b"".join([chunk async for chunk in response.body_iterator]) if hasattr(response, 'body_iterator') else b""
    
    return Response(content=body, media_type="application/json; charset=utf-8")

# ✅ Read API key from environment
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("Missing ANTHROPIC_API_KEY in environment variables or .env file.")

# ✅ Initialize Claude Client
client = anthropic.Anthropic(api_key=anthropic_api_key)

# ✅ Initialize Naturalizer
naturalizer = TurkishTextNaturalizer(anthropic_api_key)

# ✅ Define Request Model
class TextRequest(BaseModel):
    text: str
    action: str
    summarize_original: bool = False
    summarize_corrected: bool = False

# ✅ Define POST Route
@app.post("/correct")
async def api_correct_text(req: TextRequest):
    """
    Handles text correction, summarization, and naturalization requests.
    """
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        logging.info(f"📤 Received request: {req.text}")

        if req.action == "correct":
            summary_of_changes, corrected_text, model_reply = correct_turkish_text(req.text)
            return {
                "corrected_text": corrected_text,
                "summary_of_changes": summary_of_changes,
                "debug_full_reply": model_reply
            }

        elif req.action == "summarize":
            if should_summarize(req.text):
                summary = summarize_text(req.text, model_type="claude")
                return {"summary": summary}
            else:
                return {"message": "Text is too short for summarization."}

        elif req.action == "natural_output":
            natural_text = naturalizer.naturalize_text(req.text)
            return {
                "corrected_text": natural_text["corrected_text"],
                "uncertain_words": natural_text["uncertain_words"]
            }

        elif req.action == "summarize_corrected":
            summary_of_changes, corrected_text, model_reply = correct_turkish_text(req.text)
            if should_summarize(corrected_text):
                summary = summarize_text(corrected_text, model_type="llama")
                return {
                    "corrected_text": corrected_text,
                    "summary": summary
                }
            else:
                return {"corrected_text": corrected_text, "message": "Corrected text is too short for summarization."}

        else:
            raise HTTPException(status_code=400, detail="Invalid action.")

    except anthropic.APIError as e:
        logging.error(f"🚨 Anthropic API error: {str(e)}")
        raise HTTPException(status_code=500, detail="Anthropic API error")

    except Exception as e:
        logging.error(f"⚠️ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
