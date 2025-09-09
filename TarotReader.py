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
    spread = Spread(spread_data['id'], spread_data['name'],spread_data['positions'])
    for _ in range(spread_data['number_of_cards']):
        spread.draw_card(deck)
    interpretation = spread.interpret()
    save_reading(spread, interpretation)
    print_interpretation(interpretation)

def save_reading(spread, interpretation):
    conn = sqlite3.connect("veilArchive.db")
    c = conn.cursor()

    # Insert the reading
    c.execute("INSERT INTO readings (spread_id) VALUES (?)", (spread.spread_id,))
    reading_id = c.lastrowid

    # Insert each drawn card
    for pos_index, (position, card_info) in enumerate(interpretation.items(), start=1):
        card_id = card_info['id']

        c.execute(
            "INSERT INTO reading_cards (reading_id, card_id, position_index, is_reversed) VALUES (?, ?, ?, ?)",
            (reading_id, card_id, pos_index, card_info["reverse"])
        )

    conn.commit()
    conn.close()


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