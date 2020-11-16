import pandas as pd

df = pd.read_csv('../data/COVID-19_Case_Surveillance_Public_Use_Data.csv', header=0, usecols=[6, 9], delimiter=",")

df["Race and ethnicity (combined)"].replace({"Hispanic/Latino":int(0),
                                             "American Indian/Alaska Native, Non-Hispanic":int(1),
                                             "Asian, Non-Hispanic":int(2),
                                             "Black, Non-Hispanic":int(3),
                                             "Native Hawaiian/Other Pacific Islander, Non-Hispanic":int(4),
                                             "White, Non-Hispanic":int(5),
                                             "Multiple/Other, Non-Hispanic":int(6),
                                             "Unknown":int(7)}, inplace=True)

df["death_yn"].replace({"No":0, "Yes":1, "Missing":2, "Unknown":3}, inplace=True)

# test = df["Race and ethnicity (combined)"].isnull().sum() is equal to 10
# test = df["death_yn"].isnull().sum() is equal to 0

df = df.dropna() #Drop rows that contain a nan value
df["Race and ethnicity (combined)"] = df["Race and ethnicity (combined)"].astype("int")

df.to_csv("../data/Covid_Race_Death_Numerical_Data.csv", index=False)