import os
import json
import requests
import sys
import time
import random
import optionsmenu
import inputcheck
import draftpool
import aipicks

def clearScreen():
    try:
        # For Windows
        if os.name == 'nt':
            _ = os.system('cls')
        # For POSIX systems (Mac and Linux)
        elif os.name == 'posix':
            _ = os.system('clear')
    except Exception:
        # Fall back to printing newlines if other methods fail
        print('\n' * 100)

'''
def clearScreen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Mac and Linux (os.name: 'posix')
    else:
        _ = os.system('clear')
'''
def gatherPlayers(jf, type):
	with open(jf) as fp:
		players = json.load(fp)
	if type == "H":
		for record in players:
			record["G"] = int(record["G"])
			record["AB"] = int(record["AB"])
			record["R"] = int(record["R"])
			record["H"] = int(record["H"])
			record["2B"] = int(record["2B"])
			record["3B"] = int(record["3B"])
			record["HR"] = int(record["HR"])
			record["RBI"] = int(record["RBI"])
			record["BB"] = int(record["BB"])
			record["K"] = int(record["K"])
			record["HB"] = int(record["HB"])
			record["SB"] = int(record["SB"])
			record["CS"] = int(record["CS"])
			record["Avg"] = float(record["Avg"])
			record["OBP"] = float(record["OBP"])
			record["SLG"] = float(record["SLG"])
			record["Price"] = int(record["Price"])
	else:
		for record in players:
			record["G"] = int(record["G"])
			record["GS"] = int(record["GS"])
			record["CG"] = int(record["CG"])
			record["SHO"] = int(record["SHO"])
			record["W"] = int(record["W"])
			record["L"] = int(record["L"])
			record["SV"] = int(record["SV"])
			record["IP"] = float(record["IP"])
			record["H"] = int(record["H"])
			record["ER"] = int(record["ER"])
			record["HR"] = int(record["HR"])
			record["BB"] = int(record["BB"])
			record["K"] = int(record["K"])
			record["WP"] = int(record["WP"])
			record["BK"] = int(record["BK"])
			record["ERA"] = float(record["ERA"])
			record["WHIP"] = float(record["WHIP"])
			record["Price"] = int(record["Price"])
	return players
	
def setUpTeams(numteams, randomDraft, humannum):
    league = [{} for _ in range(numteams)]
    teamnameary = []
    setHumanDraftSlot = [0]
    randomDraftOrder = []
    randomDraftOrder = optionsmenu.optionSetRandomDraft(numteams)
    if humannum > 0:
    	if not randomDraft:
    		setHumanDraftSlot = optionsmenu.optionSetDraftPosition(numteams, humannum)

    counter = 1
    draftCounter = 0
    aiSequenceSlot = 1
    for team in league:
        # TeamID
        team["TeamID"] = counter
        team["AIFocus"] = aiFocus()
        if humannum > 0: 
        	team["TeamName"] = input(f"Human Team {team['TeamID']}: What do you want for the team name? ")
        	team["Human"] = True
        	team["TeamName"] = team["TeamName"].capitalize()
        	while team["TeamName"] in teamnameary:
        		team["TeamName"] = input(f"Try again, team name already exists - Human Team {team['TeamID']}: What do you want for the team name? ")
        		team["TeamName"] = team["TeamName"].capitalize()
        	teamnameary.append(team["TeamName"])
        else:
        	team["TeamName"] = input(f"AI Team {team['TeamID']}: What do you want for the team name? ")
        	team["Human"] = False
        	team["TeamName"] = team["TeamName"].capitalize()
        	while team["TeamName"] in teamnameary:
        		team["TeamName"] = input(f"Try again, team name already exists - AI Team {team['TeamID']}: What do you want for the team name? ")
        		team["TeamName"] = team["TeamName"].capitalize()
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
	return draftLog
		
	
