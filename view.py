import tkinter as tk
from functools import partial
from tkinter import INSERT

from controller import GamePageController, ChooseSeedPageController

import constant as cst
from exception import *
from observer import Subscriber

# the global seed, which is modified in the application and keeps its new value from a frame to another.
seed = ""

WIDTH = 5
HEIGHT = 2
IPADX = 3
IPADY = 3
PADX = 3
PADY = 3

class SampleApp(tk.Tk):
    """
    The SampleApp class is the main window of the application.
    It contains and shows the frames, whenever it is asked by the user.
    """

    def __init__(self, *args, **kwargs):
        """
        The constructor of the SampleApp class.
        It initializes all the frames the application needs. Those frames are its attributes.
        """

        # call the Tk controller, the parent class of the SampleApp class.
        tk.Tk.__init__(self, *args, **kwargs)
        # initialize and pack the first frame of the application on which every other will be packed.
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        # initialize every frame of the application
        self.frames = {}
        for frame_class in (StartPage, GamePage, ChooseSeedPage):
            # give to every page the name of the corresponding class
            page_name = frame_class.__name__
            # initialize every frame and associate it to a parent (the container) and to a controller (the TK)
            frame = frame_class(parent=container, tk_controller=self)
            self.frames[page_name] = frame
            # pack the frame
            frame.grid(row=0, column=0, sticky="nsew")
        # show the start page of the application
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """
        Show a frame for the given page name
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def update_seed(self):
        """
        Update the seed value to its new value for every frame.
        """
        for frame in self.frames.values():
            frame.update_seed()


class YamFrame(tk.Frame):
    """
    The YamFrame class every frame of the application inherit from.
    It exists to ensure that every frame implements the update_seed and the update_error methods.
    """

    def __init__(self, parent, tk_controller):
        """
        The constructor of the YamFrame class.
        """
        tk.Frame.__init__(self, parent)
        self.tk_controller = tk_controller
        self.text_error = tk.Text(self)

    def update_seed(self) -> None:
        """
        Update the seed widget of the frame (for example the label where it is shown).
        """
        pass

    def update_error(self, error_message: str):
        """
        Update the error text widget of the frame.
        """
        self.text_error.configure(state='normal')
        self.text_error.insert(INSERT, error_message)
        self.text_error.configure(state='disabled')


class StartPage(YamFrame):
    """
    The first frame of the application, where the user can choose to change the seed or to start a new game.
    """

    def __init__(self, parent, tk_controller):
        """
        The constructor of the StartPage class.
        It is composed of two buttons : one to start a new game (i.e. switch to GamePage frame), the other to choose a
        seed (i.e. switch to ChooseSeedPage frame).
        Show the current seed value.
        """

        # define the seed as global.
        global seed
        # init the super constructor YamFrame.
        YamFrame.__init__(self, parent, tk_controller)
        # init the seed label variable
        self.seed_label_var = tk.StringVar()
        self.seed_label_var.set("Seed : Random")
        # init the switching page buttons and pack it
        start_game_button = tk.Button(self, text="Start Game",
                                      command=lambda: tk_controller.show_frame("GamePage"))
        choose_seed_button = tk.Button(self, text="Choose Seed",
                                       command=lambda: tk_controller.show_frame("ChooseSeedPage"))
        start_game_button.pack()
        choose_seed_button.pack()
        # init and pack the seed label
        seed_label = tk.Label(self, textvariable=self.seed_label_var)
        seed_label.pack()

    def update_seed(self) -> None:
        """
        Update the seed label variable, according to the choice made by the user.
        """
        global seed
        if seed != "":
            self.seed_label_var.set("Seed : " + seed)
        else:
            self.seed_label_var.set("Seed : Random")


class GamePage(YamFrame, Subscriber):
    """
    The GamePage class is the frame where all the game is played.
    It is a subscriber of a game (of the Game class) in order to be notified whenever the game is updated.
    """

    def __init__(self, parent, tk_controller):
        """
        The constructor of the GamePage class.
        It initializes all the element of the page (the action buttons, the grid, etc.).
        """

        # define the seed as global.
        global seed

        # initialize the game controller of the page, which checks the request of the user and sends it to the model.
        if seed == "":
            self.game_controller = GamePageController(self)
        else:
            seed_int = int(seed)
            self.game_controller = GamePageController(self, seed_int)

        # init the super constructor YamFrame.
        YamFrame.__init__(self, parent, tk_controller)
        self.tk_controller = tk_controller

        # create all the variables which are associated to all the widgets of the page
        self.seed_label_var = tk.StringVar()
        self.roll_number_var = tk.StringVar()
        self.turn_var = tk.StringVar()
        self.bet_var = tk.StringVar()
        self.total_and_bonus_var = {}
        self.boxes_button = {}
        self.box_radio_var = tk.StringVar()
        self.dices_button = []  # list which contains the dices widgets
        self.dice_var = []
        self.action_button = {}  # every action (fill, roll, bet) is associated with a button in this dictionary
        self.final_score_var = tk.StringVar()

        # init the variables associated to labels
        self.seed_label_var.set("Seed : Random")
        self.roll_number_var.set("Roll Number : 0")
        self.turn_var.set("Turn : 0")
        self.bet_var.set("Bet : None")
        self.final_score_var.set("Final Score : ")

        # pack some labels in the grid.
        tk.Label(self, textvariable=self.seed_label_var).grid(row=0, column=0)
        tk.Label(self, textvariable=self.roll_number_var).grid(row=0, column=1)
        tk.Label(self, textvariable=self.turn_var).grid(row=0, column=2)
        tk.Label(self, textvariable=self.bet_var).grid(row=0, column=3)

        # an iterator that contains the number of rows of the grid
        max_row_index = 0

        # Init the game grid.
        # The first column and row are the entries of the game grid. It shifts all the content of the grid. That's why
        # it is shifted back, using cst.COLUMNS[i-1] or cst.ROWS[i-1] (instead of cst.COLUMNS[i] or cst.ROWS[i]).
        for col_index in range(len(cst.COLUMNS) + 1):
            self.grid_columnconfigure(col_index, weight=1)
            for row_index in range(len(cst.ROWS) + 1):
                # the first row of the grid is made of column type (free, ascending, descending, betcol) labels.
                if row_index == 0 and col_index != 0:
                    max_row_index += 1
                    tk.Label(self, text=cst.COLUMNS[col_index - 1]).grid(row=row_index + 1, column=col_index)
                # the first col of the grid is made of the rows (one to column_total) labels.
                elif col_index == 0 and row_index != 0:
                    max_row_index += 1
                    tk.Label(self, text=cst.ROWS[row_index - 1]).grid(row=row_index + 1, column=col_index)
                # the inner grid is filled with the score obtained during the game.
                elif col_index != 0 and row_index != 0:
                    current_row = cst.ROWS[row_index - 1]
                    current_col = cst.COLUMNS[col_index - 1]
                    # when the current row corresponds to a bonus or a total, create a label showing the current value
                    # of the box.
                    if current_row in cst.BONUS_AND_TOTAL:
                        if current_col not in self.total_and_bonus_var:
                            self.total_and_bonus_var[current_col] = {}
                        self.total_and_bonus_var[current_col][current_row] = tk.IntVar()
                        tk.Label(self, textvariable=self.total_and_bonus_var[current_col][current_row]) \
                            .grid(row=row_index + 1, column=col_index)
                    # all the boxes can be filled by the user and are buttons.
                    else:
                        self.boxes_button[current_col] = {}
                        self.boxes_button[current_col][current_row] = \
                            tk.Radiobutton(self, variable=self.box_radio_var, text="",
                                           value={f"{current_col}_{current_row}"}, indicatoron=False,
                                           activebackground="yellow", width=WIDTH, height=HEIGHT)
                        self.boxes_button[current_col][current_row].grid(row=row_index + 1, column=col_index)

        # init the dices checkbuttons the user selects to roll.
        for j in range(cst.NUMBER_OF_DICES):
            self.dice_var.append(tk.IntVar())
            self.dices_button.append(tk.Checkbutton(self, text=cst.DEFAULT_DICE_VALUE, variable=self.dice_var[j],
                                                    onvalue=j, offvalue=-1, indicatoron=False,
                                                    width=WIDTH, height=HEIGHT))
            self.dices_button[j].grid(row=1 + max_row_index, column=j)
            self.dices_button[j].deselect()

        max_row_index += 1

        # init the action buttons the player uses to confirm his or her choice.
        for action_index in range(len(cst.ACTIONS)):
            action = cst.ACTIONS[action_index]
            self.action_button[action] = tk.Button(self, text=action.upper(), command=partial(self.play, action),
                                                   width=WIDTH, height=HEIGHT)
            self.action_button[action].grid(row=max_row_index + 1, column=action_index)

        max_row_index += 1

        # init the label to show the final score.
        tk.Label(self, textvariable=self.final_score_var).grid(row=max_row_index + 1, column=0)

        max_row_index += 1

        # pack the text_error
        self.text_error.grid(row=max_row_index + 1, column=0, columnspan=5)

    def play(self, action: str) -> None:
        """
        Creates the request, according to the choices of the user and the action button he clicked on, and sends it to
        the game controller.
        """

        # the request is a dictionary containing the type of action made by the user (roll, fill, bet) and its details
        request = {"action": action}

        # if the action is "roll", add an entry whose key is "dices" and the value is a list of the dices chosen by the
        # user to be rolled.
        if action == "roll":
            dices = set()
            for i in range(len(self.dice_var)):
                if self.dice_var[i].get() == i:
                    dices.add(i)
            request["dices"] = dices

        # if the action is "fill" or "bet", add two entries whose keys are "col" and "row" and the values are the
        # corresponding column or row chosen by the user.
        elif action == "fill" or action == "bet":
            value = self.box_radio_var.get()
            if self.box_radio_var.get():
                col, row = value.split(sep="_")
                request["col"] = col
                request["row"] = row

        try:
            # send the request to the controller.
            self.game_controller.play(request)
        except (UserRequestException, GameRulesException) as error:
            # update the error text widget
            self.update_error(str(error))

    def update_seed(self) -> None:
        """
        Update the seed label variable, according to the choice made by the user.
        """
        global seed
        self.seed_label_var.set("Seed : " + seed)

    def update_subscriber(self, context: dict):
        """
        Override the update_subscriber method of the Subscriber parent class.
        Update the GamePage widgets when the game (from the model) is modified.
        The context is a dictionary containing all the modifications of the game.
        """

        # update the bet label
        bet = context["bet"]
        if bet == "":
            self.bet_var.set("Bet : None")
        else:
            self.bet_var.set("Bet : " + bet)

        # update the roll_number label
        roll_number = context["roll_number"]
        self.roll_number_var.set("Roll Number : " + str(roll_number))

        # update the turn label
        turn = context["turn"]
        self.turn_var.set("Turn : " + str(turn))

        # update the final_score label
        final_score = context["final_score"]
        self.final_score_var.set("Final Score : " + str(final_score))

        # update the dices buttons and variables
        dices = context["dices"]
        for i in range(len(dices)):
            self.dice_var[i].set(dices[i])
            self.dices_button[i].config(text=dices[i])
            self.dices_button[i].deselect()
            # if the roll_number has reached the maximum rolls per turn allowed, the buttons are set to DISABLED
            if roll_number == cst.ROLLS_PER_TURN:
                self.dices_button[i].config(state=tk.DISABLED)
            else:
                self.dices_button[i].config(state=tk.NORMAL)

        # update the box which has been filled
        if "fill" in context.keys():
            fill = self["fill"]
            row = fill["row"]
            col = fill["col"]
            value = fill["value"]
            # the box button can't be pressed anymore
            self.boxes_button[col][row].config(text=value, state=tk.DISABLED)
            self.boxes_button[col][row].deselect()

        # update the bonus and total box
        for key in cst.BONUS_AND_TOTAL:
            if key in context.keys():
                bonus_or_tot = context[key]
                col = bonus_or_tot["col"]
                value = bonus_or_tot["value"]
                self.total_and_bonus_var[col][key].set(value)

        # update the action buttons : set to DISABLED depending on the roll number
        if roll_number == 0:
            self.action_button["fill"].config(state=tk.DISABLED)
        else:
            self.action_button["fill"].config(state=tk.NORMAL)

        if roll_number != 1 or bet != "":
            self.action_button["bet"].config(state=tk.DISABLED)
        else:
            self.action_button["bet"].config(state=tk.NORMAL)

        if roll_number == 3:
            self.action_button["roll"].config(state=tk.DISABLED)
        else:
            self.action_button["roll"].config(state=tk.NORMAL)

        # if the game is over (i.e. the final_score isn't empty), DISABLED all the action buttons.
        if final_score != "":
            self.action_button["roll"].config(state=tk.NORMAL)
            self.action_button["fill"].config(state=tk.DISABLED)
            self.action_button["bet"].config(state=tk.DISABLED)


class ChooseSeedPage(YamFrame):
    """
    The ChooseSeedPage class is the frame where the seed is chosen.
    """

    def __init__(self, parent, tk_controller):
        """
        The constructor of the ChooseSeedPage class.
        """

        # the seed is set to global
        global seed
        # init the variable to be shown in the seed label.
        self.seed_var = tk.StringVar()
        # call the super constructor (the YamFrame constructor)
        YamFrame.__init__(self, parent, tk_controller)
        self.tk_controller = tk_controller
        # init the seed controller, used to check if the request made by the user is valid
        self.seed_controller = ChooseSeedPageController()
        # init all the widgets (a label, the set text entry and the confirm button)
        seed_label = tk.Label(self, text="Seed")
        seed_label.pack()
        seed_entry = tk.Entry(self, textvariable=self.seed_var)
        seed_entry.pack()
        # the confirm button
        confirm_button = tk.Button(self, text="Confirm", command=lambda: self.confirm_seed())
        confirm_button.pack()
        # the error text
        self.text_error.pack()

    def confirm_seed(self):
        """
        Confirm the seed choice of the user.
        If there is an error, show it, otherwise switch to the start page.
        """

        try:
            # check if the user entry is valid
            self.seed_controller.check_seed(self.seed_var.get()),
            # change the seed
            self.__set_seed(),
            # update the seed view on every frame of the application
            self.tk_controller.update_seed(),
            # switch to the starting page
            self.tk_controller.show_frame("StartPage")
        except (UserRequestException, GameRulesException) as error:
            # show the error
            self.update_error(str(error))

    def __set_seed(self):
        """
        Update the global seed to the value set by the user.
        """
        global seed
        seed = self.seed_var.get()
        self.seed_var.set("")


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
