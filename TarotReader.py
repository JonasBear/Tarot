import json
import random
from Cards import Card
from Spreads import Spread

# Function to load card data from the JSON file
def load_cards_from_json(filename="cards_data.json"):
    with open(filename, "r") as file:
        data = json.load(file)
    return data

# Create the deck using the loaded JSON data
card_data = load_cards_from_json()
major_arcana = Card.create_major_arcana(card_data)
minor_arcana = Card.create_minor_arcana(card_data)
deck = major_arcana + minor_arcana
random.shuffle(deck)

simple_draw = Spread("simple three card spread", {1: "past", 2: "present", 3: "future"})

for _ in range(len(simple_draw.positions)):
    simple_draw.draw_card(deck)

interpretation = simple_draw.interpret()
print(interpretation)