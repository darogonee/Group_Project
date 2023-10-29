data = {
    "nutrition_log": {
        "2023-10-29": {
            "food": [
                {
                    "name": "cake",
                    "quantity": "1",
                    "units": "serve",
                    "calories": "263.7",
                    "carbs": "38.3",
                    "fat": "11.8",
                    "protein": "2.0"
                },
                {
                    "name": "carrot",
                    "quantity": "2",
                    "units": "serve",
                    "calories": "31.2",
                    "carbs": "7.6",
                    "fat": "0.2",
                    "protein": "0.7"
                },
                {
                    "name": "cantaloupe",
                    "quantity": "3",
                    "units": "serve",
                    "calories": "166.5",
                    "carbs": "40.1",
                    "fat": "0.9",
                    "protein": "4.2"
                }
            ],
            "totals": {
                "total_calories": "461.4",
                "total_carbs": "86.0",
                "total_fat": "12.9",
                "total_protein": "6.9"
            },
            "data_transferred": "True"
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
            }
        }
    }
}

# Iterate through the dates and set "data_transferred" to "False"
for date_data in data["nutrition_log"].values():
    date_data["data_transferred"] = "False"

print(data)
