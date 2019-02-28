#
# Routines for writing out updated decks based on either the player piles or the shared piles
#
from datetime import datetime as dt
import collections
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer as json #since .net 3.5?

PLAYER_DECK = ['Library', 'Crypt']

def saveTable(group, x=0, y=0):
	mute()
	
	if 1 != askChoice('You are about to SAVE the table states including the elements on the table and each player\'s hand and piles.\nThis option should be execute on the a game host.'
		, ['I am the Host!', 'I am not...'], ['#dd3737', '#d0d0d0']):
		return
	
	try:
		tab = {"table":[], "shared": {}, 'counters': None, "players": None}
		
		# loop and retrieve cards from the table
		for card in table:
			tab['table'].append(serializeCard(card))
			
		# loop each player
		players = sorted(getPlayers(), key=lambda x: x._id, reverse=False)
		tab['players'] = [serializePlayer(pl) for pl in players]
	
		dir = wd('table-state-{}.json'.format('{:%Y%m%d%H%M%S}'.format(dt.now())))
		filename = "Decks".join(dir.rsplit('OCTGN',1))
		
		filename = askString('Please input the path to save the game state', filename)
		
		if filename == None:
			return
		
		with open(filename, 'w+') as f:
			f.write(json().Serialize(tab))
		
		notify("Table state saves to {}".format(filename))
	finally:
		notify("Table state saved sucessfully")
		
def autosaveTable(group, x=0, y=0):
	mute()
	
	try:
		tab = {"table":[], "shared": {}, 'counters': None, "players": None}
		
		# loop and retrieve cards from the table
		for card in table:
			tab['table'].append(serializeCard(card))
			
		# loop each player
		players = sorted(getPlayers(), key=lambda x: x._id, reverse=False)
		tab['players'] = [serializePlayer(pl) for pl in players]
	
		dir = wd('autosave.json'.format('{:%Y%m%d%H%M%S}'.format(dt.now())))
		filename = "Decks".join(dir.rsplit('OCTGN',1))
		
		with open(filename, 'w+') as f:
			f.write(json().Serialize(tab))
		
	finally:
		notify("Table autosave state created sucessfully")

def loadTable(group, x=0, y=0):
	mute()
	
	if 1 != askChoice('You are about to LOAD the table states including the elements on the table and each player\'s hand and piles.\nThis option should be execute on the a game host.'
		, ['I am the Host!', 'I am not...'], ['#dd3737', '#d0d0d0']):
		return
	
	try:
		dir = wd('table-state.json')
		filename = "Decks".join(dir.rsplit('OCTGN',1))

		filename = askString('Please provide the file path to load the table states', filename)
		
		if filename == None:
			return
		
		resetGame()
		
		with open(filename, 'r') as f:
			tab = json().DeserializeObject(f.read())
		
		deserializeTable(tab['table'])
		
		if tab['counters'] is not None and len(tab['counters']) > 0:
			deserializeCounters(tab['counters'], shared)

		if tab['players'] is not None and len(tab['players']) > 0:
			for player in tab['players']:
				deserializePlayer(player)

		notify("Successfully load table state from {}".format(filename))
	finally:
		notify("Table state loaded sucessfully")
		
def loadautosaveTable(group, x=0, y=0):
	mute()
	
	try:
		resetGame()
		dir = wd('autosave.json')
		filename = "Decks".join(dir.rsplit('OCTGN',1))

		with open(filename, 'r') as f:
			tab = json().DeserializeObject(f.read())
		
		deserializeTable(tab['table'])
		
		if tab['counters'] is not None and len(tab['counters']) > 0:
			deserializeCounters(tab['counters'], shared)

		if tab['players'] is not None and len(tab['players']) > 0:
			for player in tab['players']:
				deserializePlayer(player)

	finally:
		notify("Table autosaved state loaded sucessfully")