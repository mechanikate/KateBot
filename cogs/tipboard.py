import discord, json, random, re

from discord import app_commands
from discord.ext import commands
from discord.utils import get as get_reactions

TIPS_PATH = "/home/kate/bots/katebot-2.0/tips/"
tipboard_config = {
    1084421458819829841: {
        "required_reacts": 3,
        "upvote_emoji": "✅",
        "downvote_emoji": "❌",
        "channel": 1365471775303012422
    }
}

class Tipboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        tips_json_path = f"{TIPS_PATH}/{message.guild.id}.json"
        tipboard_config_entry = tipboard_config[message.guild.id]
        with open(tips_json_path, "r") as f:
            if(str(message.id) in json.load(f).keys()):
                return
        if(message.channel.id != tipboard_config_entry["channel"] or reaction.emoji not in [tipboard_config_entry["upvote_emoji"], tipboard_config_entry["downvote_emoji"]]):
            return
        upvote_reacts = get_reactions(message.reactions, emoji=tipboard_config_entry["upvote_emoji"])
        downvote_reacts = get_reactions(message.reactions, emoji=tipboard_config_entry["downvote_emoji"])
        tally = 0
        if upvote_reacts is not None:
            tally = upvote_reacts.count
            async for reactor in upvote_reacts.users():
                if reactor.id == message.author.id:
                    tally -= 1
                    break
        if downvote_reacts is not None:
            async for reactor in downvote_reacts.users():
                if reactor.id == message.author.id:
                    continue
                tally -= 1
        print(f"votes for {message.id}: {tally}")
        if tally < tipboard_config_entry["required_reacts"]:
            return
        contents = {}
        content = message.content
        result = ""
        mention_pattern = r"<@!?(\d+)>"
        last_end = 0
        for match in re.finditer(mention_pattern, content):
            start, end = match.span()
            user_id = int(match.group(1))
            result += content[last_end:start]
            pinged_user = message.guild.get_member(user_id)
            if pinged_user:
                result += "\\@"+user.name
            else:
                try:
                    pinged_user = await self.bot.fetch_user(user_id)
                except:
                    result += match.group(0)
                last_end = last_end
        result += content[last_end:]
        result = result.replace("@everyone", "everyoneping")
        result = result.replace("@here", "hereping")
        with open(tips_json_path, "r") as f:
            contents = json.load(f)
            contents[message.id] = "{message}\n\n *from {usermention}*".format(message = result, usermention = message.author.name)
        with open(tips_json_path, "w") as f:
            json.dump(contents, f)
    @app_commands.command(
        name="tip",
        description="Get user-submitted loading screen tips"
    )
    async def tip(self, interaction):
        with open(f"{TIPS_PATH}/{interaction.guild.id}.json", "r") as f:
            return await interaction.response.send_message(random.choice(list(json.load(f).values())))

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.guild.id not in tipboard_config:
                return
        except:
            return
        tipboard_config_entry = tipboard_config[message.guild.id]
        if(message.channel.id == tipboard_config_entry["channel"]):
            await message.add_reaction(tipboard_config_entry["upvote_emoji"])
            await message.add_reaction(tipboard_config_entry["downvote_emoji"])
async def setup(bot):
    await bot.add_cog(Tipboard(bot))
