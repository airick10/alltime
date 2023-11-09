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
	choice = inputcheck.inputCheck("Select what stat to sort. Type 0 to ignore and go back. ", 0, 20)
	match choice:
		case 0:
			return "Price"
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
			return "Price"
			
			
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



def getDraftPool(hitters, pitchers, type, sortvalue, selected_list):
	#X is the number of players displayed at once.
	X = 30
	choicearray = [0]
	if type == "H":
		hitters = sortList(hitters, sortvalue, "H")
	else:
		pitchers = sortList(pitchers, sortvalue, "P")
	
	
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
				#POSITION CHECK
				if sortvalue == "Position" and position[1]:
					position[0] = str(position[0])
					if hitters[counter]['DP1'] == position[0]:
						choicearray = getDraftPoolList(hitters[counter]['ID'], hitters[counter]['FirstName'], hitters[counter]['LastName'], hitters[counter]['Year'], hitters[counter]['Team'], choicearray, listcounter)
						listcounter += 1
				elif sortvalue == "Position" and not position[1]:
					if hitters[counter]['DP1'] == position[0] or hitters[counter]['DP2'] == position[0] or hitters[counter]['DP3'] == position[0] or hitters[counter]['DP4'] == position[0] or hitters[counter]['DP5'] == position[0] or hitters[counter]['DP6'] == position[0] or hitters[counter]['DP7'] == position[0] or hitters[counter]['DP8'] == position[0]:
						choicearray = getDraftPoolList(hitters[counter]['ID'], hitters[counter]['FirstName'], hitters[counter]['LastName'], hitters[counter]['Year'], hitters[counter]['Team'], choicearray, listcounter)
						listcounter += 1		
				#IF POSITION CHECK ISN'T SELECTED
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
	
	
	
