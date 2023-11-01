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
    program = {"monday":None, "tuesday":None, "wednesday":None, "thursday":None, "friday":None, "saturday":None, "sunday":None}
    cardio = False
    weights = False
    cardio_weights_split = False

    equipment = [""]
    weights_training_days = []
    training_days = []

    weights_days_count = 0
    cardio_days_count = 0
    training_days_count = 0 

    level = data["level"]

    muscle_goal = data["muscle_goals"]

    cardio = data["cardio"]
    fav_cardio_bool = data["fav_cardio"]
    fav_cardio = []

    # weights?
    if muscle_goal:
        weights = True

    # cardio?
    if cardio == "cardio_True":
        cardio = True
    elif cardio == "cardio_False":
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
        for cardio_type, val in fav_cardio_bool.items():
            if val == True:
                fav_cardio.append(cardio_type)
            elif isinstance(val, str):
                if val != "":
                    fav_cardio.append(val)
                    
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
        if exercises == "Cardio":
            random_cardio = random.choice(fav_cardio)
            program[day] = random_cardio.capitalize()

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
            for i in range(len(filtered_data)):
                exercise = random.choice(filtered_data)
                if exercise not in exercises:
                    exercises.append(exercise)
                    break

    if exercises == []:
        exercises == ""
        
    return exercises

