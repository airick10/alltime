import random

def aiFocus():
	choices = [1,2,3,4,5,6]
	choice = random.choice(choices)
	return choice

def aiSelect(league, hitters, pitchers, selected_list):
	for player in hitters:
		if player['ID'] not in selected_list:
			print(f"{player['FirstName']} {player['LastName']}")
			return player['ID']
