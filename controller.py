import random

import util as util
import exception
from model import Game
from observer import Subscriber


class GamePageController:
    """
    The Controller class receives the request from the GUI, checks if this request is valid (format,...) and pass the
    request to the model (the Game), which will carry out all the operations.
    """

    def __init__(self, view: Subscriber, seed: int = random.randint(0, 2 ** 32 - 1)):
        """
        The constructor of the Controller class.
        Initialize a game.
        Add the view in parameter (a subscriber) to subscribers list of the Game (the publisher)
        """
        self.game = Game(seed)
        self.game.subscribe(view)

    def play(self, request: dict):
        """
        Process the request, which is a dictionary, from the GUI :
        - check the potential error,
        - send operations to be done to the Game
        """
        try:
            # check the request (if the format is valid, if it's in the game rules,...)
            util.check_game_request(request, self.game)

            # send the request to the game, according to the value associated with the action key of the request.
            action = request["action"]
            if action == "roll":
                dices = request["dices"]
                if dices:
                    self.game.roll(dices)
                else:
                    self.game.roll()
            else:
                row = request["row"]
                col = request["col"]

                if action == "bet":
                    self.game.set_bet(row)
                elif action == "fill":
                    self.game.fill(col, row)

        # raise an exception if the request is not valid
        except (exception.UserRequestException, exception.GameRulesException) as error:
            raise error


class ChooseSeedPageController:
    """
    The ChooseSeedPageController receives a seed from the gui and checks it is valid, otherwise it raises an exception.
    """

    def __init__(self):
        """
        The constructor from the ChooseSeedPageController.
        """
        pass

    def check_seed(self, seed):
        """
        Checks if the seed is valid and sends an exception otherwise.
        """
        try:
            util.check_seed_request(seed)
        except (exception.UserRequestException, exception.GameRulesException) as error:
            raise error
