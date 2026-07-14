import discord,asyncio,requests,datetime,re,os,random,time,math,json,sys,pycron
from discord.utils import get
from discord import app_commands
from collections import OrderedDict

bot_secret = os.environ["BOT_SECRET"] # BOT_SECRET env var, and you aren't getting a copy of it
channelParent = None # xboard channel class (from id xboard_channel)

# GENERAL
owner_id = 292043731237076992 # bot owner/admin id
bot_id = 1325537288662286477
# TEXT COMMAND NAMES
sync_slash_commands = "!!!syncslash"
tips_json_path = "/home/kate/bots/katebot/tips.json"
quotes_json_path = "/home/kate/bots/katebot/quotes.json"
econ_json_path = "/home/kate/bots/katebot/econ.json"
# XBOARD
required_for_xboard = 3 # how many reacts to get on xboard
required_for_tips = 3 # how many net checkmarks to get added to /tip
xboard_channel = 1376332166622871602 # send xboard/starboard to this ID
tips_channel_id = 1365471775303012422 # deal with tip suggestions in this channel ID
deletion_log_channel_id = 1380937180628783254 # send message revision logs to this ID
deletion_log_channel = None # keep as none
catalogued_messages = {} # keep empty unless we're adding old keys too (which is unnecessary since katebot doesn't look @ previous messages)
adding_emoji = "❌" # this will add to the counter for all except the op
user_adding_emoji = "✅" # this will also add to the counter only if added by the user
backup_id = 1410220669773287486 # channel to backup message log deletions

upvote_emoji = "✅" # for /tip command
downvote_emoji = "❌" # for /tip command
# THREAD AUTOREMOVAL
thread_restricted_channels = [1351059421844869130, 1307570398409396305, 1371374422665072660] # question-of-the-day, rules, polls-and-the-like disabled here (no order)

# MESSAGE LOGGING
do_not_track = [bot_id, 432610292342587392, 1307052801687420981, 1211781489931452447] # don't track these users for message modifications (KateBot itself, mudae, and dyno)
tracking_servers = [1084421458819829841] # servers to track message editing in


# KateBot's emojis for the consuls (originally from Queen's server)
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
