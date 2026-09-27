from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
import requests
import json
import os

app = FastAPI()

# Using your active, funded OpenRouter Key directly
OPENROUTER_API_KEY = "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"

@app.post("/v1/convai/conversations/get_signed_url")
async def get_signed_url(request: Request):
    return JSONResponse(status_code=200, content={
        "signed_url": "wss://openrouter.ai/api/v1"
    })

@app.post("/v1/convai/agents/{agent_id}/initiate-websocket")
async def mock_agent_websocket(agent_id: str):
    return {"websocket_url": "wss://openrouter.ai/api/v1"}

@app.post("/v1/text-to-speech/{voice_id}")
async def mock_eleven_labs_tts(voice_id: str, request: Request):
    try:
        payload = await request.json()
        text_to_speak = payload.get("text", "Hello")
        
        # Route voice configurations straight through OpenRouter audio processing models
        or_url = "https://openrouter.ai"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        or_payload = {
            "model": "openai/gpt-4o-mini", 
            "messages": [{"role": "user", "content": f"Read this text out loud: {text_to_speak}"}],
            "response_format": { "type": "json_object" }
        }
        
        response = requests.post(or_url, headers=headers, json=or_payload)
        return StreamingResponse(response.iter_content(chunk_size=1024), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "Nights Software & Raze AI Global Bypass Active"}
