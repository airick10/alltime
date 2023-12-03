from random import randrange
import draftpool
import optionsmenu
import random

# 0 - No Position Check
# 1 - Only pick a Starting Pitcher
# 2 - Only pick a Catcher
# 11 - Only pick a Relief Pitcher
# 13 - Left Handed Hitter/Pitcher
# 14 - Up the middle. Look for Catchers, 2nd base, Short, and CF
# 12 - Position Player position check (Looking for 1s on defense)

def aiSelectSnippet(log, playerpool, selected_list, threshold, defCheck, direction):
	print(log)
	print(f"DefCheck - {defCheck}")

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
			if threshold < 0 or counter > threshold:
				return player['ID']
			counter += 1

	return None


def firstRounds(roll, hitters, pitchers, selected_list, position):
	print("**AI LOG** - Best Price")
	#Putting the hitter pool in its own playerpool for the AI
	hproll = randrange(100)
	position_array = [0,1,0]
	if hproll < roll:
		print("**AI LOG** - Hitter Selected")
		playerpool = hitters
		print("**AI LOG** - Best Price")
		playerpool = draftpool.sortList(playerpool, "Price", "H")
		player_to_select = topFourGrabs("H", playerpool, selected_list, position_array, 0)
	else:
		print("**AI LOG** - Pitcher Selected")
		playerpool = pitchers
		print("**AI LOG** - Best Price")
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		player_to_select = topFourGrabs("P", playerpool, selected_list, position_array, 0)
	return player_to_select


def topFourGrabs(type, playerpool, selected_list, position, direction):
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
			player_to_select = aiSelectSnippet("**AI LOG** - 1st Hitter", playerpool, selected_list, -1, defCheck, direction)
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 1st Pitcher", playerpool, selected_list, -1, defCheck, direction)
	#If the roll is 40 - 69 (30%), apply a counter at 0.  The counter needs to be at 1 to take a player.
	#So the script will take the second best.
	elif newRoll < 70 and newRoll >= 40:
		if type == "H":
			player_to_select = aiSelectSnippet("**AI LOG** - 2nd Hitter", playerpool, selected_list, 0, defCheck, direction)
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 2nd Pitcher", playerpool, selected_list, 0, defCheck, direction)
	#If the roll is 70 - 89 (20%), apply a counter at 0.  The counter needs to be at 2 to take a player.
	#So the script will take the third best.				
	elif newRoll < 90 and newRoll >= 70:
		if type == "H":
			player_to_select = aiSelectSnippet("**AI LOG** - 3rd Hitter", playerpool, selected_list, 1, defCheck, direction)
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 3rd Pitcher", playerpool, selected_list, 1, defCheck, direction)
	#If the roll is 90 - 99 (10%), apply a counter at 0.  The counter needs to be at 3 to take a player.
	#So the script will take the second best.
	else:
		if type == "H":
			player_to_select = aiSelectSnippet("**AI LOG** - 4th Hitter", playerpool, selected_list, 2, defCheck, direction)
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 4th Pitcher", playerpool, selected_list, 2, defCheck, direction)

	return player_to_select

def aiOne(position, hitters, pitchers, selected_list):
	print("**AI LOG** - Focus: Best Overall")
	#Gets a random number.  For this, 80% of the time you go by price.
	#20% of the time, go by OBP.  For pitchers, go to ERA.
	randnum = randrange(100)
	#Deciding on hitter or pitcher.
	side = randrange(2)
	if side == 0:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI.
		playerpool = hitters
		#If that random roll was from 0 - 79, look for the overall price.
		if randnum < 80:
			print("**AI LOG** - Best Price")
			#Sort out the playerpool array by Price for hitters.
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			#If we aren't taking based on price, take by slugging instead.
			print("**AI LOG** - Not best Price, go with best Slugging")
			playerpool = draftpool.sortList(playerpool, "SLG", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
	#Same as above, but for a pitcher.
	else:
		print("**AI LOG** - Pitcher Selected")
		#Putting the pitcher pool in its own playerpool for the AI.
		playerpool = pitchers
		#If that random roll was from 0 - 79, look for the overall price.
		if randnum < 80:
			print("**AI LOG** - Best Price")
			#Sort out the playerpool array by Price for pitchers.
			playerpool = draftpool.sortList(playerpool, "Price", "P")
			if randrange(100) > 15:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
			else:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)
		else:
			#If we aren't taking based on price, take by ERA instead
			print("**AI LOG** - Not best Price, go with best ERA")
			playerpool = draftpool.sortList(playerpool, "ERA", "P")
			if randrange(100) > 20 and position[0] > 0:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
			else:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	return player_to_select
		

