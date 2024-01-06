import alltimedraft
import aipicks
import random
import json
from tabulate import tabulate

def gatherPlayers(jf, type):
	with open(jf) as fp:
		players = json.load(fp)
	if type == "H":
		for record in players:
			record["ID"] = str(record["ID"])
			record["DP1"] = str(record["DP1"])
			record["DR1"] = str(record["DR1"])
			record["DP2"] = str(record["DP2"])
			record["DR2"] = str(record["DR2"])
			record["DP3"] = str(record["DP3"])
			record["DR3"] = str(record["DR3"])
			record["DP4"] = str(record["DP4"])
			record["DR4"] = str(record["DR4"])
			record["DP5"] = str(record["DP5"])
			record["DR5"] = str(record["DR5"])
			record["DP6"] = str(record["DP6"])
			record["DR6"] = str(record["DR6"])
			record["DP7"] = str(record["DP7"])
			record["DR7"] = str(record["DR7"])
			record["DP8"] = str(record["DP8"])
			record["DR8"] = str(record["DR8"])
			record["Avg"] = "{:.3f}".format(record["Avg"]).lstrip('0')
			record["OBP"] = "{:.3f}".format(record["OBP"]).lstrip('0')
			record["SLG"] = "{:.3f}".format(record["SLG"]).lstrip('0')
	else:
		for record in players:
			record["ID"] = str(record["ID"])
			record["ERA"] = "{:.2f}".format(record["ERA"]).lstrip('0')
			record["WHIP"] = "{:.3f}".format(record["WHIP"]).lstrip('0')
	return players
	
def setUpTeams(numteams, randomDraft, humannum):
    league = [{} for _ in range(numteams)]
    teamnameary = []
    setHumanDraftSlot = [0]
    randomDraftOrder = []
    randomDraftOrder = optionSetRandomDraft(numteams)
    if humannum > 0:
    	if not randomDraft:
    		setHumanDraftSlot = optionSetDraftPosition(numteams, humannum)

    counter = 1
    draftCounter = 0
    aiSequenceSlot = 1

    randomNameChoice = input("Press 'Y' if you want randomly assigned names.  Press any key to input your own  ")
    if randomNameChoice == "Y" or randomNameChoice == "y":
    	randomTeamNames = False
    	teamnames = ["Wizards", "Warriors", "Barons", "Vipers", "Expos", 
    	"Packers", "Buccaneers", "Panthers", "Generals", "Storm", "Rockets", 
    	"Sharks", "Hawks", "Bombers", "Chargers", "Mavericks", "Vikings",
    	"Rams", "Lions", "Jesters", "Sluggers", "Warlocks", "Badgers",
    	"Gorillas", "Bats", "Express", "Blue Sox", "Bandits", "Rogues"]
    	selected_teams = random.sample(teamnames, numteams + 1)
    else:
    	randomTeamNames = True
    	

    for team in league:
        # TeamID
        team["TeamID"] = counter
        team["AIFocus"] = aiFocus()
        if humannum > 0:
        	if randomTeamNames: 
        		team["TeamName"] = input(f"Human Team {team['TeamID']}: What do you want for the team name? ")
        	else:
        		team["TeamName"] = selected_teams[counter]
        		print(f"Human Team Name: {selected_teams[counter]}")
        		input("Press any key to continue")
        	team["Human"] = True
        	team["TeamName"] = team["TeamName"].title()
        	while team["TeamName"] in teamnameary:
        		team["TeamName"] = input(f"Try again, team name already exists - Human Team {team['TeamID']}: What do you want for the team name? ")
        		team["TeamName"] = team["TeamName"].title()
        	teamnameary.append(team["TeamName"])
        else:
        	if randomTeamNames:
        		team["TeamName"] = input(f"AI Team {team['TeamID']}: What do you want for the team name? ")
        	else:
        		team["TeamName"] = selected_teams[counter]
        	team["Human"] = False
        	team["TeamName"] = team["TeamName"].title()
        	while team["TeamName"] in teamnameary:
        		team["TeamName"] = input(f"Try again, team name already exists - AI Team {team['TeamID']}: What do you want for the team name? ")
        		team["TeamName"] = team["TeamName"].title()
        	teamnameary.append(team["TeamName"])
        while not team["TeamName"]:
            team["TeamName"] = input(f"Try again - Team {team['TeamID']}: What do you want for the team name? ")
        # Draft Slot
        # If a random draft order was selected, take the next slot in the array and assign it as the draft slot.  Regardless if it's AI or Human
        # randomDraftOrder is taken from the optionSetRandomDraft function.  draftCounter parses through the array record by record.
        if randomDraft:
        	team["DraftSlot"] = randomDraftOrder[draftCounter]
        # If a random draft order is not selected, proceed by assigning Team 1 - Draft Slot 1.  Team 2 - Draft Slot 2.  And so on.
        else:
        # However, if a Human has selected a draft slot, assign their Team 1 team to the draft slot they wanted.
        # Human players are assigned for the first human team as Team 1, second human team as Team 2, and so on.  So we can use the draftCounter to parse through and assign the humans first.
        # setHumanDraft Slot is taken from the optionSetDraftPosition function 
        	if team["Human"]:
        		team["DraftSlot"] = setHumanDraftSlot[draftCounter]
        		team["AIFocus"] = 0
        # If this team is an AI team in a draft that has a distinct order, still assign the Team 1 - Draft Slot 1 unless a human team comes up.
        	else:
        		# aiSequenceSlot acts as a draft counter for just AI teams.  So in this first if statement, I'm asking if any human selected the current aiSequenceSlot number.  Example, in an 8 team draft, a human wanted to select pick 3.  This if statement checks if '3' exists anywhere in the setHumanDraftSlot array.  If it doesn't, assign that number to the current AI team and add the aiSequenceSlot for the next AI team.
        		if aiSequenceSlot not in setHumanDraftSlot:
        			team["DraftSlot"] = aiSequenceSlot
        			aiSequenceSlot += 1
        		# If this team is an AI team and the aiSequenceSlot WAS selected by a human, they add one to the aiSequence Slot to assign that to the AI team.  Then since aiSequenceSlot for this already assigned number will be checked, add another +1 to it for the next team.
        		else:
        			aiSequenceSlot += 1
        			team["DraftSlot"] = aiSequenceSlot
        			aiSequenceSlot += 1
       	team["C1"] = "Unassigned"
        team["C2"] = "Unassigned"
        team["1B"] = "Unassigned"
        team["2B"] = "Unassigned"
        team["3B"] = "Unassigned"
        team["SS"] = "Unassigned"
        team["LF"] = "Unassigned"
        team["CF"] = "Unassigned"
        team["RF"] = "Unassigned"
        team["SP1"] = "Unassigned"
        team["SP2"] = "Unassigned"
        team["SP3"] = "Unassigned"
        team["SP4"] = "Unassigned"
        team["SP5"] = "Unassigned"
        team["RP1"] = "Unassigned"
        team["RP2"] = "Unassigned"
        team["RP3"] = "Unassigned"
        team["RP4"] = "Unassigned"
        team["RP5"] = "Unassigned"
        team["UT1"] = "Unassigned"
        team["UT2"] = "Unassigned"
        team["UT3"] = "Unassigned"
        team["UT4"] = "Unassigned"
        team["UT5"] = "Unassigned"
        team["UT6"] = "Unassigned"
        team["Salary"] = 200000
        counter += 1
        humannum -= 1
        draftCounter += 1  
    del teamnameary
    del setHumanDraftSlot	
    del randomDraftOrder
    return league

