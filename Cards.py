import json

class Card:
    def __init__(self, name, suit=None, upright_meaning="", reversed_meaning=""):
        self.name = name
        self.suit = suit
        self.upright_meaning = upright_meaning
        self.reversed_meaning = reversed_meaning

    @staticmethod
    def create_major_arcana(data):
        major_arcana = []
        for card_data in data["major_arcana"]:
            card = Card(
                name=card_data["name"],
                upright_meaning=card_data["upright_meaning"],
                reversed_meaning=card_data["reversed_meaning"]
            )
            major_arcana.append(card)
        return major_arcana

    @staticmethod
    def create_minor_arcana(data):
        suits = ["Cups", "Pentacles", "Swords", "Wands"]
        minor_arcana = []
        for card_data in data["minor_arcana"]:
            # Split the name into rank and suit
            name_parts = card_data["name"].split(" of ")
            card = Card(
                name=card_data["name"],
                suit=card_data["suit"],
                upright_meaning=card_data["upright_meaning"],
                reversed_meaning=card_data["reversed_meaning"]
            )
            minor_arcana.append(card)
        return minor_arcana
    
    def get_meaning(self, is_reversed):
        return self.reversed_meaning if is_reversed else self.upright_meaning
