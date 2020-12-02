import pandas as pd

df = pd.read_csv('../data/stateDate.csv', header=0, delimiter=",")
df["submission_date"] = [(pd.to_datetime(x) -  pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
                         for x in df["submission_date"]]

df.to_csv("../data/stateDate.csv", index=False)