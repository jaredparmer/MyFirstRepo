#!/usr/bin/env python3

import turtle
import random
import math

""" to-dos:
        - rebuild fundamental data structure            IN PROGRESS 04/08
        - fill cells while solving?
            - gray candidates, black finals?
        - randomize solve patterns                      IN PROGRESS 31/07
            - rewrite make_puzzle to partially fill
        - optimize solve function                       IN PROGRESS 31/07
        - enhance solve fn to count solutions
        - pickle puzzles
        - removal algorithm - basic
        - removal algorithm - multiple difficulties
        - generalize turtle fns for puzzles not 9x9
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

# TO DO: generalize for puzzles not 9x9 in size
# postcondition: turtle t at origin, facing east, pen is up
def draw_board(t, box_size):
    # initialize pen and draw first set of boxes
    t.pu()
    t.goto(box_size * 4.5, box_size * 4.5)
    t.seth(180)
    t.pd()
    for i in range(10):
        if i % 3 == 0:
            t.width(2)
        else:
            t.width(1)
        draw_box(t, box_size * i)

    # initialize pen and draw second set of boxes
    t.pu()
    t.goto(box_size * -4.5, box_size * -4.5)
    t.lt(180)
    t.pd()

    # range is only 9 because outermost box already drawn
    for i in range(9):
        if i % 3 == 0:
            t.width(2)
        else:
            t.width(1)
        draw_box(t, box_size * i)

    # return pen to origin, facing east, pen down
    t.pu()
    t.goto(0, 0)

# draws a single box with lengths of given size
# precondition: turtle pen is down
# postcondition: turtle facing same as before fn call
def draw_box(t, size):
    for i in range(4):
       t.fd(size)
       t.lt(90)

# TO DO: generalize for puzzles not 9x9 in size
# postcondition: all non-zero values filled into board, pen is up
def fill_board(t, puzzle, box_size):
    size = int(math.sqrt(len(puzzle)))

    # initialize pen for cell (0, 0)
    t.pu()
    t.goto(box_size * -4.5 + box_size * (1/2),
            box_size * 3.5 + box_size * (1/4))
    t.pd()

    # fill boxes with elements from puzzle
    for i in range(len(puzzle)):
        if len(puzzle[i]) == 1:
            # cell has determinate value; print it
            t.write(puzzle[i], move=False, align="center", 
                    font=("Arial", int(box_size / 2.5), "normal"))
        elif len(puzzle[i]) == 0:
            i# cell has no candidates; puzzle is unsolvable; print error
            t.pencolor('red')
            t.write('!', move=False, align="center", 
                    font=("Arial", int(box_size / 2.5), "normal"))
            t.pencolor('black')
        # otherwise, cell has multiple candidates; print nothing and move
        t.pu()
        t.fd(box_size)
        t.pd()

        if (i + 1) % size == 0:
            # have hit right bound of puzzle; move to new line
            t.pu()
            t.bk(box_size * size)
            t.rt(90)
            t.fd(box_size)
            t.lt(90)
            t.pd()
    t.pu()

# TO DO: generalize for puzzles not 9x9 in size
# precondition: x and y be w/n range of grid
# postcondition: cell (x, y) is filled with determinate value or error is
# marked, and pen is up
def fill_cell(t, x, y, puzzle, box_size):
    pen_to_cell(t, x, y, box_size)
    i = int(math.sqrt(len(puzzle))) * x + y
    if len(puzzle[i]) == 1:
        # cell has determinate value; print it
        t.write(puzzle[i], move=False, align="center", 
                font=("Arial", int(box_size / 2.5), "normal"))
    elif len(puzzle[i]) == 0:
        # cell has no candidates; puzzle is unsolvable; print error
        t.pencolor('red')
        t.write('!', move=False, align="center", 
                font=("Arial", int(box_size / 2.5), "normal"))
        t.pencolor('black')
    # otherwise, cell has multiple candidates; print nothing
    t.pu()

""" This function initializes a blank puzzle. A puzzle is a list of 81 lists,
where each nested list represents the candidate values for a particular cell.
The row and column for each cell is implicit in the data structure as follows:
    row1col1, row1col2, ..., row1col9,
    row2col1, row2col2, ..., row2col9,
    .
    .
    .
    row9col1, row9col2, ..., row9col9
When the nested list of candidate values for a particular cell is exactly 1,
that cell has a determinate value. When the nested list of candidate values is
empty, there is no valid value for that cell and the puzzle is thus unsolvable.
"""
def init_puzzle(size):
    puzzle = []
    candidates = ''
    for i in range(1, size + 1):
        candidates += str(i)
    for i in range(size**2):
        puzzle.append(candidates)
    return puzzle

# generates randomly filled puzzle
# TO DO: partially fill puzzle as prep for generation via solve fn
def make_puzzle(puzzle):
    size = math.sqrt(len(puzzle))
    for i in range(len(puzzle)):
        puzzle[i] = str(random.randint(1, size))

# TO DO: generalize for puzzles not 9x9 in size
# preconditions: x and y be within the range of the grid's row and columns
# postcondition: turtle t is pen down in cell (x, y) of grid
def pen_to_cell(t, x, y, box_size):
    # initialize pen to cell (0, 0) of grid, facing east
    t.pu()
    t.goto(box_size * -4.5 + box_size * (1/2), 
            box_size * 3.5 + box_size * (1/4))
    t.seth(0)

    # move pen to cell (x, y) of grid
    t.fd(y * box_size)
    t.rt(90)
    t.fd(x * box_size)

    # prep pen to fill cell (x, y)
    t.lt(90)
    t.pd()

# prints puzzle in makeshift board in console, faster for debugging
def print_puzzle(puzzle):
    size = math.sqrt(len(puzzle))
    box_size = math.sqrt(size)
    for i in range(len(puzzle)):
        row = i // size
        col = i % size
        if row % box_size == 0 and col == 0:
            # starting a new row; print horizontal bar
            print('-------------------------')
        if col % box_size == 0:
            # entered a new box; print vertical bar
            print('|', end= ' ')

        if len(puzzle[i]) > 1:
            # cell has multiple candidates
            print("0", end=' ')
        elif len(puzzle[i]) == 1:
            # cell has a determinate value
            print(puzzle[i][0], end=' ')
        else:
            # cell has no candidates, puzzle is unsolvable
            print("!", end=' ')

        if col == size - 1:
            # hit right edge of puzzle; move to next line
            print('|')
    print('-------------------------')

def puzzle_is_complete(puzzle):
    for i in range(len(puzzle)):
        if len(puzzle[i]) > 1:
            return False
    return True

""" The following functions remove a given candidate from the candidate
lists of all cells in the given row, column, or box.