def draftOrderAnnounce(league, slotnum):
	humanbool = False
	for team in league:
		if team["DraftSlot"] == slotnum:	
			input ("{} will now draft!  Press Enter to Continue...".format(team["TeamName"]))
			humanbool = team["Human"]
	return humanbool

def draftOrderIncrement(slotnum, numteams, direction):
	#If 12 team draft, take number 6 and add one if we are moving to slot 7, but only if the slot is
	#less then the total teams in the draft.  If a 12 team draft and slotnum = 12, just return it to start
	#the downward flow.

	if direction == "Up":
		if numteams > slotnum:
			slotnum += 1
			return slotnum
		else:
			return slotnum
	if direction == "Down":
		if slotnum > 1:
			slotnum -= 1
			return slotnum
		else:
			return slotnum


def getDraftLog(league, numteams):
	draftLog = []
	draftOrder = []
	rdCounter = 1
	for i in range(numteams + 1):
		for team in league:
			if i == team['DraftSlot']:
				draftOrder.append(team['TeamName'])
		#draftOrder.append(team['DraftSlot'])
	while rdCounter < 26:
		for i in range(numteams):
			draftLog.append(draftOrder[i])
		for i in range(numteams - 1, -1, -1):
			draftLog.append(draftOrder[i])
		rdCounter += 1
	print("")
	print("Draft Order (Snake Format)")
	print("-----------")
	for i in range(numteams):
		print(f"{i+1}: {draftLog[i]}")
	return draftLog
		
	
def viewTeam(league, hitters, pitchers, select, salaryCap):
	counter = 0
	idSelected = False
	choicearray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#select is the DraftSlot.  That doesn't mean it's the TeamID slot.
	#This loop goes through League and captures the TeamID of the DraftSlot
	#Because an array starts at 0, I'm turning record['TeamID'] into an int and subtracting by 1.
	for record in league:
		if record['DraftSlot'] == select:
			if salaryCap:
				salary = int(record['Salary'])
				print(f"{record['TeamName']} - ${salary:,} left")
			else:
				print(f"{record['TeamName']}")
			print("-----------------")
			teamid = int(record['TeamID']) - 1	
	#k = Key, v = Va	
	for k,v in league[teamid].items():
		empty_slot = True
		if k != "TeamID" and k != "DraftSlot" and k != "Human" and k != "Salary" and k != "AIFocus":
			#if k == "TeamName":
				#print(f"{v}")
				#print("-------------")
				
			if "SP" not in k and "RP" not in k:
				for player in hitters:
					if player['ID'] == v:
						playerid = int(v)
						choicearray[counter] = v
						idSelected = True
						empty_slot = False
					if idSelected:
						if salaryCap:
							print(f"{counter}. {k} - {player['FirstName']} {player['LastName']}: ${player['Price']:,}")
						else:
							print(f"{counter}. {k} - {player['FirstName']} {player['LastName']}")
					idSelected = False
							
			else:
				for player in pitchers:
					if player['ID'] == v:
						playerid = int(v)
						choicearray[counter] = v
						idSelected = True
						empty_slot = False
					if idSelected:
						if salaryCap:
							print(f"{counter}. {k} - {player['FirstName']} {player['LastName']}: ${player['Price']:,}")
						else:
							print(f"{counter}. {k} - {player['FirstName']} {player['LastName']}")
					idSelected = False

			if empty_slot and k != "TeamName":
				print(f"{counter}. {k}")
			counter += 1
	
	choice = alltimedraft.inputCheck("Choose a player to view details.  Press 0 to go back to the Draft Menu ", 0, 27)
	while choicearray[choice] == 0 and choice != 0:
		choice = alltimedraft.inputCheck("Player is unassigned at this slot.  Try again.  Choose a player to view details.  Press 0 to go back to the Draft Menu ", 0, 27)
	else:
		choice = 0

	return choicearray[choice]
	
	

