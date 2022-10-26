from Server import Lab4HTTPRequestHandler
from socketserver import TCPServer


if __name__ == '__main__':
    with TCPServer(('', 8081), Lab4HTTPRequestHandler) as tcp_server:
        print('Serving on http://localhost:8081')
        tcp_server.serve_forever()
