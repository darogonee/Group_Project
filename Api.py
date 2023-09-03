import requests, json, os



# user data
def load():
    if os.path.exists("users/me.json"):
        global refresh_token, access_token
        user_info = json.load(open("users/me.json"))
        refresh_token = user_info["refresh_token"]
        access_token = user_info["access_token"]
load()

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
    print(res)
    return res["access_token"], res["refresh_token"]


def get_user_activites():
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    header = {'Authorization': 'Bearer ' +
              refresh_tokens(client_id, client_secret, refresh_token)[0]}
    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(
        activites_url, headers = header, params = param).json()

    with open("activite.json", "w") as file:
        json.dump(my_dataset, file)

    return my_dataset

def save(access_token, refresh_token, path):
    with open(path, "w") as file:
        json.dump(
            {
                "refresh_token": refresh_token,
                "access_token": access_token
            },
            file
        )