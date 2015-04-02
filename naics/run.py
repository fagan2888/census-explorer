import requests
import json

#res = requests.get("http://api.naics.us/v0/q?year=2012")
data = json.load(open("data/naics_2012.json"))

formatted = [{x["title"] : str(x["code"])} for x in data]
attrs = {}

for x in data:
    fullcode = str(x["code"])
    title = str(x["title"])
    attrs[fullcode] = {"name": title}

#json.dump(formatted, open("output/naics.js", "w"))
json.dump(attrs, open("output/attrs_naics.json", "w"))
