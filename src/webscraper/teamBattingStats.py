from selenium import webdriver
from selenium.webdriver.common.by import By
import pprint
import json
from alive_progress import alive_bar

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
    "LAA",
    "LAD",
    "MIA",
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
    "TBR",
    "TEX",
    "TOR",
    "WSN"
]

team_stats = {} #quad-nested dictionary for storing four stats for every game for every year

#create empty nested dict to fill in later
for team in team_codes:
    years = team_stats.setdefault(team, {})
    for i in range(2024, 2025):
        years.setdefault(i, {})

#populating nested dict with values pulled from the website
for team in team_codes:
    print("Working on {}...".format(team))
    with alive_bar(1) as bar:
        for year in range(2024, 2025):
            url = "https://www.baseball-reference.com/teams/tgl.cgi?team={team}&t=b&year={year}".format(team = team, year = str(year))
            driver.get(url)
            table = driver.find_element(By.ID, "team_batting_gamelogs")
            datarows = table.find_elements(By.CSS_SELECTOR, '[id][data-row]')
            for row in datarows:
                team_stats[team][year][row.find_element(By.CSS_SELECTOR, '[data-stat="date_game"]').get_attribute("csk")[:10]] = {
                    "BA" : float(row.find_element(By.CSS_SELECTOR, '[data-stat="batting_avg"]').text),
                    "OBP" : float(row.find_element(By.CSS_SELECTOR, '[data-stat="onbase_perc"]').text),
                    "SLG" : float(row.find_element(By.CSS_SELECTOR, '[data-stat="slugging_perc"]').text),
                    "OPS" : float(row.find_element(By.CSS_SELECTOR, '[data-stat="onbase_plus_slugging"]').text)
                }
            bar()

pprint.pp(team_stats)

with open('data/pitcherstats24.json', 'w') as f:
    json.dump(team_stats, f)
    f.close()