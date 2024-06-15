import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("data/allData.csv")
df.head()

# url = "http://www.stat.columbia.edu/~gelman/arm/examples/police/frisk_with_noise.dat" 
# df = pd.read_csv(url, skiprows=6, delimiter=" ")
# print(df.head())
# print("-----------")

X = (df
    .groupby(['player', 'Date'])
    .sum()
    .reset_index()
    .pipe(pd.get_dummies, columns=['eth', 'precinct'])
    .assign(intercept=1)  # Adds a column called 'intercept' with all values equal to 1.
    .sort_values(by='stops')
    .reset_index(drop=True)
)
print(X)
print("-----------")

y = X.pop("stops")
print(y)

# model_no_indicators = sm.GLM(
#     y,
#     X["intercept"],
#     offset=np.log(X["past.arrests"]),
#     family=sm.families.Poisson(),
# )
# result_no_indicators = model_no_indicators.fit()
# print(result_no_indicators.summary())