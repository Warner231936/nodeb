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
from engage.engagement import should_respond, log_interaction
from engage.database import Database

def start_services(config):
    memory = CatchMemory()
    db = Database(config["database"]["uri"])

    ports = config["ports"]["dispatch"]

    # Start Discord bot
    threading.Thread(target=start_bot, args=(config.get("discord_token"), memory), daemon=True).start()

    # Start placeholder LLMs
    llm_intent = LocalLLM()
    llm_emotion = LocalLLM()
    llm_thoughts = LocalLLM()
    for llm in (llm_intent, llm_emotion, llm_thoughts):
        threading.Thread(target=llm.start, daemon=True).start()

    def process_message(user: str, message: str):
        try:
            intent = analyze_intent(message)
            emotion = analyze_emotion(message)
            if should_respond(user, message, intent, emotion):
                thoughts = summarize(user, intent, emotion, llm_thoughts)
                response = f"{user}: {thoughts}"
                log_interaction(db, user, message, intent, emotion)
                dispatch(response, ports)
        except Exception as e:  # pragma: no cover
            handle_error(e)

    # Example of processing a placeholder message
    threading.Thread(target=process_message, args=("system", "hello"), daemon=True).start()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-gui', action='store_true', help='Run without GUI')
    parser.add_argument('--test', action='store_true', help='Run test mode and exit')
    args = parser.parse_args()

    with open('config.json') as f:
        config = json.load(f)

    start_services(config)

    if not args.no_gui:
        gui = SystemGUI()
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
