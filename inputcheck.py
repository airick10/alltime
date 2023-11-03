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
