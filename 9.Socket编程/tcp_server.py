import socketserver


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024)
        # print(self.client_address[0])
        print(self.data)
        self.request.send(self.data.upper())


if __name__ == '__main__':
    HOST, PORT = "localhost", 9999
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTcpHandler) as server:
        server.serve_forever()