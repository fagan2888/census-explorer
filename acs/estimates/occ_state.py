import pandas as pd
import numpy as np
import attrs
import util

def compute_totals(frame):
    names = [x.replace("_male", "").replace("_female", "") for x in frame.columns if x not in ["name", "Total:", "Male:", "Female:"] and "_moe" not in x]
    uniq = set(names)
    for c in uniq:
        frame[c + "_total"] = frame[c+"_male"] + frame[c+"_female"]
        frame[c + "_moe_total"] = (frame[c+"_moe_male"] ** 2 + frame[c+"_moe_female"] ** 2) ** 0.5
    return frame

def generate(df, mode="state", show="num_emp"):
    df = compute_totals(df)
    df = df.stack().reset_index()
    df = df.rename(columns={"level_0": "geo", "level_1": "occ", 0: show})
    df = df[df.occ.str.endswith("_total")] # -- only look at totals

    df["kind"] = df.occ.str.extract('._(moe)_total$')
    df.loc[df.kind.isnull(), 'kind'] = 'value'

    df['soc'] = df.occ.str.replace('(_moe_total|_total)\s*$', '')    
    
    df[show] = df[show].astype(float)
    df.geo = df.geo.astype(str)
    df = pd.pivot_table(df, values=show, index=['geo', 'soc'], columns=['kind'])
    df = df.reset_index()

    df["name"], df["l0"], df["l1"], df["l2"], df["l3"], df["l4"], df["l5"], df["cleanname"] = zip(*df["soc"].map(attrs.lookup))

    # df.geo = df.geo.str.replace('05000US', '') #14000US39001
    df.geo = df.geo.str.replace('14000US', '')
    df.to_json("output/ohio_{}_{}.json".format(mode, show), orient="records")
    print df.head()
    return df


acs_release='acs2010_1yr'
state_df = util.get_dataframe(tables='B24020', geoids='040|04000US39',col_names=True, geo_names=True, include_moe=True,release=acs_release)
mydf=generate(state_df, mode="county", show="num_emp")
mydf = mydf.fillna('')

print mydf.head()
