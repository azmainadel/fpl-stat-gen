import requests
import json
import csv
import argparse
import logging
import sys
from tqdm import tqdm

# Replace with your own login email and password for FPL
LOGIN_EMAIL = 'FPL ID EMAIL' 
LOGIN_PASSWORD =  'ENTER PASSWORD FOR FIRST TIME USE'

FPL_URL = "https://fantasy.premierleague.com/api/"
LOGIN_URL = "https://users.premierleague.com/accounts/login/"
USER_SUMMARY_SUBURL = "element-summary/"
LEAGUE_CLASSIC_STANDING_SUBURL = "leagues-classic/"
LEAGUE_H2H_STANDING_SUBURL = "leagues-h2h/"
TEAM_ENTRY_SUBURL = "entry/"
PLAYERS_INFO_SUBURL = "bootstrap-static/"
PLAYERS_INFO_FILENAME = "2020-21/allPlayersInfo.json"

USER_SUMMARY_URL = FPL_URL + USER_SUMMARY_SUBURL
PLAYERS_INFO_URL = FPL_URL + PLAYERS_INFO_SUBURL
START_PAGE = 1

# POST login information and start request session
payload = {
    'login':LOGIN_EMAIL,
    'password':LOGIN_PASSWORD,
    'redirect_uri': 'https://fantasy.premierleague.com/',
    'app':'plfpl-web'
}
s = requests.session()
s.post(LOGIN_URL, data=payload)

# Download all player database in JSON file
def getPlayersInfo():
    r = s.get(PLAYERS_INFO_URL)
    jsonResponse = r.json()
    with open(PLAYERS_INFO_FILENAME, 'w') as outfile:
        json.dump(jsonResponse, outfile)


# Get users in a specific league using league id
def getUserEntryIds(league_id, ls_page, league_Standing_Url):
    entries = []

    while (True):
        league_url = league_Standing_Url + \
            str(league_id) + "/standings/" + \
            "?page_new_entries=1&page_standings=" + str(ls_page) + "&phase=1"

        logging.info(league_url)
        r = s.get(league_url)
        jsonResponse = r.json()
    
        managers = jsonResponse["standings"]["results"]
        if not managers:
            print("Total Managers : ", len(entries))
            break

        for player in managers:
            entries.append(player["entry"])
        ls_page += 1

    return entries


# Get the team in a GW for a specific manager using entry id
def getplayersPickedForEntryId(entry_id, GWNumber):

    eventSubUrl = "event/" + str(GWNumber) + "/picks/"
    playerTeamUrlForSpecificGW = FPL_URL + \
        TEAM_ENTRY_SUBURL + str(entry_id) + "/" + eventSubUrl

    r = s.get(playerTeamUrlForSpecificGW)
    jsonResponse = r.json()

    try:
        picks = jsonResponse["picks"]
    except:
        if jsonResponse["detail"]:
            print("entry_id "+str(entry_id) +
                  " doesn't have info for this gameweek")
        return None, None
    elements = []
    captainId = 1
    
    for pick in picks:
        elements.append(pick["element"])
        if pick["is_captain"]:
            captainId = pick["element"]

    return elements, captainId


# Read player info from JSON
def getAllPlayersDetailedJson():
    with open(PLAYERS_INFO_FILENAME) as json_data:
        d = json.load(json_data)
        return d


# Write info to CSV
def writeToFile(countOfplayersPicked, fileName):
    with io.open(fileName, "w", encoding="utf-8") as out:
        csv_out = csv.writer(out, delimiter=",")
        csv_out.writerow(['Name', 'Count'])

        for row in countOfplayersPicked:
            csv_out.writerow(row)


# Main method
parser = argparse.ArgumentParser(description='Get players picked in your league in a certain GameWeek')
parser.add_argument('-g', '--gameweek', help='gameweek number', required=True)
parser.add_argument('-t', '--type', help='league type')
parser.add_argument('-d', '--debug', help='deubg mode on')
args = vars(parser.parse_args())

if args['debug']:
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

getPlayersInfo()
playerElementIdToNameMap = {}
allPlayers = getAllPlayersDetailedJson()

for element in allPlayers["elements"]:
    playerElementIdToNameMap[element["id"]
                             ] = element["web_name"]  # .encode('ascii', 'ignore')

countOfplayersPicked = {}
countOfCaptainsPicked = {}
totalNumberOfPlayersCount = 0
pageCount = START_PAGE
GWNumber = args['gameweek']
leagueIdSelected = 33386 # League code for Noibeddo FPL

if args['type'] == "h2h":
    leagueStandingUrl = FPL_URL + LEAGUE_H2H_STANDING_SUBURL
    print("Leage mode: H2H")
else:
    leagueStandingUrl = FPL_URL + LEAGUE_CLASSIC_STANDING_SUBURL
    print("League mode: CLASSIC")

try:
    entries = getUserEntryIds(
        leagueIdSelected, pageCount, leagueStandingUrl)
except Exception as err:
    print("Error occured in getting entries/managers.")
    print(err)
    raise

print("Gameweek: "+str(GWNumber)+"\n")  

for entry in tqdm(entries):    
    try:
        elements, captainId = getplayersPickedForEntryId(entry, GWNumber)
    except Exception as err:
        print("Error occured in getting players and captain of the entry/manager")
        print(err)
        raise
    if not elements:
        continue
    for element in elements:
        name = str(playerElementIdToNameMap[element])
        if name in countOfplayersPicked:
            countOfplayersPicked[name] += 1
        else:
            countOfplayersPicked[name] = 1

    captainName = str(playerElementIdToNameMap[captainId])
    if captainName in countOfCaptainsPicked:
        countOfCaptainsPicked[captainName] += 1
    else:
        countOfCaptainsPicked[captainName] = 1

print("\n")

listOfcountOfplayersPicked = sorted(
    countOfplayersPicked.items(), key=lambda x: x[1], reverse=True)
writeToFile(listOfcountOfplayersPicked,
            "2020-21/GW"+str(GWNumber)+" Players " + "Noibeddo FPL" + ".csv")
listOfCountOfCaptainsPicked = sorted(
    countOfCaptainsPicked.items(), key=lambda x: x[1], reverse=True)
writeToFile(listOfCountOfCaptainsPicked,
            "2020-21/GW" + str(GWNumber)+" Captains " + "Noibeddo FPL" + ".csv")
