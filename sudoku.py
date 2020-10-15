#!/usr/bin/env python3

import random
import math
import time


""" todos:
    - create Sudoku class                                 DONE 01/10
        - solve_fast() and helper fns need puzzle as arg  DONE 01/10
    - enhance solve fn to count solutions                 DONE 15/10
    - write scoring function                              IN PROGRESS 15/10
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
    - write fns for IDing strategies
        - X wing
        - XY wing
        - Schrodinger cell
        - swordfish pattern
        - empty rectangle
        - jellyfish pattern
"""


class Sudoku:
    """ represents a Sudoku puzzle """

    # TODO: error catch sizes that aren't perfect squares or not int
    # TODO: generalize to Sudokus of any (perfect square) size
    def __init__(self, size=9, label=time.time(), puzzle=[]):
        # instance attributes:
        self.size = size
        self.box_size = int(math.sqrt(size))
        self.label = str(label)
        self.candidates = ''
        for i in range(self.size):
            self.candidates += str(i + 1)
               
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
        self.puzzle = puzzle

        """ a list of complete, valid solutions to the given puzzle; an
        unsolvable given puzzle has an empty list of solutions; a uniquely
        solvable given puzzle has a single-element list of solutions, etc.
        Only a given puzzle with a unique solution is valid. """
        self.solutions = []

        """ difficulty associated with corresponding solution given by:
             difficulty = B * 100 + E
        where B is the sum (Bi - 1) ** 2 for every branching factor, and E is
        the number of empty cells in the given puzzle. This score is computed
        in solve_all(). """
        self.difficulties = []
        self.branch_factors = []

        if self.puzzle == []:
            # user has not provided puzzle values; make a puzzle from scratch
            self.make()
        else:
            """ TODO: ensure user did not provide invalid values (e.g., two 9s
            in the same row """
            
            # ensure any empty cells are populated with candidates
            for i in range(len(puzzle)):
                if not isinstance(puzzle[i], int) or puzzle[i] == 0:
                    # user did not provide value for cell
                    puzzle[i] = self.candidates
                    
            """ ensure puzzle has the right number of elements (e.g., 81 for a
            classix 9x9 puzzle); if not, extend with candidates """
            for i in range(self.size ** 2 - len(puzzle)):
                # user did not provide enough values to fill entire puzzle;
                self.puzzle.append(self.candidates)


    def make(self):
        """ fills the first three boxes and first column of a blank puzzle """

        # step zero: initialize puzzle with all candidates
        for i in range(self.size**2):
            self.puzzle.append(self.candidates)

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
                    brc = self.size * (self.box_size - 1) + self.box_size
                    
                    for v in values:
                        """ temporarily remove v from candidates for cell in
                        bottom-right corner of the current/second box """
                        brc_wo_v = self.puzzle[brc].replace(v, '')
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
        

    def __str__(self):
        return self.print()


    def fewest_candidates(self, puzzle=None):
        """ helper function for solve(). returns the index of cell in
        puzzle with fewest remaining candidate values.
        """
        if puzzle is None:
            puzzle = self.puzzle
            
        fewest = -1
        for i in range(self.size**2):
            if isinstance(puzzle[i], int):
                # cell is solved; skip it
                continue
            if len(puzzle[i]) <= 1:
                """ cell has only one candidate, or is unsolvable; this cell
                should be processed immediately by caller function.
                """
                return i
            if fewest == -1:
                # first candidate has been found;
                fewest = i
            elif len(puzzle[i]) < len(puzzle[fewest]):
                # cell has fewest candidates of cells checked so far
                fewest = i
        return fewest


    def insert(self, value, index, puzzle=None):
        """ Inserts given value into given cell of Sudoku puzzle. Helper
        function for __init__() and solve(). """
        if puzzle is None:
            puzzle = self.puzzle
            
        row = index // self.size
        col = index % self.size            
        box_r = row - (row % self.box_size)
        box_c = col - (col % self.box_size)

        # step one: remove value from candidates elsewhere in box
        # cell in top-left corner of relevant box
        top_left = box_r * int(math.sqrt(len(puzzle))) + box_c
        # now traverse all cells in box
        for i in range(0, self.size * self.box_size, self.size):
            for j in range(top_left + i, top_left + i + self.box_size):
                if isinstance(puzzle[j], int):
                    continue
                if value in puzzle[j]:
                    puzzle[j] = puzzle[j].replace(value, '')

        # step two: remove from candidates elsewhere in column
        for i in range(0, self.size**2, self.size):
            j = i + col
            if isinstance(puzzle[j], int):
                continue
            if value in puzzle[j]:
                puzzle[j] = puzzle[j].replace(value, '')

        # step three: remove from candidates elsewhere in row
        row_index = row * self.size
        for i in range(0, self.size):
            j = row_index + i
            if isinstance(puzzle[j], int):
                continue
            if value in puzzle[j]:
                puzzle[j] = puzzle[j].replace(value, '')

        # step four: insert value
        puzzle[index] = int(value)


    def is_complete(self, puzzle=None):
        """ checks whether any cells have not been solved. Cells with
        candidates remaining (i.e., a non-empty string) or cells with no valid
        solution (i.e., an empty string) cause it to return False. Otherwise,
        the puzzle is complete and the function returns True.
        """
        if puzzle is None:
            puzzle = self.puzzle
            
        for i in range(self.size**2):
            if not isinstance(puzzle[i], int):
                return False
        return True


    def is_valid(self, candidate, index, puzzle=None):
        """ helper function for solve(). Checks whether given value is
        valid for cell at given index in puzzle.
        """
        if puzzle is None:
            puzzle = self.puzzle
            
        row = index // self.size
        col = index % self.size
        return (not self.used_in_row(row, candidate, puzzle) and
                not self.used_in_col(col, candidate, puzzle) and
                not self.used_in_box(row, col, candidate, puzzle))


    def print(self, puzzle=None):
        if puzzle is None:
            puzzle = self.puzzle
            
        res = self.label + ':\n'
        for i in range(self.size**2):
            row = i // self.size
            col = i % self.size
            if row % self.box_size == 0 and col == 0:
                # starting a new row; print horizontal bar
                res += '-------------------------\n'
            if col % self.box_size == 0:
                # entered a new box; print vertical bar
                res += '| '

            if isinstance(puzzle[i], int):
                # cell has determinate value
                res += str(puzzle[i]) + ' '
            elif len(puzzle[i]) > 1:
                # cell has multiple candidates
                res += '0 '
            elif len(puzzle[i]) == 1:
                # cell has one candidate, but not officially solved
                res += '* '
            else:
                # cell has no candidates, puzzle is unsolvable
                res += '! '

            if col == self.size - 1:
                # hit right edge of puzzle; move to next line
                res += '|\n'
        res += '-------------------------\n'
        return res


    # TODO: check to ensure given puzzle is valid; e.g., solve() currently
    # ignores the fact that the puzzle has two 1s in the top row
    def solve(self, puzzle=None):
        """ solver function that utilizes backtracking, randomization, and
        optimization. Returns solved puzzle, or None if given puzzle is
        unsolvable.

        the optimization is that, rather than traversing all cells in order
        (from 0 to 80 in a 9x9 puzzle, for example), the main loop of this
        function picks the cell with the fewest candidates.
        """
        if puzzle is None:
            puzzle = self.puzzle[:]
            
        while not self.is_complete(puzzle):
            i = self.fewest_candidates(puzzle)
            # fewest_candidates() skips solved cells
            
            if len(puzzle[i]) == 1:
                # all candidates but one have been eliminated; officially
                # solve cell with insert()
                self.insert(puzzle[i], i, puzzle)
                continue
            if len(puzzle[i]) == 0:
                # cell has no possible solutions; puzzle unsolvable
                return None
            if len(puzzle[i]) > 1:
                # cell has more than one candidate
                candidates = random.sample(puzzle[i], len(puzzle[i]))
                for candidate in candidates:
                    if self.is_valid(candidate, i, puzzle):
                        # candidate looks good; insert into copy for recursion
                        puzzle_copy = puzzle[:]

                        self.insert(candidate, i, puzzle_copy)

                        # recurse on copy
                        puzzle_copy = self.solve(puzzle_copy)
                        if puzzle_copy is not None:
                            # candidate works
                            return puzzle_copy
                        # otherwise, candidate is bad; try the next one
                # none of the candidates work; puzzle is unsolvable
                return None
        # puzzle is complete
        return puzzle


    # TODO: check to ensure given puzzle is valid; e.g., solve() currently
    # ignores the fact that the puzzle has two 1s in the top row
    def solve_all(self, puzzle=None):
        """ solver function that utilizes backtracking, randomization, and
        optimization. Returns solved puzzle, or None if given puzzle is
        unsolvable. Stores found solutions in self.solutions list.

        the optimization is that, rather than traversing all cells in order
        (from 0 to 80 in a 9x9 puzzle, for example), the main loop of this
        function picks the cell with the fewest candidates.
        """
        if puzzle is None:
            puzzle = self.puzzle[:]
            
        while not self.is_complete(puzzle):
            i = self.fewest_candidates(puzzle)
            # fewest_candidates() skips solved cells
            
            if len(puzzle[i]) == 1:
                # all candidates but one have been eliminated; officially
                # solve cell with insert()
                self.insert(puzzle[i], i, puzzle)
                continue
            if len(puzzle[i]) == 0:
                # cell has no possible solutions; puzzle unsolvable
                return None
            if len(puzzle[i]) > 1:
                # cell has more than one candidate
                candidates = random.sample(puzzle[i], len(puzzle[i]))
                branches = 1
                for candidate in candidates:
                    if self.is_valid(candidate, i, puzzle):
                        # candidate looks good; insert into copy for recursion
                        puzzle_copy = puzzle[:]

                        print(f"trying {candidate} in ({i // self.size + 1}, "
                              f"{i % self.size + 1})...")

                        self.insert(candidate, i, puzzle_copy)

                        # recurse on copy and mark branching
                        branches += 1
                        puzzle_copy = self.solve_all(puzzle_copy)

                        # check that we haven't found more than one solution
                        if (len(self.solutions) == 2
                            and puzzle_copy is not None):
                            # we have, so start kick
                            return puzzle_copy
                        
                # search tree is exhausted from this node
                self.branch_factors.append(branches)
                return None
            
        # puzzle is complete; store it in solutions and score
        if puzzle not in self.solutions:
            self.solutions.append(puzzle)

            # scoring step one: calculate B, branch-difficulty score
            terms = [(self.branch_factors[i] - 1) ** 2
                     for i in range(len(self.branch_factors))]
            B = sum(terms)

            print("branch_factors: ", self.branch_factors)
            print("terms: ", terms)
            print("B = ", B)

            # scoring step two: fetch number of empty cells in given puzzle
            empty_cells = 0
            for i in range(len(self.puzzle)):
                if not isinstance(self.puzzle[i], int):
                    empty_cells += 1

            print("# of empty cells = ", empty_cells)

            # scoring step three: calculate puzzle difficulty score
            self.difficulties.append(B * 100 + empty_cells)
            
        return puzzle


    def used_in_box(self, row, col, candidate, puzzle=None):
        if puzzle is None:
            puzzle = self.puzzle
            
        # row and col values for cell in top-left corner of relevant box
        box_r = row - (row % self.box_size)
        box_c = col - (col % self.box_size)
        # cell in top-left corner of relevant box
        top_left = box_r * self.size + box_c
        # now traverse all cells in box
        for i in range(0, self.size * self.box_size, self.size):
            for j in range(top_left + i, top_left + i + self.box_size):
                if puzzle[j] == int(candidate):
                    return True
        return False


    def used_in_col(self, col, candidate, puzzle=None):
        if puzzle is None:
            puzzle = self.puzzle
            
        for i in range(0, self.size**2, self.size):
            j = i + col
            if puzzle[j] == int(candidate):
                return True
        return False


    def used_in_row(self, row, candidate, puzzle=None):
        if puzzle is None:
            puzzle = self.puzzle
            
        row_index = row * self.size
        for i in range(0, self.size):
            j = row_index + i
            if puzzle[j] == int(candidate):
                return True
        return False


