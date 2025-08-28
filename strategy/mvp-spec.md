# MVP Specification

## Overview
**Goal:** Launch the world's best YouTube summarizer in 4 weeks

**Core Value Prop:** Paste a YouTube link, get a beautiful summary in <5 seconds

**Target Users:** Information consumers who watch lots of YouTube content about tech, entrepreneurship, self-development

## User Journey

### 1. Landing Page
**URL:** summarizely.com

**Above the Fold:**
- **Headline:** "2-Hour Podcasts in 30 Seconds"
- **Subheadline:** "Powered by AI that actually understands context"
- **Input field:** Large, centered, with placeholder "Paste any YouTube URL..."
- **CTA Button:** "Summarize Now" (big, green, obvious)
- **Social proof:** "Join 1,000+ people learning 100x faster"

**Below the Fold:**
- Example summaries (3 popular videos)
- How it works (3 steps)
- Testimonials
- FAQ

### 2. Summary Generation
**Input:** YouTube URL
**Process:** 
1. Show loading state with progress messages:
   - "Fetching video details..." (0-1s)
   - "Extracting insights..." (1-3s)
   - "Creating your summary..." (3-5s)
2. Display summary progressively as it generates

**Output:** Beautiful, formatted summary

### 3. Summary Display
**Layout:**
- Video thumbnail and title at top
- Summary content (varied formatting)
- Action buttons below

**Actions:**
- Share (copy link)
- Save (requires account)
- Regenerate (different style)
- Watch original

### 4. Account Creation (Optional)
**Triggered by:** Save, or after 3 summaries
**Simplified flow:** 
- Email only (magic link)
- Or continue with Google
- Skip option available

## Core Features

### 1. Summary Generation

**Input Support:**
- YouTube URLs (all formats)
- YouTube Shorts
- YouTube Live (if has captions)
- Playlist URLs (first video only for MVP)

**Summary Styles:**
```
1. Comprehensive (default) - Your proven CLI format
2. Key Points - Bullet point takeaways
3. ELI5 - Explain like I'm 5
4. Academic - Formal structure
5. Newsletter - Shareable format
```

**Quality Features:**
- Timestamp references
- Key quotes preserved
- Statistical data highlighted
- Action items extracted
- Main takeaways boxed

### 2. Sharing System

**Public Summary Page:**
- Clean URL: summarizely.com/s/[shortcode]
- Shows summary + video embed
- "Summarize More Videos" CTA
- Social meta tags for preview

**Share Options:**
- Copy link
- Twitter ("I just learned X in 30 seconds")
- WhatsApp
- Email

### 3. User Library (Authenticated)

**Features:**
- All summaries saved
- Search summaries
- Filter by date/topic
- Export to Notion/Markdown
- Delete summaries

**Organization:**
- Auto-categorization by topic
- Manual collections/folders
- Favorite summaries
- Recently viewed

### 4. Browser Extension (Chrome)

**Features:**
- One-click summarize on YouTube
- Floating summary sidebar
- Save without leaving YouTube
- Share from YouTube page

**Installation flow:**
- Prompt after 5th summary
- One-click install
- Auto-open YouTube to test

## Technical Requirements

### Frontend

**Stack:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Radix UI components
- Framer Motion (animations)

**Key Pages:**
- `/` - Landing page
- `/s/[id]` - Public summary
- `/library` - User library
- `/settings` - User settings

**Performance:**
- <2s initial load
- <100ms interactions
- Optimistic updates
- Progressive enhancement

### Backend

**Stack:**
- Next.js API routes
- PostgreSQL (Supabase)
- Redis (Upstash) for cache
- OpenAI API for summaries

**Database Schema:**
```sql
users
- id
- email
- created_at
- subscription_tier

summaries
- id
- user_id (nullable)
- youtube_url
- youtube_id
- title
- thumbnail
- duration
- summary_content
- summary_style
- view_count
- created_at

user_sessions
- id
- user_id
- token
- expires_at
```

**API Endpoints:**
- `POST /api/summarize` - Generate summary
- `GET /api/summary/[id]` - Get summary
- `POST /api/auth/login` - Magic link login
- `GET /api/user/summaries` - User's summaries

### YouTube Integration

**Data Extraction (via Transcript Service):**
1. Python microservice using youtube-transcript-api
2. FastAPI endpoint for extraction
3. Returns transcript with metadata
4. Error handling for videos without captions

**Rate Limiting:**
- 10 summaries/minute for free users
- 60 summaries/minute for paid users
- Queue system for high load

### AI Pipeline (via Summarization Service)

**Service Architecture:**
- Node.js microservice for LLM interactions
- Provider-agnostic (Claude, OpenAI, Groq)
- Fallback logic between providers
- Containerized for independent scaling

**Prompting Strategy:**
- Use proven Summarizely CLI prompt as base
- Adjust for different styles
- Include video metadata for context
- Token optimization (<4k per summary)

**Speed Optimizations:**
- Stream responses
- Cache popular video summaries
- Use Claude Haiku for speed, Claude Opus for quality

## Design System

### Brand
- **Primary Color:** Green (#10B981)
- **Secondary:** Dark gray (#1F2937)
- **Accent:** Blue (#3B82F6)
- **Font:** Inter for UI, Merriweather for summaries

### Components
- Cards with subtle shadows
- Smooth animations (250ms)
- Loading skeletons
- Toast notifications
- Responsive grid layouts

## Launch Checklist

### Week 1: Foundation
- [ ] Landing page built
- [ ] Summary generation working
- [ ] Basic database setup
- [ ] YouTube integration complete

### Week 2: Core Features
- [ ] User accounts (magic link)
- [ ] Save summaries
- [ ] Share functionality
- [ ] Public summary pages

### Week 3: Polish
- [ ] Browser extension MVP
- [ ] Mobile responsive
- [ ] Error handling
- [ ] Loading states
- [ ] Analytics setup

### Week 4: Launch Prep
- [ ] Performance optimization
- [ ] Security audit
- [ ] Load testing
- [ ] Documentation
- [ ] Feedback widget

## Success Metrics

### Technical
- <5s summary generation
- 99.9% uptime
- <2% error rate
- <100ms API response

### User
- 50% of visitors try it
- 30% create account
- 20% return within 7 days
- 10% share a summary

## Non-Goals for MVP

**Not doing yet:**
- Mobile apps
- Podcast support
- Article summarization
- Paid subscriptions
- Team features
- API access
- Advanced personalization
- Multiple languages

## Security & Privacy

- No storing YouTube videos
- Summaries deleted after 90 days (free tier)
- GDPR compliant
- Clear privacy policy
- Secure authentication (magic links)
- Rate limiting on all endpoints

## Monitoring

**Tools:**
- Vercel Analytics (performance)
- PostHog (product analytics)
- Sentry (error tracking)
- Uptime Robot (availability)

**Key Alerts:**
- Summary generation >10s
- Error rate >5%
- API quota approaching
- Database connection issues

## Post-Launch Iterations

**Week 5-6:**
- A/B test summary formats
- Implement user feedback
- Add more video sources

**Week 7-8:**
- Premium tier launch
- Referral program
- Email digests

The goal: 1,000 people saying "How did I live without this?" within 30 days.