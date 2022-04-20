import random

class Hand:

	def __init__(self):
		self.dice_arr = [1, 1, 1, 1, 1]

	def roll(self, dice_to_roll = range(5)):
		for i in dice_to_roll:
			self.dice_arr[i] = random.randint(1,6)


	def is_combination(self, combination):

		amount_of_values = self.get_dice_array_dictionary().values()

		if combination == "fullhouse":
			if (3 in amount_of_values and 2 in amount_of_values) or (5 in amount_of_values): 
				return True
			else:
				return False

		elif combination == "fourofakind":
			if 4 in amount_of_values or 5 in amount_of_values:
				return True
			else: 
				return False

		elif combination == "straight":
			if (max(amount_of_values) == 1) and (not (1 in self.dice_arr and 6 in self.dice_arr)):
				return True
			else:
				return False

		elif combination == "yahtzee":
			if (5 in amount_of_values):
				return True
			else: 
				return False 


	def get_dice_array_dictionary(self):
		dice_array_dictionary = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
		for dice in self.dice_arr:
			dice_array_dictionary[dice] += 1
		return dice_array_dictionary


	def print(self):
		print(' '.join([str(value) for value in self.dice_arr]), sep=' ')
