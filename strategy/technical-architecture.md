# Technical Architecture

## Overview

Summarizely is a YouTube video summarization platform built for speed and reliability. This document outlines the technical architecture for the MVP and initial scaling phases.

## Core Architecture

```
┌─────────────────┐
│   Browser       │
│  (Next.js)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API Gateway    │
│  (Vercel)       │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────────────┐  ┌─────────────────┐
│   Transcript    │  │  Summarization  │
│   Service       │  │    Service      │
│   (Python)      │  │   (Node.js)     │
└─────────────────┘  └─────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│  YouTube API    │  │   LLM APIs      │
│  (Extraction)   │  │  - Claude       │
└─────────────────┘  │  - OpenAI       │
                     │  - Groq         │
                     └─────────────────┘
         │
         ▼
┌─────────────────────────┐
│     Supabase            │
│  - PostgreSQL DB        │
│  - Cached Summaries     │
│  - Rate Limiting        │
└─────────────────────────┘
```

### Microservices Architecture

1. **Transcript Service** (Python)
   - Extracts YouTube transcripts
   - Deployed as containerized service
   - Single responsibility: transcript extraction

2. **Summarization Service** (Node.js)
   - Handles all LLM interactions
   - Provider agnostic (Claude, OpenAI, Groq)
   - Single responsibility: text summarization

3. **Frontend/API Gateway** (Next.js on Vercel)
   - Orchestrates between services
   - Handles user sessions
   - Serves UI

## Tech Stack

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Deployment:** Vercel
- **Analytics:** Google Analytics, Amplitude
- **Error Tracking:** Sentry

### Backend Services
- **Transcript Service:** Python + FastAPI (containerized)
- **Summarization Service:** Node.js + Express/Fastify (containerized)
- **Database:** Supabase (PostgreSQL)
- **Caching:** Supabase cached_summaries table (later Redis via Upstash)
- **Queue:** QStash (Upstash) for background jobs
- **Authentication:** None for MVP (localStorage), BetterAuth later

### AI/ML
- **Primary LLM:** Claude (Anthropic)
- **Fallbacks:** OpenAI GPT-3.5, Groq
- **Future:** Self-hosted models on Fly.io

## YouTube Extraction Pipeline

### Python-Only Approach

After testing, JavaScript packages for YouTube extraction proved unreliable and outdated. We're using Python exclusively:

**Transcript Service (Python):**
```python
# Containerized Python service
# Uses: youtube-transcript-api (v1.2.2+)
# Pros: Reliable, well-maintained, handles most videos
# Cons: Doesn't work for videos without captions
```

### Extraction Flow
1. Frontend sends YouTube URL to Transcript Service
2. Service extracts video ID and fetches transcript
3. Returns transcript with metadata (duration, language, is_generated)
4. Cache successful extractions for 30 days

### Test Results
- **Success Rate:** 80% (4/5 videos tested)
- **Performance:** 1-2 seconds average extraction time
- **Limitations:** Cannot extract from videos without captions

## Database Schema

### Core Tables

```sql
-- Main summaries table
summaries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  youtube_url TEXT NOT NULL,
  youtube_id TEXT NOT NULL,
  video_title TEXT NOT NULL,
  video_duration INTEGER, -- seconds
  thumbnail_url TEXT,
  channel_name TEXT,
  summary_content JSONB NOT NULL, -- Structured summary data
  summary_style TEXT DEFAULT 'comprehensive',
  created_at TIMESTAMP DEFAULT NOW(),
  ip_address INET, -- for rate limiting
  view_count INTEGER DEFAULT 0,
  share_count INTEGER DEFAULT 0
)

-- Cached summaries for faster retrieval
cached_summaries (
  video_id TEXT PRIMARY KEY,
  summary_style TEXT,
  summary_content JSONB,
  transcript TEXT,
  created_at TIMESTAMP,
  expires_at TIMESTAMP -- 30 days from creation
)

-- Rate limiting (MVP - will move to Redis later)
rate_limits (
  ip_address INET PRIMARY KEY,
  daily_count INTEGER DEFAULT 0,
  last_reset TIMESTAMP DEFAULT NOW()
)
```

## API Design

### Service Endpoints

#### Transcript Service (Python - Port 8000)

**POST /extract**
```json
// Request
{
  "url": "https://youtube.com/watch?v=..."
}

// Response
{
  "success": true,
  "video_id": "...",
  "transcript": "full transcript text",
  "duration": 123.45,
  "language": "en",
  "is_generated": false
}
```

