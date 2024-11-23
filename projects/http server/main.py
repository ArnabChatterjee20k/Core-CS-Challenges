from SimpleTCPServer import SimpleTCPServer
from SimpleHTTPServer import SimpleHTTPServer
with SimpleTCPServer(('0.0.0.0', 8000),SimpleHTTPServer) as http:
    http.serve_forever()