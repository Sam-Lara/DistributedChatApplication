import socket

def initialize_client_unicast():
    try:
        # initalize a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect client socket to the server socket
        server_socket_address = ("localhost", 10000)
        client_socket.connect(server_socket_address)

        # infinite while loop to continue messaging server
        while 1:
            client_message = "ip:port:Yay Area!!!"
            print(client_message)
            # send and receieve messages
            client_socket.sendall(client_message.encode())
            data = client_socket.recv(512)
            print(f"Received unicast message: {data.decode()}", flush=True)
    except KeyboardInterrupt as error:
        print(f"\nDiscconnected from server {error}")
        client_socket.close()

initialize_client_unicast()
