import discord
from discord import app_commands
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
        if fileName.endswith(".py") and fileName != "music.py":
            await bot.load_extension(f"commands.{fileName[:-3]}")

@bot.event
async def on_ready():
    activity = discord.Game(name="/commands for commands")
    await bot.change_presence(activity=activity)
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)
    print(f"{bot.user.name} is now online!")
    

async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())