# An amazing library which is the sole reason
# why this program has been written in python
import numpy as np
import random
import itertools
import copy

correct = list(range(1, 10))

# Hard-coded the starting point because it's
# faster than anything else

# Step 1: Starting point
# A known solved 2d array for Sudoku
sudo_list_template = np.array([
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 1, 5, 6, 4, 8, 9, 7],
    [5, 6, 4, 8, 9, 7, 2, 3, 1],
    [8, 9, 7, 2, 3, 1, 5, 6, 4],
    [3, 1, 2, 6, 4, 5, 9, 7, 8],
    [6, 4, 5, 9, 7, 8, 3, 1, 2],
    [9, 7, 8, 3, 1, 2, 6, 4, 5],
])

sudo_list = []


def shuffle_list(start: int, end: int, transpose: bool = False) -> None:
    '''A Random Shuffler function to dry up the code'''

    # Need this to modify the global scoped sudo_list
    global sudo_list

    if transpose:
        # np coming in handy
        np.random.shuffle(np.transpose(sudo_list[:, start:end]))
    else:
        np.random.shuffle(sudo_list[start:end, :])


def sudokuGenerator() -> list:
    '''
    A unique sudoku generator

    NOTE: This function was previously just a normal callable
    however, as of 21.8.2021, it is a generator
    @mkpro118 converted this function to a generator in order
    to allow multiple sudoku boards to be generated faster
    and allow infinite generation of sudoku boards

    Multiple for blocks used to increase randomness
    Throw-away variables used for the loops to increase speed
    '''

    # Needed to modify the global scoped sudo_list
    global sudo_list_template, sudo_list

    while True:
        sudo_list = np.copy(sudo_list_template)
        # Anywhere between 5 to 10 random shuffling
        # for every step

        # Shuffling happens in 9 ways

        a = list(range(1, 10))
        b = list(range(1, 10))

        # Step 2: Swap Numbers
        for _ in range(random.randint(5, 10)):
            random.shuffle(a)
            random.shuffle(b)

            ref = dict(zip(a, b))

            for i, row in enumerate(sudo_list):
                for j, col in enumerate(row):
                    sudo_list[i, j] = ref[col]

        # Step 3: Shuffling Col 1-3
        for _ in range(random.randint(5, 10)):
            shuffle_list(0, 3, True)

        # Step 4: Shuffling Col 4-6
        for _ in range(random.randint(5, 10)):
            shuffle_list(3, 6, True)

        # Step 5: Shuffling Col 7-9
        for _ in range(random.randint(5, 10)):
            shuffle_list(6, 9, True)

        # Step 6: Shuffling Row 1-3
        for _ in range(random.randint(5, 10)):
            shuffle_list(0, 3)

        # Step 7: Shuffling Row 4-6
        for _ in range(random.randint(5, 10)):
            shuffle_list(3, 6)

        # Step 8: Shuffling Row 7-9
        for _ in range(random.randint(5, 10)):
            shuffle_list(6, 9)

        # Step 9: Shuffling rows in sets of 3 (3x9)
        rows = np.array_split(sudo_list, 3)
        for _ in range(random.randint(5, 10)):
            # not using numpy's random function because
            # rows is a list, not a np.ndarray
            random.shuffle(rows)
        sudo_list = np.vstack(rows)

        # Step 10: Shuffling columns in sets of 3 (9x3)
        cols = np.array_split(sudo_list.T, 3)
        for _ in range(random.randint(5, 10)):
            # not using numpy function because cols
            # is a list, not a np.ndarray
            random.shuffle(cols)
        sudo_list = np.vstack(cols)

        yield sudo_list.tolist()


def sudokuCheck(rows: list) -> dict:
    '''
    Sudoku Solution Validator.
    Validates a Sudoku before sending it for masking

    Paramters:
    rows -> a 2d list containing a generated sudoku
    '''

    # Creates list of all columns
    cols = [col for col in list(zip(*rows))]
    squares = []
    # Creates list of all squares
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            squares.append(list(itertools.chain(*[row[j:j + 3] for row in rows[i:i + 3]])))

    wrong_rows, wrong_cols, wrong_squares = [], [], []
    # Checks for errors in rows
    for number, row in enumerate(rows, 1):
        if not (correct == sorted(row)):
            wrong_rows.append(number)

    # Checks for errors in columns
    for number, col in enumerate(cols, 1):
        if not (correct == sorted(col)):
            wrong_cols.append(number)

    # Checks for errors in squares
    for number, square in enumerate(squares, 1):
        if not (correct == sorted(square)):
            wrong_squares.append(number)
    if len(wrong_rows) == len(wrong_cols) == len(wrong_squares) == 0:
        return {'valid': True, }
    else:
        return {'valid': False, 'rows': wrong_rows, 'cols': wrong_cols, 'squares': wrong_squares, }


def maskSudoku(sudoku: list, level: str) -> list:
    '''
    Masking function
    Removes random spots from the sudoku
    THe number of spot removed depends on
    the level of the sudoku
    Easy -> 30 spots are filled
    Medium -> 27 spots are filled
    Hard -> 25 spots are filled
    Expert -> 22 spots are filled

    Paramters:
    sudoku -> a 2d list containing a solved sudoku
    level -> the level of difficulty
    '''
    sudoku_copy = copy.deepcopy(sudoku)
    mask = []
    num = 30 if level == 'Easy' else 27 if level == 'Medium' else 25 if level == 'Hard' else 22
    num = 81 - num
    while len(mask) < num:
        pos = (random.randint(0, 8), random.randint(0, 8))
        if pos not in mask:
            mask.append(pos)
    for row, col in mask:
        sudoku_copy[row][col] = 0
    return sudoku_copy


# Driver Code to test the program
# if __name__ == '__main__':
#     level = 'Easy'
#     generator = sudokuGenerator()
#     print(solution := sudokuCheck(next(generator))['valid'])
#     print(solution)
#     print(problem := maskSudoku(solution, level))