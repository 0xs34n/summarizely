# Summarizely Backend Services

Microservices architecture for YouTube video summarization.

## Architecture

```
Frontend (Next.js)
    ↓
┌──────────────┐      ┌──────────────┐
│  Transcript  │      │Summarization │
│   Service    │      │   Service    │
│   (Python)   │      │  (Node.js)   │
└──────────────┘      └──────────────┘
```

## Services

### 1. Transcript Service (`/transcript-service`)
- **Purpose:** Extract transcripts from YouTube videos
- **Language:** Python + FastAPI
- **Port:** 8000
- **Endpoint:** POST `/extract`

**Features:**
- Extracts transcripts using youtube-transcript-api
- Returns metadata (duration, language, auto-generated flag)
- 80% success rate (works for videos with captions)
- 1-2 second extraction time

### 2. Summarization Service (`/summarization-service`)
- **Purpose:** Generate summaries using LLMs
- **Language:** Node.js + Express/Fastify
- **Port:** 8001
- **Endpoint:** POST `/summarize`
- **Status:** To be built

**Planned Features:**
- Multiple LLM providers (Claude, OpenAI, Groq)
- Fallback logic between providers
- Different summary styles
- Token usage tracking

## Local Development

### Running Transcript Service
```bash
cd transcript-service
pip install -r requirements.txt
python api.py
# Service runs at http://localhost:8000
```

### With Docker
```bash
cd transcript-service
docker build -t transcript-service .
docker run -p 8000:8000 transcript-service
```

## Testing

### Test Transcript Extraction
```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

## Deployment

Each service can be deployed independently to:
- **Fly.io** - Recommended for production
- **Railway** - Simple GitHub integration
- **Any Docker host** - Using provided Dockerfiles

### Deploy to Fly.io
```bash
cd [service-folder]
flyctl launch
flyctl deploy
```

## Environment Variables

### Transcript Service
None required for basic operation.

### Summarization Service (Coming Soon)
- `CLAUDE_API_KEY`
- `OPENAI_API_KEY`
- `GROQ_API_KEY`

## Architecture Decisions

### Why Microservices?
1. **Independent scaling** - Transcript and summarization have different resource needs
2. **Language flexibility** - Python for extraction, Node.js for API calls
3. **Fault isolation** - One service failing doesn't break the other
4. **Easy updates** - Deploy services independently

### Why Python for Transcripts?
- Best library available (youtube-transcript-api)
- JavaScript alternatives are outdated/unreliable
- Proven 80% success rate in testing

### Why Node.js for Summarization?
- Simple HTTP calls to LLM APIs
- Same ecosystem as frontend (Next.js)
- Fast cold starts
- Easy provider switching

## Next Steps

1. Build Summarization Service
2. Set up Supabase for caching
3. Deploy both services
4. Connect frontend