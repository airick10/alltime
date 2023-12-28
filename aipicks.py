from random import randrange
import alltime_lib
import random

# 0 - No Position Check
# 1 - Only pick a Starting Pitcher
# 2 - Only pick a Catcher
# 11 - Only pick a Relief Pitcher
# 13 - Left Handed Hitter/Pitcher
# 14 - Up the middle. Look for Catchers, 2nd base, Short, and CF
# 12 - Position Player position check (Looking for 1s on defense)

def aiSelectSnippet(log, playerpool, selected_list, threshold, defCheck, direction, avgSalary):
	defchecklog = f"DefCheck - {defCheck}"
	with open('log.txt', 'a') as file:
		file.write(log + '\n')
		file.write(defchecklog + '\n')
	#print(log)
	#print(f"DefCheck - {defCheck}")

    # Create a dictionary that maps defCheck values to corresponding lambda functions
	check_functions = {
        0: lambda player: True,
        1: lambda player: player['Role'] == "S",
        2: lambda player: player['DP1'] == "2" or player['DP2'] == "2" or player['DP3'] == "2", 
        3: lambda player: player['DP1'] == "3" or player['DP2'] == "3" or player['DP3'] == "3",
        4: lambda player: player['DP1'] == "4" or player['DP2'] == "4" or player['DP3'] == "4",
        5: lambda player: player['DP1'] == "5" or player['DP2'] == "5" or player['DP3'] == "5",
        6: lambda player: player['DP1'] == "6" or player['DP2'] == "6" or player['DP3'] == "6",
        7: lambda player: player['DP1'] == "7" or player['DP2'] == "7" or player['DP3'] == "7",
        8: lambda player: player['DP1'] == "8" or player['DP2'] == "8" or player['DP3'] == "8",
        9: lambda player: player['DP1'] == "9" or player['DP2'] == "9" or player['DP3'] == "9",
        10: lambda player: True,
        11: lambda player: player['Role'] == "R",
        12: lambda player: player['DR1'] == "1",
        13: lambda player: player.get('Bat', "") == "L" or player.get('Throw', "") == "L",
        14: lambda player: player['DP1'] in ("2", "4", "6", "8"),
        20: lambda player: player['DP1'] == "2" 
    }


    #So for each player in playerpool, check_functions[defCheck](player) calls the lambda function associated with the current defCheck value and checks the condition against that player. If the condition is met, it returns True; otherwise, it returns False.
	#For example:
    #If defCheck is 0, then check_functions[defCheck] is lambda player: True. When called with a player argument, it will always return True.
  	#If defCheck is 1, then check_functions[defCheck] is lambda player: player['DR1'] == "1". When called with a player argument, it will return True if player['DR1'] is equal to "1", otherwise False.
	counter = 0
	for player in playerpool:
		#print(player['LastName'])
		if player['ID'] not in selected_list and check_functions[defCheck](player):
			if player['Price'] > avgSalary:
				with open('log.txt', 'a') as file:
					file.write("**AI LOG** - Salary Fail" + '\n')
			else:
				if threshold < 0 or counter > threshold:
					return player['ID']
				counter += 1

	return None


def firstRounds(roll, hitters, pitchers, selected_list, position, avgSalary):
	avgSalary = 20000
	with open('log.txt', 'a') as file:
		file.write("**AI LOG** - Best Price" + '\n')
	#Putting the hitter pool in its own playerpool for the AI
	hproll = randrange(100)
	position_array = [0,1,0]
	if hproll < roll:
		with open('log.txt', 'a') as file:
			file.write("**AI LOG** - Hitter Selected" + '\n')
		playerpool = hitters.copy()
		with open('log.txt', 'a') as file:
			file.write("**AI LOG** - Best Price" + '\n')
		#playerpool = alltime_lib.sortList(playerpool, "Price", "H")
		player_to_select = topFourGrabs("H", playerpool, selected_list, position_array, 0, avgSalary)
	else:
		with open('log.txt', 'a') as file:
			file.write("**AI LOG** - Pitcher Selected" + '\n')
		playerpool = pitchers.copy()
		with open('log.txt', 'a') as file:
			file.write("**AI LOG** - Best Price" + '\n')
		#playerpool = alltime_lib.sortList(playerpool, "Price", "P")
		player_to_select = topFourGrabs("P", playerpool, selected_list, position_array, 0, avgSalary)
	return player_to_select


