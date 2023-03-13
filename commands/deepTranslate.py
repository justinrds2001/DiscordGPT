import deepl
from discord.ext import commands
import os

class DeepTranslate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

    @commands.command()
    async def translate(self, ctx, *args):
        """Translate"""
        result = self.translator.translate_text("Hello, world!", target_lang="FR")
        await ctx.send(result)
        await ctx.send(self.getUsage())

    def getSourceLang(self):
        print("Source languages:")
        for language in self.translator.get_source_languages():
            print(f"{language.name} ({language.code})")  # Example: "German (DE)"

    def getTargetLang(self):
        print("Target languages:")
        for language in self.translator.get_target_languages():
            if language.supports_formality:
                print(f"{language.name} ({language.code}) supports formality")
                # Example: "Italian (IT) supports formality"
            else:
                print(f"{language.name} ({language.code})")
                # Example: "Lithuanian (LT)"

    def getUsage(self):
        usage = self.translator.get_usage()
        if usage.any_limit_reached:
            return 'Translation limit reached.'
        if usage.character.valid:
            return f"Character usage: {usage.character.count} of {usage.character.limit}"
        if usage.document.valid:
            return f"Document usage: {usage.document.count} of {usage.document.limit}"

async def setup(bot: commands.Bot):
    await bot.add_cog(DeepTranslate(bot))