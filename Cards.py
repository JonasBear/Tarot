import sqlite3

class Card:
    def __init__(self, id=None, name="", suit=None, upright_meaning="", reversed_meaning=""):
        self.id = id
        self.name = name
        self.suit = suit
        self.upright_meaning = upright_meaning
        self.reversed_meaning = reversed_meaning
    
    @staticmethod
    def load_cards_from_db():
        conn = sqlite3.connect("./veilArchive.db")
        c = conn.cursor()

        # Major arcana
        c.execute("SELECT id, name, upright_meaning, reversed_meaning FROM cards WHERE arcana_type='major'")
        major = [
            Card(id, name, upright, reversed_,)
            for id, name, upright, reversed_ in c.fetchall()
        ]

        # Minor arcana
        c.execute("SELECT id, name, suit, upright_meaning, reversed_meaning FROM cards WHERE arcana_type='minor'")
        minor = [
            Card(id, name, suit, upright, reversed_,)
            for id, name, suit, upright, reversed_ in c.fetchall()
        ]

        conn.close()
        return major, minor
        
    def get_meaning(self, is_reversed):
        return self.reversed_meaning if is_reversed else self.upright_meaning
    