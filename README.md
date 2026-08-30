# JARVIS AI 5.0 & Ultron Holographic HUD

A complete next-generation Personal AI Assistant & 3D Holographic HUD system, engineered with clean modular Python architecture, high-speed intent routing, real desktop computer automation, Chrome multi-account profile dispatching, continuous voice recognition, and MediaPipe hand gesture controls.

---

## 🏛️ System Architecture

```
d:/Ultron x jarvis/
├── jarvis/                             # Modular Python AI Backend
│   ├── api/                            # FastAPI REST & WebSocket Server
│   │   ├── server.py                   # Real-time WebSocket (/ws/hud) & REST (/api/chat)
│   │   ├── schemas.py                  # Pydantic data contracts
│   │   └── websocket_manager.py        # Connection manager
│   │
│   ├── core/                           # Core AI Intelligence
│   │   ├── brain.py                    # NLP Intent Router (NVIDIA NIM / Ollama / Gemini / OpenAI)
│   │   ├── agent.py                    # Master autonomous execution coordinator
│   │   ├── planner.py                  # Multi-step task graph planner
│   │   ├── permission_manager.py       # Granular RBAC & security consent engine
│   │   ├── context_manager.py          # Real-time system & user context
│   │   └── conversation.py             # Multi-turn conversation manager
│   │
│   ├── computer/                       # Verified Desktop Automation
│   │   ├── browser_controller.py       # Direct Chrome / Edge / Multi-Account Profile controller
│   │   ├── application_manager.py      # Windows software lifecycle & process management
│   │   ├── keyboard_controller.py      # Input injector with safety bounds
│   │   ├── mouse_controller.py         # Coordinate-free cursor control
│   │   └── computer_controller.py      # Unified coordinator
│   │
│   ├── voice/                          # Multilingual Voice Engine
│   │   ├── speech_to_text.py           # Multilingual STT (English, Hindi, Marathi, Hinglish)
│   │   ├── text_to_speech.py           # Multi-tier TTS (pyttsx3 + Windows SAPI5 fallback)
│   │   ├── listener.py                 # Pause-aware silence detector
│   │   ├── wake_word.py                # Wake word detector ("Jarvis", "Ultron")
│   │   └── speaker.py                  # Direct speaker module export
│   │
│   ├── vision/                         # Computer Vision & Gestures
│   │   ├── screen_reader.py            # Active window OCR & screen capture
│   │   └── gesture_detection.py        # MediaPipe gesture tracking bridge
│   │
│   ├── memory/                         # Persistent & Context Memory
│   │   ├── short_term_memory.py        # In-memory sliding window buffer
│   │   ├── long_term_memory.py         # Persistent structured JSON fact store
│   │   ├── conversation_history.py     # Persistent chat history
│   │   └── user_preferences.py         # Custom user aliases & workflows
│   │
│   ├── internet/                       # Web & Information Retrieval
│   │   ├── web_search.py               # Multi-source search aggregator
│   │   └── research_agent.py           # Multi-source web summarizer
│   │
│   ├── communication/                  # Communication Assistance
│   │   └── messaging.py                # Draft messages with explicit confirmation
│   │
│   ├── tools/                          # Extensible Tool Registry
│   │   ├── base_tool.py                # BaseTool & ToolResult interfaces
│   │   ├── registry.py                 # Singleton ToolRegistry with schema generator
│   │   ├── system_tools.py             # System, browser, tab, and profile tools
│   │   ├── productivity_tools.py       # Memory and time tools
│   │   └── automation_tools.py         # Custom workflow execution tools
│   │
│   ├── config/                         # Configuration & Settings
│   │   ├── settings.py                 # Pydantic BaseSettings loaded from .env
│   │   └── constants.py                # Permission scopes, levels, and canonical mappings
│   │
│   ├── tests/                          # Automated Unit Tests
│   │   └── test_suite.py               # Complete test suite
│   │
│   ├── requirements.txt                # Python package dependencies
│   ├── .env.example                    # Template environment variables
│   └── main.py                         # CLI entrypoint
│
└── ultron-by-sagar-builds-main/        # 3D Holographic UI (Next.js + Three.js)
    ├── components/
    │   ├── JarvisOrb.tsx               # Holographic 3D Core with Web Speech & WebSocket
    │   ├── HudInputBar.tsx             # Zero-lag memoized command bar
    │   ├── HudStatusPanel.tsx          # System telemetry & permissions panel
    │   ├── HudTaskPanel.tsx            # Task planner & tool explorer
    │   ├── HudWaveform.tsx             # Audio-reactive glowing waveform
    │   └── PermissionModal.tsx         # Holographic interactive consent popup
    ├── lib/
    │   ├── orbScene.ts                 # Three.js Shader particle engine
    │   ├── handTracker.ts              # 60FPS MediaPipe hand gesture tracker
    │   └── jarvisSocket.ts             # Auto-reconnecting WebSocket client
    └── app/                            # Next.js App Router
```

---

## 🚀 Quick Start Guide

### 1. Start the Python AI Backend
In the root directory (`d:\Ultron x jarvis`):
```bash
python -m jarvis.main --mode server
```
- API Server runs at: `http://127.0.0.1:8000`
- Interactive WebSocket endpoint: `ws://127.0.0.1:8000/ws/hud`

### 2. Start the Ultron 3D Web HUD
In the frontend directory (`d:\Ultron x jarvis\ultron-by-sagar-builds-main`):
```bash
npm run dev
```
- Open in your desktop browser: **`http://localhost:3000`**

### 3. Cross-Device Access (Mobile & Laptop)
Any phone, tablet, or secondary laptop connected to the same Wi-Fi network can control JARVIS by opening:
👉 **`http://192.168.0.104:3000`**

---

## 🎯 Verified Voice & Text Commands

| Command | Action Performed |
|---|---|
| `"Open YouTube in Chrome"` | Opens live YouTube in Google Chrome |
| `"Open YouTube in Manomay account"` | Opens YouTube in Chrome `Profile 1` |
| `"Open YouTube in College account"` | Opens YouTube in Chrome Somaiya account (`Profile 4`) |
| `"Search YouTube for Avengers"` | Performs real YouTube search in browser |
| `"Search Google for Quantum AI"` | Performs real Google search in browser |
| `"Open Notepad"` / `"Open Calculator"` | Launches Windows desktop applications |
| `"Open a new tab"` / `"Close tab"` | Desktop browser tab controls (`Ctrl+T` / `Ctrl+W`) |
| `"Reopen closed tab"` | Restores previous tab (`Ctrl+Shift+T`) |
| `"Remember that I like Python"` | Saves persistent fact to Long-Term Memory |
| `"What time is it?"` | Returns current system time and speaks aloud |
| `"List Chrome accounts"` | Shows all detected Google accounts & profiles |
| `"Take screenshot"` | Captures screen to timestamped artifact |

---

## 🔒 Granular Security & Permission Control
Safe actions (`app:launch`, `browser:control`, `internet:research`, `screen:read`) are pre-granted for smooth interaction.
Sensitive actions (like sending emails or external messages) trigger the **Holographic Permission Modal** in the HUD with options:
- **Allow Once**
- **Allow For This Session**
- **Always Allow**
- **Deny**

---

## 🧪 Running Unit Tests
```bash
python -m unittest jarvis/tests/test_suite.py
```
*(All 5/5 test suites pass with code 0)*
