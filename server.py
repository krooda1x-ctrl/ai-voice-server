from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your_openrouter_key")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "your_deepgram_key")

class ConversationPayload(BaseModel):
    # This matches the schema ElevenLabs uses when initializing agents
    dynamic_variables: dict = {}

# Intercept conversational agent initialization
@app.post("/v1/convai/agents/{agent_id}/initiate-websocket")
async def mock_agent_websocket(agent_id: str):
    # This tells the script where to route its voice traffic
    return {"websocket_url": "wss://://deepgram.com"}

# Fallback endpoint if it falls back to standard text-to-speech
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
    return {"status": "ElevenLabs Agent Proxy Active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