def viewTeam(league, hitters, pitchers, select, enddraft):
	counter = 0
	idSelected = False
	choicearray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#select is the DraftSlot.  That doesn't mean it's the TeamID slot.
	#This loop goes through League and captures the TeamID of the DraftSlot
	#Because an array starts at 0, I'm turning record['TeamID'] into an int and subtracting by 1.
	for record in league:
		if record['DraftSlot'] == select:
			print(f"{record['TeamName']} - {record['TeamID']}")
			teamid = int(record['TeamID']) - 1	
	#league[select]['C1']
	print("")
	#k = Key, v = Va	
	for k,v in league[teamid].items():
		empty_slot = True
		if k != "TeamID" and k != "DraftSlot" and k != "Human":
			if k == "TeamName":
				print(f"{v}")
				print("-------------")
				
			if "SP" not in k and "RP" not in k:
				for player in hitters:
					if player['ID'] == v:
						playerid = int(v)
						choicearray[counter] = v
						idSelected = True
						empty_slot = False
					if idSelected:
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
						print(f"{counter}. {k} - {player['FirstName']} {player['LastName']}")
					idSelected = False

			if empty_slot and k != "TeamName":
				print(f"{counter}. {k}")
			counter += 1
	
	if not enddraft:
		choice = inputcheck.inputCheck("Choose a player to view details.  Press 0 to go back to the Draft Menu ", 0, 27)
		while choicearray[choice] == 0 and choice != 0:
			choice = inputcheck.inputCheck("Player is unassigned at this slot.  Try again.  Choose a player to view details.  Press 0 to go back to the Draft Menu ", 0, 27)
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
				position = inputcheck.posConvert(player['DP1'])
		for player in pitchers:
			if pick == player['ID']:
				name = player['FirstName'] + " " + player['LastName']
				position = inputcheck.posConvert(player['Role'])
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














