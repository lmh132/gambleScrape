import pandas as pd
import json
import datetime
import pprint
import collections

a = open("data/teamstats.json")
b = open("data/pitcherstats.json")

teamstats = json.load(a)
pitcherstats = json.load(b)

df = pd.DataFrame({
    "IP" : [],
    "avgSO" : [],
    "Pit" : [],
    "Str" : [],
    "BA" : [],
    "OBP" : [],
    "SLG" : [],
    "OPS" : [],
    "SO" : []
})

for pitcher in pitcherstats:
    for season in pitcherstats[pitcher]:
        games = pitcherstats[pitcher][season]
        games = collections.OrderedDict(sorted(games.items()))

        for i in range(len(games.keys())-1):
            game = pitcherstats[pitcher][season][list(games.keys())[i]]
            row = [game["IP"], 
                   game["avgSO"], 
                   game["Pit"], 
                   game["Str"], 
                   teamstats[game["Opp"]][season][list(games.keys())[i]]["BA"], 
                   teamstats[game["Opp"]][season][list(games.keys())[i]]["OBP"], 
                   teamstats[game["Opp"]][season][list(games.keys())[i]]["SLG"], 
                   teamstats[game["Opp"]][season][list(games.keys())[i]]["OPS"], 
                   pitcherstats[pitcher][season][list(games.keys())[i+1]]["SO"]]
            df.loc[-1] = row
            df.index += 1
            df = df.sort_index()

pprint.pp(df)