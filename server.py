'''
Zamo Fitness App
Programmed by Oliver Thiessen, Oliver Magill, Alex Tran, and Lewis Clennett

'''

# required imports
from http.server import BaseHTTPRequestHandler, HTTPServer

from python.Nutrition_Calculator import nutrition_calculator as nc
from python.hash_function import password_hash 
from python.pie_chart import generate_pie_chart
from python.Create_Program import create_program
from python.polyline_decoder import decode_polyline

from python.requirements import *
from datetime import datetime

import time, json, datetime, uuid, os, calendar
import python.Api

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

# NOTE restart server aprox 30 days

hostName = "localhost"
serverPort = 8080
uuid2user = {}

class FittnessServer(BaseHTTPRequestHandler):
    # sets response to 200 (Okay)
    def set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        content = json.loads(post_data.decode('utf-8'))
        match content["title"]:
            case "edit-json":
                data = json.load("data/"+content["body"][0])
                del data["food_log"][content["body"][1]]

                response = "deletion-successful"
            case "get-calories":
                date = self.get_current_date()
                perm_nutrition = self.get_user_data("perm_nutrition_log")
                user_info = self.get_user_data("user_data")
                total_calories = perm_nutrition["nutrition_log"][date]["totals"]["total_calories"]
                goal_calories = user_info["goal_cals"]
                response = [total_calories, goal_calories]
            case _:
                response = "err:invalid-title"

        self.set_response()
        if type(response) != type(""):
            response = json.dumps(response)
        self.wfile.write(bytes('{"response":'+response+',"title":"'+content["title"]+'"}',"utf-8"))
        print("request fulfilled")

    def redirect(self, link):
        self.set_response()
        with open("web/html/redirect.html", "r") as file:
            self.wfile.write(file.read().replace("url", link).encode())
    
    # query handling: returns dictionary of query split into key, value pairs
    def query(self):
        # if query is invalid
        if "?" not in self.path:
            return {}
        query_string = self.path.split("?")[1].split("&")
        values = {}
        # query split into key, value pairs
        for query in query_string:
            name = query.split("=")[0]
            value = query.split("=")[1]
            values[name] = value
        return values

    # gets cookie: returns dictionary of cookie split into key, value pairs
    def get_cookie(self):
        # handles invalid cookie
        if self.headers.get("Cookie") is None:
            return {}
        cookie = self.headers.get("Cookie").split(";")
        values = {}
        # cookie split into key, value pairs
        for query in cookie:
            name = query.split("=")[0].strip()
            value = query.split("=")[1].strip()
            values[name] = value
        return values
    
    # sets cookie
    def set_cookie(self, user):
        user_uuid = uuid.uuid4().hex
        uuid2user[user_uuid] = user
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=30) # expires in 30 days
        self.send_header("Set-Cookie", f"user={user_uuid}; Expires={expires.strftime('%a, %d %b %Y %H:%M:%S GMT')}")
        self.end_headers()

    # gets username
    def get_username(self):
        cookie = self.get_cookie()
        if "user" in cookie: 
            if cookie["user"] in uuid2user:
                return uuid2user[cookie["user"]]       
        self.redirect("/signin") # redirected to signin page if cookie or user invalid

    # returns user data from specified folder 
    def get_user_data(self, folder):
        user = self.get_username() # get username
        if os.path.exists(f"{folder}/{user}.json"): # check file exists
            user_data_file = f"{folder}/{user}.json"
            # read file
            with open(user_data_file, "r") as data_file:
                data = json.load(data_file)
            return data
        else:
            return False
    # returns current date
    def get_current_date(self):
        current_date = str(datetime.date.today())

        return current_date
    
    # thiessen can do this cos idk what it does
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
    
    @staticmethod
    def calculate_color(difference):
        if difference <= 0.5: # if the difference is between 0 and 0.5 (green @ 0 - yellow @ 0.5)
            return (2 * difference, 1, 0)
        elif difference < 1: # if the difference is between 0.5 and 1 (yellow @ 0.5 - red @ 1)
            return (1, -2 * difference + 2, 0)
        else: # if difference over 1 (red)
            return (1, 0, 0)
    
    # returns colours for pie chart based on % of calories taken up by different macronutrients
    def get_pie_colours(self, carbs_calories_percent, protein_calories_percent, fat_calories_percent):
        # decimal difference between goal % and actual %
        carbs_dif = round(abs(50 - carbs_calories_percent) / ((50 + carbs_calories_percent) / 2), 2)
        protein_dif = round(abs(25 - protein_calories_percent) / ((25 + protein_calories_percent) / 2), 2)
        fat_dif = round(abs(25 - fat_calories_percent) / ((25 + fat_calories_percent) / 2), 2)

        # get color based on differences
        carbs_colour = self.calculate_color(carbs_dif)
        protein_colour = self.calculate_color(protein_dif)
        fat_colour = self.calculate_color(fat_dif)

        return [carbs_colour, protein_colour, fat_colour]
    
    @staticmethod
    def calculate_sign(under_goal):

        if under_goal < 0:
            sign = "↑"
        elif under_goal == 0:
            sign = "-"
        else:
            sign = "↓"
        
        return sign
    
    def do_GET(self):
        match self.path.split("?")[0]:
            case "/regenerate_my_program":
                user = self.get_username()

                user_data = self.get_user_data("user_data")
                my_program_data = self.get_user_data("program")
            
                program = create_program(user_data)  # create new program
                my_program_data["program"] = program
                
                with open(f"program/{user}.json", "w") as write_my_program: # write new program
                    json.dump(program, write_my_program)

                self.redirect("/myprogram") # redirect to myprogram page


            case "/food":
                self.set_response()
                user = self.get_username()
                with open("web/html/food.html", "r") as food_file:
                    with open("web/html/html-template/nutrition_table_template.html", "r") as food_template_file:
                        food_template = food_template_file.read()
                        food_file = food_file.read()
                        food_file = food_file.replace("template_profile_img", python.Api.athelete_profile_img(user))
                        nutrition_log_data = self.get_user_data("perm_nutrition_log")
                        user_data = self.get_user_data("user_data")
                        tbody = ""
                        
                        if "nutrition_log" in nutrition_log_data: 
                            for date,food_data in nutrition_log_data["nutrition_log"].items(): # iterates over all dates logged 
                                food = food_template
                                food = food.replace("template_date", datetime.datetime.strptime(date, '%Y-%m-%d').strftime("%a, %d/%m/%Y")) # formatted date in html
                                food_list = ""
                                for i in range(len(food_data["food"])): # iterates over all food in date
                                    if food_data["food"][i]["quantity"] == "serve": 
                                        food_quantity = "x"
                                    else:
                                        food_quantity = food_data["food"][i]["quantity"]
                                    
                                    food_list = f'{food_list}{food_quantity} {food_data["food"][i]["units"]} {food_data["food"][i]["name"]}<br>' # formatted list of food

                                food = food.replace("template_food_list", food_list)  

                                # cals and macros logged
                                total_carbs = int(float(food_data["totals"]["total_carbs"]))
                                total_protein = int(float(food_data["totals"]["total_protein"]))
                                total_fat = int(float(food_data["totals"]["total_fat"]))
                                total_calories = int(float(food_data["totals"]["total_calories"]))

                                # goal cals and macros
                                goal_carbs = int(float(user_data["goal_carbs"]))
                                goal_protein = int(float(user_data["goal_protein"]))
                                goal_fat = int(float(user_data["goal_fat"]))
                                goal_cals = int(float(user_data["goal_cals"]))

                                # percentage of calories taken up by each macronutrient
                                carbs_calories_percent = int((total_carbs * 4)/total_calories * 100) 
                                protein_calories_percent = int((total_protein * 4)/total_calories * 100)
                                fat_calories_percent = int((total_fat * 9)/total_calories * 100)
                                
                                # percentage under goal
                                carbs_under_goal = (goal_carbs - total_carbs)/goal_carbs
                                protein_under_goal = (goal_protein - total_protein)/goal_protein
                                fat_under_goal = (goal_fat - total_fat)/goal_fat
                                calories_under_goal = (goal_cals - total_calories)/goal_cals

                                # get pie chart colour and sign based on percentage under goal
                                carbs_sign = self.calculate_sign(carbs_under_goal)
                                protein_sign = self.calculate_sign(protein_under_goal)
                                fat_sign = self.calculate_sign(fat_under_goal)
                                calories_sign = self.calculate_sign(calories_under_goal)

                                # display on nutrition log table
                                carbs_display = f"Carbs: {total_carbs}g ({round(abs(carbs_under_goal)*100)}% {carbs_sign})</p>"
                                protein_display = f"Protein: {total_protein}g ({round(abs(protein_under_goal)*100)}% {protein_sign})</p>"
                                fat_display = f"Fat: {total_fat}g ({round(abs(fat_under_goal)*100)}% {fat_sign})</p>"
                                calories_display = f"Calories: {total_calories} kcal ({round(abs(calories_under_goal)*100)}% {calories_sign})</p>"

                                # generate and save pie chart to user folder
                                generate_pie_chart([carbs_calories_percent, protein_calories_percent, fat_calories_percent], ["Carbohydrates", "Protein", "Fat"], self.get_pie_colours(carbs_calories_percent, protein_calories_percent, fat_calories_percent), f"pie_chart_{date}.png", user)
                                food = food.replace("template_macros", f"{carbs_display}<br><br>{protein_display}<br><br>{fat_display}<br><br>{calories_display}")
                                food = food.replace("template_pie_chart", f"<img src='images/generated/user_charts/{user}/pie_chart_{date}.png'")
                    
                                tbody += food
        
                    food_final = food_file.replace("template_nutrition_table", tbody)
                    self.wfile.write(food_final.encode()) # write replaced html to html file

            case "/myprogram":
                self.set_response()
                with open("web/html/myprogram.html", "r") as myprogram_file:
                    with open("web/html/html-template/myprogram-template.html", "r") as myprogram_template_file:
                        myprogram_template = myprogram_template_file.read()
                        my_program_data = self.get_user_data("program")
                        user_data = self.get_user_data("user_data")
                        username = self.get_username()
                        myprogram_file = myprogram_file.read()
                        myprogram_file = myprogram_file.replace("template_profile_img", python.Api.athelete_profile_img(username))
                        if "program" not in my_program_data:
                            program = create_program(user_data)
                            my_program_data["program"] = program
                            with open(f"program/{username}.json", "w") as file:
                                json.dump(my_program_data, file)
                        else:
                            program = my_program_data["program"]

                        tbody = ""
                        myprogram = myprogram_template
          
                        for day, exercises in program.items(): 
                            if isinstance(exercises, list): # if weightlifting 
                                name_body = ""
                                reps_body = ""
                                sets_body = ""
                                muscle_group_body = ""
                                for exercise in exercises: # iterates over exercises in program
                                    name_body += f"<a href='https://www.muscleandstrength.com/exercises/{exercise['exercise_name'].lower().replace(' ', '-')}.html'>{exercise['exercise_name']}</a>" + "<br>" #links wesbite that gives tutorial on how to do exercise
                                    reps_body += exercise["reps"] + "<br>"
                                    sets_body += exercise["sets"] + "<br>"
                                    muscle_group_body += exercise["muscle_group"] + "<br>"
                                
                                # replace html for name, reps, sets, and muscle group
                                myprogram = (myprogram.replace(f"template_{day}_name", name_body)
                                    .replace(f"template_{day}_reps", reps_body)
                                    .replace(f"template_{day}_sets", sets_body)
                                    .replace(f"template_{day}_muscle_group", muscle_group_body)
                                )
                            else: # if cardio or rest day
                                if exercises == "Rest":
                                    myprogram = myprogram.replace(f"template_{day}_name", "") # rest day nothing in row
                                else:
                                    myprogram = myprogram.replace(f"template_{day}_name", str(program[day])) # cardio

                                # replace html for name, reps, sets, and muscle group
                                myprogram = (myprogram.replace(f"template_{day}_reps", "")
                                    .replace(f"template_{day}_sets", "")
                                    .replace(f"template_{day}_muscle_group", "")
                                    .replace(f"template_{day}_reps", "")
                                )
                        tbody += myprogram
                        myprogram_final = myprogram_file.replace("template_myprogram", tbody)                         
                        self.wfile.write(myprogram_final.encode()) # write to myprogram file

            case "/remove_sqn": # remove user data file and redirect to reenter signup questions
                user = self.get_username()
                os.remove(f"user_data/{user}.json")
                self.redirect("/signupqs")

            case "/logfood": 
                self.set_response()
                user = self.get_username()
                with open("web/html/logfood.html", "r") as file:
                    logfoodwater_page = file.read()
                    logfoodwater_page = logfoodwater_page.replace("template_profile_img", python.Api.athelete_profile_img(user))
                    self.wfile.write(logfoodwater_page.encode())

                # clear temporary nutrition log
                with open(f"temp_nutrition_log/{user}.json", "w") as file:
                    json.dump({}, file)

                # load permanent nutrition log
                with open(f"perm_nutrition_log/{user}.json", "r") as file:
                    perm_nutrition_data = json.load(file)

                if "nutrition_log" in perm_nutrition_data: # if there is a log
                    for date_data in perm_nutrition_data["nutrition_log"].values(): 
                        date_data["data_transferred"] = "False" # data transferred ensures that all data is transferred from temp to perm nutrition log

                with open(f"perm_nutrition_log/{user}.json", "w") as write_perm_nutrition:
                    json.dump(perm_nutrition_data, write_perm_nutrition)

            case "/action_logfoodauto": 
                user = self.get_username()
                self.set_response()

                query = self.query()
                name = query["food_name"]    
                quantity = query["amount"]
                units = query["food_units"]
                date = query["log_food_date"]
                
                food_not_found = True
                existing_food_log = False

                if os.path.exists(f"temp_nutrition_log/{user}.json"):
                    with open(f"temp_nutrition_log/{user}.json", "r") as file:
                        data = json.load(file)
                else:
                    data = {"date":date, "food_log":[]}

                if not os.path.exists(f"perm_nutrition_log/{user}.json"):
                    with open(f"perm_nutrition_log/{user}.json", "w") as file:
                        json.dump({}, file)

                with open(f"perm_nutrition_log/{user}.json", "r") as perm_nutrition_log:
                    perm_nutrition_data = json.load(perm_nutrition_log)

                
                if "nutrition_log" in perm_nutrition_data.keys(): 
                    if date in perm_nutrition_data["nutrition_log"].keys(): # perm nutrition log exists
                        existing_food_log = True
                    else:
                        existing_food_log = False
                    
                try:
                    if date != data["date"]: # if query date is not date in temp log, 
                        data = {"date":date, "food_log":[]} 
                except KeyError:
                    data = {"date":date, "food_log":[]}

                 # if food log with date given in query exists in temp file, add this data to perm file
                if existing_food_log:
                    if perm_nutrition_data["nutrition_log"][date]["data_transferred"] == "False": # data not transferred from temp -> perm
                        for i in range(len(perm_nutrition_data["nutrition_log"][date]["food"])): # number of foods logged in date
                            data["food_log"].append(perm_nutrition_data["nutrition_log"][date]["food"][i]) # add to permanent food log  
                            
                        perm_nutrition_data["nutrition_log"][date]["data_transferred"] = "True" # data is transferred

                        with open(f"perm_nutrition_log/{user}.json", "w") as write_perm_nutrition: # write to perm food log
                            json.dump(perm_nutrition_data, write_perm_nutrition)

                try:
                    nutrition = nc(quantity, units, name) # get macros and calories of specified food
                    data["food_log"].append({"name":" ".join(name.split("+")), "quantity":str(quantity), "units":str(units), "calories":str(nutrition["calories"]), "carbs":str(nutrition["carbs"]), "fat":str(nutrition["fat"]), "protein":str(nutrition["protein"])})
                    data["date"] = date
                    with open(f"temp_nutrition_log/{user}.json", "w") as file: # write to temp log
                        json.dump(data, file) 
                    food_not_found = False

                except IndexError: # if food is not found
                    food_not_found = True

                with open("web/html/logfood.html", "r") as food_file:
                    with open("web/html/html-template/nutrition-template.html", "r") as food_template_file:
                        food_template = food_template_file.read()
                        tbody = ""
                        for i in range(len(data["food_log"])): # 
                            food = food_template
                            food = (food.replace("template_quantity", data["food_log"][i]["quantity"]) # replaces template info with actule info
                            .replace("template_units", data["food_log"][i]["units"])
                            .replace("template_food_name", data["food_log"][i]["name"])
                            .replace("template_food_calories", data["food_log"][i]["calories"])
                            .replace("template_carbs", data["food_log"][i]["carbs"])
                            .replace("template_protein", data["food_log"][i]["protein"])
                            .replace("template_fat", data["food_log"][i]["fat"])
                        )
                            tbody += food

                        food = food_template
                        food = (food.replace('<button onclick="deleteRow(this)">Delete</button>', "") # replace template info with actule info
                            .replace("template_quantity", "")
                            .replace("template_units", "")
                            .replace("template_food_name", "<b>Total</b>")
                            .replace("template_food_calories", "<b>" + str(round(sum(float(item["calories"]) for item in data["food_log"]), 1))+"</b>")
                            .replace("template_carbs", "<b>"+str(round(sum(float(item["carbs"]) for item in data["food_log"]), 1))+"</b>")
                            .replace("template_protein", "<b>"+str(round(sum(float(item["protein"]) for item in data["food_log"]), 1))+"</b>")
                            .replace("template_fat", "<b>"+str(round(sum(float(item["fat"]) for item in data["food_log"]), 1))+"</b>")
                        )
                        tbody += food

                        food_final = ""

                        food_final = food_file.read().replace("template_nutrition", tbody)  

                        if food_not_found:
                            food_final = food_final.replace("</body>", food_not_found_alert_script + "</body>")  
                        food_final = food_final.replace("template_profile_img", python.Api.athelete_profile_img(user))
                        self.wfile.write(food_final.encode()) # replace the old info in the file with the new info
                    
            case "/action_confirm_food_log":
                self.set_response()
                user = self.get_username()
            
                perm_nutrition_data = self.get_user_data("perm_nutrition_log")

                logged_data = self.get_user_data("temp_nutrition_log")

                

                if "date" in logged_data:
                    # setting nessasery veriables
                    total_calories = str(round(sum(float(item["calories"]) for item in logged_data["food_log"]), 1))
                    total_carbs = str(round(sum(float(item["carbs"]) for item in logged_data["food_log"]), 1))
                    total_fat = str(round(sum(float(item["fat"]) for item in logged_data["food_log"]), 1))
                    total_protein = str(round(sum(float(item["protein"]) for item in logged_data["food_log"]), 1))
                    date = logged_data["date"]
                    # checks if the user has nutrition file
                    if not "nutrition_log" in perm_nutrition_data: 
                        perm_nutrition_data["nutrition_log"] = {}
                    
                    perm_nutrition_data["nutrition_log"][date] = {"food":logged_data["food_log"], "totals":{"total_calories":total_calories, "total_carbs":total_carbs, "total_fat":total_fat, "total_protein":total_protein}}

                    with open(f"perm_nutrition_log/{user}.json", "w") as perm_nutrition_data_file:
                        json.dump(perm_nutrition_data, perm_nutrition_data_file)
                
                self.redirect("/logfood")

            case "/activities":
                user = self.get_username()
                self.send_response(200)
                self.send_header("Content-type", "text/html")

                self.end_headers()
                with open("web/html/activities.html", "r") as activities_file:
                    with open("web/html/html-template/activity-template.html", "r") as activity_file:
                        activity_template = activity_file.read()
                        activities_file = activities_file.read()
                        python.Api.refresh(user) # calls a function from the api file to refresh the users data
                        activity_data = python.Api.get_user_activites(user) # use the get_user_activites function and gets info from the user strava acount
                        table_activity_data = []
                        tbody=""
                        for i in range(min(200, len(activity_data))): # goes throught 200 of the user most recent activies
                            activity_type = self.query().get("type", "")
                            if activity_data[i]['type'] == activity_type or activity_type == "":
                                activity = activity_template 
                                activity = activity.replace("template_type", str(activity_data[i]["type"])) 

                                input_datetime = datetime.datetime.strptime(activity_data[i]["start_date_local"], "%Y-%m-%dT%H:%M:%SZ")
                                formatted_date = input_datetime.strftime("%a, %d/%m/%Y")         
                                activity = (activity.replace("template_date", str(formatted_date))
                                .replace("template_id", str(activity_data[i]['id'])))
                           
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

                                if "kilojoules" in activity_data[i]: # checks that the users activite recorded kilogoules
                                    activity = activity.replace("template_calories", str(round(activity_data[i]["kilojoules"]/4.184, 2))) # converts to calouries
                                else:
                                    activity = activity.replace("template_calories", "0") # if theres no kilogoues record set it to 0

                                tbody += activity # adds the template data replaced to tbody each time the loop is run

                                table_activity_data.append({"type":activity_data[i]["type"], "date":activity_data[i]["start_date_local"], "name":activity_data[i]["name"], "time":str(activity_data[i]["moving_time"]), "distance":str(distancekm), "elevgain":str(activity_data[i]["total_elevation_gain"])})
                        activities_file = activities_file.replace("template_profile_img", python.Api.athelete_profile_img(user))
                        activity_final = activities_file.replace("template_activities", tbody) # replaces template_activities with tbody                                          
                        self.wfile.write(activity_final.encode())
     
            case "/logout":
                uuid2user.pop(self.get_cookie()['user']) # removes the cookie from the users browser

            case "/refresh": # call get_user_activites.clear_args to clear the cache and refresh it
                user = self.get_username()
                values = self.query()
                python.Api.get_user_activites.clear_args(user)
                self.redirect(values["path"])
              
            case "/oauth":
                values = self.query()
                code = values["code"]
                cookie = self.get_cookie()  
                if "user" not in cookie: # check if the user has a cookie
                    self.redirect("/signin") # if they dont it redirects them to the signup page
                    return  
                user = self.get_username()            
                python.Api.save(*python.Api.get_access(python.Api.client_id, python.Api.client_secret, code), f"users/{user}.json")
                self.redirect("/")

            case "/main.css": # loads the main.css file
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("web/css/main.css", "rb") as file:
                    self.wfile.write(file.read())
            
            case "/main.js": # loads the main.js file
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.end_headers()
                with open("web/js/main.js", "rb") as file:
                    self.wfile.write(file.read())
            
            case "/signin": # loads the sign pages html
                self.set_response()
                with open("web/html/signin.html", "r") as file:
                    login_page = file.read()                        
                    self.wfile.write(login_page.encode())

            case "/action_signin":
                with open("data/passwords.json", "r") as file:
                    data = json.load(file)
                values = self.query()
                username = values["username"].lower().replace("+", "")
                if username in data: # checks if the user already exists
                    hash_password = password_hash(values["password"].replace("+", ""), data[username][1])
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    if hash_password == data[username][0]: # checks if the password the user put in is the same as the password in the password json file
                        self.set_cookie(username)
                        with open("web/html/redirect.html", "r") as file:
                            self.wfile.write(file.read().replace("url", "/").encode()) # if they match redirects them to the home page
                        return
                    self.redirect("/signin")
                self.redirect("/signup")
            
            case "/action_signup":
                with open("data/passwords.json", "r") as file:
                    data = json.load(file)
                values = self.query()
                username = values["username"].lower().replace("+", "")
                if username in data: # checks if the user already exist
                    self.redirect("/signin") # if it does take the user to the login page
                    return
                if len(username) < 3 or len(username) > 24 or values["password"].replace("+", "") != values["password-rentry"].replace("+", ""): # if it doesnt exist check the legn of the password entered
                    self.redirect("/signup")
                    return
                
                salt = uuid.uuid4().hex
                
                hash_password = password_hash(values["password"].replace("+", ""), salt) # hashes the password the user put in origanly

                self.send_response(200)
                self.send_header("Content-type", "text/html")

                data[username] = [hash_password, salt] # add the user uuid and hashed password to the passwords file
                with open("data/passwords.json", "w") as file:
                    json.dump(data, file, indent = 4)

                self.set_cookie(username) # sets the cookie to the users username
                
                with open("web/html/redirect.html", "r") as file:
                    self.wfile.write(file.read().replace("url", "/signupqs").encode()) 

            case "/signup": # loads the signup pages html
                self.set_response()
                with open("web/html/signup.html", "r") as file:
                    signup_page = file.read()                        
                    self.wfile.write(signup_page.encode())

            case "/signupqs": # loads the signup question html
                self.set_response()
                with open("web/html/signupquestions.html", "r") as file:
                    signup_page = file.read()                        
                    self.wfile.write(signup_page.encode())

            case "/new-home":
                self.set_response()
                with open("web/html/new-home.html", "r") as file:
                    signup_page = file.read()                        
                    self.wfile.write(signup_page.encode())

            case "/":
                self.set_response()

                user = self.get_username()
                cookie = self.get_cookie()
                if "user" not in cookie: # checks the users cookie
                    self.redirect("/signin") # if they dont have a cookie takes them to the signin page
                    return
                if not python.Api.check(user): # checks if the user has authorized starva
                    self.redirect("https://www.strava.com/oauth/authorize?client_id=112868&redirect_uri=http%3A%2F%2Flocalhost:8080/oauth&response_type=code&scope=activity%3Aread_all,activity%3Awrite")
                    return
                if not os.path.exists(f"user_data/{user}.json"): # checks if the users answered the sign up questions
                    self.redirect("/signupquestions")
                    return
                date = self.get_current_date()   

                with open("web/html/home.html", "r") as home_file:
                    with open(f"perm_nutrition_log/{user}.json", "r") as perm_nutrition_data_file:
                        perm_nutrition_log = json.load(perm_nutrition_data_file)

                    with open(f"user_data/{user}.json", "r") as user_data_file:
                        user_data = json.load(user_data_file)         

                    now = datetime.datetime.now()
                    startofmonth = datetime.date(now.year, now.month, 1)
                    try:
                        month_activitys = python.Api.get_user_activites(user, param = {'per_page': 200, 'page': 1, 'after': startofmonth.strftime('%s')})
                    except ValueError as e:
                        print(f"Windows Erro: {e}")
                        month_activitys = []
                        
                    # sets a defult veriable for recent_activity
                    recent_activity = {'resource_state': 2, 'athlete': {'id': 0, 'resource_state': 1}, 'name': 'n/a', 'distance': 0, 'moving_time': 0, 'elapsed_time': 0, 'total_elevation_gain': 0, 'type': 'Run', 'sport_type': 'Run', 'workout_type': 0, 'id': 0, 'start_date': '2023-11-02T07:19:42Z', 'start_date_local': '2023-11-02T18:19:42Z', 'timezone': '(GMT+10:00) Australia/Hobart', 'utc_offset': 39600.0, 'location_city': None, 'location_state': None, 'location_country': None, 'achievement_count': 0, 'kudos_count': 3, 'comment_count': 0, 'athlete_count': 1, 'photo_count': 0, 'map': {'id': 'a10151679572', 'summary_polyline': '', 'resource_state': 2}, 'trainer': False, 'commute': False, 'manual': True, 'private': False, 'visibility': 'everyone', 'flagged': False, 'gear_id': 'g15342740', 'start_latlng': [], 'end_latlng': [], 'average_speed': 3.342, 'max_speed': 0, 'has_heartrate': False, 'heartrate_opt_out': False, 'display_hide_heartrate_option': False, 'upload_id': None, 'external_id': None, 'from_accepted_tag': False, 'pr_count': 0, 'total_photo_count': 0, 'has_kudoed': False}

                    #NOTE ITS EPIC ITS lambda: checks if `activity` has a map and summary_polyline
                    check_map = lambda activity: "map" in activity and "summary_polyline" in activity['map'] and activity['map']['summary_polyline']

                    # keeps going back intill it find an activite with a summary polyline
                    emptym = 0
                    while now.month - emptym >= 2:
                        i = -1
                        while -i <= len(month_activitys) and not check_map(month_activitys[i]):
                            i -= 1
                        if -i > len(month_activitys):
                            emptym += 1
                            startofmonthnext = startofmonth
                            startofmonth = datetime.date(now.year, now.month-emptym, 1)
                            try:
                                month_activitys = python.Api.get_user_activites(user, param = {'per_page': 200, 'page': 1, 'after': startofmonth.strftime('%s'), 'before': startofmonthnext.strftime('%s')})
                            except ValueError as e:
                                print(f"Windows Erro: {e}")
                                month_activitys = []
                        else:
                            recent_activity = month_activitys[i]
                            break              

                    cords = []
                    most_north = most_south = most_east = most_west = size = 0
                    
                    if check_map(recent_activity): # checks if the users recnet activity has a map
                        cords = decode_polyline(recent_activity['map']['summary_polyline'])
                        most_north, most_south, most_east, most_west, size = self.map_bounds(cords)
    
                    if "nutrition_log" in perm_nutrition_log and "goal_cals" in user_data: # checks if user has logged any food
                        if date in perm_nutrition_log["nutrition_log"]:
                            total_calories = perm_nutrition_log["nutrition_log"][date]["totals"]["total_calories"]
                            goal_cals = user_data["goal_cals"]
                            calories_remaining = int(float(goal_cals)) - int(float(total_calories))
                            
                            if goal_cals == 0: # checks if the goals is 0
                                calories_percent_eaten = "0"
                            else:
                                calories_percent_eaten = int(round(int(float(total_calories)) / int(goal_cals) * 100))
                        
                            # sets a bunch of veriables
                            total_carbs = float(perm_nutrition_log["nutrition_log"][date]["totals"]["total_carbs"])
                            total_protein = float(perm_nutrition_log["nutrition_log"][date]["totals"]["total_protein"])
                            total_fat = float(perm_nutrition_log["nutrition_log"][date]["totals"]["total_fat"])
                            total_calories = float(perm_nutrition_log["nutrition_log"][date]["totals"]["total_calories"])

                            carbs_calories_percent = int((total_carbs * 4)/total_calories * 100) 
                            protein_calories_percent = int((total_protein * 4)/total_calories * 100)
                            fat_calories_percent = int((total_fat * 9)/total_calories * 100)
                            
                            # ues the veriable set to great a piechart and saves it the users generated images file
                            generate_pie_chart([carbs_calories_percent, protein_calories_percent, fat_calories_percent], ["Carbohydrates", "Protein", "Fat"], self.get_pie_colours(carbs_calories_percent, protein_calories_percent, fat_calories_percent),  f"pie_chart_{date}.png", user)
                        else: # if the havent loged any food
                            total_calories = "N/A"
                            goal_cals = "N/A"
                            calories_percent_eaten = "N/A"
                            calories_remaining = "N/A"
                    else:
                        total_calories = "N/A"
                        goal_cals = "N/A"
                        calories_percent_eaten = "N/A"
                        calories_remaining = "N/A"


                    calories_content_body = f"{str(total_calories)}/{str(goal_cals)}<br>({str(calories_percent_eaten)}% of goal)<br>{str(calories_remaining)} calories remaining"
                    
                    if os.path.exists(f"web/images/generated/user_charts/{user}/pie_chart_{date}.png"): # checks if the userr has a generated image
                        macros_content_body = f'<img src="images/generated/user_charts/{user}/pie_chart_{date}.png" style="width:50%;" class="centre">'
                    else:
                        macros_content_body = 'No food logged today'

                    formatted_time = time.strftime('%H:%M:%S', time.gmtime(recent_activity["moving_time"]))
                   
                    input_datetime = datetime.datetime.strptime(recent_activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ")
                    formatted_date = input_datetime.strftime("%a, %d/%m/%Y")  

                    month_day, month_length = calendar.monthrange(startofmonth.year, startofmonth.month)
                    day_data = [[0, 0] for _ in range(month_length)]
               
                    month_distance = 0
                    month_time = 0
                    for activity in month_activitys: # goes throught the last month activites and add there time and distance together
                        month_distance += activity['distance']
                        month_time += activity['moving_time'] 

                        start_time = datetime.datetime.strptime(activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ")
                        day = start_time.day-1
                        
                        day_data[day][0] += activity['distance']
                        day_data[day][1] += activity['moving_time']

                    home_page = (home_file.read() # replace info on the home page with the corect data
                        .replace("calories_content", calories_content_body)
                        .replace("macros_content", macros_content_body)
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

                        .replace("template_month_day", str(month_day))
                        .replace("template_month_data", str(day_data))
                        .replace("template_profile_img", python.Api.athelete_profile_img(user))
                    )
                    self.wfile.write(home_page.encode())

            case "/logexercise":
                self.set_response()
                user = self.get_username()
                with open("web/html/logexercise.html", "r") as file:
                    logexercise_page = file.read()
                    logexercise_page = logexercise_page.replace("template_profile_img", python.Api.athelete_profile_img(user))
                    self.wfile.write(logexercise_page.encode())

                value = self.query()             
                date = value['workout-date'].split("-")
                times = value['workout-time'].split("%3A")
                workout_time = (int(value['workout-hrs'] or "0")*3600) + (int(value['workout-mins'] or "0")*60) + int(value['workout-secs'] or "0") 
                timestamp = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(times[0]), int(times[1]))
                
                # the comment section code for the upload activites section
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
                self.set_response()
                user = self.get_username()

                with open("web/html/myprofile.html", "r") as file: # loads the html for the home page
                    myprofile_page = file.read()
                    myprofile_page = myprofile_page.replace("name-temp", user.replace("%40", "@"))

                    with open(f"user_data/{user}.json", "r") as user_data_file:
                        user_data_pro = json.load(user_data_file)

                    birth_day = str(user_data_pro['dob']).split('-')
                    today = str(datetime.datetime.today()).split(' ')[0].split("-")
                    age = int(today[0])-int(birth_day[0])
                    myprofile_page = myprofile_page.replace("age-temp", str(age))

                    myprofile_page = (myprofile_page.replace("gender-temp", user_data_pro['sex'])
                        .replace("muscle-goals-temp", user_data_pro['muscle_goals'])
                        .replace("cardio-temp", user_data_pro['cardio'])
                    )
                    if user_data_pro['fav_cardio']:
                        for type in user_data_pro['fav_cardio']:
                            if user_data_pro['fav_cardio']['other'] != '':
                                type = user_data_pro['fav_cardio']['other']
                                myprofile_page = myprofile_page.replace("fav-sport-temp", type)
                            elif user_data_pro['fav_cardio'][type] == True:
                                myprofile_page = myprofile_page.replace("fav-sport-temp", type)
                    else:
                        myprofile_page = myprofile_page.replace("fav-sport-temp", "N/A")
                    myprofile_page = (myprofile_page.replace("lvl-temp", user_data_pro['level'])
                        .replace("weight-goal-temp", user_data_pro['weight_goal'])
                        .replace("weight-units-temp", user_data_pro['weight-units'])
                        .replace("weight-temp", user_data_pro['weight'])
                        .replace("height-units-temp", user_data_pro['height-units'])
                        .replace("height-temp", user_data_pro['height'])
                        .replace("dob-temp", user_data_pro['dob'])
                        .replace("template_profile_img", python.Api.athelete_profile_img(user))
                    )
                    
                    days = [] # organises the training days output
                    for day in user_data_pro['training_days']:
                        if user_data_pro['training_days'][day] == True:
                            days.append(day)
                    days = (str(days).replace("'", "")
                        .replace("[", "")
                        .replace("]", "")
                    )
                    myprofile_page = (myprofile_page.replace("training-days-temp", days)
                        .replace("dob-temp", user_data_pro['dob'])
                        .replace("rhr-temp", user_data_pro['rhr'])
                    )
                    equipment = [] # put all the equipment the user loged into a list
                    for key,value in user_data_pro['equipment'].items():
                        if value:
                            equipment.append(key)
                    myprofile_page = myprofile_page.replace("equipment-temp", "<br><br>".join(equipment)) # replace equipment-temp with the list created

                    if python.Api.check(user): # checks if the user has the strava info  
                        myprofile_page = myprofile_page.replace("Strava Api: False", "Strava Api: True")                
                    
                    self.wfile.write(myprofile_page.encode())

            case "/activity":
                self.set_response()
                user = self.get_username()
                with open("web/html/html-template/individual_activitie.html", "r") as file:
                    id = int(self.query()["id"])
                    activity = python.Api.get_user_activity(user, id)
                    activity_page = file.read()
                    try:
                        description = activity["description"].replace("{", "") 
                        description = description.replace("}", "")
                    except AttributeError:
                        description = "N/A"
                    activity_page = (activity_page.replace("template_name", str(activity["name"]))
                        .replace("template_distance", str(round(int(activity["distance"])/1000, 2)))
                        .replace("template_moving_time", str(round(int(activity["moving_time"])/60, 2)))
                        .replace("template_elapsed_time", str(round(int(activity["elapsed_time"])/60, 2)))
                        .replace("template_total_elevation_gain", str(activity["total_elevation_gain"]))
                        .replace("template_type", str(activity["type"]))
                        .replace("template_sport_type", str(activity["sport_type"]))
                        .replace("template_start_date", str(activity["start_date"]).split("T")[0])
                        .replace("template_kudos_count", str(activity["kudos_count"]))
                        .replace("template_achievement_count", str(activity["achievement_count"]))
                        .replace("template_comment_count", str(activity["comment_count"]))
                        .replace("template_achievement_count", str(activity["achievement_count"]))
                        .replace("template_athlete_count", str(activity["athlete_count"]))
                        .replace("template_trainer", str(activity["trainer"]))
                        .replace("template_commute", str(activity["commute"]))
                        .replace("template_private", str(activity["private"]))
                        .replace("template_visibility", str(activity["visibility"].replace("_", " ")))
                        .replace("template_average_speed", str(round((activity["average_speed"]*3.6))))
                        .replace("template_max_speed", str(round((activity["max_speed"]*3.6))))
                        .replace("template_description", description.replace("ZAMO_DATA", "")))
                    try:
                        activity_page = (activity_page.replace("template_elev_high", str(activity["elev_high"]))
                            .replace("template_elev_low", str(activity["elev_low"])))
                    except:
                        activity_page = (activity_page.replace("template_elev_high", str(0))
                            .replace("template_elev_low", str(0)))
                    self.wfile.write(activity_page.encode())

            case "/signupquestions": # loads the sign up questions
                self.set_response()
                with open("web/html/signupquestions.html", "r") as file:
                    signupquestions_page = file.read()
                    self.wfile.write(signupquestions_page.encode())

            case "/signupquestions_action":
                user = self.get_username() # get the user username
                with open(f"user_data/{user}.json", "w") as file:
                    value = self.query()
                    goal_cals = calculate_goal_cals(calculate_eer(calculateAge(value["date_of_birth"]), imperial_to_metric_weight(int(value["weight"]), value["weight-units"]), imperial_to_metric_height(int(value["height"]), value["height-units"]), value["sex"], get_pal(str(value["pal"]))), value["weight_goal"])
                    json.dump( # dumps all the info collected from the signup questions into a new file for each user
                    {
                        "pal":str(get_pal(value["pal"])),
                        "muscle_goals":value["muscle_goals"],
                        "cardio":value["cardio"],
                        "fav_cardio": {
                            "running": "fav_cardio_running" == value["fav_cardio"],
                            "cycling": "fav_cardio_cycling" == value["fav_cardio"],
                            "swimming": "fav_cardio_swimming" == value["fav_cardio"],
                            "other": (value["other"].replace("+", " ") if "fav_cardio_other_box" == value["fav_cardio"] else ""),
                        } if "fav_cardio" in value else None,
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

                    }, file, indent = 4 # formates the user json file
                )
                    
                user_file = f"{user}.json"

                if not os.path.exists(f"program/{user_file}"): # checks if the user has a program file
                    with open(f"program/{user_file}", "w") as file:
                        json.dump({}, file)
                
                if not os.path.exists(f"temp_nutrition_log/{user_file}"): # checks if the user has a temp nutrition file
                    with open(f"temp_nutrition_log/{user_file}", "w") as file:
                        json.dump({}, file)
                
                if not os.path.exists(f"perm_nutrition_log/{user_file}"): # checks if the user has a perm nutrition file
                    with open(f"perm_nutrition_log/{user_file}", "w") as file:
                        json.dump({}, file)

                if not os.path.exists(f"web/images/generated/user_charts/{user}"): # checks if the user has a generated image file
                    os.mkdir(f"web/images/generated/user_charts/{user}")
                    
                self.redirect("/")

            case _: # the defult case manily used for images
                self.send_response(200)
                file_type = self.path.split(".")[-1]
                self.send_header("Content-type", MIME_TYPES.get(file_type, f"image/{file_type}"))
                self.end_headers()
                with open("web"+self.path, "rb") as file:
                    file_data = file.read()                        
                    self.wfile.write(file_data)

if __name__ == "__main__": # checks if the file is being run localy  
    webServer = HTTPServer((hostName, serverPort), FittnessServer)
    print(f"Server started http://{hostName}:{serverPort}")
    try:
        webServer.serve_forever(1)
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")


# TODO

# 1 - make a button that connects with strava in my profile

# 2 - 