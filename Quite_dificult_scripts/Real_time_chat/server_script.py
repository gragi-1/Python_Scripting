# server.py
import socket
import threading

class Server:
    def __init__(self, host = '127.0.0.1', port = 55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.nicknames = []

    def broadcast(self, message, sender):
        if ":" in message:
            recipient, message = message.split(":", 1)
            if recipient in self.nicknames:
                recipient_index = self.nicknames.index(recipient)
                self.clients[recipient_index].send(f'{sender}: {message}'.encode('ascii'))
        else:
            for client in self.clients:
                client.send(message.encode('ascii'))

def handle(self, client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            self.broadcast(message, self.nicknames[self.clients.index(client)])
        except socket.error:
            print("Failed to receive message from client")
            client.close()
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            self.broadcast(f'{nickname} left the chat!', nickname)
            break

    def receive(self):
        while True:
            try:
                client, address = self.server.accept()
                print(f"Connected with {str(address)}")

                client.send('NICK'.encode('ascii'))
                nickname = client.recv(1024).decode('ascii')
                self.nicknames.append(nickname)
                self.clients.append(client)

                print(f"Nickname of the client is {nickname}!")
                self.broadcast(f'{nickname} joined the chat!'.encode('ascii'))
                client.send('Connected to the server!'.encode('ascii'))

                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            except socket.error:
                print("Failed to accept new connection")

if __name__ == "__main__":
    server = Server()
    server.receive()