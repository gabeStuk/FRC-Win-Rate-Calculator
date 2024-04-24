import requests
import sys

baseUrl = 'http://www.thebluealliance.com/api/v3/'
header = {
    'X-TBA-Auth-Key': 'wGzJseZbdMKuFK9zflg15hCUMOz7ZMWDSeLgtGlhorVXLgxqeY2v6SXSAQeTeDVU'}


def getTBAData(url):
    return requests.get(baseUrl + url, headers=header).json()

if len(sys.argv) <= 2:
    team1 = input("Team 1 number: ")
    team2 = input("Team 2 number: ")
else:
    team1 = sys.argv[1]
    team2 = sys.argv[2]
team1JSON = getTBAData("team/frc" + team1)
team1Start = team1JSON['rookie_year']
team1Name = team1JSON['nickname']
team2JSON = getTBAData("team/frc" + team2)
team2Start = team2JSON['rookie_year']
team2Name = team2JSON['nickname']
currYear = getTBAData('status')['current_season']
startDate = 0
endDate = 0
played = True
if len(sys.argv) <= 4:
    if startDateIn := input("Start Date: "):
        startDate = int(startDateIn)
        if startDate == currYear:
            endDate = currYear
        else:
            if endDateIn := input("End Date: "):
                endDate = int(endDateIn)
            else:
                endDate = currYear
    else:
        startDate = max(team1Start, team2Start)
        endDate = currYear
else:
    if startDateIn := sys.argv[3]:
        startDate = int(startDateIn)
        if startDate == currYear:
            endDate = currYear
        else:
            if endDateIn := sys.argv[4]:
                endDate = int(endDateIn)
            else:
                endDate = currYear
    else:
        startDate = max(team1Start, team2Start)
        endDate = currYear


# get events
t1EventsJSON = getTBAData('team/frc' + team1 + '/events/simple')
t2EventsJSON = getTBAData('team/frc' + team2 + '/events/simple')
eventJSON = [x for x in t1EventsJSON if x in t2EventsJSON]

team1Wins = 0
team2Wins = 0
ties = 0

t1WinMatches = []
t2WinMatches = []
tieMatches = []

lastYear = 0

if eventJSON != []:
    print("\nEvents shared: ")

for event in eventJSON:
    year = event['year']
    if year < startDate or year > endDate:
        continue

    if year != lastYear:
        print(" - " + str(lastYear := year))
    print("   - " + event['name'])

    # get matches
    matchJSON = getTBAData('event/' + str(event['key']) + '/matches/simple')
    for match in matchJSON:
        alliances = match['alliances']
        if ('frc' + team1) in alliances['blue']['team_keys'] and ('frc' + team2) in alliances['red']['team_keys']:
            if match['winning_alliance'] == 'blue':
                team1Wins += 1
                t1WinMatches.append(match['key'])
            elif match['winning_alliance'] == '':
                ties += 1
                tieMatches.append(match['key'])
            else:
                team2Wins += 1
                t2WinMatches.append(match['key'])
        elif ('frc' + team2) in alliances['blue']['team_keys'] and ('frc' + team1) in alliances['red']['team_keys']:
            if match['winning_alliance'] == 'red':
                team1Wins += 1
                t1WinMatches.append(match['key'])
            elif match['winning_alliance'] == '':
                ties += 1
                tieMatches.append(match['key'])
            else:
                team2Wins += 1
                t2WinMatches.append(match['key'])
try:
    print('\n' + team1Name + " win rate vs " + team2Name + ": " + str(team1Wins) + '-' + str(team2Wins) + '-' +
          str(ties) + " (" + str(round(team1Wins / (team1Wins + team2Wins) * 100)) + "%)")
except ZeroDivisionError:
    print("\nNo matches played between " + team1Name + " and " + team2Name + (" in " + str(startDate)
          if startDate == endDate else " between " + str(startDate) + " and " + str(endDate)) +
          " resulting in a win. They have had " + str(ties) + " ties.")
    played = False
if played:
    if team1Wins > 0:
        print('\n' + team1Name + " wins: ")
        for match in t1WinMatches:
            print(" - https://thebluealliance.com/match/" + match)
    if team2Wins > 0:
        print('\n' + team2Name + " wins: ")
        for match in t2WinMatches:
            print(" - https://thebluealliance.com/match/" + match)
    if ties > 0:
        print("\nTies: ")
        for match in tieMatches:
            print(" - https://thebluealliance.com/match/" + match)