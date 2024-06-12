import pickle
import pprint

with open("teamstats.pickle", "rb") as f:
    idk = pickle.load(f)
    pprint.pp(idk)