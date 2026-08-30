# JARVIS 4.0 — Phase 1: Stable Foundation

A modular, voice-controlled personal AI assistant running locally via Ollama.

---

## What's Working

| Feature | Status |
|---|---|
| Voice input (Google Speech Recognition) | ✅ |
| Text-to-speech (pyttsx3) | ✅ |
| Open Chrome, Notepad, Calculator | ✅ |
| Open 10 websites (YouTube, Google, Gmail, etc.) | ✅ |
| Google Search | ✅ |
| YouTube Search | ✅ |
| Tab controls (new, close, next, previous, reopen) | ✅ |
| Window controls (close, minimize, maximize) | ✅ |
| Screenshot | ✅ |
| Natural language routing (watch/play → YouTube, find → Google) | ✅ |
| AI action classifier via Ollama | ✅ |
| Persistent memory (JSON file) | ✅ |
| Time query | ✅ |
| Centralized config (settings.py + constants.py) | ✅ |

---

## Project Structure

```
JARVIS_4_0_Phase_1/
│
├── main.py                  ← Entry point (voice loop)
│
├── config/
│   ├── settings.py          ← All user-configurable values
│   └── constants.py         ← Allowlists, URL maps, keyword sets
│
├── core/
│   ├── brain.py             ← Command router + AI brain
│   └── memory.py            ← Long-term memory (JSON)
│
├── tools/
│   └── computer.py          ← Computer/browser automation
│
├── voice/
│   ├── listener.py          ← Speech recognition
│   └── speaker.py           ← Text-to-speech
│
└── memory/
    └── memories.json        ← Persistent memory storage
```

---

## Setup

### 1. Python 3.11+

```bash
python --version
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If PyAudio fails to install, download the matching wheel from  
> https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio  
> and run: `pip install PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl`

### 4. Start Ollama

Make sure Ollama is running with the llama3.2 model:

```bash
ollama run llama3.2
```

### 5. Configure Chrome profile (if needed)

Open `config/settings.py` and set `CHROME_PROFILE` to match your Chrome profile.  
To find it: open Chrome → address bar → `chrome://version/` → look at "Profile Path" → use the last folder name (e.g. `"Default"` or `"Profile 1"`).

### 6. Run JARVIS

```bash
python main.py
```

---

## Voice Commands

```
help
time
open chrome / open notepad / open calculator
open youtube / open google / open gmail / open github / open chatgpt
search google for <topic>
search youtube for <topic>
watch <something>
find <something>
close tab / new tab / next tab / previous tab / reopen tab
close window / minimize window / maximize window
close chrome
take screenshot
remember <something>
memories
exit
```

---

## Configuration

Edit `config/settings.py` to change:
- Chrome profile
- Ollama model and URL
- Voice rate and volume
- Speech phrase time limit

Edit `config/constants.py` to add:
- New allowed apps
- New allowed websites
- New keyword aliases

---

## Roadmap

| Phase | Description | Status |
|---|---|---|
| 1 | Stable foundation + config system | ✅ Done |
| 2 | Modular action router (split brain.py) | 🔜 Next |
| 3 | Permission management system | ⬜ Planned |
| 4 | Conversation context + improved memory | ⬜ Planned |
| 5 | Multi-step task planning | ⬜ Planned |
| 6 | FastAPI backend | ⬜ Planned |
| 7 | Futuristic web interface | ⬜ Planned |
| 8 | WebSocket real-time connection | ⬜ Planned |
| 9 | Desktop application | ⬜ Planned |
| 10 | Mobile architecture | ⬜ Planned |
| 11 | Multilingual support | ⬜ Planned |
| 12 | Approved learning & automations | ⬜ Planned |
