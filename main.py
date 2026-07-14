from constants import *
# Redirect printing
#old_stdout = sys.stdout
#log_file = open("bot.log", "w")
#sys.stdout = log_file
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client,
	allowed_contexts=app_commands.AppCommandContext(
		guild=True,
		dm_channel=True,
		private_channel=True
	),
	allowed_installs=app_commands.AppInstallationType(
		guild=True,
		user=True
	)
)
cooldown_starts = {}

def printl(txt): # Print with time
	curr_time = str(datetime.datetime.now().time())
	print("["+curr_time+"] "+txt)
"""def global_cooldown(timer=5, error_message="Command on cooldown! Wait another {TIMELEFT} second(s)."):
	def global_cooldown_decorator(f):
		async def decor(interaction):
			if(cooldown_starts.get(f.__name__) is None):
				cooldown_starts[f.__name__] = time.time()
				return await f(interaction)
			since_run = time.time() - cooldown_starts[f.__name__]
			if(since_run < timer):
				return await interaction.response.send_message(error_message.replace("{TIMELEFT}", str(math.ceil(timer-since_run))), ephemeral=True)
			cooldown_starts[f.__name__] = time.time()
			return await f(interaction)
		return decor
	return global_cooldown_decorator"""
@client.event
async def on_ready():
	global channelParent
	global deletion_log_channel
	printl("ready")
	channelParent = client.get_channel(xboard_channel)
	deletion_log_channel = client.get_channel(deletion_log_channel_id)
	printl("putting xboard in #"+channelParent.name)
	printl("putting deletion log in #"+deletion_log_channel.name)
@client.event
async def on_message(message):
	global channelParent
	if(message.channel.id in [tips_channel_id]): # and message.author.id not in [708183413814984744]):
		await message.add_reaction(upvote_emoji)
		await message.add_reaction(downvote_emoji)
	if(message.content == sync_slash_commands and message.author.id == owner_id):
		printl("Syncing slash comands!! Don't get ratelimited bozo")
		await tree.sync()
		return
	if(client.user.mentioned_in(message) and "quote" in message.content):
		printl("Quoting...")
		await quote_add(message)
	if not message.guild and message.author.id not in do_not_track: # consulify via dm
		alf = list(re.sub('[^a-zA-Z\n]+', '', re.sub('[ \n]', '\n', message.content)).lower())
		await message.reply(" ".join([f":{i.upper()}{i}:" if i not in " \n" else "\n" for i in alf]))
		return
	if message.content.lower() == "faggot":
		await message.add_reaction("🇸")
		await asyncio.sleep(0.25)
		await message.add_reaction("🇲")
		await asyncio.sleep(0.25)
		await message.add_reaction("🇴")
		await asyncio.sleep(0.25)
		await message.add_reaction("🇰")
		await asyncio.sleep(0.25)
		await message.add_reaction("🇪")
		await asyncio.sleep(0.25)
		return
	if len(message.content) == 1 and message.content.isalpha(): # react with corresponding consul emoji
		await message.add_reaction(consul_emojis[message.content.lower()])
		return
async def handle_xboard_replying(reaction, user):
	message = reaction.message
	ref = None
	try:
		ref = await message.channel.fetch_message(message.reference.message_id)
	except AttributeError:
		return None
	embed = discord.Embed()
	embed.set_author(name="Replying to "+ref.author.name, icon_url=ref.author.avatar.url)
	embed.add_field(name="", value=ref.content)
	embed.timestamp = ref.created_at
	return embed

