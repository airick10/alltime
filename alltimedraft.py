import os
import json
import requests
import sys
import time
import random
import alltime_lib
import aipicks
import webbrowser
import wget

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

def fieldGrade(rating):
	match rating:
		case "1":
			return "A"
		case "2":
			return "B"
		case "3":
			return "C"
		case "4":
			return "D"
		case "5":
			return "F"
		case _:
			return "F"



if __name__ == "__main__":
	file_path = 'log.txt'
	try:
		os.remove(file_path)
	except FileNotFoundError:
		print(f"The file {file_path} does not exist.")
	clearScreen()
	print("Welcome to the All Time Draft!  Gathering players...")
	#Takes in the file either submitted by the user or the default.  TO DO
	pitchersjsonfile = 'pitchers.json'
	hittersjsonfile = 'hitters.json'
	if not os.path.exists(pitchersjsonfile):
		url = 'http://www.rontoe.com/pitchers.json'
		output_path = 'pitchers.json'
		try:
			pitchersjsonfile = wget.download(url, out=output_path)
		except Exception as e:
			print(f"File Download Error: {e}")
	if not os.path.exists(hittersjsonfile):
		url = 'http://www.rontoe.com/hitters.json'
		output_path = 'hitters.json'
		try:
			hittersjsonfile = wget.download(url, out=output_path)
		except Exception as e:
			print(f"File Download Error: {e}")

	selected_list = []
	
	#Calls two functions.  gatherPitchers and gatherHitters.  Takes the string of the file location
	#as the parameter.  The functions will extract the json data and put them into lists for use
	#throughout this program.
	pitchers = alltime_lib.gatherPlayers(pitchersjsonfile, "P")
	hitters = alltime_lib.gatherPlayers(hittersjsonfile, "H")
	time.sleep(3)	
	
	input("""
This program allows you to draft a all time team of 25 players (15 hitters/10 pitchers).
At the end of the draft, teams will evaluated against each other using rotisserie baseball style standings.
The stats used to calcuate are:

Hitters: Runs, Home Runs, RBI, SB (minus CS), Strikeouts (minus BB), Team OPS, and Team Defense rating
Pitchers: Wins (minus L), Strikeouts, Shutouts, Saves, Team ERA, Team WHIP
And also the total Price of the player.

Standings are determined by ranked order in each category and compiled together for a final total.

Keep in mind, counting stats for hitters (Runs, HR, RBI, etc...) will receive the full amount for starting players
and only half the amount if the player is on the bench.

Also, pitching staffs with all pitchers throwing from one side (with one pitcher exception) will be penalized 5 points.

Have fun and good luck!

Press Enter to continue
""")

	#Asks how many teams will be drafting.
	clearScreen()
	numteams = inputCheck("How many teams? (Max: 30)  ", 1, 30)
	print (f"Great! {numteams} teams will draft!")
	
	#Now asks for how many players are human
	print("")
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
	salCapCheck = input("Press 'Y' if you want a $200 salary cap.  Press Enter for a straight draft  ")
	if salCapCheck == "Y" or salCapCheck == "y":
		salaryCap = True
	else:
		salaryCap = False
	
	#Starts the Draft Counter
	draftcounter = 1
	draftSlotNum = 1
	direction = "Up"
	roundCounter = 1
	
	#Gathers up the teams in a draft log array carrying the team['DraftSlot'] integers in proper order.
	draftlog = alltime_lib.getDraftLog(league, numteams)
	
	while (numteams * 25) >= draftcounter:
		if (draftcounter % numteams) == 1:
			with open('log.txt', 'a') as file:
				file.write("" + '\n')
				file.write("Round {} Started!".format(roundCounter) + '\n')
				file.write("------------" + '\n')
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
					select = alltime_lib.getDraftPool(hitters, pitchers, "H", "None", selected_list, salaryCap)
					if select > 0:
						clearScreen()
						player_to_draft = alltime_lib.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0
					
					
				if choice == 2:
					select = alltime_lib.getDraftPool(hitters, pitchers, "P", "None", selected_list, salaryCap)
					if select > 0:
						clearScreen()
						player_to_draft = alltime_lib.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0


				if choice == 3:
					select = alltime_lib.viewTeam(league, hitters, pitchers, draftSlotNum, salaryCap)
					if select > 0:
						clearScreen()
						select = alltime_lib.playerDetails(hitters, pitchers, select, True)
					else:
						choice = 0
				
					
				if choice == 4:
					select = alltime_lib.viewOtherTeamList(league, numteams, draftSlotNum)
					if select > 0:
						choice = alltime_lib.viewTeam(league, hitters, pitchers, select, salaryCap)
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
					select = alltime_lib.searchPlayer(hitters, pitchers, selected_list, False)
					if select == 1:
						select = alltime_lib.searchPlayer(hitters, pitchers, selected_list, True)
					if select > 0:
						clearScreen()
						player_to_draft = alltime_lib.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0

				if choice == 7:
					select = alltime_lib.getDraftPool(hitters, pitchers, "H", "Position", selected_list, salaryCap)
					if select > 0:
						clearScreen()
						player_to_draft = alltime_lib.playerDetails(hitters, pitchers, select, False)
					else:
						choice = 0


				if choice == 8:
					sortvalue = alltime_lib.sortListMenu()
					
					if sortvalue == "None":
						select = alltime_lib.getDraftPool(hitters, pitchers, "H", "None", selected_list, salaryCap)
					elif sortvalue == "H" or sortvalue == "R" or sortvalue == "HHR" or sortvalue == "RBI" or sortvalue == "HBB" or sortvalue == "HK" or sortvalue == "SB" or sortvalue == "Avg" or sortvalue == "OBP" or sortvalue == "SLG":
						select = alltime_lib.getDraftPool(hitters, pitchers, "H", sortvalue, selected_list, salaryCap)
					else:
						select = alltime_lib.getDraftPool(hitters, pitchers, "P", sortvalue, selected_list, salaryCap)
						
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
					selected_position = alltime_lib.selectPlayer(league, hitters, pitchers, player_to_draft, draftSlotNum, salaryCap)
					if selected_position != "None":
						league = alltime_lib.assignToRoster(league, hitters, pitchers, player_to_draft, draftSlotNum, selected_position)
						selected_list.append(player_to_draft)
					else:
						choice = 0
	


					
	#When the AI Picks
		else:
			aiPickSuccess = False
			while not aiPickSuccess:
				player_to_draft = aipicks.aiSelect(league, hitters, pitchers, selected_list, draftSlotNum, roundCounter, salaryCap)
				selected_position = alltime_lib.selectPlayer(league, hitters, pitchers, player_to_draft, draftSlotNum, salaryCap)
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

