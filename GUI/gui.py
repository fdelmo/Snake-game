import tkinter as tk
from typing import *


class GUI:
    """Class to encapsulate all matters of grapghical user interface
    functions and definitions"""

    def __init__(self, title: str, pad: tuple) -> None:
        self.window = tk.Tk()
        self.window.title(title)
        # MAY NOT WORK, TRY WRITING SEPARATED OR * NOTATION
        self.window.config(padx=pad[0], pady=[1])
        self.window.eval('tk::PlaceWindow . center')
        self.welcome_text = "This is a prototype to test the GUI of SnAIke. \n Enjoy the ride!"

    def clean_window(self) -> None:
        """
        Method to remove the widgets and sprites in window and clean it 
        before rendering the next screen.
        """
        for widget in self.window.winfo_children():
            widget.destroy()

    def WelcomeScreen(self) -> None:
        """
        Welcome screen with welcome message, play button and learn more button.
        """
        self.window.geometry('675x400')  # TODO: decide on final size

        frame = tk.Frame(self.window)
        frame.config(pady=150)
        frame.pack(side=tk.TOP)

        lbl = tk.Label(frame, text=self.welcome_text)
        lbl.config(padx=2, pady=10, justify=tk.CENTER)
        lbl.pack(side=tk.TOP)

        button = tk.Button(frame, text="Start", command=self.InitialMenu)
        button.config(relief=tk.RAISED, padx=8, pady=4)
        button.pack(side=tk.BOTTOM)

    def InitialMenu(self) -> None:
        """
        Start menu of the game, where we can choose between playing solo,
        multiplayer, vs AI or view records.
        """

        # clean the window of widgets and sprites
        self.clean_window()

        # Setting the frames
        frameu = tk.Frame(self.window)
        frameu.pack(side=tk.TOP)

        framed = tk.Frame(self.window)
        framed.pack(side=tk.BOTTOM)

        frame1ua = tk.Frame(frameu)
        frame1ua.pack(side=tk.LEFT)

        frame1ub = tk.Frame(frameu)
        frame1ub.pack(side=tk.RIGHT)

        frame2ua = tk.Frame(framed)
        frame2ua.pack(side=tk.LEFT)

        frame2ub = tk.Frame(framed)
        frame2ub.pack(side=tk.RIGHT)

        # setting the buttons
        buttons_config = {
            "relief": tk.RAISED,
            "padx": 8,
            "pady":  4
        }

        button_solo = tk.Button(
            frame1ua,
            text='Play solo',
            # command=pass,
            **buttons_config
        )

        button_multiplayer = tk.Button(
            frame1ub,
            text='Play Multiplayer',
            # command=pass,
            **buttons_config
        )

        button_AI = tk.Button(
            frame2ua,
            text='Play vs AI',
            # command=pass,
            **buttons_config
        )

        button_records = tk.Button(
            frame2ub,
            text='View Records',
            # command=pass,
            **buttons_config
        )

        # TODO: Fix the packing situation

        button_solo.pack()
        button_multiplayer.pack()
        button_AI.pack()
        button_records.pack()


if __name__ == '__main__':
    gui = GUI("SnAIke Prototype", (15, 10))

    gui.WelcomeScreen()

    # main looP
    gui.window.mainloop()
