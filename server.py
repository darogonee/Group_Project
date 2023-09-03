# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import Api, os


# print("Activity Name -", Activity_data["name"])
# print("Activity Distance -", round(Activity_data["distance"]/1000, 2),"km")
# print("Activity Time-", round(Activity_data["moving_time"]/60, 1),"m","/",round(Activity_data["elapsed_time"]/60, 1),"m")

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def redirect(self, link):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open("web_templates/redirect.html", "r") as file:
            self.wfile.write(file.read().replace("url", link).encode())

    def do_GET(self):
        match self.path.split("?")[0]:
            case  "/":
                if not os.path.exists("users/me.json"):
                    self.redirect("https://www.strava.com/oauth/authorize?client_id=112868&redirect_uri=http%3A%2F%2Flocalhost:8080/oauth&response_type=code&scope=activity%3Aread_all")
                    return
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/activities.html", "r") as activities_file:
                    with open("web_templates/activity.html", "r") as activity_file:
                        activity_template = activity_file.read()

                        # later check
                        Api.save(*Api.refresh_tokens(Api.client_id, Api.client_secret, Api.refresh_token), "users/me.json")
                        Activity_data = Api.get_user_activites()
                        tbody = ""
                         
                        # change the number to how ever many activities you want to load
                        for i in range(12):  
                            # if str(Activity_data[i]["name"]) != "Run":
                              
                            activity = activity_template                 
                            activity = activity.replace("template_name", str(Activity_data[i]["name"]))
                            activity = activity.replace("template_type", str(Activity_data[i]["type"]))
                            activity = activity.replace("template_distancekm", str(round(Activity_data[i]["distance"]/1000, 2))+" km")
                            activity = activity.replace("template_time", str(round(Activity_data[i]["moving_time"]/60, 1))+" m")
                            activity = activity.replace("template_elevgain", str(Activity_data[i]["total_elevation_gain"])+" m")

                            tbody += activity

                        activity_final = activities_file.read().replace("template_activities", tbody)                         
                        self.wfile.write(activity_final.encode())
            case "/oauth":
                quire_string = self.path.split("?")[1].split("&")
                values = {}
                for quire in quire_string:
                    name = quire.split("=")[0]
                    value = quire.split("=")[1]
                    values[name] = value
                code = values["code"]
                                           
                Api.save(*Api.get_access(Api.client_id, Api.client_secret, code), "users/me.json")
                self.redirect("/")

            case "/main.css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("main.css", "rb") as file:
                    self.wfile.write(file.read())

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever(1)
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

