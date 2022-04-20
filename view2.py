from observer import *
from Controller import *
import tkinter as tk
from tkinter import *
from functools import partial
from math import *


WIDTH_WINDOW_RATIO  = 1 / 2
HEIGHT_WINDOW_RATIO = 4 / 5
PADY = 3
PADX = 3


class Tkinter_View():

	def __init__(self):



		self.controller = Controller()
		self.root = Tk()
		self.root.title("yams")

		screen_width  = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()

		"""self.root_width  = floor(screen_width * WIDTH_WINDOW_RATIO)
		self.root_height = floor(screen_height * HEIGHT_WINDOW_RATIO)

		self.root.geometry(f"{self.root_height}x{self.root_height}")"""

		self.root.geometry("400x610")

		self.box_variable  = StringVar(self.root, "box")
		self.dice_variable = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
		
		self.dice_buttons = []
		self.grid_buttons = {}
		self.text_bonus_and_total = {}
		
		self.text_error = Text(self.root, height=1, padx = PADX, pady = PADY)
		self.text_roll  = Text(self.root, width=10, height=1, padx = PADX, pady = PADY)
		self.text_final_score = Text(self.root, width=10, height=1, padx = PADX, pady = PADY)
		self.text_bet = Text(self.root, width=10, height=1, padx = PADX, pady = PADY)

		for i in range(6):
			self.root.grid_columnconfigure(i, weight=1, uniform="foo")






		for j in range(len(columns)+1):
			
			for i in range(len(rows)+1):

				if j != 0 or i != 0:

					if i == 0:
						text = Text(self.root, width=10, height=1, padx = PADX, pady = PADY)
						text.tag_configure("tag_name", justify='center')
						text.insert(END, columns[j-1])
						text.grid(row = i,column = j)
						text.tag_add("tag_name", "1.0", "end")
						text.configure(state = 'disabled')

					elif j==0:
						text = Text(self.root, width=10, height=1, padx = PADX, pady = PADY)
						text.tag_configure("tag_name", justify='center')
						text.insert(END, rows[i-1])
						text.grid(row = i,column = j)
						text.tag_add("tag_name", "1.0", "end")
						text.configure(state = 'disabled')

					elif rows[i-1] in ["totalup", "bonus", "totalmed", "totallow", "columntotal"]:
						self.text_bonus_and_total[(f"{columns[j-1]}", f"{rows[i-1]}")] = Text(self.root, width=10, height=1, padx = PADX, pady = PADY, bg="green")
						text = self.text_bonus_and_total[(f"{columns[j-1]}", f"{rows[i-1]}")]
						text.tag_configure("tag_name", justify='center')
						text.insert(END, "")
						text.grid(row = i,column = j)
						text.tag_add("tag_name", "1.0", "end")
						text.configure(state = 'disabled')

					else:
						self.grid_buttons[(f"{columns[j-1]}", f"{rows[i-1]}")] = Radiobutton(self.root, variable=self.box_variable, text="", value=f"{columns[j-1]}_{rows[i-1]}", indicatoron = 0, activebackground="yellow", width=10, height=1, padx = PADX, pady = PADY)
						self.grid_buttons[(f"{columns[j-1]}", f"{rows[i-1]}")].grid(row = i,column = j)


		text = Text(self.root, height=1, padx = PADX, pady = PADY, bg="blue")
		text.tag_configure("tag_name", justify='center')
		text.insert(END, "DICES")
		text.grid(row = 18,column = 0, columnspan = 5)
		text.tag_add("tag_name", "1.0", "end")
		text.configure(state = 'disabled')


		for j in range(5):
			button = Checkbutton(self.root, text=1, variable=self.dice_variable[j], onvalue=f"{j}", offvalue="", indicatoron = 0, width=10, height=3, padx = PADX, pady = PADY)
			button.grid(row = 19, column = j)
			self.dice_buttons.append(button)


		action_list = ["ROLL", "FILL", "BET"]

		for i in range(len(action_list)):

			button = Button(self.root, text=action_list[i], width=10, height=1, padx = PADX, pady = PADY, command = partial(self.play, action_list[i].lower()))
			button.grid(row = 1+i, column = 5, columnspan = 3)


		self.text_error.tag_configure("tag_name", justify='center')
		self.text_error.insert(END, "")
		self.text_error.grid(row = 20,column = 0, columnspan = 5)
		self.text_error.tag_add("tag_name", "1.0", "end")
		self.text_error.configure(state = 'disabled')

		self.text_roll.tag_configure("tag_name", justify='center')
		self.text_roll.insert(END, "0")
		self.text_roll.grid(row = 0,column = 6)
		self.text_roll.tag_add("tag_name", "1.0", "end")
		self.text_roll.configure(state = 'disabled')

		self.text_final_score.tag_configure("tag_name", justify='center')
		self.text_final_score.insert(END, "")
		self.text_final_score.grid(row = 20,column = 6)
		self.text_final_score.tag_add("tag_name", "1.0", "end")
		self.text_final_score.configure(state = 'disabled')

		self.text_bet.tag_configure("tag_name", justify='center')
		self.text_bet.insert(END, "")
		self.text_bet.grid(row = 19,column = 6)
		self.text_bet.tag_add("tag_name", "1.0", "end")
		self.text_bet.configure(state = 'disabled')



		self.root.mainloop()




	def play(self, action):

		request = ""

		if action == "roll":
			dice_str = ""
			for i in range(len(self.dice_buttons)):
				if self.dice_variable[i].get() != "":
					dice_str += self.dice_variable[i].get()

			if dice_str == "":
				request = "roll"
			else:
				request = "roll" + "_" + dice_str


		elif action == "fill":
			request = "fill_" + self.box_variable.get()

		elif action == "bet":
			request = "bet_" + self.box_variable.get()

		response = self.controller.play(request)

		self.update_view(response)




	def update_view(self, response):

		if "error" in response.keys():

			clear_text_box(self.text_error)
			update_text_box(self.text_error, response["error"])

		else:

			clear_text_box(self.text_error)

			clear_text_box(self.text_roll)
			update_text_box(self.text_roll, response["roll_number"])


			for i in range(len(response["dices"])):
				self.dice_buttons[i].config(text=response["dices"][i])
				self.dice_buttons[i].deselect()


			if (response["bet_value"] != None):
				clear_text_box(self.text_bet)
				update_text_box(self.text_bet, response["bet_value"])
			else:
				clear_text_box(self.text_bet)


			if "grid" in response.keys():

				grid_response = response["grid"]

				for col in columns:
			
					for row in rows:

						if row in ["totalup", "bonus", "totalmed", "totallow", "columntotal"]:

							if (grid_response[col][row] != "empty"):
								clear_text_box(self.text_bonus_and_total[(col,row)])
								update_text_box(self.text_bonus_and_total[(col,row)], grid_response[col][row])

						else:

							if (grid_response[col][row] != "empty"):
								self.grid_buttons[(col,row)].config(text=grid_response[col][row], state = DISABLED)
								self.grid_buttons[(col,row)].deselect()


			if "final_score" in response.keys():

				update_text_box(self.text_final_score, response["final_score"])





def clear_text_box(text_box):
	text_box.configure(state = 'normal')
	text_box.delete("1.0", END)
	text_box.configure(state = 'disabled')


def update_text_box(text_box, text_str):
	text_box.configure(state = 'normal')
	text_box.insert(INSERT, text_str)
	text_box.configure(state = 'disabled')


view = Tkinter_View()





		


