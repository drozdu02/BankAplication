import sqlite3

class DataBase:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('bank_database.db')
        self.cursor = self.conn.cursor()
        self.create_clients_table()

    def create_clients_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                client_id TEXT PRIMARY KEY,
                balance REAL,
                limit_withdrawal INTEGER,
                login_pin TEXT,
                help_question TEXT
            )
        ''')
        self.conn.commit()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def fetch_one(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()