import requests
import json
def nutrition_calculator(food):
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(food)
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

nutrition_calculator(input())