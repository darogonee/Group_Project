import requests
import json

# NOTE from: https://api-ninjas.com/api/nutrition
# function take to parameters and sends request to through api
def nutrition_calculator(number, units, food):
    api_url = f'https://api.api-ninjas.com/v1/nutrition?query={number} {units} {food}'
    response = requests.get(api_url, headers={'X-Api-Key': 'f+eHE4GyqdBw4+qAdCmEag==9wegAJ3ahmSJIHw4'})
    if response.status_code != requests.codes.ok:
        print("Error:", response.status_code, response.text)
        return response.status_code
    content = json.loads(response.text)[0]
    name =content["name"]
    calories = content["calories"]
    fat= content["fat_total_g"]
    protein = content["protein_g"] 
    carb = content["carbohydrates_total_g"]
    
    return {"name":name, "calories":calories, "fat":fat, "protein":protein, "carbs":carb}

if __name__ == "__main__":
    number = 1
    units = "oz"
    food = "apple"
    print(nutrition_calculator(number, units, food))