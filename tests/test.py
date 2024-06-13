import pickle
import json

a = open("data/teamstats.json")
data = json.load(a)

for i in range(0, len(data)):
    print(data[i])