import openai
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatRecord import Record
from discord.ext import commands

class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gpt(self, ctx, *args):
        message = ' '.join(args)
        try:
            record = Record.get_instance()
            # get channel id
            channelId = ctx.channel.id
            # add message to record
            record.add_message(channelId, message)
            # get messages from record
            messages = record.get_record(channelId)

            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages
            )
            # get content property of result
            response = response.choices[0].message.content
            await ctx.send(response)
        except Exception as e:
            await ctx.send(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(Gpt(bot))