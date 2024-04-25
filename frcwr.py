import requests
import sys
try:
    useCLInput = len(sys.argv) > 1

    baseUrl = 'http://www.thebluealliance.com/api/v3/'
    header = {
        'X-TBA-Auth-Key': 'wGzJseZbdMKuFK9zflg15hCUMOz7ZMWDSeLgtGlhorVXLgxqeY2v6SXSAQeTeDVU'}


    def getTBAData(url):
        result = requests.get(baseUrl + url, headers=header)
        if result.status_code != 200 or (len(result.json()) == 1 and result.json().keys()[0] == "Error"):
            print("--API Error-- Status code: " + str(result.status_code) + ", Error message: [" + result.json()['Error'] + ']')
            exit(404)
        return result.json()


    # decode CLinput
    if useCLInput:
        team1 = ""
        team2 = ""
        startDate = 0
        endDate = 0
        for i in range(len(sys.argv)):
            match sys.argv[i]:
                case "-team1":
                    if i == len(sys.argv) - 1 or sys.argv[i + 1].__contains__('-'):
                        print("-team1: Value is required")
                        exit()
                    team1 = sys.argv[i + 1]
                case "-team2":
                    if i == len(sys.argv) - 1 or sys.argv[i + 1].__contains__('-'):
                        print("-team2: Value is required")
                        exit()
                    team2 = sys.argv[i + 1]
                case "-start":
                    if i < len(sys.argv) - 1 and not(sys.argv[i + 1].__contains__('-')):
                        try:
                            startDate = int(sys.argv[i + 1])
                        except ValueError:
                            print("Error: start year value must be a valid integer")
                            exit(1)
                case "-end":
                    if i < len(sys.argv) - 1 and not(sys.argv[i + 1].__contains__('-')):
                        try:
                            endDate = int(sys.argv[i + 1])
                        except ValueError:
                            print("Error: start year value must be a valid integer")
                            exit(1)

        team1JSON = getTBAData("team/frc" + team1)
        team1Start = team1JSON['rookie_year']
        team1Name = team1JSON['nickname']
        team2JSON = getTBAData("team/frc" + team2)
        team2Start = team2JSON['rookie_year']
        team2Name = team2JSON['nickname']
        currYear = getTBAData('status')['current_season']
        played = True

        if startDate == 0:
            startDate = max(team1Start, team2Start)

        if endDate == 0:
            endDate = currYear

        if startDate > endDate:
            print("Error: start year cannot be greater than end year")
            exit(1)

    else:
        team1 = input("Team 1 number: ")
        team2 = input("Team 2 number: ")

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

        if startDateIn := input("Start Year: "):
            startDate = int(startDateIn)
            if startDate == currYear:
                endDate = currYear
            else:
                if endDateIn := input("End Year: "):
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

    exit(0)
except KeyboardInterrupt:
    exit(130)