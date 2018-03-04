import socket

client = socket.socket()
client.connect(("localhost", 9999))

while True:
    user_input = input(">>:").strip()
    if user_input:
        client.send(user_input.encode())
client.close()
