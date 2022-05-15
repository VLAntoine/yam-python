NUMBER_OF_DICES = 5
DICE_VALUES = [1, 2, 3, 4, 5, 6]
DEFAULT_DICE_VALUE = 1

ROLLS_PER_TURN = 3

# every combination and the corresponding amount of points the player earns by realizing it.
COMBINATIONS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "min": 0, "max": 0, "fullhouse": 20,
                "fourofakind": 30, "straight": 40, "yahtzee": 50}

# a list of the keys of the combinations dictionary
COMBINATIONS_KEYS = [*COMBINATIONS]


UPPER_SECTION = ["one", "two", "three", "four", "five", "six"]
MEDIUM_SECTION = ["min", "max"]
LOWER_SECTION = ["fullhouse", "fourofakind", "straight", "yahtzee"]

BONUS_AND_TOTAL = ["totalup", "bonus", "totalmed", "totallow", "columntotal"]

ROWS = UPPER_SECTION + ["totalup", "bonus"] + MEDIUM_SECTION + ["totalmed"] + LOWER_SECTION + ["totallow", "columntotal"]
COLUMNS = ["free", "ascending", "descending", "betcol"]

NUMBER_OF_BOXES = len(COLUMNS) * len(COMBINATIONS.keys())

ACTIONS = ["roll", "fill", "bet"]
