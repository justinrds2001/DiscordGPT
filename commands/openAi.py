import openai
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatRecord import Record
from discord.ext import commands
from discord import app_commands
import discord

class OpenAi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def chat(self, interaction: discord.Interaction, message: str):
        """Generate text using OpenAI"""
        try:
            record = Record.get_instance()
            # get channel id
            channelId = interaction.channel_id
            # add the message to record
            record.add_message(channelId, message)
            # get messages from record
            messages = record.get_record(channelId)
            await interaction.response.defer()
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages
            )
            # get content property of result
            response = response.choices[0].message.content
            responses = split_message(response)
            for response in responses:
                await interaction.followup.send(response)
        except Exception as e:
            print(e)
            await interaction.followup.send(e)

    @app_commands.command()
    async def img(self, interaction: discord.Interaction, description: str):
        """Generate an image using DALL-E"""
        try:
            await interaction.response.defer()
            response = await openai.Image.acreate(
                prompt = description,
                n = 1,
                size = "1024x1024"
            )
            
            response = response.data[0].url
            await interaction.followup.send(response)
        except Exception as e:
            await interaction.followup.send(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(OpenAi(bot))

def split_message(msg):
    """
    Splits a message into a list of strings, each containing at most 2000 characters.
    The splitting is done at spaces if possible.
    """
    msgs = []
    curr = ''
    for word in msg.split():
        if len(curr) + len(word) +1 <= 2000:
            curr += ' ' + word if curr else word
        else:
            msgs.append(curr)
            curr = word
    if curr:
        msgs.append(curr)
    return msgs