from model import Game
from constant import *
import constant as cst
import re
from exception import *


def check_seed_request(seed):
    """
    Check whether the seed request sent by the user on the ChooseSeedPage is valid or not.
    """
    # if the seed is not an instance of String
    if not isinstance(seed, str):
        raise UserRequestException("La seed doit être une chaîne de caractère.")
    # if the seed is not made of digits or empty
    elif not re.compile("^[0-9]*$").match(seed):
        raise UserRequestException("La seed doit être constituée de chiffres uniquement.")
    # if the seed, when converted into integer, is greater (or equal) than 2 ** 32
    elif seed != "" and int(seed) >= 2 ** 32:
        raise UserRequestException("La seed ne doit pas dépassée 2^32")


def check_game_request(request: dict, game: Game):
    """
    Check whether the game request sent by the user on the GamePage is valid or not.
    """
    try:
        # if the game is over, i.e. the final score field is filled
        if game.final_score != "":
            raise GameRulesException("La partie est finie, vous ne pouvez plus jouer.")
        # if the string "action" is not a request key
        elif "action" not in request.keys():
            raise UserRequestException("Vous devez spécifier une action à effectuer.")
        # if the value associated to "action" isn't in ["fill", "roll", "bet"]
        elif request["action"] not in cst.ACTIONS:
            raise UserRequestException("L'action que vous tentez d'effectuer n'existe pas.")

        # check the request, depending on the specific action made by the user (fill, roll or bet)
        action = request["action"]
        if action == "roll":
            __check_roll(request, game)
        elif action == "bet":
            __check_bet(request, game)
        elif action == "fill":
            __check_fill(request, game)

    except (UserRequestException, GameRulesException) as error:
        raise error


def __check_roll(request: dict, game: Game):
    """
    Check the request when the user rolls the dices.
    """
    # Raise an exception if :
    # the user has reached the authorized limit of dices rolls per turn
    if game.roll_number >= cst.ROLLS_PER_TURN:
        raise GameRulesException("Vous avez atteint la limite maximale de lancer pour ce tour")
    # "dices" isn't a key of the request
    elif "dices" not in request.keys():
        raise UserRequestException("Vous devez spécifier des dés à lancer")
    # the value associated to "dices" in the request isn't a list of integers
    elif not (isinstance(request["dices"], set)
              and all(isinstance(dice_index, int) for dice_index in request["dices"])):
        raise UserRequestException("Les dés doivent être fournis sous forme d'un set d'entiers")
    # there is one dice or more, which is not rolled at the first roll
    elif game.roll_number == 0 and (request["dices"] != set() or
                                    all(dice in request["dices"] for dice in range(cst.NUMBER_OF_DICES))):
        raise GameRulesException("Vous devez lancer tous les dés au premier jet")


def __check_bet(request: dict, game: Game):
    """
    Check the request when the user bets on a box.
    """
    # Raise an exception if :
    # "col" isn't a key of the request
    if "col" not in request.keys():
        raise UserRequestException("Vous devez choisir une colonne sur laquelle annoncer.")
    # "row" isn't a key of the request
    elif "row" not in request.keys():
        raise UserRequestException("Vous devez choisir une ligne sur laquelle annoncer.")
    # the column of the box to bet on isn't in the columns list of the game (cst.COLUMNS)
    # and the row of the box to bet on isn't in the rows list of the game (cst.COMBINATIONS_KEYS)
    elif request["col"] not in cst.COLUMNS or request["row"] not in cst.COMBINATIONS_KEYS:
        raise UserRequestException("Vous devez annoncer sur une case qui existe.")
    else:
        col = request["col"]
        row = request["row"]
        # the column of the box to bet on isn't dedicated to this action
        if col != "betcol":
            raise GameRulesException("Vous ne pouvez annoncer que dans la colonne dédiée")
        # the bet isn't made just after the first roll of a turn
        elif game.roll_number != 1:
            raise GameRulesException("Vous ne pouvez annoncer qu'après votre premier lancer")
        # the box to bet on has already been filled
        elif game.grid["betcol"][row] != "empty":
            raise GameRulesException("Vous avez déjà rempli cette case")
        # the user has already bet
        elif game.bet_value != "":
            raise GameRulesException("Vous avez déjà parié à ce tour")


def __check_fill(request: dict, game: Game):
    """
    Check the request when the user fills a box.
    """
    # Raise an exception if :
    # "col" isn't a key of the request
    if "col" not in request.keys():
        raise UserRequestException("Vous devez choisir la colonne de la case à remplir.")
    # "row" isn't a key of the request
    elif "row" not in request.keys():
        raise UserRequestException("Vous devez choisir la ligne de la case à remplir.")
    # the column of the box to be filled isn't in the columns list of the game (cst.COLUMNS)
    # and the row of the box to be filled isn't in the rows list of the game (cst.COMBINATIONS_KEYS)
    elif request["col"] not in cst.COLUMNS or request["row"] not in cst.COMBINATIONS_KEYS:
        raise UserRequestException("Vous devez remplir une case qui existe.")
    else:
        col = request["col"]
        row = request["row"]
        # the user tries to fill the grid without rolling dices
        if game.roll_number == 0:
            raise GameRulesException("Vous ne pouvez remplir la grille qu'après votre premier lancer")
        # the user has bet and doesn't fill a "betcol" column
        elif game.bet_value != "" and col != "betcol":
            raise GameRulesException("Vous avez annoncé, vous devez remplir cette colonne")
        # the user has bet and doesn't fill the value (the row) associated to its bet
        elif game.bet_value != "" and row != game.bet_value:
            raise GameRulesException("Vous devez remplir la case sur laquelle vous avez annoncé")
        # the user tries to fill a bet column without having bet
        elif game.bet_value == "" and col == "betcol":
            raise GameRulesException("Vous ne pouvez pas remplir dans la colonne des annoncés si vous n'avez pas "
                                     "annoncé avant")
        # the box to be filled has already been filled
        elif game.grid[col][row] != "empty":
            raise GameRulesException("Vous avez déjà rempli cette case")
        # the user tries to fill a descending column without respecting the descending order
        elif col == "descending" and row != "one" and \
                game.grid[col][cst.COMBINATIONS_KEYS[cst.COMBINATIONS_KEYS.index(row) - 1]] == "empty":
            raise GameRulesException("La colonne descendante doit être remplie de haut en bas dans l'ordre")
        # the user tries to fill an ascending column without respecting the ascending order
        elif col == "ascending" and row != "yahtzee" and \
                game.grid[col][COMBINATIONS_KEYS[COMBINATIONS_KEYS.index(row) + 1]] == "empty":
            raise GameRulesException("La colonne ascendante doit être remplie de bas en haut dans l'ordre")
