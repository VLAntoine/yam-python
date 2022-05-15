import random
import constant as cst
from observer import Publisher


class Game(Publisher):
    """
    Game class : contains all the datas about the game (the grid, the turn, etc.)
    It carries out the operation on the hand and the grid according to request sent by the controller.
    """

    def __init__(self, seed_root):
        """
        The constructor of the Game class.
        The only parameter is the seed which will define the randomness of the game. The result of the nth
        dices rolls of 2 same seeded games will be same.
        It initializes the other values.
        """

        super(Game, self).__init__()

        self.turn = 0
        self.roll_number = 0
        self.hand = Hand()

        # the grid is made of all the boxes (total and bonus boxes included)
        # WARNING : the first parameter is the column and the second one is the row.
        self.grid = {}
        for column in cst.COLUMNS:
            self.grid[column] = {}
            for row in cst.ROWS:
                # by default, a box is set to "empty"
                self.grid[column][row] = "empty"

        self.bet_value = ""  # if the player bets on a box, the bet value will be the row of that box.
        self.final_score = ""  # while the game isn't over, final score is empty.
        self.random_seed = RandomSeed(seed_root)  # gives a seed per turn to ensure that the first roll of every turn
        # will be the same for every game with the same seed_root.

    def roll(self, dice_to_roll=range(cst.NUMBER_OF_DICES)):
        """
        Roll the dices of the game's hand.
        The input dice_to_roll is the list of dices to be rolled. By default, all the dices are rolled.
        """

        # If this is the first roll of the turn, a new seed is set, using the seed_root.
        # It ensures that the first roll of every turn will be same from on game to another with the same seed_root.
        # See more details about RandomSeed class.
        if self.roll_number == 0:
            random.seed(self.random_seed.seed_list[self.turn])

        # Roll the dices and iterate the roll number of the turn.
        self.hand.roll(dice_to_roll)
        self.roll_number += 1

        # Notify the changes to the subscribers
        self.notify()

    def set_bet(self, row: str):
        """
        Set the bet to a row.
        The box filled at the end of the turn will be grid["bet"][row].
        """

        self.bet_value = row

        # Notify the change to the subscribers
        self.notify()

    def fill(self, col, row):
        """
        Fill the box grid[col][row] and end the turn.
        Initialize the game parameters for the next turn.
        """

        # notification dictionary that is sent to the views (the subscribers)
        notification = {}

        # if row is "one", "two", "three", "four", "five" or "six"
        if row in cst.UPPER_SECTION:
            # get the corresponding value (1 for "one", 2 for "two", etc.).
            dice_value = cst.COMBINATIONS[row]
            # set the value of the box (grid[col][row]) to the product of the dice value and the amount of times it
            # appears in the hand.
            self.grid[col][row] = dice_value * self.hand.get_dices_dictionary()[dice_value]
            # updating the notification with the box value
            notification["fill"] = {"row": row, "col": col, "value": self.grid[col][row]}

            # set a list of all the values in the upper section of the column
            up_array = [self.grid[col][row_item] for row_item in cst.UPPER_SECTION]
            # if all the boxes in the upper section of the column are filled, calculate the score of this section and a
            # potential bonus
            if "empty" not in up_array:
                self.grid[col]["totalup"] = sum(up_array)
                # set the bonus of the section to 30 if score >= 60, 0 otherwise.
                if self.grid[col]["totalup"] >= 60:
                    self.grid[col]["bonus"] = 30
                else:
                    self.grid[col]["bonus"] = 0
                # updating the notification with the totalup value and the bonus value
                notification["totalup"] = {"col": col, "value": self.grid[col]["totalup"]}
                notification["bonus"] = {"col": col, "value": self.grid[col]["bonus"]}

        # if row is "min" or "max"
        elif row in cst.MEDIUM_SECTION:
            # set the value of the box (grid[col][row]) to the sum of all the dices
            self.grid[col][row] = sum(self.hand.dices)
            # updating the notification with the max or min value
            notification["fill"] = {"row": row, "col": col, "value": self.grid[col][row]}
            # if both "min" and "max" boxes are filled in the column, calculate the score of this section
            if (self.grid[col]["min"] != "empty") and (self.grid[col]["max"] != "empty"):
                # total of this section is the sum of both values (min and max) if value of min < value of max, 0
                # otherwise
                if self.grid[col]["min"] >= self.grid[col]["max"]:
                    self.grid[col]["totalmed"] = 0
                else:
                    self.grid[col]["totalmed"] = self.grid[col]["min"] + self.grid[col]["max"]
                # updating the notification with the totalmed value
                notification["totalmed"] = {"col": col, "value": self.grid[col]["totalmed"]}

        # if row is "fullhouse", "fourofakind", "straight" or "yahtzee"
        elif row in cst.LOWER_SECTION:
            # if the hand realizes the combination, set grid box value (grid[col][row]) to the score
            # of this combination (cst.COMBINATION[row]), 0 otherwise.
            if self.hand.is_combination(row):
                self.grid[col][row] = cst.COMBINATIONS[row]
            else:
                self.grid[col][row] = 0
            # updating the notification with the combination box value
            notification["fill"] = {"row": row, "col": col, "value": self.grid[col][row]}
            # if the lower section of this column is fully filled, calculate the lower section total and complete the
            # grid
            low_array = [self.grid[col][row_item] for row_item in cst.LOWER_SECTION]
            if "empty" not in low_array:
                self.grid[col]["totallow"] = sum(low_array)
                # updating the notification with the total low value
                notification["totallow"] = {"col": col, "value": self.grid[col]["totallow"]}

        # if the column is fully filled, calculate the column score and complete the grid.
        subtotal_arr = [self.grid[col]["totalup"], self.grid[col]["totalmed"], self.grid[col]["totallow"],
                        self.grid[col]["bonus"]]
        if "empty" not in subtotal_arr:
            self.grid[col]["columntotal"] = sum(subtotal_arr)
            # updating the notification with the column total value
            notification["columntotal"] = {"col": col, "value": self.grid[col]["columntotal"]}

        # if the grid is fully filled, calculate the final score, else initialize the game attributes for the next turn.
        column_totals = [self.grid[col_item]["columtotal"] for col_item in cst.COLUMNS]
        if "empty" not in column_totals:
            self.final_score = sum(column_totals)
        else:
            self.turn += 1
            self.roll_number = 0
            self.hand = Hand()
            self.bet_value = ""

        # notify the subscribers
        self.notify(notification)

    def notify(self, *fill):
        context = {"turn": self.turn, "roll_number": self.roll_number, "dices": self.hand.dices, "bet": self.bet_value,
                   "final_score": self.final_score}
        context.update(fill)
        self.notify_subscriber(context)


