from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
from typing import Optional

# Import your existing agent logic
# Ensure podcast_agent.py (refactored) is in the same directory
from podcast_agent import run_podcast, AudioEngine, ScriptParser, get_ollama_models

app = FastAPI(title="Local Podcast Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Job Store ---
jobs = {}

class GenerateRequest(BaseModel):
    topic: str
    length: str = "short"
    host_name: str = "Host"
    guest_name: str = "Guest"
    model: str = "qwen2.5:0.5b" 

class ManualRequest(BaseModel):
    script: str

def process_podcast_generation(job_id: str, topic: str, length: str, host: str, guest: str, model: str):
    """Background task wrapper"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["message"] = "Starting generation..."
        
        filename = f"podcast_{job_id}.wav"
        
        # We need to handle the output path. run_podcast returns the path.
        output_path = run_podcast(
            topic=topic,
            output_file=filename,
            length=length,
            allow_human_input=False,
            host_name=host,
            guest_name=guest,
            llm_model_name=model
        )
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["message"] = "Podcast generated successfully."
        jobs[job_id]["filename"] = filename
        
    except Exception as e:
        print(f"Job {job_id} failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["message"] = str(e)

@app.get("/")
def read_root():
    return {"status": "Podcast Agent API is running"}

@app.get("/api/models")
def list_models():
    return {"models": get_ollama_models()}

@app.post("/api/generate")
async def generate_endpoint(req: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = uuid.uuid4().hex
    jobs[job_id] = {
        "status": "queued", 
        "message": "Job queued...",
        "filename": None
    }
    
    background_tasks.add_task(
        process_podcast_generation,
        job_id,
        req.topic,
        req.length,
        req.host_name,
        req.guest_name,
        req.model
    )
    
    return {"jobId": job_id, "status": "queued"}

@app.get("/api/status/{job_id}")
def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.post("/api/manual")
async def manual_endpoint(req: ManualRequest):
    # Keep manual synchronous for now, as it sends pre-written text is fast
    try:
        filename = f"manual_{uuid.uuid4().hex[:8]}.wav"
        engine = AudioEngine()
        clips = []
        parsed_lines = ScriptParser.parse(req.script)
        
        idx = 0
        for speaker, text in parsed_lines:
            try:
                clip_path = engine.generate_clip(text, speaker, idx)
                clips.append(clip_path)
                idx += 1
            except Exception as e:
                print(f"Skipping line {idx}: {e}")

        engine.mix_audio(clips, filename)
        return {"filename": filename, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    file_path = f"./{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
