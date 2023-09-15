import requests

url = "https://dietagram.p.rapidapi.com/apiFood.php"

food_name = input("Enter food name: ")

food_possibilities_nutrition = []
food_possibilities_names = []

querystring = {"name":food_name,"lang":"en"}

headers = {
	"X-RapidAPI-Key": "27b7b42651msh6394f906c81a54cp13303ejsnb3e98812c5ff",
	"X-RapidAPI-Host": "dietagram.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
foods = response.json()["dishes"]

for food in foods:
    food_possibilities_nutrition.append(food)
    food_possibilities_names.append(food["name"].lower().strip("\n"))


while True:
    food_name2 = input("\nType food from above list: ").lower()

    if food_name2 not in food_possibilities_names:
        print("Invalid food")
    else:
        for food in food_possibilities_nutrition:
            if food["name"].lower().strip("\n") == food_name2:
                print(food)
                break
        break 