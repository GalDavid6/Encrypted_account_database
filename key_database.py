import sqlite3


class KeysDatabase:
    def __init__(self, database_name="keys_database.db"):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        # Create the keys table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS keys (
                user_id INTEGER PRIMARY KEY,
                enc STRING,
                dec STRING
            )
        ''')
        self.connection.commit()

    def insert_keys(self, s, h):
        self.cursor.execute("INSERT INTO keys (enc, dec) VALUES (?,?)", (str(s), str(h),))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_keys(self, user_id):
        self.cursor.execute("SELECT enc, dec FROM keys WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return int(result[0]), int(result[1])
