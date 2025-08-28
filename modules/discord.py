"""Discord bot module."""

import asyncio

try:
    import discord
except Exception:  # pragma: no cover - library may be missing
    discord = None

from .catch import CatchMemory

class RequestBot(discord.Client):
    def __init__(self, memory: CatchMemory, **kwargs):
        super().__init__(**kwargs)
        self.memory = memory

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!req'):
            content = message.content[4:].strip()
            self.memory.remember(message.author.name, content)
            await message.channel.send("Request noted.")

async def run_bot(token: str, memory: CatchMemory):
    if discord is None:
        print("discord.py not installed; bot will not run.")
        return
    bot = RequestBot(memory=memory, intents=discord.Intents.default())
    try:
        await bot.start(token)
    except Exception as e:
        print(f"Discord bot failed: {e}")

def start_bot(token: str, memory: CatchMemory):
    if not token or token == 'YOUR_DISCORD_TOKEN':
        print("Discord token missing; bot not started.")
        return
    asyncio.run(run_bot(token, memory))
