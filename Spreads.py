import random
import sqlite3

class Spread:
    def __init__(self, spread_id, spread_name, positions):
        self.spread_id = spread_id
        self.spread_name = spread_name
        self.positions = positions  
        self.cards = []  # List to hold drawn cards
    
    @staticmethod
    def load_spreads_from_db():
        conn = sqlite3.connect("veilArchive.db")
        c = conn.cursor()
        c.execute("SELECT id, name, description, number_of_cards, deck_used FROM spreads")
        spreads = []
        for spread_id, name, desc, num_cards, deck_used in c.fetchall():
            c.execute("SELECT position_index, position_name FROM spread_positions WHERE spread_id=?", (spread_id,))
            positions = {pos: name for pos, name in c.fetchall()}
            spreads.append({"id": spread_id, "name": name, "description": desc, "number_of_cards": num_cards, "positions": positions, "deck_used": deck_used})
        conn.close()
        return spreads

    @staticmethod
    def shuffle(deck):
        return random.shuffle(deck)
    
    def draw_card(self, deck):
        is_reversed = random.choice([True,False])
        card = random.choice(deck)
        self.cards.append({
            "card": card,
            "reversed": is_reversed
        })
        deck.remove(card)
        return deck
    
    def interpret(self):
        interpretation = {}
        for idx, card_info in enumerate(self.cards):
            card = card_info["card"]
            is_reversed = card_info["reversed"]
            position = self.positions[idx+1]
            interpretation[position] = {
                "id": card.id,
                "card": card.name,
                "suit": card.suit,
                "reverse": is_reversed,
                "meaning": card.get_meaning(is_reversed)
            }
        self.cards.clear()
        return interpretation
