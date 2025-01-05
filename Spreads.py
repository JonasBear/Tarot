import random
class Spread:
    def __init__(self, spread_name, positions):
        self.spread_name = spread_name
        self.positions = positions  # Dictionary of positions (e.g., {1: "past", 2: "present"})
        self.cards = []  # List to hold drawn cards

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
            position = self.positions[idx + 1]  # Get position meaning from positions map
            interpretation[position] = {
                "card": card.name,
                "suit": card.suit,
                "reverse": is_reversed,
                "meaning": card.get_meaning(is_reversed)
            }
        return interpretation
