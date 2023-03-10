import openai
from discord.ext import commands

class Img(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    await bot.add_cog(Img(bot))