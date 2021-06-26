

import numpy
import pdb

import copy

class GameRow(object):

    MAX_LENGTH_ROW = 9

    def __init__(self):

        self._values = []

    def get_numbers(self):

        return self._values

    def get_number(self, position):

        return self._values[position] if position < len(self._values) else 0

    def cross_number(self, position):

        self._values[position] = 'X'

    def append_number(self, number):

        return_value = False

        if len(self._values) < self.MAX_LENGTH_ROW:
            self._values.append(number)
            return_value = True

        return return_value

    def is_solved(self):

        return self._values.count('X') == 9

    def get_as_string(self):

        row = ""
        for elm in self._values:
            row += ( " " + str(elm))
        return row


class GameSet(object):

    def __init__(self, row1, row2, num1, num2):

        self._row1 = row1
        self._row2 = row2
        self._num1 = num1
        self._num2 = num2

    def get_values(self):

        return [self._row1, self._row2, self._num1, self._num2]

class GameBoard(object):

    def __init__(self, numbers):

        self._rows = [GameRow()]

        for number in numbers:
            if self._rows[-1].append_number(number):
                continue
            else:
                self._rows.append(GameRow())
                self._rows[-1].append_number(number)

    def print_board(self):

        for row in self._rows:
            print(row.get_as_string())

    def print_solution(self, solution):

        for i, row in enumerate(self._rows):

            tmp_row = []

            if i == solution._row1 or i == solution._row2:
                for j, num in enumerate(row.get_numbers()):
                    if j == solution._num1 or j == solution._num2:
                        tmp_row.append('O')
                    else:
                        tmp_row.append(row.get_number(j))

                print(tmp_row)
            else:
                print(row.get_numbers())

    def apply_solution(self, solution):

        for i, row in enumerate(self._rows):
            if i == solution._row1 or i == solution._row2:
                for j, num in enumerate(row.get_numbers()):
                    if j == solution._num1 or j == solution._num2:
                        row.cross_number(j)


    def get_row(self, number):

        if number >= 0:
            return self._rows[number]

    def get_number_of_rows(self):

        return len(self._rows)

    def get_posibities(self):

        total_number_of_rows = self.get_number_of_rows()

        solutions = []

        for row_nr in range(total_number_of_rows-1):

            for offset in range(1, total_number_of_rows-row_nr):

                for i, number in enumerate(self.get_row(row_nr).get_numbers()):

                    if self.get_row(row_nr+offset).get_number(i) == 'X' or number == 'X':
                        continue

                    if number == self.get_row(row_nr+offset).get_number(i):
                        solutions.append(GameSet(row_nr, row_nr+offset, i, i))

                    if number + self.get_row(row_nr+offset).get_number(i) == 10:
                        solutions.append(GameSet(row_nr, row_nr+offset, i, i))

        for row_nr in range(total_number_of_rows):
            for i, number in enumerate(self.get_row(row_nr).get_numbers()[:-1]):

                if self.get_row(row_nr).get_number(i+1) == 'X' or number == 'X':
                    continue

                if number == self.get_row(row_nr).get_number(i+1):
                    solutions.append(GameSet(row_nr, row_nr, i, i+1))

                if number + self.get_row(row_nr).get_number(i+1) == 10:
                    solutions.append(GameSet(row_nr, row_nr, i, i+1))




        return solutions

    def create_new_rows(self):

        numbers = []

        for row in self._rows:
            numbers.extend(row.get_numbers())

        numbers2 = []
        for num in numbers:
            if num != 'X':
                numbers2.append(num)

        for num in numbers2:
            if not self._rows[-1].append_number(num):
                self._rows.append(GameRow())
                self._rows[-1].append_number(num)

    def clean_board(self):
    
        remaining = []
        for row in self._rows:
            if not row.is_solved():
                remaining.append(row)
                
        self._rows = remaining

class MainGame(object):

    def __init__(self, board):

        self._boards = [board]

    def set_board(self, board):

        self._boards[0] = board

    def get_board(self):

        return self._boards[0]

    def solve_iteration(self):

        pass

    def get_solutions(self):

        return self._boards[0].get_posibities()

    def print_solutions(self, solutions):

        print()


    def create_board(self, solution):

        new_board = copy.deepcopy(self._boards[0])
        new_board.apply_solution(solution)
        return new_board




if __name__ == "__main__":

    print("Starting game")

    game_board = GameBoard([1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7, 1, 8])
    game_board.print_board()
    game = MainGame(game_board)

    print("solving: ")
    for i in range(50):
        print("iteration: {0}, rows total: {1}".format(i, game.get_board().get_number_of_rows()))
        foo = game.get_solutions()

        if len(foo) == 0:
            # print('no more solutions, adding numbers')
            game.get_board().create_new_rows()
            # game.get_board().print_board()
            # break
        else:
            print('number of solutions: {0}'.format(len(foo)))
            board = game.create_board(foo[0])
            game.set_board(board)


    game.get_board().clean_board()
    game.get_board().print_board()
