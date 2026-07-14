import discord, datetime, re

from discord import app_commands
from discord.ext import commands

MESSAGE_LOG_BACKUP_CHANNEL_ID = 1410220669773287486 # channel to backup message log deletions
DO_NOT_TRACK_IDS = [432610292342587392, 1307052801687420981, 1211781489931452447] # don't track these users for message modifications (mudae, dyno, wordle)
TRACKING_SERVERS = {1084421458819829841: 1380937180628783254}


fix_spoilers = lambda text: text + "||" if text.count("||") % 2 == 1 else text # add || to end of message if it's unbalanced (this will mess up but it saves people from being spoiled)
fix_tags = lambda text: fix_spoilers(text).replace("*", "\\*").replace("`", "\\`").replace("_", "\\_").replace("-", "\\-")
remove_spoilers = lambda text: re.sub(r"(\|\|)|( )", "", text) # remove all spoilers AND SPACES from message to get its uniqueness if edited

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def should_skip_log(self, message=None, after=None): # check if bot should skip logging this edit/deletion
        should_skip = (message is not None and after is not None and message.content == "" and after.content != "")
        should_skip = should_skip or (message.author.id in DO_NOT_TRACK_IDS) 
        should_skip = should_skip or (message.guild.id not in TRACKING_SERVERS.keys())
        return should_skip

    async def message_deletion(self, message=None, after=None): # message deletion event
        if(message.author.id == self.bot.user.id and message.channel.id in TRACKING_SERVERS.values()):
            channel = await self.bot.fetch_channel(MESSAGE_LOG_BACKUP_CHANNEL_ID)
            await channel.send(embed=message.embeds[0])
            return
        if(self.should_skip_log(message,after)):
            return
        deletion_log_channel = await self.bot.fetch_channel(TRACKING_SERVERS[message.guild.id])
        embed = discord.Embed(color=0xaa0000) # set up embed with red color
        embed.set_author(name="Message deletion from OP "+message.author.name, icon_url=message.author.avatar.url) # Set pfp icon for OP of message
        embed.add_field(name="", value=message.content+"\n\n[**Click to jump to message!**]("+message.jump_url+")")
        embed.timestamp = datetime.datetime.now(datetime.UTC)
        await deletion_log_channel.send(embed=embed)

    async def message_edit(self, message=None, after=None): # message edit event
        if(remove_spoilers(message.content) == remove_spoilers(after.content) or self.should_skip_log(message,after)): # sometimes the bot bugs and detects edits when there are none, so we check here
            return 
        deletion_log_channel = await self.bot.fetch_channel(TRACKING_SERVERS[message.guild.id])
        embed = discord.Embed(color=0xaaaa00) # set up embed with yellow color
        embed.set_author(name="Message revision by "+message.author.name, icon_url=message.author.avatar.url)
        embed.add_field(name="", value="**Before**\n"+fix_tags(message.content)+"\n\n**After**\n"+fix_tags(after.content)+"\n\n[**Click to jump to message!**]("+message.jump_url+")")
        embed.timestamp = datetime.datetime.now(datetime.UTC)
        await deletion_log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.message_deletion(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.message_edit(before, after)

async def setup(bot):
    await bot.add_cog(Logging(bot))
