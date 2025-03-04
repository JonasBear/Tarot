import json
import time
from Cards import Card
from Spreads import Spread

def load_data_from_json(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data

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

def picking_cards_timer():
    print("Please give me a second to hear the calling of the right cards for you...")
    time.sleep(2)
    print(".")
    time.sleep(1)
    print("..")
    time.sleep(1)
    print("...\n")
    time.sleep(1)
    print("These cards seem to show a strong energy in your presence:\n")

card_data = load_data_from_json("cards_data.json")
major_arcana = Card.create_major_arcana(card_data)
minor_arcana = Card.create_minor_arcana(card_data)
spread_data = load_data_from_json("spreads.json")

print("Hello and welcome to Casper's Veil.")
input()

print("Please choose a spread for a peek into your matter: ")
time.sleep(2)
for index, spreads in enumerate(spread_data, start = 1):
    print(f"{index}. Name: {spreads['name']}")
    print(f"   Description: {spreads['description']}\n")
prefered_spread = int(input("So, what's it gonna be? : "))

print("\nI had a feeling you'd choose that one!\n")
time.sleep(1)

picking_cards_timer()

generate_spread(major_arcana, minor_arcana, spread_data[prefered_spread-1])