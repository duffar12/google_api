import requests
import yaml
import json
import time
import geopy
import pandas as pd



def get_postcode(df):
    def get_zipcode(df, geolocator, lat_field, lon_field):
        location = geolocator.reverse((df[lat_field], df[lon_field]))
        return location.raw['address']['postcode']

    geolocator = geopy.Nominatim(user_agent='my-geo-app')
    
    # Or just convert all these at the end in your last step
    zipcodes = df.apply(get_zipcode, axis=1, geolocator=geolocator, lat_field='lat', lon_field='lng')
    return zipcodes.iloc[0]

ONE_KM_LAT = 0.009
ONE_KM_LON = 0.015
with open("keys.yaml", "r") as fi:
    api_key = yaml.load(fi)["key"]

RADIUS = 1500
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"


cost = 0
LAT_TRAVERSED = 0
lat = 51.389998957821525
while LAT_TRAVERSED <= 18:
    lng = -0.3369715150190131
    LNG_TRAVERSED = 0
    while LNG_TRAVERSED <= 24:
        params = {"type": "physiotherapist", "radius": RADIUS, "location": f"{lat},{lng}", "key": api_key, "keyword": "pilates"}
        i = 0
        next_page_token = "xoyo"
        text = ""
        while next_page_token:
            cost += 0.17
            i += 1
            response = requests.get(url=url, params=params)
            next_page_token = response.json().get("next_page_token", "")
            params = {"pagetoken": next_page_token, "key": api_key}
            text = response.text
            num_results = len(response.json()["results"])
            print(f"writing full_search_pilates/{lat}_{lng}{i}.json - num_results = {num_results}")
            with open(f"full_search_pilates/{lat}_{lng}{i}.json", "w+")as fi:
                fi.write(text)
            time.sleep(3)
        lng += (ONE_KM_LON * 3)
        LNG_TRAVERSED += 3
        print(f"cost=${cost} LAT_TRAVERSED={LAT_TRAVERSED}, LNG_TRAVERSED={LNG_TRAVERSED} {lat},{lng}")
    lat += (ONE_KM_LAT * 3)
    LAT_TRAVERSED += 3
