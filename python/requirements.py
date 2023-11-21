
from datetime import datetime

# calculates the users pal
def get_pal(pal_reported: str):
    if pal_reported == "sedentary":
        pal = 1.45
    elif pal_reported == "minimally_active":
        pal = 1.65
    elif pal_reported == "moderately_active":
        pal = 1.85
    elif pal_reported == "very_active":
        pal = 2.25
    print(f"pal: {pal}")
    return pal


# converts between imperical and metric. weight
def imperial_to_metric_weight(weight, weight_units): # convert to kg
    if weight_units == "lb":
        metric_weight = weight/2.205
    elif weight_units == "st":
        metric_weight = weight*6.35
    else:
        metric_weight = weight

    print(f"weight: {metric_weight}")
    return metric_weight

# converts between imperical and metric. height
def imperial_to_metric_height(height, height_units): # convert to metres
    if height_units == "in":
        metric_height = (height*2.54)/100
    elif height_units == "ft":
        metric_height = (height*30.48)/100
    elif height_units == "cm":
        metric_height = height/100
    else:
        metric_height = height
    print(f"height: {metric_height})")
    return metric_height

    

# determines the user age based of there dob
def calculateAge(dob):
    current_date = datetime.now()

    dob = datetime.strptime(dob, '%Y-%m-%d')
    
    age = int(current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day)))
    print(f"age {age}")
    return age 

# calculates the user eer using the age, weight, height, sex, pal
def calculate_eer(age, weight, height, sex, pal): # works with meters and kg
    bmi = weight/(height**2)
    print(f"bmi: {bmi}")

    if bmi <= 25:
        if age < 18:
            if sex == "male":
                eer = 113.5 - (61.9*age) + pal*(26.7 * weight + 903 * height)
            elif sex == "female":
                eer = 160.3 - (30.8*age)  + pal*(10 * weight + 934 * height)
            else:
                eer = ((113.5 - (61.9*age) + pal*(26.7 * weight + 903 * height)) + (160.3 - (30.8*age)  + pal*(10 * weight + 934 * height)))/2
        else:
            if sex == "male":
                eer = 661.8 - 9.53*age + pal*(15.91* weight + 539.6* height)
            elif sex == "female":
                eer = 354.1 - 6.91*age + pal*(9.36* weight + 726* height)
            else:
                eer = ((661.8 - 9.53*age + pal*(15.91* weight + 539.6* height))+(354.1 - 6.91*age + pal*(9.36* weight + 726* height)))/2
    else:
        if age <= 18:
            if sex == "male":
                eer = -114.1-50.9*age + pal * (19.5*weight + 1161.4*height)
            elif sex == "female":
                eer = 389.2 - 41.2*age + pal * (15 * weight  + 701.6 * height)
            else:
                eer = ((-114.1-50.9*age + pal * (19.5*weight + 1161.4*height))+(389.2 - 41.2*age + pal * (15 * weight  + 701.6 * height)))/2

        else:
            if sex == "male":
                eer = 1085.6 - 10.08*age  + pal*(13.7* weight + 416* height)
            elif sex == "female":
                eer = 447.6 - 7.95*age  + pal*(11.4* weight + 619* height)
            else:
                eer = ((1085.6 - 10.08*age  + pal*(13.7* weight + 416* height))+(447.6 - 7.95*age  + pal*(11.4* weight + 619* height)))/2
    print(f"eer: {eer}")
    return eer

# calculates the users requirded cals
def calculate_goal_cals(eer, weight_goal):
    if weight_goal == "gain":
        goal_cals = eer + 500
    elif weight_goal == "lose":
        goal_cals = eer - 500
    else:
        goal_cals = eer

    goal_cals = round(goal_cals)
    print(f"goal cals: {goal_cals}")
    return goal_cals

# calculates the users required water
def water_requirement(weight):
    water = 0.033 * weight
    return water

# random_data = [
#     {"age": 25, "weight": 68.43, "height": 1.73, "sex": "male", "pal": 1.72},
#     {"age": 42, "weight": 56.89, "height": 1.66, "sex": "female", "pal": 1.84},
#     {"age": 31, "weight": 77.21, "height": 1.89, "sex": "intersex", "pal": 1.67},
#     {"age": 52, "weight": 91.12, "height": 1.58, "sex": "male", "pal": 1.53},
#     {"age": 36, "weight": 63.75, "height": 1.77, "sex": "female", "pal": 1.61},
#     {"age": 48, "weight": 74.02, "height": 1.62, "sex": "intersex", "pal": 1.75},
#     {"age": 22, "weight": 83.57, "height": 1.94, "sex": "male", "pal": 1.68},
#     {"age": 29, "weight": 50.38, "height": 1.81, "sex": "female", "pal": 1.57},
#     {"age": 39, "weight": 69.84, "height": 1.74, "sex": "intersex", "pal": 1}
# ]

# for user in random_data:
#     user_data = []
#     for key, value in user.items():
#         user_data.append(value)
#     print(calculate_eer(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4]))