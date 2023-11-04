import socket
import pickle
from account_database import AccountDatabase


def handle_request(data, db):
    command, *args = data

    if command == "create_account":
        user_id = db.create_account()
        return user_id
    elif command == "get_balance":
        user_id = args[0]
        balance = db.get_balance(user_id)
        return balance
    elif command == "process_transaction":
        sender_id, receiver_id, amount = args
        result = db.process_transaction(sender_id, receiver_id, amount)
        return result
    elif command == "view_table":
        user_table = db.get_all_users()
        return user_table
    else:
        return "Invalid command"


def main():
    host = "127.0.0.1"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server is listening on {}:{}".format(host, port))

    db = AccountDatabase()  # Create an instance of the AccountDatabase class

    while True:
        client_socket, address = server_socket.accept()
        print(f"Accepted connection from {address}")

        data = client_socket.recv(1024)
        if not data:
            break

        request = pickle.loads(data)
        response = handle_request(request, db)  # Use the AccountDatabase instance for processing

        client_socket.send(pickle.dumps(response))
        client_socket.close()

    db.close()  # Close the database connection when the server exits


if __name__ == "__main__":
    main()
