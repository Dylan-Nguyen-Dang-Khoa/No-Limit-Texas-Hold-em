from random import shuffle, randint

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hole_cards = []

    def __str__(self):
        return f"Name: {self.name}, Balance: {self.money}"
    
    def __repr__(self):
        return str(self)

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        return str(self)

class Deck:
    def __init__(self):
        suits = ["diamonds", "hearts", "clubs", "spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.deck = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        shuffle(self.deck)
    
    def deal(self):
        return self.deck.pop(0)
    
    def __str__(self):
        return str(self.deck)
    
    def __repr__(self):
        return str

class PokerGame:
    def __init__(self):
        self.deck = Deck() 
        self.deck.shuffle() 
        self.player_num_init()  
        self.blinds_init() 
        self.players_init() 
        self.dealer = randint(0, len(self.players_list)-1) 
        self.small_blind_player = (self.dealer+1) % len(self.players_list) 
        self.big_blind_player = (self.dealer + 2) % len(self.players_list) 
        self.community = []
        self.pot = 0
        """
        self.deck is shuffled card deck
        self.player_num is number of players
        self.big_blind_amount is the big blind amount
        self.small_blind amount is the small blind amount
        self.players_list is the list with all the player objects
        self.dealer is the dealer position in self.players_list
        self.small_blind_player is the small blind position in self.players_list
        self.big_blind_player is the big blind position in self.players_list
        """

    def movebutton(self):
        self.dealer = (self.dealer+1) % len(self.players_list) 
        self.small_blind_player = (self.dealer + 1) % len(self.players_list) 
        self.big_blind_player = (self.dealer + 2) % len(self.players_list)

    def preflop(self):
        contributions = [0 * self.player_num]
        player_playing = 1
        while len(set(contributions)) != 0:
            print(f"{self.players_list[player_playing-1].name()}, please step forward")
            confirmation = input("Please confirm your presence by clicking enter")
            print("Here are your hole cards")
            print()
            print(self.players_list[player_playing-1].hole_cards())


    def players_init(self):
        self.players_list = [Player(input(f"Player {i+1}, please input your name: "), 1500) for i in range(self.player_num)]

    def deal(self):
        for _ in range(2):
            for player in self.players_list:
                player.hole_cards.append(self.deck.deal())

    def player_num_init(self):
        self.player_num = None
        while self.player_num is None or not 2 <= self.player_num <= 10:
            try:
                self.player_num = int(input("Please input the number of players you want (2-10): "))
            except ValueError:
                print("Please input a number")
    
    def blinds_init(self):
        self.big_blind_amount = None
        while self.big_blind_amount is None or not self.big_blind >= 2:
            try:
                self.big_blind_amount = int(input("Please input your big blind: "))
            except ValueError:
                print("Please input a number")
        self.small_blind_amount = self.big_blind_amount//2
    
    def __str__(self):
        return "Hi! This is the poker game object."
    
    def __repr__(self):
        return str(self)

class HandEvaluator:
    ...

def main():
    game = PokerGame()
    quit = ""
    while quit != "q":
        game.deal()
        game.preflop()
        game.flop()
        game.river()
        game.showdown()
        game.movebutton()
        quit = input("Press q to quit, anything else to continue: ").lower()
    print("99% of gamblers quit before they win big")



main()
