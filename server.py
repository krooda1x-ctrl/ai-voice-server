from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Configuration (Use your actual environment variables)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your_openrouter_key")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "your_deepgram_key")

class TTSRequest(BaseModel):
    text: str
    model_id: str = "eleven_monolingual_v1" # Mimicking ElevenLabs payload

# Fake ElevenLabs Endpoint that your game script calls
@app.post("/v1/text-to-speech/{voice_id}")
async def mock_eleven_labs_tts(voice_id: str, payload: TTSRequest):
    try:
        # 1. OPTIONAL: If your script only sends text and needs an LLM reply first:
        # (Skip this block if the script already sends the final text to be spoken)
        # response = requests.post(
        #     "https://openrouter.ai",
        #     headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        #     json={"model": "meta-llama/llama-3-70b-instruct", "messages": [{"role": "user", "content": payload.text}]}
        # )
        # text_to_speak = response.json()['choices'][0]['message']['content']
        
        text_to_speak = payload.text 

        # 2. Forward the text to Deepgram for Aura/Flux TTS generation
        # We target Deepgram's ultra-low latency text-to-speech API
        dg_url = "https://deepgram.com" 
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }
        dg_payload = {"text": text_to_speak}
        
        dg_response = requests.post(dg_url, headers=headers, json=dg_payload, stream=True)
        
        if dg_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Deepgram API Error")

        # 3. Stream the raw audio bytes back to the game client exactly like ElevenLabs
        return StreamingResponse(dg_response.iter_content(chunk_size=1024), media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
