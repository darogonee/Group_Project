# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time, os


hostName = "localhost"
serverPort = 8080
u = b"hi"
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        match self.path:
            case  "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/activities.html", "r") as activities_file:
                    with open("web_templates/activity.html", "r") as activity_file:
                        activity = activity_file.read()
                        activity = activity.replace("template_name", )

                        activity_final = (activities_file.read().replace("template_activities", activity))
                        self.wfile.write(bytes(activity_final))


                # with open("activite.json", "rb") as file:
                #     self.wfile.write(file.read())

            case "/main.css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("main.css", "rb") as file:
                    self.wfile.write(file.read())

            case "/test":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("index.html", "rb") as file:
                    self.wfile.write(file.read().replace(b"Recent_Activites", b"egegeg Activite's"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever(1)
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
