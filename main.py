"""Main entry point launching GUI and background services."""

import argparse
import json
import threading
import time

from modules.gui import SystemGUI
from modules.discord import start_bot
from modules.intent import analyze_intent
from modules.emotions import analyze_emotion
from modules.llm import LocalLLM
from modules.thoughts import summarize
from modules.catch import CatchMemory
from modules.fallback import handle_error
from modules.dispatch import dispatch
from modules.reflect import reflect
from engage.engagement import should_respond, log_interaction
from engage.database import Database

def start_services(config):
    memory = CatchMemory()
    db_cfg = config["database"]
    db = Database(db_cfg["uri"], db_cfg.get("name"))

    ports = config["ports"]["dispatch"]

    # Start placeholder LLMs
    llm_intent = LocalLLM()
    llm_emotion = LocalLLM()
    llm_thoughts = LocalLLM()
    llm_reflect = LocalLLM()
    for llm in (llm_intent, llm_emotion, llm_thoughts, llm_reflect):
        threading.Thread(target=llm.start, daemon=True).start()

    def process_message(user: str, message: str):
        try:
            if memory.gui:
                memory.gui.log_event(f"msg:{user}")
            intent = analyze_intent(message)
            emotion = analyze_emotion(message)
            memory.enqueue(user, message, intent, emotion)
            if should_respond(user, message, intent, emotion):
                thoughts = summarize(user, intent, emotion, llm_thoughts)
                reflection = reflect(user, message, llm_reflect)
                response = f"{user}: {thoughts} | reflect: {reflection}"
                log_interaction(db, user, message, intent, emotion)
                dispatch(response, ports)
                if memory.gui:
                    memory.gui.log_event(f"dispatch:{user}")
                    memory.gui.display_output(response)
        except Exception as e:  # pragma: no cover
            handle_error(e)

    # Start Discord bot
    threading.Thread(
        target=start_bot,
        args=(config.get("discord_token"), memory, process_message),
        daemon=True,
    ).start()

    # Example of processing a placeholder message
    threading.Thread(target=process_message, args=("system", "hello"), daemon=True).start()

    return memory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-gui', action='store_true', help='Run without GUI')
    parser.add_argument('--test', action='store_true', help='Run test mode and exit')
    args = parser.parse_args()

    with open('config.json') as f:
        config = json.load(f)

    memory = start_services(config)

    if not args.no_gui:
        gui = SystemGUI(memory)
        memory.bind_gui(gui)
        gui.run()

    if args.test:
        time.sleep(2)
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