def topFourGrabs(type, playerpool, selected_list, position, direction, avgSalary):
	if type == "P":
		if direction == 1 and position[1] == 1:
			defCheck = 1
		elif direction == 11 and position[2] == 11:
			defCheck = 11
		else:
			defCheck = 0
	else:
		defCheck = position[0]

	newRoll = randrange(100)
	#If the roll is 0 - 39 (40%), don't apply a counter.  Just take the highest price.
	if newRoll < 40:
		if type == "H":
			player_to_select = aiSelectSnippet("**AI LOG** - 1st Hitter", playerpool, selected_list, -1, defCheck, direction, avgSalary)
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 1st Pitcher", playerpool, selected_list, -1, defCheck, direction, avgSalary)
	#If the roll is 40 - 69 (30%), apply a counter at 0.  The counter needs to be at 1 to take a player.
	#So the script will take the second best.
	elif newRoll < 70 and newRoll >= 40:
		if type == "H":
			player_to_select = aiSelectSnippet("**AI LOG** - 2nd Hitter", playerpool, selected_list, 0, defCheck, direction, avgSalary)
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 2nd Pitcher", playerpool, selected_list, 0, defCheck, direction, avgSalary)
	#If the roll is 70 - 89 (20%), apply a counter at 0.  The counter needs to be at 2 to take a player.
	#So the script will take the third best.				
	elif newRoll < 90 and newRoll >= 70:
		if type == "H":
			player_to_select = aiSelectSnippet("**AI LOG** - 3rd Hitter", playerpool, selected_list, 1, defCheck, direction, avgSalary)
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 3rd Pitcher", playerpool, selected_list, 1, defCheck, direction, avgSalary)
	#If the roll is 90 - 99 (10%), apply a counter at 0.  The counter needs to be at 3 to take a player.
	#So the script will take the second best.
	else:
		if type == "H":
			player_to_select = aiSelectSnippet("**AI LOG** - 4th Hitter", playerpool, selected_list, 2, defCheck, direction, avgSalary)
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 4th Pitcher", playerpool, selected_list, 2, defCheck, direction, avgSalary)

	return player_to_select


def autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary):
	sideThreshold = 50
	side = random.randrange(100)

	if roundCounter < 3:
		sideThreshold = 90

	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(30, hitters, pitchers, selected_list, position, avgSalary)
	elif side < sideThreshold:
		key_index = weighted_random_choice([0, 1, 2], [70, 20, 10])  # Weighted random choice for key_index
		key_str = keys[key_index]  # Select the key using the randomly chosen index
		logstr = f"**AI LOG** - Hitter Selected ({key_str})"
		with open('log.txt', 'a') as file:
			file.write(logstr + '\n')
		playerpool = hitters.copy()
		rolerandom = random.randrange(100)
		logstr = f"**AI LOG** - Category: {key_str}"
		with open('log.txt', 'a') as file:
			file.write(logstr + '\n')
		playerpool = alltime_lib.sortList(playerpool, key_str, "H")
		if focus < 15 and focus > 11:
			if randrange(100) < 65:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, focus, avgSalary)
			else:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0, avgSalary)
		else:
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, focus, avgSalary)
	else:
		key_index = weighted_random_choice([3, 4, 5], [70, 20, 10])  # Weighted random choice for key_index
		key_str = keys[key_index]  # Select the key using the randomly chosen index
		logstr = f"**AI LOG** - Pitcher Selected ({key_str})"
		with open('log.txt', 'a') as file:
			file.write(logstr + '\n')
		playerpool = pitchers.copy()
		rolerandom = random.randrange(100)
		if rolerandom < 80 and position[1] > 0:
			with open('log.txt', 'a') as file:
				file.write("**AI LOG** - Select Starting Pitcher" + '\n')
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1, avgSalary)
		else:
			with open('log.txt', 'a') as file:
				file.write("**AI LOG** - Select Relief Pitcher" + '\n')
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11, avgSalary)
	return player_to_select


def autoSelectPitcher(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary):
	sideThreshold = 50
	side = random.randrange(100)

	if roundCounter < 3:
		sideThreshold = 90

	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(30, hitters, pitchers, selected_list, position, avgSalary)
	elif side < sideThreshold:
		key_index = weighted_random_choice([0, 1, 2], [70, 20, 10])  # Weighted random choice for key_index
		key_str = keys[key_index]  # Select the key using the randomly chosen index
		logstr = f"**AI LOG** - Pitcher Selected ({key_str})"
		with open('log.txt', 'a') as file:
			file.write(logstr + '\n')
		playerpool = pitchers.copy()
		rolerandom = random.randrange(100)
		logstr = f"**AI LOG** - Category: {key_str}"
		with open('log.txt', 'a') as file:
			file.write(logstr + '\n')
		playerpool = alltime_lib.sortList(playerpool, key_str, "P")

		if rolerandom < 80 and position[1] > 0:
			with open('log.txt', 'a') as file:
				file.write("**AI LOG** - Select Starting Pitcher" + '\n')
			if focus == 13:
				if randrange(100) < 65:
					player_to_select = topFourGrabs("P", playerpool, selected_list, position, focus, avgSalary)
				else:
					player_to_select = topFourGrabs("P", playerpool, selected_list, position, 0, avgSalary)
			else:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1, avgSalary)
		else:
			with open('log.txt', 'a') as file:
				file.write("**AI LOG** - Select Relief Pitcher" + '\n')
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11, avgSalary)
	else:
		key_index = weighted_random_choice([3, 4, 5], [70, 20, 10])  # Weighted random choice for key_index
		key_str = keys[key_index]  # Select the key using the randomly chosen index
		logstr = f"**AI LOG** - Hitter Selected ({key_str})"
		with open('log.txt', 'a') as file:
			file.write(logstr + '\n')
		playerpool = hitters.copy()
		player_to_select = topFourGrabs("H", playerpool, selected_list, position, focus, avgSalary)

	return player_to_select


