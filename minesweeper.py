import random, time
import re


# Let's create a board object to represent the minesweeper game
# This is so that we can just say "create a new board object" or
# "dig here", or "render this game for this object"


class Board:
    def __init__(self, dim_size, num_bombs):
        # init is to implement all the actions that append when we initialize a new board

        # let's keep track of these parameters
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # let's create the board
        # helper function
        self.board = self.make_new_board()  # plant the bomb
        self.assign_values_to_board()  # assign the number of neighboring bombs to each case

        # initialize a set to keep track of which locations we've uncovered
        # we'll save (row, col) tuples into this set
        self.dug = set()

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
        # we sould construct the list of lists here (or whatever representation you prefer)
        # but since we have a 2D board, list of lists is most natural

        # generate new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # this creates an array like this:
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  ...,
        #  [None, None, ..., None]]
        # we can see how this represents a board!

        # plant the bomb
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size  # number of times dim_size goes into loc
            col = loc % self.dim_size  # the remainder to tell us what index in that row

            if board[row][col] == "*":
                # this means we've already planted a bomb there already so keep going
                # this is why we use a 'while' loop instead of a 'for' loop
                continue

            board[row][col] = "*"
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # now that we have the bombs planted, lets assign value to each case with the number of neighboring bombs

        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue
                else:
                    self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        # check all neighboring locations (need to add extra +1 due to python indexing)
        # add min, max to tackle the side of the board
        for r in range(max(0, row - 1), min(row + 1, self.dim_size - 1) + 1):
            for c in range(max(0, col - 1), min(col + 1, self.dim_size - 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == "*":
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at that location
        # return True if succesful dig, False if bomb

        # a few scenario
        # hit a bomb -> game over
        # dig at location with neighboring bombs -> finish dig
        # dig at location with no neighboring bombs -> recursively dig neighbors!

        self.dug.add((row, col))

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(row + 1, self.dim_size - 1) + 1):
            for c in range(max(0, col - 1), min(col + 1, self.dim_size - 1) + 1):
                if (r, c) in self.dug:
                    continue  # don't dig where you already dig
                self.dig(r, c)

        # if our initial dig didn't hit a bomb, we shouldn't hit a bomb here
        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represnts what the user would see
        visible_board = [
            [None for _ in range(self.dim_size)] for _ in range(self.dim_size)
        ]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

        # put this together in a string
        string_rep = ""
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = "   "
        cells = []
        for idx, col in enumerate(indices):
            format = "%-" + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += "  ".join(cells)
        indices_row += "  \n"

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f"{i} |"
            cells = []
            for idx, col in enumerate(row):
                format = "%-" + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += " |".join(cells)
            string_rep += " |\n"

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + "-" * str_len + "\n" + string_rep + "-" * str_len

        return string_rep


def play(dim_size=10, num_bombs=10):
    # Step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # Step 2: show the user the board and ask for where they want to dig

    # Step 3a: if location is a bomb, show game over message
    # Step 3b: if location is not a bomb, dig recursively until each square is at least next to a bomb
    # Step 4: repeat steps 2 and 3 until there are no more places to dig -> VICTORY!

    safe = True

    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)
        # 0,0 or 0, 0 or 0,   0
        user_input = re.split(
            ",(\\s)*", input("Where would you like to dig ? Input as row, col: ")
        )  # ',\\s)* says : split every time you see a coma and any number of space
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location. Try again!")
            continue

        # if valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb
            break  # game over rip

        # 2 ways to end loop
    if safe:
        print("Congratulations, you're victorious!")
    else:
        print("GAME OVER!")
        # let's reveal the whole board
        board.dug = [
            (r, c) for r in range(board.dim_size) for c in range(board.dim_size)
        ]
        print(board)


if __name__ == "__main__":
    play()