#### Summarization Service (Node.js - Port 8001)

**POST /summarize**
```json
// Request
{
  "text": "transcript text...",
  "provider": "claude", // optional
  "style": "comprehensive" // optional
}

// Response
{
  "summary": {
    "overview": "...",
    "keyPoints": ["..."],
    "details": ["..."],
    "takeaways": ["..."]
  },
  "provider_used": "claude",
  "tokens_used": 1234
}
```

#### Frontend API Gateway (Next.js)

**POST /api/summarize**
```typescript
// Orchestrates between services
// 1. Calls Transcript Service
// 2. Calls Summarization Service
// 3. Stores in database
// 4. Returns complete response
```

## Caching Strategy

### Cache Levels

1. **Database Cache** (Supabase)
   - Key: `${youtube_id}:${style}:${version}`
   - Duration: 30 days
   - Store: Full summary + transcript

2. **Future: Redis Hot Cache** (Upstash)
   - Most viewed summaries
   - Duration: 24 hours
   - Instant retrieval

### Cache Flow
1. Check cache before extraction
2. Return cached if exists and not expired
3. Generate new if not cached
4. Store in cache after generation

## Rate Limiting

### MVP Approach
- **Limit:** 3 summaries per IP per day
- **Storage:** Supabase rate_limits table
- **Reset:** Rolling 24-hour window
- **Bypass:** None for MVP (paid tiers later)

### Implementation
```typescript
// Check on each request
if (dailyCount >= 3) {
  return { 
    error: "Daily limit reached",
    upgradeUrl: "/pricing" 
  }
}
```

## Security Considerations

### MVP Security
- Input validation (valid YouTube URLs only)
- Rate limiting by IP
- Parameterized queries (SQL injection prevention)
- CORS configuration
- API timeout limits (10s max)

### Future Security
- API keys for heavy users
- DDoS protection (Cloudflare)
- Content moderation for public summaries
- GDPR compliance for EU users

## Deployment Strategy

### Environments
- **Development:** Local Next.js
- **Staging:** Vercel Preview deployments
- **Production:** Vercel production

### CI/CD
1. Push to main → Auto deploy to production
2. PR → Preview deployment
3. Manual testing checklist before deploy

## Monitoring & Observability

### Key Metrics
- Summary generation time (target: <5s)
- Extraction success rate (target: >95%)
- API error rate (target: <1%)
- Daily active users
- Summaries per user
- Share rate

### Monitoring Tools
- **Performance:** Vercel Analytics
- **Errors:** Sentry
- **Usage:** Amplitude
- **Uptime:** Vercel built-in

## Scaling Considerations

### Phase 1 (MVP - 0-1K users)
- Everything on Vercel
- Single database
- No queues needed

### Phase 2 (1K-10K users)
- Add Redis caching
- Implement queue for batch processing
- Add CDN for share pages

### Phase 3 (10K+ users)
- Separate summarization service (Fly.io)
- Multiple LLM providers with smart routing
- Database read replicas
- Full microservices architecture

## Cost Optimization

### Strategies
1. Cache aggressively (same video = same summary)
2. Use GPT-3.5/Claude Haiku for first pass
3. Upgrade to GPT-4/Claude Opus on request
4. Implement smart rate limits
5. Batch similar requests

### Cost Projections (Monthly)
- Vercel: $20 (Pro plan)
- Supabase: $25 (Pro plan)
- Claude API: ~$50 (1000 summaries @ $0.05 each)
- Domain: Already paid
- **Total:** <$100/month until 1K daily users

## Development Workflow

### Local Development
```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Add: CLAUDE_API_KEY, SUPABASE_URL, SUPABASE_ANON_KEY

# Run development server
npm run dev
```

### Testing Strategy
- Manual testing for MVP
- E2E tests for critical path (URL → Summary)
- Load testing before launch

## Technical Debt Acceptance

For MVP speed, we're accepting:
1. No auth system (localStorage only)
2. Basic rate limiting (IP only)
3. Single summary style
4. English only
5. No background jobs
6. Minimal error handling

These will be addressed post-launch based on user feedback.

## Success Criteria

Technical success for Week 1:
- [ ] <5 second summary generation
- [ ] 95%+ extraction success rate
- [ ] Zero downtime during launch
- [ ] <$100 spent on infrastructure
- [ ] 100+ summaries generated

## Next Steps

1. Test YouTube extraction methods
2. Set up Supabase database
3. Create API endpoints
4. Build frontend
5. Deploy to Vercel
6. Test with friends
7. Launch!