def weighted_random_choice(choices, weights):
	total_weight = sum(weights)
	threshold = random.uniform(0, total_weight)
	current_weight = 0
	
	for choice, weight in zip(choices, weights):
		current_weight += weight
		if current_weight >= threshold:
			return choice


def eligiblePosition(team):
	positions = {
    "C1": 2, "C2": 20, "1B": 3, "2B": 4, "3B": 5, 
    "SS": 6, "LF": 7, "CF": 8, "RF": 9, "UT1": 10, 
    "UT2": 10, "UT3": 10, "UT4": 10, "UT5": 10, "UT6": 10, 
    "SP1": 1, "SP2": 1, "SP3": 1, "SP4": 1, 
    "SP5": 1, "RP1": 11, "RP2": 11, "RP3": 11, "RP4": 11, 
    "RP5": 11
	}

	position_lottery = []
	

	for key, value in team.items():
		if key in positions:
			if value == "Unassigned" and value not in position_lottery:
				position_lottery.append(positions[key])

	selected_array = [0,0,0]
	selected_value = 0

	if 1 in position_lottery:
		selected_array[1] = 1
	if 11 in position_lottery:
		selected_array[2] = 11



	selected_value = random.choice(position_lottery)
	if all(val in [1, 11] for val in position_lottery):
		selected_value = 0
	else:
		while selected_value == 1 or selected_value == 11:
			selected_value = random.choice(position_lottery)
	selected_array[0] = selected_value
		
	
	if team['AIFocus'] == 15:
		if any(n in position_lottery for n in (8, 4, 6, 2)):
			while selected_array[0] not in (8, 4, 6, 2): 
				selected_array[0] = random.choice(position_lottery)

	if selected_value == 20 and 2 in position_lottery:
		selected_array[0] = 2

	return selected_array


	


def aiSelect(league, hitters, pitchers, selected_list, draftSlotNum, roundCounter, salaryCap):
	for team in league:
		if draftSlotNum == team['DraftSlot']:
			position = eligiblePosition(team)
			if salaryCap:
				if (26 - roundCounter) > 0:
					avgSalary = team['Salary'] / (26 - roundCounter)
				else:
					avgSalary = team['Salary']
			else:
				avgSalary = 500000
			match team['AIFocus']:
				case 1:
					#Best Overall
					keys = ["Price", "Price", "Price", "Price", "Price", "Price"]
					focus = 0
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 2:
					#Power Hitting
					keys = ["HR", "SLG", "RBI", "Price", "K", "ERA"]
					focus = 0
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 3:
					#Starting Pitching
					keys = ["Price", "W", "ERA", "Price", "OBP", "HR"]
					focus = 0
					player_selected = autoSelectPitcher(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 4:
					#Batting Avg/Speed
					keys = ["Avg", "SB", "Price", "Price", "WHIP", "ERA"]
					focus = 0
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 5:
					#Defense/Hits
					keys = ["Price", "H", "Avg", "Price", "W", "K"]
					focus = 12
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 6:
					#Defense/Speed
					keys = ["Price", "SB", "Avg", "Price", "W", "K"]
					focus = 12
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 7:
					#Strong Bullpen
					keys = ["Price", "SV", "ERA", "Price", "HR", "RBI"]
					focus = 11
					player_selected = autoSelectPitcher(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 8:
					#WHIP kings
					keys = ["WHIP", "ERA", "Price", "Price", "Avg", "RBI"]
					focus = 0
					player_selected = autoSelectPitcher(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 9:
					#Speed
					keys = ["SB", "OBP", "Price", "Price", "WHIP", "W"]
					focus = 0
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 10:
					#Gappers - Doubles/Triples
					keys = ["2B", "SLG", "3B", "Price", "K", "WHIP"]
					focus = 0
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 11:
					#On Base Team
					keys = ["OBP", "Avg", "Price", "Price", "WHIP", "ERA"]
					focus = 0
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 12:
					#Power Pitchers
					keys = ["K", "WHIP", "Price", "Price", "HR", "SLG"]
					focus = 0
					player_selected = autoSelectPitcher(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 13:
					#Lefty Dome
					keys = ["Price", "Avg", "SLG", "Price", "ERA", "WHIP"]
					focus = 13
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 14:
					#Balance. Hitters and Pitchers back and forth
					keys = ["Price", "Avg", "HR", "Price", "ERA", "W"]
					focus = 0
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 15:
					#Strong Up the Middle
					keys = ["Price", "Avg", "HR", "Price", "ERA", "W"]
					focus = 14
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)
				case 16:
					#Clutch Hitters
					keys = ["RBI", "SLG", "Price", "Price", "WHIP", "K"]
					focus = 0
					player_selected = autoSelectHitter(position, hitters, pitchers, selected_list, roundCounter, focus, keys, avgSalary)

	return player_selected

