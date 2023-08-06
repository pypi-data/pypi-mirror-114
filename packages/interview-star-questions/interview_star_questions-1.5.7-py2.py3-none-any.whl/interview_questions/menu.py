""" This module houses the menu for the entire program, along with the `Option` helper class.
"""
import os
import subprocess
import sys

from .printer import Printer
from . import commands

printer = Printer()
questions = commands.Questions()
answers = commands.Answers()
tips = commands.Tips()
notes = commands.Notes()


def clear_screen(return_data=None):
    clear = 'cls' if os.name == 'nt' else 'clear'
    print("\n" * 150)
    subprocess.call(clear, shell=True)
    return None


def reset_program(return_data=None):
    """ Reset entire program to defaults. """
    make_sure = input('Are you sure you want to reset the program? Y/N: ')
    if make_sure.upper() == 'Y':
        clear_screen()
        printer.print_title_bar('Reset Program')
        questions.reset_to_default(title=False)
        answers.reset_to_default(title=False)
        tips.reset_to_default(title=False)
        notes.reset_to_default(title=False)
    else:
        print('That was a close call!')
        print('\n\n')
    return None


def exit_program(return_date=None):
    sys.exit('👍 👍 👍 THANKS FOR PRACTICING 👍 👍 👍')


class Option:
    """ Class for holding each of the menu options """
    def __init__(self, name, menu_to_print, command):
        self.name = name
        self.menu_to_print = menu_to_print
        self.command = command

    def execute(self, return_data):
        if return_data:
            return self.command(return_data)
        return self.command()


