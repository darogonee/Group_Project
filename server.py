# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time, os


hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        match self.path:
            case  "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("index.html", "rb") as file:
                    self.wfile.write(file.read().replace(b"hi", b"by"))
            case "/main.css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("main.css", "rb") as file:
                    self.wfile.write(file.read())
            case "/stop":
                webServer.server_close()
                webServer.shutdown()
                os.abort()
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever(1)
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
