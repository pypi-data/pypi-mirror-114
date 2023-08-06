""" This is the main entry point to this program, through the command line
"""

from . import commands, defaults
from .menu import Menu, clear_screen


def main():
    """ Main function to run the command line program"""
    first_run = commands.check_for_first_run()

    questions = commands.Questions(defaults=defaults.default_questions)
    questions.create_table()

    answers = commands.Answers()
    answers.create_table()

    tips = commands.Tips()
    tips.create_table()

    notes = commands.Notes()
    notes.create_table()

    if first_run:
        questions._populate_defaults()

    clear_screen()
    menu = Menu()

    menu.print_menu()
    return_data = None

    while True:
        command = menu.get_command()
        clear_screen()
        return_data = command.execute(return_data=return_data)
        menu.print_menu()


if __name__ == '__main__':
    main()
