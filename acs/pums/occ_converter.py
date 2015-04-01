import pandas as pd

occ0210 = pd.read_csv('data/recodes/occ02to10.csv', converters={"2002 OCCP": str, "2010 OCCP": str})
occ1012 = pd.read_csv('data/recodes/occ10to12.csv', converters={"2010 OCCP": str, "2012 OCCP": str})

COL_RATE = "Total Conversion Rate"
COL_02 = "2002 OCCP"
COL_10 = "2010 OCCP"
COL_12 = "2012 OCCP"

def occ_trans(df, occ_trans_df, on_col, value_col):
    df = pd.merge(df, occ_trans_df, on=on_col)
    df[value_col] = df[value_col] * df[COL_RATE]
    return df.drop([on_col, COL_RATE], axis=1)

def occ_02_to_10(df, value_col):
    return occ_trans(df, occ0210, COL_02, value_col)

def occ_10_to_12(df, value_col):
    return occ_trans(df, occ1012, COL_10, value_col)

def occ_02_to_12(df, val_col):
    df = occ_02_to_10(code, val_col)
    return occ_10_to_12(code_10, val_col)

if __name__ == '__main__':
    moi = pd.DataFrame({"x": [10], COL_02: "0130"})
    res = occ_02_to_10(moi, "x")
    print res