def aiTwo(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Power Hitting")
	#Gets a random number.  For this, 60% of the time you go by HR.
	#20% of the time, go by SLG.
	#20% of the time, go by RBI.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 70
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		if randnum < 60:
			print("**AI LOG** - Most HR")
			playerpool = draftpool.sortList(playerpool, "HHR", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		elif randnum < 80 and randnum >= 60:
			print("**AI LOG** - Best SLG")
			playerpool = draftpool.sortList(playerpool, "SLG", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Most RBI")
			playerpool = draftpool.sortList(playerpool, "RBI", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
	else:
		print("**AI LOG** - Pitcher Selected")
		print("**AI LOG** - Best Price")
		playerpool = pitchers
		#Sort out the playerpool array by Price for pitchers.
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		if randrange(100) > 20 and position[0] > 0:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		else:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	return player_to_select


def aiThree(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Starting Pitching")
	#Gets a random number.  For this, 30% of the time you go by Price.
	#30% of the time, go by Wins.
	#20% of the time, go by ERA.
	#20% of the time, go by Strikeouts.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 70
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold:
		print("**AI LOG** - Pitcher Selected")
		#Putting the pitcher pool in its own playerpool for the AI
		playerpool = pitchers
		if randnum < 30:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "P")
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		elif randnum < 60 and randnum >= 30:
			print("**AI LOG** - Most Wins")
			playerpool = draftpool.sortList(playerpool, "W", "P")
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		elif randnum < 80 and randnum >= 60:
			print("**AI LOG** - Most Strikeouts")
			playerpool = draftpool.sortList(playerpool, "PK", "P")
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		else:
			print("**AI LOG** - Best ERA")
			playerpool = draftpool.sortList(playerpool, "ERA", "P")
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
	else:
		print("**AI LOG** - Hitter Selected")
		print("**AI LOG** - Best Price")
		playerpool = hitters
		#Sort out the playerpool array by Price for hitters.
		playerpool = draftpool.sortList(playerpool, "Price", "H")
		player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)

	return player_to_select

def aiFour(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Batting Avg/Speed")
	#Gets a random number.  For this, 40% of the time you go by Avg.
	#40% of the time, go by SB.
	#20% of the time, go by Price.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	
	sideThreshold = 60
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(60, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		if randnum < 40:
			print("**AI LOG** - Best Avg")
			playerpool = draftpool.sortList(playerpool, "Avg", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		elif randnum < 80 and randnum >= 40:
			print("**AI LOG** - Most SB")
			playerpool = draftpool.sortList(playerpool, "SB", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)

	else:
		print("**AI LOG** - Pitcher Selected")
		print("**AI LOG** - Best Price")
		playerpool = pitchers
		#Sort out the playerpool array by Price for pitchers.
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		if randrange(100) > 20 and position[0] > 0:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		else:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	return player_to_select


def aiFive(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Defense/Hits")
	#Gets a random number.  For this, 60% of the time you go by Price.
	#30% of the time, go by Hits.
	#10% of the time, go by Avg.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 70
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(60, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		if randnum < 60:
			print("**AI LOG** - Best Price (Def Check)")
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 12)
		elif randnum < 90 and randnum >= 60:
			print("**AI LOG** - Most Hits (Def Check)")
			playerpool = draftpool.sortList(playerpool, "H", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 12)
		else:
			print("**AI LOG** - Best Avg (Def Check)")
			playerpool = draftpool.sortList(playerpool, "Avg", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 12)
			
	else:
		print("**AI LOG** - Pitcher Selected")
		print("**AI LOG** - Best Price")
		playerpool = pitchers
		#Sort out the playerpool array by Price for pitchers.
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		if randrange(100) > 20 and position[0] > 0:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		else:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	return player_to_select


def aiSix(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Defense/Speed")
	#Gets a random number.  For this, 60% of the time you go by Price.
	#30% of the time, go by SB.
	#10% of the time, go by Avg.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 70
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(50, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		if randnum < 60:
			print("**AI LOG** - Best Price (Def Check)")
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 12)
		elif randnum < 90 and randnum >= 60:
			print("**AI LOG** - Most Stolen Bases (Def Check)")
			playerpool = draftpool.sortList(playerpool, "SB", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 12)
		else:
			print("**AI LOG** - Best Avg (Def Check)")
			playerpool = draftpool.sortList(playerpool, "Avg", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 12)
			
	else:
		print("**AI LOG** - Pitcher Selected")
		print("**AI LOG** - Best Price")
		playerpool = pitchers
		#Sort out the playerpool array by Price for pitchers.
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		if randrange(100) > 20 and position[0] > 0:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		else:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	return player_to_select

def aiSeven(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Bullpen")
	#Gets a random number.  For this, 40% of the time you go by Price with Bullpen.
	#40% of the time, go by Price with Starters.
	#20% of the time, go by ERA.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 70
	side = randrange(100)
	if roundCounter < 6:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		print("**AI LOG** - Best Price")
		#Putting the hitter pool in its own playerpool for the AI
		hproll = randrange(100)
		if hproll < 40:
			print("**AI LOG** - Hitter Selected")
			playerpool = hitters
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			rolerandom = randrange(100)
			print("**AI LOG** - Pitcher Selected")
			playerpool = pitchers
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "P")
			if rolerandom < 70:
				print("**AI LOG** - Select Starting Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
			else:
				print("**AI LOG** - Select Relief Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	elif side < sideThreshold:
		print("**AI LOG** - Pitcher Selected")
		#Putting the pitcher pool in its own playerpool for the AI
		playerpool = pitchers
		if randnum < 40:
			print("**AI LOG** - Best Price (Def Check)")
			playerpool = draftpool.sortList(playerpool, "Price", "P")
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 0)
		elif randnum < 80 and randnum >= 40:
			print("**AI LOG** - Most Saves (Def Check)")
			playerpool = draftpool.sortList(playerpool, "SV", "P")
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)
		else:
			print("**AI LOG** - Best ERA")
			playerpool = draftpool.sortList(playerpool, "ERA", "P")
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 0)
			
	else:
		print("**AI LOG** - Hitter Selected")
		print("**AI LOG** - Best Price")
		playerpool = hitters
		#Sort out the playerpool array by Price for hitters.
		playerpool = draftpool.sortList(playerpool, "Price", "H")
		player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)

	return player_to_select


def aiEight(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: WHIP Kings")
	#Gets a random number.  For this, 60% of the time you go by WHIP.
	#20% of the time, go by ERA.
	#20% of the time, go by Price.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 70
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(30, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Pitcher Selected")
		#Putting the pitchers pool in its own playerpool for the AI
		playerpool = pitchers
		rolerandom = randrange(100)
		if randnum < 60:
			print("**AI LOG** - Best WHIP")
			playerpool = draftpool.sortList(playerpool, "WHIP", "P")
			if rolerandom < 80:
				print("**AI LOG** - Select Starting Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
			else:
				print("**AI LOG** - Select Relief Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)
		elif randnum < 80 and randnum >= 60:
			print("**AI LOG** - Best ERA")
			playerpool = draftpool.sortList(playerpool, "ERA", "P")
			if rolerandom < 80:
				print("**AI LOG** - Select Starting Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
			else:
				print("**AI LOG** - Select Relief Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)
		else:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "P")
			if rolerandom < 80:
				print("**AI LOG** - Select Starting Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
			else:
				print("**AI LOG** - Select Relief Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)
			
	else:
		print("**AI LOG** - Hitter Selected")
		print("**AI LOG** - Best Price")
		playerpool = hitters
		#Sort out the playerpool array by Price for hitters.
		playerpool = draftpool.sortList(playerpool, "Price", "H")
		player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)

	return player_to_select


def aiNine(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Speed")
	#Gets a random number.  For this, 60% of the time you go by Stolen Bases.
	#30% of the time, go by OBP.
	#10% of the time, go by Price.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 70
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(60, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		if randnum < 60:
			print("**AI LOG** - Most Stolen Bases")
			playerpool = draftpool.sortList(playerpool, "SB", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		elif randnum < 90 and randnum >= 60:
			print("**AI LOG** - On Base Percentage")
			playerpool = draftpool.sortList(playerpool, "OBP", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
	else:
		print("**AI LOG** - Pitcher Selected")
		print("**AI LOG** - Best Price")
		playerpool = pitchers
		#Sort out the playerpool array by Price for pitchers.
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		if randrange(100) > 20 and position[0] > 0:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		else:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	return player_to_select


def aiTen(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Doubles/Triples")
	#Gets a random number.  For this, 50% of the time you go by Doubles.
	#30% of the time, go by SLG.
	#20% of the time, go by Triples.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 70
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(70, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		if randnum < 50:
			print("**AI LOG** - Most Doubles")
			playerpool = draftpool.sortList(playerpool, "2B", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		elif randnum < 80 and randnum >= 50:
			print("**AI LOG** - Best Slugging")
			playerpool = draftpool.sortList(playerpool, "SLG", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Most Triples")
			playerpool = draftpool.sortList(playerpool, "3B", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
	else:
		print("**AI LOG** - Pitcher Selected")
		print("**AI LOG** - Best Price")
		playerpool = pitchers
		#Sort out the playerpool array by Price for pitchers.
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		if randrange(100) > 20 and position[0] > 0:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		else:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	return player_to_select


def aiEleven(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: On Base Team")
	#Gets a random number.  For this, 60% of the time you go by On Base.
	#30% of the time, go by Batting Avg.
	#10% of the time, go by Price.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 70
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(60, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		if randnum < 60:
			print("**AI LOG** - Best On Base")
			playerpool = draftpool.sortList(playerpool, "OBP", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		elif randnum < 90 and randnum >= 60:
			print("**AI LOG** - Best Avg")
			playerpool = draftpool.sortList(playerpool, "Avg", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
	else:
		print("**AI LOG** - Pitcher Selected")
		print("**AI LOG** - Best Price")
		playerpool = pitchers
		#Sort out the playerpool array by Price for pitchers.
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		if randrange(100) > 20 and position[0] > 0:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		else:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	return player_to_select


def aiTwelve(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Power Pitchers")
	#Gets a random number.  For this, 70% of the time you go by Strikeouts.
	#20% of the time, go by WHIP.
	#10% of the time, go by Price.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 70
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(30, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Pitcher Selected")
		#Putting the pitchers pool in its own playerpool for the AI
		playerpool = pitchers
		rolerandom = randrange(100)
		if randnum < 70:
			print("**AI LOG** - Most Strikeouts")
			playerpool = draftpool.sortList(playerpool, "K", "P")
			if rolerandom < 80:
				print("**AI LOG** - Select Starting Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
			else:
				print("**AI LOG** - Select Relief Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)
		elif randnum < 90 and randnum >= 70:
			print("**AI LOG** - Best WHIP")
			playerpool = draftpool.sortList(playerpool, "WHIP", "P")
			if rolerandom < 80:
				print("**AI LOG** - Select Starting Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
			else:
				print("**AI LOG** - Select Relief Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)
		else:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "P")
			if rolerandom < 80:
				print("**AI LOG** - Select Starting Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
			else:
				print("**AI LOG** - Select Relief Pitcher")
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)
			
	else:
		print("**AI LOG** - Hitter Selected")
		print("**AI LOG** - Best Price")
		playerpool = hitters
		#Sort out the playerpool array by Price for hitters.
		playerpool = draftpool.sortList(playerpool, "Price", "H")
		player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)

	return player_to_select


def aiThirteen(position, hitters, pitchers, selected_list):
	print("**AI LOG** - Focus: Lefty Dome")
	#Gets a random number.  For this, 80% of the time you go by Price.
	#10% of the time, go by Batting Avg.
	#10% of the time, go by Slugging.
	#Gets a random number.  For pitchers, 80% of the time you go by Price.
	#10% of the time, go by ERA.
	#10% of the time, go by WHIP.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 50
	side = randrange(100)
	if side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		handroll = randrange(100)
		if randnum < 80:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			if handroll < 80:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 13)
			else:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		elif randnum < 90 and randnum >= 80:
			print("**AI LOG** - Best Avg")
			playerpool = draftpool.sortList(playerpool, "Avg", "H")
			if handroll < 80:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 13)
			else:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Best Slugging")
			playerpool = draftpool.sortList(playerpool, "SLG", "H")
			if handroll < 80:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 13)
			else:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
	else:
		print("**AI LOG** - Pitcher Selected")
		#Putting the pitcher pool in its own playerpool for the AI
		playerpool = pitchers
		handroll = randrange(100)
		if randnum < 80:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "P")
			if handroll < 80:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 13)
			else:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 0)
		elif randnum < 90 and randnum >= 80:
			print("**AI LOG** - Best ERA")
			playerpool = draftpool.sortList(playerpool, "ERA", "P")
			if handroll < 80:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 13)
			else:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Best WHIP")
			playerpool = draftpool.sortList(playerpool, "WHIP", "P")
			if handroll < 80:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 13)
			else:
				player_to_select = topFourGrabs("P", playerpool, selected_list, position, 0)

	return player_to_select

def aiFourteen(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Balanced")
	#Gets a random number.  For this, 35% of the time you go by Price.
	#35% of the time, go by Batting Avg.
	#30% of the time, go by Home Runs.
	#Gets a random number.  For pitchers, 35% of the time you go by Price.
	#35% of the time, go by ERA.
	#30% of the time, go by Wins.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 50
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(50, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		if randnum < 35:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		elif randnum < 70 and randnum >= 35:
			print("**AI LOG** - Most Home Runs")
			playerpool = draftpool.sortList(playerpool, "HHR", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Best Average")
			playerpool = draftpool.sortList(playerpool, "Avg", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
	else:
		print("**AI LOG** - Pitcher Selected")
		#Putting the pitcher pool in its own playerpool for the AI
		playerpool = pitchers
		if randnum < 35:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "P")
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 0)
		elif randnum < 70 and randnum >= 35:
			print("**AI LOG** - Best ERA")
			playerpool = draftpool.sortList(playerpool, "ERA", "P")
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Most Wins")
			playerpool = draftpool.sortList(playerpool, "W", "P")
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 0)

	return player_to_select


def aiFifteen(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Up the Middle")
	#Gets a random number.  For this, 60% of the time you go by Price.
	#20% of the time, go by Batting Avg.
	#20% of the time, go by Slugging.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 50
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(50, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		handroll = randrange(100)
		if randnum < 60:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			if handroll < 65:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 14)
			else:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		elif randnum < 80 and randnum >= 60:
			print("**AI LOG** - Best Avg")
			playerpool = draftpool.sortList(playerpool, "Avg", "H")
			if handroll < 65:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 14)
			else:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Best Slugging")
			playerpool = draftpool.sortList(playerpool, "SLG", "H")
			if handroll < 65:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 14)
			else:
				player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
	else:
		print("**AI LOG** - Pitcher Selected")
		print("**AI LOG** - Best Price")
		playerpool = pitchers
		#Sort out the playerpool array by Price for pitchers.
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		if randrange(100) > 20 and position[0] > 0:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		else:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	return player_to_select


def aiSixteen(position, hitters, pitchers, selected_list, roundCounter):
	print("**AI LOG** - Focus: Clutch Hitters")
	#Gets a random number.  For this, 50% of the time you go by RBI.
	#30% of the time, go by Slugging.
	#20% of the time, go by Price.
	randnum = randrange(100)
	#Deciding on hitter (70%) or pitcher (30%).
	sideThreshold = 60
	side = randrange(100)
	if roundCounter < 3:
		sideThreshold = 90
	if side < sideThreshold and roundCounter < 3:
		player_to_select = firstRounds(60, hitters, pitchers, selected_list, position)
	elif side < sideThreshold:
		print("**AI LOG** - Hitter Selected")
		#Putting the hitter pool in its own playerpool for the AI
		playerpool = hitters
		if randnum < 50:
			print("**AI LOG** - Most RBI")
			playerpool = draftpool.sortList(playerpool, "RBI", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		elif randnum < 80 and randnum >= 50:
			print("**AI LOG** - Best Slugging")
			playerpool = draftpool.sortList(playerpool, "SLG", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)
		else:
			print("**AI LOG** - Best Price")
			playerpool = draftpool.sortList(playerpool, "Price", "H")
			player_to_select = topFourGrabs("H", playerpool, selected_list, position, 0)

	else:
		print("**AI LOG** - Pitcher Selected")
		print("**AI LOG** - Best Price")
		playerpool = pitchers
		#Sort out the playerpool array by Price for pitchers.
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		if randrange(100) > 20 and position[0] > 0:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 1)
		else:
			player_to_select = topFourGrabs("P", playerpool, selected_list, position, 11)

	return player_to_select


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
	'''
	while selected_value == 1 or selected_value == 11:
		selected_value = random.choice(position_lottery)
	selected_array[0] = selected_value
	'''
		
	
	if team['AIFocus'] == 15:
		if any(n in position_lottery for n in (8, 4, 6, 2)):
			while selected_array[0] not in (8, 4, 6, 2): 
				selected_array[0] = random.choice(position_lottery)

	if selected_value == 20 and 2 in position_lottery:
		selected_array[0] = 2

	return selected_array


	


def aiSelect(league, hitters, pitchers, selected_list, draftSlotNum, roundCounter):
	for team in league:
		if draftSlotNum == team['DraftSlot']:
			position = eligiblePosition(team)
			#print(f"Position - {position}")
			match team['AIFocus']:
				case 1:
					#Best Overall
					player_selected = aiOne(position, hitters, pitchers, selected_list)
				case 2:
					#Power Hitting
					player_selected = aiTwo(position, hitters, pitchers, selected_list, roundCounter)
				case 3:
					#Starting Pitching
					player_selected = aiThree(position, hitters, pitchers, selected_list, roundCounter)
				case 4:
					#Batting Avg/Speed
					player_selected = aiFour(position, hitters, pitchers, selected_list, roundCounter)
				case 5:
					#Defense/Hits
					player_selected = aiFive(position, hitters, pitchers, selected_list, roundCounter)
				case 6:
					#Defense/Speed
					player_selected = aiSix(position, hitters, pitchers, selected_list, roundCounter)
				case 7:
					#Strong Bullpen
					player_selected = aiSeven(position, hitters, pitchers, selected_list, roundCounter)
				case 8:
					#WHIP kings
					player_selected = aiEight(position, hitters, pitchers, selected_list, roundCounter)
				case 9:
					#Speed
					player_selected = aiNine(position, hitters, pitchers, selected_list, roundCounter)
				case 10:
					#Gappers - Doubles/Triples
					player_selected = aiTen(position, hitters, pitchers, selected_list, roundCounter)
				case 11:
					#On Base Team
					player_selected = aiEleven(position, hitters, pitchers, selected_list, roundCounter)
				case 12:
					#Power Pitchers
					player_selected = aiTwelve(position, hitters, pitchers, selected_list, roundCounter)
				case 13:
					#Lefty Dome
					player_selected = aiThirteen(position, hitters, pitchers, selected_list)
				case 14:
					#Balance. Hitters and Pitchers back and forth
					player_selected = aiFourteen(position, hitters, pitchers, selected_list, roundCounter)
				case 15:
					#Strong Up the Middle
					player_selected = aiFifteen(position, hitters, pitchers, selected_list, roundCounter)
				case 16:
					#Clutch Hitters
					player_selected = aiSixteen(position, hitters, pitchers, selected_list, roundCounter)

	return player_selected