def getLog(league, hitters, pitchers, team_ary, selected_ary, numteams):
	counter = 0
	rdCounter = 1
	rdLabel = 1
	overallCounter = 0
	print(f"---- Round {rdLabel} ----")
	for pick in selected_ary:
		if rdCounter > numteams:
			print("")
			rdLabel += 1
			print(f"---- Round {rdLabel} ----")
			rdCounter = 1
		for player in hitters:
			if pick == player['ID']:
				name = player['FirstName'] + " " + player['LastName']
				position = alltimedraft.posConvert(player['DP1'])
		for player in pitchers:
			if pick == player['ID']:
				name = player['FirstName'] + " " + player['LastName']
				position = alltimedraft.posConvert(player['Role'])
		print(f"{overallCounter + 1}. {team_ary[overallCounter]}: {position} - {name}")
		overallCounter += 1
		rdCounter += 1
		counter += 1
	input("Press any key to go back to the draft menu")
	return 0


def aiFocus():
	choices = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
	choice = random.choice(choices)
	return choice	


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
	choice = alltimedraft.inputCheck("Select what option you want.", 1, 9)
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
    
	selected_team = alltimedraft.inputCheck("Select a team.  Press 0 to go back to the Draft Menu ", 0, numteams)
	
	return teamchoice[selected_team]


def searchPlayer(hitters, pitchers, selected_list, tryagain):
	if tryagain:
		search = input("No matches found!  One more try.  Type the name of a player to look for ")
		while search == "":
			search = input("Type in a name.  Type the name of a player to look for ")
	else:
		search = input("Type the name of a player to look for.  Only players that have not been drafted will be found! ")
		while search == "":
			search = input("Type in a name.  Type the name of a player to look for ")
	search = search.title()
	player_list = [0]
	counter = 1
	for player in hitters:
		if 'FirstName' in player and 'LastName' in player:
			if search in player['FirstName'] or search in player['LastName']:
				if player['ID'] not in selected_list:
					playerid = int(player['ID'])
					player_list.append(playerid)
					print(f"{counter}. {player['FirstName']} {player['LastName']}")
					counter += 1
	for player in pitchers:
		if 'FirstName' in player and 'LastName' in player:
			if search in player['FirstName'] or search in player['LastName']:
				if player['ID'] not in selected_list:
					playerid = int(player['ID'])
					player_list.append(playerid)
					print(f"{counter}. {player['FirstName']} {player['LastName']}")
					counter += 1
	if counter > 1:
		choice = alltimedraft.inputCheck("Select the number for a player you want to see more details of.  Select 0 to go back to the menu.  ", 0, counter)
		return player_list[choice]
	else:
		return 1


def playerDetails(hitters, pitchers, playerid, viewOnly):
	playerid = str(playerid)
	type = alltimedraft.hitterOrPitcher(hitters, pitchers, playerid)
	if type == "H":
		for player in hitters:
			if player['ID'] == playerid:
				print(f"Name: {player['FirstName']} {player['LastName']}")
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
		draftConfirm = input("Do you wish to draft this player?  Type 'Y' for yes.  Press any key to go back to the Draft Menu  ")
		if draftConfirm == "Y" or draftConfirm == "y":
			print("")
			return playerid
		else:
			return 0

