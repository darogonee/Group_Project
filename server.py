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
        match self.path:
            case  "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/activities.html", "r") as activities_file:
                    with open("web_templates/activity.html", "r") as activity_file:
                        activity_template = activity_file.read()

                        tbody = ""
                        i = 0
                        Activity_data = Api.get_user_activites() 

                        # change the number to how ever many activities you want to load
                        while i < 12:      
                            activity = activity_template                 
                            activity = activity.replace("template_name", str(Activity_data[i]["name"]))
                            activity = activity.replace("template_type", str(Activity_data[i]["type"]))
                            activity = activity.replace("template_distancekm", str(round(Activity_data[i]["distance"]/1000, 2))+" km")
                            activity = activity.replace("template_time", str(round(Activity_data[i]["moving_time"]/60, 1))+" m")
                            activity = activity.replace("template_elevgain", str(Activity_data[i]["total_elevation_gain"])+" m")

                            tbody += activity
                            i += 1

                        activity_final = activities_file.read().replace("template_activities", tbody)                         
                        self.wfile.write(activity_final.encode())

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

