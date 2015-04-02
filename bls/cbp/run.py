import requests
import json
import os

api_key = os.environ.get('CENSUS_API_KEY') 
year = 2012
state = "39"

#url = 'http://api.census.gov/data/{}/ewks?get=EMP,ESTAB,NAICS2012_TTL&in=state:{}&for=county:*&NAICS2012=*&key={}'
#target = url.format(year, state, api_key)
target='http://api.census.gov/data/2012/cbp?get=EMP,ESTAB,NAICS2012_TTL&for=county:*&in=state:39&NAICS2012=*'

print "hitting", target
response = requests.get(target)
data = json.loads( response.text )
headers = data[0]
results = data[1:]

# '''
# {'NAICS2012': '48-49', 'name': 'Transportation and Warehousing'}
# {'NAICS2012': '31-33', 'name': 'Manufacturing'}
# {'NAICS2012': '44-45', 'name': 'Retail Trade'}
# '''

def genL0(x):
    if int(x) in [48, 49]:
        return "48-49"
    elif int(x) in [44, 45]:
        return "44-45"
    elif int(x) in [31, 32, 33]:
        return "31-33"
    else:
        return x

def to_json(arr):
    res = { headers[idx] : val for idx,val in enumerate(arr) }
    res["geo"] = int( state.zfill(2) + res["county"].zfill(3) )
    del res["county"]
    res["EMP"] = int(res["EMP"])
    res["ESTAB"] = int(res["ESTAB"])
    naics = str(res["NAICS2012"])
    res["l0"] = genL0(naics[:2])
    res["l1"] = naics[:4]
    return res

formatted_json = [] # [ to_json(x) for x in results
for x in results:
    mycode =str(x[headers.index("NAICS2012")])
    if "-" in mycode:
        print mycode
    if mycode != '00':
        formatted_json.append(to_json(x))
# group by county

json.dump(formatted_json, open("output/cbp_{}.json".format(state), "w"))
print "done"
