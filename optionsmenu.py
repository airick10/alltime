import inputcheck
import random

def draftMenu():
	print("------------")
	print("Draft Menu")
	print("What do you want to do?")
	print("1. View Top Available Hitters")
	print("2. View Top Available Pitchers")
	print("3. View Your Team")
	print("4. View Another team")
	print("5. View Draft Log")
	print("6. Search for a specific player")
	print("7. Look for a specific list of Positions / Pitcher Roles")
	print("8. Sort by a specific stat")
	print("9. Exit Program")
	choice = inputcheck.inputCheck("Select what option you want.", 1, 9)
	'''
	choice = input("Select what option you want")
	while not choice.isdigit():
		choice = input("Please select a number.  Which option do you want? ")
	choice = int(choice)
	'''
	return choice
	
def optionSetDraftPosition(numteams, humannum):
	setDraft = []
	totalteams = humannum
	while totalteams > 0:
		tempslot = int(input("You have selected {} human teams.  This will be a snake draft.  Between slot 1-{}, which slot do you want a human team picking? ".format(humannum, numteams)))
		print("")
		while tempslot > numteams or tempslot < 1:
			tempslot = int(input("Please try again, the slot selected it outside the draft range!  You have selected {} human teams.  This will be a snake draft.  Between slot 1-{}, which slot do you want a human team picking? ".format(humannum, numteams)))
			print("")
		while tempslot in setDraft:
			tempslot = int(input("This slot is already selected.  Choose again.  You have selected {} human teams.  This will be a snake draft.  Between slot 1-{}, which slot do you want a human team picking? ".format(humannum, numteams)))
			print("")
		setDraft.append(tempslot)
		totalteams -= 1 
	return setDraft	
	

def optionSetRandomDraft(max_range):
	if max_range <= 0:
		return []

	if max_range < 2:
		return [1]

	numbers = list(range(1, max_range + 1))
	random.shuffle(numbers)
	return numbers
	
	
def viewOtherTeamList(league, numteams, draftSlotNum):
	
	teamchoice = [0]		
	counter = 1
	checkrange = numteams - 1
	print("----- Team List -----")
	for team in league:
		if team['DraftSlot'] != draftSlotNum:	
			print(f"{counter}. {team['TeamName']}")
			teamchoice.append(team['DraftSlot'])
			counter += 1
    
	selected_team = inputcheck.inputCheck("Select a team.  Press 0 to go back to the Draft Menu ", 0, numteams)
	
	return teamchoice[selected_team]


def searchPlayer(hitters, pitchers, tryagain):
	if tryagain:
		search = input("No matches found!  One more try.  Type the name of a player to look for ")
	else:
		search = input("Type the name of a player to look for ")
	search = search.capitalize()
	player_list = [0]
	counter = 1
	for player in hitters:
		if 'FirstName' in player and 'LastName' in player:
			if search in player['FirstName'] or search in player['LastName']:
				playerid = int(player['ID'])
				player_list.append(playerid)
				print(f"{counter}. {player['FirstName']} {player['LastName']}")
				counter += 1
	for player in pitchers:
		if 'FirstName' in player and 'LastName' in player:
			if search in player['FirstName'] or search in player['LastName']:
				playerid = int(player['ID'])
				player_list.append(playerid)
				print(f"{counter}. {player['FirstName']} {player['LastName']}")
				counter += 1
	if counter > 1:
		choice = inputcheck.inputCheck("Select the number for a player you want to see more details of.  Select 0 to go back to the menu.", 0, counter)
		return player_list[choice]
	else:
		return 1


