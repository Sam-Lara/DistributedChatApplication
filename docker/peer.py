import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
from sqlalchemy import create_engine, text
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy import insert
from database import Database, User, Message


class Peer:
    def __init__(self, name, password, port, db, id, other_id, ip_addr='localhost'):
        self.id = id
        self.other_id = other_id
        self.ip_addr = ip_addr
        self.port = port
        self.name = name
        self.password = password
        self.db = db
        self.root = tk.Tk()
        self.root.title("Peer-to-Peer Chat")

        self.chat_history = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.chat_history.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack(padx=10, pady=(0, 10))

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        server_socket.listen(1)
        print(f'Peer listening on port {self.port}')

        while True:
            client_socket, addr = server_socket.accept()
            print(f'Connected to peer at {addr[0]}:{addr[1]}')

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            received_message = data.decode()
            sender_name, message = received_message.split(":", 1)
            self.chat_history.insert(tk.END, f'{sender_name}: {message}\n')

    def send_message(self):
        message = f'{self.name}: {self.message_entry.get()}'
        if message:
            self.chat_history.insert(tk.END, f'{self.name}: {self.message_entry.get()}\n')
            self.message_entry.delete(0, tk.END)
            peer_address = ('localhost', self.other_peer_port)
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect(peer_address)
            peer_socket.send(message.encode())
            peer_socket.close()
            Database.add_message(self.db, self.id, self.other_id, message)

    def set_other_peer_port(self, other_peer_port):
        self.other_peer_port = other_peer_port

    def run(self):
        self.root.mainloop()
