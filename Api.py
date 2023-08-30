# import requests

# activate_url = "https://www.strava.com/api/v3/athlete/activities"

# header = {'Authoriation': 'bearer' + "36d07eace45f649858cbbdbc6b00be92f3c88771"}
# param = {'per page': 200, 'page': 1}
# my_dataset = requests.get(activate_url, headers = header, params = param).json()


# print(my_dataset)


# import requests
# import json

# url="https://www.strava.com/api/v3/athlete/activities"

# api_key = "36d07eace45f649858cbbdbc6b00be92f3c88771"

# # city = input("which city -> ")
# repsone = requests.get(url+api_key).content
# # weather = json.loads(repsone)
# print(repsone)


import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "112868",
    'client_secret': '6357af21299074aba1ea779a5edac54131293873',
    'refresh_token': 'b8b94c28acd58d39f433bf3660c535d7f632f94d',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

print("Access Token = {}\n".format(access_token))
header = {'Authorization': 'Bearer ' + access_token}

# The first loop, request_page_number will be set to one, so it requests the first page. Increment this number after
# each request, so the next time we request the second page, then third, and so on...
request_page_num = 1
all_activities = []

while True:
    param = {'per_page': 200, 'page': request_page_num}
    # initial request, where we request the first page of activities
    my_dataset = requests.get(activites_url, headers=header, params=param).json()

    # check the response to make sure it is not empty. If it is empty, that means there is no more data left. So if you have
    # 1000 activities, on the 6th request, where we request page 6, there would be no more data left, so we will break out of the loop
    if len(my_dataset) == 0:
        print("breaking out of while loop because the response is zero, which means there must be no more activities")
        break

    # if the all_activities list is already populated, that means we want to add additional data to it via extend.
    if all_activities:
        print("all_activities is populated")
        all_activities.extend(my_dataset)

    # if the all_activities is empty, this is the first time adding data so we just set it equal to my_dataset
    else:
        print("all_activities is NOT populated")
        all_activities = my_dataset

    request_page_num += 1

print(len(all_activities))
for count, activity in enumerate(all_activities):
    print(activity["name"])
    print(count)