import openai
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatRecord import Record
from discord.ext import commands

class OpenAi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def chat(self, ctx, *args):
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
            responses = split_message(response)
            for response in responses:
                await ctx.send(response)
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def img(self, ctx, *args):
        message = ' '.join(args)
        try:
            response = await openai.Image.acreate(
                prompt = message,
                n = 1,
                size = "512x512"
            )
            response = response.data[0].url
            await ctx.send(response)
        except Exception as e:
            await ctx.send(e)


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