"""async def handle_xboard(reaction,user):
	global channelParent
	message = reaction.message
	if(not reaction.emoji in [adding_emoji, user_adding_emoji] or message.channel.id in [tips_channel_id]):
		return
	count = get(message.reactions, emoji=adding_emoji)
	count_check = get(message.reactions, emoji=user_adding_emoji)
	countint = 0
	if(count is not None): # If the poster x-reacts, don't count
		countint = count.count
		async for userv in count.users():
			if(userv.id == message.author.id):
				countint -= 1
				break
	if(count_check is not None): # If the poster check-reacts, add 1 to the x-react count
		async for userv in count_check.users():
			if(userv.id == message.author.id):
				countint += 1
			else:
				countint -= 1
	printl("x count for "+str(message.id)+": "+str(countint))
	if(countint < required_for_xboard):
		return
	if(message.id in list(catalogued_messages.keys())):
		sent_prev = catalogued_messages[message.id]
		await sent_prev.edit(content=":x: "+str(countint)+" | "+message.channel.mention)
		return
	# ADD TO #xboard
	embed = discord.Embed()
	embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
	embed.add_field(name="", value=message.content+"\n\n[**Click to jump to message!**]("+message.jump_url+")")
	embed.timestamp = message.created_at
	if(len(message.attachments) != 0 and message.attachments[0] is not None):
		embed.set_image(url=message.attachments[0].url)
	embeds = []
	reply_embed = await handle_xboard_replying(reaction, user)
	if(reply_embed is not None):
		embeds.append(reply_embed)
	embeds.append(embed)
	sent_msg = await channelParent.send(adding_emoji+" "+str(required_for_xboard)+" | "+message.channel.mention, embeds=embeds)
	catalogued_messages[message.id] = sent_msg
async def handle_tips(reaction,user):
	message = reaction.message
	with open(tips_json_path, "r") as f: # if already addded as tip, exit early
		if(str(message.id) in list(json.load(f).keys())):
			return
	if(message.channel.id not in [tips_channel_id] or reaction.emoji not in [upvote_emoji, downvote_emoji]):
		return
	count = get(message.reactions, emoji=upvote_emoji)
	count_down = get(message.reactions, emoji=downvote_emoji)
	countint = 0
	to_subtr = 0
	if(count is not None): # handle selfreacts
		countint = count.count
		async for userv in count.users():
			if(userv.id in [message.author.id]):
				countint -= 1
	if(count_down is not None): # handle downvotes
		to_subtr = count_down.count
		async for userv in count_down.users():
			if(userv.id in [message.author.id]):
				to_subtr -= 1
	countint -= to_subtr
	print("Upvote count for "+str(message.id)+": "+str(countint))
	if(countint < required_for_tips): #or message.author.id in [708183413814984744]):
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
		user = message.guild.get_member(user_id)
		if user:
			result+="\\@"+user.display_name
		else:
			try:
				user = await client.fetch_user(user_id)
				result += "\\@"+user.name
			except Exception as e:
				result += match.group(0)
		last_end = end
	result += content[last_end:]
	result = result.replace("@everyone", "everyoneping")
	result = result.replace("@here", "hereping")
	print(result)
	with open(tips_json_path, "r") as f:
		contents = json.load(f)
		contents[message.id] = "{message}\n\n *from {usermention}*".format(message = result, usermention = message.author.name)
	with open(tips_json_path, "w") as f:
		f.write(json.dumps(contents))
@client.event
async def on_reaction_add(reaction, user):
	await handle_xboard(reaction, user)
	await handle_tips(reaction, user)
"""
@client.event
async def on_thread_create(thread):
	if(thread.parent_id in thread_restricted_channels): # delete threads in restricted channels list if they're the parent channel id
		await thread.delete()

