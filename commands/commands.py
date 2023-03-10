import discord
from discord.ext import commands
from discord import app_commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def commands(self, interaction: discord.Interaction):
        """List of available commands"""
        embed = discord.Embed(title="Help", description="List of available commands:")
        for cog in self.bot.cogs:
            command_list = ""
            for command in self.bot.get_cog(cog).get_commands():
                if not command.hidden:
                    command_list += f"!{command.name} - {command.help}\n"
            if command_list != "":
                embed.add_field(name=cog, value=command_list, inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))