import inputcheck

def getDraftPoolList(id, firstName, lastName, year, team, choicearray, counter):
		print(f"{counter}. {firstName} {lastName} ({year}) - {team}")
		playerid = int(id)
		choicearray.append(playerid)
		return choicearray
		
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
		position_ary[0] = inputcheck.inputCheck("Select what option you want. Type 0 to ignore and go back. ", 0, 10)
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

def getDraftPool(hitters, pitchers, type, sortvalue, selected_list):
	#X is the number of players displayed at once.
	X = 30
	choicearray = [0]
	#hitters.sort(key=lambda x: x['Name'],reverse=True)
	
	#Gather records 30 - 60, for example.
	#for index, player in enumerate(hitters[30:60], start=30):
    #print(f"{index}. {player['Name']}, HR: {player['HR']}")
  
  #Counter actually measures the hitters/pitchers array and counts regardless of if a player is picked.  It keeps track of the actual source array.
  #Listcounter only increments when a player is available and gives the user a 1-30 choice.  Thus, the loop is based off that.
	counter = 1
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
		#for index, player in enumerate(hitters[:X]):
		while listcounter < 31 and len(hitters) > counter:	
			#Look for players who have not been drafted yet
			if hitters[counter]['ID'] not in selected_list:
				position[0] = str(position[0])
				if sortvalue == "Position":
					if hitters[counter]['DP1'] == position[0]:
						choicearray = getDraftPoolList(hitters[counter]['ID'], hitters[counter]['FirstName'], hitters[counter]['LastName'], hitters[counter]['Year'], hitters[counter]['Team'], choicearray, listcounter)
						listcounter += 1
				else:
					choicearray = getDraftPoolList(hitters[counter]['ID'], hitters[counter]['FirstName'], hitters[counter]['LastName'], hitters[counter]['Year'], hitters[counter]['Team'], choicearray, listcounter)
					listcounter += 1
			counter += 1
	else:
		#for index, player in enumerate(pitchers[:X]):
		while listcounter < 31 and len(pitchers) > counter:
			#Look for players who have not been drafted yet
			if pitchers[counter]['ID'] not in selected_list:
				if sortvalue == "Position":
					if pitchers[counter]['Role'] == position[0]:
						chiocearray = getDraftPoolList(pitchers[counter]['ID'], pitchers[counter]['FirstName'], pitchers[counter]['LastName'], pitchers[counter]['Year'], pitchers[counter]['Team'], choicearray, listcounter)
						listcounter += 1
				else:
					choicearray = getDraftPoolList(pitchers[counter]['ID'], pitchers[counter]['FirstName'], pitchers[counter]['LastName'], pitchers[counter]['Year'], pitchers[counter]['Team'], choicearray, listcounter)
					listcounter += 1
			counter += 1
	
	choice = inputcheck.inputCheck("Select the number for a player you want to see more details of.  Select 0 to go back to the menu.", 0, 30)
	return choicearray[choice]
	
	
	