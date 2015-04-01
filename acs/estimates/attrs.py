import requests
import pandas as pd

occ_col = 'Occupation 2010 Description'

def clean(x):
    t = x.replace(" ", "").replace("-", "").replace(":", "").lower().replace(",", "")
    return t

attrs = pd.read_csv("data/CensusCrosswalk.csv", converters={occ_col: str, "Level 5": str, "Level 4":str,"Level 3":str, "Level 2":str})
attrs['clean_name'] = attrs[occ_col].apply(clean)


def lookup(name):
    cleaned = clean(name)
    res = attrs[attrs.clean_name == cleaned]
    if res.empty:
        res = attrs[attrs.clean_name == (cleaned + 's')]
    res = res.iloc[-1]
    return res[occ_col], res["Level 0"], res["Level 1"], res["Level 2"],res["Level 3"],res["Level 4"], res["Level 5"], res["clean_name"]

if __name__ == "__main__":
    print lookup('Protective service occupations:')

