import sqlite3

class Card:
    def __init__(self, name, suit=None, upright_meaning="", reversed_meaning=""):
        self.name = name
        self.suit = suit
        self.upright_meaning = upright_meaning
        self.reversed_meaning = reversed_meaning
    
    @staticmethod
    def load_cards_from_db():
        conn = sqlite3.connect("veilarchive.db")
        c = conn.cursor()

        # Major arcana
        c.execute("SELECT name, suit, upright_meaning, reversed_meaning FROM cards WHERE arcana_type='major'")
        major = [
            Card(name, upright, reversed_,)
            for name, upright, reversed_ in c.fetchall()
        ]

        # Minor arcana
        c.execute("SELECT name, suit, upright_meaning, reversed_meaning FROM cards WHERE arcana_type='minor'")
        minor = [
            Card(name, suit, upright, reversed_,)
            for name, suit, upright, reversed_ in c.fetchall()
        ]

        conn.close()
        return major, minor
        
    def get_meaning(self, is_reversed):
        return self.reversed_meaning if is_reversed else self.upright_meaning
    