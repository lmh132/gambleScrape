from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
import time
import pprint

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

#team codes tp iterate through
team_codes = [
    "ARI", 
    "ATL",
    "BAL",
    "BOS",
    "CHC",
    "CHW",
    "CIN",
    "CLE",
    "COL",
    "DET",
    "HOU",
    "KCR",
    "ANA",
    "LAD",
    "MIL",
    "MIN",
    "NYM",
    "NYY",
    "OAK",
    "PHI",
    "PIT",
    "SDP",
    "SFG",
    "SEA",
    "STL",
    "TBD",
    "TEX",
    "TOR",
    "WSN"
]

team_stats = {} #quad-nested dictionary for storing four stats for every game for every year

#create empty nested dict to fill in later
for team in team_codes:
    years = team_stats.setdefault(team, {})
    for i in range(2019, 2024):
        years.setdefault(i, {})

#populating nested dict with values pulled from the website
for team in team_codes:
    print("Working on {}...".format(team))
    for year in range(2019, 2024):
        print(year)
        driver.get("https://www.baseball-reference.com/teams/tgl.cgi?team={team}&t=b&year={year}".format(team = team, year = str(year)))
        table = driver.find_element(By.ID, "team_batting_gamelogs")
        gtm = 1
        datarows = table.find_elements(By.CSS_SELECTOR, '[id~="team_batting"]')
        for row in datarows:
            team_stats[team][year] = {
                "BA" : row.find_element(By.CSS_SELECTOR, '[data-stat="batting_avg"]').text,
                "OBP" : row.find_element(By.CSS_SELECTOR, '[data-stat="onbase_perc"]').text,
                "SLG" : row.find_element(By.CSS_SELECTOR, '[data-stat="slugging_perc"]').text,
                "OPS" : row.find_element(By.CSS_SELECTOR, '[data-stat="onbase_plus_slugging"]').text
            }

pprint.pp(team_stats)

"""
out = pd.DataFrame({

})



base_url = "https://www.baseball-reference.com/"

for team in team_codes:
    for year in range(2014, 2024):
        driver.get(base_url + "teams/{team}/{year}.shtml".format(team = team, year = str(year)))
        table = driver.find_element(By.ID, "team_pitching")
        players = table.find_elements(By.CSS_SELECTOR, "[href]")
        for player in players:
            link = player.get_attribute("href")
            driver.get(base_url + link)
"""