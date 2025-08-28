# YouTube Transcript Service

A simple microservice for extracting YouTube video transcripts.

## Features
- Extract transcripts from any YouTube video with captions
- Returns transcript text, duration, language, and metadata
- Fast API with CORS support for web frontends
- Dockerized for easy deployment

## API Endpoints

### GET /
Health check endpoint

### POST /extract
Extract transcript from YouTube video

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "transcript": "Full transcript text...",
  "duration": 123.45,
  "language": "en",
  "is_generated": false
}
```

## Local Development

### Without Docker
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python api.py
```

Server runs at http://localhost:8000

### With Docker
```bash
# Build the image
docker build -t transcript-service .

# Run the container
docker run -p 8000:8000 transcript-service
```

## Deployment

### Deploy to Fly.io
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch (first time)
flyctl launch

# Deploy
flyctl deploy
```

### Deploy to Railway
1. Push to GitHub
2. Connect repo to Railway
3. Railway auto-detects Dockerfile
4. Deploy!

## Environment Variables
None required for basic operation.

For production, consider adding:
- `ALLOWED_ORIGINS` - CORS origins (default: localhost:3000)
- `PORT` - Server port (default: 8000)

## Limitations
- Only works with videos that have captions
- Auto-generated captions may be poor quality for music videos
- No authentication (add if needed)