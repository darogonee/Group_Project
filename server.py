from http.server import BaseHTTPRequestHandler, HTTPServer
import python.Api, os, random
from python.hash_function import password_hash 
from datetime import datetime
from Nutrition_Calculator import nutrition_calculator
import time, json, datetime, uuid 


# NOTE restart server aprox 30 days NOTE

hostName = "localhost"
serverPort = 8080

uuid2user = {}

class FittnessServer(BaseHTTPRequestHandler):
    def redirect(self, link):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open("web/html/redirect.html", "r") as file:
            self.wfile.write(file.read().replace("url", link).encode())
    
    def query(self):
        if "?" not in self.path:
            return {}
        query_string = self.path.split("?")[1].split("&")
        values = {}
        for query in query_string:
            name = query.split("=")[0]
            value = query.split("=")[1]
            values[name] = value
        return values

    def get_cookie(self):
        if self.headers.get("Cookie") is None:
            return {}
        cookie = self.headers.get("Cookie").split(";")
        values = {}
        for query in cookie:
            name = query.split("=")[0].strip()
            value = query.split("=")[1].strip()
            values[name] = value
        return values
        
    def set_cookie(self, user):
        user_uuid = uuid.uuid4().hex
        uuid2user[user_uuid] = user
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=30) # expires in 30 days
        self.send_header("Set-Cookie", f"user={user_uuid}; Expires={expires.strftime('%a, %d %b %Y %H:%M:%S GMT')}")
        self.end_headers()
        datetime.datetime.isoformat
    def get_username(self):
        cookie = self.get_cookie()
        if cookie["user"] in uuid2user:
            return uuid2user[cookie["user"]]
        self.redirect("/signin")

    def get_user_data(self):
        user = self.get_username()
        user_data_file = f"/user_data/{user}.json"
        with open(user_data_file, "r") as file:
            data = json.load(file)

        print(data)

    def create_program(self, data):
        program = {"monday":None, "tuesday":None, "wednesday":None, "thursday":None, "friday":None, "saturday":None}
        weight_programs = {1:"full-body", 2:"upper-lower", 3:"ppl", 4:"upper-lower-twice", 5:"ulppl", 6:"ppl-twice"}
        fitness_goals = []
        equipment = []
        training_days = []
        
        for key,value in data["fitness-goals"].items():
            if value:
                fitness_goals.append(key)
        
        for key,value in data["equipment"].items():
            if value:
                equipment.append(key)

        for key,value in data["training_days"].items():
            if value:
                training_days.append(key)

        # rest day if all days ticked
        if training_days.count() > 6:
            rest_day = random.choice(training_days)
            training_days.remove(rest_day)

        #available days True and unavailable days False
        for day in program.keys():
            program[day] = day in training_days

        if "endurance" in fitness_goals or "strength" in fitness_goals or "hypertrophy" in fitness_goals:
           ...
            

        


        

        
        
        


    def do_GET(self):
        match self.path.split("?")[0]:
            case  "/activities":
                user = self.get_username()
                self.send_response(200)
                self.send_header("Content-type", "text/html")

                self.end_headers()
                with open("web/html/activities.html", "r") as activities_file:
                    with open("web/html/activity-template.html", "r") as activity_file:
                        activity_template = activity_file.read()
                        # later check
                        python.Api.refresh(user)
                        activity_data = python.Api.get_user_activites(user)
                        tbody = ""
                        # change the number to how ever many activities you want to load
                        table_activity_data = []
                        for i in range(min(200, len(activity_data))):
                            
                            activity_type = self.query().get("type", "")
                            if activity_data[i]['type'] == activity_type or activity_type == "":
                                print("Run found: " + activity_data[i]['name'])  

                                activity = activity_template 
                                activity = activity.replace("template_type", str(activity_data[i]["type"])) 

                                input_datetime = datetime.datetime.strptime(activity_data[i]["start_date_local"], "%Y-%m-%dT%H:%M:%SZ")
                                formatted_date = input_datetime.strftime("%a, %d/%m/%Y")         
                                activity = activity.replace("template_date", str(formatted_date))

                                activity = activity.replace("template_name", str(activity_data[i]["name"]))

                
                                formatted_time = time.strftime('%H:%M:%S', time.gmtime(activity_data[i]["moving_time"]))
                                                            
                                activity = activity.replace("template_time", str(formatted_time))
                                distancekm = round(activity_data[i]["distance"]/1000, 2)
                                activity = activity.replace("template_distancekm", str(distancekm)+" km")
                                activity = activity.replace("template_elevgain", str(activity_data[i]["total_elevation_gain"])+" m")

                                try:
                                    activity = activity.replace("template_calories", str(round(activity_data[i]["kilojoules"]/4.184, 2)))
                                except KeyError:
                                    activity = activity.replace("template_calories", "0")

                                tbody += activity

                                table_activity_data.append({"type":activity_data[i]["type"], "date":activity_data[i]["start_date_local"], "name":activity_data[i]["name"], "time":str(activity_data[i]["moving_time"]), "distance":str(distancekm), "elevgain":str(activity_data[i]["total_elevation_gain"])})


                        activity_final = activities_file.read().replace("template_activities", tbody)                         
                        self.wfile.write(activity_final.encode())

                        
            case "/logout":
                uuid2user.pop(self.get_cookie()['user'])

            case "/refresh":
                user = self.get_username()
                # print("Ballz (pay ID 0499076683, pay me)")
                python.Api.get_user_activites.clear(user)
                self.redirect("/activities")
              
            case "/oauth":
                values = self.query()
                code = values["code"]
                cookie = self.get_cookie()  
                if "user" not in cookie:
                    self.redirect("/signin")
                    return  
                user = self.get_username()            
                python.Api.save(*python.Api.get_access(python.Api.client_id, python.Api.client_secret, code), f"users/{user}.json")
                self.redirect("/")

            case "/main.css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("web/css/main.css", "rb") as file:
                    self.wfile.write(file.read())
            
            case "/main.js":
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.end_headers()
                with open("web/js/main.js", "rb") as file:
                    self.wfile.write(file.read())
            
            case "/signin":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/signin.html", "r") as file:
                    login_page = file.read()                        
                    self.wfile.write(login_page.encode())

            case "/action_signin":
                values = self.query()
                username = values["username"].lower()
                password = password_hash(values["password"])
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                with open("data/passwords.json", "r") as file:
                    data = json.load(file)  
                if username in data:
                    if password == data[username]:
                        self.set_cookie(username)
                        with open("web/html/redirect.html", "r") as file:
                            self.wfile.write(file.read().replace("url", "/").encode())
                        return
                self.redirect("/signin")
            
            case "/action_signup":
                values = self.query()
                # replace the .replace funtion with something to remove special charicters
                username = values["username"].lower()
                password = password_hash(values["password"])
                passwordrentry = password_hash(values["password-rentry"])
                if len(username) < 3 or len(username) > 13 or password != passwordrentry or not username.isalnum():
                    self.redirect("/signup")
                    return

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                with open("data/passwords.json", "r") as file:
                    data = json.load(file)  

                    if username in data:
                        self.redirect("/signup")
                        return

                    data[username] = password
                    with open("data/passwords.json", "w") as file:
                        json.dump(data, file, indent = 4)

                self.set_cookie(username)
                
                with open("web/html/redirect.html", "r") as file:
                    self.wfile.write(file.read().replace("url", "/signupqs").encode())

            case "/signup":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/signup.html", "r") as file:
                    signup_page = file.read()                        
                    self.wfile.write(signup_page.encode())

            case "/signupqs":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/signupquestions.html", "r") as file:
                    signup_page = file.read()                        
                    self.wfile.write(signup_page.encode())


            case "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/home.html", "r") as file:
                    home_page = file.read()                        
                    self.wfile.write(home_page.encode())

                cookie = self.get_cookie()
                if "user" not in cookie:
                    self.redirect("/signin")
                    return
                user = self.get_username()
                if not python.Api.check(user):
                    self.redirect("https://www.strava.com/oauth/authorize?client_id=112868&redirect_uri=http%3A%2F%2Flocalhost:8080/oauth&response_type=code&scope=activity%3Aread_all,activity%3Awrite")
                    return
                if not os.path.exists(f"user_data/{user}.json"):
                    self.redirect("/signupquestions")
                    return

            case "/myprogram":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/myprogram.html", "r") as file:
                    myprogram_page = file.read()                        
                    self.wfile.write(myprogram_page.encode())

                user = self.get_username()
                print(user)
                user_data_file = f"user_data/{user}.json"
                with open(user_data_file, "r") as file:
                    data = json.load(file)

                print(data)
                self.create_program(data)


            case "/food&water":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/food&water.html", "r") as file:
                    foodwater_page = file.read()
                    self.wfile.write(foodwater_page.encode())


            case "/logexercise":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/logexercise.html", "r") as file:
                    logexercise_page = file.read()
                    self.wfile.write(logexercise_page.encode())
                
                user = self.get_username()
                value = self.query()             
                date = value['workout-date'].split("-")
                times = value['workout-time'].split("%3A")
                workout_time = (int(value['workout-hrs'])*3600) + (int(value['workout-mins'])*60) + int(value['workout-secs']) 
                timestamp = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(times[0]), int(times[1]))

                exercises = {}
                for item in value:
                    if item.startswith("exercise_input"):
                        number = int(item[len("exercise_input"):])
                        current = exercises.get(number, {})
                        current['name'] = value[item]
                        exercises[number] = current
                    elif item.startswith("repstime_input"):
                        number = int(item[len("repstime_input"):])
                        current = exercises.get(number, {})
                        current['reps'] = value[item]
                        exercises[number] = current
                    elif item.startswith("sets_input"):
                        number = int(item[len("sets_input"):])
                        current = exercises.get(number, {})
                        current['sets'] = value[item]
                        exercises[number] = current
                    elif item.startswith("rest_input"):
                        number = int(item[len("rest_input"):])
                        current = exercises.get(number, {})
                        current['rest'] = value[item]
                        exercises[number] = current
                python.Api.upload(user, value['title'], value['sport'], str(timestamp), 
                    workout_time, value['distance'], value['elev-gain'], "hello?", 0, 0, 
                    int(value['percieved-exertion']), exercises)

            case "/logfood&water":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/logfood&water.html", "r") as file:
                    logfoodwater_page = file.read()
                    self.wfile.write(logfoodwater_page.encode())

                nutrition_calculator(input())


                value = self.query()  

                # value[]

            case "/myprofile":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/myprofile.html", "r") as file:
                    myprofile_page = file.read()
                    self.wfile.write(myprofile_page.encode())

            case "/signupquestions":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/signupquestions.html", "r") as file:
                    signupquestions_page = file.read()
                    self.wfile.write(signupquestions_page.encode())

            case "/signupquestions_action":
                user = self.get_username()
                with open(f"user_data/{user}.json", "w") as file:
                    value = self.query()

                    json.dump(
                    {
                        "fitness-goals": {
                            "cardio": "fitness_goals_cardio" in value,
                            "strength": "fitness_goals_strength" in value,
                            "hypertrophy": "fitness_goals_hypertrophy" in value,
                            "endurance": "fitness_goals_endurance" in value,
                        },
                        "fav-"
                        "weight-goal": value['weight-goal'],
                        "weight-units": value['weight-units'],
                        "weight": value['weight'],
                        "height-units": value['height-units'],
                        "height": value['height'],
                        "dob": value['date_of_birth'],
                      "sex": value['sex'],
                        "equipment": {
                            "bench": "equipment_bench" in value,
                            "medicine-ball": "equipment_medicine-ball" in value,
                            "cable-machine": "equipment_cable-machine" in value,  
                            "torso-rotation-machine": "equipment_torso-rotation-machine" in value,  
                            "ab-roller": "equipment_ab-roller" in value,  
                            "dumbbell": "equipment_dumbbell" in value,  
                            "barbell": "equipment_barbell" in value,  
                            "assisted-pullup-machine": "equipment_assisted-pullup-machine" in value,  
                            "lat-pulldown-machine": "equipment_lat-pulldown-machine" in value,  
                            "pullup-bar": "equipment_pullup-bar" in value,   
                            "v-bar": "equipment_v-bar" in value,           
                            "machine-row": "equipment_machine-row" in value,           
                            "ez-bar": "equipment_ez-bar" in value,           
                            "preacher-curl-machine": "equipment_preacher-curl-machine" in value,           
                            "rope": "equipment_rope" in value,           
                            "leg-press-machine": "equipment_leg-press-machine" in value,           
                            "smith-machine": "equipment_smith-machine" in value,           
                            "calf-raise-machine": "equipment_calf-raise-machine" in value,          
                            "chest-press-machine": "equipment_chest-press-machine" in value,          
                            "bench-press-machine": "equipment_bench-press-machine" in value,          
                            "plates": "equipment_plate" in value,          
                            "dip-assist-machine": "equipment_dip-assist-machine" in value,          
                            "dip-machine": "equipment_dip-machine" in value,                           
                        },
                        "training_days": {
                            "monday": "monday" in value,
                            "tuesday": "tuesday" in value,
                            "wednesday": "wednesday" in value,
                            "thursday": "thursday" in value,
                            "friday": "friday" in value,
                            "saturday": "saturday" in value,
                            "sunday": "sunday" in value,
                        },
                        "rhr": value['rhr']
                    }, file, indent = 4
                )
                
                self.redirect("/")

            case _:
                self.send_response(200)
                file_type = self.path.split(".")[-1]
                self.send_header("Content-type", f"image/{file_type}")
                self.end_headers()
                with open("web"+self.path, "rb") as file:
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

# NOTE
# 1 - food thing

# 2 - individual activities view

# 3 -

# 4 - 

# 5 - put stuff in the home page

# 6 - remove the defult case off get for lewis to do

# NOTE/BUG/FIXME/TODO

### Think done needs bug testing BUG 

# 1 - upload info from sign up questions into users json file

# 2 - add activaites when user trys too