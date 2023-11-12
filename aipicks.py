from random import randrange
import draftpool

def aiSelectSnippet(log, playerpool, selected_list, threshold):
	print(log)
	if threshold < 0:
		for player in playerpool:
			if player['ID'] not in selected_list:
				return player['ID']
	else:
		counter = 0
		for player in playerpool:
			if player['ID'] not in selected_list:
				if counter > threshold:
					return player['ID']
				else:
					counter += 1

def aiOne(team, hitters, pitchers, selected_list):
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
		else:
			#If we aren't taking based on price, take by slugging instead.
			print("**AI LOG** - Not best Price, go with best Slugging")
			playerpool = draftpool.sortList(playerpool, "SLG", "H")
		#Roll again and see if you will take the best player, second best, third best, or fourth best.
		#40% - 1st, 30% - 2nd, 20% - 3rd, 10% - 4th
		newRoll = randrange(100)
		#If the roll is 0 - 39 (40%), don't apply a counter.  Just take the highest price.
		if newRoll < 40:
			player_to_select = aiSelectSnippet("**AI LOG** - 1st Hitter", playerpool, selected_list, -1)
		#If the roll is 40 - 69 (30%), apply a counter at 0.  The counter needs to be at 1 to take a player.
		#So the script will take the second best.
		elif newRoll < 70 and newRoll >= 40:
			player_to_select = aiSelectSnippet("**AI LOG** - 2nd Hitter", playerpool, selected_list, 0)
		#If the roll is 70 - 89 (20%), apply a counter at 0.  The counter needs to be at 2 to take a player.
		#So the script will take the third best.				
		elif newRoll < 90 and newRoll >= 70:
			player_to_select = aiSelectSnippet("**AI LOG** - 3rd Hitter", playerpool, selected_list, 1)
		#If the roll is 90 - 99 (10%), apply a counter at 0.  The counter needs to be at 3 to take a player.
		#So the script will take the second best.
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 4th Hitter", playerpool, selected_list, 2)
		
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
		else:
			#If we aren't taking based on price, take by ERA instead
			print("**AI LOG** - Not best Price, go with best ERA")
			playerpool = draftpool.sortList(playerpool, "ERA", "P")
		#Roll again and see if you will take the best player, second best, third best, or fourth best.
		#40% - 1st, 30% - 2nd, 20% - 3rd, 10% - 4th
		newRoll = randrange(100)
		#If the roll is 0 - 39 (40%), don't apply a counter.  Just take the highest price.
		if newRoll < 40:
			player_to_select = aiSelectSnippet("**AI LOG** - 1st Pitcher", playerpool, selected_list, -1)
		#If the roll is 40 - 69 (30%), apply a counter at 0.  The counter needs to be at 1 to take a player.
		#So the script will take the second best.			
		elif newRoll < 70 and newRoll >= 40:
			player_to_select = aiSelectSnippet("**AI LOG** - 2nd Pitcher", playerpool, selected_list, 0)
		#If the roll is 70 - 89 (20%), apply a counter at 0.  The counter needs to be at 2 to take a player.
		#So the script will take the third best.
		elif newRoll < 90 and newRoll >= 70:
			player_to_select = aiSelectSnippet("**AI LOG** - 3rd Pitcher", playerpool, selected_list, 1)
		#If the roll is 90 - 99 (10%), apply a counter at 0.  The counter needs to be at 3 to take a player.
		#So the script will take the second best.
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 3rd Pitcher", playerpool, selected_list, 2)

	return player_to_select
		

