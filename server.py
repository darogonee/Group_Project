from http.server import BaseHTTPRequestHandler, HTTPServer
import python.Api, os, random, calendar
from python.hash_function import password_hash 
from python.Nutrition_Calculator import nutrition_calculator as nc
from datetime import datetime
from python.Create_Program import create_program
from python.requirements import *
import time, json, datetime, uuid 
from datetime import date
from python.polyline_decoder import decode_polyline

MIME_TYPES = {
    "svg": "image/svg+xml",
    "png": "image/png",
    "jpg": "image/jpg"
}

food_not_found_alert_script = """
                <script>
                    window.onload = function() {
                        alert("Food not found. Please enter a valid food");
                    };
                </script>
                """

# NOTE restart server aprox 30 days NOTE

hostName = "localhost"
serverPort = 8080

uuid2user = {}

class FittnessServer(BaseHTTPRequestHandler):
    # def _set_response(self):
    #     self.send_response(200)
    #     self.send_header('Content-type', 'text/html')
    #     self.end_headers()

    # def do_POST(self):
    #     content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
    #     post_data = self.rfile.read(content_length) # <--- Gets the data itself
    #     content = json.loads(post_data.decode('utf-8'))
    #     match content["title"]:
    #         case "edit-json":
    #             data = json.load("data/"+content["body"][0])
                # del data["food_log"][content["body"][1]]

    #             response = "deletion-successful"
    #         case _:
    #             response = "err:invalid-title"


    #     self._set_response()
    #     if type(response) != type(""):
    #         response = json.dumps(response)
    #     self.wfile.write(bytes('{"response":'+response+',"title":"'+content["title"]+'"}',"utf-8"))
    #     print("request fulfilled")

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

    def get_username(self):
        cookie = self.get_cookie()
        if "user" in cookie:
            if cookie["user"] in uuid2user:
                return uuid2user[cookie["user"]]       
        self.redirect("/signin")

    def get_user_data(self, folder):
        try:
            user = self.get_username()
            user_data_file = f"{folder}/{user}.json"
            with open(user_data_file, "r") as data_file:
                data = json.load(data_file)
            return data
        except:
            return False
        
    def get_current_date(self):
        current_date = str(datetime.date.today())

        return current_date
    
    def map_bounds(self, cords):
        most_north = cords[0][0]
        most_south = cords[0][0]
        most_east  = cords[0][1]
        most_west  = cords[0][1]
        for lat, lng in cords:
            most_north = max(most_north, lat)
            most_south = min(most_south, lat)
            most_east  = max(most_east,  lng)
            most_west  = min(most_west,  lng)
        size = (most_north - most_south +  most_east - most_west)*2
        return most_north, most_south, most_east, most_west, size
    
    def do_GET(self):
        match self.path.split("?")[0]:
            case "/regenerate_my_program":
                user = self.get_username()
                with open(f"program/{user}.json", "r") as read_user_data:
                    user_data = json.load(read_user_data)
                
                program = create_program(user_data)
                user_data["program"] = program
                

                with open(f"program/{user}.json", "w") as write_user_data:
                    json.dump(user_data, write_user_data)

                self.redirect("/myprogram")

            case "/myprogram":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("web/html/myprogram.html", "r") as myprogram_file:
                    with open("web/html/html-template/myprogram-template.html", "r") as myprogram_template_file:
                        myprogram_template = myprogram_template_file.read()
                        data = self.get_user_data("user_data")
                        program = create_program(data)
                        username = self.get_username()
                        data["program"] = program
                        with open(f"program/{username}.json", "w") as file:
                            json.dump(data, file)


                        tbody = ""
                        myprogram = myprogram_template
          
                        for day, exercises in program.items():
                            if isinstance(exercises, list):
                                name_body = ""
                                reps_body = ""
                                sets_body = ""
                                muscle_group_body = ""
                                for exercise in program[day]:
                                    name_body = name_body + f"<a href='https://www.muscleandstrength.com/exercises/{exercise['exercise_name'].lower().replace(' ', '-')}.html'>{exercise['exercise_name']}</a>" + "<br>"
                                    reps_body = reps_body + exercise["reps"] + "<br>"
                                    sets_body = sets_body + exercise["sets"] + "<br>"
                                    muscle_group_body = muscle_group_body + exercise["muscle_group"] + "<br>"
                                
                                myprogram = myprogram.replace(f"template_{day}_name", name_body)
                                myprogram = myprogram.replace(f"template_{day}_reps", reps_body)
                                myprogram = myprogram.replace(f"template_{day}_sets", sets_body)
                                myprogram = myprogram.replace(f"template_{day}_muscle_group", muscle_group_body)
                                
                            else:
                                if exercises == "Rest":
                                    myprogram = myprogram.replace(f"template_{day}_name", "")
                                else:
                                    myprogram = myprogram.replace(f"template_{day}_name", str(program[day]))
                                myprogram = myprogram.replace(f"template_{day}_reps", "")
                                myprogram = myprogram.replace(f"template_{day}_sets", "")
                                myprogram = myprogram.replace(f"template_{day}_muscle_group", "")
                                myprogram = myprogram.replace(f"template_{day}_reps", "")


                        tbody += myprogram
                        myprogram_final = myprogram_file.read().replace("template_myprogram", tbody)                         
                        self.wfile.write(myprogram_final.encode())

            case "/remove_sqn":
                user = self.get_username()
                os.remove(f"user_data/{user}.json")
                self.redirect("/signupqs")

            case "/logfood&water":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                user = self.get_username()
                with open("web/html/logfood&water.html", "r") as file:
                    logfoodwater_page = file.read()
                    self.wfile.write(logfoodwater_page.encode())

                with open(f"temp_nutrition_log/{user}.json", "w") as file:
                    json.dump({}, file)

                with open(f"perm_nutrition_log/{user}.json", "r") as user_data_file:
                    user_data = json.load(user_data_file)

                try:
                    for date_data in user_data["nutrition_log"].values():
                        date_data["data_transferred"] = "False"
                except KeyError:
                    pass
            
                with open(f"perm_nutrition_log/{user}.json", "w") as write_user_data_file:
                    json.dump(user_data, write_user_data_file)


            case "/action_logfood&water": # delete data from json file if delete button pressed
                user = self.get_username()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                query = self.query()
                name = query["food_name"]
                quantity = query["amount"]
                units = query["food_units"]
                date = query["log_food_date"]

                
                food_not_found = True
                existing_food_log = False

                try:
                    with open(f"temp_nutrition_log/{user}.json", "r") as file:
                        data = json.load(file)

                except:
                    data = {"date":date, "food_log":[]}

                with open(f"perm_nutrition_log/{user}.json", "r") as user_data_file:
                    user_data = json.load(user_data_file)

                if "nutrition_log" in user_data.keys():
                    if date in user_data["nutrition_log"].keys():
                        existing_food_log = True
                    else:
                        existing_food_log = False
                    
                try:
                    if date != data["date"]:
                        data = {"date":date, "food_log":[]}
                except KeyError:
                    data = {"date":date, "food_log":[]}

                 # if food log with date given in query exists in user_data, add this data to nutrititionlog.json
                if existing_food_log:
                    if user_data["nutrition_log"][date]["data_transferred"] == "False":
                        for i in range(len(user_data["nutrition_log"][date]["food"])):
                            data["food_log"].append(user_data["nutrition_log"][date]["food"][i])
                            
                        user_data["nutrition_log"][date]["data_transferred"] = "True"

                        with open(f"perm_nutrition_log/{user}.json", "w") as write_user_data:
                            json.dump(user_data, write_user_data)

                try:
                    nutrition = nc(quantity, units, name)
                    data["food_log"].append({"name":" ".join(name.split("+")), "quantity":str(quantity), "units":str(units), "calories":str(nutrition["calories"]), "carbs":str(nutrition["carbs"]), "fat":str(nutrition["fat"]), "protein":str(nutrition["protein"])})
                    data["date"] = date
                    with open(f"temp_nutrition_log/{user}.json", "w") as file:
                        json.dump(data, file)
                    food_not_found = False

                except IndexError:
                    food_not_found = True

                with open("web/html/logfood&water.html", "r") as food_water_file:
                    with open("web/html/html-template/nutrition-template.html", "r") as food_water_template_file:
                        food_water_template = food_water_template_file.read()
                        tbody = ""
                        for i in range(len(data["food_log"])):
                            food_water = food_water_template
                            food_water = food_water.replace("template_quantity", data["food_log"][i]["quantity"])
                            food_water = food_water.replace("template_units", data["food_log"][i]["units"])
                            food_water = food_water.replace("template_food_name", data["food_log"][i]["name"])
                            food_water = food_water.replace("template_food_calories", data["food_log"][i]["calories"])
                            food_water = food_water.replace("template_carbs", data["food_log"][i]["carbs"])
                            food_water = food_water.replace("template_protein", data["food_log"][i]["protein"])
                            food_water = food_water.replace("template_fat", data["food_log"][i]["fat"])

                            tbody += food_water

                        food_water = food_water_template
                        food_water = food_water.replace('<button onclick="deleteRow(this)">Delete</button>', "")
                        food_water = food_water.replace("template_quantity", "")
                        food_water = food_water.replace("template_units", "")
                        food_water = food_water.replace("template_food_name", "<b>Total</b>")
                        food_water = food_water.replace("template_food_calories", "<b>" + str(round(sum(float(item["calories"]) for item in data["food_log"]), 1))+"</b>")
                        food_water = food_water.replace("template_carbs", "<b>"+str(round(sum(float(item["carbs"]) for item in data["food_log"]), 1))+"</b>")
                        food_water = food_water.replace("template_protein", "<b>"+str(round(sum(float(item["protein"]) for item in data["food_log"]), 1))+"</b>")
                        food_water = food_water.replace("template_fat", "<b>"+str(round(sum(float(item["fat"]) for item in data["food_log"]), 1))+"</b>")

                        tbody += food_water

                        food_water_final = ""

                        food_water_final = food_water_file.read().replace("template_nutrition", tbody)  

                        if food_not_found:
                            food_water_final = food_water_final.replace("</body>", food_not_found_alert_script + "</body>")  

                        self.wfile.write(food_water_final.encode())
                    
            case "/action_confirm_food_log":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                user = self.get_username()
                with open(f"temp_nutrition_log/{user}.json", "r") as nutrition_log:
                    logged_data = json.load(nutrition_log)

                with open(f"perm_nutrition_log/{user}.json", "r") as user_data_file:
                    user_data = json.load(user_data_file)

                total_calories = str(round(sum(float(item["calories"]) for item in logged_data["food_log"]), 1))
                total_carbs = str(round(sum(float(item["carbs"]) for item in logged_data["food_log"]), 1))
                total_fat = str(round(sum(float(item["fat"]) for item in logged_data["food_log"]), 1))
                total_protein = str(round(sum(float(item["protein"]) for item in logged_data["food_log"]), 1))
                date = logged_data["date"]

                if not "nutrition_log" in user_data:
                    user_data["nutrition_log"] = {}
                
                user_data["nutrition_log"][date] = {"food":logged_data["food_log"], "totals":{"total_calories":total_calories, "total_carbs":total_carbs, "total_fat":total_fat, "total_protein":total_protein}}

                with open(f"perm_nutrition_log/{user}.json", "w") as user_data_file:
                    json.dump(user_data, user_data_file)

                
                self.redirect("/logfood&water")

                

                    
            case  "/activities":
                user = self.get_username()
                self.send_response(200)
                self.send_header("Content-type", "text/html")

                self.end_headers()
                with open("web/html/activities.html", "r") as activities_file:
                    with open("web/html/html-template/activity-template.html", "r") as activity_file:
                        activity_template = activity_file.read()
                        # later check
                        python.Api.refresh(user)
                        activity_data = python.Api.get_user_activites(user)
                        # change the number to how ever many activities you want to load
                        table_activity_data = []
                        tbody=""
                        for i in range(min(200, len(activity_data))):
                            activity_type = self.query().get("type", "")
                            if activity_data[i]['type'] == activity_type or activity_type == "":
                                activity = activity_template 
                                activity = activity.replace("template_type", str(activity_data[i]["type"])) 

                                input_datetime = datetime.datetime.strptime(activity_data[i]["start_date_local"], "%Y-%m-%dT%H:%M:%SZ")
                                formatted_date = input_datetime.strftime("%a, %d/%m/%Y")         
                                activity = activity.replace("template_date", str(formatted_date))
                                activity = activity.replace("template_id", str(activity_data[i]['upload_id'])) #not working

                                
                                if "-" not in activity_data[i]["name"]:
                                    activity_string = str(activity_data[i]["name"])[:25]
                                    if len(str(activity_data[i]["name"])) >= 25:
                                        activity_string = activity_string + "..."
                                    activity = activity.replace("template_name", activity_string)
                                    
                                else:
                                    activity = activity.replace("template_name", str(activity_data[i]["name"]).split("-")[0])

                
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
                python.Api.get_user_activites.clear_args(user)
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
                with open("data/passwords.json", "r") as file:
                    data = json.load(file)  
                values = self.query()
                username = values["username"].lower()
                if username in data:
                    hash_password = password_hash(values["password"], data[username][1])
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    if hash_password == data[username][0]:
                        self.set_cookie(username)
                        with open("web/html/redirect.html", "r") as file:
                            self.wfile.write(file.read().replace("url", "/").encode())
                        return
                    self.redirect("/signin")
                self.redirect("/signup")
            
            case "/action_signup":
                with open("data/passwords.json", "r") as file:
                    data = json.load(file)
                values = self.query()
                username = values["username"].lower()
                if username in data:
                    self.redirect("/signin")
                    return
                if len(username) < 3 or len(username) > 13 or values["password"] != values["password-rentry"] or not username.isalnum():
                    self.redirect("/signup")
                    return
                
                salt = uuid.uuid4().hex
                
                hash_password = password_hash(values["password"], salt)

                self.send_response(200)
                self.send_header("Content-type", "text/html")

                data[username] = [hash_password, salt]
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


                user = self.get_username()
                cookie = self.get_cookie()
                if "user" not in cookie:
                    self.redirect("/signin")
                    return
                if not python.Api.check(user):
                    self.redirect("https://www.strava.com/oauth/authorize?client_id=112868&redirect_uri=http%3A%2F%2Flocalhost:8080/oauth&response_type=code&scope=activity%3Aread_all,activity%3Awrite")
                    return
                if not os.path.exists(f"user_data/{user}.json"):
                    self.redirect("/signupquestions")
                    return
                date = self.get_current_date()
                

                with open("web/html/home.html", "r") as home_file:
                    with open(f"user_data/{user}.json", "r") as user_data_file:
                        user_data = json.load(user_data_file)

                    now = datetime.datetime.now()
                    startofmonth = datetime.date(now.year, now.month, 1).strftime('%s')
                    month_activitys = python.Api.get_user_activites(user, param = {'per_page': 200, 'page': 1, 'after': startofmonth})

                    try:
                        recent_activity = month_activitys[0]
                    except:
                        recent_activity = {'resource_state': 2, 'athlete': {'id': 59474850, 'resource_state': 1}, 'name': 'n/a', 'distance': 0, 'moving_time': 0, 'elapsed_time': 0, 'total_elevation_gain': 0, 'type': 'Run', 'sport_type': 'Run', 'workout_type': 0, 'id': 10151679572, 'start_date': '2023-11-02T07:19:42Z', 'start_date_local': '2023-11-02T18:19:42Z', 'timezone': '(GMT+10:00) Australia/Hobart', 'utc_offset': 39600.0, 'location_city': None, 'location_state': None, 'location_country': None, 'achievement_count': 0, 'kudos_count': 3, 'comment_count': 0, 'athlete_count': 1, 'photo_count': 0, 'map': {'id': 'a10151679572', 'summary_polyline': '', 'resource_state': 2}, 'trainer': False, 'commute': False, 'manual': True, 'private': False, 'visibility': 'everyone', 'flagged': False, 'gear_id': 'g15342740', 'start_latlng': [], 'end_latlng': [], 'average_speed': 3.342, 'max_speed': 0, 'has_heartrate': False, 'heartrate_opt_out': False, 'display_hide_heartrate_option': False, 'upload_id': None, 'external_id': None, 'from_accepted_tag': False, 'pr_count': 0, 'total_photo_count': 0, 'has_kudoed': False}


                    cords = []
                    most_north = most_south = most_east = most_west = size = 0
                    
                    if "map" in recent_activity and "summary_polyline" in recent_activity['map'] and recent_activity['map']['summary_polyline']:
                        cords = decode_polyline(recent_activity['map']['summary_polyline'])
                        most_north, most_south, most_east, most_west, size = self.map_bounds(cords)
    
                    try:
                        total_calories = user_data["nutrition_log"][date]["totals"]["total_calories"]
                        goal_cals = user_data["goal_cals"]
                        calories_remaining = int(float(goal_cals)) - int(float(total_calories))
                        try:
                            calories_percent_eaten = int(round(int(total_calories) / int(goal_cals) * 100))
                        except:
                            calories_percent_eaten = "0"
                            
                    except KeyError:
                        total_calories = "N/A"
                        goal_cals = "N/A"
                        calories_percent_eaten = "N/A"
                        calories_remaining = "N/A"

                    calories_content_body = f"{str(total_calories)}/{str(goal_cals)}<br>({str(calories_percent_eaten)}% of goal)<br>{str(calories_remaining)} calories remaining"
                    formatted_time = time.strftime('%H:%M:%S', time.gmtime(recent_activity["moving_time"]))
                   
                    input_datetime = datetime.datetime.strptime(recent_activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ")
                    formatted_date = input_datetime.strftime("%a, %d/%m/%Y")  


                    month_distance = 0
                    month_time = 0
                    for activity in month_activitys:
                        month_distance += activity['distance']
                        month_time += activity['moving_time']       
                    
                    home_page = (home_file.read().replace("calories_content", calories_content_body)
                        .replace("template_topleft", str([most_north + size, most_west - size]))
                        .replace("template_bottomright", str([most_south - size, most_east + size]))
                        .replace("template_points", str([list(coord) for coord in cords]))
                        .replace("template_activity_name", recent_activity['name'])
                        .replace("template_type", recent_activity['type'])
                        .replace("template_distance", str(round(recent_activity['distance']/1000, 2))+"km")
                        .replace("template_date", formatted_date)
                        .replace("template_time", formatted_time)
                        .replace("template_lastm_distance", str(round(month_distance/1000, 2))+"km")
                        .replace("template_lastm_activities", str(len(month_activitys)))
                        .replace("template_lastm_ttime", str(datetime.timedelta(seconds=month_time)))
                    )
                    self.wfile.write(home_page.encode())
                    
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
                
                #do calories
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
                    workout_time, value['distance'], value['elev-gain'], value['description'], 0, 0, 
                    int(value['percieved-exertion']), exercises)


            case "/myprofile":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                user = self.get_username()

                with open("web/html/myprofile.html", "r") as file:
                    myprofile_page = file.read()
                    myprofile_page = myprofile_page.replace("name-temp", user)
                    user_data_pro = open(f"user_data/{user}.json")
                    user_data_pro = json.load(user_data_pro)

                    birth_day = str(user_data_pro['dob']).split('-')
                    today = str(datetime.datetime.today()).split(' ')[0].split("-")
                    age = int(today[0])-int(birth_day[0])
                    myprofile_page = myprofile_page.replace("age-temp", str(age))

                    myprofile_page = myprofile_page.replace("gender-temp", user_data_pro['sex'])
                    myprofile_page = myprofile_page.replace("muscle-goals-temp", user_data_pro['muscle_goals'])
                    myprofile_page = myprofile_page.replace("cardio-temp", user_data_pro['cardio'])
                    for type in user_data_pro['fav_cardio']:
                        if user_data_pro['fav_cardio']['other'] != '':
                            type = user_data_pro['fav_cardio']['other']
                            myprofile_page = myprofile_page.replace("fav-sport-temp", type)
                        elif user_data_pro['fav_cardio'][type] == True:
                            myprofile_page = myprofile_page.replace("fav-sport-temp", type)
                    myprofile_page = myprofile_page.replace("lvl-temp", user_data_pro['level'])
                    myprofile_page = myprofile_page.replace("weight-goal-temp", user_data_pro['weight_goal'])
                    myprofile_page = myprofile_page.replace("weight-units-temp", user_data_pro['weight-units'])
                    myprofile_page = myprofile_page.replace("weight-temp", user_data_pro['weight'])
                    myprofile_page = myprofile_page.replace("height-units-temp", user_data_pro['height-units'])
                    myprofile_page = myprofile_page.replace("height-temp", user_data_pro['height'])
                    myprofile_page = myprofile_page.replace("dob-temp", user_data_pro['dob'])
                    days = []
                    for day in user_data_pro['training_days']:
                        if user_data_pro['training_days'][day] == True:
                            days.append(day)
                    myprofile_page = myprofile_page.replace("training-days-temp", str(days))
                    myprofile_page = myprofile_page.replace("dob-temp", user_data_pro['dob'])
                    myprofile_page = myprofile_page.replace("rhr-temp", user_data_pro['rhr'])
                    equipment = []
                    for key,value in user_data_pro['equipment'].items():
                        if value:
                            equipment.append(key)
                    myprofile_page = myprofile_page.replace("equipment-temp", "<br>".join(equipment))

                    if python.Api.check(user):    
                        myprofile_page = myprofile_page.replace("Strava Api: False", "Strava Api: True")                
                    
                    self.wfile.write(myprofile_page.encode())

            case "/activity":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                user = self.get_username()
                with open("web/html/html-template/individual_activitie.html", "r") as file:
                    id = int(self.query()["id"])
                    for activity in python.Api.get_user_activites(user):
                        if id == activity["upload_id"]:
                            activity_page = file.read()
                            activity_page = (activity_page.replace("template_name", str(activity["name"]))
                                .replace("template_distance", str(round(int(activity["distance"])/1000, 2)))
                                .replace("template_moving_time", str(round(int(activity["moving_time"])/60, 2)))
                                .replace("template_elapsed_time", str(round(int(activity["elapsed_time"])/60, 2))+"mins elapsed")
                                .replace("template_total_elevation_gain", str(activity["total_elevation_gain"]))
                                .replace("template_type", str(activity["type"]))
                                .replace("template_sport_type", str(activity["sport_type"]))
                                .replace("template_start_date", str(activity["start_date"]))
                                .replace("template_kudos_count", str(activity["kudos_count"]))
                                .replace("template_achievement_count", str(activity["achievement_count"]))
                                .replace("template_comment_count", str(activity["comment_count"]))
                                .replace("template_achievement_count", str(activity["achievement_count"]))
                                .replace("template_athlete_count", str(activity["athlete_count"]))
                                .replace("template_trainer", str(activity["trainer"]))
                                .replace("template_commute", str(activity["commute"]))
                                .replace("template_private", str(activity["private"]))
                                .replace("template_visibility", str(activity["visibility"]))
                                .replace("template_average_speed", str(activity["average_speed"]))
                                .replace("template_max_speed", str(activity["max_speed"]))
                                .replace("template_elev_high", str(activity["elev_high"]))
                                .replace("template_elev_low", str(activity["elev_low"])))
                            self.wfile.write(activity_page.encode())

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

                    goal_cals = calculate_goal_cals(calculate_eer(calculateAge(value["date_of_birth"]), imperial_to_metric_weight(int(value["weight"]), value["weight-units"]), imperial_to_metric_height(int(value["height"]), value["height-units"]), value["sex"], get_pal(str(value["pal"]))), value["weight_goal"])
                    json.dump(
                    {
                        "pal":str(get_pal(value["pal"])),
                        "muscle_goals":value["muscle_goals"],
                        "cardio":value["cardio"],
                        "fav_cardio": {
                            "running": "fav_cardio_running" in value,
                            "cycling": "fav_cardio_cycling" in value,
                            "swimming": "fav_cardio_swimming" in value,
                            "other": value["other"].replace("+", " ")
                        },
                        "level":value["level"],
                        "weight_goal": value["weight_goal"],
                        "weight-units": value["weight-units"],
                        "weight": value["weight"],
                        "height-units": value["height-units"],
                        "height": value["height"],
                        "dob": value["date_of_birth"],
                        "sex": value["sex"],
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
                            "dip-machine": "equipment_dip-machine" in value                           
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
                        "rhr": value['rhr'],
                        "goal_cals":goal_cals,
                        "goal_water":str(water_requirement(imperial_to_metric_weight(int(value["weight"]), value["weight-units"]))),
                        "goal_carbs":goal_cals/8,
                        "goal_fat": goal_cals/32,
                        "goal_protein": goal_cals/16

                    }, file, indent = 4
                )
                    
                user_file = f"{user}.json"

                
                open(f"program/{user_file}", "w")
                
                open(f"temp_nutrition_log/{user_file}", "w")
                
                open(f"perm_nutrition_log/{user_file}", "w")
                
                self.redirect("/")

            case _:
                self.send_response(200)
                file_type = self.path.split(".")[-1]
                self.send_header("Content-type", MIME_TYPES.get(file_type, f"image/{file_type}"))
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
    print()

# NOTE
# 1 - only one fav sport     why???

# 2 - 

# 3 - add intersex option when choosing sex    impossible when calculating calories

# 4 - 

# 5 - put stuff in the home page

# 6 - remove the defult case off get for lewis to do 

# NOTE/BUG/FIXME/TODO

### Think done needs bug testing BUG 

# 1 - 

# 2 - 