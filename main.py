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
    return zipcodes

ONE_KM_LAT = 0.009
ONE_KM_LON = 0.015

with open("keys.yaml", "r") as fi:
    api_key = yaml.load(fi)["key"]

RADIUS = 1500
LOCATION = "51.47664479722215, -0.1968614101732617"
#Pimlico - 60 Vauxhaul bridge
RADIUS = 2000
#LOCATION = "51.49074883981019, -0.1331301312074909"
LOCATION = "51.472648922681046, -0.1660479190757905" # Battersea 1
LOCATION = "51.4779990105888, -0.14852622778473215" # Battersea 2
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
#params = {"type": "physiotherapist", "radius": RADIUS, "location": LOCATION, "key": api_key, "keyword": "pilates"}
params = {"type": "physiotherapist", "radius": RADIUS, "location": LOCATION, "key": api_key}
params = {"type": "physiotherapist", "radius": RADIUS, "location": LOCATION, "key": api_key, "keyword": "pilates"}



next_page_token = "xoyo"
i = 0
text = ""
while next_page_token:
    i += 1
    response = requests.get(url=url, params=params)
    next_page_token = response.json().get("next_page_token", "")
    params = {"pagetoken": next_page_token, "key": api_key}
    text = response.text
    print(params)
    print(len(response.json()["results"]))
    print(next_page_token)
    time.sleep(3)
    with open(f"battersea2_pilates/{i}.json", "w+")as fi:
        fi.write(text)