def aiTwo(team, hitters, pitchers, selected_list, roundCounter):
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
		elif randnum < 80 and randnum >= 60:
			print("**AI LOG** - Best SLG")
			playerpool = draftpool.sortList(playerpool, "SLG", "H")
		else:
			print("**AI LOG** - Most RBI")
			playerpool = draftpool.sortList(playerpool, "RBI", "H")
		#Roll again and see if you will take the best player, second best, third best, or fourth best.
		#40% - 1st, 30% - 2nd, 20% - 3rd, 10% - 4th
		newRoll = randrange(100)
		#If the roll is 0 - 39 (40%), don't apply a counter.  Just take the highest player.
		if newRoll < 40:
			player_to_select = aiSelectSnippet("**AI LOG** - 1st Hitter", playerpool, selected_list, -1)
		#If the roll is 40 - 69 (30%), apply a counter at 0.  The counter needs to be at 1 to take a player.
		#So the script will take the second best.
		elif newRoll < 70 and newRoll >= 40:
			player_to_select = aiSelectSnippet("**AI LOG** - 2nd Hitter", playerpool, selected_list, 0)
		#If the roll is 70 - 89 (20%), apply a counter at 0.  The counter needs to be at 2 to take a player.
		#So the script will take the third best.				
		elif newRoll < 90 and newRoll >= 70:
			player_to_select = aiSelectSnippet("**AI LOG** - 3rd Hitter", playerpool, selected_list, 1)
		#If the roll is 90 - 99 (10%), apply a counter at 0.  The counter needs to be at 3 to take a player.
		#So the script will take the second best.
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 4th Hitter", playerpool, selected_list, 2)
	else:
		print("**AI LOG** - Pitcher Selected")
		print("**AI LOG** - Best Price")
		#Sort out the playerpool array by Price for pitchers.
		playerpool = draftpool.sortList(playerpool, "Price", "P")
		#Roll again and see if you will take the best player, second best, third best, or fourth best.
		#40% - 1st, 30% - 2nd, 20% - 3rd, 10% - 4th
		newRoll = randrange(100)
		#If the roll is 0 - 39 (40%), don't apply a counter.  Just take the highest price.
		if newRoll < 40:
			player_to_select = aiSelectSnippet("**AI LOG** - 1st Pitcher", playerpool, selected_list, -1)
		#If the roll is 40 - 69 (30%), apply a counter at 0.  The counter needs to be at 1 to take a player.
		#So the script will take the second best.			
		elif newRoll < 70 and newRoll >= 40:
			player_to_select = aiSelectSnippet("**AI LOG** - 2nd Pitcher", playerpool, selected_list, 0)
		#If the roll is 70 - 89 (20%), apply a counter at 0.  The counter needs to be at 2 to take a player.
		#So the script will take the third best.
		elif newRoll < 90 and newRoll >= 70:
			player_to_select = aiSelectSnippet("**AI LOG** - 3rd Pitcher", playerpool, selected_list, 1)
		#If the roll is 90 - 99 (10%), apply a counter at 0.  The counter needs to be at 3 to take a player.
		#So the script will take the second best.
		else:
			player_to_select = aiSelectSnippet("**AI LOG** - 3rd Pitcher", playerpool, selected_list, 2)

	return player_to_select





def aiSelect(league, hitters, pitchers, selected_list, draftSlotNum, roundCounter):
	for team in league:
		if draftSlotNum == team['DraftSlot']:
			match team['AIFocus']:
				case 1:
					player_selected = aiOne(team, hitters, pitchers, selected_list)
				case 2:
					player_selected = aiTwo(team, hitters, pitchers, selected_list, roundCounter)
				#case 3:
					#Starting Pitching
				#case 4:
					#Batting Avg/Speed
				#case 5:
					#Defense/Hits
				#case 6:
					#Defense/Speed
				#case 7:
					#Strong Bullpen
				#case 8:
					#WHIP kings
				#case 9:
					#Speed
				#case 10:
					#Gappers - Doubles/Triples
				#case 11:
					#On base team
				#case 12:
					#Pitchers who don't give up dingers
				#case 13:
					#Lefty Dome
				#case 14:
					#Balance. Hitters and Pitchers back and forth
				#case 15:
					#Strong Up the Middle
				#case 16:
					#Double Plays.  None Hitting, lots pitching.
	return player_selected

