# import random
import json
import random

disallowed_exercises = []
weight_programs = {
    1: [
        [
            "Back",
            "Biceps",
            "Calves",
            "Chest",
            "Quadriceps",
            "Shoulders",
            "Triceps",
            "Hamstrings"
        ]
    ],
    2: [
        [
            "Back",
            "Biceps",
            "Chest",
            "Shoulders",
            "Triceps",
            "Chest" 
        ],
        [
            "Calves",
            "Quadriceps",
            "Hamstrings",
            "Quadriceps",
            "Hamstrings"
        ]
    ],
    3: [
        [
            "Chest",
            "Triceps",
            "Shoulders",
            "Chest",
            "Triceps",
            "Shoulders",

        ],
        [
            "Back",
            "Biceps",
            "Back",
            "Biceps",
            "Back",
            "Biceps"
        ],
        [
            "Calves",
            "Quadriceps",
            "Hamstrings",
            "Quadriceps",
            "Hamstrings"
        ]

    ],
    4: [
        [
            [
            "Back",
            "Biceps",
            "Chest",
            "Shoulders",
            "Triceps",
            "Chest" 
        ],
        [
            "Calves",
            "Quadriceps",
            "Hamstrings",
            "Quadriceps",
            "Hamstrings"
        ],
        [
            "Back",
            "Biceps",
            "Chest",
            "Shoulders",
            "Triceps",
            "Chest" 
        ],
        [
            "Calves",
            "Quadriceps",
            "Hamstrings",
            "Quadriceps",
            "Hamstrings"
        ]
        ]
    ], 5: [
        [
            "Back",
            "Biceps",
            "Chest",
            "Shoulders",
            "Triceps",
            "Chest" 
        ],
        [
            "Calves",
            "Quadriceps",
            "Hamstrings",
            "Quadriceps",
            "Hamstrings"
        ], 
        [
            "Chest",
            "Triceps",
            "Shoulders",
            "Chest",
            "Triceps",
            "Shoulders",

        ],
        [
            "Back",
            "Biceps",
            "Back",
            "Biceps",
            "Back",
            "Biceps"
        ],
        [
            "Calves",
            "Quadriceps",
            "Hamstrings",
            "Quadriceps",
            "Hamstrings"
        ]
    ], 6:[
        [
            "Chest",
            "Triceps",
            "Shoulders",
            "Chest",
            "Triceps",
            "Shoulders",

        ],
        [
            "Back",
            "Biceps",
            "Back",
            "Biceps",
            "Back",
            "Biceps"
        ],
        [
            "Calves",
            "Quadriceps",
            "Hamstrings",
            "Quadriceps",
            "Hamstrings"
        ],
        [
            "Chest",
            "Triceps",
            "Chest",
            "Triceps",
            "Chest",
            "Triceps",

        ],
        [
            "Back",
            "Biceps",
            "Shoulders",
            "Back",
            "Biceps",
            "Shoulders"
        ],
        [
            "Calves",
            "Quadriceps",
            "Hamstrings",
            "Quadriceps",
            "Hamstrings"
        ]
    ]
}

reps_sets = {"strength":["3-5", "2-6"], "hypertrophy":["3-4", "6-12"], "endurance":["2-3", "12-20"]}

get_levels = {"beginner":"beginner", "intermediate":["beginner", "intermediate"], "advanced":["beginner", "intermediate", "advanced"]}

