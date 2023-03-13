import discord
import os
from discord import app_commands
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("BOT_TOKEN")

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print("The bot is now running!")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name="kanker", description="gekankerd")
async def self(interaction: discord.Interaction, persoon: str, object: str):
    try:
        await interaction.response.send_message(f"Je kanker {persoon} op een {object}")
    except Exception as e:
        print(e)
        
client.run(token)