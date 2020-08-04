#!/usr/bin/env python3

import turtle
import random
import math

""" to-dos:
        - rebuild fundamental data structure            IN PROGRESS 04/08
        - fill cells while solving?
            - gray candidates, black finals?
        - randomize solve patterns                      IN PROGRESS 31/07
        - optimize solve function                       IN PROGRESS 31/07
        - enhance solve fn to count solutions
        - pickle puzzles
        - removal algorithm - basic
        - removal algorithm - multiple difficulties
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

""" REQUIRES UPDATE TO REFLECT NEW DS
"""
# postcondition: all non-zero values filled into board, pen is up
def fill_board(t, puzzle, box_size):
    # initialize pen
    t.pu()
    t.goto(box_size * -4.5 + box_size * (1/2),
            box_size * 3.5 + box_size * (1/4))
    t.pd()

    # fill boxes with elements from puzzle
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != 0:
                t.write(str(puzzle[i][j]), move=False, align="center", 
                        font=("Arial", int(box_size / 2.5), "normal"))
            t.pu()
            t.fd(box_size)
            t.pd()
        t.pu()
        t.bk(box_size * 9)
        t.rt(90)
        t.fd(box_size)
        t.lt(90)
        t.pd()
    t.pu()

""" REQUIRES UPDATE TO REFLECT NEW DS
"""
# precondition: x and y be w/n range of grid, puzzle have corresponding value
# postcondition: cell (x, y) is filled with puzzle[x][y], pen is up
def fill_cell(t, x, y, puzzle, box_size):
    pen_to_cell(t, x, y, box_size)
    if puzzle[x][y] != 0:
        t.write(str(puzzle[x][y]), move=False, align="center",
                font=("Arial", 12, "normal"))
    t.pu()

""" This function initializes a blank puzzle. A puzzle is a list of 81 lists,
where each inner list represents the candidate values for a particular cell.
The row and column for each cell is implicit in the data structure as follows:
    row1col1, row1col2, ..., row1col9,
    row2col1, row2col2, ..., row2col9,
    .
    .
    .
    row9col1, row9col2, ..., row9col9
When the list of candidate values for a particular cell is exactly 1, that
cell has a determinate value. When the list of candidate values is empty,
there is no valid value for that cell and the puzzle is thus unsolvable.
"""
def init_puzzle(size):
    puzzle = []
    for i in range(size**2):
        candidates = []
        for j in range(1, size + 1):
            candidates.append(j)
        puzzle.append(candidates)
    return puzzle

# generates randomly filled puzzle
def make_puzzle(puzzle, size):
    for i in range(len(puzzle)):
        puzzle[i] = []
        puzzle[i].append(random.randint(1, size))
    return puzzle

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

""" REQUIRES UPDATE TO REFLECT NEW DS
"""
def solve_puzzle(puzzle):
    # base case: puzzle is completely filled out
    if puzzle_is_complete(puzzle):
        print("puzzle is complete!")
        return True

    # recursion case
    # traverse entire puzzle, by row and column
    for row in range(9):
        for col in range(9):
            # verify present cell is empty
    #        print(f"checking cell ({row}, {col})...")
            if puzzle[row][col] == 0:
    #            print("cell is empty...")
                for candidate in range(1, 10):
    #                print(f"trying {candidate} in ({row}, {col})...")
                    if (not used_in_row(puzzle, row, candidate) and
                        not used_in_col(puzzle, col, candidate) and
                        not used_in_box(puzzle, row, col, candidate)):
                        # if all met, candidate looks good; tentatively assign
    #                    print(f"{candidate} looks promising...")
                        puzzle[row][col] = candidate
                        if solve_puzzle(puzzle):
                            return True
                        # otherwise, candidate is bad; unassign and try again
    #                    print(f"no dice! removing {candidate} from "
    #                          f"{row}, {col}...")
                        puzzle[row][col] = 0
                return False                                            
    return False

""" REQUIRES UPDATE TO REFLECT NEW DS
"""
def used_in_row(puzzle, size, candidate):
    for i in range(0, size**2, size):
        if len(puzzle[i]) == 1 and puzzle[i][0] == candidate:
            return True
    return False

""" REQUIRES UPDATE TO REFLECT NEW DS
"""
def used_in_col(puzzle, col, candidate):
    for i in range(9):
        if puzzle[i][col] == candidate:
            return True
    return False

""" REQUIRES UPDATE TO REFLECT NEW DS
"""
def used_in_box(puzzle, row, col, candidate):
    box_r = row - (row % 3)
    box_c = col - (col % 3)
    for i in range(3):
        for j in range(3):
            if puzzle[box_r + i][box_c + j] == candidate:
                return True
    return False

def main():
    puzzle = init_puzzle(9)
    print_puzzle(puzzle)
    puzzle = make_puzzle(puzzle, 9)
    print_puzzle(puzzle)

#    if solve_puzzle(puzzle):
#        print_puzzle(puzzle)
#        print("this puzzle is valid!")
#    else:
#        print("No solution exists!")

#    if solve_puzzle(puzzle):
#        pen = turtle.Turtle()
#        box_size = 50
#        pen.speed(0)
#        draw_board(pen, box_size)
#        fill_board(pen, puzzle, box_size)
#        pen.hideturtle()
#        turtle.mainloop() 
#    else:
#        print("no solution exists!")

if __name__ == '__main__':
    main()
