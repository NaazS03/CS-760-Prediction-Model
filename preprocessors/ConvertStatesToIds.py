import pandas as pd
import us #so we can process the US states easily

stateAbbrMapping = us.states.mapping('abbr','fips')

df = pd.read_csv('../data/stateDate.csv', header=0, delimiter=",")
df["state"] = [stateAbbrMapping[x] for x in df["state"]]
df.to_csv("../data/stateDate.csv", index=False)