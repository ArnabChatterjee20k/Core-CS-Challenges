import io,logging,os
from http import HTTPStatus
logging.basicConfig(level=logging.INFO)
class SimpleHTTPServer:
    """
        Supports GET and HEAD
    """
    def __init__(self,req_stream:io.BufferedIOBase,res_stream:io.BufferedIOBase) -> None:
        self.req_stream = req_stream
        self.res_stream = res_stream
        self.command = ""
        self.path = ""
        self.headers = {
            "Content-Type":"text/html",
            "Content-Length":"0",
            "Connection":"close"
        }
        self.data = ""
        self.handle()

    def handle(self):
        self._parse_request()
        if not self._validate_path():
            logging.error("not found")
            return self._return_404()

        if self.command == "POST":
            return self._return_403()
        
        if self.command not in ("GET","HEAD"):
            return self._return_405()
        
        # for calling the handle_GET,handle_HEAD
        command = getattr(self,f"handle_{self.command}")
        command()

    def handle_GET(self):
        """Copying file data and writing to the output buffer"""
        self.handle_HEAD()
        with open(self.path,"rb") as f:
            body = f.read()
        self.res_stream.write(body)
        self.res_stream.flush()
    
    def handle_HEAD(self):
        self._write_response_line(200)
        # needed to send to the content size even without the body
        # to the frontend so that it can be determined before hand
        extra_headers_for_head = {
            "Content-Length":os.path.getsize(self.path)
        }
        print(extra_headers_for_head)
        self._write_headers(**extra_headers_for_head)
        self.res_stream.flush()

    def _validate_path(self):
        # path or directory
        # if directory look for the index.html file in the dir
        # ex-> /index.html
        path = self.path.lstrip("/")
        self.path = os.path.join(os.getcwd(),path)
        if os.path.isdir(self.path):
            self.path = os.path.join(self.path,"index.html")
        
        elif os.path.isfile(self.path):
            pass
            
        if not os.path.exists(self.path):
            return False

        return True
            
    def _parse_request(self):
        """
        <COMMAND> <PATH>
        <optional headers>
        \r\n (CRLF)
        <optional data>

        for get data is not present
        """
        logging.info("parsing request line")
        # for command and path
        requestline = self.req_stream.readline().decode()
        requestline = requestline.rstrip("\r\n")
        logging.info("requested line is" + requestline)
        self.command = requestline.split(" ")[0]
        self.path = requestline.split(" ")[1]
        
        headers = {}
        line = self.req_stream.readline().decode()
        while line not in ("\r\n","\n","\r",""):
            header = line.rstrip("\r\n").split(": ")
            key,value = header
            headers[key] = value
            line = self.req_stream.readline().decode()

        logging.info(headers)
    
    def _write_response_line(self,status_code:int)->None:
        resp_line = f"HTTP/1.1 {status_code} {HTTPStatus(status_code).phrase}\r\n"
        logging.info(resp_line.encode())
        # writing in form of bytes
        self.res_stream.write(resp_line.encode())

    def _write_headers(self,*args,**kwargs):
        headers_copy = self.headers.copy()
        headers_copy.update(**kwargs)
        headers_lines = "\r\n".join(
            f"{k}: {v}" for k,v in headers_copy.items()
        )
        logging.info(headers_lines.encode())
        self.res_stream.write(headers_lines.encode())
        # mark the end of the headers
        self.res_stream.write(b'\r\n\r\n')
        self.res_stream.flush()
    
    def _return_404(self):
        '''NOT FOUND'''
        self._write_response_line(404)
        self._write_headers()

    def _return_403(self):
        """FORBIDDEN"""
        self._write_response_line(403)
        self._write_headers()
    
    def _return_405(self):
        """METHOD NOT ALLOWED"""
        self._write_response_line(405)
        self._write_headers()
    
if __name__ == "__main__":
    # mock_request = (
    #     b"GET /index.html HTTP/1.1\r\n"
    #     b"Host: localhost\r\n"
    #     b"User-Agent: TestClient\r\n"
    #     b"Accept: */*\r\n"
    #     b"\r\n"
    # )

    mock_request = (
        b"GET /index.html HTTP/1.1\r\n"
        b"Host: 127.0.0.1:8000\r\n"
        b"Connection: keep-alive\r\n"
        b"Cache-Control: max-age=0\r\n"
        b'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"\r\n'
        b"sec-ch-ua-mobile: ?0\r\n"
        b'sec-ch-ua-platform: "Linux"\r\n'
        b"Upgrade-Insecure-Requests: 1\r\n"
        b"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36\r\n"
        b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n"
        b"Sec-Fetch-Site: none\r\n"
        b"Sec-Fetch-Mode: navigate\r\n"
        b"Sec-Fetch-User: ?1\r\n"
        b"Sec-Fetch-Dest: document\r\n"
        b"Accept-Encoding: gzip, deflate, br, zstd\r\n"
        b"Accept-Language: en-US,en;q=0.9\r\n"
        b"\r\n"
    )

    req_stream = io.BytesIO(mock_request)
    mock_response = io.BytesIO()

    server = SimpleHTTPServer(req_stream,mock_response)
    print(server.res_stream)