def playerDetails(hitters, pitchers, playerid, viewOnly):
	playerid = str(playerid)
	type = inputcheck.hitterOrPitcher(hitters, pitchers, playerid)
	if type == "H":
		for player in hitters:
			if player['ID'] == playerid:
				print(f"Name: {player['FirstName']} {player['LastName']}")
				print(f"Year: {player['Year']}")
				print(f"Team: {player['Team']}")
				print(f"Bat: {player['Bat']}")
				print(f"Games: {player['G']}")
				print(f"At Bats: {player['AB']}")
				print(f"Runs: {player['R']}")
				print(f"Hits: {player['H']}")
				print(f"Doubles: {player['2B']}")
				print(f"Triples: {player['3B']}")
				print(f"Home Runs: {player['HR']}")
				print(f"RBI: {player['RBI']}")
				print(f"Walks: {player['BB']}")
				print(f"Strikeouts: {player['K']}")
				print(f"Hit By Pitch: {player['HB']}")
				print(f"Stolen Bases: {player['SB']}")
				print(f"Caught Stealing: {player['CS']}")
				print(f"Batting Avg: {player['Avg']}")
				print(f"OnBase Percentage: {player['OBP']}")
				print(f"Slugging Percentage: {player['SLG']}")
				playername = player['FirstName'] + " " + player['LastName']
	else:
		for player in pitchers:
			if player['ID'] == playerid:
				print(f"Name: {player['FirstName']} {player['LastName']}")
				print(f"Year: {player['Year']}")
				print(f"Team: {player['Team']}")
				print(f"Throw: {player['Throw']}")
				print(f"Games: {player['G']}")
				print(f"Games Started: {player['GS']}")
				print(f"Complete Games: {player['CG']}")
				print(f"Shutouts: {player['SHO']}")
				print(f"Wins: {player['W']}")
				print(f"Losses: {player['L']}")
				print(f"Saves: {player['SV']}")
				print(f"Innings Pitched: {player['IP']}")
				print(f"Hits: {player['H']}")
				print(f"Earned Runs: {player['ER']}")
				print(f"Home Runs: {player['HR']}")
				print(f"Walks: {player['BB']}")
				print(f"Strikeouts: {player['K']}")
				print(f"Wild Pitches: {player['WP']}")
				print(f"Balks: {player['BK']}")
				print(f"ERA: {player['ERA']}")
				print(f"WHIP: {player['WHIP']}")
				playername = player['FirstName'] + " " + player['LastName']
	if viewOnly:
		input("Press any key to go back to the Draft Menu")
		return 0
	else:
		draftConfirm = input("Do you wish to draft this player?  Type 'Y' for yes.  Press any key to go back to the Draft Menu")
		if draftConfirm == "Y" or draftConfirm == "y":
			print(f"{playername} has been drafted!")
			return playerid
		else:
			return 0


def assignToRoster(team, playerid, playerlist, type):
	if type == "H":
	# Dictionary to map positions to team roster spots
		position_map = {
			0: ['UT1', 'UT2', 'UT3', 'UT4', 'UT5', 'UT6', 'UT7'],
			2: ['C1', 'C2'],
			3: ['1B'],
			4: ['2B'],
			5: ['3B'],
			6: ['SS'],
			7: ['LF'],
			8: ['CF'],
			9: ['RF'],
		}

		#Go through individual player's DP listings.  DP1 - DP8.
		#Check and see what is assigned at DP1, DP2, and so on.
		for i in range(1, 9):  # Assuming DP1 to DP8 are consecutive.
			#Looping through, assigning pos to DP1, then loop to DP2, then loop to DP3
			pos = int(playerlist[f'DP{i}'])
			#Using the self made position_map above, grab the value depending on the pos (which is the key)
			#roster_spot is now the value (C1, 2B, LF) of position_map[2] and [4] and [7].
			#Use that value as the key for team.
			for roster_spot in position_map.get(pos):
				if team[roster_spot] == "Unassigned":
					team[roster_spot] = playerid
					return team
		# ... previous code ...

	else:
	# Dictionary to map roles to team roster spots
		role_map = {
			'S': ['SP1', 'SP2', 'SP3', 'SP4', 'SP5'],
			'R': ['RP1', 'RP2', 'RP3', 'RP4', 'RP5'],
		}
		
		role = playerlist['Role']
		# role is 'S' or 'R', depending on the pitcher array.
		# get will take the key value (role, associated with role_map).
		for roster_spot in role_map.get(role):
			if team[roster_spot] == "Unassigned":
				team[roster_spot] = playerid
				return team

	return team
		

def selectPlayer(league, hitters, pitchers, player_to_draft, draftSlotNum):
	type = inputcheck.hitterOrPitcher(hitters, pitchers, player_to_draft)
	for team in league:
		if team['DraftSlot'] == draftSlotNum:
			for player in hitters:
				if player['ID'] == player_to_draft:
    			#NEED MORE LOGIC HERE
					#team['C1'] = player_to_draft
					team = assignToRoster(team, player_to_draft, player, "H")
			for player in pitchers:
				if player['ID'] == player_to_draft:
 					#NEED MORE LOGIC HERE
					#team['SP1'] = player_to_draft
					team = assignToRoster(team, player_to_draft, player, "P")
	return league



