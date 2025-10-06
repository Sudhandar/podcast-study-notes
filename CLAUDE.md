# Podcast Study Notes Generator

## Mission
Given a podcast episode URL from Listen Notes, produce comprehensive study notes with time-stamped highlights in markdown format.

## Execution Flow
1. Use `fetch-podcast <episode-url>` to get metadata.json and audio URL
2. Use `download-audio <audio-url>` to download podcast.mp3
3. Use `transcribe-audio podcast.mp3` to generate transcript.txt
4. Read transcript.txt and metadata.json files directly
5. Generate study-notes.md with exact formatting requirements below
6. Verify output meets all success criteria
7. Stop when study-notes.md is complete and valid

## Available Tools
- `fetch-podcast <episode-url>` → metadata.json (episode info + audio URL)
- `download-audio <audio-url>` → podcast.mp3 (actual audio file)  
- `transcribe-audio <audio-file>` → transcript.txt (Whisper transcription)

## Success Criteria

Final **study-notes.md** must contain ALL sections below with proper formatting:

### Required Structure:

```markdown
# [Episode Title from metadata]

**Podcast:** [Podcast Name from metadata]  
**Duration:** [X] minutes  
**Date:** [Publication date from metadata]

---

## Executive Summary
[Write 3-4 sentences that capture: (1) main theme, (2) key insight or argument, (3) who should listen and why. Make this compelling enough that someone can decide if they want to listen to the full episode.]

---

## Key Points

### [Descriptive Topic Name - NOT "Topic 1"]
- **[MM:SS]** [Main insight or claim from this part of discussion]
- **[MM:SS]** [Supporting detail, example, or data point]
- **[MM:SS]** [Related concept or implication]

### [Second Descriptive Topic Name]
- **[MM:SS]** [Key point]
- **[MM:SS]** [Supporting detail]
- **[MM:SS]** [Example or implication]

### [Third Descriptive Topic Name]
- **[MM:SS]** [Key point]
- **[MM:SS]** [Detail]

[Continue for minimum 3 topics, maximum 7 topics. Each topic should have 2-4 timestamped points.]

---

## Notable Quotes

> "First impactful quote - choose quotes that are insightful, memorable, or controversial"  
> *Timestamp: MM:SS*

> "Second quote - should represent key ideas or memorable phrasings"  
> *Timestamp: MM:SS*

> "Third quote"  
> *Timestamp: MM:SS*

[Minimum 3 quotes, maximum 5. Quotes must be verbatim from transcript.]

---

## Key Takeaways

- [First actionable insight, practical lesson, or important concept to remember]
- [Second takeaway - what should listeners apply or think about differently?]
- [Third takeaway - summarize a key mental model or framework discussed]

[Minimum 3 takeaways, maximum 5. These should be practical and memorable.]

---

## Resources Mentioned

- [Book title, tool name, website, or specific reference mentioned in episode]
- [Second resource with context if helpful]
- [Any companies, products, or studies cited]

[If no specific resources were mentioned, write: "No specific resources mentioned in this episode"]

---
```

## Timestamp Guidelines

**IMPORTANT:** Whisper's txt output does NOT include timestamps. You must estimate them based on:

1. **Total duration** from metadata.json (duration_min field)
2. **Transcript position**: If a point appears 1/3 through transcript, estimate timestamp as 1/3 of total duration
3. **Distribution**: Spread timestamps throughout episode (don't cluster all at beginning)
4. **Format**: Use MM:SS for episodes under 60 minutes (e.g., 08:45, 23:12, 51:30)

**Calculation approach:**
- Count approximate position in transcript (beginning/early/middle/late/end)
- Beginning = 0-20% of duration
- Early = 20-40%  
- Middle = 40-60%
- Late = 60-80%
- End = 80-100%

## Quality Standards

### Topic Headers
- Must be specific and descriptive (e.g., "The Role of Dopamine in Motivation" NOT "Topic 1" or "Neuroscience Discussion")
- Should reflect actual content discussed
- Should help reader navigate to sections of interest

### Executive Summary
- Must be compelling and informative
- Should answer: What is this about? What's the key insight? Who should care?
- Should be dense with information, not generic

### Quotes
- Must be exact text from transcript
- Choose impactful, memorable, or controversial statements
- Avoid generic or obvious quotes

### Takeaways  
- Must be actionable or memorable
- Should synthesize key ideas, not just repeat facts
- Think: "What should someone remember a week later?"

### Resources
- Include full context (e.g., "Deep Work by Cal Newport" not just "Deep Work")
- If URLs mentioned, include them
- Be specific about what was discussed

## Error Recovery

- If `fetch-podcast` fails → verify URL format and API key
- If `download-audio` fails → check network connection, try once more
- If `transcribe-audio` takes >5 minutes → this is normal for longer episodes, be patient
- If transcript quality is poor (lots of [inaudible]) → note this in Executive Summary
- If no clear structure in conversation → organize chronologically with descriptive headers
- If very few resources mentioned → that's okay, be honest in that section

## File Reading Instructions

After transcription completes:
1. Read metadata.json for title, podcast name, duration, date
2. Read transcript.txt for full content
3. Analyze transcript to identify main topics and structure
4. Write study-notes.md with all required sections
5. Double-check all sections are present and properly formatted

## Stop Condition

Stop when study-notes.md exists and contains:
- All 6 required sections (Summary, Key Points, Quotes, Takeaways, Resources)
- Minimum content requirements met (3+ topics, 3+ quotes, 3+ takeaways)
- Timestamps distributed throughout episode
- Proper markdown formatting