if __name__ == "__main__":
    print(create_program({
    "pal": "1.85",
    "muscle_goals": "hypertrophy",
    "cardio": "cardio_True",
    "fav_cardio": {
        "running": True,
        "cycling": True,
        "swimming": False,
        "other": "Rock Climbing"
    },
    "level": "advanced",
    "weight_goal": "gain",
    "weight-units": "kg",
    "weight": "70",
    "height-units": "cm",
    "height": "177",
    "dob": "2007-10-27",
    "sex": "male",
    "equipment": {
        "bench": True,
        "medicine-ball": False,
        "cable-machine": False,
        "torso-rotation-machine": False,
        "ab-roller": False,
        "dumbbell": True,
        "barbell": True,
        "assisted-pullup-machine": False,
        "lat-pulldown-machine": False,
        "pullup-bar": False,
        "v-bar": False,
        "machine-row": False,
        "ez-bar": False,
        "preacher-curl-machine": False,
        "rope": False,
        "leg-press-machine": False,
        "smith-machine": False,
        "calf-raise-machine": False,
        "chest-press-machine": False,
        "bench-press-machine": False,
        "plates": False,
        "dip-assist-machine": False,
        "dip-machine": False
    },
    "training_days": {
        "monday": True,
        "tuesday": True,
        "wednesday": True,
        "thursday": True,
        "friday": True,
        "saturday": True,
        "sunday": True
    },
    "rhr": "69",
    "goal_cals": 298768,
    "goal_water": "2.31",
    "goal_carbs": 37346.0,
    "goal_fat": 9336.5,
    "goal_protein": 18673.0,
    "program": {
        "monday": [
            {
                "exercise_id": 47,
                "muscle_group": "Back",
                "exercise_name": "Bent-Over Barbell Row",
                "level": "beginner",
                "ulc": "Upper",
                "pp": "Pull",
                "modality": "FW",
                "joint": "M",
                "equipment": "barbell",
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 101,
                "muscle_group": "Biceps",
                "exercise_name": "Spider Curl",
                "level": "advanced",
                "ulc": "Upper",
                "pp": "Pull",
                "modality": "FW",
                "joint": "S",
                "equipment": [
                    "bench",
                    "barbell"
                ],
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 52,
                "muscle_group": "Back",
                "exercise_name": "Bent-Over Single-Arm Long Barbell Row",
                "level": "advanced",
                "ulc": "Upper",
                "pp": "Pull",
                "modality": "FW",
                "joint": "M",
                "equipment": "barbell",
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 86,
                "muscle_group": "Biceps",
                "exercise_name": "Preacher Barbell Curl",
                "level": "advanced",
                "ulc": "Upper",
                "pp": "Pull",
                "modality": "FW",
                "joint": "S",
                "equipment": [
                    "bench",
                    "barbell"
                ],
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 51,
                "muscle_group": "Back",
                "exercise_name": "Bent-Over Reverse-Grip Barbell Row",
                "level": "advanced",
                "ulc": "Upper",
                "pp": "Pull",
                "modality": "FW",
                "joint": "M",
                "equipment": "barbell",
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 98,
                "muscle_group": "Biceps",
                "exercise_name": "Single-Arm Barbell Curl",
                "level": "beginner",
                "ulc": "Upper",
                "pp": "Pull",
                "modality": "FW",
                "joint": "S",
                "equipment": "barbell",
                "reps": "3-4",
                "sets": "6-12"
            }
        ],
        "tuesday": "Cardio",
        "wednesday": [
            {
                "exercise_id": 137,
                "muscle_group": "Chest",
                "exercise_name": "Wide-Grip Push-Up",
                "level": "beginner",
                "ulc": "Upper",
                "pp": "Push",
                "modality": "FW",
                "joint": "M",
                "equipment": "",
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 234,
                "muscle_group": "Triceps",
                "exercise_name": "Forward Lean Dips",
                "level": "intermediate",
                "ulc": "Upper",
                "pp": "Push",
                "modality": "FW",
                "joint": "M",
                "equipment": "",
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 217,
                "muscle_group": "Shoulders",
                "exercise_name": "Barbell Front Raise",
                "level": "intermediate",
                "ulc": "Upper",
                "pp": "Push",
                "modality": "FW",
                "joint": "S",
                "equipment": "barbell",
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 113,
                "muscle_group": "Chest",
                "exercise_name": "Barbell bench Press",
                "level": "intermediate",
                "ulc": "Upper",
                "pp": "Push",
                "modality": "FW",
                "joint": "M",
                "equipment": [
                    "bench",
                    "barbell"
                ],
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 233,
                "muscle_group": "Triceps",
                "exercise_name": "Close-Grip bench Press",
                "level": "advanced",
                "ulc": "Upper",
                "pp": "Push",
                "modality": "FW",
                "joint": "M",
                "equipment": [
                    "bench",
                    "barbell"
                ],
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 208,
                "muscle_group": "Shoulders",
                "exercise_name": "Barbell Shoulder Press",
                "level": "advanced",
                "ulc": "Upper",
                "pp": "Push",
                "modality": "FW",
                "joint": "M",
                "equipment": "barbell",
                "reps": "3-4",
                "sets": "6-12"
            }
        ],
        "thursday": "Cardio",
        "friday": "Cardio",
        "saturday": [
            {
                "exercise_id": 102,
                "muscle_group": "Calves",
                "exercise_name": "Barbell Calf Raise",
                "level": "advanced",
                "ulc": "Lower",
                "pp": "Push",
                "modality": "FW",
                "joint": "S",
                "equipment": "barbell",
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 190,
                "muscle_group": "Quadriceps",
                "exercise_name": "Single-Leg Barbell Squat",
                "level": "advanced",
                "ulc": "Lower",
                "pp": "Push",
                "modality": "FW",
                "joint": "M",
                "equipment": "barbell",
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 151,
                "muscle_group": "Hamstrings",
                "exercise_name": "Elevated Single-Leg Hip Lift",
                "level": "advanced",
                "ulc": "Lower",
                "pp": "Pull",
                "modality": "FW",
                "joint": "M",
                "equipment": "",
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 163,
                "muscle_group": "Quadriceps",
                "exercise_name": "Barbell Reverse Lunge",
                "level": "intermediate",
                "ulc": "Lower",
                "pp": "Push",
                "modality": "FW",
                "joint": "M",
                "equipment": "barbell",
                "reps": "3-4",
                "sets": "6-12"
            },
            {
                "exercise_id": 152,
                "muscle_group": "Hamstrings",
                "exercise_name": "Hip Lift",
                "level": "beginner",
                "ulc": "Lower",
                "pp": "Pull",
                "modality": "FW",
                "joint": "M",
                "equipment": "",
                "reps": "3-4",
                "sets": "6-12"
            }
        ],
        "sunday": "Rest"
    },
    "nutrition_log": {
        "2023-10-29": {
            "food": [
                {
                    "name": "cake",
                    "quantity": "2",
                    "units": "serve",
                    "calories": "527.4",
                    "carbs": "76.6",
                    "fat": "23.6",
                    "protein": "4.0"
                },
                {
                    "name": "pumpkin",
                    "quantity": "1",
                    "units": "serve",
                    "calories": "50.2",
                    "carbs": "12.0",
                    "fat": "0.2",
                    "protein": "1.8"
                },
                {
                    "name": "apple",
                    "quantity": "2",
                    "units": "serve",
                    "calories": "192.7",
                    "carbs": "51.2",
                    "fat": "0.6",
                    "protein": "0.9"
                },
                {
                    "name": "burger",
                    "quantity": "3",
                    "units": "serve",
                    "calories": "1611.6",
                    "carbs": "122.8",
                    "fat": "78.3",
                    "protein": "103.2"
                },
                {
                    "name": "donut",
                    "quantity": "4",
                    "units": "serve",
                    "calories": "998.1",
                    "carbs": "112.8",
                    "fat": "53.5",
                    "protein": "14.7"
                }
            ],
            "totals": {
                "total_calories": "3380.0",
                "total_carbs": "375.4",
                "total_fat": "156.2",
                "total_protein": "124.6"
            },
            "data_transferred": "False"
        },
        "2023-10-28": {
            "food": [
                {
                    "name": "banana",
                    "quantity": "1",
                    "units": "serve",
                    "calories": "105.5",
                    "carbs": "27.4",
                    "fat": "0.4",
                    "protein": "1.3"
                },
                {
                    "name": "burger",
                    "quantity": "1",
                    "units": "serve",
                    "calories": "537.2",
                    "carbs": "40.9",
                    "fat": "26.1",
                    "protein": "34.4"
                },
                {
                    "name": "beetroot",
                    "quantity": "1",
                    "units": "serve",
                    "calories": "22.6",
                    "carbs": "5.0",
                    "fat": "0.1",
                    "protein": "0.8"
                }
            ],
            "totals": {
                "total_calories": "665.3",
                "total_carbs": "73.3",
                "total_fat": "26.6",
                "total_protein": "36.5"
            },
            "data_transferred": "False"
        }
    }
}))
