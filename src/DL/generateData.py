import pandas as pd
import json
import pickle
import pprint
from collections import OrderedDict
from sklearn.preprocessing import StandardScaler

a = open("data/teamstats.json")
b = open("data/pitcherstats2.json")
scaler = StandardScaler()

teamstats = json.load(a)
pitcherstats = json.load(b)

prevgames = []
oppstats = []
strikeouts = []

window_size = 3

for pitcher in pitcherstats:
    for season in pitcherstats[pitcher]:
        pitchergames = OrderedDict(sorted(pitcherstats[pitcher][season].items()))
        pitcherkeys = list(pitchergames.keys())

        for i in range(len(pitcherkeys)-window_size-1):
            seq = []
            for j in range(window_size):
                game = pitchergames[pitcherkeys[i+j]]
                opp = teamstats[game["Opp"]][season][pitcherkeys[i+j]]
                seq.append([game["IP"],game["SO"], game["Pit"], game["Str"], opp["BA"], opp["OBP"], opp["SLG"], opp["OPS"]])
            
            foo = teamstats[pitchergames[pitcherkeys[i+window_size]]["Opp"]][season][pitcherkeys[i+window_size]]
            opponent = [foo["BA"], foo["OBP"], foo["SLG"], foo["OPS"]]
            sos = pitchergames[pitcherkeys[i+window_size]]["SO"]

            prevgames += seq
            oppstats += opponent
            strikeouts.append(sos)

pprint.pp(prevgames[:6])