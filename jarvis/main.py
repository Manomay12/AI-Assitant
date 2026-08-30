# ==================================================
# JARVIS AI 5.0 — Master Application Entrypoint
# ==================================================

import argparse
import asyncio
import os
import sys
import uvicorn

# Ensure the workspace root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jarvis.config.settings import settings
from jarvis.core.agent import agent
from jarvis.voice.listener import listener
from jarvis.voice.speaker import speaker
from jarvis.voice.wake_word import wake_word_detector


import io
import sys

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def print_banner():
    banner = """
    ==================================================================
        _   _   ___ __   __ ___  ___     _    ___
       | | /_\ | _ \\ \ / /|_ _|/ __|   /_\  |_ _|
    _  | |/ _ \|   / \ V /  | | \__ \  / _ \  | |
   | |_| /_/ \_\_|_\  \_/  |___||___/ /_/ \_\|___|
                 Next-Gen Personal AI Assistant & Holographic HUD
    ==================================================================
    """
    print(banner)
    print(f"    [SYSTEM] Active Provider : {settings.AI_PROVIDER.upper()}")
    print(f"    [SYSTEM] API Host & Port : {settings.HOST}:{settings.PORT}")
    print(f"    [SYSTEM] Platform        : Windows 64-bit")
    print("    ==================================================================\n")


async def run_voice_loop():
    """Continuous voice / wake-word assistant loop."""
    print("[JARVIS] Initializing voice systems...")
    speaker.speak("JARVIS systems online. Ready for command.")

    while True:
        try:
            print("\n[JARVIS] Listening for wake phrase ('Jarvis' or 'Hey Jarvis')...")
            # Listen for wake phrase or direct input
            command = await listener.listen_async()
            if not command:
                continue

            print(f"[USER] {command}")
            response = await agent.process_input(command)
            if response:
                await speaker.speak_async(response)

            if "shutting down" in response.lower() or "goodbye" in response.lower():
                break

        except (KeyboardInterrupt, asyncio.CancelledError):
            print("\n[JARVIS] Voice loop terminated.")
            break
        except Exception as e:
            print(f"[JARVIS ERROR] {e}")


async def run_text_console():
    """Interactive text console loop."""
    print("[JARVIS] Text command console ready. Type your command (or 'exit' to quit):\n")
    while True:
        try:
            user_input = input("[YOU] > ").strip()
            if not user_input:
                continue

            response = await agent.process_input(user_input)
            print(f"[JARVIS] > {response}\n")

            if user_input.lower() in ("exit", "quit", "shutdown"):
                break
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break


def run_api_server():
    """Launch the FastAPI server with WebSocket support for the HUD interface."""
    uvicorn.run(
        "jarvis.api.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
        log_level="info",
    )


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="JARVIS AI Next-Gen Assistant")
    parser.add_argument(
        "--mode",
        choices=["server", "voice", "text", "all"],
        default="server",
        help="Execution mode: 'server' (API/HUD backend), 'voice' (interactive voice), 'text' (CLI), 'all'",
    )
    args = parser.parse_args()

    if args.mode == "text":
        asyncio.run(run_text_console())
    elif args.mode == "voice":
        asyncio.run(run_voice_loop())
    elif args.mode == "server":
        print(f"[JARVIS] Starting FastAPI REST and WebSocket Server on http://{settings.HOST}:{settings.PORT}")
        run_api_server()
    elif args.mode == "all":
        print("[JARVIS] Launching unified server and background voice monitor...")
        # Start server as primary process
        run_api_server()


if __name__ == "__main__":
    main()
