from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')
url = webdriver.Chrome(options=options)
url.get("https://www.baseball-reference.com/players/gl.fcgi?id=ohtansh01&t=b&year=2024")

bs = BeautifulSoup(url.page_source,"html5lib")

df = pd.DataFrame({
    "Rk" : [],
    "Gcar" : [],
    "Gtm" : [],
    "Date" : [],
    "Tm" : [],
    "HoA" : [],
    "Opp" : [],
    "Rslt" : [],
    "Inngs" : [],
    "PA" : [],
    "AB" : [],
    "R" : [],
    "H" : [],
    "2B" : [],
    "3B" : [],
    "HR" : [],
    "RBI" : [],
    "BB" : [],
    "IBB" : [],
    "SO" : [],
    "HBP" : [],
    "SH" : [],
    "SF" : [],
    "ROE" : [],
    "GDP" : [],
    "SB" : [],
    "CS" : [],
    "BA" : [],
    "OBP" : [],
    "SLG" : [],
    "OPS" : [],
    "BOP" : [],
    "aLI" : [],
    "WPA" : [],
    "acLI" : [],
    "cWPA" : [],
    "RE24" : [],
    "DFS(DK)" : [],
    "DFS(FD)" : [],
    "POS" : []
})

stat_names = {
    "Rk" : "ranker",
    "Gcar" : "career_game_num",
    "Gtm" : "team_game_num",
    "Date" : "date_game",
    "Tm" : "teamID",
    "HoA" : "team_homeORaway",
    "Opp" : "opp_ID",
    "Rslt" : "game_result",
    "Inngs" : "player_game_span",
    "PA" : "PA",
    "AB" : "AB",
    "R" : "R",
    "H" : "H",
    "2B" : "2B",
    "3B" : "3B",
    "HR" : "HR",
    "RBI" : "RBI",
    "BB" : "BB",
    "IBB" : "IBB",
    "SO" : "SO",
    "HBP" : "HBP",
    "SH" : "SH",
    "SF" : "SF",
    "ROE" : "ROE",
    "GDP" : "GIDP",
    "SB" : "SB",
    "CS" : "CS",
    "BA" : "",
    "OBP" : [],
    "SLG" : [],
    "OPS" : [],
    "BOP" : [],
    "aLI" : [],
    "WPA" : [],
    "acLI" : [],
    "cWPA" : [],
    "RE24" : [],
    "DFS(DK)" : [],
    "DFS(FD)" : [],
    "POS" : []
}

for i in range(702, 765):
    game_code = "batting_gamelogs.{}".format(i)
    gamelog = bs.find("tr", attrs = {"id" : game_code})
