
import json
import pandas as pd
import geopy
import glob
import time

geolocator = geopy.Nominatim(user_agent='my-geo-app')
def get_zipcode(lat_lon):
    location = geolocator.reverse((lat_lon))
    return location.raw['address']['postcode']

results = []
path = "full_search_pilates/*.json"
files = [f for f in glob.iglob(path)]
for f in files:
    with open(f, "r") as fi:
        r = fi.read()
    results = results + json.loads(r)['results']

print(f"len results = {len(results)}")

final_results = []

keys = [
    "name",
    'postcode',
    "postcode_prefix",
    'vicinity', 
    "business_status",
    'rating',
    'user_ratings_total',
    'types',
    'lat',
    'lng',
    ]

for result in results:
    result["lat"] = result["geometry"]["location"]["lat"] 
    result["lng"] = result["geometry"]["location"]["lng"]
    result["postcode"] = ""
    result["postcode_prefix"] = ""
    r = {k:v for k,v in result.items() if k in keys}
    final_results.append(r)

df = pd.DataFrame(final_results)
df = df.drop_duplicates(subset=["name", "lat", "lng"])
df = df[keys]
print(f"len results = {len(df)}")
for i in range(len(df)):
    try:
        postcode = get_zipcode((df.lat.iloc[i], df.lng.iloc[i]))
        df.postcode.iat[i] = postcode
        df.postcode_prefix.iat[i] = postcode[:5]
    except Exception as e:
        print(f"error: {e}")

df.to_excel("full_search_pilates.xlsx")

