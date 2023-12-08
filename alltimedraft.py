import os
import json
import requests
import sys
import time
import random
import alltime_lib
import aipicks
import webbrowser

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

def inputCheck(initial, rangelow, rangehigh):
	#Ensures the user puts in a value that is legit (an integer) and withen the range asked for.
	desired_value = input(initial)
	while not desired_value.isdigit():
		desired_value = input(f"Please select a number. {initial} ")
	desired_value = int(desired_value)
	while desired_value > rangehigh or desired_value < rangelow:
		desired_value = input(f"Out of the provided range. {initial} ")
		while not desired_value.isdigit():
			desired_value = input(f"Please select a number. {initial} ")
		desired_value = int(desired_value)
	return desired_value
	
def hitterOrPitcher(hitters, pitchers, playerid):
	for player in hitters:
		if player["ID"] == playerid:
			return "H"
	for player in pitchers:
		if player["ID"] == playerid:
			return "P"
	return "X"	
	
	
def posConvert(pos):
	match pos:
		case "2":
			return "C"
		case "3":
			return "1B"
		case "4":
			return "2B"
		case "5":
			return "3B"
		case "6":
			return "SS"
		case "7":
			return "LF"
		case "8":
			return "CF"
		case "9":
			return "RF"
		case "S":
			return "SP"
		case "R":
			return "RP"
		case _:
			return ""



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
	pitchers = alltime_lib.gatherPlayers(pitchersjsonfile, "P")
	hitters = alltime_lib.gatherPlayers(hittersjsonfile, "H")
	time.sleep(3)	
	
	#Asks how many teams will be drafting.
	clearScreen()
	numteams = inputCheck("How many teams?  ", 1, 30)
	print (f"Great! {numteams} teams will draft!")
	
	#Now asks for how many players are human
	humannum = inputCheck("How many human players?  ", 0, numteams)
	
	
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
	league = alltime_lib.setUpTeams(numteams, randomDraft, humannum)		
	
	
	#Starts the Draft Counter
	draftcounter = 1
	draftSlotNum = 1
	direction = "Up"
	roundCounter = 1
	enddraft = False
	
	#Gathers up the teams in a draft log array carrying the team['DraftSlot'] integers in proper order.
	draftlog = alltime_lib.getDraftLog(league, numteams)
	
	while (numteams * 25) > draftcounter:
		if (draftcounter % numteams) == 1:
			print("")
			print("Round {} Started!".format(roundCounter))
			print("------------")
			roundCounter += 1
		humanbool = alltime_lib.draftOrderAnnounce(league, draftSlotNum)
		#When a Human Picks
		if humanbool:
			choice = 0
			select = 0

			while choice == 0:
				player_to_draft = 0
				choice = alltime_lib.draftMenu()
				clearScreen()
				if choice == 1:
					select = alltime_lib.getDraftPool(hitters, pitchers, "H", "Price", selected_list)
					if select > 0:
						clearScreen()
						player_to_draft = alltime_lib.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0
					
					
				if choice == 2:
					select = alltime_lib.getDraftPool(hitters, pitchers, "P", "Price", selected_list)
					if select > 0:
						clearScreen()
						player_to_draft = alltime_lib.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0


				if choice == 3:
					select = alltime_lib.viewTeam(league, hitters, pitchers, draftSlotNum, enddraft)
					if select > 0:
						clearScreen()
						select = alltime_lib.playerDetails(hitters, pitchers, select, True)
					else:
						choice = 0
				
					
				if choice == 4:
					select = alltime_lib.viewOtherTeamList(league, numteams, draftSlotNum)
					if select > 0:
						choice = alltime_lib.viewTeam(league, hitters, pitchers, select, enddraft)
						if choice > 0:
							clearScreen()
							player_to_draft = alltime_lib.playerDetails(hitters, pitchers, select, True)
					else:
						choice = 0
				
				if choice == 5:
					clearScreen()
					select = alltime_lib.getLog(league, hitters, pitchers, draftlog, selected_list, numteams)
					choice = 0				
			

				if choice == 6:
					select = alltime_lib.searchPlayer(hitters, pitchers, False)
					if select == 1:
						select = alltime_lib.searchPlayer(hitters, pitchers, True)
					if select > 0:
						clearScreen()
						player_to_draft = alltime_lib.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0

				if choice == 7:
					select = alltime_lib.getDraftPool(hitters, pitchers, "H", "Position", selected_list)
					if select > 0:
						clearScreen()
						player_to_draft = alltime_lib.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0


				if choice == 8:
					sortvalue = alltime_lib.sortListMenu()
					
					if sortvalue == "H" or sortvalue == "R" or sortvalue == "HHR" or sortvalue == "RBI" or sortvalue == "HBB" or sortvalue == "HK" or sortvalue == "SB" or sortvalue == "Avg" or sortvalue == "OBP" or sortvalue == "SLG":
						select = alltime_lib.getDraftPool(hitters, pitchers, "H", sortvalue, selected_list)
					else:
						select = alltime_lib.getDraftPool(hitters, pitchers, "P", sortvalue, selected_list)
						
					if select > 0:
						clearScreen()
						player_to_draft = alltime_lib.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0
						
				if choice == 9:
					exit()

				if player_to_draft == 0:
					choice = 0
				else:
					selected_position = alltime_lib.selectPlayer(league, hitters, pitchers, player_to_draft, draftSlotNum)
					if selected_position != "None":
						league = alltime_lib.assignToRoster(league, hitters, pitchers, player_to_draft, draftSlotNum, selected_position)
						selected_list.append(player_to_draft)
					else:
						choice = 0
	


					
	#When the AI Picks
		else:
			aiPickSuccess = False
			while not aiPickSuccess:
				player_to_draft = aipicks.aiSelect(league, hitters, pitchers, selected_list, draftSlotNum, roundCounter)
				selected_position = alltime_lib.selectPlayer(league, hitters, pitchers, player_to_draft, draftSlotNum)
				if selected_position != "None":
					league = alltime_lib.assignToRoster(league, hitters, pitchers, player_to_draft, draftSlotNum, selected_position)
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
		newDraftSlotNum = alltime_lib.draftOrderIncrement(draftSlotNum, numteams, direction)
		if draftSlotNum == newDraftSlotNum:
			if direction == "Up":
				direction = "Down"
			else:
				direction = "Up"
		else:
			draftSlotNum = newDraftSlotNum
		draftcounter += 1


	htmlcode = "<html><body>"
	htmlcode += "<style>caption {font-weight: bold;font-size: 14px;}table{font-family: Arial, Helvetica, sans-serif;"
	htmlcode += "border-collapse: collapse;width: 100%;font-size: 12px;}th {padding-top: 4px;padding-bottom: 4px;"
	htmlcode += "text-align: left;font-weight: bold;}tr:nth-child(even){background-color: #f2f2f2;}tr:hover {background-color: #ddd;}"
	htmlcode += "</style></head>"
	for team in league:
		enddraft = True
		print("Showing Rosters")
		choice = alltime_lib.viewTeam(league, hitters, pitchers, team['DraftSlot'], enddraft)
		input("Press any key to advance to the next team")
		print("---------------------------")
		htmlcode += alltime_lib.teamHTML(team, hitters, pitchers)

	htmlcode += alltime_lib.getLogFormat(league, hitters, pitchers, draftlog, selected_list, numteams)
	htmlcode += "</body></html>"


	with open('alltimedraft.html', 'w') as f:
		f.write(htmlcode)

	webbrowser.open('alltimedraft.html')