"""
This is the only file you should change in your submission!
"""
from basicplayer import basic_evaluate, minimax, get_all_next_moves, is_terminal
from util import memoize, run_search_function, INFINITY, NEG_INFINITY


# TODO Uncomment and fill in your information here. Think of a creative name that's relatively unique.
# We may compete your agent against your classmates' agents as an experiment (not for marks).
# Are you interested in participating if this competition? Set COMPETE=TRUE if yes.

STUDENT_ID = 20747512
AGENT_NAME = "DE007"
# COMPETE = False

# TODO Change this evaluation function so that it tries to win as soon as possible
# or lose as late as possible, when it decides that one side is certain to win.
# You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    The modified focused-evaluate function.
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won
        #if board.is_win() == 2:
        #        score = 10*(42-board.num_tokens_on_board())-1000
        #else:
        #        score = -10*(42-board.num_tokens_on_board())-1000
        score = -10*(42-board.num_tokens_on_board())-1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score


# Create a "player" function that uses the focused_evaluate function
# You can test this player by choosing 'quick' in the main program.
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)


# TODO Write an alpha-beta-search procedure that acts like the minimax-search
# procedure, but uses alpha-beta pruning to avoid searching bad ideas
# that can't improve the result. The tester will check your pruning by
# counting the number of static evaluations you make.

# You can use minimax() in basicplayer.py as an example.
# NOTE: You should use get_next_moves_fn when generating
# next board configurations, and is_terminal_fn when
# checking game termination.
# The default functions for get_next_moves_fn and is_terminal_fn set here will work for connect_four.
def alpha_beta_find_values(board,
                           depth,
                           eval_fn,
                           alpha,
                           beta,
                           get_next_moves_fn=get_all_next_moves,
                           is_terminal_fn=is_terminal):

    #When we have reached our limit of depth we go back up in our recursion with the chosen evaluation function for the board
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    #get all possible next moves and start iterating
    for move, new_board in get_next_moves_fn(board):

        
        alpha = max(alpha, -alpha_beta_find_values(new_board, depth - 1, eval_fn, -beta, -alpha, get_next_moves_fn, is_terminal_fn))
        if alpha >= beta:
            return alpha
    return alpha

def alpha_beta_search(board, depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    
    """
    This is heavily inspired by the minimax search implemented in basicplayer.py
    """
    
    best_val = None

    for move, new_board in get_next_moves_fn(board):
        val = -1 * alpha_beta_find_values(new_board, depth - 1, eval_fn, -float("inf"), float("inf"), get_next_moves_fn, is_terminal_fn)
        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)

    return best_val[1]




# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined alpha_beta_search.)
def alpha_beta_player(board):
    return alpha_beta_search(board, depth=8, eval_fn=focused_evaluate)


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
def ab_iterative_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=focused_evaluate, timeout=5)


# TODO Finally, come up with a better evaluation function than focused-evaluate.
# By providing a different function, you should be able to beat
# simple-evaluate (or focused-evaluate) while searching to the same depth.

def better_evaluate(board):
    raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)


# A player that uses alpha-beta and better_evaluate:
def my_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=better_evaluate, timeout=5)

# my_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)
