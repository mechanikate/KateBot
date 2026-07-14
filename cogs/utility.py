import discord

from discord import app_commands
from discord.ext import commands

SYNC_SLASH_MESSAGE = "!!!syncslash"
OWNER_ID = 292043731237076992

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if(message.content == SYNC_SLASH_MESSAGE and message.author.id == OWNER_ID):
            print("* syncing slash commands...")
            await self.bot.tree.sync()
            print("\\--> [PASS] synced")
async def setup(bot):
    await bot.add_cog(Utility(bot))
