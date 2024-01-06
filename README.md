# All Time Baseball Draft

## Introduction
This program allows you to draft an all-time baseball team consisting of 25 players (15 hitters/10 pitchers). Teams are evaluated using rotisserie baseball style standings based on various statistical categories.

### Statistical Categories
- **Hitters**: Runs, Home Runs, RBI, SB (minus CS), Strikeouts (minus BB), Team OPS, and Team Defense rating.
- **Pitchers**: Wins (minus L), Strikeouts, Shutouts, Saves, Team ERA, Team WHIP.
- **General**: Total Price of the player.

Standings are determined by the ranked order in each category, compiling a final total. Note that counting stats for hitters are fully counted for starters and half for bench players. Pitching staffs composed predominantly of pitchers throwing from one side (with one exception) will incur a 5-point penalty.

## Usage and Installation
This program is written in Python and optimized for Python 3.10+.

### Modules Required
- `random` (included in Python)
- `json` (included in Python)
- `sys` (included in Python)
- `time` (included in Python)
- `webbrowser` (optional for web browser results, included in Python)
- `requests` (requires separate installation)
- `tabulate` (requires separate installation)

### Installation Commands
Install the necessary modules using the following command:

For pip users:
```markdown
pip install tabulate requests
```

For python 3.10:
```markdown
python3.10 -m pip install tabulate requests
```



