from peer import Peer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
import threading
from database import Database
import random
import sys

# Define the connection parameters
username = "postgres"
password = sys.argv[1] 
host_url = "localhost"
port = 5432
database_name = "postgres"
app_schema = "chat"

# Create the SQLAlchemy engine
connection_string = f"postgresql+psycopg2://{username}:{password}@{host_url}:{port}/{database_name}"
db = create_engine(connection_string, connect_args={"options": f"-csearch_path={app_schema}"})


def login_or_signup():
    while True:
        choice = input("Do you want to (l)ogin or (s)ign up? ").lower()
        if choice == 'l':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = Database.log_in(db, username, password)
            if user:
                print("Login successful!")
                return user
            else:
                print("Invalid username or password. Please try again.")
        elif choice == 's':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            if Database.log_in(db, username, password):
                print("Username already taken. Please choose a different username.")
            else:
                ip_addr = "localhost"
                port = random.randint(10000, 50000)
                ports_taken = Database.get_used_ports(db)
                unique_port = False
                while not unique_port:
                    if port in ports_taken:
                        port = random.randint(10000, 50000)
                    else:
                        unique_port = True
                Database.signup(db, username, password, ip_addr, port)
                print("Sign up successful! You can now login.")
        else:
            print("Invalid choice. Please choose 'l' for login or 's' for sign up.")


def display_active_users():
    active_users = Database.get_active_users(db)
    print("Active Users:")
    for i in range(len(active_users)):
        print(f"{i+1}. {active_users[i]}")


def logout(user):
    user.online = False
    print("Logout successful.")
    # Update user's online status in the database
    Database.update_user_status(db, user.user_name)


def main():
    # Initialize database connection
    # Prompt the user to login or sign up
    user = login_or_signup()
    if user:
        Database.update_user_status(db, user.user_name)
        # Start chatting
    while True:
        print("Options:")
        print("1. Display Active Chatters")
        print("2. Connect With Chatter")
        print("3. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            print()
            display_active_users()
        elif choice == '2':
            # Implement connection with another chatter
            print()
            chatter = input("Enter Chatter's Name: ")
            chatter_info = Database.get_user(db, chatter)
            if chatter_info:
                print(f"Chat with {chatter_info.user_name} will begin shortly")
                peer = Peer(user.user_name, user.password, user.port, db, user.user_id, chatter_info.user_id)
                peer.set_other_peer_port(chatter_info.port)
                threading.Thread(target=peer.start_server).start()

                peer.set_other_peer_port(chatter_info.port)

                # Run the GUI
                peer.run()
            else:
                print("Invalid Chatter's name")
        elif choice == '3':
            logout(user)
        else:
            print("Invalid choice. Please try again.")


'''
def main():
    args = sys.argv

    peer = Peer(args[1], args[2], int(args[3]), database_param, int(args[5]), int(args[6]))
    # Start the server
    threading.Thread(target=peer.start_server).start()

    peer.set_other_peer_port(int(args[4]))

    # Run the GUI
    peer.run()
'''

if __name__ == "__main__":
    main()
