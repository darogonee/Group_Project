import random
import json

def create_program(data):
    program = {"monday":None, "tuesday":None, "wednesday":None, "thursday":None, "friday":None, "saturday":None}
    weight_programs = {1:"full-body", 2:"upper-lower", 3:"ppl", 4:"upper-lower-twice", 5:"ulppl", 6:"ppl-twice"}
    fitness_goals = []
    equipment = [""]
    training_days = []
    weights = False
    cardio = False
    level = data["level"]

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
        weights = True

    if "cardio" in fitness_goals:
        cardio = True

    #5-8 exercises each workout

    training_days_count = training_days.count()
    if training_days_count == 1:
        muscle_groups = ["Back", "Biceps", "Calves", "Chest", "Quadriceps", "Shoulders", "Triceps", "Hamstrings"]
        training_day = program[training_days[0]]
        muscle_groups.append(get_exercises(valid_exercises(level, equipment),"muscle_group", muscle_groups))
        training_days[training_day] = muscle_groups

    elif training_days_count == 2:
        muscle_groups1 = ["Back", "Biceps", "Chest", "Shoulders", "Triceps", "Chest"]
        muscle_groups2 = ["Calves", "Quadriceps", "Hamstrings", "Quadriceps", "Hamstrings"]

        training_day1 = program[training_days[0]]
        training_day2 = program[training_days[1]]





def valid_exercises(user_level, user_equipment):
    with open("data/exercises.json", "r") as file:
        exercise_data = json.load(file)

    get_levels = {"Beginner":"Beginner", "Intermediate":["Beginner", "Intermediate"], "Advanced":["Beginner", "Intermediate", "Advanced"]}
    level_filtered_data = []

    for level in get_levels[user_level]:
        level_filtered_data.extend([item for item in exercise_data if item.get("level") == level])

    equipment_filtered_data = []

    for item in exercise_data:
        equipment = item.get("equipment")
        
        if isinstance(equipment, list):
            equipment_count = 0
            for required_equipment in equipment:
                if required_equipment in user_equipment:
                    equipment_count = equipment_count + 1
            
            if equipment_count == len(equipment):
                equipment_filtered_data.append(item)

        elif isinstance(equipment, str):
            if equipment in user_equipment:
                equipment_filtered_data.append(item)

    return equipment_filtered_data

def get_exercises(valid_exercises, filter_type, values):
    exercises = []
    for value in values:
        filtered_data = [item for item in valid_exercises if item.get(filter_type) == value]
        try:
            exercises.append(random.choice(filtered_data))
        except IndexError:
            exercises.append(None)
    return exercises

print(get_exercises(valid_exercises("Advanced", ["bench", "", "dumbell"]),"muscle_group", ["Back", "Biceps", "Calves", "Chest", "Quadriceps", "Shoulders", "Triceps"]))