"""@client.event
async def on_message_delete(message): # log message deletion via send_log_embed
	await send_log_embed(event="Message deletion", message=message)

@client.event
async def on_message_edit(before, after): # log message revision via send_log_embed
	await send_log_embed(event="Message edit", message=before, after=after)

fix_spoilers = lambda text: text + "||" if text.count("||") % 2 == 1 else text # add || to end of message if it's unbalanced (this will mess up but it saves people from being spoiled)
fix_tags = lambda text: fix_spoilers(text).replace("*", "\\*").replace("`", "\\`").replace("_", "\\_").replace("-", "\\-")
remove_spoilers = lambda text: re.sub(r"(\|\|)|( )", "", text) # remove all spoilers AND SPACES from message to get its uniqueness if edited

async def send_log_embed(event="Message deletion", message=None, after=None): # handl message logging!
	printl("Received event: "+event) # logging
	if(message.author.id == bot_id and event=="Message deletion" and message.channel.id == deletion_log_channel_id):
		channel = await client.fetch_channel(backup_id)
		await channel.send(embed=message.embeds[0])
	if(after is not None and message.content == "" and after.content != ""):
		return printl("Message @ ID "+str(message.id)+" started as nothing, thus it is probably a bot processing a command. Ignoring...")
	if(message.author.id in do_not_track): # don't track them? then don't log it either
		return printl("User "+message.author.name+" is in the do-not-track list") # log and exit
	if(message.guild.id not in tracking_servers): # if we're not tracking Camp Chloe, then don't log
		return printl("Guild "+message.guild.name+" is not in the tracking list for messages") # log and exit
	if(event == "Message deletion"): # Deletion of message
		embed = discord.Embed(color=0xaa0000) # set up embed with red color
		embed.set_author(name="Message deletion from OP "+message.author.name, icon_url=message.author.avatar.url) # Set pfp icon for OP of message
		embed.add_field(name="", value=message.content+"\n\n[**Click to jump to channel!**]("+message.channel.jump_url+")")
		embed.timestamp = datetime.datetime.now(datetime.UTC)
		return await deletion_log_channel.send(embed=embed)
	elif(event == "Message edit"):
		if(remove_spoilers(message.content) == remove_spoilers(after.content)): # sometimes the bot bugs and detects edits when there are none, so we check here
			return printl("Messages for message edit are the same (barring messed-up spoilers and spaces), returning") # if they're similar/same, log & return
		embed = discord.Embed(color=0xaaaa00) # set up embed with yellow color
		embed.set_author(name="Message revision by "+message.author.name, icon_url=message.author.avatar.url)
		embed.add_field(name="", value="**Before**\n"+fix_tags(message.content)+"\n\n**After**\n"+fix_tags(after.content)+"\n\n[**Click to jump to message!**]("+message.jump_url+")")
		embed.timestamp = datetime.datetime.now(datetime.UTC)
		return await deletion_log_channel.send(embed=embed)
	else: # if the event field doesnt' match any of our cases (this shouldn't happen!) log and return
		return printl("Event \""+event+"\" does not match any in list of events")

@tree.command( # equivalent to dming katebot in prev. versions
	name="consulify",
	description="Turn a message into Consul emojis (e.g. abc --> :Aa: :Bb: :Cc:)",
)
@app_commands.describe(
	message="The message to consulify.", # base message (required!)
	as_emojis="(Optional) If true, show the text as the actual emojis, otherwise print in plain text." # render emojis?
)
@app_commands.allowed_installs(guilds=True, users=True) # allow via dms and installation as apps
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def consulify(interaction, message: str, as_emojis: bool = True):
	alf = list(re.sub('[^a-zA-Z\n]+', '', re.sub('[ \n]', '\n', message)).lower())
	if(as_emojis):
		await interaction.response.send_message(" ".join([consul_emojis[i] if i not in " \n" else "\n" for i in alf]), ephemeral=True)
	else:
		await interaction.response.send_message(" ".join([f":{i.upper()}{i}:" if i not in " \n" else "\n" for i in alf]), ephemeral=True)

@tree.command(
	name="kateban",
	description="\"Bans\" a user."
)
@app_commands.describe(
	user="User to \"ban\".",
	reason="Reason for ban"
)
async def fakeban(interaction, user: discord.User, reason: str):
	if(random.randint(0,9) == 0):
		return await interaction.response.send_message("Who?")
	if(user.id in [292043731237076992, 466670325317238784, 1325537288662286477] or interaction.user.id in [1024300377761386526]):
		return await interaction.response.send_message("Fuck you")
#	if(user.id in [1024300377761386526] and random.randint(0,1)==1):
#		return await interaction.response.send_message("Fuck you")
	await interaction.response.send_message("✅: "+user.mention+" has been banned for reason: "+reason)

@tree.command(
	name="gamble",
	description="Gamble your life savings"
)
async def gamble(interaction):
	user_id = str(interaction.user.id)
	data = {"odds_power": 3, "balances": {}}
	try:
		with open(econ_json_path, "r") as f:
			data = json.load(f)
	except:
		pass
	if(user_id not in data["balances"]):
		data["balances"][user_id] = 100
	cap = 2**(data["odds_power"]//3)
	if(random.randint(0,cap) == cap):
		winnings=cap+random.uniform(-cap/4, cap/3)
		data["balances"][user_id] += winnings
		data["odds_power"]+=1
		await interaction.response.send_message("You win ${winnings:.2f}!".format(winnings=winnings))
	else:
		data["balances"][user_id] -= 1
		await interaction.response.send_message("You lost $1.00 :(")

	with open(econ_json_path, "w+") as f:
		json.dump(data, f)

@tree.command(
	name="balance",
	description="Get your current money balance from gambling"
)
@app_commands.describe(
	user="(Optional) The user to get the balance of. Defaults to the sender"
)
async def balance(interaction, user: discord.User = None):
	if(user is None):
		user = interaction.user
	user_id = str(user.id)
	data = {"odds_power": 3, "balances": {}}
	try:
		with open(econ_json_path, "r") as f:
			data = json.load(f)
	except:
		pass
	if(user_id not in data["balances"]):
		data["balances"][user_id] = 100
	await interaction.response.send_message("{name} has ${bal:.2f}.".format(name=user.name, bal=data["balances"][user_id]))
	with open(econ_json_path, "w+") as f:
		json.dump(data, f)

@tree.command(
	name="wisdom",
	description="Get some of the dev (kate's) wisdom"
)
@global_cooldown(timer=3600)
async def wisdom(interaction):
	await interaction.response.send_message(random.choice(wisdom_list))
@tree.command(
	name="tip",
	description="Get user-submitted loading screen tips"
)
async def tip(interaction):
	with open(tips_json_path, "r") as f:
		# printl(list(json.load(f).values()))
		return await interaction.response.send_message(random.choice(list(json.load(f).values())))

"""

