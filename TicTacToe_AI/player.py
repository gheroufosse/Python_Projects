import random
import math


class Player:
    def __init__(self, letter):
        # letter is x  or o
        self.letter = letter

    # we want all players to get their next move given a game
    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "'s turn. Input move (1-9):")
            # we're going to check that this is a correct value by trying to cast
            # it to an integer, and it it's not, then we say its invalid
            # if that spot is not available on the board, we also say its invalid
            try:
                val = int(square) - 1
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid square. Try again")

        return val


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(
                game.available_moves()
            )  # randomnly choose one if start
        else:
            # choose square based on mi-max algo
            square = self.minimax(game, self.letter)["position"]
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = "0" if player == "X" else "X"

        # first, we want to check if the previous move is a winner
        # this is our base case -> the one that regulate the choice for the computer
        # All moves are gonna be played recursively and eventually we will have a winner,
        # the computer tracks this and make the best choice according to the probable winner
        if state.current_winner == other_player:
            # we should return position AND score because we need to keep track of the score
            # for minmax to work
            return {
                "position": None,
                "score": 1 * (state.num_empty_squares() + 1)
                if other_player == max_player
                else -1 * (state.num_empty_squares() + 1),
            }

        elif not state.num_empty_squares():
            return {"position": None, "score": 0}

        if player == max_player:
            best = {
                "position": None,
                "score": -math.inf,
            }  # each score should maximize (be larger)
        else:
            best = {
                "position": None,
                "score": math.inf,
            }  # each score should be minimize for other player

        for possible_move in state.available_moves():
            # step 1: make a move, try that spot
            state.make_move(possible_move, player)
            # step 2: recurse using minimax to simulate a game after maknig that move
            sim_score = self.minimax(
                state, other_player
            )  # now, we alternate player -> 1 player plays after each other

            # step 3: undo that move
            state.board[possible_move] = " "
            state.current_winner = None
            sim_score[
                "position"
            ] = possible_move  # otherwise this will get messed up from the recursion
            # step 4: update the dictionaries if necessary
            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best = sim_score
            else:
                if sim_score["score"] < best["score"]:
                    best = sim_score

        return best