class Hand:
    """
    Hand class carries out the operation on the dices (roll, etc.)
    and determines whether they realize a well-known combination or not.
    """

    def __init__(self):
        """
        The constructor of the Hand class.
        Its attribute is the array of dices values (NUMBER_OF_DICES values : 1 per dice).
        By default, the value of every dice is set to DEFAULT_DICE_VALUE.
        """
        self.__dices = [cst.DEFAULT_DICE_VALUE for i in range(cst.NUMBER_OF_DICES)]

    @property
    def dices(self):
        """
        The getter of the dice_arr attribute
        """
        return self.__dices

    def roll(self, dice_to_roll=range(cst.NUMBER_OF_DICES)):
        """
        Roll the dices.
        By default, if no dice_to_roll attribute is specified, roll all the dices.
        Dice values are randomly chosen from the DICE_VALUES constant
        """
        for i in dice_to_roll:
            self.dices[i] = random.choice(cst.DICE_VALUES)

    def is_combination(self, combination):
        """
        Return true if the hand realizes the combination (fullhouse, fourofakind, straight, yahtzee), false otherwise.
        """

        # amount_of_values is a dictionary where :
        # - each key is a value of a dice present in the hand
        # - the value is the amount of times, the value appears in the hand
        amount_of_values = self.get_dices_dictionary().values()

        # a fullhouse is a combination of 3 dices of the same value + 2 of another one (can be the same value)
        if combination == "fullhouse":
            if (3 in amount_of_values and 2 in amount_of_values) or (5 in amount_of_values):
                return True
            else:
                return False

        # a fourofakind is realized when the hand contains, at least, four dices of a same value.
        elif combination == "fourofakind":
            if 4 in amount_of_values or 5 in amount_of_values:
                return True
            else:
                return False

        # a straight is realized when the hand contains 1,2,3,4,5 or 2,3,4,5,6.
        elif combination == "straight":
            if (max(amount_of_values) == 1) and (not (1 in self.dices and 6 in self.dices)):
                return True
            else:
                return False

        # a yahtzee is realized when the hand contains 5 dices of the same value.
        elif combination == "yahtzee":
            if 5 in amount_of_values:
                return True
            else:
                return False

    def get_dices_dictionary(self):
        """
        return dices_dictionary, which is a dictionary where :
        - each key is a value of a dice present in the hand
        - the value is the amount of times, the value appears in the hand
        """

        dices_dictionary = {}

        for dice in self.dices:
            if dice in dices_dictionary:
                dices_dictionary[dice] += 1
            else:
                dices_dictionary[dice] = 1
        return dices_dictionary

    def print(self):
        """
        print the hand in the console.
        """
        print(' '.join([str(value) for value in self.dices]), sep=' ')


class RandomSeed:
    """
    Class that rules the randomness of the game.
    """

    def __init__(self, seed_root):
        """
        Constructor of the RandomSeed class.
        The seed root defines the seed list which ensures that the first dices roll of every turn of a game will be the
        same as the first dices roll of a game with the same seed root.
        """
        self.__seed_root = seed_root
        random.seed(seed_root)
        self.__seed_list = [random.randint(0, 2 ** 32 - 1) for i in range(cst.NUMBER_OF_BOXES)]

    @property
    def seed_root(self):
        """
        Getter of the seed root.
        """
        return self.__seed_root

    @property
    def seed_list(self):
        """
        Getter of the seed list.
        A list that defines the randomness of every turn : ensures that the first dices roll of every turn of a game
        will be the same as the first dices roll of a game with the same seed root.
        """
        return self.__seed_list
