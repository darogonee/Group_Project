import requests, json, os
from functools import cache

def check(user):
    return os.path.exists(f"users/{user}.json")

def load(user):
    if check(user):
        user_info = json.load(open(f"users/{user}.json"))
        refresh_token = user_info["refresh_token"]
        access_token = user_info["access_token"]
        return refresh_token, access_token
    raise FileNotFoundError

strava_api = json.load(open("strava_api.json"))
client_secret = strava_api["client_secret"]
client_id = strava_api["client_id"]

def get_access(client_id, client_secret, code):
    res = requests.post(
        f"https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code").json()
    return res["access_token"], res["refresh_token"]

def refresh_tokens(client_id, client_secret, refresh_token):
    res = requests.post(
        f"https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token").json()
    return res["access_token"], res["refresh_token"]

# line 27 single handly more then triples the loading speed of the activites
@cache
def get_user_activites(user):
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    header = {'Authorization': 'Bearer ' +
              refresh_tokens(client_id, client_secret, load(user)[1])[0]}

    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(
        activites_url, headers = header, params = param).json()
    return my_dataset

def save(access_token, refresh_token, path):
    with open(path, "w") as file:
        json.dump(
            {
                "refresh_token": refresh_token,
                "access_token": access_token
            },
            file, indent = 4
        )
def refresh(user):
    save(*refresh_tokens(client_id, client_secret, load(user)[1]), f"users/{user}.json")