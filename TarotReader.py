import sqlite3
import time
from Cards import Card
from Spreads import Spread

def generate_spread(major_arcana, minor_arcana, spread_data):
    if (spread_data['deck_used'] == 1):
        deck = major_arcana + minor_arcana
    else:
        deck = major_arcana
        
    Spread.shuffle(deck)
    spread = Spread(spread_data['name'],spread_data['positions'])
    for _ in range(spread_data['number_of_cards']):
        spread.draw_card(deck)
    interpretation = spread.interpret()
    print_interpretation(interpretation)

def print_interpretation(interpretation):
    for index, (position, card_info) in enumerate(interpretation.items(), start=1):
        print((f"{index}. " if len(interpretation)>1 else "") + position)
        print(f"Card Name: {card_info['card']}"+ (", Reversed" if card_info['reverse'] else ""))
        if (card_info['suit'] != None):
            print(f"Suit: {card_info['suit']}")
        print(f"Meaning: {card_info['meaning']}")
        print()

major_arcana, minor_arcana = Card.load_cards_from_db()
spread_data = Spread.load_spreads_from_db()

print("Hello and welcome to Casper's Veil.")
input()

for index, spreads in enumerate(spread_data, start = 1):
    print(f"{index}. Name: {spreads['name']}")
    print(f"   Description: {spreads['description']}\n")
prefered_spread = int(input("So, what's it gonna be? : "))

generate_spread(major_arcana, minor_arcana, spread_data[prefered_spread-1])