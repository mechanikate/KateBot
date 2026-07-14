import discord, json, random

from cogs.tipboard import tipboard_config
from discord import app_commands
from discord.ext import commands
from discord.utils import get as get_reactions

starboard_config = {
    1084421458819829841: {
        "channel": 1376332166622871602,
        "required_reacts": 3,
        "upvote_emoji": "❌",
        "downvote_emoji": "✅",
        "selfreact_upvote_modifier": -1, 
        "selfreact_downvote_modifier": 1
    },
    1384564360592097280: {
        "channel": 1398402612033884344,
        "required_reacts": 1,
        "upvote_emoji": "❌",
        "downvote_emoji": "✅",
        "selfreact_upvote_modifier": -1, 
        "selfreact_downvote_modifier": 1
    }
}
class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.catalogued_messages = {}

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user): 
        message = reaction.message
        starboard_config_entry = starboard_config[message.guild.id]
        if(message.channel.id == tipboard_config[message.guild.id]["channel"] or reaction.emoji not in [starboard_config_entry["upvote_emoji"], starboard_config_entry["downvote_emoji"]]):
            return
        channel_parent = self.bot.get_channel(starboard_config_entry["channel"])
        upvote_reacts = get_reactions(message.reactions, emoji=starboard_config_entry["upvote_emoji"])
        downvote_reacts = get_reactions(message.reactions, emoji=starboard_config_entry["downvote_emoji"])
        tally = 0
        if upvote_reacts is not None:
            tally = upvote_reacts.count
            async for reactor in upvote_reacts.users():
                if reactor.id == message.author.id:
                    tally += starboard_config_entry["selfreact_upvote_modifier"]
                    break
        if downvote_reacts is not None:
            async for reactor in downvote_reacts.users():
                if reactor.id == message.author.id:
                    tally += starboard_config_entry["selfreact_downvote_modifier"]
                else:
                    tally -= 1
        print(f"star count for {message.id}: {tally}")
        if tally < starboard_config_entry["required_reacts"]:
            return
        # edit xboard if entry exists
        if message.id in self.catalogued_messages.keys():
            sent_prev = self.catalogued_messages[message.id]
            await sent_prev.edit(content=":x: "+str(tally)+" | "+message.channel.mention)
            return
        # add to #xboard if entry does not exists
        embed = discord.Embed()
        embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
        embed.add_field(name="", value=message.content+"\n\n[**Click to jump to message!**]("+message.jump_url+")")
        embed.timestamp = message.created_at
        if(len(message.attachments) != 0 and message.attachments[0] is not None):
            embed.set_image(url=message.attachments[0].url)
        embeds = []
        reply_embed = None
        try:
            ref = await message.channel.fetch_message(message.reference.message_id)
            reply_embed = discord.Embed()
            reply_embed.set_author(name="Replying to "+ref.author.name, icon_url=ref.author.avatar.url)
            reply_embed.add_field(name="", value=ref.content)
            reply_embed.timestamp = ref.created_at
        except AttributeError:
            pass
        if(reply_embed is not None):
            embeds.append(reply_embed)
        embeds.append(embed)
        sent_msg = await channel_parent.send(starboard_config_entry["upvote_emoji"]+" "+str(tally)+" | "+message.channel.mention, embeds=embeds)
        self.catalogued_messages[message.id] = sent_msg
            
async def setup(bot):
    await bot.add_cog(Starboard(bot))
