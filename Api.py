import requests, json, urllib3

client_id = "112868"
client_secret = "6357af21299074aba1ea779a5edac54131293873"
code = "edbe9c425bc0c0c19a5580502ff01553f429ad1d"

# res = requests.post(f"https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code")
# with open("respones.json", "w") as file:
#     json.dump(res.json(), file)


refresh_toekn = "003ec2f9a8d3bdc38a569989fda4a6ce595c4988"

res = requests.post(f"https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_toekn}&grant_type=refresh_token")
with open("respones.json", "w") as file:
    json.dump(res.json(), file)



# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# auth_url = "https://www.strava.com/oauth/token"
# activites_url = "https://www.strava.com/api/v3/athlete/activities"

# payload = {
#     'client_id': client_id,
#     'client_secret': client_secret,
#     'refresh_token': refresh_toekn,
#     'grant_type': "refresh_token",
#     'f': 'json'
# }

# print("Requesting Token...\n")
# res = requests.post(auth_url, data=payload, verify=False)
# access_token = res.json()['access_token']
# print("Access Token = {}\n".format(access_token))

# header = {'Authorization': 'Bearer ' + access_token}
# param = {'per_page': 200, 'page': 1}
# my_dataset = requests.get(activites_url, headers=header, params=param).json()

# with open("activite.json", "w") as file:
#     json.dump(my_dataset, file)
