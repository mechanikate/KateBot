import asyncio, discord, json, random

from discord import app_commands
from discord.ext import commands

ECON_PATH = "/home/kate/bots/katebot-2.0/econ/"

format_balance = lambda balance: "${balance:.2f}".format(balance=balance)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def retrieve_data(self, server_id: int):
        data = {"odds_power": 3, "balances": {}, "payout_mults": {"win": 1.5, "blackjack": 2, "forfeit": 0.5}}
        try:
            with open(f"{ECON_PATH}/{server_id}.json", "r") as f:
                data = json.load(f)
        except json.JSONDecodeError, FileNotFoundError:
            self.save_data(data, server_id)
        return data

    def save_data(self, data, server_id: int):
        with open(f"{ECON_PATH}/{server_id}.json", "w+") as f:
            json.dump(data, f)

    def retrieve_balance(self, user_id: str, server_id: int):
        data = self.retrieve_data(server_id)
        if(str(user_id) not in data["balances"]):
            data["balances"][str(user_id)] = 100
            self.save_data(data, server_id)
        return data["balances"][str(user_id)]
    
    def store_balance(self, user_id: str, amount: float, server_id: int):
        data = self.retrieve_data(server_id)
        data["balances"][str(user_id)] = amount
        self.save_data(data, server_id)

    def retrieve_odds_power(self, server_id: int):
        data = self.retrieve_data(server_id)
        return data["odds_power"]
    
    def store_odds_power(self, odds_power: int, server_id: int):
        data = self.retrieve_data(server_id)
        data["odds_power"]=odds_power
        self.save_data(data, server_id)

    def store_payout_mults(self, payout_mults, server_id: int):
        data = self.retrieve_data(server_id)
        data["payout_mults"] = payout_mults
        self.save_data(data, server_id)

    def retrieve_payout_mults(self, server_id: int):
        data = self.retrieve_data(server_id)
        if("payout_mults" not in data):
            data["payout_mults"] = {"win": 1.5, "blackjack": 2, "forfeit": 0.5}
        return data["payout_mults"]

