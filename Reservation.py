import sqlite3

class ReservationDatabase:
    def __init__(self, db_name="restaurant.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT NOT NULL,
                table_number INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def add_reservation(self, user_id, date, table_number, price):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO reservations (user_id, date, table_number, price) VALUES (?, ?, ?, ?)',
                       (user_id, date, table_number, price))
        self.conn.commit()
        print(f"\nYour reservation (Date: {date}, Table number: {table_number}, Price: {price})")


    def delete_reservation(self, reservation_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM reservations WHERE id=?', (reservation_id,))
        self.conn.commit()

    def filter_reservations(self, user_id=None, date=None):
        cursor = self.conn.cursor()
        if user_id is not None:
            cursor.execute('SELECT * FROM reservations WHERE user_id=?', (user_id,))
        elif date is not None:
            cursor.execute('SELECT * FROM reservations WHERE date=?', (date,))
        else:
            cursor.execute('SELECT * FROM reservations')
        return cursor.fetchall()

    def close_connection(self):
        self.conn.close()