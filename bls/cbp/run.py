import requests
import json
import os

api_key = os.environ.get('CENSUS_API_KEY') 
year = 2012
state = "39"

url = 'http://api.census.gov/data/{}/ewks?get=EMP,ESTAB,NAICS2012_TTL&in=state:{}&for=county:*&NAICS2012=*&key={}'
target = url.format(year, state, api_key)

print "hitting", target
response = requests.get(target)
data = json.loads( response.text )
headers = data[0]
results = data[1:]

def to_json(arr):
    res = { headers[idx] : val for idx,val in enumerate(arr) }
    res["geo"] = int( state.zfill(2) + res["county"].zfill(3) )
    del res["county"]
    res["EMP"] = int(res["EMP"])
    res["ESTAB"] = int(res["ESTAB"])
    return res

formatted_json = [ to_json(x) for x in results]

# group by county

json.dump(formatted_json, open("output/cbp_{}.json".format(state), "w"))
print "done"
