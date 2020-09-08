#!/usr/bin/env python3

import random
import math


""" todos:
    - create Sudoku class                                 IN PROGRESS 08/09
        - solve_fast() and helper fns need puzzle as arg  START ASAP
    - enhance solve fn to count solutions                 IN PROGRESS 08/09
    - pickle puzzles
    - removal algorithm - basic
    - removal algorithm - multiple difficulties
    - generalize turtle fns for puzzles not 9x9
    - generalize initialize() and make() for size
    - implement GUI
        - fill cells
        - call for solvability
        - call for final check
        - get hint/freebie
        - candidate marks
            - corner notation
            - center notation
        - highligher
        - highlight selected number (every 8, e.g.)
"""


class Sudoku:
    """ represents a Sudoku puzzle """

    # TODO: error catch sizes that aren't perfect squares or not int
    # TODO: generalize to Sudokus of any (perfect square) size
    def __init__(self, size=9, label=''):
        # instance attributes
        self.size = size
        self.box_size = int(math.sqrt(size))
        self.solutions = 0
        self.label = str(label)
        self.puzzle = []
        """ A puzzle is a list of elements that are either strings of candidate
        values for a particular cell, or the integer solution for that cell.
        The row and column for each cell is implicit in the data structure as
        follows:
            row1col1, row1col2, ..., row1col9,
            row2col1, row2col2, ..., row2col9,
            .
            .
            .
            row9col1, row9col2, ..., row9col9
        When the string of candidate values is empty, there is no valid value
        for that cell and the puzzle is thus unsolvable.
        """
      
        """ The remainder of this initialization produces a solved puzzle. """
        # step zero: initialize puzzle with all candidates
        for i in range(self.size**2):
            self.puzzle.append('123456789')

        # step one: fill box 1
        # traverse by row and col the cells within the first box
        top_left_index = 0
        row_index_delta = self.size
        row_beyond_box_index = self.size * self.box_size
        for i in range(top_left_index, row_beyond_box_index, row_index_delta):
            # create random sequence of candidates for row
            values = random.sample(list(self.puzzle[i]), len(self.puzzle[i]))        
            for j in range(i, i + self.box_size):
                # pull random value and assign to cell
                candidate = values.pop()
                self.insert(candidate, j)

        # step two: fill box 2
        # traverse by row and col the cells within the second box
        top_left_index += self.box_size
        row_beyond_box_index += self.box_size
        for i in range(top_left_index, row_beyond_box_index, row_index_delta):
            # create random sequence of candidates for row
            values = random.sample(list(self.puzzle[i]), len(self.puzzle[i]))
            for j in range(i, i + self.box_size):
                row = j // self.size
                if row < self.box_size - 1:
                    """ we're not on last row, so only pick a value for the
                    cell that won't make last row unsolvable. """
                    bottom_right_cell = self.size * (self.box_size - 1)
                                        + self.box_size
                    for v in values:
                        """ temporarily remove v from candidates for cell in
                        bottom-right corner of the current/second box """
                        brc_wo_v =
                                self.puzzle[bottom_right_cell].replace(v, '')
                        if len(brc_wo_v) >= self.box_size:
                            # bottom row of box will still be solvable
                            candidate = v
                            values.remove(v)
                            break
                else:
                    # in last row of box; simply pick value and fill
                    candidate = values.pop()

                self.insert(candidate, j)

        # step three: fill box 3
        # traverse by row and col the cells within third box
        top_left_index += self.box_size
        row_beyond_box_index += self.box_size
        for i in range(top_left_index, row_beyond_box_index, row_index_delta):
            # create random sequence of candidates for row
            values = random.sample(list(self.puzzle[i]), len(self.puzzle[i]))
            for j in range(i, i + self.box_size):
                candidate = values.pop()
                self.insert(candidate, j)

        # step four: fill column 1
        # traverse first col of entire puzzle, starting below first box
        top_left_index = self.size * self.box_size
        row_beyond_puzzle_index = self.size**2
        for i in range(top_left_index, row_beyond_puzzle_index,
                       row_index_delta):
            values = random.sample(list(self.puzzle[i]), len(self.puzzle[i]))
            candidate = values.pop()
            self.insert(candidate, i)

        # step five: fill rest of puzzle using backtracking solve_fast()
        self.puzzle = self.solve_fast()
        

    def __str__(self):
        print(self.label + ':\n')
        for i in range(self.size**2):
            row = i // self.size
            col = i % self.size
            if row % self.box_size == 0 and col == 0:
                # starting a new row; print horizontal bar
                print('-------------------------')
            if col % self.box_size == 0:
                # entered a new box; print vertical bar
                print('|', end= ' ')

            if isinstance(self.puzzle[i], int):
                # cell has determinate value
                print(self.puzzle[i], end= ' ')
            elif len(self.puzzle[i]) > 1:
                # cell has multiple candidates
                print("0", end=' ')
            elif len(self.puzzle[i]) == 1:
                # cell has one candidate, but not officially solved
                print("*", end=' ')
            else:
                # cell has no candidates, puzzle is unsolvable
                print("!", end=' ')

            if col == size - 1:
                # hit right edge of puzzle; move to next line
                print('|')
        print('-------------------------')


    def fewest_candidates(self):
        """ helper function for solve_fast(). returns the index of cell in
        puzzle with fewest remaining candidate values.
        """
        fewest = -1
        for i in range(self.size**2):
            if isinstance(self.puzzle[i], int):
                # cell is solved; skip it
                continue
            if len(self.puzzle[i]) <= 1:
                """ cell has only one candidate, or is unsolvable; this cell
                should be processed immediately by caller function.
                """
                return i
            if fewest == -1:
                # first candidate has been found;
                fewest = i
            elif len(self.puzzle[i]) < len(self.puzzle[fewest]):
                # cell has fewest candidates of cells checked so far
                fewest = i
        return fewest


    def insert(self, value, index):
        """ Inserts given value into given cell of Sudoku puzzle. Helper
        function for __init__() and solve_fast(). """
        row = index // self.size
        col = index % self.size

        # step one: remove value from candidates in row
        row_index = row * self.size
        for i in range(0, self.size):
            j = row_index + i
            if isinstance(self.puzzle[j], int):
                continue
            if candidate in self.puzzle[j]:
                self.puzzle[j] = self.puzzle[j].replace(candidate, '')

        # step two: now remove it from candidates in column
        for i in range(0, self.size**2, self.size):
            j = i + col
            if isinstance(self.puzzle[j], int):
                continue
            if candidate in self.puzzle[j]:
                self.puzzle[j] = self.puzzle[j].replace(candidate, '')

        # step three: finally remove it from candidates in box
        # row and col values for cell in top-left corner of relevant box
        box_r = row - (row % 3)
        box_c = col - (col % 3)
        # cell in top-left corner of relevant box
        top_left = box_r * int(math.sqrt(len(puzzle))) + box_c
        # now traverse all cells in box
        for i in range(0, 19, 9):
            for j in range(top_left + i, top_left + i + 3):
                if isinstance(puzzle[j], int):
                    continue
                if candidate in puzzle[j]:
                    puzzle[j] = puzzle[j].replace(candidate, '')        

        # step four: insert value
        self.puzzle[index] = int(value)


    def is_complete(self):
        """ checks whether any cells have not been solved. Cells with
        candidates remaining (i.e., a non-empty string) or cells with no valid
        solution (i.e., an empty string) cause it to return False. Otherwise,
        the puzzle is complete and the function returns True.
        """
        for i in range(self.size**2):
            if not isinstance(self.puzzle[i], int):
                return False
        return True


    def is_valid(self, candidate, index):
        """ helper function for solve_fast(). Checks whether given value is
        valid for cell at given index in puzzle.
        """
        row = index // self.size
        col = index % self.size
        return (not self.used_in_row(row, candidate) and
                not self.used_in_col(col, candidate) and
                not self.used_in_box(row, col, candidate))


    def solve_fast(self, puzzle=self.puzzle):
        """ solver function that utilizes backtracking, randomization, and
        optimization. returns solved puzzle object, or None if given puzzle is
        unsolvable.

        the optimization is that, rather than traversing all cells in order
        (from 0 to 80 in a 9x9 puzzle, for example), the main loop of this
        function picks the cell with the fewest candidates.
        """

        while not self.is_complete():
            i = self.fewest_candidates()
            # fewest_candidates() skips solved cells
            
            if len(self.puzzle[i]) == 1:
                # all candidates but one have been eliminated; officially
                # solve cell with insert()
                self.insert(puzzle[i], i)
                continue
            if len(self.puzzle[i]) == 0:
                # cell has no possible solutions; puzzle unsolvable
                return None
            if len(self.puzzle[i]) > 1:
                # cell has more than one candidate
                candidates = random.sample(self.puzzle[i], len(self.puzzle[i]))
                for candidate in candidates:
                    if self.is_valid(candidate, i):
                        # candidate looks good; insert into copy for recursion
                        puzzle_copy = self.puzzle[:]


                        # THIS AND REST OF IF STATEMENT WON'T WORK
                        insert(candidate, i, puzzle_copy)

                        # recurse on copy
                        puzzle_copy = solve_fast(puzzle_copy)
                        if puzzle_copy:
                            # candidate works; make copy main puzzle
                            puzzle = puzzle_copy
                            return puzzle
                        # otherwise, candidate is bad; try the next one
                # none of the candidates work; puzzle is unsolvable
                return None
        # puzzle is complete and hence valid; return it
        return puzzle


    def used_in_row(self, row, candidate):
        row_index = row * self.size
        for i in range(0, self.size):
            j = row_index + i
            if self.puzzle[j] == int(candidate):
                return True
        return False


    def used_in_col(self, col, candidate):
        for i in range(0, self.size**2, self.size):
            j = i + col
            if self.puzzle[j] == int(candidate):
                return True
        return False


    def used_in_box(self, row, col, candidate):
        # row and col values for cell in top-left corner of relevant box
        box_r = row - (row % 3)
        box_c = col - (col % 3)
        # cell in top-left corner of relevant box
        top_left = box_r * self.size + box_c
        # now traverse all cells in box
        for i in range(0, 19, 9):
            for j in range(top_left + i, top_left + i + 3):
                if self.puzzle[j] == int(candidate):
                    return True
        return False


##puzzle = make()
##puzzle = solve(puzzle)
##print_puzzle(puzzle)
