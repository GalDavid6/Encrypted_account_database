import socket
import pickle
from account_database import AccountDatabase  # Import the modified AccountDatabase class


def send_request(host, port, request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Create an instance of the AccountDatabase class
    db = AccountDatabase()

    request_data = pickle.dumps(request)
    client_socket.send(request_data)

    response_data = client_socket.recv(1024)
    response = pickle.loads(response_data)

    client_socket.close()

    db.close()  # Close the database connection

    return response


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 12345

    while True:
        print("Options:")
        print("1. Create Account")
        print("2. Get Balance")
        print("3. Process Transaction")
        print("4. View All Users")
        print("5. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            response = send_request(host, port, ["create_account"])
            print("New User Created With ID:", response)
        elif choice == "2":
            user_id = input("Enter User ID: ")
            response = send_request(host, port, ["get_balance", user_id])
            print("Balance:", response)
        elif choice == "3":
            sender_id = input("Enter Sender ID: ")
            receiver_id = input("Enter Receiver ID: ")
            amount = int(input("Enter Amount: "))
            response = send_request(host, port, ["process_transaction", sender_id, receiver_id, amount])
            print("Transaction result:", response)
        elif choice == "4":
            response = send_request(host, port, ["view_table"])
            print("User ID | Balance")
            for user_id, balance in response:
                print(f"{user_id} | {balance}")
        elif choice == "5":
            break
        else:
            print("Invalid choice")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
