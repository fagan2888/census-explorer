import requests
import json

res = requests.get("http://api.naics.us/v0/q?year=2012")
data = json.loads(res.text)

formatted = [{x["title"] : str(x["code"])} for x in data]

json.dump(formatted, open("output/naics.js", "w"))
