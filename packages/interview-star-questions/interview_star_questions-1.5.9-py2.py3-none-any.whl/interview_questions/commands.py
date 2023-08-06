""" This module houses all of the commands for adding, editing, and deleting entries into the database.
"""
import pathlib
from appdirs import AppDirs
from .database import DatabaseManager
from .printer import Printer

db_name = 'interview.db'
dirs = AppDirs('interview-star-questions')
data_path = pathlib.Path(dirs.user_data_dir)
pathlib.Path.mkdir(data_path, exist_ok=True)
save_path = data_path.joinpath(db_name)
db = DatabaseManager(save_path)
printer = Printer()


def check_for_first_run():

    return db.table_exists().fetchone()[0] == 0


def get_valid_id(prompt, table_name):
    id = input(f'{prompt}')
    answer = db.id_exists(id, table_name).fetchone()[0]
    while answer < 1:
        print(f'Invalid ID: {id}')
        id = input(f'{prompt}')
        answer = db.id_exists(id, table_name).fetchone()[0]
    return id


def validate_input(input_message, option_map):
    """Validate user input, retry on invalid input

    Parameters
    ----------
    option_map : `dict`
        Dictionary of key-value mappings of valid options
    """
    choice = input(f'{input_message} ').upper()
    while choice not in option_map.keys():
        choice = input(f'{input_message} ').upper()
    return option_map.get(choice)


class Command:
    """Base class for handling all common commands"""

    def __init__(self, defaults):
        self.defaults = defaults

    def _populate_defaults(self):
        for record in self.defaults:
            db.add(self.table_name, record)

    def delete(self, return_data=None):
        printer.print_title_bar('Delete by ID')
        if return_data is not None:
            delete_id = return_data.get('return_id')
        else:
            delete_id = input('ID to Delete: ')
        cursor = db.select(table_name=self.table_name, criteria={'id': delete_id})
        record = cursor.fetchone()
        if record is not None:
            db.delete(self.table_name, {'id': delete_id})
            print()
            print(f'~~ Successfully Deleted {self.table_name[:-1:].capitalize()} ~~')
        else:
            printer.print_no_records()
        return None

    def delete_all(self, return_data=None):
        """Drop and re-create the table"""
        printer.print_title_bar(f'Delete All {self.table_name}')
        self._drop_table()
        self.create_table()
        print(f'~~ Successfully Deleted All {self.table_name.capitalize()} ~~')
        print('\n\n')
        return None

    def reset_to_default(self, return_data=None, title=True):
        """Drop and re-create the table, include defaults if available.

        Parameters
        ----------
        title : `bool`
            Display the title bar.  Set to False when resetting multiple tables at once (`reset_program` function)

        """
        if title:
            printer.print_title_bar(f'Reset All {self.table_name} to Default')
        self._drop_table()
        self.create_table()
        if self.defaults:
            self._populate_defaults()
        print(f'~~ Successfully Set All {self.table_name.capitalize()} to Default ~~')
        print('\n\n')
        return None

    def _drop_table(self, return_data=None):
        db.drop_table(self.table_name)


class Jobs(Command):  # this class and table isn't going to be used in v1.0
    """Jobs commands
    NOTE: This class is not being implemented until v2.0!
    """

    def create_table(self, data=None):
        db.create_table(
            'jobs',
            {
                'id': 'integer primary key autoincrement',
                'job': 'text not null',
                'date_added': 'text',
            },
        )

    def view_practiced(self):
        db.select('jobs', criteria={'reviewed': True})

    def view_not_practiced(self):
        db.select('jobs', criteria={'reviewed': False})


