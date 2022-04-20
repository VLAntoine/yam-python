from Hand import *
from observer import *
import random

SEED_ROOT = 17

random.seed(SEED_ROOT)

SEED_ARRAY = [random.randint(0, 2**32 - 1) for i in range(48)]




COMBINATIONS = {"one" : 1, "two" : 2, "three" : 3, "four" : 4, "five" : 5, "six" : 6, "min" : 0, "max" : 0, "fullhouse" : 20, "fourofakind" : 30, "straight" : 40, "yahtzee" : 50}

columns = ["free", "ascending", "descending", "betcol"]
rows = ["one", "two", "three", "four", "five", "six", "totalup", "bonus", "min", "max", "totalmed", "fullhouse", "fourofakind", "straight", "yahtzee", "totallow", "columntotal"]


class Game():

	def __init__(self):

		self.turn = 0

		self.roll_number = 0

		self.hand = Hand()

		self.grid = {}
		for column in columns:
			self.grid[column] = {}
			for row in rows:
				self.grid[column][row] = "empty"

		self.bet_value = None

		self.final_score = "empty"
	

	def roll(self, dice_to_roll = range(5)):
		
		if self.roll_number == 0:

			random.seed(SEED_ARRAY[self.turn])

		self.hand.roll(dice_to_roll)
		self.roll_number += 1
		

	def set_bet(self, row):
		self.bet_value = row


	def fill(self, col, row):


		if row in ["one", "two", "three", "four", "five", "six"]:
			dice_value = COMBINATIONS[row]
			self.grid[col][row] = dice_value * self.hand.get_dice_array_dictionary()[dice_value]

			up_array = [self.grid[col]["one"], self.grid[col]["two"], self.grid[col]["three"], self.grid[col]["four"], self.grid[col]["five"], self.grid[col]["six"]]

			if not ("empty" in up_array):
				self.grid[col]["totalup"] = sum(up_array)
				if self.grid[col]["totalup"] >= 60:
					self.grid[col]["bonus"] = 30
				else:
					self.grid[col]["bonus"] = 0


		elif row in ["min", "max"]:
			self.grid[col][row] = sum(self.hand.dice_arr)
			if (self.grid[col]["min"] != "empty") and (self.grid[col]["max"] != "empty"):
				if (self.grid[col]["min"] >= self.grid[col]["max"]) :
					self.grid[col]["totalmed"] = 0
				else:
					self.grid[col]["totalmed"] = self.grid[col]["min"] + self.grid[col]["max"]


		elif row in ["fullhouse", "fourofakind", "straight", "yahtzee"]:
			if (self.hand.is_combination(row)):
				self.grid[col][row] = COMBINATIONS[row]
			else:
				self.grid[col][row] = 0

			low_array = [self.grid[col]["fullhouse"], self.grid[col]["fourofakind"], self.grid[col]["straight"], self.grid[col]["yahtzee"]]

			if (not "empty" in low_array):
				self.grid[col]["totallow"] = sum(low_array)


		subtotal_arr = [self.grid[col]["totalup"], self.grid[col]["totalmed"], self.grid[col]["totallow"], self.grid[col]["bonus"]]

		if (not "empty" in subtotal_arr):
			self.grid[col]["columntotal"] = sum(subtotal_arr)


		self.is_over()

		self.turn += 1
		self.roll_number = 0
		self.hand = Hand()
		self.bet_value = None



	def is_over(self):
		column_totals = [self.grid["free"]["columntotal"], self.grid["ascending"]["columntotal"], self.grid["descending"]["columntotal"], self.grid["betcol"]["columntotal"]]

		if ("empty" not in column_totals):
			self.final_score = sum(column_totals)
			return True

		else:
			return False