import sqlite3
from elgamal_encryption import encrypt, decrypt, keys_initializer


class AccountDatabase:
    def __init__(self, database_name="account_database.db"):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        # Create the accounts table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                user_id INTEGER PRIMARY KEY,
                balance BLOB
            )
        ''')
        self.connection.commit()

    def create_account(self):
        # Creating keys
        key_id = keys_initializer()
        # Encrypt the default value
        encrypted_msg = encrypt('0', key_id)
        # Insert the encrypted balance into the database
        self.cursor.execute("INSERT INTO accounts (balance) VALUES (?)", (encrypted_msg,))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_balance(self, user_id):
        self.cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            # Decrypt the balance using the loaded keys
            decrypted_balance = decrypt(result[0], user_id)
            return int(decrypted_balance)
        else:
            return "User does not exist. Try again."

    def process_transaction(self, sender_id, receiver_id, amount):
        self.cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (sender_id,))
        sender_row = self.cursor.fetchone()
        self.cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (receiver_id,))
        receiver_row = self.cursor.fetchone()
        if sender_row and receiver_row:
            sender_balance = self.get_balance(sender_id)
            receiver_balance = self.get_balance(receiver_id)
            sender_balance -= amount
            receiver_balance += amount
            # Encrypt the updated balances before storing them in the database
            sender_balance_encrypted = encrypt(str(sender_balance), sender_id)
            receiver_balance_encrypted = encrypt(str(receiver_balance), receiver_id)
            self.cursor.execute("UPDATE accounts SET balance = ? WHERE user_id = ?",
                                (sender_balance_encrypted, sender_id))
            self.cursor.execute("UPDATE accounts SET balance = ? WHERE user_id = ?",
                                (receiver_balance_encrypted, receiver_id))
            self.connection.commit()
            return "Completed!"
        else:
            return "Error!"

    def get_all_users(self):
        self.cursor.execute("SELECT user_id, balance FROM accounts")
        results = self.cursor.fetchall()
        user_table = []

        for user_id, balance in results:
            user_table.append((user_id, balance))

        return user_table

    def close(self):
        self.connection.close()