class Questions(Command):
    """Questions commands"""

    def __init__(self, defaults=None, print_fuction=printer.question_printer):
        super().__init__(defaults)
        self.table_name = 'questions'
        self.print_function = print_fuction

    def create_table(self):
        db.create_table(
            self.table_name,
            {
                'id': 'integer primary key autoincrement',
                'question': 'text not null',
                'answered': 'integer',
            },
        )

    def get_random_question(self, return_data=None):
        printer.print_title_bar('Random Question')
        cursor = db.select_random(self.table_name)
        record = cursor.fetchone()
        if record is not None:
            question_id = record[0]
            printer.print_records(record, self.print_function)
        else:
            printer.print_no_records()
            question_id = None
        return_data = {'return_id': question_id}
        return return_data

    def get_random_unanswered_question(self, return_data=None):
        printer.print_title_bar('Random Unanswered Question')
        cursor = db.select_random(self.table_name, criteria={'answered': 0})
        record = cursor.fetchone()
        if record is not None:
            question_id = record[0]
            printer.print_records(record, self.print_function)
        else:
            printer.print_no_records()
            question_id = None
        return_data = {'return_id': question_id}
        return return_data

    def view_answered(self, return_data=None):
        """View only questions that have been marked as answered"""
        printer.print_title_bar('Answered Questions')
        cursor = db.select(self.table_name, criteria={'answered': 1})
        records = cursor.fetchall()
        if records:
            printer.print_records(records, self.print_function)
        else:
            printer.print_no_records()
        return None

    def view_all_questions(self, return_data=None):
        printer.print_title_bar('View all questions')
        cursor = db.select(self.table_name)
        records = cursor.fetchall()
        if records:
            printer.print_records(records, self.print_function)
        else:
            printer.print_no_records()
        return None

    def view_question_by_id(self, return_data=None):
        printer.print_title_bar('View by ID')
        id = input('ID to View: ')
        cursor = db.select(self.table_name, criteria={'id': id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, self.print_function)
        else:
            printer.print_no_records()
        return_data = {'return_id': id}
        return return_data

    def add_question(self, return_data=None):
        printer.print_title_bar('Add Question')
        input_data = input('Enter new question: ')
        table_data = {'question': input_data, 'answered': 0}
        return_cursor = db.add(self.table_name, table_data)
        inserted_id = return_cursor.lastrowid
        new_cursor = db.select(self.table_name, criteria={'id': inserted_id})
        new_record = new_cursor.fetchone()
        print()
        print('~~ Successfully Added Question ~~')
        printer.print_records(new_record, self.print_function)
        return_data = {'return_id': inserted_id}
        return return_data

    def edit_question(self, return_data=None):
        printer.print_title_bar('Edit Question')
        if return_data is not None:
            question_id = return_data.get('return_id')
        else:
            question_id = input('Enter question ID: ')
        cursor = db.select(self.table_name, criteria={'id': question_id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, self.print_function)
            edited_question = input('Enter the edited question: ')
            answered = validate_input(
                f'Question is answered? (Currently: {"Y" if record[2] == 1 else "N"}), Y/N?',
                {'Y': 1, 'N': 0},
            )
            update_data = {
                'id': question_id,
                'question': edited_question,
                'answered': answered,
            }
            db.update(self.table_name, {'id': question_id}, update_data)
            edited_cursor = db.select(self.table_name, criteria={'id': question_id})
            edited_record = edited_cursor.fetchone()
            print()
            print('~~ Successfully Edited Question ~~')
            printer.print_records(edited_record, self.print_function)
        else:
            printer.print_no_records()
        return_data = {'return_id': question_id}
        return return_data

    def delete_question(self, return_data=None):
        """Deletes question and all associated answers, notes, and tips"""
        printer.print_title_bar('Delete by ID')
        if return_data is not None:
            question_id = return_data.get('return_id')
        else:
            question_id = input('ID to Delete: ')
        question_cursor = db.select(
            table_name=self.table_name, criteria={'id': question_id}
        )
        question_record = question_cursor.fetchone()
        if question_record is not None:
            print('     WARNING     '.center(80, '!'))
            print()
            print('~~ This Question has the following associated data: ~~')
            print()
            printer.print_records(question_record, self.print_function)
            answer_cursor = db.select('answers', criteria={'question_id': question_id})
            answer_records = answer_cursor.fetchall()
            print('Answers:')
            print('----------')
            if answer_records:
                printer.print_records(answer_records, printer.answer_printer)
            else:
                printer.print_no_records()
            note_cursor = db.select('notes', criteria={'question_id': question_id})
            note_records = note_cursor.fetchall()
            print('Notes:')
            print('----------')
            if note_records:
                printer.print_records(note_records, printer.note_printer)
            else:
                printer.print_no_records()
            tip_cursor = db.select('tips', criteria={'question_id': question_id})
            tip_records = tip_cursor.fetchall()
            print('Tips:')
            print('----------')
            if tip_records:
                printer.print_records(tip_records, printer.tip_printer)
            else:
                printer.print_no_records()

            make_sure = input('Are you sure you want to delete this question? Y/N: ')
            if make_sure.upper() == 'Y':
                db.delete('questions', {'id': question_id})
                if answer_records:
                    for record in answer_records:
                        db.delete('answers', {'id': record[0]})
                if note_records:
                    for record in note_records:
                        db.delete('notes', {'id': record[0]})
                if tip_records:
                    for record in tip_records:
                        db.delete('tips', {'id': record[0]})

                print()
                print(f'~~ Successfully Deleted {self.table_name[:-1:].capitalize()} ~~')
        else:
            printer.print_no_records()
        return None

    def view_all_info(self, return_data=None, title=True):
        """View question and associated answers, notes, and tips."""
        if title:
            printer.print_title_bar('View All Question Info')
        question_id = return_data.get('return_id')
        question_cursor = db.select(self.table_name, criteria={'id': question_id})
        question_record = question_cursor.fetchone()
        if question_record is not None:
            printer.print_records(question_record, self.print_function)
            answer_cursor = db.select('answers', criteria={'question_id': question_id})
            answer_records = answer_cursor.fetchall()
            print('Answers:')
            print('----------')
            if answer_records:
                printer.print_records(answer_records, printer.answer_printer)
            else:
                printer.print_no_records()
            note_cursor = db.select('notes', criteria={'question_id': question_id})
            note_records = note_cursor.fetchall()
            print('Notes:')
            print('----------')
            if note_records:
                printer.print_records(note_records, printer.note_printer)
            else:
                printer.print_no_records()
            tip_cursor = db.select('tips', criteria={'question_id': question_id})
            tip_records = tip_cursor.fetchall()
            print('Tips:')
            print('----------')
            if tip_records:
                printer.print_records(tip_records, printer.tip_printer)
            else:
                printer.print_no_records()
        else:
            printer.print_no_records()
            question_id = None
        return_data = {'return_id': question_id}
        return return_data


class Answers(Command):
    """Answers commands"""

    def __init__(self, defaults=None, print_fuction=printer.answer_printer):
        super().__init__(defaults)
        self.table_name = 'answers'
        self.print_function = print_fuction

    def create_table(self):
        db.create_table(
            self.table_name,
            {
                'id': 'integer primary key autoincrement',
                'question_id': 'integer not null',
                'answer': 'text not null',
            },
        )

    def view_answer_by_id(self, return_data=None):
        printer.print_title_bar('View by ID')
        answer_id = input('ID to View: ')
        print()
        cursor = db.select(self.table_name, criteria={'id': answer_id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, self.print_function)
            question_id = record[1]
            question_cursor = db.select('questions', criteria={'id': question_id})
            question_record = question_cursor.fetchone()
            print('Question for Reference:')
            print(question_record[1])
            print()
        else:
            printer.print_no_records()
            answer_id = None
        return_data = {'return_id': answer_id}
        return return_data

    def add_answer(self, return_data=None):
        printer.print_title_bar('Add Answer')
        if return_data is not None:
            question_id = return_data.get('return_id')
        else:
            question_id = input('Enter question ID: ')
        print()
        cursor = db.select('questions', criteria={'id': question_id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, printer.question_printer)
            new_answer = input('Enter new answer: ')
            table_data = {'question_id': question_id, 'answer': new_answer}
            return_cursor = db.add(self.table_name, table_data)
            answer_id = return_cursor.lastrowid
            new_cursor = db.select(self.table_name, criteria={'id': answer_id})
            new_record = new_cursor.fetchone()
            print()
            print('~~ Successfully Added Answer ~~')
            printer.print_records(new_record, self.print_function)
            # update question to answered
            update_data = {'id': question_id, 'answered': 1}
            db.update('questions', {'id': question_id}, update_data)
        else:
            printer.print_no_records()
            question_id = None
        return_data = {'return_id': question_id}
        return return_data

    def edit_answer(self, return_data=None):
        printer.print_title_bar('Edit Answer')
        if return_data is not None:
            id = return_data.get('return_id')
        else:
            id = input('Enter Answer ID: ')
        cursor = db.select(self.table_name, criteria={'id': id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, self.print_function)
            answer_id, question_id, answer = record
            question_cursor = db.select('questions', criteria={'id': question_id})
            question_record = question_cursor.fetchone()
            print('Question for Reference:')
            print(question_record[1])
            print()
            edited_answer = input('Enter the new answer: ')
            update_data = {
                'id': answer_id,
                'question_id': question_id,
                'answer': edited_answer,
            }
            db.update(self.table_name, {'id': answer_id}, update_data)
            edited_cursor = db.select(self.table_name, criteria={'id': answer_id})
            edited_record = edited_cursor.fetchone()
            print()
            print('~~ Successfully Edited Question ~~')
            printer.print_records(edited_record, self.print_function)
        else:
            printer.print_no_records()
            answer_id = None
        return_data = {'return_id': answer_id}
        return return_data


class Notes(Command):
    """Notes commands"""

    def __init__(self, defaults=None, print_fuction=printer.note_printer):
        super().__init__(defaults)
        self.table_name = 'notes'
        self.print_function = print_fuction

    def create_table(self):
        db.create_table(
            self.table_name,
            {
                'id': 'integer primary key autoincrement',
                'question_id': 'integer not null',
                'note': 'text not null',
            },
        )

    def view_note_by_id(self, return_data=None):
        printer.print_title_bar('View by ID')
        note_id = input('Note to View: ')
        print()
        cursor = db.select(self.table_name, criteria={'id': note_id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, self.print_function)
            question_id = record[1]
            question_cursor = db.select('questions', criteria={'id': question_id})
            question_record = question_cursor.fetchone()
            print('Question for Reference:')
            print(question_record[1])
            print()
        else:
            printer.print_no_records()
            note_id = None
        return_data = {'return_id': note_id}
        return return_data

    def add_note(self, return_data=None):
        printer.print_title_bar('Add note')
        if return_data is not None:
            question_id = return_data.get('return_id')
        else:
            question_id = input('Enter question ID: ')
        print()
        cursor = db.select('questions', criteria={'id': question_id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, printer.question_printer)
            new_note = input('Enter new note: ')
            table_data = {'question_id': question_id, 'note': new_note}
            return_cursor = db.add(self.table_name, table_data)
            note_id = return_cursor.lastrowid
            note_cursor = db.select(self.table_name, criteria={'id': note_id})
            note_record = note_cursor.fetchone()
            print()
            print('~~ Successfully Added note ~~')
            printer.print_records(note_record, self.print_function)
        else:
            printer.print_no_records()
            question_id = None
        return_data = {'return_id': question_id}
        return return_data

    def edit_note(self, return_data=None):
        printer.print_title_bar('Edit note')
        if return_data is not None:
            id = return_data.get('return_id')
        else:
            id = input('Enter note ID: ')
        cursor = db.select(self.table_name, criteria={'id': id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, self.print_function)
            note_id, question_id, note = record
            question_cursor = db.select('questions', criteria={'id': question_id})
            question_record = question_cursor.fetchone()
            print('Question for Reference:')
            print(question_record[1])
            print()
            edited_note = input('Enter the new note: ')
            update_data = {'id': note_id, 'question_id': question_id, 'note': edited_note}
            db.update(self.table_name, {'id': note_id}, update_data)
            edited_cursor = db.select(self.table_name, criteria={'id': note_id})
            edited_record = edited_cursor.fetchone()
            print()
            print('~~ Successfully Edited Question ~~')
            printer.print_records(edited_record, self.print_function)
        else:
            printer.print_no_records()
            note_id = None
        return_data = {'return_id': note_id}
        return return_data


class Tips(Command):
    """Tips commands"""

    def __init__(self, defaults=None, print_fuction=printer.tip_printer):
        super().__init__(defaults)
        self.table_name = 'tips'
        self.print_function = print_fuction

    def create_table(self):
        db.create_table(
            self.table_name,
            {
                'id': 'integer primary key autoincrement',
                'question_id': 'integer not null',
                'tip': 'text not null',
            },
        )

    def view_tip_by_id(self, return_data=None):
        printer.print_title_bar('View by ID')
        tip_id = input('ID to View: ')
        print()
        cursor = db.select(self.table_name, criteria={'id': tip_id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, self.print_function)
            question_id = record[1]
            question_cursor = db.select('questions', criteria={'id': question_id})
            question_record = question_cursor.fetchone()
            print('Question for Reference:')
            print(question_record[1])
            print()
        else:
            printer.print_no_records()
            tip_id = None
        return_data = {'return_id': tip_id}
        return return_data

    def add_tip(self, return_data=None):
        printer.print_title_bar('Add tip')
        if return_data is not None:
            question_id = return_data.get('return_id')
        else:
            question_id = input('Enter question ID: ')
        print()
        cursor = db.select('questions', criteria={'id': question_id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, printer.question_printer)
            new_tip = input('Enter new tip: ')
            table_data = {'question_id': question_id, 'tip': new_tip}
            return_cursor = db.add(self.table_name, table_data)
            tip_id = return_cursor.lastrowid
            tip_cursor = db.select(self.table_name, criteria={'id': tip_id})
            tip_record = tip_cursor.fetchone()
            print()
            print('~~ Successfully Added tip ~~')
            printer.print_records(tip_record, self.print_function)
        else:
            printer.print_no_records()
            question_id = None
        return_data = {'return_id': question_id}
        return return_data

    def edit_tip(self, return_data=None):
        printer.print_title_bar('Edit tip')
        if return_data is not None:
            id = return_data.get('return_id')
        else:
            id = input('Enter tip ID: ')
        cursor = db.select(self.table_name, criteria={'id': id})
        record = cursor.fetchone()
        if record is not None:
            printer.print_records(record, self.print_function)
            tip_id, question_id, tip = record
            question_cursor = db.select('questions', criteria={'id': question_id})
            question_record = question_cursor.fetchone()
            print('Question for Reference:')
            print(question_record[1])
            print()
            edited_tip = input('Enter the new tip: ')
            update_data = {'id': tip_id, 'question_id': question_id, 'tip': edited_tip}
            db.update(self.table_name, {'id': tip_id}, update_data)
            edited_cursor = db.select(self.table_name, criteria={'id': tip_id})
            edited_record = edited_cursor.fetchone()
            print()
            print('~~ Successfully Edited Question ~~')
            printer.print_records(edited_record, self.print_function)
        else:
            printer.print_no_records()
            tip_id = None
        return_data = {'return_id': tip_id}
        return return_data
