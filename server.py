# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import Api


# print("Activity Name -", Activity_data["name"])
# print("Activity Distance -", round(Activity_data["distance"]/1000, 2),"km")
# print("Activity Time-", round(Activity_data["moving_time"]/60, 1),"m","/",round(Activity_data["elapsed_time"]/60, 1),"m")

hostName = "localhost"
serverPort = 8080
u = b"hi"
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        i = 0
        match self.path:
            case  "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/activities.html", "r") as activities_file:
                    with open("web_templates/activity.html", "r") as activity_file:
                        activity = activity_file.read()
                        
                        Activity_data = Api.get_user_activites()
                        
                        while i < 5:                           
                            activity = activity.replace("template_name", str(Activity_data[i]["name"]))
                            activity = activity.replace("template_type", str(Activity_data[i]["type"]))
                            activity = activity.replace("template_distancekm", str(round(Activity_data[i]["distance"]/1000, 2)))
                            activity = activity.replace("template_time", str(round(Activity_data[i]["moving_time"]/60, 1)))
                            activity = activity.replace("template_elevgain", str(Activity_data[i]["total_elevation_gain"]))



                            activity_final = activities_file.read().replace("template_activities", activity*5)
                            
                            self.wfile.write(activity_final.encode())
                            i += 1



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
