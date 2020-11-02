#!/usr/bin/env python3

import random
import math
import time
import numpy as np


""" todos:
    - create Sudoku class                                 DONE 01/10
        - solve_fast() and helper fns need puzzle as arg  DONE 01/10
    - enhance solve fn to count solutions                 DONE 15/10
    - write scoring function                              DONE 02/11
    - set-oriented solve optimization                     IN PROGRESS 02/11
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
        self.puzzle = []
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

        if puzzle == []:
            # user has not provided puzzle values; make a puzzle from scratch
            self.make()
        else:
            """ TODO: ensure user did not provide invalid values (e.g., two 9s
            in the same row """

            """ step one: set self.puzzle to a blank puzzle """
            for i in range(self.size ** 2):
                self.puzzle.append(self.candidates)

            """ step two: insert any given values with insert(), which also
            removes that value from the candidate list of neighbors """
            for i in range(len(puzzle)):
                if isinstance(puzzle[i], int) and puzzle[i] != 0:
                    # caller provided value for cell
                    self.insert(str(puzzle[i]), i)


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
        """ helper function for solve_all(). returns the index of cell in
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


    def fewest_positions(self, puzzle=None):
        """ helper function for solve_all(). returns the candidate value with
        the fewest possible positions in a given set (row, column, or box) and
        the indices of that set. """
        if puzzle is None:
            puzzle = self.puzzle

        fpp_candidate = ''
        fpp_positions = list(range(self.size**2))
        
        # find value with fewest candidate positions by column
        d = {}
        for col in range(0, 1):
            for i in range(0, self.size**2, self.size):
                j = i + col
                if isinstance(puzzle[j], int):
                    continue
                
                for candidate in puzzle[j]:
                    if candidate in d:
                        d[candidate].append(j)
                    else:
                        d[candidate] = [j]

            print(f"after traversing column {col + 1}")
            print(d)

        for candidate in d:
            if len(d[candidate]) < len(fpp_positions):
                fpp_candidate = candidate
                fpp_positions = d[candidate]

##        # now by row
##        d = {}
##
##        for candidate, positions in d.items():
##            if len(candidate[positions]) < len(fpp_positions):
##                fpp_candidate = candidate
##                fpp_positions = positions
##
##        # now by box
##        d = {}
##
##        for candidate, positions in d.items():
##            if len(candidate[positions]) < len(fpp_positions):
##                fpp_candidate = candidate
##                fpp_positions = positions        
        
        return fpp_candidate, fpp_positions


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
            elif len(puzzle[i]) >= 1:
                # cell has multiple candidates
                res += '0 '
            else:
                # cell has no candidates, puzzle is unsolvable
                res += '! '

            if col == self.size - 1:
                # hit right edge of puzzle; move to next line
                res += '|\n'
        res += '-------------------------\n'
        return res


    def score(self):
        # step one: calculate B, branch-difficulty score
        terms = [(self.branch_factors[i] - 1) ** 2
                 for i in range(len(self.branch_factors))]
        B = sum(terms)

        # step two: fetch number of empty cells in given puzzle
        empty_cells = 0
        for i in range(len(self.puzzle)):
            if not isinstance(self.puzzle[i], int):
                empty_cells += 1
                
##      print("branch_factors: ", self.branch_factors)
##      print("terms: ", terms)
##      print("B = ", B)
##      print("# of empty cells = ", empty_cells)

        # step three: calculate and store puzzle difficulty score
        self.difficulties.append(B * 100 + empty_cells)


    # TODO: check to ensure given puzzle is valid; e.g., solve() currently
    # ignores the fact that the puzzle has two 1s in the top row
    def solve_all(self, puzzle=None):
        """ solver function that utilizes backtracking, randomization, and
        optimization. Returns solved puzzle, or None if given puzzle is
        unsolvable. Stores found solutions in self.solutions list.

        The optimization is that this solver does not traverse all cells in
        order (from 0 to 80 in a 9x9 puzzle, for example). Instead, it picks
        the cell with the fewest remaining candidates, or the set and value
        with the fewest possible positions, whichever is smaller.
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

                #search_set = []
                # find set and value with fewest possible positions
                #fpp_value, fpp_positions = self.fewest_possible_positions(puzzle)
                #if len(fpp_positions) < len(puzzle[i]):
                #    for position in fpp_positions:
                #        search_set.append((fpp_value, position))
                #else:
                #    candidates = random.sample(puzzle[i], len(puzzle[i]))
                #    for candidate in candidates:
                #        search_set.append((candidate, i))

                #branches = 0
                #for candidate, position in candidates:
                
                candidates = random.sample(puzzle[i], len(puzzle[i]))
                branches = 0
                for candidate in candidates:
                    if self.is_valid(candidate, i, puzzle):
                        # candidate looks good; insert into copy for recursion
                        puzzle_copy = puzzle[:]

##                        print(f"trying {candidate} in ({i // self.size + 1}, "
##                              f"{i % self.size + 1})...")
##                        print("all candidates for cell: ", candidates)

                        self.insert(candidate, i, puzzle_copy)

                        ##print("state of puzzle:")
                        ##print(self.print(puzzle=puzzle_copy))

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
            self.score()
            
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


dlbeer_55 = [5,3,4,0,0,8,0,1,0,
             0,0,0,0,0,2,0,9,0,
             0,0,0,0,0,7,6,0,4,
             0,0,0,5,0,0,1,0,0,
             1,0,0,0,0,0,0,0,3,
             0,0,9,0,0,1,0,0,0,
             3,0,5,4,0,0,0,0,0,
             0,8,0,2,0,0,0,0,0,
             0,6,0,7,0,0,3,8,2]

dlbeer_551 = [3,7,0,0,0,9,0,0,6,
              8,0,0,1,0,3,0,7,0,
              0,0,0,0,0,0,0,0,8,
              0,2,0,0,8,0,0,0,5,
              1,8,7,0,0,0,6,4,2,
              5,0,0,0,2,0,0,1,0,
              7,0,0,0,0,0,0,0,0,
              0,5,0,6,0,2,0,0,7,
              2,0,0,3,0,0,0,6,1]

# testing fewest_positions()
puzzle = Sudoku(label='dlbeer 551', puzzle=dlbeer_551)
print(puzzle)
candidate, positions = puzzle.fewest_positions()
print("Results of fewest_positions:")
print(candidate, positions)

# running trials
##scores = []
##puzzle = Sudoku(label='dlbeer 551', puzzle=dlbeer_551)
##print(puzzle)
##for i in range(1000):
##    puzzle.solve_all()
##    scores.append(puzzle.difficulties[0])
##    puzzle.solutions = []
##    puzzle.difficulties = []
##    puzzle.branch_factors = []
##
##print(f"average difficulty score = {np.mean(scores)}")
    