group = app_commands.Group(name="quote", description="Handle quotes")
@group.command(
	name="get",
	description="Get a quote from a user"
)
@app_commands.describe(
	user="The user to get the quote from",
	number="The quote ID/index"
)
async def quote(interaction, user: discord.User, number: int):
	id = str(user.id)
	with open(quotes_json_path, "r") as f:
		loaded = json.load(f)
		if(id not in loaded):
			return await interaction.response.send_message("No quote found!")
		userli = loaded[id]
		if(userli is None or len(userli) < number or number < 1):
			return await interaction.response.send_message("No quote found!")
		return await interaction.response.send_message(userli[number-1])

@group.command(
	name="stats",
	description="Get number of quotes for a user or in total"
)
@app_commands.describe(
	user="(Optional) The user to get the number of quotes from"
)
async def stats(interaction, user: discord.User = None):
	with open(quotes_json_path, "r") as f:
		loaded = json.load(f)
		if(user is None):
			return await interaction.response.send_message("Total quotes for all users: "+str(sum([len(v) for v in list(loaded.values())])))
		id = str(user.id)
		if(id not in loaded):
			return await interaction.response.send_message("There are 0 quotes attributed to "+user.display_name+".")
		return await interaction.response.send_message("There are "+str(len(loaded[id]))+" quote(s) attributed to "+user.display_name+".")
async def quote_add(message):
	ref = None
	try:
		ref = await message.channel.fetch_message(message.reference.message_id)
	except AttributeError:
		return await message.reply("You aren't replying to a message to quote!")
	user = ref.author
	contents = ref.content
	id = str(user.id)
	if(user.id == message.author.id):
		return await message.reply("You can't quote yourself!")
	json_dat = None
	with open(quotes_json_path, "r") as f:
		json_dat = json.load(f)
	with open(quotes_json_path, "w") as f:
		if(id not in json_dat):
			json_dat[id] = []
		if(contents in json_dat[id]):
			json.dump(json_dat, f)
			return await message.reply("This exact message has already been quoted for this user!")
		json_dat[id].append(contents)
		json_dat[id] = list(OrderedDict.fromkeys(json_dat[id]))
		json.dump(json_dat, f)
		return await message.reply("Added quote number "+str(len(json_dat[id]))+" for user \""+user.display_name+"\"")

tree.add_command(group)
# pycron.start()
client.run(bot_secret)
#sys.stdout = old_stdout
#log_file.close()
