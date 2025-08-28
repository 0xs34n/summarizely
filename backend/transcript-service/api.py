#!/usr/bin/env python3
"""
Simple FastAPI endpoint for YouTube transcript extraction
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional

app = FastAPI()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptRequest(BaseModel):
    url: str

class TranscriptResponse(BaseModel):
    success: bool
    video_id: Optional[str] = None
    transcript: Optional[str] = None
    duration: Optional[float] = None
    language: Optional[str] = None
    is_generated: Optional[bool] = None
    error: Optional[str] = None

def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats"""
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    elif "youtube.com" in url:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
    return url  # Assume it's already a video ID

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "transcript-extraction-api"}

@app.post("/extract", response_model=TranscriptResponse)
async def extract_transcript(request: TranscriptRequest):
    """
    Extract transcript from a YouTube video URL
    """
    try:
        video_id = extract_video_id(request.url)
        
        # Get transcript using youtube-transcript-api
        api = YouTubeTranscriptApi()
        fetched_transcript = api.fetch(video_id)
        
        # Extract snippets
        snippets = fetched_transcript.snippets
        
        # Combine all text
        full_text = " ".join([snippet.text for snippet in snippets])
        
        # Calculate duration
        if snippets:
            last_snippet = snippets[-1]
            total_duration = last_snippet.start + last_snippet.duration
        else:
            total_duration = 0
        
        return TranscriptResponse(
            success=True,
            video_id=video_id,
            transcript=full_text,
            duration=round(total_duration, 2),
            language=fetched_transcript.language_code,
            is_generated=fetched_transcript.is_generated
        )
        
    except Exception as e:
        return TranscriptResponse(
            success=False,
            video_id=extract_video_id(request.url) if request.url else None,
            error=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)