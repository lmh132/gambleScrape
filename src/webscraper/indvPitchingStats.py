from selenium import webdriver
from selenium.webdriver.common.by import By
import pprint
import json
from alive_progress import alive_bar
from statistics import mean
import time

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

pitcher_stats = {}

class Queue:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.queue = []

    def full(self):
        return len(self.queue) == self.maxsize
    
    def empty(self):
        return len(self.queue) == 0

    def put(self, val):
        if self.full():
            self.queue.pop(0)
        self.queue.append(val)

    def mean(self):
        return mean(self.queue)

def get_playercode(url: str):
    foo = url.split("/")
    bar = foo[-1][:-6]
    return bar


starttime = time.time()
for team in team_codes:
    for year in range(2019, 2024):
        print("Gathering data for {team} in {year}".format(year = year, team = team))
        pitchers = []
        url = "https://www.baseball-reference.com/teams/{team}/{year}.shtml".format(team = team, year = year)
        driver.get(url)
        table = driver.find_element(By.ID, "team_pitching")
        data_rows = table.find_elements(By.CSS_SELECTOR, "[data-row]")
        for row in data_rows:
            if row.get_attribute("class") == "":
                try:
                    pos = row.find_element(By.CSS_SELECTOR, '[data-stat="pos"]').find_element(By.XPATH, "./strong").text
                    if pos == "SP":
                        pitchers.append(row.find_element(By.CSS_SELECTOR, '[data-stat="player"]').find_element(By.XPATH, "./a").get_attribute("href"))
                except:
                    continue
        for pitcher_url in pitchers:
            playercode = get_playercode(pitcher_url)
            print("Working on {}...".format(playercode))
            gamelog_url = "https://www.baseball-reference.com/players/gl.fcgi?id={playercode}&t=p&year={year}".format(playercode = playercode, year = year)
            driver.get(gamelog_url)
            table = driver.find_element(By.ID, "pitching_gamelogs")
            data_rows = table.find_elements(By.CSS_SELECTOR, '[id][data-row]')

            #queueIP = Queue(3)
            #queueSO = Queue(3)
            #queuePit = Queue(3)
            #queueStr = Queue(3)
            
            with alive_bar(len(data_rows)) as progbar:
                for row in data_rows:
                    date = row.find_element(By.CSS_SELECTOR, '[data-stat="date_game"]').get_attribute("csk")[:10]
                    innings_pitched = float(row.find_element(By.CSS_SELECTOR, '[data-stat="IP"]').text)
                    strikeouts = float(row.find_element(By.CSS_SELECTOR, '[data-stat="SO"]').text)
                    pitches = row.find_element(By.CSS_SELECTOR, '[data-stat="pitches"]').text
                    strikes = row.find_element(By.CSS_SELECTOR, '[data-stat="strikes_total"]').text

                    pitches = float(pitches) if pitches != "" else 80
                    strikes = float(strikes) if strikes != "" else 50

                    """
                    queueIP.put(innings_pitched)
                    queueSO.put(strikeouts)
                    if pitches == None:
                        if queuePit.empty():
                            queuePit.put(80)
                        else:
                            queuePit.put(queuePit.mean())
                    else:
                        queuePit.put(pitches)

                    if strikes == None:
                        if queueStr.empty():
                            queueStr.put(50)
                        else:
                            queueStr.put(queueStr.mean())
                    else:
                        queueStr.put(strikes)
                    """
                    foo = pitcher_stats.setdefault(playercode, {})
                    bar = foo.setdefault(year, {})
                    bar.setdefault(date, {})
                    
                    pitcher_stats[playercode][year][date] = {
                        "Opp" : row.find_element(By.CSS_SELECTOR, '[data-stat="opp_ID"]').find_element(By.XPATH, "./a").text,
                        "IP" : innings_pitched,
                        "SO" : strikeouts,
                        "Pit" : pitches,
                        "Str" : strikes
                    }
                    progbar()

with open('data/pitcherstats2.json', 'w') as f:
    json.dump(pitcher_stats, f)
    f.close()

print("Program finished in {} seconds".format(time.time() - starttime))