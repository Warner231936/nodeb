"""Discord bot module."""

import asyncio

try:
    import discord
except Exception:  # pragma: no cover - library may be missing
    discord = None

from .catch import CatchMemory


if discord is not None:
    class RequestBot(discord.Client):
        """Listen for messages and forward them for processing."""

        def __init__(self, memory: CatchMemory, handler, **kwargs):
            super().__init__(**kwargs)
            self.memory = memory
            self.handler = handler

        async def on_message(self, message):
            if message.author == self.user:
                return
            content = message.content
            if content.startswith('!req'):
                req_text = content[4:].strip()
                self.memory.remember(message.author.name, req_text)
                await message.channel.send("Request noted.")
            await self.handler(message.author.name, content)
else:  # pragma: no cover - executed only when discord.py missing
    class RequestBot:  # type: ignore
        def __init__(self, *_, **__):
            raise RuntimeError("discord.py not installed")

async def run_bot(token: str, memory: CatchMemory, handler):
    if discord is None:
        print("discord.py not installed; bot will not run.")
        return
    intents = discord.Intents.default()
    intents.message_content = True
    bot = RequestBot(memory=memory, handler=handler, intents=intents)
    try:
        await bot.start(token)
    except Exception as e:
        print(f"Discord bot failed: {e}")

def start_bot(token: str, memory: CatchMemory, handler):
    if not token or token == 'YOUR_DISCORD_TOKEN':
        print("Discord token missing; bot not started.")
        return
    asyncio.run(run_bot(token, memory, handler))
