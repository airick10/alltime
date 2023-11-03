import os
import json
import requests
import sys
import time
import optionsmenu
import inputcheck
import draftpool


def gatherPlayers(jf):
	with open(jf) as fp:
		players = json.load(fp)
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
        #CHECK ON THIS.  OUT OF RANGE.  MAYBE DO A TRY/EXCEPT?
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
        team["DraftSlot"] = counter
        # Draft Slot
        if randomDraft:
        	team["DraftSlot"] = randomDraftOrder[draftCounter]
        if not randomDraft:
        	if team["Human"]:
        		team["DraftSlot"] = setHumanDraftSlot[draftCounter]
        	else:
        		while aiSequenceSlot in setHumanDraftSlot:
        			aiSequenceSlot += 1
        			team["DraftSlot"] = aiSequenceSlot
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
        team["UT7"] = "Unassigned"
        counter += 1
        humannum -= 1
        draftCounter += 1
        aiSequenceSlot += 1
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


				

def viewTeam(league, hitters, pitchers, select):
	counter = 0
	#select -= 1
	idSelected = False
	choicearray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#league[select]['C1']
	print("")
	#k = Key, v = Value
	for k,v in league[select].items():
		empty_slot = True
		if k != "TeamID" and k != "DraftSlot" and k != "Human":
			if k == "TeamName":
				print(f"{v}")
				print("-------------")
			if "SP" in k or "RP" in k:
				for player in hitters:
					if player['ID'] == v:
						playerid = int(v)
						choicearray[counter] = v
						idSelected = True
						empty_slot = False
					if idSelected:
						if player['FirstName'] == v:
							firstName = v
						if player['LastName'] == v:
							lastName = v
							idSelected = False
							#GETTING ERROR HERE -  KeyError: 'FirstName'
							print(f"{counter}. {k} - {firstName} {lastName}")
			else:
				for player in pitchers:
					if player['ID'] == v:
						playerid = int(v)
						choicearray[counter] = v
						idSelected = True
						empty_slot = False
					if idSelected:
						if player['FirstName'] == v:
							firstName = v
						if player['LastName'] == v:
							lastName = v
							idSelected = False
							#GETTING ERROR HERE -  KeyError: 'FirstName'
							print(f"{counter}. {k} - {firstName} {lastName}")

			if empty_slot and k != "TeamName":
				print(f"{counter}. {k}")
			counter += 1
	
	choice = inputcheck.inputCheck("Choose a player to view details.  Press 0 to go back to the Draft Menu ", 0, 27)
	while choicearray[choice] == 0 and choice != 0:
		choice = inputcheck.inputCheck("Player is unassigned at this slot.  Try again.  Choose a player to view details.  Press 0 to go back to the Draft Menu ", 0, 27)
	return choicearray[choice]
	
	

#--TO DO---


def selectPick(league, slotnum, playerid):
	for team in league:
		if team["DraftSlot"] == slotnum:
			print("Do Stuff")
			
#--TO DO END---			




if __name__ == "__main__":
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
	pitchers = gatherPlayers(pitchersjsonfile)
	hitters = gatherPlayers(hittersjsonfile)
	time.sleep(3)
	
	
	#Asks how many teams will be drafting.
	numteams = inputcheck.inputCheck("How many teams?", 1, 30)
	print ("Great! %s many teams will draft!" % (numteams))
	
	#Now asks for how many players are human
	humannum = inputcheck.inputCheck("How many human players?", 0, numteams)
	
	
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
	
	while (numteams * 25) > draftcounter:
		if (draftcounter % numteams) == 1:
			print("")
			print("Round {} Started!".format(roundCounter))
			print("------------")
			roundCounter += 1
		humanbool = draftOrderAnnounce(league, draftSlotNum)
		#When a Human Picks
		if humanbool:
			#print("Human Pick")
			choice = 0

			while choice == 0:
				player_to_draft = 0
				choice = optionsmenu.draftMenu()
				if choice == 1:
					select = draftpool.getDraftPool(hitters, pitchers, "H", "None", selected_list)
					if select > 0:
						player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0
					
					
				if choice == 2:
					select = draftpool.getDraftPool(hitters, pitchers, "P", "None", selected_list)
					if select > 0:
						player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0


				if choice == 3:
					select = viewTeam(league, hitters, pitchers, draftSlotNum)
					if select > 0:
						select = optionsmenu.playerDetails(hitters, pitchers, select, True)
					else:
						choice = 0
				
					
				if choice == 4:
					select = optionsmenu.viewOtherTeamList(league, numteams, draftSlotNum)
					if select > 0:
						choice = viewTeam(league, hitters, pitchers, select)
						if choice > 0:
							player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, True)
					else:
						choice = 0
				

				if choice == 6:
					select = optionsmenu.searchPlayer(hitters, pitchers, False)
					if select == 1:
						select = optionsmenu.searchPlayer(hitters, pitchers, True)
					if select > 0:
						player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0

				if choice == 7:
					select = draftpool.getDraftPool(hitters, pitchers, "H", "Position", selected_list)
					if select > 0:
						player_to_draft = optionsmenu.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0

					
				if choice == 9:
					sys.exit()

				if player_to_draft == 0:
					choice = 0
				else:
					optionsmenu.selectPlayer(league, hitters, pitchers, player_to_draft, draftSlotNum)
					selected_list.append(player_to_draft)


					
	#When the AI Picks
		else:
			print("AI Pick")
		
		
		
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
	
	
	
	
	

		

	'''
  #LOOK AT PLAYERS---
	print(pitchers)
	
	for player in hitters:
		if 'Name' in player:
			print(player['Name'], player['Bat'], player['Fielding'])
		else:
			print("")
			xxxx
	'''
