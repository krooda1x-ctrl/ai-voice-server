from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Hardcoded active API keys
OPENROUTER_API_KEY = "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"
DEEPGRAM_API_KEY = "a5fe63c9bb493a745b6256d0321ac5f35fc03bf0"

# Handshake endpoint for Raze_NPCAI conversation initiation
@app.post("/v1/convai/conversations/get_signed_url")
async def get_signed_url(request: Request):
    return JSONResponse(status_code=200, content={
        "signed_url": "wss://://deepgram.com"
    })

# Fallback initialization endpoint for Conversational AI agents
@app.post("/v1/convai/agents/{agent_id}/initiate-websocket")
async def mock_agent_websocket(agent_id: str):
    return {"websocket_url": "wss://://deepgram.com"}

# Text-to-speech engine fallback
@app.post("/v1/text-to-speech/{voice_id}")
async def mock_eleven_labs_tts(voice_id: str, payload: dict):
    try:
        text_to_speak = payload.get("text", "Hello")
        dg_url = "https://deepgram.com" 
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }
        dg_response = requests.post(dg_url, headers=headers, json={"text": text_to_speak}, stream=True)
        return StreamingResponse(dg_response.iter_content(chunk_size=1024), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "Proxy Connection Fully Authenticated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
