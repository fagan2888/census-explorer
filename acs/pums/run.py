# coding: utf-8
import pandas as pd

attrs = pd.read_csv("data/occp12.csv", converters={"code":str})
attrs = attrs.set_index(["code"])

def occ_look(x):
    return attrs.ix[x].occname

df = pd.read_csv("data/ohio_2013_1yr_pums.csv")
df = df[["OCCP", "PUMA", "POWSP", "PWGTP"]]
# df["count"] = 1
df["value"] = df.PWGTP

df = df[df.POWSP == 39].copy()
df['geo'] = -9

df.loc[df['PUMA'] > 0, 'geo'] = df.PUMA
df.geo = "39" + df.geo.astype(str).str.zfill(5)
df['occ'] = df["OCCP"].astype(int).astype(str).str.zfill(4)

df = df.groupby(["geo", "occ"]).agg({"value": pd.Series.sum})
df = df.reset_index()
df['occ_name'] = df.occ.map(occ_look)

df.to_json("data/ohio_pums_data.json", orient="records")
