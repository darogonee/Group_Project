# import random
import json
import random

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
            "Shoulders"
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
    if cardio == "cardio_true":
        cardio = True

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

    random.shuffle(training_days)

    assigned_workouts = {}
    for day in training_days[:cardio_days_count]:
        assigned_workouts[day] = "Cardio"

    for day in training_days[cardio_days_count:]:
        assigned_workouts[day] = "weights"
        weights_training_days.append(day)

    for key,value in program.items():
        if key in training_days:
            program[key] = assigned_workouts[key]
        else:
            program[key] = "Rest"


    muscle_groups = weight_programs[weights_days_count]
    exercise_list = []
    for muscle_group in muscle_groups:
        exercise_list.append(get_exercises(valid_exercises(level, equipment), "muscle_group", muscle_group))


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

def get_exercises(valid_exercises, filter_type, values):
    exercises = []
    for value in values:
        filtered_data = [item for item in valid_exercises if item.get(filter_type) == value]
        try:
            exercises.append(random.choice(filtered_data))
        except IndexError:
            exercises.append({'exercise_id': 129, 'muscle_group': 'Chest', 'exercise_name': 'Kneeling Push-Up', 'level': 'beginner', 'ulc': 'Upper', 'pp': 'Push', 'modality': 'FW', 'joint': 'M', 'equipment': ''})
    return exercises

