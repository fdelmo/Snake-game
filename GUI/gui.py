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

    def WelcomeScreen(self) -> None:
        """
        Welcome screen with welcome message, play button and learn more button.
        """
        self.window.geometry('675x400')

    def InitialMenu(self) -> None:
        pass


if __name__ == '__main__':
    gui = GUI("test", (15, 10))

    gui.WelcomeScreen()
    gui.window.mainloop()
