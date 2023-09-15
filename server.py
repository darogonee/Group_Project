from http.server import BaseHTTPRequestHandler, HTTPServer
import Api, os, random
from datetime import datetime
import time, json

hostName = "localhost"
serverPort = 8080

class FittnessServer(BaseHTTPRequestHandler):
    def redirect(self, link):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open("web_templates/redirect.html", "r") as file:
            self.wfile.write(file.read().replace("url", link).encode())
    
    def query(self):
        query_string = self.path.split("?")[1].split("&")
        values = {}
        for query in query_string:
            name = query.split("=")[0]
            value = query.split("=")[1]
            values[name] = value
        return values

    def cookie(self):
        if self.headers.get("Cookie") is None:
            return {}
        cookie = self.headers.get("Cookie").split(";")
        values = {}
        for query in cookie:
            name = query.split("=")[0].strip()
            value = query.split("=")[1].strip()
            values[name] = value
        return values

    def do_GET(self):
        match self.path.split("?")[0]:
            case  "/activities":
                cookie = self.cookie()
                if "user" not in cookie:
                    self.redirect("/signin")
                    return
                if not Api.load(cookie["user"]):
                    self.redirect("https://www.strava.com/oauth/authorize?client_id=112868&redirect_uri=http%3A%2F%2Flocalhost:8080/oauth&response_type=code&scope=activity%3Aread_all")
                    return
                self.send_response(200)
                self.send_header("Content-type", "text/html")

                self.end_headers()
                with open("web_templates/activities.html", "r") as activities_file:
                    with open("web_templates/activity-template.html", "r") as activity_file:
                        activity_template = activity_file.read()
                        # later check
                        Api.save(*Api.refresh_tokens(Api.client_id, Api.client_secret, Api.refresh_token), f"users/{cookie['user']}.json")
                        activity_data = Api.get_user_activites()
                        tbody = ""
                         
                        # change the number to how ever many activities you want to load
                        table_activity_data = []
                        # change the 5 to how ever many activities you want to load
                        for i in range(min(12, len(activity_data))):      
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
                values = self.query()
                code = values["code"]
                cookie = self.cookie()   
                if "user" not in cookie:
                    self.redirect("/signin")
                    return             
                Api.save(*Api.get_access(Api.client_id, Api.client_secret, code), f"users/{cookie['user']}.json")
                self.redirect("/")

            case "/main.css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("main.css", "rb") as file:
                    self.wfile.write(file.read())
            
            case "/main.js":
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.end_headers()
                with open("main.js", "rb") as file:
                    self.wfile.write(file.read())

            case "/dosomething":
                activity_data_to_print =  activity_data[:5]
                sorted_workouts = sorted(activity_data_to_print, key=lambda x: x["name"])
                for workout in sorted_workouts:
                    print(workout["name"])
            
            case "/signin":

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/signin.html", "r") as file:
                    login_page = file.read()                        
                    self.wfile.write(login_page.encode())

            case "/action_signin":
                values = self.query()
                username = values["username"]
                password = values["password"]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                with open("passwords.json", "r") as file:
                    data = json.load(file)  
                if username in data:
                    if password == data[username]:
                        self.send_header("Set-Cookie", f"user={username}")
                        self.end_headers()
                        with open("web_templates/redirect.html", "r") as file:
                            self.wfile.write(file.read().replace("url", "/").encode())
                        return
                self.redirect("/signin")
            
            case "/action_signup":
                values = self.query()
                username = values["username"]
                password = values["password"]

                if len(username) < 3 or len(username) > 13 or not username.isalnum():
                    self.redirect("/signup")
                    # check for "_" later
                    return
   
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                with open("passwords.json", "r") as file:
                    data = json.load(file)  

                    if username in data:
                        self.redirect("/signup")
                        return

                    data[username] = password
                    with open("passwords.json", "w") as file:
                        json.dump(data, file, indent = 4)

                self.send_header("Set-Cookie", f"user={username}")
                self.end_headers()
                with open("web_templates/redirect.html", "r") as file:
                    self.wfile.write(file.read().replace("url", "/").encode())

            case "/signup":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/signup.html", "r") as file:
                    signup_page = file.read()                        
                    self.wfile.write(signup_page.encode())

            # case "/signup":
            #     values = {}
            #     query_string = self.path.split("?")[1].split("&")
                
            #     for query in query_string:
            #         name = query.split("=")[0]
            #         print(name)
            #         value = query.split("=")[1]
            #         values[name] = value
                
            #     username = values["username"]
            #     password = values["password"]
            #     password_reentry = values["password-reentry"]

            #     print(f"User: {username}")
            #     print(f"Pw: {password}")
            #     print(f"Pw re: {password_reentry}")
                          
            #     with open("web_templates/redirect.html", "r") as file:
            #         self.wfile.write(file.read().replace("url", "/").encode())



            case "/signupqs.html":
                # for signup questions
                # ensure that all fields are inputted     
                query_string = self.path.split("?")[1].split("&")

            case "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/home.html", "r") as file:
                    home_page = file.read()                        
                    self.wfile.write(home_page.encode())

            case "/activities.html":
                pass
            # put activities page here when homepage is done


            case "/myprogram.html":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/myprogram.html", "r") as file:
                    myprogram_page = file.read()                        
                    self.wfile.write(myprogram_page.encode())

            case "/food&water.html":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/food&water.html", "r") as file:
                    foodwater_page = file.read()
                    self.wfile.write(foodwater_page.encode())


            case "/logexercise.html":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/logexercise.html", "r") as file:
                    logexercise_page = file.read()
                    self.wfile.write(logexercise_page.encode())

            case "/logfood&water.html":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/logfood&water.html", "r") as file:
                    logfoodwater_page = file.read()
                    self.wfile.write(logfoodwater_page.encode())

            case "/myprofile.html":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/myprofile.html", "r") as file:
                    myprofile_page = file.read()
                    self.wfile.write(myprofile_page.encode())

            case "/signupquestions.html":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web_templates/signupquestions.html", "r") as file:
                    signupquestions_page = file.read()
                    self.wfile.write(signupquestions_page.encode())
            

            case _:
                self.send_response(200)
                file_type = self.path.split(".")[-1]
                self.send_header("Content-type", f"image/{file_type}")
                self.end_headers()
                with open("."+self.path, "rb") as file:
                    file_data = file.read()                        
                    self.wfile.write(file_data)


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), FittnessServer)
    print(f"Server started http://{hostName}:{serverPort}")
    try:
        webServer.serve_forever(1)
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")