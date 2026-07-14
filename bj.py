import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.score = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}[rank]
        self.uid = {"S": 0, "H": 13, "C": 26, "D": 39}[suit]+{"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "10": 8, "J": 9, "Q": 10, "K": 11, "A": 12}[rank]
    def render(self):
        return {"S": "♠", "H": "♥", "C": "♣", "D": "♦"}[self.suit]+self.rank
    @staticmethod
    def from_uid(uid):
        rank_id = uid % 13
        suit_id = uid // 13
        return Card(list("SHCD")[suit_id], (list("23456789")+["10","J","Q","K","A"])[rank_id])

class Deck:
    def __init__(self):
        ranks, suits = list("23456789")+["10","J","Q","K","A"], list("SHCD")
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

class Blackjack:
    def __init__(self, wager=1):
        self.player_total, self.dealer_total = 0, 0
        self.deck = Deck().shuffle()
        self.player_hand = self.deck.draw(2)
        self.dealer_hand = self.deck.draw(2)
        self.wager = wager
        self.player_done = False
    def is_player_done(self):
        return self.score()[0] > 21 or self.player_done
    def is_dealer_done(self):
        return sum([card.score for card in self.dealer_hand]) >= 17
    @staticmethod
    def score_hand(hand):
        score = sum([card.score for card in hand if card.rank != "A"])
        aces = [11 for card in hand if card.rank == "A"]
        i = 0
        while score + sum(aces) > 21 and len(aces) > 0:
            aces[i] = 1
        return score+sum(aces)
    def score(self):
        return __class__.score_hand(self.player_hand), __class__.score_hand(self.dealer_hand)
    def player_won(self):
        player_score, dealer_score = self.score() 
        if(player_score > 21):
            return 0
        if(player_score == 21):
            return 2*self.wager
        if(dealer_score > 21 or dealer_score < player_score):
            return 1.5*self.wager
        if(dealer_score > player_score):
            return 0
        return self.wager
    def calculate_dealer_step(self):
        if(sum([card.score for card in self.dealer_hand]) < 17):
            self.dealer_hand.append(*self.deck.draw(1))
        return ([card.render() for card in self.player_hand], [card.render() for card in self.dealer_hand])
    def calculate_player_step(self, move="hit"): # "hit", "stand", "doubledown"
        if(move == "hit"):
            self.player_hand.append(*self.deck.draw(1))
        if(move == "stand"):
            self.player_done = True
        if(move == "doubledown"):
            self.wager *= 2
            self.player_hand.append(*self.deck.draw(1))
            self.player_done = True

bj = Blackjack()
while 1:
    ps, ds = bj.score()
    print("\t".join([card.render() for card in bj.player_hand])+"\t("+str(ps)+")")
    print("\t".join([card.render() for card in bj.dealer_hand])+"\t("+str(ds)+")")
    bj.calculate_player_step(input("move?: "))
    if(bj.is_player_done()):
        while not bj.is_dealer_done():
            bj.calculate_dealer_step()
            print("\t".join([card.render() for card in bj.dealer_hand])+"\t("+str(ds)+")")
        print(bj.player_won())
        break
