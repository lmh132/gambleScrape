from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')
url = webdriver.Chrome(options=options)
url.get("https://www.baseball-reference.com/leagues/MLB-standings.shtml")

bs = BeautifulSoup(url.page_source,"html5lib")

df = pd.DataFrame({
    "Tm" : [],
    "W" : [],
    "L" : [],
    ">.500" : [],
    ">.500" : [],
    "last10" : []
})

stat_names = {
    "Tm" : "team_ID",
    "W" : "W",
    "L" : "L",
    ">.500" : "record_vs_over_500",
    ">.500" : "record_vs_under_500",
    "last10" : "record_last_10"
}

table = bs.find("tbody")
entry = table.find("tr", attrs = {"data-row" : "0"})
print(entry)

for i in range(0, 30):
    entry = table.find("tr", attrs = {"data-row" : str(i)})
    for stat in stat_names.keys():
        val = entry.find("td", attrs = {"data-stat" : stat})
        print(val.getText())
