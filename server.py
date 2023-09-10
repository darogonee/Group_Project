from http.server import BaseHTTPRequestHandler, HTTPServer
import Api, os, random
from datetime import datetime
import time
#oliver bison is itch
hostName = "localhost"
serverPort = 8080

class FittnessServer(BaseHTTPRequestHandler):
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
                        activity_data = Api.get_user_activites()
                        tbody = ""
                         
                        # change the number to how ever many activities you want to load
                        table_activity_data = []
                        # change the 5 to how ever many activities you want to load
                        for i in range(12):      
                            activity = activity_template 
                            activity = activity.replace("template_type", str(activity_data[i]["type"])) 

                            input_datetime = datetime.strptime(activity_data[i]["start_date_local"], "%Y-%m-%dT%H:%M:%SZ")
                            formatted_date = input_datetime.strftime("%a, %d/%m/%Y")         
                            activity = activity.replace("template_date", str(formatted_date))

                            activity = activity.replace("template_name", str(activity_data[i]["name"]))
            
                            formatted_time = time.strftime('%H:%M:%S', time.gmtime(activity_data[i]["moving_time"]))
                                                           
                            activity = activity.replace("template_time", str(formatted_time))
                            distancekm = round(activity_data[i]["distance"]/1000, 2)
                            activity = activity.replace("template_distancekm", str(distancekm)+" km")
                            activity = activity.replace("template_elevgain", str(activity_data[i]["total_elevation_gain"])+" m")

                            tbody += activity

                            table_activity_data.append({"type":activity_data[i]["type"], "date":activity_data[i]["start_date_local"], "name":activity_data[i]["name"], "time":str(activity_data[i]["moving_time"]), "distance":str(distancekm), "elevgain":str(activity_data[i]["total_elevation_gain"])})


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
                Api.load()
                self.redirect("/")

            case "/main.css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("main.css", "rb") as file:
                    self.wfile.write(file.read())

            case "/dosomething":
                # self.send_response(200)
                # self.send_header("Content-type", "text/text")
                # self.end_headers()
                # self.wfile.write(random.choice(["hello", "hi", "hey"]).encode())
                activity_data_to_print =  activity_data[:5]
                sorted_workouts = sorted(activity_data_to_print, key=lambda x: x["name"])
                for workout in sorted_workouts:
                    print(workout["name"])
                print("Button clicked! Doing something...")
            
            case "/Home":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open(b"web_templates/home.html", "r") as file:
                    home_page = file.read()                        
                    self.wfile.write(home_page.encode())

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), FittnessServer)
    print(f"Server started http://{hostName}:{serverPort}")
    try:
        webServer.serve_forever(1)
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")

    #test
    #test