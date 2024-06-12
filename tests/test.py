import pickle
import json

with open("teamstats.pickle", "rb") as f:
    a = pickle.load(f)
    with open("teamstats.json", "w") as g:
        json.dump(a, g)
        g.close()
    f.close()