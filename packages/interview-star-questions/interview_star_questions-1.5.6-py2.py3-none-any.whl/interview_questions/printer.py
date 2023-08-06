class Printer:
    '''Prints database records'''

    def __init__(self):
        pass

    def print_title_bar(self, name):
        """ Prints a centered title bar with variable length dependent
            upon length of name.
        """
        max_width = 80
        space = max_width - len(name) - 10
        left_pad = ('⎼' * (space // 2)) + (' ' * 5)
        right_pad = (' ' * 5) + ('⎼' * (space // 2))
        title = f'{left_pad}{name.upper()}{right_pad}'
        top_border = '⎺' * len(title)
        bottom_border = '⎽' * len(title)
        print('\n'.join([top_border, title, bottom_border, '']))

    def print_records(self, records, print_function):
        if isinstance(records, list):
            for record in records:
                print_function(record)
        else:
            print_function(records)

    def print_no_records(self):
        print('No matching records found.')
        print()
        print('-' * 80)
        print()

    def question_printer(self, record):
        question_id, question, answered = record
        print(f'ID: {question_id}')
        print(f'Question: {question}')
        print(f'Answered: {"Y" if answered == 1 else "N" if answered == 0 else answered}')
        print()

    def answer_printer(self, record):
        id, question_id, answer = record
        print(f'ID: {id}')
        print(f'Question ID: {question_id}')
        print(f'Answer: {answer}')
        print()

    def note_printer(self, record):
        id, question_id, note = record
        print(f'ID: {id}')
        print(f'Question ID: {question_id}')
        print(f'Note: {note}')
        print()

    def tip_printer(self, record):
        id, question_id, tip = record
        print(f'ID: {id}')
        print(f'Question ID: {question_id}')
        print(f'Tip: {tip}')
        print()
