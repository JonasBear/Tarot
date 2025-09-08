import sqlite3, json
from Cards import Card

conn = sqlite3.connect("tarot.db")
c = conn.cursor()

# Load JSON
with open("cards_data.json", "r") as f:
    card_data = json.load(f)

major_arcana = Card.create_major_arcana(card_data)
minor_arcana = Card.create_minor_arcana(card_data)

# Insert cards
for card in major_arcana + minor_arcana:
    c.execute(
        "INSERT INTO cards (name, suit, upright_meaning, reversed_meaning) VALUES (?, ?, ?, ?)",
        (card.name, card.suit, card.upright_meaning, card.reversed_meaning)
    )

with open("spreads.json", "r") as f:
    spread_data = json.load(f)

with open("spreads.json", "r") as f:
    spreads_data = json.load(f)

for spread in spreads_data:
    # Insert the spread
    c.execute(
        "INSERT INTO spreads (name, description, number_of_cards) VALUES (?, ?, ?)",
        (spread["name"], spread["description"], spread["number_of_cards"])
    )
    spread_id = c.lastrowid  # get the spread id we just inserted

    # Insert positions
    for pos_index, pos_name in spread["positions"].items():
        c.execute(
            "INSERT INTO spread_positions (spread_id, position_index, position_name) VALUES (?, ?, ?)",
            (spread_id, int(pos_index), pos_name)
        )

conn.commit()
conn.close()