# All Time Baseball Draft
## Intro

This program allows you to draft a all time baseball team of 25 players (15 hitters/10 pitchers).
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

## Usage and Install
This program uses Python and runs best on Python 3.10+.
It also uses a few Python modules you'll need to ensure are installed.

Modules needed are (Only requests and tabulate are needed seperately from Python):
- random
- json
- requests
- sys
- time
- webbrowser (If you want to have a web browser show the results)
- tabulate

To install request and tabulate, run this command
> **pip install tabulate requests**

OR

> **python3.10 -m pip install tabulate requests**



