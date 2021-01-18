# DECK CLASS
import random
import requests
from bs4 import BeautifulSoup
import webbrowser
import functools


class Deck():
    def __init__(self):
        cards = [[(y, x) for x in ['Clubs', 'Diamonds', 'Hearts', 'Spades']] for y in range(1, 14)]
        cards = [x for sublist in cards for x in sublist]
        self.cards = cards

    def __str__(self):
        return (f'deck = {self.cards}')

    def __len__(self):
        count = 0
        for x in self.cards:
            count += 1
        return (count)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            try:
                return (self.cards[idx])
            except(KeyError):
                print("list index out of range")
        else:
            raise (typeError)

    def __setitem__(self, slice_, value):
        print(f'{slice_} this is index input')

        try:
            if str(value[1]).lower() in ['clubs', 'diamonds', 'hearts', 'spades']:
                if isinstance(slice_, int):
                    self.cards[slice_] = (value[0], value[1])
                else:
                    self.cards[slice_.start:slice_.stop:slice_.step] = [(value[0], value[1])]
            else:
                print('color of card must be either clubs, diamonds, hearts, spades')
        except(KeyError):
            print('list index out of range')

    def __delitem__(self, idx):
        if isinstance(idx, int):
            try:
                self.cards[idx:idx + 1] = []
            except(KeyError):
                print('list index out of range')

    def __iter__(self):
        return iter(self.cards)

    @staticmethod
    def describtion():
        print(
            'This is a standard 52-card deck of French-suited playing cards. it is the most common pack of playing cards used today')

    # is a static method. It’s not dependent on the class,
    # Static methods can be called on either an instance or the class.

    def pop(self, idx):
        return self.cards.pop(idx)

    def shuffle(self):
        random.shuffle(self.cards)


# PARTICIPANT

class Participant():
    game_status = 1

    def __init__(self, cash=0, status=0):
        self.hand = [[]]
        self.cash = cash
        self.status = status

    def receive_card(self, card, idx):
        self.hand[idx].insert(0, card)

    def result(self, amount, game_over='Game over'):
        self.cash += amount
        if self.cash == 0:
            self.game_status = game_over

    def round_over(self, result):
        self.cash += result


# PLAYER

class Player(Participant):
    bet = [[]]

    def __init__(self, dealer):
        super().__init__()
        self.cash = 500
        self.dealer = dealer

    def place_bet(self, p_bet=0, target='none', double='none'):
        if self.cash - p_bet < 0:
            p_bet = self.cash
            print(f'insufficient funds placed bet of {p_bet} instead')
        if target == 'none':
            self.cash -= p_bet
            self.bet[0] = p_bet
        elif double == 'none':
            self.cash -= self.bet[target]
            self.bet = [x for i, x in enumerate(self.bet) if i != target] + [self.bet[target], self.bet[target]]
        else:
            self.cash -= self.bet[target]
            self.bet[target] = self.bet[target] * 2
        print(f'cash : {self.cash}')

    def result(self, amount, game_over='Game over player broke'):
        return super().result(amount, game_over)

    def hit(self, idx):
        self.dealer.deal(idx, 1)

    def split(self, target):
        self.hand = [x for i, x in enumerate(self.hand) if i != target] + [[x] for x in self.hand[target]]

    def receive_card(self, card, idx):
        super().receive_card(card, idx)
        if len(self.hand) == 1 and all(len(x) >= 2 for x in self.hand):
            print(f'Player hand: {self.hand}')
        elif all(len(x) >= 2 for x in self.hand):
            for i, y in enumerate(self.hand):
                print(f'Player hand number {i}: {y}')


# DEALER