IMPORTANT: These fns should be run *before* the candidate is placed in the
desired cell. They should also be run *after* the used_in_x() fns, as they
assume the candidate is not an already-found solution to a cell in the row,
column, or box.
"""
def rm_from_row(puzzle, row, candidate):
    size = int(math.sqrt(len(puzzle)))
    row_index = row * size
    for i in range(0, size):
        j = row_index + i
        if candidate in puzzle[j]:
            puzzle[j] = puzzle[j].replace(candidate, '')

def rm_from_col(puzzle, col, candidate):
    size = int(math.sqrt(len(puzzle)))
    for i in range(0, size**2, size):
        j = i + col
        if candidate in puzzle[j]:
            puzzle[j] = puzzle[j].replace(candidate, '')

def rm_from_box(puzzle, row, col, candidate):
    # row and col values for cell in top-left corner of relevant box
    box_r = row - (row % 3)
    box_c = col - (col % 3)
    # cell in top-left corner of relevant box
    top_left = box_r * int(math.sqrt(len(puzzle))) + box_c
    # now traverse all cells in box
    for i in range(0, 19, 9):
        for j in range(top_left + i, top_left + i + 3):
            if candidate in puzzle[j]:
                puzzle[j] = puzzle[j].replace(candidate, '')

""" REQUIRES UPDATE TO REFLECT NEW DS
"""
# counts recursions
count = 0
# returns solved puzzle object, or None if given puzzle is unsolvable
def solve_puzzle(puzzle):
    global count

    # base case: puzzle is completely filled out
    if puzzle_is_complete(puzzle):
        print("puzzle is complete!")
        return puzzle

    # recursion case
    # traverse entire puzzle
    size = len(puzzle)
    for i in range(size):
        row = i // int(math.sqrt(size))
        col = i % int(math.sqrt(size))
        if len(puzzle[i]) == 1:
            # cell has a solution; move on
            continue
        if len(puzzle[i]) == 0:
            # cell has no possible solutions; puzzle unsolvable
            return None
        if len(puzzle[i]) > 1:
            # cell has more than one candidate
            for candidate in puzzle[i]:
                if (not used_in_row(puzzle, row, candidate) and
                    not used_in_col(puzzle, col, candidate) and
                    not used_in_box(puzzle, row, col, candidate)):

                    # candidate looks good; make copy for recursion
                #   print(f"candidate {candidate} looks good, trying...")
                    puzzle_copy = puzzle[:]

                    # remove candidate from candidates of all cells in same
                    # row, column, or box
                    rm_from_row(puzzle_copy, row, candidate)
                    rm_from_col(puzzle_copy, col, candidate)
                    rm_from_box(puzzle_copy, row, col, candidate)

                    # assign candidate to cell
                    puzzle_copy[i] = candidate

                    # recurse on copy
                    count += 1
                    puzzle_copy = solve_puzzle(puzzle_copy)
                    if puzzle_copy:
                        # candidate works; make copy main puzzle
                        puzzle = puzzle_copy
                        return puzzle
                    # otherwise, candidate is bad; try the next one
            return None                                            
    return None

def used_in_row(puzzle, row, candidate):
    size = int(math.sqrt(len(puzzle)))
    row_index = row * size
    for i in range(0, size):
        j = row_index + i
        if puzzle[j] == candidate:
            return True
    return False

def used_in_col(puzzle, col, candidate):
    size = int(math.sqrt(len(puzzle)))
    for i in range(0, size**2, size):
        j = i + col
        if puzzle[j] == candidate:
            return True
    return False

def used_in_box(puzzle, row, col, candidate):
    # row and col values for cell in top-left corner of relevant box
    box_r = row - (row % 3)
    box_c = col - (col % 3)
    # cell in top-left corner of relevant box
    top_left = box_r * int(math.sqrt(len(puzzle))) + box_c
    # now traverse all cells in box
    for i in range(0, 19, 9):
        for j in range(top_left + i, top_left + i + 3):
            if puzzle[j] == candidate:
                return True
    return False

puzzle = init_puzzle(9)
# make_puzzle(puzzle)
# print_puzzle(puzzle)

#pen = turtle.Turtle()
#box_size = 50
#pen.speed(0)
#draw_board(pen, box_size)

puzzle = solve_puzzle(puzzle)
if puzzle:
    print_puzzle(puzzle)
    print("this puzzle is valid!")
#    fill_board(pen, puzzle, box_size)
else:
    print("no solution exists!")

print("Recursions performed: " + str(count))

#pen.hideturtle()
#turtle.mainloop() 