# AFTER THE DRAFT
	standings_dict = {}  # Create an empty dictionary

	for team in league:
		key = team['TeamName']
		standings_dict[key] = 0
	htmlcode = "<html><body>"
	htmlcode += "<style>caption {font-weight: bold;font-size: 14px;}table{font-family: Arial, Helvetica, sans-serif;"
	htmlcode += "border-collapse: collapse;width: 100%;font-size: 12px;}th {padding-top: 4px;padding-bottom: 4px;"
	htmlcode += "text-align: left;font-weight: bold;}tr:nth-child(even){background-color: #f2f2f2;}tr:hover {background-color: #ddd;}"
	htmlcode += "</style></head><body><a href='#log'>Draft Log</a><p>"
	htmlcode += "<table><caption>Standings</caption><th title='Total Runs'>R</th><th title='Total Home Runs'>HR</th><th title='Total RBI'>RBI</th><th title='Takes Steals minus Caught Totals'>SB/CS</th><th title='Total Strikeouts minus Walks'>K/BB</th><th title='Total Team OPS'>OPS</th><th  title='Measures best defense ratings'>Defense</th>"
	htmlcode += "<tr>"
	
	returned_html1, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "R", "H", "Runs", numteams)
	returned_html2, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "HR", "H", "Home Runs", numteams)
	returned_html3, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "RBI", "H", "RBI", numteams)
	returned_html4, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "SB", "H", "Steals", numteams)
	returned_html5, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "K", "H", "StrikeoutsH", numteams)
	returned_html6, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "OPS", "H", "OPS", numteams)
	returned_html7, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "Defense", "H", "Defense", numteams)
	htmlcode = htmlcode + returned_html1 + returned_html2 + returned_html3 + returned_html4 + returned_html5 + returned_html6 + returned_html7
	htmlcode += "</tr></table>"
	htmlcode += "<table><th title='Takes Wins minus Losses Total'>W/L</th><th title='Total Strikeouts Minus Walks'>Strikeouts</th><th title='Total Shutouts'>Shutouts</th><th title='Total Saves'>Saves</th><th title='Total Team ERA'>ERA</th><th title='Total Team WHIP'>WHIP</th><th title='Total Average Salary'>Price</th><tr>"
	returned_html1, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "W", "P", "Wins", numteams)
	returned_html2, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "K", "P", "Strikeouts", numteams)
	returned_html3, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "SHO", "P", "Shutouts", numteams)
	returned_html4, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "SV", "P", "Saves", numteams)
	returned_html5, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "ERA", "P", "ERA", numteams)
	returned_html6, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "WHIP", "P", "WHIP", numteams)
	returned_html7, standings_dict = alltime_lib.fantasyTable(league, hitters, pitchers, standings_dict, "Price", "P", "Price", numteams)
	htmlcode = htmlcode + returned_html1 + returned_html2 + returned_html3 + returned_html4 + returned_html5 + returned_html6 + returned_html7
	htmlcode += "</tr></table><p><hr><p>"
	standings_dict = alltime_lib.pitcherSideCheck(league, standings_dict, pitchers)
	standings_dict = dict(sorted(standings_dict.items(), key=lambda item: item[1], reverse=True))
	htmlcode += "<h3>Complete Standings:</h3><p><ol>"
	for k,v in standings_dict.items():
		htmlcode += f"<li>{k}: {v}</li>"
	htmlcode += "</ol>"
	print("The draft is complete!  How would you like to view the results?")
	print("1. View Rosters and Results here")
	print("2. View Rosters and Results in Web Browser")
	print("3. View Both")
	print("4. End Program")
	htmlOnce = True
	endchoice = inputCheck("Select an option  ", 1, 4)
	while endchoice < 4:
		for team in league:
			htmlcode += alltime_lib.teamHTML(team, hitters, pitchers, endchoice, salaryCap)
			if endchoice == 1 or endchoice == 3:
				input("Press any key to advance to the next team")
				clearScreen()

		if endchoice == 1 or endchoice == 3:
			alltime_lib.inCodeFantasyTable(league, hitters, pitchers, numteams, standings_dict)
			if endchoice == 3:
				input("Press any key to open up the web browser.  Note: Will end the program")

		if endchoice == 2 or endchoice == 3:
			htmlcode += alltime_lib.getLogFormat(league, hitters, pitchers, draftlog, selected_list, numteams)
			htmlcode += "</body></html>"
			if htmlOnce:
				finalcode = htmlcode
				htmlOnce = False
			with open('alltimedraft.html', 'w') as f:
				f.write(finalcode)
			webbrowser.open('alltimedraft.html')
			endchoice = 4

		if endchoice < 4:
			print("Would you like to view the results again?")
			print("1. View Results here")
			print("2. View Results in Web Browser")
			print("3. View Both")
			print("4. End Program")
			endchoice = inputCheck("Select an option  ", 1, 4)
