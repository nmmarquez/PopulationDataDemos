"""FB Key demo."""
import json
import requests
import datetime
from facebook_business.adobjects.targetingsearch import TargetingSearch
from facebook_business.api import FacebookAdsApi

states = {
         'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
         'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
         'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
         'Maine' 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
         'Mississippi',  'Missouri', 'Montana', 'Nebraska', 'Nevada',
         'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
         'North Carolina', 'North Dakota', 'Ohio',
         'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
         'South  Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
         'Vermont', 'Virginia', 'Washington', 'West Virginia',
         'Wisconsin', 'Wyoming'
    }


def migrantMX2USA(state, age_min=13, age_max=65, gender=None):
    """
    Return the estimated number of migrants form Mexico to the United States.

    :param state: string, full name of a state, capital first letter.
    :param age_min: int, numeric minimum age to search but >= 13.
    :param age_max: int, numeric minimum age to search but <= 65.
    :param gender: string, either male or female or None for both.
    """
    assert state in states, "state must be a first letter capital valid state"
    stateKey = TargetingSearch.search({
        'q': state,
        'type': 'adgeolocation',
        'location_types': ['region']
    })
    stateKey = [x for x in stateKey if x["country_code"] == "US"]
    stateKey = stateKey[0]["key"]
    call = (
        "https://graph.facebook.com/v3.0/act_" + fbkeys['ads_id'] +
        "/delivery_estimate?access_token=" +
        fbkeys['access_token'] +
        "&optimization_goal=AD_RECALL_LIFT&targeting_spec=" +
        '{"flexible_spec":[{"behaviors":[{' +
        '"id":"6015559470583","name":"Ex-pats (Mexico)"}]}],' +
        '"geo_locations":{"regions":[{' +
        '"key":"' + stateKey + '",' +
        '"name":"' + state + '"' +
        '}]},"facebook_positions":["feed"],' +
        '"age_min":' + str(age_min) +
        ',"age_max":' + str(age_max) +
        ',"device_platforms":["mobile","desktop"],"locales":[28],' +
        '"publisher_platforms":["facebook"]'
        )
    if gender is None:
        call += '}'
    else:
        gassert = "gender param must be male or female."
        assert gender in ("male", "female"), gassert
        call += ',"genders":[' + str(1 if gender == "male" else 2) + "]}"
    response = requests.get(url=call)
    data = response.json()
    data["age_min"] = age_min
    data["age_max"] = age_max
    data["gender"] = gender
    data["state"] = state
    data["time"] = str(datetime.datetime.now()).split('.')[0]
    return data


if __name__ == '__main__':
    with open('../keys/fbkey.json') as json_data:
        fbkeys = json.load(json_data)

    FacebookAdsApi.init(
        fbkeys['app_id'],
        fbkeys['app_secret'],
        fbkeys['access_token'])