class Dealer(Participant):
    d_h_sum = 0

    def __init__(self, deck):
        super().__init__()
        self.cash = 100000
        self.player = None
        self.deck = deck

    @property
    def d_h_sum(self):
        return self.__d_h_sum

    @d_h_sum.setter
    def d_h_sum(self, inp):
        if isinstance(inp, int):
            self.__d_h_sum = inp

    def __draw(self):
        try:
            return self.deck.pop(0)
        except IndexError:
            print('No more cards in deck, new deck was inserted in shoe')
            self.deck = Deck()
            self.deck.shuffle()
            return self.deck.pop(0)

    def __deal_player_card(self, card, idx):
        self.player.receive_card(card, idx)

    def deal(self, idx, target=0):
        card = self.__draw()
        if target == 0:
            self.__receive_card(card)
        else:
            self.__deal_player_card(card, idx)

    def add_player(self, player):
        self.player = player

    def result(self, amount, game_over='Congratulazions you beat the house, the game is over!'):
        return super().result(amount, game_over)

    def round_over(self, bets):
        for i in bets:
            if i[1] == 0:  # draw
                self.player.result(i[0])
            if i[1] == 1:  # dealer blackjack
                self.result(i[0])
                self.player.result(0)
            if i[1] == 2:  # player blackjack
                self.player.result(i[0] + i[0] * 1.5)
                self.result(-(i[0] * 1.5))
            if i[1] == 3:  # player won
                self.player.result(i[0] * 2)
                self.result(-i[0])

    def __receive_card(self, card):
        super().receive_card(card, 0)
        if len(self.hand[0]) == 2:
            print(f'Dealer hand: [{self.hand[0][0]}, [x, xxxxx]]')

    def evaluate(self, a_hand):

        self.d_h_sum = self.__count_sum(self.hand[0])
        p_h_sum = self.__count_sum(a_hand)

        if (self.status == 5):

            if (len(self.hand[0]) == 2 and (self.hand[0][0][0] == 1 or self.hand[0][1][0] == 1) and
                    (self.hand[0][0][0] >= 10 or self.hand[0][1][0] >= 10)):

                if (len(a_hand) == 2 and (a_hand[0][0] == 1 or a_hand[1][0] == 1) and
                        (a_hand[0][0] >= 10 or a_hand[1][0] >= 10)):
                    print('----------------DRAW! PLAYER AND DEALER BLACKJACK-----------------')
                    return 0
                else:
                    print('------------------------DEALER BLACKJACK!-------------------------')
                    return 1
            if len(a_hand) == 2 and (a_hand[0][0] == 1 or a_hand[1][0] == 1) and (
                    a_hand[0][0] >= 10 or a_hand[1][0] >= 10):
                print('------------------------PLAYER BLACKJACK!-------------------------')
                return 2

            if (self.d_h_sum > 21 and p_h_sum > 21):
                print('----------------DEALER WON! PLAYER AND DEALER BUST-----------------')
                return 1
            elif (self.d_h_sum > 21):
                print('-----------------------PLAYER WON, DEALER BUST!-------------------------')
                return 3
            elif (p_h_sum > 21):
                print('-----------------------DEALER WON, PLAYER BUST!-------------------------')
                return 1

            if p_h_sum > self.d_h_sum and p_h_sum <= 21:
                print('---------------------------PLAYER WON!----------------------------')
                return 3
            elif p_h_sum == self.d_h_sum:
                print('----------------DRAW! PLAYER AND DEALER SAME VALUE-----------------')
                return 0
            else:
                print('---------------------------DEALER WON!----------------------------')
                return 1

        elif p_h_sum >= 21:
            return 7

        return 6

    def __count_sum(self, hand):
        hand_sum = 0
        aces = 0
        for i in hand:
            if (i[0] == 1):
                aces += 1
                continue
            elif (i[0] >= 10):
                hand_sum += 10
                continue
            hand_sum += i[0]
        for i in range(aces):
            if hand_sum + 11 > 21:
                hand_sum += 1
            else:
                hand_sum += 11
        return (hand_sum)


# UTILITY FUNCTIONS

def user_input(string=None, integer=False, legals=None):
    while True:
        if integer != False:
            try:
                return int(input())
            except ValueError:
                print('Insert valid integer amount')
        else:
            temp = str(input(string)).lower()
            temp.lower()
            if temp in legals:
                return temp
            else:
                print(f'You cant do that, your legal actions are {legals}')


# about, rules, strategy


def display_strategy_table():
    webbrowser.open('https://www.blackjackapprenticeship.com/wp-content/uploads/2018/08/BJA_Basic_Strategy.jpg')


def load_info_from_web():
    response = requests.get('http://www.hitorstand.net/strategy.php').text
    soup = BeautifulSoup(response, features='lxml')

    with open('Black_jack_info.txt', 'w') as f:
        f.write(
            ' <intro> ' + soup.p.text + ' <intro> ' + ' <h2> ' + soup.h1.text + ' <h2> ' + ' <rules> ' + soup.ul.text + ' <rules> ')


def word_for_word_generator():
    with open('Black_jack_info.txt', 'r') as f:
        for line in f:
            for word in line.split():
                yield (word)


def reader(flag, information, inf_dict):
    count = 0
    paragraph = ''
    flag_word = False
    if flag in inf_dict:
        print('--------------------------------------------------------------')
        print(inf_dict[flag])
    else:
        for word in information:
            if word.startswith('<') and word.endswith('>') and word != flag_word:
                flag_word = word
            elif word == flag_word:
                inf_dict[word] = paragraph
                flag_word = False
                paragraph = ''

            if information != None:
                if flag == word:
                    count += 1
                    if count == 2:
                        print('--------------------------------------------------------------')
                        print(inf_dict[flag])
                        break
                elif not word.startswith('<') and not word.endswith('>'):
                    paragraph += word + ' '
                    if word.endswith('.'):
                        paragraph += '\n'


