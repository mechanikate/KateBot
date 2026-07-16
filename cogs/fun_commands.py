import discord, random, re

from discord import app_commands
from discord.ext import commands
# KateBot's emojis for the consuls (originally from Queen/consul.p's server)
consul_emojis = {                        
        "a": "<:Aa:1384672401396076554>",
        "b": "<:Bb:1384672386917601362>",
        "c": "<:Cc:1384672377069371412>",
        "d": "<:Dd:1384672366751121449>",
        "e": "<:Ee:1384672351907483739>",
        "f": "<:Ff:1384672336208203906>",
        "g": "<:Gg:1384672325848273018>",
        "h": "<:Hh:1384672317157802004>",
        "i": "<:Ii:1384672308148310116>",
        "j": "<:Jj:1384672299734794445>",
        "k": "<:Kk:1384672289219543120>",
        "l": "<:Ll:1384672280449388554>",
        "m": "<:Mm:1384672270198247454>",
        "n": "<:Nn:1384672257074528337>",
        "o": "<:Oo:1384672247704322159>",
        "p": "<:Pp:1384672237570756709>",
        "q": "<:Qq:1384672227617804409>",
        "r": "<:Rr:1384672193652326580>",
        "s": "<:Ss:1384672177844125781>",
        "t": "<:Tt:1384672167941247007>",
        "u": "<:Uu:1384672153776947260>",
        "v": "<:Vv:1384672137838592120>",
        "w": "<:Ww:1384672127436722418>",
        "x": "<:Xx:1384672107882872942>",
        "y": "<:Yy:1384672097665548429>",
        "z": "<:Zz:1384672078518816909>"
}
# kate's random wisdom/bullshit
wisdom_list = [
	"""1.
* pack bowl
* light hemp wick
* light bowl
* take rip
* blow out hemp wick with exhaling smoke
* outta there""",
	"""2.
the naked man fears no pickpocket""",
	"""3.
I am going to send Fifteen Hundred Pinkertons with Guns to Kill you""",
	"""4.
Did Jesus stop preaching when the Romans told him to stop? No. So keep spewing bullshit""",
	"""5.
Every day is monkey mondays""",
	"""6.
every afternoon is ape afternoons""",
	"""7.
"who give a shit" ~ Rene Descartes""",
	"""8.
Nobody knows how the water got in the coconut. It's a fact of life.""",
	"""9.
We didn't start the fire (it was always burning (since the world's been turning)), but we definitely poured a fuckton of gasoline on it""",
	"""10.
Australia is the furthest country from a cultural victory in irl Civilization, like what the hell are they doing there man""",
	"""11.
Contrary to popular belief, I did not shit myself on the mile in the 4th grade""",
	"""12.
A child prodigy musician that has been ran over could be called a "A-flat minor." This is rude, but nobody who can be offended by this joke is with us here today""",
	"""13.
In JavaScript:
```js
(true+true)**(((true+true)**((true+true+true)**(true+true)+true)))
```
equals an infinite truthnuke""",
	"""14.
in a sigma world I would smack you upside the head""",
	"""15.
Do you ever look in the mirror and just say "Fuck."? Not just you""",
	"""16.
There are hundreds of thousands if not over a million words in the English language, and yet I can't use any of them effectively. sucks2suck i guess""",
	"""17.
John B. Goodenough is the name of a real Nobel laureate. He probably won that shit just for his last name. Maybe the Nobel Prize is just a funny name award""",
	"""18.
I hatd One (1) Mike's Hard Lemonade and I'm fucking Wasted.""",
	"""19.
It is possible to buy seeds for a strain of weed named Michael Jordan Feminized""",
	"""20.
baby yoda fucking loves marlboro reds""",
	"""21.
There is a comment on a video titled "Bernie Sanders 8 1/2 hour Filibuster but it's Lofi" with the following contents:
> 5 years later, Bernie has been sidelined by the oligarchy. Trump is back, America is decaying.
> 
> Fuck I'm gunna smoke the fattest blunt and fall asleep to this, hope I find a new timeline.
Godspeed, lucienlachance9294."""
]

BLACKLISTED_USERS = [1024300377761386526]
UNBANNABLE_USERS = [292043731237076992, 466670325317238784, 1325537288662286477]
class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command( # equivalent to dming katebot in prev. versions
        name="consulify",
        description="Turn a message into Consul emojis (e.g. abc --> :Aa: :Bb: :Cc:)",
    )
    @app_commands.describe(
        message="The message to consulify.", # base message (required!)
        as_emojis="(Optional) If true, show the text as the actual emojis, otherwise print in plain text." # render emojis?
    )
    @app_commands.allowed_installs(guilds=True, users=True) # allow via dms and installation as apps
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def consulify(self, interaction, message: str, as_emojis: bool = True):
        alf = list(re.sub('[^a-zA-Z\n]+', '', re.sub('[ \n]', '\n', message)).lower())
        if(as_emojis):
            await interaction.response.send_message(" ".join([consul_emojis[i] if i not in " \n" else "\n" for i in alf]), ephemeral=True)
        else:
            await interaction.response.send_message(" ".join([f":{i.upper()}{i}:" if i not in " \n" else "\n" for i in alf]), ephemeral=True)
    
    @app_commands.command(
        name="kateban",
        description="\"Bans\" a user."
    )
    @app_commands.describe(
        user="User to \"ban\".",
        reason="Reason for ban"
    )
    async def fakeban(self, interaction, user: discord.User, reason: str):
        if(user.id in UNBANNABLE_USERS or interaction.user.id in BLACKLISTED_USERS):
            return await interaction.response.send_message("Fuck you")
        await interaction.response.send_message("✅: "+user.mention+" has been banned for reason: "+reason)

    @app_commands.command(
        name="wisdom",
        description="Get some of the dev (Kate)'s wisdom"
    )
    @app_commands.checks.cooldown(1, 3600, key=lambda i: i.guild_id)
    async def wisdom(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(wisdom_list))

    async def cog_app_command_error(self, ctx: discord.Interaction, error: commands.CommandError):
        await ctx.response.send_message(f"Command on cooldown for another {int(error.retry_after+1)} seconds!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FunCommands(bot))
