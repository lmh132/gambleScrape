import pickle
import json
import numpy as np

with open("data/traindatapickles/PREV.pkl", "rb") as f:
    data = pickle.load(f)
    print(data.shape[0])
    f.close()