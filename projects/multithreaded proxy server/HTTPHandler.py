"""
    will act as the http parser and handler
    for corresponding path a specific value will be assigned with some db actions
"""

from http import HTTPStatus
import io,secrets
from CSVDatabase import CSVDatabase
class HTTPHandler:
    def __init__(self,req_stream:io.BufferedIOBase,res_stream:io.BufferedIOBase) -> None:
        self.req_stream = req_stream
        self.res_stream = res_stream
        self.command = ""
        self.path = ""
        self.default_headers_list = {
            "Content-Type":"text/html",
            "Content-Length":"0",
            "Connection":"close"
        }
        self.data = ""
        self.db = CSVDatabase("new.csv")
        self._handler()

    def _handler(self):
        self._parse_request()
        if self.command == "POST":
            return self._forbidden()
        elif self.command == "HEAD":
            return self._HEAD()
        elif self.command == "GET":
            return self._GET()
        else:
            return self._method_not_allowed()
        
    def _GET(self):
        token = self.write_data_if_not_exists()
        data = f"<html><body><h1>{token}</h1></body></html>"
        headers = {"Content-Length":len(data)}
        # needed to be done in the order due to the semantic of http
        self._write_response(200)
        self._write_headers(**headers)
        self.res_stream.write(data.encode())
        self.res_stream.flush()

    def _HEAD(self):
        headers = {"Content-Length": len("<html><body><h1>Hello, World!</h1></body></html>")}
        self._write_response(200)
        self._write_headers(**headers)
        self.res_stream.flush()
    
    def write_data_if_not_exists(self):
        data = self.db.get(self.path)
        if data:
            return data
        token = secrets.token_hex()
        self.db.write(self.path,token)
        return token

    def _parse_request(self):
        """
            <COMMAND> <PATH>
            <optional headers>
            \r\n (CRLF)
            <optional data>

            for get request, data is not present
            headers not required here
        """
        requestedline = self.req_stream.readline().decode()
        requestedline = requestedline.rstrip("\r\n")
        self.command = requestedline.split(" ")[0]
        self.path = requestedline.split(" ")[1]

    def _write_response(self,status_code:int):
        resp_line = f"HTTP/1.1 {status_code} {HTTPStatus(status_code).phrase}\r\n"
        self.res_stream.write(resp_line.encode())
    
    def _write_headers(self,*arg,**kwargs):
        headers_copy = self.default_headers_list.copy()
        headers_copy.update(**kwargs)
        headers_lines = "\r\n".join(
            f"{k}: {v}" for k,v in headers_copy.items()
        )
        self.res_stream.write(headers_lines.encode())
        # mark the end of the headers
        self.res_stream.write(b'\r\n\r\n')
        self.res_stream.flush()


    def _method_not_allowed(self):
        self._write_response(405)
        self._write_headers()
    
    def _forbidden(self):
        self._write_response(403)
        self._write_headers()