class Menu:
    """ Class for holding and displaying all of the menus.

    Parameters
    ----------
    current_menu : `str`
        Menu assigned by `get_menu` method for use in `print_menu` method.
        Menus are not attached to methods, any menu can be printed after any method call.

    """
    def __init__(self):
        self.current_menu = 'main'
        self._menus = {
            'main': {

                # (name, menu, command)
                '1': Option('Get a Random Question', 'single_question', questions.get_random_question),
                '2': Option('Get a Random Unanswered Question', 'single_question', questions.get_random_question),
                '3': Option('Questions Menu', 'questions', clear_screen),
                '4': Option('Answers Menu', 'answers', clear_screen),
                '5': Option('Notes Menu', 'notes', clear_screen),
                '6': Option('Tips Menu', 'tips', clear_screen),
                'R': Option('Reset Program to Defaults', 'main', reset_program),
                'Q': Option('Quit Program', 'main', exit_program)
            },
            'questions': {
                '1': Option('Get a Random Question', 'single_question', questions.get_random_question),
                '2': Option('Get a Random Unanswered Question', 'single_question', questions.get_random_unanswered_question),
                '3': Option('View Answered Questions', 'questions', questions.view_answered),
                'A': Option('View All Questions', 'questions', questions.view_all_questions),
                'B': Option('View a Question by ID', 'single_question', questions.view_question_by_id),
                'C': Option('Add a question', 'questions', questions.add_question),
                'D': Option('Edit a question', 'questions', questions.edit_question),
                'E': Option('Delete a question', 'questions', questions.delete_question),
                'F': Option('Delete All questions', 'questions', questions.delete_all),
                'G': Option('Reset questions to Default', 'questions', questions.reset_to_default),
                'M': Option('Return to Main Menu', 'main', clear_screen),
                'Q': Option('Quit Program', 'main', exit_program)
            },
            'answers': {
                'B': Option('View an answer by ID', 'single_answer', answers.view_answer_by_id),
                'C': Option('Add an answer', 'answers', answers.add_answer),
                'D': Option('Edit an answer', 'answers', answers.edit_answer),
                'E': Option('Delete an answer', 'answers', answers.delete),
                'F': Option('Delete All answers', 'answers', answers.delete_all),
                'G': Option('Reset answers to Default', 'answers', answers.reset_to_default),
                'M': Option('Return to Main Menu', 'main', clear_screen),
                'Q': Option('Quit Program', 'main', exit_program)
            },
            'notes': {
                'B': Option('View a note by ID', 'single_note', notes.view_note_by_id),
                'C': Option('Add a note', 'notes', notes.add_note),
                'D': Option('Edit a note', 'notes', notes.edit_note),
                'E': Option('Delete a note', 'notes', notes.delete),
                'F': Option('Delete All notes', 'notes', notes.delete_all),
                'G': Option('Reset notes to Default', 'notes', notes.reset_to_default),
                'M': Option('Return to Main Menu', 'main', clear_screen),
                'Q': Option('Quit Program', 'main', exit_program)
            },
            'tips': {
                'B': Option('View a tip by ID', 'single_tip', tips.view_tip_by_id),
                'C': Option('Add a tip', 'tips', tips.add_tip),
                'D': Option('Edit a tip', 'tips', tips.edit_tip),
                'E': Option('Delete a tip', 'tips', tips.delete),
                'F': Option('Delete All tips', 'tips', tips.delete_all),
                'G': Option('Reset tips to Default', 'tips', tips.reset_to_default),
                'M': Option('Return to Main Menu', 'main', clear_screen),
                'Q': Option('Quit Program', 'main', exit_program)
            },
            'single_question': {
                '1': Option('View All Question Info', 'single_question', questions.view_all_info),
                '2': Option('Add an Answer to this Question', 'single_question', answers.add_answer),
                '3': Option('Add a Note to this Question', 'single_question', notes.add_note),
                '4': Option('Add a Tip to this Question', 'single_question', tips.add_tip),
                'E': Option('Edit this Question', 'single_question', questions.edit_question),
                'D': Option('Delete this Question', 'questions', questions.delete_question),
                'R': Option('Return to Questions Menu', 'questions', clear_screen),
                'M': Option('Return to Main Menu', 'main', clear_screen),
                'Q': Option('Quit Program', 'main', exit_program)
            },
            'single_answer': {
                'E': Option('Edit this Answer', 'answers', answers.edit_answer),
                'D': Option('Delete this Answer', 'answers', answers.delete),
                'R': Option('Return to Answers Menu', 'answers', clear_screen),
                'M': Option('Return to Main Menu', 'main', clear_screen),
                'Q': Option('Quit Program', 'main', exit_program)
            },
            'single_note': {
                'E': Option('Edit this Note', 'notes', notes.edit_note),
                'D': Option('Delete this Note', 'notes', notes.delete),
                'R': Option('Return to Notes Menu', 'notes', clear_screen),
                'M': Option('Return to Main Menu', 'main', clear_screen),
                'Q': Option('Quit Program', 'main', exit_program)
            },
            'single_tip': {
                'E': Option('Edit this Tip', 'tips', tips.edit_tip),
                'D': Option('Delete this Tip', 'tips', tips.delete),
                'R': Option('Return to Tips Menu', 'tips', clear_screen),
                'M': Option('Return to Main Menu', 'main', clear_screen),
                'Q': Option('Quit Program', 'main', exit_program)
            },
        }

    def _option_choice_is_valid(self, choice, options):
        return choice in options

    def get_command(self):
        """ Retrieves user input for command, validates against available options.
        Side effect: Sets `current_menu` for menu to print after command is executed.

        Returns
        -------
        command: `func`
            Function to execute.
        """
        submenu = self._menus.get(self.current_menu)
        choice = input('Choose option: ').upper()
        while not self._option_choice_is_valid(choice, options=submenu):
            print()
            print(f'Invalid option: "{choice}"')
            print()
            choice = input('Choose option: ').upper()
        command = submenu.get(choice)
        self.current_menu = command.menu_to_print
        return command

    def print_menu(self):
        """Print `current_menu` set by `get_command` method"""
        border = '⑊ '
        width = (80 - len(self.current_menu)) // 6
        padding = 5
        menu_string = f'{border*width}{" "*padding}{self.current_menu.upper()} MENU{" "*padding}{border*width}'
        q, r = divmod(len(menu_string), len(border))
        adjusted_menu_string = f'{border*width}{" "*padding}{self.current_menu.upper()} MENU{" "*padding}{" "*r}{border*width}'
        print(border * (q + r))
        print(' ' + adjusted_menu_string)
        print('  ' + border * (q + r))
        print()
        submenu = self._menus.get(self.current_menu)
        for key, option in submenu.items():
            print(f'{key} : {option.name}')
            print()
