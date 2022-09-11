import random as rd
import sys
import statistics as st
import matplotlib.pyplot as plt
from time import time

# borrowed from Blackjack project
CARD_SUITS = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
CARD_SUIT_SYMBOLS = {'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'}
CARD_RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class Card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
		self.value = self.get_value()
		self.name = self.get_name()

	def get_value(self):
		if self.rank == 'A':
			return 11
		elif self.rank == 'J' or self.rank == 'Q' or self.rank == 'K':
			return 10
		else:
			return int(self.rank)

	def get_name(self):
		return self.rank + CARD_SUIT_SYMBOLS[self.suit]
	def __repr__(self):
		return self.name

def create_deck():
	deck = []
	for suit in CARD_SUITS:
		for rank in CARD_RANKS:
			deck.append(Card(suit, rank))
	return deck

def hit(cards, deck):
	cards.append(deck.pop(rd.randint(0, len(deck) - 1)))
	c = 0
	while sum(c.value for c in cards) > 21 and c < len(cards):
		if cards[c].rank == 'A':
			cards[c].value = 1
		c += 1
	return cards

# we want to win the round with 3 hits or more (so 5 cards in hand)
def round():
	deck = create_deck()
	player_cards = []
	dealer_cards = []
	player_score = 0
	dealer_score = 0
	while len(player_cards) < 2:
		player_cards = hit(player_cards, deck)
		dealer_cards = hit(dealer_cards, deck)
		player_score = sum(c.value for c in player_cards)
		dealer_score = sum(c.value for c in dealer_cards)
		if player_score == 21 or dealer_score == 21: # blackjack, so no hits
			return 0
	while player_score < 21 and len(player_cards) < 5:
		player_cards = hit(player_cards, deck)
		player_score = sum(c.value for c in player_cards)
		if player_score > 21: # bust
			return 0
		elif player_score == 21: break
	while dealer_score < 17:
		dealer_cards = hit(dealer_cards, deck)
		dealer_score = sum(c.value for c in dealer_cards)
		if dealer_score > 21: # dealer bust
			if len(player_cards) >= 5: # 5-card win
				return 1
			else:
				return 0
		elif dealer_score == 21: break
	if player_score > dealer_score: # player win
		if len(player_cards) >= 5: # 5-card win
			return 1
		else:
			return 0
	elif player_score <= dealer_score: # dealer win or draw
		return 0

# we want to do it 3 times (see RDR2 gambler challenge rank 8)
def play():
	fives = 0
	rounds = 0
	while fives < 3:
		fives += round()
		rounds += 1
	# print(f"Rounds: {rounds}, 5-card wins: {fives}, 5-card win rate: {fives / rounds * 100:.2f}%")
	return rounds

def main():
	if len(sys.argv) != 2 or not sys.argv[1].isdigit():
		print("Please specify the number of simulation loops.")
	else: 
		rounds = []
		tStart = time()
		for i in range(int(sys.argv[1])):
			rounds.append(play())
		tEnd = time()
		mode = st.multimode(rounds)
		print(f"Simulation time: {tEnd - tStart:.2f}s")
		print(f"Average rounds: {st.mean(rounds):.2f}")
		print(f"Median rounds: {st.median(rounds)}")
		print(f"Standard deviation: {st.stdev(rounds):.2f}")
		print(f"Mode: {mode[0] if len(mode) == 1 else mode}")
		print(f"Max rounds: {max(rounds)}")
		print(f"Min rounds: {min(rounds)}")
		plt.grid(which='both'), plt.xlabel('Rounds'), plt.ylabel('Frequency')
		plt.hist(rounds, bins=range(1, max(rounds) + 2))
		plt.show()

if __name__ == '__main__':
	main()