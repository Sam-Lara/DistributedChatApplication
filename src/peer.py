import socket
import threading
import psycopg2

class Peer:
    '''
    Represents a Peer in a the distributed chat application

    Attributes:
        conn (obj): the connection object for the PostgresSQL database
        port (int): the port number the Peer is binded to
    '''

    def __init__(self, conn):
        '''
        Initializes a new Peer object

        Params: 
            conn (obj): the connection object for the PostgresSQL database
        '''

        self.conn = conn
        self.port = self.get_free_port()

    def register_with_database(self, server_address):
        '''
        Registers the Peer with the database
        '''
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)

        ip_address = socket.gethostbyname(socket.gethostname())
        port = self.get_free_port()
        registration_data = f'{ip_address}:{port}'
        client_socket.send(registration_data.encode())

        client_socket.close()

    def start_server(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', port))
        server_socket.listen(5)
        print('Server started. Listening for connections...')

        while True:
            client_socket, addr = server_socket.accept()
            print(f'Connected to {addr[0]}:{addr[1]}')

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                sender, recipient, message = data.split(':')
                self.insert_message(sender, recipient, message)

                print(f'Received message from {sender}: {message}')

            except Exception as e:
                print(f'Error: {e}')
                break

        client_socket.close()

    def insert_message(self, sender, recipient, message):
        # Assuming you have a table named chat_messages in your PostgreSQL database
        with self.conn.cursor() as cur:
            # queries subject to change 
            cur.execute('''INSERT INTO chat_messages (sender, recipient, message)
                           VALUES (%s, %s, %s)''', (sender, recipient, message))
            self.conn.commit()

    def get_messages(self):
        with self.conn.cursor() as cur:
            # queries subject to change 
            cur.execute('''SELECT * FROM chat_messages''')
            return cur.fetchall()

    @staticmethod
    def get_free_port():
        '''
        Get a free port number to facilitate communication
        '''
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.bind(('localhost', 0))
        port = temp_socket.getsockname()[1]
        temp_socket.close()
        return port
