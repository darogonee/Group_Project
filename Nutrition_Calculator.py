import requests
def nutrition_calculator(food):
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(food)
    response = requests.get(api_url, headers={'X-Api-Key': 'f+eHE4GyqdBw4+qAdCmEag==9wegAJ3ahmSJIHw4'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
    return response


input('Type in quantity and food: ')