def create_program(data):
    global disallowed_exercises
    program = {"monday":None, "tuesday":None, "wednesday":None, "thursday":None, "friday":None, "saturday":None, "sunday":None}
    cardio = False
    weights = False
    cardio_weights_split = False

    fitness_goals = []
    equipment = [""]
    weights_training_days = []
    training_days = []

    weights_days_count = 0
    cardio_days_count = 0
    training_days_count = 0 

    level = data["level"]

    # add fitness goals to fitness_goals
    muscle_goal = data["muscle_goals"]

    cardio = data["cardio"]

    # weights?
    if muscle_goal:
        weights = True

    # cardio?
    if cardio == "cardio_True":
        cardio = True
    elif cardio == "cardio_false":
        cardio = False

    # both?
    if cardio and weights:
        cardio_weights_split = True

    # add user equiopment to equipment list
    for key,value in data["equipment"].items():
        if value:
            equipment.append(key)

    # add traininng days
    for key, value in data["training_days"].items():
        if value:
            training_days.append(key)

    # rest day if all days ticked
    if len(training_days) > 6:
        rest_day = random.choice(training_days)
        training_days.remove(rest_day)

    training_days_count = len(training_days)

    #available days True and unavailable days False
    for day in program.keys():
        program[day] = day in training_days

    if cardio_weights_split:
        cardio_days_count = training_days_count // 2
        weights_days_count = training_days_count - cardio_days_count
    else:
        if weights:
            weights_days_count = training_days_count
        elif cardio:
            cardio_days_count = training_days_count

    random.shuffle(training_days)

    assigned_workouts = {}
    if cardio:
        for day in training_days[:cardio_days_count]:
            assigned_workouts[day] = "Cardio"

    for day in training_days[cardio_days_count:]:
        assigned_workouts[day] = "weights"
        weights_training_days.append(day)

    for key,value in program.items():
        print(str(key), str(value))
        if key in training_days:
            program[key] = assigned_workouts[key]
        else:
            program[key] = "Rest"


    program_template = weight_programs[weights_days_count]
    exercise_list = []
    for daily_program in program_template:
        exercise_list.append(get_exercises(valid_exercises(level, equipment), daily_program))


    for i in range(weights_days_count):
        program[weights_training_days[i]] = exercise_list[i]

    # if endurance, strength, and hypertrophy: 

    reps = reps_sets[muscle_goal][0]
    sets = reps_sets[muscle_goal][1]
    for day, exercises in program.items():
        if exercises != "Rest" and exercises != "Cardio":
            for exercise in exercises:
                exercise['reps'] = reps
                exercise['sets'] = sets
    return program

    


def valid_exercises(user_level, user_equipment):
    with open("data/exercises.json", "r") as file:
        exercise_data = json.load(file)

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

def get_exercises(valid_exercises, daily_program):
    exercises = []
    for muscle_group in daily_program:
        filtered_data = [item for item in valid_exercises if item.get("muscle_group") == muscle_group]

        if filtered_data:
            while True:
                exercise = random.choice(filtered_data)
                if exercise not in exercises:
                    exercises.append(exercise)
                    break

    if exercises == []:
        exercises == ""
        
    return exercises

# print(create_program(

# {
#     "pal": "1.85",
#     "muscle_goals": "hypertrophy",
#     "cardio": "cardio_false",
#     "fav-cardio": "Running",
#     "level": "beginner",
#     "weight_goal": "gain",
#     "weight-units": "kg",
#     "weight": "70",
#     "height-units": "cm",
#     "height": "178",
#     "dob": "2023-10-12",
#     "sex": "male",
#     "equipment": {
#         "bench": False,
#         "medicine-ball": False,
#         "cable-machine": False,
#         "torso-rotation-machine": False,
#         "ab-roller": False,
#         "dumbbell": False,
#         "barbell": False,
#         "assisted-pullup-machine": False,
#         "lat-pulldown-machine": False,
#         "pullup-bar": False,
#         "v-bar": False,
#         "machine-row": False,
#         "ez-bar": False,
#         "preacher-curl-machine": False,
#         "rope": False,
#         "leg-press-machine": False,
#         "smith-machine": False,
#         "calf-raise-machine":False,
#         "chest-press-machine": False,
#         "bench-press-machine": False,
#         "plates": False,
#         "dip-assist-machine": False,
#         "dip-machine": False
#     },
#     "training_days": {
#         "monday": True,
#         "tuesday": True,
#         "wednesday": True,
#         "thursday": True,
#         "friday": True,
#         "saturday": True,
#         "sunday": True
#     },
#     "rhr": "70",
#     "goal_cals": "7412",
#     "goal_water": "2.31"

# }

# ))