if __name__ == "__main__":
	clearScreen()
	print("Welcome to the All Time Draft!  Gathering players...")
	#Takes in the file either submitted by the user or the default.  TO DO
	#pitchersjsonfile = "/Users/eric/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/pythonista/Alltimeapp/pitchers.json"
	#hittersjsonfile = "/Users/eric/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/pythonista/Alltimeapp/hitters.json"
	pitchersjsonfile = 'pitchers.json'
	hittersjsonfile = 'hitters.json'
	selected_list = []
	
	#Calls two functions.  gatherPitchers and gatherHitters.  Takes the string of the file location
	#as the parameter.  The functions will extract the json data and put them into lists for use
	#throughout this program.
	pitchers = gatherPlayers(pitchersjsonfile, "P")
	hitters = gatherPlayers(hittersjsonfile, "H")
	time.sleep(3)	
	
	#Asks how many teams will be drafting.
	clearScreen()
	numteams = inputcheck.inputCheck("How many teams?  ", 1, 30)
	print (f"Great! {numteams} teams will draft!")
	
	#Now asks for how many players are human
	humannum = inputcheck.inputCheck("How many human players?  ", 0, numteams)
	
	
	#Checks if the user wants the draft order to be random or they set it
	setHumanDraftSlot = []
	if humannum > 0:		
		randomDraftCheck = input("Do you want the draft order to be random?  'Y' for yes and 'N' for no: ")
		print("")
		while randomDraftCheck != "Y" and randomDraftCheck != "y" and randomDraftCheck != "N" and randomDraftCheck != "n":
			randomDraftCheck = input("Try again, Do you want the draft order to be random?  'Y' for yes and 'N' for no: ")	
			print("")
		if randomDraftCheck == "N" or randomDraftCheck == "n":
			randomDraft = False
		else:
			randomDraft = True
	else:
		randomDraft = True
	
	
	#Creates the league array for all the teams and draft slots.
	league = setUpTeams(numteams, randomDraft, humannum)		
	
	
	#Starts the Draft Counter
	draftcounter = 1
	draftSlotNum = 1
	direction = "Up"
	roundCounter = 1
	enddraft = False
	
	#Gathers up the teams in a draft log array carrying the team['DraftSlot'] integers in proper order.
	draftlog = getDraftLog(league, numteams)
	
	while (numteams * 25) > draftcounter:
		if (draftcounter % numteams) == 1:
			print("")
			print("Round {} Started!".format(roundCounter))
			print("------------")
			roundCounter += 1
		humanbool = draftOrderAnnounce(league, draftSlotNum)
		#When a Human Picks
		if humanbool:
			choice = 0
			select = 0

			while choice == 0:
				player_to_draft = 0
				choice = optionsmenu.draftMenu()
				clearScreen()
				if choice == 1:
					select = draftpool.getDraftPool(hitters, pitchers, "H", "Price", selected_list)
					if select > 0:
						clearScreen()
						player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0
					
					
				if choice == 2:
					select = draftpool.getDraftPool(hitters, pitchers, "P", "Price", selected_list)
					if select > 0:
						clearScreen()
						player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0


				if choice == 3:
					select = viewTeam(league, hitters, pitchers, draftSlotNum, enddraft)
					if select > 0:
						clearScreen()
						select = optionsmenu.playerDetails(hitters, pitchers, select, True)
					else:
						choice = 0
				
					
				if choice == 4:
					select = optionsmenu.viewOtherTeamList(league, numteams, draftSlotNum)
					if select > 0:
						choice = viewTeam(league, hitters, pitchers, select, enddraft)
						if choice > 0:
							clearScreen()
							player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, True)
					else:
						choice = 0
				
				if choice == 5:
					clearScreen()
					select = getLog(league, hitters, pitchers, draftlog, selected_list, numteams)
					choice = 0				
			

				if choice == 6:
					select = optionsmenu.searchPlayer(hitters, pitchers, False)
					if select == 1:
						select = optionsmenu.searchPlayer(hitters, pitchers, True)
					if select > 0:
						clearScreen()
						player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0

				if choice == 7:
					select = draftpool.getDraftPool(hitters, pitchers, "H", "Position", selected_list)
					if select > 0:
						clearScreen()
						player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0


				if choice == 8:
					sortvalue = draftpool.sortListMenu()
					
					if sortvalue == "H" or sortvalue == "R" or sortvalue == "HHR" or sortvalue == "RBI" or sortvalue == "HBB" or sortvalue == "HK" or sortvalue == "SB" or sortvalue == "Avg" or sortvalue == "OBP" or sortvalue == "SLG":
						select = draftpool.getDraftPool(hitters, pitchers, "H", sortvalue, selected_list)
					else:
						select = draftpool.getDraftPool(hitters, pitchers, "P", sortvalue, selected_list)
						
					if select > 0:
						clearScreen()
						player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0
						
				if choice == 9:
					exit()

				if player_to_draft == 0:
					choice = 0
				else:
					selected_position = optionsmenu.selectPlayer(league, hitters, pitchers, player_to_draft, draftSlotNum)
					if selected_position != "None":
						league = optionsmenu.assignToRoster(league, hitters, pitchers, player_to_draft, draftSlotNum, selected_position)
						selected_list.append(player_to_draft)
					else:
						choice = 0
	


					
	#When the AI Picks
		else:
			aiPickSuccess = False
			while not aiPickSuccess:
				player_to_draft = aipicks.aiSelect(league, hitters, pitchers, selected_list, draftSlotNum, roundCounter)
				selected_position = optionsmenu.selectPlayer(league, hitters, pitchers, player_to_draft, draftSlotNum)
				if selected_position != "None":
					league = optionsmenu.assignToRoster(league, hitters, pitchers, player_to_draft, draftSlotNum, selected_position)
					selected_list.append(player_to_draft)
					aiPickSuccess = True
					print("")
		

		# After Pick
		'''Constructing draft order
	Start at 1 with the direction going up. Call the draftOrderIncrement function to increment or decrement
	the draft slot depending on direction.
	It returns the new (or already existing) draft slot depending if we are at the top or bottom of the direction
	If the returned draft slot is the same, we've reached the edge of the snake.  Check what the
	direction is and change it.  If the draft slot is not the same, simple assign the given slot to the official
	slot and move on.
	'''
		newDraftSlotNum = draftOrderIncrement(draftSlotNum, numteams, direction)
		if draftSlotNum == newDraftSlotNum:
			if direction == "Up":
				direction = "Down"
			else:
				direction = "Up"
		else:
			draftSlotNum = newDraftSlotNum
		draftcounter += 1


	for team in league:
		enddraft = True
		print("Showing Rosters")
		choice = viewTeam(league, hitters, pitchers, team['DraftSlot'], enddraft)
		input("Press any key to advance to the next team")
		print("---------------------------")