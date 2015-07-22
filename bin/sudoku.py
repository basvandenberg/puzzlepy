#!/usr/bin/env python3

import os
import sys
import argparse
import traceback

from puzzlepy import sudoku

def main(task, puzzle):

    # Solve and evaluate.
    if(task == 'solve'):

        file = '../data/sudoku_%04d.txt' % (puzzle)
        sudoku = sudoku.Sudoku.load(file)
        solver = sudoku.SudokuSolver(sudoku)
        level = solver.evaluate_difficulty()

        print('level: %i' % (level))

    # Generate.
    if(task == 'generate'):

        outdir = '../data/'

        for i in range(5000):

            grid = sudoku.SudokuPatternGenerator.random_grid()
            pattern = sudoku.SudokuPatternGenerator.to_string(grid)
            #print(pattern)

            sudoku.SudokuGenerator.generate_from_pattern(pattern, 25, outdir, backtrack=False)

def solve(fin, fout):

    print(fin)
    print(fout)

def generate(fout):

    print(fout)

if __name__ == "__main__":

    # Parse arguments.
    parser = argparse.ArgumentParser()

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--solve', action='store_true')
    action.add_argument('--generate', action='store_true')

    parser.add_argument('--input-file', type=argparse.FileType())
    parser.add_argument('--output-file', type=argparse.FileType('w'), 
                        optional=True)

    args = parser.parse_args()

    if(args.solve):
        solve(args.input_file, args.output_file)

    elif(args.generate):
        generate(args.output_file)