def start_decor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('This is a game of Blackjack that I have designed, rules are the standard rules, without any add-ons')
        func(*args, **kwargs)

    return wrapper


@start_decor
def rules_and_info(information, inf_dict):
    while True:
        inp = str(input(
            'To start game type hit enter, for introduction type "intro", for rules type "rules" for strategy type "strategy"')).lower()
        if inp == 'intro':
            reader('<intro>', information, inf_dict)
        elif inp == 'rules':
            reader('<h2>', information, inf_dict)
            reader('<rules>', information, inf_dict)
        elif inp == '':
            break
        elif inp == 'strategy':
            display_strategy_table()


# GAME LOOP

def game_loop():
    # Load data to file from website
    load_info_from_web()
    # create generator
    info = word_for_word_generator()
    info_dict = {}  # dict for storing info

    rules_and_info(info, info_dict)

    while True:

        deck = Deck()
        dealer = Dealer(deck=deck)
        player = Player(dealer)
        dealer.add_player(player)
        deck.shuffle()

        while (dealer.game_status == 1 and player.game_status == 1):
            player.hand = [[]]
            dealer.hand = [[]]
            player.bet = [[]]

            print('New Round!')
            print(f'Player place your bet!, your balance is {player.cash}')
            player.place_bet(user_input(integer=True))

            dealer.deal(target=1, idx=0)
            dealer.deal(target=0, idx=0)
            dealer.deal(target=1, idx=0)
            dealer.deal(target=0, idx=0)

            control_idx = 0

            while (control_idx + 1) <= len(player.hand):
                print('------------------------------------------------------------------')

                status = dealer.evaluate(player.hand[control_idx])
                if status == 7:
                    print(f'status: {status}')
                    control_idx += 1
                    continue

                if len(player.hand) >= 2:
                    print(f'You are currently playing on this hand: {player.hand[control_idx]}')

                if (len(player.hand[control_idx]) == 2 and player.hand[control_idx][0][0] ==
                        player.hand[control_idx][1][0]
                        and player.bet[control_idx] <= player.cash):
                    player_decision = user_input(string='player make your move, you can hit,stand,double or split!',
                                                 legals=['hit', 'stand', 'double', 'split'])
                    if player_decision == 'split':
                        player.split(0)
                        player.place_bet(target=control_idx)
                        player.hit(-1)
                        player.hit(-2)
                        continue

                    if player_decision == 'double':
                        player.place_bet(target=control_idx, double=True)
                        player.hit(control_idx)
                        control_idx += 1
                        continue

                elif len(player.hand[control_idx]) == 2 and player.bet[control_idx] <= player.cash:
                    player_decision = user_input(string='Player make your move, you can hit,stand or double!',
                                                 legals=['hit', 'stand', 'double'])
                    if player_decision == 'double':
                        player.place_bet(target=control_idx, double=True)
                        player.hit(control_idx)
                        control_idx += 1
                        continue

                else:
                    player_decision = user_input(string='Player make your move, you can hit or stand!',
                                                 legals=['hit', 'stand'])

                if player_decision == 'hit':
                    player.hit(control_idx)
                    status = dealer.evaluate(player.hand[control_idx])
                    if status == 7:
                        control_idx += 1
                    continue
                if player_decision == 'stand':
                    control_idx += 1
                    continue

            if len(player.hand) < control_idx + 1:
                while (dealer.d_h_sum < 17):
                    dealer.deal(0)
                    dealer.d_h_sum = dealer._Dealer__count_sum(dealer.hand[0])
                else:
                    print(f'DEALER FINAL HAND: {dealer.hand}')

                dealer.status = 5
                for i in range(len(player.hand)):
                    status = dealer.evaluate(player.hand[i])
                    player.bet[i] = (player.bet[i], status)
                control_idx = len(player.hand) - 1

            dealer.status = 6  # hand played

            dealer.round_over(player.bet)
            dealer.status = 6
            control_idx = 0

            if dealer.game_status != 1:
                print(dealer.game_status)
            elif player.game_status != 1:
                print(player.game_status)
        while True:
            inp = str(input('Play agian, "yes" or "no" ')).lower()
            if inp == 'yes':
                break
            if inp == 'no':
                break
        if inp == 'no':
            break

game_loop()

