import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("BOT_TOKEN")

intents: discord.Intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def load():
    for fileName in os.listdir("./commands"):
        if fileName.endswith(".py"):
            await bot.load_extension(f"commands.{fileName[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())