import requests
import sys
import os
try:
    useCLInput = len(sys.argv) > 1

    apikey = ""

    # i know this is bad
    if useCLInput:
        apikey = [sys.argv[i + 1]
                  for i in range(len(sys.argv)) if sys.argv[i] == "-key"][0]

    if apikey == "":
        if os.path.exists("apikey.txt") and os.path.getsize("apikey.txt") > 0:
            with open("apikey.txt") as f:
                apikey = f.read()
        else:
            apikey = input("Enter TBA API Key: ")
            with open("apikey.txt", 'w') as f:
                f.truncate(0)
                f.write(apikey)

    baseUrl = 'http://www.thebluealliance.com/api/v3/'
    header = {
        'X-TBA-Auth-Key': apikey}

    def getTBAData(url):
        try:
            result = requests.get(baseUrl + url, headers=header)
        except requests.exceptions.ConnectionError:
            print("Error: Bad network connection. Make sure you are connected to Wi-Fi")
            exit(1)
        except:
            e_type, e_val, e_trace = sys.exc_info()
            print("Unexpected exception: \n\t-Type: {}, \n\t-Message: {}, \n\t-Traceback: {}".format(
                e_type.__name__, e_val, e_trace))
            print("Report to https://github.com/gabeStuk/FRC-Win-Rate-Calculator/issues")
            exit(1)
        if result.status_code != 200 or (len(result.json()) == 1 and list(result.json())[0] == "Error"):
            if result.json()['Error'] == "X-TBA-Auth-Key is invalid. Please get an access key at https://www.thebluealliance.com/account/login?next=http://www.thebluealliance.com/account.":
                print("Error with TBA auth key.")
                exit(1)
            print("--API Error-- Status code: " + str(result.status_code) +
                  ", Error message: [" + result.json()['Error'] + ']')
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
                    team1 = sys.argv[i + 1].lstrip("0")
                case "-team2":
                    if i == len(sys.argv) - 1 or sys.argv[i + 1].__contains__('-'):
                        print("-team2: Value is required")
                        exit()
                    team2 = sys.argv[i + 1].lstrip("0")
                case "-start":
                    if i < len(sys.argv) - 1 and not (sys.argv[i + 1].__contains__('-')):
                        try:
                            startDate = int(sys.argv[i + 1])
                        except ValueError:
                            print("Error: start year value must be a valid integer")
                            exit(1)
                case "-end":
                    if i < len(sys.argv) - 1 and not (sys.argv[i + 1].__contains__('-')):
                        try:
                            endDate = int(sys.argv[i + 1])
                        except ValueError:
                            print("Error: start year value must be a valid integer")
                            exit(1)

        team1JSON = getTBAData("team/frc" + team1.lstrip("0"))
        team1Start = team1JSON['rookie_year']
        team1Name = team1JSON['nickname']
        team2JSON = getTBAData("team/frc" + team2.lstrip("0"))
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
        team1 = input("Team 1 number: ").lstrip("0")
        team2 = input("Team 2 number: ").lstrip("0")

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
        matchJSON = getTBAData(
            'event/' + str(event['key']) + '/matches/simple')
        for match in matchJSON:
            alliances = match['alliances']
            if ('frc' + team1) in alliances['blue']['team_keys'] and ('frc' + team2) in alliances['red']['team_keys']:
                if match['winning_alliance'] == 'blue' and alliances['blue']['score'] != -1:
                    team1Wins += 1
                    t1WinMatches.append(match['key'])
                elif match['winning_alliance'] == '' and alliances['blue']['score'] != -1:
                    ties += 1
                    tieMatches.append(match['key'])
                elif alliances['blue']['score'] != -1:
                    team2Wins += 1
                    t2WinMatches.append(match['key'])
            elif ('frc' + team2) in alliances['blue']['team_keys'] and ('frc' + team1) in alliances['red']['team_keys']:
                if match['winning_alliance'] == 'red' and alliances['red']['score'] != -1:
                    team1Wins += 1
                    t1WinMatches.append(match['key'])
                elif match['winning_alliance'] == '' and alliances['red']['score'] != -1:
                    ties += 1
                    tieMatches.append(match['key'])
                elif alliances['red']['score'] != -1:
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
except:
    e_type, e_val, e_trace = sys.exc_info()
    if (e_type != SystemExit):
        print("Unexxpected exception: \n\t-Type: {}, \n\t-Message: {}, \n\t-Traceback: {}".format(
            e_type.__name__, e_val, e_trace))
        print("Report to https://github.com/gabeStuk/FRC-Win-Rate-Calculator/issues/new")
        exit(1)
