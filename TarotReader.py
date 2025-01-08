import json
import time
from Cards import Card
from Spreads import Spread

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

def load_data_from_json(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data

card_data = load_data_from_json("cards_data.json")
major_arcana = Card.create_major_arcana(card_data)
minor_arcana = Card.create_minor_arcana(card_data)
spread_data = load_data_from_json("spreads.json")

print("Hello and welcome to Casper's Veil.")
input()

input("Please choose a spread for a peak into your matter: ")
for index, spreads in enumerate(spread_data, start = 1):
    print(f"{index}. Name: {spreads['name']}")
    print(f"   Description: {spreads['description']}\n")
prefered_spread = int(input("So, what's it gonna be? : "))

print("\nI had a feeling you'd choose that one!\n")
time.sleep(1)

deck = major_arcana + minor_arcana
Spread.shuffle(deck)

picking_cards_timer()
spread = Spread("", {1: "past", 2: "present", 3: "future"})
for _ in range(3):
    spread.draw_card(deck)

interpretation = spread.interpret()
print(interpretation)