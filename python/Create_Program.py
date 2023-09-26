import random
import json

def create_program(data):
    program = {"monday":None, "tuesday":None, "wednesday":None, "thursday":None, "friday":None, "saturday":None}
    weight_programs = {1:"full-body", 2:"upper-lower", 3:"ppl", 4:"upper-lower-twice", 5:"ulppl", 6:"ppl-twice"}
    fitness_goals = []
    equipment = []
    training_days = []
    weights = False
    cardio = False

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
        ...
    #full body: "Back - Latissimus Dorsi" OR "Back - Lat.Dorsi/Rhomboids", "Biceps", "Calves - Gastrocnemius", "Chest - Pectoralis", "Legs - Hamstrings", "Legs - Quadriceps", "Shoulders - Delts/Traps", "Triceps"

def valid_exercises(user_level, user_equipment):
    with open("data/exercises.json", "r") as file:
        exercise_data = json.load(file)

    level_filtered_data = [item for item in exercise_data if item.get("level") == user_level]
    equipment_filtered_data = []

    for item in exercise_data:
        equipment = item.get("equipment")
        
        if isinstance(equipment, list):
            # If equipment is a list, check if any of the user's equipment is in the list
            if any(e in user_equipment for e in equipment):
                equipment_filtered_data.append(item)
        elif isinstance(equipment, str):
            # If equipment is a string, check if it matches any of the user's equipment
            if equipment in user_equipment:
                equipment_filtered_data.append(item)

    return equipment_filtered_data

print(valid_exercises("Beginner", ["barbell", "n/a"]))