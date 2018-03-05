import socketserver


class MyTcpHandler(socketserver.BaseRequestHandler):
    # 该方法在handle()之前调用。默认情况下，它不执行任何操作。如果希望服务器实现更多连接设置，可以在这里实现
    def setup(self):
        pass

    def handle(self):
        try:
            print("new connection:", self.client_address[0])
            while True:
                data = self.request.recv(1024)
                if data:
                    print("recv:", data.decode())
        except ConnectionResetError:
            print(self.client_address[0], "已断开")

    # 调用本方法可以在执行完handle()之后执行清除操作。如果setup()和 handle()都不生成异常，则无需调用该方法
    def finish(self):
        pass


if __name__ == '__main__':
    HOST, PORT = "localhost", 9999
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTcpHandler) as server:
        server.serve_forever()
        # server.shutdown()  # 停止server_forever()循环