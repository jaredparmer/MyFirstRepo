#!/usr/bin/env python3

import random

def make_puzzle():
    puzzle = []
    for i in range(0, 9):
        row = []
        while len(row) != 9:
            temp = random.randint(1,9)
            if temp not in row:
                row.append(temp)
        puzzle.append(row)
    return puzzle

def print_puzzle(puzzle):
    for i in range(len(puzzle)):
        if i % 3 == 0:
            print('-------------------------')
        for j in range(len(puzzle[i])):
            if j % 3 == 0:
                print('|', end= ' ')
            print(puzzle[i][j], end=' ')
        print('|')
    print('-------------------------')

def main():
    puzzle = make_puzzle()
    print_puzzle(puzzle)

if __name__ == '__main__':
    main()
