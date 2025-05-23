
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
    return pal


# converts between imperical and metric. weight
def imperial_to_metric_weight(weight, weight_units): # convert to kg
    if weight_units == "lb":
        metric_weight = weight/2.205
    elif weight_units == "st":
        metric_weight = weight*6.35
    else:
        metric_weight = weight #kg
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
    return metric_height

    

# determines the user age based of there dob
def calculateAge(dob):
    current_date = datetime.now()

    dob = datetime.strptime(dob, '%Y-%m-%d')
    
    age = int(current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day)))
    return age 

# calculates the user eer using the age, weight, height, sex, pal
def calculate_eer(age, weight, height, sex, pal): # works with meters and kg
    bmi = weight/(height**2)

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
    return goal_cals

# calculates the users required water
def water_requirement(weight):
    water = 0.033 * weight
    return water