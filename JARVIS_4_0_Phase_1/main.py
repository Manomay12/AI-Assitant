# ==================================================
# JARVIS 4.0 — Main Entry Point
# Phase 1: Stabilized Foundation
# ==================================================

from core.brain import JarvisBrain
from core.memory import Memory
from tools.computer import ComputerTools
from voice.listener import Listener
from voice.speaker import Speaker

from config.constants import EXIT_PHRASES


def main():

    print("=" * 58)
    print("                    JARVIS 4.0")
    print("              Phase 1 — Stable Foundation")
    print("=" * 58)

    # Initialize all modules
    memory = Memory()
    computer = ComputerTools()

    brain = JarvisBrain(
        memory=memory,
        computer=computer
    )

    listener = Listener()
    speaker = Speaker()

    speaker.speak("JARVIS online. Voice systems are ready.")

    # Main command loop
    while True:

        command = listener.listen()

        if not command:
            continue

        command = command.strip()

        if not command:
            continue

        lower = command.lower()

        # Check for exit before passing to brain
        if lower in EXIT_PHRASES:
            speaker.speak("Shutting down. Goodbye.")
            break

        response = brain.handle(command)

        if response:
            speaker.speak(response)


if __name__ == "__main__":
    main()