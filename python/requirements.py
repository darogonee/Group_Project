
from datetime import date

def calculateAge(born):
    today = date.today()
    
    try:

        birthday = born.replace(year = today.year)
 
    except ValueError:
        birthday = born.replace(year = today.year,
                  month = born.month + 1, day = 1)
 
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year
         
# Driver code
listtt = []
listt = input().split("-")
for val in listt:
    listtt.append(int(val))
print(calculateAge(input(tuple(listtt))))


print(date(1997, 2, 3))

def calculate_eer(age, weight, height, sex, pal):
    bmi = weight/(height^2)
    if bmi < 25:
        if age < 18:
            if sex == "male":
                eer = 113.5 - 61.9*age + pal*(26.7 * weight + 903 * height)
            elif sex == "female":
                eer = 160.3 - 30.8*age  + pal*(10 * weight + 934 * height)
        elif age > 18:
            if sex == "male":
                eer = 661.8 - 9.53*age + pal*(15.91* weight + 539.6* height)
            elif sex == "female":
                eer = 354.1 - 6.91*age + pal*(9.36* weight + 726* height)
    elif bmi > 25:
        if age < 18:
            if sex == "male":
                eer = -114.1-50.9*age + pal * (19.5*weight + 1161.4*height)
            elif sex == "female":
                eer = 389.2 - 41.2*age + pal * (15 * weight  + 701.6 * height)
        elif age > 18:
            if sex == "male":
                eer = 1085.6 - 10.08*age  + pal*(13.7* weight + 416* height)
            elif sex == "female":
                eer = 447.6 - 7.95*age  + pal*(11.4* weight + 619* height)

    return eer
# there nothing checking if the value is exaclty the coresponding number
def calculate_goal_cals(eer, weight_goal):
    if weight_goal == "gain":
        goal_cals = eer + 500
    elif weight_goal == "maintain":
        goal_cals = eer
    elif weight_goal == "lose":
        goal_cals = eer - 500
    return goal_cals