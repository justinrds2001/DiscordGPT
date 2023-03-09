import openai
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatRecord import Record
from discord.ext import commands

class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Gpt is ready')

    @commands.command()
    async def gpt(self, ctx, *args):
        record = Record.get_instance()
        # get channel id
        channelId = ctx.channel.id
        # add message to record
        record.add_message(channelId, ' '.join(args))
        # get messages from record
        messages = record.get_record(channelId)
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        print(response)
        # get content property of result
        response = response.choices[0].message.content
        await ctx.send(response)

async def setup(bot: commands.Bot):
    await bot.add_cog(Gpt(bot))