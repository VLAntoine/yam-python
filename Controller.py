from Hand import *
from Game import *
from Rules import *


class Controller:

    def __init__(self):
        self.game = Game()

    def play(self, action):

        response = {}

        try:

            check_rules(action, self.game)

            action_type = action.rsplit("_")[0]

            if action_type == "roll":

                if "_" in action:
                    dice_to_roll_str = action.rsplit("_")[1]
                    dice_to_roll = []
                    for i in range(len(dice_to_roll_str)):
                        dice_to_roll.append(int(dice_to_roll_str[i]))

                    self.game.roll(dice_to_roll)

                else:
                    self.game.roll()

            elif action_type == "bet":
                row = action.rsplit("_")[2]
                self.game.set_bet(row)

            elif action_type == "fill":
                action_list = action.rsplit("_")
                col = action_list[1]
                row = action_list[2]

                self.game.fill(col, row)

                response.update({"fill": {(col, row): self.game.grid[col][row]}})

            if self.game.final_score != "empty":
                response.update({"final_score": self.game.final_score})

            response.update({"roll_number": self.game.roll_number, "dices": self.game.hand.dice_arr,
                             "bet_value": self.game.bet_value, "grid": self.game.grid})

            return response

        except Exception as error:

            response = {"error": error}
            return response
