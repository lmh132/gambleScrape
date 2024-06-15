import numpy as np
import json
import pickle
import pprint
from collections import OrderedDict
from sklearn.preprocessing import StandardScaler

a = open("data/teamstats.json")
b = open("data/pitcherstats2.json")

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
            oppstats.append(opponent)
            strikeouts.append(sos)



scaler1 = StandardScaler().fit(prevgames)
scaler2 = StandardScaler().fit(oppstats)

scaled_prevgamedata = scaler1.transform(prevgames)
scaled_oppdata = scaler2.transform(oppstats)

PREV = np.array(scaled_prevgamedata).reshape(-1, 3, 8)
OPP = np.array(scaled_oppdata)
SO = np.array(strikeouts)

with open("data/PREV.pkl", "wb") as f:
    pickle.dump(PREV, f)
    f.close()

with open("data/OPP.pkl", "wb") as f:
    pickle.dump(OPP, f)
    f.close()

with open("data/SO.pkl", "wb") as f:
    pickle.dump(SO, f)
    f.close()