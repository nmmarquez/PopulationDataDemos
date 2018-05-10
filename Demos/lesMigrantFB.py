#! /usr/bin/env python3
"""FB Key demo."""
import requests
import datetime


def migrantLesvos(adsid, acstok, expat=False, recent=False, arabicOnly=False):
    """
    Estimate facebook sub-populations for Lesvos, Greece.

    The population of Lesvos, Greece that falls under a certain demographic
    umbrella is pulled from the facebook marketing api. The api can be
    interacted with manually at https://www.facebook.com/adsmanager/creation
    and the delivery estimate specification can be found by monitoring network
    calls.

    :param adsid: str, Facebook ads id, found on the link in description,
    :param acstok: str, Facebook ads access token
    :param expat: bool, Limit search to only expats.
    :param recent: bool, Limit search to only recently in th location.
    :param arabicOnly: bool, Limit search to Arabic speaking users only.
    """
    tspec = {
        "age_min": 18,
        "age_max": 65,
        "geo_locations": {
            # custom location for Lesvos
            "custom_locations": [{
                "name": "(39.1382, 26.5054)",
                "distance_unit": "kilometer",
                "latitude": 39.111615,
                "longitude": 26.501907,
                "primary_city_id": 871047,
                "radius": 16,
                "region_id": 4173,
                "country": "GR"}],
            # Get both recent and home count changes later if only want recent
            "location_types": ["home", "recent"]},
        "facebook_positions": ["feed"],
        "device_platforms": ["mobile", "desktop"],
        "publisher_platforms": ["facebook"]}
    if expat:
        # identifier for expats
        tspec["flexible_spec"] = [{
            "behaviors": [{"id": "6015559470583", "name": "Ex-pats (All)"}]}]
    if recent:
        tspec["geo_locations"]["location_types"] = ["recent"]
    if arabicOnly:
        # identifier for arabic speaking
        tspec["locales"] = [28]
    # convert the targeting spec to a string for use in the url api call
    tsrting = str(tspec).replace(' ', '').replace('\'', '"')
    call = (
        'https://graph.facebook.com/v3.0/act_' + adsid +
        '/delivery_estimate?access_token=' + acstok +
        '&optimization_goal=AD_RECALL_LIFT&targeting_spec=' + tsrting)
    response = requests.get(url=call)
    data = response.json()
    data["targeting_spec"] = tspec
    data["expat"] = expat
    data["recent"] = recent
    data["arabicOnly"] = arabicOnly
    data["time"] = str(datetime.datetime.utcnow()).split('.')[0]
    return data


if __name__ == '__main__':
    import os
    import json
    import itertools as it

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = dir_path + "/../data/lesvos.json"
    with open(dir_path + '/../keys/fbkey.json') as json_data:
        fbkeys = json.load(json_data)

    newresults = list()
    adsid = fbkeys['ads_id']
    acstok = fbkeys['access_token']
    for expat, recent, arabic in it.product((True, False), repeat=3):
        newresults.append(migrantLesvos(adsid, acstok, expat, recent, arabic))

    if not os.path.isfile(data_path):
        lesvosData = list()
        with open(data_path, 'w') as outfile:
            json.dump(lesvosData, outfile)

    with open(data_path) as json_data:
        lesvosData = json.load(json_data)

    lesvosData += newresults

    with open(data_path, 'w') as outfile:
        json.dump(lesvosData, outfile)
