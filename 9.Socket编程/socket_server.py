import socket

server = socket.socket()
server.bind(("localhost", 9999))
server.listen()

conn, addr = server.accept()
data = conn.recv(1024)
print(data.decode())
