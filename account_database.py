import sqlite3
from encryption import initialize_keys, encrypt_message, decrypt_message


class AccountDatabase:
    def __init__(self, database_name="account_database.db"):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        # Initialize keys (if not already done)
        initialize_keys()
        # Create the accounts table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                user_id INTEGER PRIMARY KEY,
                balance BLOB
            )
        ''')
        self.connection.commit()

    def create_account(self):
        # Encrypt the initial balance (0) using the loaded keys
        encrypted_balance = encrypt_message(str(0))
        # Insert the encrypted balance into the database
        self.cursor.execute("INSERT INTO accounts (balance) VALUES (?)", (encrypted_balance,))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_balance(self, user_id):
        self.cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            # Decrypt the balance using the loaded keys
            decrypted_balance = decrypt_message(result[0])
            return float(decrypted_balance)
        else:
            return "User does not exist. Try again."

    def process_transaction(self, sender_id, receiver_id, amount):
        sender_balance = self.get_balance(sender_id)
        receiver_balance = self.get_balance(receiver_id)
        if sender_balance is not None and receiver_balance is not None:
            # Update the balances
            sender_balance -= amount
            receiver_balance += amount
            # Encrypt the updated balances using the loaded keys
            sender_balance_encrypted = encrypt_message(str(sender_balance))
            receiver_balance_encrypted = encrypt_message(str(receiver_balance))
            # Update the encrypted balances in the database
            self.cursor.execute("UPDATE accounts SET balance = ? WHERE user_id = ?", (sender_balance_encrypted, sender_id))
            self.cursor.execute("UPDATE accounts SET balance = ? WHERE user_id = ?", (receiver_balance_encrypted, receiver_id))
            self.connection.commit()
            return "Completed!"
        else:
            return "Error!"

    def get_all_users(self):
        self.cursor.execute("SELECT user_id, balance FROM accounts")
        results = self.cursor.fetchall()
        user_table = []

        for user_id, balance in results:
            # Decrypt the balances using the loaded keys
            decrypted_balance = decrypt_message(balance)
            user_table.append((user_id, float(decrypted_balance)))

        return user_table

    def close(self):
        self.connection.close()





# class AccountDatabase:
#     def __init__(self, database_name="account_database.db", key_file="elgamal_keys.text"):
#         self.connection = sqlite3.connect(database_name)
#         self.cursor = self.connection.cursor()
#         self.public_key, self.private_key = self._load_keys(key_file)
#
#         # Create the accounts table if it doesn't exist
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS accounts (
#                 user_id INTEGER PRIMARY KEY,
#                 balance REAL
#             )
#         ''')
#         self.connection.commit()
#
#     @staticmethod
#     def _load_keys(key_file):
#         try:
#             # Try to load keys from the file
#             public_key, private_key = load_keys(key_file)
#         except FileNotFoundError:
#             # If the file doesn't exist, generate new keys
#             public_key, private_key = generate_keys()
#             save_keys(public_key, private_key, key_file)
#         return public_key, private_key
#
#     def create_account(self):
#         # Encrypt the initial balance before storing it in the database
#         encrypted_balance = encrypt(self.public_key, str(0).encode())
#         self.cursor.execute("INSERT INTO accounts (balance) VALUES (?)", encrypted_balance)
#         self.connection.commit()
#         return self.cursor.lastrowid
#
#     def get_balance(self, user_id):
#         self.cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (user_id,))
#         result = self.cursor.fetchone()
#         if result:
#             # Decrypt the balance and convert it to a float
#             decrypted_balance = decrypt(self.private_key, bytes(result[0]))
#             return float(decrypted_balance)
#         else:
#             return "User not exist, Try again."
#
#     def process_transaction(self, sender_id, receiver_id, amount):
#         self.cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (sender_id,))
#         sender_row = self.cursor.fetchone()
#         self.cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (receiver_id,))
#         receiver_row = self.cursor.fetchone()
#         if sender_row and receiver_row:
#             sender_balance = self.get_balance(sender_id)
#             receiver_balance = self.get_balance(receiver_id)
#             sender_balance -= amount
#             receiver_balance += amount
#             # Encrypt the updated balances before storing them in the database
#             sender_balance_encrypted = encrypt(self.public_key, str(sender_balance).encode())
#             receiver_balance_encrypted = encrypt(self.public_key, str(receiver_balance).encode())
#             self.cursor.execute("UPDATE accounts SET balance = ? WHERE user_id = ?",
#                                 (sender_balance_encrypted, sender_id))
#             self.cursor.execute("UPDATE accounts SET balance = ? WHERE user_id = ?",
#                                 (receiver_balance_encrypted, receiver_id))
#             self.connection.commit()
#             return "Completed!"
#         else:
#             return "Error!"
#
#     # def process_transaction(self, sender_id, receiver_id, amount):
#     #     self.cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (sender_id,))
#     #     sender_row = self.cursor.fetchone()
#     #     self.cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (receiver_id,))
#     #     receiver_row = self.cursor.fetchone()
#     #     if sender_row and receiver_row:
#     #         self.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE user_id = ?", (amount, sender_id))
#     #         self.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE user_id = ?", (amount, receiver_id))
#     #         self.connection.commit()
#     #         return "Completed!"
#     #     else:
#     #         return "Error!"
#
#     def get_all_users(self):
#         self.cursor.execute("SELECT user_id, balance FROM accounts")
#         return self.cursor.fetchall()
#
#     def close(self):
#         self.connection.close()
