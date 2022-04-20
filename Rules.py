from Game import *
from Hand import *

COMBINATIONS_KEYS = [*COMBINATIONS]


def check_rules(action, game):

	try:

		action_type = action.rsplit("_")[0]

		if action_type == "roll":
			check_roll(action, game)
		elif action_type == "bet":
			check_bet(action, game)
		elif action_type == "fill":
			check_fill(action, game)

	except Exception as error:
		raise error



def check_roll(action, game):
	if game.roll_number >= 3:
		raise Exception("Vous avez atteint la limite maximale de lancer")
	elif game.roll_number == 0 and action != "roll":
		raise Exception("Vous devez lancer tous les dés au premier jet")


def check_bet(action, game):

	bet_list = action.rsplit("_")

	if len(bet_list) != 3:
		raise Exception("Vous devez choisir une case sur laquelle annoncer")

	else:
		col = bet_list[1]
		row = bet_list[2]

		if col != "betcol":
			raise Exception("Vous ne pouvez annoncé que dans la colonne dédiée")
		elif game.roll_number != 1:
			raise Exception("Vous ne pouvez annoncer qu'entre votre premier et votre second lancer")
		elif game.grid["betcol"][row] != "empty":
			raise Exception("Vous avez déjà rempli cette case")
		elif game.bet_value != None:
			raise Exception("Vous avez déjà parié à ce tour")


def check_fill(action, game):

	fill_list = action.rsplit("_")

	if len(fill_list) != 3:
		raise Exception("Vous devez choisir une case à remplir")

	else:

		col = fill_list[1]
		row = fill_list[2]

		if game.roll_number == 0:
			raise Exception("Vous ne pouvez remplir la grille qu'après votre premier lancer")
		elif game.bet_value != None and col != "betcol":
			raise Exception("Vous avez annoncé, vous devez remplir cette colonne")
		elif game.bet_value != None and row != game.bet_value:
			raise Exception("Vous devez remplir la case sur laquelle vous avez annoncé")
		elif game.bet_value == None and col == "betcol":
			raise Exception("Vous ne pouvez pas remplir dans la colonne des annoncés si vous n'avez pas annoncé avant")
		elif game.grid[col][row] != "empty":
			raise Exception("Vous avez déjà rempli cette case")
		elif col == "descending" and row != "one" and game.grid[col][COMBINATIONS_KEYS[COMBINATIONS_KEYS.index(row) - 1]] == "empty":
			raise Exception("La colonne descendante doit être remplie de haut en bas dans l'ordre")
		elif col == "ascending" and row != "yahtzee" and game.grid[col][COMBINATIONS_KEYS[COMBINATIONS_KEYS.index(row) + 1]] == "empty":
			raise Exception("La colonne ascendante doit être remplie de bas en haut dans l'ordre")
