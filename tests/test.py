import pickle
import json
import numpy as np

with open("data/traindatapickles/PROC.pkl", "rb") as f:
    data = pickle.load(f)
    print(data[0])
    f.close()