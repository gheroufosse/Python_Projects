def find_next_empty(puzzle):
    # finds the next row, col on the puzzle that's not filled yet --> rep with -1
    # return row, col tuple (or (None, None) if there is None)
    # keep in mind 0-indexing

    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c

    return None, None  # if no empty case in the puzzle left


def is_valid(puzzle, guess, row, col):
    # figures out whether the gues at the row/col of the puzzle is a valid guess
    # returns True if is valid, False otherwise

    # let's start with the row:
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    # and then now the square
    # this is tricky, but we want to get where the 3x3 square starts
    # and iterate over the 3 values in the row/col

    row_start = (row // 3) * 3  # in which row the square starts
    col_start = (col // 3) * 3  # which col

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False  # already in this 3x3 matrix -> not the right guess

    # if we get here, it is valid guess
    return True


def solve_sudoku(puzzle):
    # solve sudoku using backtracking
    # input = list of lists for each row of the puzzle
    # return whether a solution exists and return the solution if it exists

    # step1: choose somewhere on the puzzle to make a guess

    row, col = find_next_empty(puzzle)

    # step 1.1: if there's nowhere left, then we're done because we only allowed valid inputs

    if row is None:
        return True

    # step 2: if there is a place to put a number, then make a guess between 1 and 9
    for guess in range(1, 10):  # 1, 2, ... 9.
        # step 3: check if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            # step 3.1: if this is valid, then place that guess on the puzzle!
            puzzle[row][col] = guess
            # now recurse usnig this puzzle!
            # step 4: recursively call our function
            if solve_sudoku(puzzle):
                return True
        # step 5: if not valid OR if our guess does not solve the puzzle, then we need to
        # backtrack and try a new number -> reset
        puzzle[row][col] = -1

    # step 6: if none of the numbers that we try work, then this puzzle is UNSOLVABLE
    return False


if __name__ == "__main__":
    example_board = [
        [3, 9, -1, -1, 5, -1, -1, -1, -1],
        [-1, -1, -1, 2, -1, -1, -1, -1, 5],
        [-1, -1, -1, 7, 1, 9, -1, 8, -1],
        [-1, 5, -1, -1, 6, 8, -1, -1, -1],
        [2, -1, 6, -1, -1, 3, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, 4],
        [5, -1, -1, -1, -1, -1, -1, -1, -1],
        [6, 7, -1, 1, -1, 5, -1, 4, -1],
        [1, -1, 9, -1, -1, -1, 2, -1, -1],
    ]
    print(solve_sudoku(example_board))
    print(example_board)
