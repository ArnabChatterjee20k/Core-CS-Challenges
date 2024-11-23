import socket, threading,logging
from SimpleHTTPServer import SimpleHTTPServer
class SimpleTCPServer:
    def __init__(self,
                 socket_address:tuple[str,int],
                 request_handler:"SimpleHTTPServer"
                 ) -> None:
        self.request_handler = request_handler
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socket.bind(socket_address)
        self.socket.listen()
    
    def serve_forever(self)->None:
        while True:
            conn,addr = self.socket.accept()
            with conn:
                logging.info(f"Accepted connection from {addr}")
                req_stream = conn.makefile("rb")
                res_stream = conn.makefile("wb")
                self.request_handler(
                    req_stream = req_stream,
                    res_stream = res_stream
                )
                logging.info(f"Closed connection from {addr}")

    def __enter__(self) -> "SimpleTCPServer":
        return self
    
    def __exit__(self) -> "SimpleTCPServer":
        self.socket.close()
