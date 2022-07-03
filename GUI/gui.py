from pickle import FRAME
import tkinter as tk
from turtle import down
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
        pass


if __name__ == '__main__':
    gui = GUI("SnAIke Prototype", (15, 10))

    gui.WelcomeScreen()

    # main loop
    gui.window.mainloop()
