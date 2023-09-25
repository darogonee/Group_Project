import requests, json, os
from python.cache import cache

def check(user):
    return os.path.exists(f"users/{user}.json")

def load(user):
    if check(user):
        user_info = json.load(open(f"users/{user}.json"))
        refresh_token = user_info["refresh_token"]
        access_token = user_info["access_token"]
        return refresh_token, access_token
    raise FileNotFoundError(f"User '{user}' has no data file. Perhaps it was deleted?")

strava_api = json.load(open("data/strava_api.json"))
client_secret = strava_api["client_secret"]
client_id = strava_api["client_id"]

def get_access(client_id, client_secret, code):
    res = requests.post(
        f"https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code").json()
    return res["access_token"], res["refresh_token"]

def refresh_tokens(client_id, client_secret, refresh_token):
    try:
        res = requests.post(
            f"https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token").json()
        return res["access_token"], res["refresh_token"]
    except KeyError as e:
        print(res, refresh_token)
        return None

@cache(max_age=10*60)
def get_user_activites(user):
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    header = {'Authorization': 'Bearer ' +
              refresh_tokens(client_id, client_secret, load(user)[0])[0]}

    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(
        activites_url, headers = header, params = param).json()
    return my_dataset

def save(access_token, refresh_token, path):
    with open(path, "w") as file:
        json.dump(
            {
                "refresh_token": refresh_token,
                "access_token": access_token,
            },
            file, indent = 4
        )
def refresh(user):
    save(*refresh_tokens(client_id, client_secret, load(user)[0]), f"users/{user}.json")


# LOOK AT ME i work!
def upload(user:str, name:str, type:str, start_date_local:str, 
        elapsed_time:int, distance:float = 0, elevation:float = 0, 
        description:str = "", trainer:int = 0, commute:int = 0,
        percieved_exertion:int = 5, exercises = {}):

    ex_description = description + "\nZAMO_DATA\n" + json.dumps({
        "percieved_exertion": percieved_exertion,
        "exercises": exercises
    })
    return requests.post(f"https://www.strava.com/api/v3/activities", params= {
            "name": name, 
            "type": type, 
            "sport_type": type, 
            "start_date_local": start_date_local,
            "elapsed_time": elapsed_time ,
            "description": ex_description,
            "distance": distance, 
            "elevation": elevation,
            "trainer": trainer,
            "commute": commute,
        },
        headers = {"Authorization": "Bearer "  + refresh_tokens(client_id, client_secret, load(user)[0])[0]
    }) 