import sqlite3
from Cards import Card
from Spreads import Spread

class TarotReader:
    def __init__(self):
        self.major_arcana, self.minor_arcana = Card.load_cards_from_db()
        self.spreads = Spread.load_spreads_from_db()

    def generate_spread(self, spread_index):
        spread_data = self.spreads[spread_index]

        # Build deck
        if spread_data['deck_used'] == 1:
            deck = self.major_arcana + self.minor_arcana
        else:
            deck = self.major_arcana

        Spread.shuffle(deck)
        spread = Spread(spread_data['id'], spread_data['name'], spread_data['positions'])

        for _ in range(spread_data['number_of_cards']):
            spread.draw_card(deck)

        interpretation = spread.interpret()
        TarotReader.save_reading(spread, interpretation)

        return interpretation

    def save_reading(spread, interpretation, max_readings=20):
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

        # Enforce max readings
        c.execute("SELECT COUNT(*) FROM readings")
        total_readings = c.fetchone()[0]

        if total_readings > max_readings:
            # Find oldest readings to delete
            excess = total_readings - max_readings
            c.execute("SELECT id FROM readings ORDER BY id ASC LIMIT ?", (excess,))
            old_ids = [row[0] for row in c.fetchall()]

            # Delete associated reading_cards first
            c.executemany("DELETE FROM reading_cards WHERE reading_id=?", [(rid,) for rid in old_ids])
            # Then delete readings
            c.executemany("DELETE FROM readings WHERE id=?", [(rid,) for rid in old_ids])

        conn.commit()
        conn.close()

    def get_spreads(self):
        return self.spreads
    
    def get_history():
        conn = sqlite3.connect("veilArchive.db")
        c = conn.cursor()

        c.execute("""
            SELECT r.id, r.created_at, s.name
            FROM readings r
            JOIN spreads s ON r.spread_id = s.id
            ORDER BY r.created_at DESC
        """)
        readings = c.fetchall()

        if not readings:
            print("No readings found in history.")
            conn.close()
            return

        print("\nYour past readings:\n")
        for idx, (reading_id, date, spread_name) in enumerate(readings, start=1):
            print(f"{idx}. Date: {date} | Spread: {spread_name}")

        choice = int(input("\nWhich reading would you like to view? : "))
        chosen_reading_id = readings[choice - 1][0]

        c.execute("""
            SELECT 
                rc.position_index,
                sp.position_name,
                c.id,
                c.name,
                c.suit,
                rc.is_reversed,
                c.upright_meaning,
                c.reversed_meaning
            FROM reading_cards rc
            JOIN cards c ON rc.card_id = c.id
            JOIN readings r ON rc.reading_id = r.id
            JOIN spreads s ON r.spread_id = s.id
            JOIN spread_positions sp 
                ON rc.position_index = sp.position_index 
            AND sp.spread_id = s.id
            WHERE rc.reading_id = ?
            ORDER BY rc.position_index ASC
        """, (chosen_reading_id,))
        rows = c.fetchall()
        conn.close()

        print("\nHere’s your reading:\n")
        for i, (pos_idx, pos_name, card_id, card_name, suit, is_reversed, upright, reversed_) in enumerate(rows, start=1):
            print((f"{i}. " if len(rows) > 1 else "") + pos_name)
            print(f"Card Name: {card_name}" + (", Reversed" if is_reversed else ""))
            if suit:
                print(f"Suit: {suit}")
            meaning = reversed_ if is_reversed else upright
            print(f"Meaning: {meaning}\n")