values = [1, 7, 4, 3, 8, 9, 6, 5, 2,
          3, 6, 9, 5, 2, 4, 8, 1, 7,
          5, 2, 8, 6, 1, 7, 4, 3, 9,
          2, 0, 0, 0, 0, 0, 0, 0, 0,
          6, 0, 0, 0, 0, 0, 0, 0, 0,
          9, 0, 0, 0, 0, 0, 0, 0, 0,
          8, 0, 0, 0, 0, 0, 0, 0, 0,
          4, 0, 0, 0, 0, 0, 0, 0, 0,
          7, 0, 0, 0, 0, 0, 0, 0, 0]

values = [0, 0, 0, 0, 0, 4, 0, 2, 8,
          4, 0, 6, 0, 0, 0, 0, 0, 5,
          1, 0, 0, 0, 3, 0, 6, 0, 0,
          0, 0, 0, 3, 0, 1, 0, 0, 0,
          0, 8, 7, 0, 0, 0, 1, 4, 0,
          0, 0, 0, 7, 0, 9, 0, 0, 0,
          0, 0, 2, 0, 1, 0, 0, 0, 3,
          9, 0, 0, 0, 0, 0, 5, 0, 7,
          6, 7, 0, 4, 0, 0, 0, 0, 0]

##puzzle = Sudoku(puzzle=values)
##print(puzzle)
##puzzle.solve_all()
##print("number of solutions: ", len(puzzle.solutions))
##for i in range(len(puzzle.solutions)):
##    print(f"solution #{i+1}:")
##    print(puzzle.print(puzzle=puzzle.solutions[i]))
##    print(puzzle.difficulties[i])

values = [1, 0, 0, 0,
          0, 0, 1, 0,
          4, 0, 3, 0,
          0, 3, 0, 0]

small = Sudoku(size=4, puzzle=values)
print(small.print())
small.solve_all()
print("number of solutions: ", len(small.solutions))
for i in range(len(small.solutions)):
    print(f"solution #{i+1}:")
    print(small.print(puzzle=small.solutions[i]))
    print(small.difficulties[i])
