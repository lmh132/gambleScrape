from selenium import webdriver
from selenium.webdriver.common.by import By
import pprint
import pickle
from tenacity import retry
from alive_progress import alive_bar
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
}

url = 'https://api.prizepicks.com/projections'

r = requests.get(url, headers=headers)
df = r.json()


player_id = {}
id_lines = {}

for projection in df["data"]:
    if projection["type"] == "projection":
        temp_dict_1 = projection["attributes"]
        if temp_dict_1["stat_type"] == "Pitcher Strikeouts":
            temp_dict_2 = projection["relationships"]
            id_lines[temp_dict_2["new_player"]["data"]["id"]] = projection["attributes"]["line_score"]
for projection in df["included"]:
    if projection["type"] == "new_player":
        player_id[projection["attributes"]["name"]] = projection["id"]

print(player_id)
print(id_lines)