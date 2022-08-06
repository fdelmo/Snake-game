from gui.gui import GUI


def main() -> None:
    """
    Main function of the program.
    """

    gui = GUI("SnAIke Prototype", (15, 10))

    gui.WelcomeScreen()

    gui.window.mainloop()


if __name__ == '__main__':
    main()
