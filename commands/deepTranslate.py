import deepl
from discord.ext import commands
import discord
from discord import app_commands
import os

languages = [
    deepl.Language(code="BG", name="Bulgarian"),
    deepl.Language(code="CS", name="Czech"),
    deepl.Language(code="DA", name="Danish"),
    deepl.Language(code="DE", name="German"),
    deepl.Language(code="EL", name="Greek"),
    deepl.Language(code="EN-GB", name="English"),
    deepl.Language(code="ES", name="Spanish"),
    deepl.Language(code="ET", name="Estonian"),
    deepl.Language(code="FI", name="Finnish"),
    deepl.Language(code="FR", name="French"),
    deepl.Language(code="HU", name="Hungarian"),
    deepl.Language(code="ID", name="Indonesian"),
    deepl.Language(code="IT", name="Italian"),
    deepl.Language(code="JA", name="Japanese"),
    deepl.Language(code="KO", name="Korean"),
    deepl.Language(code="NB", name="Norwegian"),
    deepl.Language(code="NL", name="Dutch"),
    deepl.Language(code="PL", name="Polish"),
    deepl.Language(code="PT-PT", name="Portuguese"),
    deepl.Language(code="RO", name="Romanian"),
    deepl.Language(code="RU", name="Russian"),
    deepl.Language(code="SK", name="Slovak"),
    deepl.Language(code="SV", name="Swedish"),
    deepl.Language(code="TR", name="Turkish"),
    deepl.Language(code="ZH", name="Chinese")
]

translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

def mapLang(language: deepl.Language):
    return app_commands.Choice(name=language.name, value=language.code)

class DeepTranslate(commands.Cog, discord.ui.View):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.choices(target_language=[
        mapLang(language) for language in languages
    ])
    async def translate(self ,interaction: discord.Interaction, target_language: app_commands.Choice[str], message: str):
        """Translate"""
        try:
            usage = translator.get_usage + len(message)
            if usage > 500000:
                raise Exception(f"Translator will have reached its limit of 500000 characters by {usage - 500000}")
            await interaction.response.defer()
            result = translator.translate_text(text=message, target_lang=target_language.value)
            send = f"Translated:\n{message}\n\nInto {target_language.name}:\n{result}"

            await interaction.followup.send(send)
            await interaction.followup.send(self.getUsage(), ephemeral=True)
        except Exception as e:
            print(e)

    def getUsage(self):
        usage = translator.get_usage()
        if usage.any_limit_reached:
            return 'Translation limit reached.'
        if usage.character.valid:
            return f"Character usage: {usage.character.count} of {usage.character.limit}"
        if usage.document.valid:
            return f"Document usage: {usage.document.count} of {usage.document.limit}"

async def setup(bot: commands.Bot):
    await bot.add_cog(DeepTranslate(bot))