def selectPlayer(league, hitters, pitchers, player_to_draft, draftSlotNum, salaryCap):
	position = "None"
	player_type = alltimedraft.hitterOrPitcher(hitters, pitchers, player_to_draft)
	for team in league:
		if team['DraftSlot'] == draftSlotNum:
			if player_type == "H":
				for player in hitters:
					if player['ID'] == player_to_draft:
						#Salary Cap Check for Human
						if team['Human'] and salaryCap and (player['Price'] > team['Salary']):
							print("Player puts you over the salary cap.  Choose another player")
							return "None"
						# Dictionary to map positions to team roster spots
						position_map = {
							0: ['UT1', 'UT2', 'UT3', 'UT4', 'UT5', 'UT6'],
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
						for i in range(1, 9):
							#Looping through, assigning pos to DP1, then loop to DP2, then loop to DP3
							pos = int(player[f'DP{i}'])
							#Using the self made position_map above, grab the value depending on the pos (which is the key)
							#roster_spot is now the value (C1, 2B, LF) of position_map[2] and [4] and [7].
							#Use that value as the key for team.
							for roster_spot in position_map.get(pos):
								if team[roster_spot] == "Unassigned":
									position = roster_spot
									return position
							if team['Human']:
								print("")
								print("Position in starting lineup is booked.  Moving to Utility slot.")
							else:
								with open('log.txt', 'a') as file:
									file.write("**AI LOG** - Position Check Failed.  Choosing another" + '\n')
			else:
				for player in pitchers:
					if player['ID'] == player_to_draft:
						#Salary Cap Check for Human
						if team['Human'] and salaryCap and (player['Price'] > team['Salary']):
							print("Player puts you over the salary cap.  Choose another player")
							return "None"
						# Dictionary to map roles to team roster spots
						role_map = {
							'S': ['SP1', 'SP2', 'SP3', 'SP4', 'SP5'],
							'R': ['RP1', 'RP2', 'RP3', 'RP4', 'RP5'],
						}
						
						role = player['Role']
						# role is 'S' or 'R', depending on the pitcher array.
						# get will take the key value (role, associated with role_map).
						for roster_spot in role_map.get(role):
							if team[roster_spot] == "Unassigned":
								position = roster_spot
								return position
						if team['Human']:
							print("")
							print("No position is available to put this player on.  Please select another.")
						else:
							with open('log.txt', 'a') as file:
								file.write("**AI LOG** - Position Check Failed.  Choosing another" + '\n')

	return position

def assignToRoster(league, hitters, pitchers, player_to_draft, draftSlotNum, position):
	player_type = alltimedraft.hitterOrPitcher(hitters, pitchers, player_to_draft)
	for team in league:
		if team['DraftSlot'] == draftSlotNum:
			if player_type == "H":
				for player in hitters:
					if player['ID'] == player_to_draft:
						team[position] = player_to_draft
						team['Salary'] -= player['Price']
						pos = alltimedraft.posConvert(player['DP1'])
						with open('log.txt', 'a') as file:
							file.write(f"{team['TeamName']} have drafted {pos} - {player['FirstName']} {player['LastName']} " + '\n')
						print(f"{team['TeamName']} have drafted {pos} - {player['FirstName']} {player['LastName']} ")
			else:
				for player in pitchers:
					if player['ID'] == player_to_draft:
						team[position] = player_to_draft
						team['Salary'] -= player['Price']
						pos = alltimedraft.posConvert(player['Role'])
						with open('log.txt', 'a') as file:
							file.write(f"{team['TeamName']} have drafted {pos} - {player['FirstName']} {player['LastName']} " + '\n')
						print(f"{team['TeamName']} have drafted {pos} - {player['FirstName']} {player['LastName']} ")
	return league


def positionList():
		position_ary = [0,False]
		print("------------")
		print("Position Filter Menu")
		print("Which position ")
		print("1. Starting Pitcher")
		print("2. Relief Pitcher")
		print("3. Catcher")
		print("4. First Baseman")
		print("5. Second Baseman")
		print("6. Third Baseman")
		print("7. Shortstop")
		print("8. Left Fielder")
		print("9. Center Fielder")
		print("10. Right Fielder")
		position_ary[0] = alltimedraft.inputCheck("Select what option you want. Type 0 to ignore and go back. ", 0, 10)
		print("------------")
		if position_ary[0] > 2:
			tempchoice = input("Do you want this to be their primary position or at least are eligible there?  Type 'Y' for just the primary and 'N' for anyone eligible ")
			while tempchoice != "y" and tempchoice != "Y" and tempchoice != "n" and tempchoice != "N":
				tempchoice = input("Please select 'Y' or 'N'.  Do you want this to be their primary position or at least are eligible there?  Type 'Y' for just the primary and 'N' for anyone eligible ")
			if tempchoice == "Y" or tempchoice == "y":
				position_ary[1] = True
			else:
				position_ary[1] = False
			return position_ary
		else:
			position_ary[1] = False
			return position_ary
			
			
def sortListMenu():
	choice = 0
	print("------------")
	print("Sort Menu")
	print("Which statistic ")
	print("--- Hitters ---")
	print("1. Hits")
	print("2. Runs")
	print("3. Home Runs")
	print("4. RBI")
	print("5. Stolen Bases")
	print("6. Walks")
	print("7. Strikeouts")
	print("8. Batting Avg")
	print("9. On Base Percentage")
	print("10. Slugging Percentage")
	print("")
	print("--- Pitchers ---")
	print("11. Innings Pitched")
	print("12. Wins")
	print("13. Losses")
	print("14. Saves")
	print("15. Earned Runs")
	print("16. Home Runs")
	print("17. Walks")
	print("18. Strikeouts")
	print("19. Earned Run Average")
	print("20. WHIP")
	choice = alltimedraft.inputCheck("Select what stat to sort. Type 0 to ignore and go back. ", 0, 20)
	match choice:
		case 0:
			return "None"
		case 1:
			return "H"
		case 2:
			return "R"
		case 3:
			return "HHR"
		case 4:
			return "RBI"
		case 5:
			return "SB"
		case 6:
			return "HBB"
		case 7:
			return "HK"
		case 8:						
			return "Avg"
		case 9:
			return "OBP"
		case 10:
			return "SLG"
		case 11:
			return "IP"
		case 12:
			return "W"
		case 13:
			return "L"
		case 14:
			return "SV"
		case 15:
			return "ER"
		case 16:
			return "PHR"
		case 17:
			return "PBB"
		case 18:
			return "PK"
		case 19:
			return "ERA"							
		case 20:
			return "WHIP"	
		case _:
			return "None"
			
			
def sortList(playerpool, sortvalue, type):
	#hitters.sort(key=lambda x: x['Name'],reverse=True)
	if sortvalue != "Position" and sortvalue != "None":
		if type == "H":
			if sortvalue == "HHR":
				sortvalue = "HR"
			elif sortvalue == "HBB":
				sortvalue = "BB"
			elif sortvalue == "HK":
				sortvalue = "K"
			playerpool.sort(key=lambda x: x[sortvalue],reverse=True)
			return playerpool
							
		else:
			if sortvalue == "PHR":
				sortvalue = "HR"
			elif sortvalue == "PBB":
				sortvalue = "BB"
			elif sortvalue == "PK":
				sortvalue = "K"
			if sortvalue == "ERA" or sortvalue == "WHIP":
				playerpool.sort(key=lambda x: x[sortvalue])
			else:
				playerpool.sort(key=lambda x: x[sortvalue],reverse=True)
			return playerpool
	else:
		return playerpool


def getDraftPoolList(player, choicearray, counter, playertype, salaryCap):
	name = player['FirstName'] + " " + player['LastName']
	price = f"${player['Price']:,}"
	if playertype == "H":
		position = alltimedraft.posConvert(player['DP1'])
		slashline = player['Avg'] + "/" + player['OBP'] + "/" + player['SLG']
		if salaryCap:
			print(f"{counter}. {player['FirstName']} {player['LastName']} ({player['Team']}): {player['Bat']}/{position} - {player['Avg']}/{player['OBP']}/{player['SLG']} - ${player['Price']:,}")
			playerrow = [counter,name,player['Team'],player['Bat'],position,slashline,price]
		else:
			print(f"{counter}. {player['FirstName']} {player['LastName']} ({player['Team']}): {player['Bat']}/{position} - {player['Avg']}/{player['OBP']}/{player['SLG']}")
			playerrow = [counter,name,player['Team'],player['Bat'],position,slashline]
		playerid = int(player['ID'])
		choicearray.append(playerid)
	else:
		position = alltimedraft.posConvert(player['Role'])
		wl = str(player['W']) + "-" + str(player['L'])
		erawhip = player['ERA'] + "/" + player['WHIP']
		if salaryCap:
			print(f"{counter}. {player['FirstName']} {player['LastName']} ({player['Team']}): {player['Throw']}/{position}   ({player['W']}-{player['L']}) - {player['SV']} SV - {player['ERA']} ERA / {player['WHIP']} WHIP - ${player['Price']:,}")
			playerrow = [counter,name,player['Team'],player['Throw'],position,wl,player['SV'],erawhip,price]
		else:
			print(f"{counter}. {player['FirstName']} {player['LastName']} ({player['Team']}): {player['Throw']}/{position}   ({player['W']}-{player['L']}) - {player['SV']} SV - {player['ERA']} ERA / {player['WHIP']} WHIP")
			playerrow = [counter,name,player['Team'],player['Throw'],position,wl,player['SV'],erawhip]
		playerid = int(player['ID'])
		choicearray.append(playerid)
	return choicearray, playerrow


def getDraftPool(hitters, pitchers, type, sortvalue, selected_list, salaryCap):
	#X is the number of players displayed at once.
	X = 30
	choicearray = [0]
	if type == "H" and sortvalue != "None":
		hitters = sortList(hitters, sortvalue, "H")
	else:
		pitchers = sortList(pitchers, sortvalue, "P")
	
	
	#Gather records 30 - 60, for example.
	#for index, player in enumerate(hitters[30:60], start=30):
    #print(f"{index}. {player['Name']}, HR: {player['HR']}")
  
  #Counter actually measures the hitters/pitchers array and counts regardless of if a player is picked.  It keeps track of the actual source array.
  #Listcounter only increments when a player is available and gives the user a 1-30 choice.  Thus, the loop is based off that.
	counter = 0
	listcounter = 1
	if sortvalue == "Position":
		position = positionList()
		if position[0] < 3 and position[0] > 0:
			type = "P"
			position[0] = str(position[0])
			if position[0] == "1":
				position[0] = "S"
			else:
				position[0] = "R"
		elif position[0] == 0:
			sortvalue == "None"
		else:
			position[0] -= 1

	if type == "H":
		if salaryCap:
			table = [["Rank","Name","Team","Bat","Position","Avg/OBP/SLG","Price"]]
		else:
			table = [["Rank","Name","Team","Bat","Position","Avg/OBP/SLG"]]
		#for index, player in enumerate(hitters[:X]):
		while listcounter < 31 and len(hitters) > counter:	
			#Look for players who have not been drafted yet
			if hitters[counter]['ID'] not in selected_list:
				playerrow = None
				#POSITION CHECK
				if sortvalue == "Position" and position[1]:
					position[0] = str(position[0])
					if hitters[counter]['DP1'] == position[0]:
						choicearray, playerrow = getDraftPoolList(hitters[counter], choicearray, listcounter, "H", salaryCap)
						listcounter += 1
				elif sortvalue == "Position" and not position[1]:
					if hitters[counter]['DP1'] == position[0] or hitters[counter]['DP2'] == position[0] or hitters[counter]['DP3'] == position[0] or hitters[counter]['DP4'] == position[0] or hitters[counter]['DP5'] == position[0] or hitters[counter]['DP6'] == position[0] or hitters[counter]['DP7'] == position[0] or hitters[counter]['DP8'] == position[0]:
						choicearray, playerrow = getDraftPoolList(hitters[counter], choicearray, listcounter, "H", salaryCap)
						listcounter += 1		
				#IF POSITION CHECK ISN'T SELECTED
				else:
					choicearray, playerrow = getDraftPoolList(hitters[counter], choicearray, listcounter, "H", salaryCap)
					listcounter += 1
				if playerrow is not None:
					table.append(playerrow)
			counter += 1
	else:
		#for index, player in enumerate(pitchers[:X]):
		if salaryCap:
			table = [["Rank","Name","Team","Throw","Role","W/L","Saves","ERA/WHIP","Price"]]
		else:
			table = [["Rank","Name","Team","Throw","Role","W/L","Saves","ERA/WHIP"]]
		while listcounter < 31 and len(pitchers) > counter:
			#Look for players who have not been drafted yet
			if pitchers[counter]['ID'] not in selected_list:
				playerrow = None
				if sortvalue == "Position":
					if pitchers[counter]['Role'] == position[0]:
						choicearray, playerrow = getDraftPoolList(pitchers[counter], choicearray, listcounter, "P", salaryCap)
						listcounter += 1
				else:
					choicearray, playerrow = getDraftPoolList(pitchers[counter], choicearray, listcounter, "P", salaryCap)
					listcounter += 1
				if playerrow is not None:
					table.append(playerrow)
			counter += 1
	
	print(tabulate(table))
	choice = alltimedraft.inputCheck("Select the number for a player you want to see more details of.  Select 0 to go back to the menu.", 0, 30)
	return choicearray[choice]

def sortTeamCat(league, hitters, pitchers, cat, type):
	catDict = {}
	TotalCat = 0
	TotalCatabip = 0
	if cat != "Price":
		if type == "H":
			pos_ary = ['C1', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C2', 'UT1', 'UT2', 'UT3', 'UT4', 'UT5', 'UT6']
			bench = ['C2', 'UT1', 'UT2', 'UT3', 'UT4', 'UT5', 'UT6']
			for team in league:
				for key in pos_ary:
					for player in hitters:
						if team[key] == player['ID']:
							if cat == "OPS":
								TotalCat += float(player['OBP']) + float(player['SLG'])
							elif cat == "Defense":
								if player['DP1'] == "6" or player['DP1'] == "4" or player['DP1'] == "8":
									TotalCat += int(player['DR1']) * 2
								else:
									TotalCat += int(player['DR1'])
							elif cat == "SB":
								if key in bench:
									TotalCat += round((player['SB'] / 2) - round(player['CS'] / 2))
								else:
									TotalCat += player['SB'] - player['CS']
							elif cat == "K":
								if key in bench:
									TotalCat += round((player['K'] / 2) - round(player['BB'] / 2))
								else:
									TotalCat += player['K'] - player['BB']
							else:
								if key in bench:
									TotalCat += round(player[cat] / 2)
								else:
									TotalCat += player[cat]
				if cat == "OPS":
					TotalCat = TotalCat / 15
					TotalCat = float("{:.3f}".format(TotalCat))
					catDict.update({team['TeamName']: TotalCat})
				else: 
					catDict.update({team['TeamName']: round(TotalCat)})
				TotalCat = 0
				TotalCatabip = 0
		elif type == "P":
			pos_ary = ['SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'RP1', 'RP2', 'RP3', 'RP4', 'RP5']
			for team in league:
				for key in pos_ary:
					for player in pitchers:
						if team[key] == player['ID']:
							if cat == "ERA":
								TotalCat += player["ER"]
								TotalCatabip += player['IP']
							elif cat == "WHIP":
								TotalCat += player['BB'] + player['H']
								TotalCatabip += player['IP']
							elif cat == "W":
								TotalCat += player['W'] - player['L']
							elif cat == "K":
								TotalCat += player['K'] - player['BB']
							else:
								TotalCat += player[cat]
				if cat == "ERA":
					TotalCat = (TotalCat / TotalCatabip) * 9
					TotalCat = float("{:.2f}".format(TotalCat))
					catDict.update({team['TeamName']: TotalCat})
				elif cat == "WHIP":
					TotalCat = TotalCat / TotalCatabip
					TotalCat = float("{:.3f}".format(TotalCat))
					catDict.update({team['TeamName']: TotalCat})
				else:
					catDict.update({team['TeamName']: round(TotalCat)})
				TotalCat = 0
				TotalCatabip = 0
	else:
		pos_aryh = ['C1', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C2', 'UT1', 'UT2', 'UT3', 'UT4', 'UT5', 'UT6']
		pos_aryp = ['SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'RP1', 'RP2', 'RP3', 'RP4', 'RP5']
		for team in league:
			for key in pos_aryh:
				for player in hitters:
					if team[key] == player['ID']:
						TotalCat += player['Price']
			for key in pos_aryp:
				for player in pitchers:
					if team[key] == player['ID']:
						TotalCat += player['Price']
			TotalCat = TotalCat / 25
			catDict.update({team['TeamName']: round(TotalCat)})

	return catDict


def fantasyTable(league, hitters, pitchers, standings_dict, cat, btype, label, numteams):
	DictH = sortTeamCat(league, hitters, pitchers, cat, btype)
	if label != "Defense" and label != "ERA" and label != "WHIP" and label != "StrikeoutsH":
		DictH = dict(sorted(DictH.items(), key=lambda item: item[1], reverse=True))
	else: 
		DictH = dict(sorted(DictH.items(), key=lambda item: item[1]))
	htmlcode = "<td><ol>"
	for k,v in DictH.items():
		standings_dict[k] += numteams
		htmlcode += f"<li>{k}: {v}</li>"
		numteams -= 1
	htmlcode += "</ol></td>"
	return htmlcode, standings_dict


def inCodeFantasyTable(league, hitters, pitchers, numteams, standings_dict):
	DictHR = sortTeamCat(league, hitters, pitchers, "R", "H")
	DictHR = dict(sorted(DictHR.items(), key=lambda item: item[1], reverse=True))
	listHR = list(DictHR.items())
	DictHHR = sortTeamCat(league, hitters, pitchers, "HR", "H")
	DictHHR = dict(sorted(DictHHR.items(), key=lambda item: item[1], reverse=True))
	listHHR = list(DictHHR.items())
	DictHRBI = sortTeamCat(league, hitters, pitchers, "RBI", "H")
	DictHRBI = dict(sorted(DictHRBI.items(), key=lambda item: item[1], reverse=True))
	listHRBI = list(DictHRBI.items())
	DictHSB = sortTeamCat(league, hitters, pitchers, "SB", "H")
	DictHSB = dict(sorted(DictHSB.items(), key=lambda item: item[1], reverse=True))
	listHSB = list(DictHSB.items())
	DictHK = sortTeamCat(league, hitters, pitchers, "K", "H")
	DictHK = dict(sorted(DictHK.items(), key=lambda item: item[1]))
	listHK = list(DictHK.items())
	DictHOPS = sortTeamCat(league, hitters, pitchers, "OPS", "H")
	DictHOPS = dict(sorted(DictHOPS.items(), key=lambda item: item[1], reverse=True))
	listHOPS = list(DictHRBI.items())
	DictHD = sortTeamCat(league, hitters, pitchers, "Defense", "H")
	DictHD = dict(sorted(DictHD.items(), key=lambda item: item[1]))
	listHD = list(DictHRBI.items())
	
	table = []
	row = ["Runs", "Home Runs", "RBI", "SB/CS", "K/BB", "OPS", "Defense"]
	table.append(row)
	for i in range(numteams):
		row = []
		# For each dictionary list, add the key-value pair if available
		if i < len(listHR):
			row.append(f'{i+1}: {listHR[i][0]} {listHR[i][1]}')
		else:
			row.append(('N/A', 'N/A'))  # Placeholder if the index doesn't exist

		if i < len(listHHR):
			row.append(f'{i+1}: {listHHR[i][0]} {listHHR[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		if i < len(listHRBI):
			row.append(f'{i+1}: {listHRBI[i][0]} {listHRBI[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		if i < len(listHSB):
			row.append(f'{i+1}: {listHSB[i][0]} {listHSB[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		if i < len(listHK):
			row.append(f'{i+1}: {listHK[i][0]} {listHK[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		if i < len(listHOPS):
			row.append(f'{i+1}: {listHOPS[i][0]} {listHOPS[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		if i < len(listHD):
			row.append(f'{i+1}: {listHD[i][0]} {listHD[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		table.append(row)
	row = ["-------", "-------", "-------", "-------", "-------", "-------", "-------"]
	table.append(row)
	DictPW = sortTeamCat(league, hitters, pitchers, "W", "P")
	DictPW = dict(sorted(DictPW.items(), key=lambda item: item[1], reverse=True))
	listPW = list(DictPW.items())
	DictPK = sortTeamCat(league, hitters, pitchers, "K", "P")
	DictPK = dict(sorted(DictPK.items(), key=lambda item: item[1], reverse=True))
	listPK = list(DictPK.items())
	DictPSHO = sortTeamCat(league, hitters, pitchers, "SHO", "P")
	DictPSHO = dict(sorted(DictPSHO.items(), key=lambda item: item[1], reverse=True))
	listPSHO = list(DictPSHO.items())
	DictPSV = sortTeamCat(league, hitters, pitchers, "SV", "P")
	DictPSV = dict(sorted(DictPSV.items(), key=lambda item: item[1], reverse=True))
	listPSV = list(DictPSV.items())
	DictPERA = sortTeamCat(league, hitters, pitchers, "ERA", "P")
	DictPERA = dict(sorted(DictPERA.items(), key=lambda item: item[1]))
	listPERA = list(DictPERA.items())
	DictPWHIP = sortTeamCat(league, hitters, pitchers, "WHIP", "P")
	DictPWHIP = dict(sorted(DictPWHIP.items(), key=lambda item: item[1]))
	listPWHIP = list(DictPWHIP.items())
	DictPrice = sortTeamCat(league, hitters, pitchers, "Price", "P")
	DictPrice = dict(sorted(DictPrice.items(), key=lambda item: item[1], reverse=True))
	listPrice = list(DictPrice.items())
	row = ["W/L", "Strikeouts", "Shutouts", "Saves", "ERA", "WHIP", "Price"]
	table.append(row)
	for i in range(numteams):
		row = []
		# For each dictionary list, add the key-value pair if available
		if i < len(listPW):
			row.append(f'{i+1}: {listPW[i][0]} {listPW[i][1]}')
		else:
			row.append(('N/A', 'N/A'))  # Placeholder if the index doesn't exist

		if i < len(listPK):
			row.append(f'{i+1}: {listPK[i][0]} {listPK[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		if i < len(listPSHO):
			row.append(f'{i+1}: {listPSHO[i][0]} {listPSHO[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		if i < len(listPSV):
			row.append(f'{i+1}: {listPSV[i][0]} {listPSV[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		if i < len(listPERA):
			row.append(f'{i+1}: {listPERA[i][0]} {listPERA[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		if i < len(listPWHIP):
			row.append(f'{i+1}: {listPWHIP[i][0]} {listPWHIP[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		if i < len(listPrice):
			row.append(f'{i+1}: {listPrice[i][0]} {listPrice[i][1]}')
		else:
			row.append(('N/A', 'N/A'))

		table.append(row)

	print(tabulate(table))
	input("Press any key to view the overall scores")
	print("----------------------------------------")
	for k,v in standings_dict.items():
		print(f'{k}: {v}')
	print("----------------------------------------")
	print("")
	print("")

def pitcherSideCheck(league, standings_dict, pitchers):
	pitch_ary = ['SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'RP1', 'RP2', 'RP3', 'RP4', 'RP5']
	rightCount = 0
	leftCount = 0
	for team in league:
		for key in pitch_ary:
			playerid = team[key]
			for record in pitchers:
				if playerid == record['ID']:
					if record['Throw'] == "R":
						rightCount += 1
					else:
						leftCount += 1
		if rightCount < 2 or leftCount < 2:
			skey = team['TeamName']
			standings_dict[skey] -= 5
		rightCount = 0
		leftCount = 0
	return standings_dict



def teamHTML(team, hitters, pitchers, endchoice, salaryCap):
	table = [[1, 2222, 30, 500], [4, 55, 6777, 1]]
	pos_ary = ['C1', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C2', 'UT1', 'UT2', 'UT3', 'UT4', 'UT5', 'UT6']
	if salaryCap:
		htmlcode = "<h3>" + team['TeamName'] + " - " + str(team['Salary']) + " left" + "</h3>"
	else:
		htmlcode = "<h3>" + team['TeamName'] + "</h3>"
	htmlcode += f"<table id='{team['TeamID']}'><caption>Hitters</caption>"
	htmlcode += "<tr><th>Name</th><th>Position</th><th>Team</th><th>Bat</th><th>Fielding</th><th>Arm</th><th>G</th>"
	htmlcode += "<th>AB</th><th>R</th><th>H</th><th>2B</th><th>3B</th><th>HR</th><th>RBI</th><th>K</th><th>BB</th><th>SB</th><th>CS</th><th>Avg</th>"
	htmlcode += "<th>OBP</th><th>SLG</th><th>Price</th></tr>"
	table = [["Name","Position","Team","Bat","Fielding","Arm",
			"G","AB","R","H","2B","3B",
			"HR","RBI","K","BB","SB","CS",
			"Avg","OBP","SLG","Price"]]
	for key in pos_ary:
		for player in hitters:
			if team[key] == player['ID']:
				grade = alltimedraft.fieldGrade(player['DR1'])
				player_values = [
					key, player['Team'],
					player['Bat'], grade, player['Arm'], player['G'],
					player['AB'], player['R'], player['H'], player['2B'],player['3B'],
					player['HR'], player['RBI'], player['K'], player['BB'], player['SB'], player['CS'], player['Avg'],
					player['OBP'], player['SLG'], player['Price']
					]
				htmlcode += f"<tr><td>{player['FirstName']} {player['LastName']}</td><td>{'</td><td>'.join(map(str, player_values))}</td></tr>"
				fullname = player['FirstName'] + " " + player['LastName']

				playerrow = [key,fullname,player['Team'],player['Bat'],grade,player['Arm'],
				player['G'],player['AB'],player['R'],player['H'],player['2B'],player['3B'],
				player['HR'],player['RBI'],player['K'],player['BB'],player['SB'],player['CS'],
				player['Avg'],player['OBP'],player['SLG'],player['Price']]

				table.append(playerrow)
	htmlcode += "</table>"
	seprow = ["---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---",]
	table.append(seprow)
	pos_ary = ['SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'RP1', 'RP2', 'RP3', 'RP4', 'RP5']
	htmlcode += f"<table><caption>Pitchers</caption>"
	htmlcode += "<tr><th>Name</th><th>Position</th><th>Team</th><th>Throw</th><th>Role</th><th>G</th><th>GS</th>"
	htmlcode += "<th>SHO</th><th>W</th><th>L</th><th>SV</th><th>IP</th><th>H</th><th>ER</th><th>HR</th><th>BB</th><th>K</th>"
	htmlcode += "<th>ERA</th><th>WHIP</th><th>Price</th></tr>"
	pitcherheadrow = ["Name","Position","Team","Throw","Role",
					"G","GS","CG","W","L","SV",
					"IP","H","ER","HR","BB","K",
					"ERA","WHIP","Price"]
	table.append(pitcherheadrow)
	for key in pos_ary:
		for player in pitchers:
			if team[key] == player['ID']:
				player_values = [
					key, player['Team'],
					player['Throw'], player['Role'], player['G'], player['GS'],
					player['SHO'], player['W'], player['L'], player['SV'],
					player['IP'], player['H'], player['ER'], player['HR'], player['BB'],
					player['K'], player['ERA'], player['WHIP'], player['Price']
					]
				htmlcode += f"<tr><td>{player['FirstName']} {player['LastName']}</td><td>{'</td><td>'.join(map(str, player_values))}</td></tr>"
				fullname = player['FirstName'] + " " + player['LastName']

				playerrow = [key,fullname,player['Team'],player['Throw'],player['Role'],
							player['G'],player['GS'],player['SHO'],player['W'],player['L'],player['SV'],
							player['IP'],player['H'],player['ER'],player['HR'],player['BB'],player['K'],
							player['ERA'],player['WHIP'],player['Price']]

				table.append(playerrow)
	htmlcode += "</table><p><hr><p>"
	if endchoice == 1 or endchoice == 3:
		if salaryCap:
			print(f"{team['TeamName']} - Roster - {team['Salary']} left")
		else:
			print(f"{team['TeamName']} - Roster")
		print(tabulate(table))
	return htmlcode


def getLogFormat(league, hitters, pitchers, team_ary, selected_ary, numteams):
	htmlcode = "<div id='log'>"
	counter = 0
	rdCounter = 1
	rdLabel = 1
	overallCounter = 0
	htmlcode += f"---- Round {rdLabel} ----<br>"
	for pick in selected_ary:
		if rdCounter > numteams:
			rdLabel += 1
			htmlcode += f"---- Round {rdLabel} ----<br>"
			rdCounter = 1
		for player in hitters:
			if pick == player['ID']:
				name = player['FirstName'] + " " + player['LastName']
				position = alltimedraft.posConvert(player['DP1'])
		for player in pitchers:
			if pick == player['ID']:
				name = player['FirstName'] + " " + player['LastName']
				position = alltimedraft.posConvert(player['Role'])
		htmlcode += f"{overallCounter + 1}. {team_ary[overallCounter]}: {position} - {name}<br>"
		overallCounter += 1
		rdCounter += 1
		counter += 1
	htmlcode += "</div>"
	return htmlcode