# regular economy activities e.g. viewing balances, viewing leaderboard of server, admin balance commands
class RegularActivities(commands.Cog):

    admin_commands = app_commands.Group(name="adminbalances", description="Economy management commands for server admins")
    admin_payout_commands = app_commands.Group(name="adminpayouts", description="Blackjack payout percentage commands for server admins")

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="balance",
        description="Get your current account balance from gambling"
    )
    @app_commands.describe(
        user="(Optional) The user to get the balance of. Defaults to the sender"
    )
    async def balance(self, interaction: discord.Interaction, user: discord.User = None):
        if(user is None):
            user = interaction.user
        user_id = str(user.id)
        economy = self.bot.get_cog("Economy")
        balance = economy.retrieve_balance(user_id, interaction.guild.id) 
        await interaction.response.send_message(f"{user.name} has {format_balance(balance)}.")

    @app_commands.command(
        name="leaderboard",
        description="Get the richest members of the server"
    )
    async def leaderboard(self, interaction: discord.Interaction):
        i = 0
        economy = self.bot.get_cog("Economy")
        embed = discord.Embed(title="Leaderboard")
        for user_id, balance in sorted(economy.retrieve_data(interaction.guild.id)["balances"].items(), key=lambda v: v[1], reverse=True):
            if(i > 25):
                break
            user = await self.bot.fetch_user(user_id)
            if not user: 
                continue
            embed.add_field(name=f"{user.name}: {format_balance(balance)}", value="", inline=False)
            i+=1
        await interaction.response.send_message(embed=embed)

    # /admin ...
    @admin_commands.command(
        name="set",
        description="Set user's balance"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def admin_set(self, interaction: discord.Interaction, new_balance: float, target_user: discord.User = None):
        if(target_user is None):
            target_user = interaction.user
        user_id = str(target_user.id)
        economy = self.bot.get_cog("Economy")
        try:
            economy.store_balance(user_id, new_balance, interaction.guild.id)
            await interaction.response.send_message(f"Set balance of {target_user.name} to ${format_balance(new_balance)}.")
        except:
            await interaction.response.send_message(f"Failed to set balance of {target_user.name} to {format_balance(new_balance)}, please send mechanikate a notice about this.")

    @admin_commands.command(
        name="give",
        description="Give user money"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def admin_give(self, interaction: discord.Interaction, amount: float, target_user: discord.User = None):
        if(target_user is None):
            target_user = interaction.user
        user_id = str(target_user.id)
        economy = self.bot.get_cog("Economy")
        try:
            balance = economy.retrieve_balance(user_id, interaction.guild.id)
            new_balance = balance + amount
            economy.store_balance(user_id, new_balance, interaction.guild.id)
            await interaction.response.send_message(f"Set balance of {target_user.name} from {format_balance(balance)} to {format_balance(new_balance)}.")
        except:
            await interaction.response.send_message(f"Failed to set balance of {target_user.name} from {format_balance(balance)} to {format_balance(new_balance)}, please send mechanikate a notice about this.")

    @admin_commands.command(
        name="remove",
        description="Remove user money"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def admin_remove(self, interaction: discord.Interaction, amount: float, target_user: discord.User = None):
        if(target_user is None):
            target_user = interaction.user
        user_id = str(target_user.id)
        economy = self.bot.get_cog("Economy")
        try:
            balance = economy.retrieve_balance(user_id, interaction.guild.id)
            new_balance = balance - amount
            economy.store_balance(user_id, new_balance, interaction.guild.id)
            await interaction.response.send_message(f"Set balance of {target_user.name} from ${format_balance(balance)} to {format_balance(new_balance)}.")
        except:
            await interaction.response.send_message(f"Failed to set balance of {target_user.name} from {format_balance(balance)} to {format_balance(new_balance)}, please send mechanikate a notice about this.")

    async def econ_set_handler(self, interaction, setter_function, params=["user_id", "value", "guild_id"], target_user: discord.User = None, value=0, getter_function = lambda economy: None):
        if(target_user is None):
            target_user = interaction.user
        user_id = str(target_user.id)
        economy = self.bot.get_cog("Economy")
        spec_params = []
        if("user_id" in params):
            spec_params.append(user_id)
        if("value" in params):
            spec_params.append(value)
        if("guild_id" in params):
            spec_params.append(interaction.guild.id)
        prev = getter_function(economy, *spec_params)
        try:
            prev_copy = prev.copy()
            curr = await setter_function(economy, prev, *spec_params)
            return 1, prev_copy, curr
        except:
            return 0, prev, None

    async def econ_set_mult_handler(self, interaction, multiplier: float, prop_name: str):
        async def setter_func(economy, prev, value, guild_id):
            prev[prop_name] = value
            economy.store_payout_mults(prev, guild_id)
            return value
        ret_code, prev, curr = await self.econ_set_handler(interaction, setter_func, params=["value", "guild_id"], value=multiplier, getter_function = lambda economy, val, guild_id: economy.retrieve_payout_mults(guild_id))
        await interaction.response.send_message(f"Set {prop_name} multiplier from {prev[prop_name]}x to {curr}x." if ret_code else f"Failed to set {prop_name} multiplier from {prev[prop_name]}x to {multiplier}x, please send mechanikate a notice about this.")

    @admin_payout_commands.command(name="win")
    @app_commands.checks.has_permissions(administrator=True)
    async def admin_set_win(self, interaction: discord.Interaction, multiplier: float = 1.5):
        await self.econ_set_mult_handler(interaction, multiplier, "win")
    @admin_payout_commands.command(name="blackjack")
    @app_commands.checks.has_permissions(administrator=True)
    async def admin_set_blackjack(self, interaction: discord.Interaction, multiplier: float = 2.0):
        await self.econ_set_mult_handler(interaction, multiplier, "blackjack")
    @admin_payout_commands.command(name="forfeit")
    @app_commands.checks.has_permissions(administrator=True)
    async def admin_set_forfeit(self, interaction: discord.Interaction, multiplier: float = 0.5):
        await self.econ_set_mult_handler(interaction, multiplier, "forfeit")


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="gamble",
        description="Gamble your life savings"
    )
    async def gamble(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        economy = self.bot.get_cog("Economy")
        balance = economy.retrieve_balance(user_id, interaction.guild.id)
        cap = 2**(economy.retrieve_odds_power(interaction.guild.id)//3)
        rand = random.randint(1,cap)
        if(rand == cap):
            winnings = cap+random.uniform(-cap/4, cap/3)
            economy.store_balance(user_id, balance+winnings, interaction.guild.id)
            economy.store_odds_power(economy.retrieve_odds_power(interaction.guild.id)+1, interaction.guild.id)
            await interaction.response.send_message("You win ${winnings:.2f}!".format(winnings=winnings))
            return

        economy.store_balance(user_id, balance-1, interaction.guild.id)
        await interaction.response.send_message("You lost $1.00 :(")

    @app_commands.command(
        name="blackjack",
        description="Play blackjack against the bot"
    )
    @app_commands.describe(
        wager="(Defaults to $1.00) How much to wager against the bot"
    )
    async def blackjack(self, interaction: discord.Interaction, wager: float = 1.0):
        economy = self.bot.get_cog("Economy")
        view = BlackjackView(wager, self.bot, interaction)
        if(wager > max(5,economy.retrieve_balance(interaction.user.id, interaction.guild.id))):
            await interaction.response.send_message("You can only gamble up to your balance (or $5 if you have <$5)!")
            return
        economy.store_balance(interaction.user.id, economy.retrieve_balance(interaction.user.id, interaction.guild.id)-wager, interaction.guild.id)
        await interaction.response.send_message(embed=BlackjackView.make_blackjack_embed(interaction, view.blackjack), view=view)

class BlackjackView(discord.ui.View):
    def __init__(self, wager, bot, start_interaction):
        super().__init__()
        self.wager = wager
        self.bot = bot
        self.start_interaction = start_interaction
        self.blackjack = BlackjackGame(self.bot, start_interaction.guild.id, start_interaction.user.id, wager)

    async def disable_if_over(self, msg):
        msg = msg.resource if hasattr(msg, "resource") else msg
        if(self.blackjack.game_over or self.blackjack.score()[0] > 21):
            for child in self.children:
                child.disabled=True
            msg = await msg.edit(view=self)
            msg = msg.resource if hasattr(msg, "resource") else msg

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.red)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        economy = self.bot.get_cog("Economy")
        economy.store_balance(interaction.user.id, economy.retrieve_balance(interaction.user.id, interaction.guild.id)+self.blackjack.calculate_player_step("hit"), interaction.guild.id)
        msg = await interaction.response.edit_message(embed=__class__.make_blackjack_embed(interaction, self.blackjack))
        await self.disable_if_over(msg)
        msg = msg.resource if hasattr(msg, "resource") else msg
        if(self.blackjack.player_done):
            await msg.edit(embed=__class__.make_blackjack_embed(interaction, self.blackjack, phase=1, show_winner=True))
            await self.disable_if_over(msg)
            return

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.green)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.blackjack.calculate_player_step("stand")
        economy = self.bot.get_cog("Economy")
        msg = await interaction.response.edit_message(embed=__class__.make_blackjack_embed(interaction, self.blackjack, phase=1))
        await self.disable_if_over(msg)
        while 1:
            await asyncio.sleep(1)
            if(self.blackjack.player_done and self.blackjack.dealer_done):
                msg = msg.resource if hasattr(msg, "resource") else msg
                await msg.edit(embed=__class__.make_blackjack_embed(interaction, self.blackjack, phase=1, show_winner=True))
                economy.store_balance(interaction.user.id, economy.retrieve_balance(interaction.user.id, interaction.guild.id)+self.blackjack.player_won(), interaction.guild.id)
                await self.disable_if_over(msg)
                return
            msg = msg.resource if hasattr(msg, "resource") else msg
            self.blackjack.calculate_dealer_step()
            msg = await msg.edit(embed=__class__.make_blackjack_embed(interaction, self.blackjack, phase=1))
            msg = msg.resource if hasattr(msg, "resource") else msg

    @discord.ui.button(label="Double Down", style=discord.ButtonStyle.blurple)
    async def doubledown(self, interaction: discord.Interaction, button: discord.ui.Button):
        economy = self.bot.get_cog("Economy")
        economy.store_balance(interaction.user.id, economy.retrieve_balance(interaction.user.id, interaction.guild.id)+self.blackjack.calculate_player_step("doubledown"), interaction.guild.id)
        msg = await interaction.response.edit_message(embed=__class__.make_blackjack_embed(interaction, self.blackjack, phase=1))
        await self.disable_if_over(msg)
        while 1:
            await asyncio.sleep(1)
            if(self.blackjack.player_done and self.blackjack.dealer_done):
                msg = msg.resource if hasattr(msg, "resource") else msg
                await msg.edit(embed=__class__.make_blackjack_embed(interaction, self.blackjack, phase=1, show_winner=True))
                economy.store_balance(interaction.user.id, economy.retrieve_balance(interaction.user.id, interaction.guild.id)+self.blackjack.player_won(), interaction.guild.id)
                await self.disable_if_over(msg)
                return
            msg = msg.resource if hasattr(msg, "resource") else msg
            self.blackjack.calculate_dealer_step()
            msg = await msg.edit(embed=__class__.make_blackjack_embed(interaction, self.blackjack, phase=1))
            msg = msg.resource if hasattr(msg, "resource") else msg
    
    @discord.ui.button(label="Forfeit", style=discord.ButtonStyle.gray)
    async def forfeit(self, interaction: discord.Interaction, button: discord.ui.Button):
        economy = self.bot.get_cog("Economy")
        economy.store_balance(interaction.user.id, economy.retrieve_balance(interaction.user.id, interaction.guild.id)+self.blackjack.calculate_player_step("forfeit"), interaction.guild.id)
        self.blackjack.forfeit = True
        self.blackjack.game_over = True
        msg = await interaction.response.edit_message(embed=__class__.make_blackjack_embed(interaction, self.blackjack, phase=1, show_winner=True, forfeit=True))
        await self.disable_if_over(msg)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.start_interaction.user:
            await interaction.response.send_message("Only the author of the command can perform this action.", ephemeral=True)
            return False
        return True 

    @staticmethod
    def make_blackjack_embed(interaction, blackjack, phase=0, show_winner=False, forfeit=False):
        embed = discord.Embed(title="Blackjack")
        player_score, dealer_score = blackjack.score()
        name_player, value_player, name_dealer, value_dealer = [
            (f"{interaction.user.name}'s hand ({player_score})", "`"+"` `".join([card.render() for card in blackjack.player_hand])+"`", f"KateBot's hand ({blackjack.dealer_hand[0].score}+?)", "`"+blackjack.dealer_hand[0].render()+"` `??`"),
            (f"{interaction.user.name}'s hand ({player_score})", "`"+"` `".join([card.render() for card in blackjack.player_hand])+"`", f"KateBot's hand ({dealer_score})", "`"+"` `".join([card.render() for card in blackjack.dealer_hand])+"`"),
        ][phase]

        embed.add_field(name=name_player, value=value_player, inline=False)
        embed.add_field(name=name_dealer, value=value_dealer, inline=False)

        if show_winner:
            embed.add_field(name=blackjack.winner(interaction.user.name), value="", inline=False)

        return embed
class Card:
    SUIT_LOGO_MAP = {"S": "♠", "H": "♥", "C": "♣", "D": "♦"}
    SUIT_UID_MAP = {"S": 0, "H": 13, "C": 26, "D": 39}
    RANK_SCORE_MAP = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
    RANK_UID_MAP = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "10": 8, "J": 9, "Q": 10, "K": 11, "A": 12}
    SUITS = list("SHCD")
    RANKS = list("23456789")+["10","J","Q","K","A"]
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.score = self.RANK_SCORE_MAP[rank]
        self.uid = self.SUIT_UID_MAP[suit]+self.RANK_UID_MAP[rank]
    def render(self):
        return self.SUIT_LOGO_MAP[self.suit]+self.rank
    @staticmethod
    def from_uid(uid):
        rank_id = uid % 13
        suit_id = uid // 13
        return Card(Card.SUITS[suit_id], Card.RANKS[rank_id])

class Deck:
    def __init__(self):
        self.deck = []
        for uid in range(52):
            self.deck.append(Card.from_uid(uid))
    def shuffle(self):
        self.deck = random.sample(self.deck, 52)
        return self
    def draw(self, n=1):
        drawn = random.sample(self.deck, n)
        drawn_uids = [card.uid for card in drawn]
        self.deck = [card for card in self.deck if card.uid not in drawn_uids]
        return drawn

class BlackjackGame:
    def __init__(self, bot, guild_id, user_id, wager=1):
        self.bot = bot
        self.guild_id = guild_id
        self.user_id = user_id
        self.deck = Deck().shuffle()
        self.player_hand = self.deck.draw(2)
        self.dealer_hand = self.deck.draw(2)
        self.wager = wager
        self.player_done = False
        self.dealer_done = False
        self.game_over = False
        self.forfeit = False
    def is_player_done(self):
        return self.score()[0] > 21 or self.player_done
    def is_dealer_done(self):
        return self.score()[1] >= 17
    @staticmethod
    def score_hand(hand):
        score = sum([card.score for card in hand if card.rank != "A"])
        aces = [11 for card in hand if card.rank == "A"]
        i = 0
        while score + sum(aces) > 21 and len(aces) > 0 and i < len(aces):
            aces[i] = 1
            i+=1
        return score+sum(aces)
    def score(self):
        return __class__.score_hand(self.player_hand), __class__.score_hand(self.dealer_hand)
    def winner(self, player_name): # get winner explanation
        player_score, dealer_score = self.score()
        if(self.player_done and self.dealer_done):
            self.game_over = True
        if(self.forfeit):
            return f"KateBot won ({player_name} forfeited)"
        if(player_score > 21):
            return f"KateBot won ({player_name} busted)"
        if(player_score == 21 and dealer_score < 21):
            return f"{player_name} won (21)"
        if(dealer_score < player_score):
            return f"{player_name} won (higher score)"
        if(dealer_score > 21):
            return f"{player_name} won (KateBot busted)"
        if(dealer_score > player_score):
            return f"KateBot won (higher score)"
        return "Tie (same scores)"
    def player_won(self): # calculate player profit
        payout_mults = self.bot.get_cog("Economy").retrieve_payout_mults(self.guild_id)
        player_score, dealer_score = self.score() 
        if(self.forfeit):
            return payout_mults["forfeit"]*self.wager
        if(player_score > 21):
            return 0
        if(player_score == 21):
            return payout_mults["blackjack"]*self.wager
        if(dealer_score > 21 or dealer_score < player_score):
            return payout_mults["win"]*self.wager
        if(dealer_score > player_score):
            return 0
        return self.wager
    def calculate_dealer_step(self): # draw if <17, stand/mark as done if >=17
        if(self.score()[1] < 17):
            self.dealer_hand.append(*self.deck.draw(1))
            return
        self.dealer_done = True
    def calculate_player_step(self, move="hit"): # "hit", "stand", "doubledown"
        if(move == "hit"):
            self.player_hand.append(*self.deck.draw(1))
            if(self.score()[0] > 21):
                self.player_done = True
            return 0 
        if(move == "stand"):
            self.player_done = True
            return 0
        if(move == "doubledown"):
            self.wager *= 2
            self.player_hand.append(*self.deck.draw(1))
            self.player_done = True
            return -self.wager
        if(move == "forfeit"):
            self.player_done = True
            self.forfeit = True
            self.dealer_done = True
            return self.bot.get_cog("Economy").retrieve_payout_mults(self.guild_id)["forfeit"]*self.wager

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Economy(bot))
    await bot.add_cog(RegularActivities(bot))
    await bot.add_cog(Gambling(bot))

