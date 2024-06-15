import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import json

f = open('/Users/kevin/Desktop/CS Projects/gambleScrape/data/pitcherstats.json')
f1 = open('/Users/kevin/Desktop/CS Projects/gambleScrape/data/teamstats.json')
data = json.load(f)
data1 = json.load(f1)

games = []

for pitcher in data.keys():
    for year in data[pitcher].keys():
        for date in data[pitcher][year].keys():
            pitcherstats = data[pitcher][year][date]
            opponent = pitcherstats["Opp"]
            opponentstats = data1[opponent][year][date]
            stats = {}
            stats["SO"] = pitcherstats["SO"]
            stats["IP"] = pitcherstats["IP"]
            stats["avgSO"] = pitcherstats["avgSO"]
            stats["Pit"] = pitcherstats["Pit"]
            stats["Str"] = pitcherstats["Str"]
            
            stats["BA"] = opponentstats["BA"]
            stats["OBP"] = opponentstats["OBP"]
            stats["SLG"] = opponentstats["SLG"]
            stats["OPS"] = opponentstats["OPS"]
            games.append(stats)

with open('/Users/kevin/Desktop/CS Projects/gambleScrape/data/gameStats.csv', 'w') as f:
    f.write(','.join(games[0].keys()))
    f.write('\n') 
    for row in games:
        f.write(','.join(str(x) for x in row.values()))
        f.write('\n')



df = pd.read_csv("/Users/kevin/Desktop/CS Projects/gambleScrape/data/gameStats.csv")
df.head()
X = df.assign(intercept = 1)
print(X)
y = df.pop("SO")
print(y)

model_no_indicators = sm.GLM(
    y,
    X[["Str", "avgSO", "BA", "OPS"]],
    offset=np.log(X["IP"] + 0.1),
    family=sm.families.Poisson(),
)
result_no_indicators = model_no_indicators.fit()
print(result_no_indicators.summary())

plt.plot(y, result_no_indicators.fittedvalues, 'o')
plt.plot(y, y, '--', label='y = x')
plt.ylabel("fitted value")
plt.xlabel("observed value")
plt.legend()
plt.show()