import pickle
import json

with open("traindata.pkl", "rb") as f:
    data = pickle.load(f)
    print(data["prevgames"][0])
    f.close()