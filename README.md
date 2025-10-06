# Podcast Study Notes Generator

> Rapid agent prototyping using Claude Code. Validate whether your AI agent can generate useful study notes from podcast audio in hours, not weeks—before building any production infrastructure.

## Overview

This repository demonstrates **rapid agent prototyping** using the [context engineering framework](https://jxnl.co/writing/2025/09/04/context-engineering-rapid-agent-prototyping/) by Jason Liu. 

## Why This Approach?

This project tests your agent idea's viability **before** building investing any significant engineering work.

Claude Code has a project runner mode (claude -p) that turns any directory into an agent execution environment. It reads a CLAUDE.md file as system instructions and executes workflows using CLI tools you provide. (This is agent agnostic, you can use it with any CLI agent like Cursor's coding agent, etc)

**The core insight:** If Claude Code can't perform your agent tasks with perfect tool access and no constraints, your production version won't either. 

If it works once in this harness, the idea is viable. If it fails consistently, you know what's missing without building any infrastructure.

**What we're testing:**
- ✅ Are the tools intuitive and their error messages helpful?
- ✅ Does the CLAUDE.md specification communicate requirements clearly?
- ✅ What are the token costs and latency for real podcasts?

**What we're NOT building yet:**
- ❌ Web UI or API endpoints
- ❌ Database or persistent storage
- ❌ User authentication
- ❌ Batch processing system

---

## Project Structure

```
podcast-study-notes/
├── CLAUDE.md                    # System instructions (executable specification)
├── tools/                       # Simple CLI wrappers
│   ├── fetch-podcast           # Get episode metadata from Listen Notes
│   ├── download-audio          # Download MP3 file
│   └── transcribe-audio        # Whisper transcription
├── tests/
│   └── test1-short-episode/
│       └── test-scenario-1.py  # Validation: pass/fail assertions
│   └── scenario-2/
│       └── test-scenario-2.py  # Validation: pass/fail assertions

└── [Generated files - gitignored]
    ├── metadata.json           # Episode info
    ├── podcast.mp3             # Audio file
    ├── transcript.txt          # Transcription
    └── study-notes.md          # Final output
```

## Agent Idea Overview

This agent automatically generates detailed study notes from podcast episodes on Listen Notes. It fetches episode metadata, downloads audio, transcribes using OpenAI Whisper, and produces formatted markdown notes in the **study-notes.md** file:

- **Executive Summary** - Quick overview of the episode's key themes
- **Timestamped Key Points** - Organized by topic with specific timestamps
- **Notable Quotes** - Memorable statements from the episode
- **Key Takeaways** - Actionable insights and lessons
- **Resources Mentioned** - Books, tools, and references cited

---

## Prerequisites

- **Python 3.8+** - For Whisper transcription
- **Claude Code CLI** - Install from [docs.claude.com](https://docs.claude.com/en/docs/claude-code)
- **System tools:**
  - `curl` - API requests (pre-installed on most systems)
  - `jq` - JSON parsing
  - `ffmpeg` - Audio processing (required by Whisper)
- **Listen Notes API Key** - [Free tier available](https://www.listennotes.com/api/)

---

## Installation

### 1. Install System Dependencies

**macOS:**
```bash
brew install jq ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install jq ffmpeg
```

**Windows (WSL):**
```bash
sudo apt update && sudo apt install jq ffmpeg
```

### 2. Install Python Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS/WSL
# OR
venv\Scripts\activate     # Windows CMD

# Install Whisper
pip install openai-whisper
```

### 3. Install Claude Code CLI

Follow the [official installation guide](https://docs.claude.com/en/docs/claude-code).

Verify installation:
```bash
claude --version
```

### 4. Get Listen Notes API Key

1. Visit [Listen Notes API](https://www.listennotes.com/api/)
2. Sign up for free account
3. Copy your API key from the dashboard

### 5. Set API Key

```bash
# Add to shell profile for persistence
echo 'export LISTENNOTES_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# Verify
echo $LISTENNOTES_API_KEY
```

### 6. Make Tools Executable

```bash
chmod +x tools/fetch-podcast tools/download-audio tools/transcribe-audio
```

---

## Finding Episode IDs

1. Navigate to any episode page on Listen Notes
2. Search for the podcast episode that you want to test
3. Click ... and select the "Use API to fetch JSON" option

![episode-search](iamges/episode-search.png)

4. Copy the episode ID

![episode-id](iamges/episode-id.png)

5. Add the episode ID to the input file

```bash
# Add episode ID to input file
echo "<your-episode-id>" > episode-url.txt
```

## Usage

```bash
# Execute the workflow
claude -p

# Claude Code will:
# - Read CLAUDE.md system instructions
# - Call fetch-podcast with the episode ID
# - Call download-audio with the audio URL
# - Call transcribe-audio to generate transcript
# - Generate study-notes.md with proper structure
# - Stop when output meets success criteria

# 4. Validate results
python check.py
```

### What You'll Observe

Watch Claude Code in real-time:
- Reading instructions and selecting tools
- Handling errors (e.g., SSL issues, missing files)
- Making decisions about next steps
- Producing the final artifact

**This is the evidence you need:** If it works once, the idea is viable.

### Example Episode IDs for Testing

| Podcast | Episode | ID |
|---------|---------|-----|
| Huberman Lab Essentials| Build Muscle Size, Increase Strength & Improve Recovery | `9d70c706ec3240f3bec2baa69e6a8cd1` |

**Recommendation:** Start with a 30-40 minute episode for fastest validation.

---

## Success Criteria

The `check.py` validation script verifies:

- ✅ `study-notes.md` exists
- ✅ Contains all required sections (Summary, Key Points, Quotes, Takeaways, Resources)
- ✅ Minimum 3 topic sections with descriptive (not generic) headers
- ✅ Minimum 5 timestamps distributed throughout episode
- ✅ Minimum 3 notable quotes with attribution
- ✅ Minimum 3 actionable takeaways

**Binary pass/fail:** Either the output meets specification or it doesn't. No subjective evaluation.

---

## What the Tools Do

### Tool Design Philosophy

Following the blog's guidance: **Tools should be deliberately simple—CLI commands that wrap your actual APIs.**

Each tool:
- Takes clear inputs via command-line arguments
- Outputs structured status messages (`STATUS:`, `OUTPUT_FILE:`, `NEXT_STEP:`)
- Provides helpful error messages that guide next actions
- Exits with proper status codes (0 = success, 1 = error)

### `fetch-podcast`

**Purpose:** Get episode metadata and audio URL from Listen Notes API

**Input:** Episode ID

**Output:** `metadata.json` containing:
- Episode title
- Podcast name
- Duration
- Audio URL
- Publication date

**Error handling:**
- Invalid API key → Shows where to get valid key
- Episode not found → Suggests trying different ID
- Network issues → Guides troubleshooting

### `download-audio`

**Purpose:** Download podcast MP3 file

**Input:** Audio URL (from metadata.json)

**Output:** `podcast.mp3`

**Error handling:**
- URL unreachable → Suggests checking network
- Download incomplete → Shows file size received
- Disk space issues → Reports space needed

### `transcribe-audio`

**Purpose:** Transcribe audio using Whisper

**Input:** Audio file path

**Output:** `transcript.txt`

**Processing time:** ~1 minute per 10 minutes of audio

**Error handling:**
- Whisper not installed → Shows installation command
- SSL certificate issues → Handles automatically
- Audio format issues → Suggests conversion tools

---

## Performance Expectations

| Task | Time (40-min podcast) |
|------|---------------------|
| Fetch metadata | < 5 seconds |
| Download audio | 30-60 seconds |
| Transcription | 3-5 minutes |
| Generate notes | 1-2 minutes |
| **Total workflow** | **5-10 minutes** |

**Token costs:** ~$0.10-0.50 per episode (depending on model and transcript length)

---

## What You Learn from Prototyping

Following the blog's economics of rapid prototyping:

### Tool Design Feedback
- Are tool names intuitive?
- Are error messages helpful?
- What information does Claude need from each tool?

### Instruction Clarity
- Does CLAUDE.md communicate requirements clearly?
- Which parts need examples?
- Where does Claude make wrong assumptions?

### Economic Transparency
- Token costs per episode
- Latency for real-world inputs
- Which operations are expensive

### Failure Modes
- Where do prompts fall short?
- Which edge cases need handling?
- What additional tools would help?

**Key insight:** You discover all this in **hours**, before writing any production code.

---

## Acknowledgments

- **[Jason Liu](https://jxnl.co/)** - Context engineering framework and methodology
- **[Listen Notes API](https://www.listennotes.com/api/)** - Podcast metadata and audio
- **[OpenAI Whisper](https://github.com/openai/whisper)** - Local speech-to-text

---

## The Core Methodology

> "Stop building agent infrastructure before you know if the idea works. Write instructions in English (CLAUDE.md), expose tools as simple CLI commands, create tests with real inputs and concrete success criteria, run `claude -p` and iterate until you get a pass."
>
> — [Context Engineering: Rapid Agent Prototyping](https://jxnl.co/writing/2025/09/04/context-engineering-rapid-agent-prototyping/)

**If Claude Code can't make it work with perfect tool access, your production version won't either. But if you get one passing test, you've proven the concept.**