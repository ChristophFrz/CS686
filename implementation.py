"""
This is the only file you should change in your submission!
"""
from basicplayer import basic_evaluate, minimax, get_all_next_moves, is_terminal
from util import memoize, run_search_function, INFINITY, NEG_INFINITY
from connectfour import ConnectFourBoard




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
        #if board.is_win() == board.get_current_player_id():
        #        score = 10*(42-board.num_tokens_on_board())-1000
        #else:
        #       score = -10*(42-board.num_tokens_on_board())-1000
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
def alphabeta_find_board_value(alpha, beta, maxTurn, board, current_moves, repetitive_moves, depth, eval_fn,
                             get_next_moves_fn=get_all_next_moves,
                             is_terminal_fn=is_terminal):
    """
    Minimax helper function: Return the minimax value of a particular board,
    given a particular depth to estimate to
    """
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    if maxTurn:
        v = -float("inf")
        for move, new_board in get_next_moves_fn(board):
            current_moves.append(move)
            val = -1 * alphabeta_find_board_value( alpha, beta, False, new_board, current_moves, repetitive_moves, depth-1, eval_fn,
                                            get_next_moves_fn, is_terminal_fn)
            v = max(v, val)
            alpha = max(alpha, v)
            if beta <= alpha:
            #if v > beta:
                break
        return v
    else:
        v = float("inf")
        for move, new_board in get_next_moves_fn(board):
            current_moves.append(move)
            val = -1 * alphabeta_find_board_value( alpha, beta, True, new_board, current_moves, repetitive_moves, depth-1, eval_fn,
                                            get_next_moves_fn, is_terminal_fn)
            v = min(v, -val)
            beta = min(beta, v)
            if beta <= alpha:
            #if v < alpha:
                break
        return -v


def alpha_beta_search(board, depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    best_val = None
    alpha = -float("inf")
    beta = float("inf")
    repetitive_moves = {}
    
    for move, new_board in get_next_moves_fn(board):
        current_moves = []
        current_moves.append(move)
        val = -1 * alphabeta_find_board_value(alpha, beta, False, new_board, current_moves, repetitive_moves, depth-1, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        #print("This is val: ", val, "move  ", move)
        if best_val is None or val > best_val[0]:
            best_val = (val, move, new_board)
    #test = list(filter(lambda x: len(x) > 1, board.chain_cells(2)))
    #print(test)
    print("MINIMAX_alphabeta: Decided on column {} with rating {}".format(best_val[1], best_val[0]))
    return best_val[1]





# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined alpha_beta_search.)
focused_evaluate = memoize(focused_evaluate)
def alpha_beta_player(board):
    return alpha_beta_search(board, depth=8, eval_fn=focused_evaluate)


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
def ab_iterative_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=focused_evaluate, timeout=5)

def find_possible4(board, chain, other_player_ID):
    possible4_by3 = 0
    possible4_by2 = 0
    for i in range(len(chain)):
        tuples = sorted(chain[i], key=lambda x:x[0], reverse=True)
        if True:
            if True:
                #tuples = sortRow_chain[i]
                # check if 4 in a row possible
                if tuples[0][0] == tuples[1][0]:
                    r_min = min(tuples[j][1] for j in range(len(tuples)))
                    r_max = max(tuples[j][1] for j in range(len(tuples)))
                    count_free = 0
                    for k in range(1, 4-len(tuples)+1):
                        if r_min - k >= 0 and board.get_cell(tuples[0][0], r_min-k) != other_player_ID:
                            count_free += 1
                            
                    if count_free == (4-len(tuples)) and len(tuples) == 3:
                        possible4_by3 += 1
                    elif count_free == (4-len(tuples)) and len(tuples) == 2:
                        possible4_by2 += 1
                        
                    count_free = 0
                    for k in range(1, 4-len(tuples)+1):
                        if r_max + k <= 6 and board.get_cell(tuples[0][0], r_max+k) != other_player_ID:
                            count_free += 1
                            
                    if count_free == (4-len(tuples)) and len(tuples) == 3:
                        possible4_by3 += 1
                    elif count_free == (4-len(tuples)) and len(tuples) == 2:
                        possible4_by2 += 1
                        
                # check if 4 in a column
                elif tuples[0][1] == tuples[1][1]:
                    #c_max = max(tuples[j][0] for j in range(len(tuples)))
                    c_min = min(tuples[j][0] for j in range(len(tuples)))
                    count_free = 0
                    for k in range(1, 4-len(tuples)+1):
                        if c_min - k >= 0 and board.get_cell(c_min-k, tuples[0][1]) != other_player_ID:
                            count_free += 1
                            
                    if count_free == (4-len(tuples)) and len(tuples) == 3:
                        possible4_by3 += 1
                    elif count_free == (4-len(tuples)) and len(tuples) == 2:
                        possible4_by2 += 1
                        
                # check if 4 diagonal
                else:
                    # currently from lowest point to upper right
                    if tuples[0][1] < tuples[1][1]:
                        # check upper right
                        r_min =  min(tuples[j][1] for j in range(len(tuples)))
                        c_max = max(tuples[j][0] for j in range(len(tuples)))
                        count_free = 0
                        for k in range(1, 4-len(tuples)+1):
                            if r_min-k >= 0 and c_max+k <= 5 and board.get_cell(c_max+k, r_min-k) != other_player_ID:
                                count_free += 1
                                
                        if count_free == (4-len(tuples)) and len(tuples) == 3:
                            possible4_by3 += 1
                        elif count_free == (4-len(tuples)) and len(tuples) == 2:
                            possible4_by2 += 1
                            
                        # check lower left
                        r_max = max(tuples[j][1] for j in range(len(tuples)))
                        c_min = min(tuples[j][0] for j in range(len(tuples)))
                        count_free = 0
                        for k in range(1, 4-len(tuples)+1):
                            if r_max+k <= 6 and c_min-k >= 0 and board.get_cell(c_min-k, r_max+k) != other_player_ID:
                                count_free += 1
                                
                        if count_free == (4-len(tuples)) and len(tuples) == 3:
                            possible4_by3 += 1
                        elif count_free == (4-len(tuples)) and len(tuples) == 2:
                            possible4_by2 += 1
                            
                    # currently from lowest point to upper left
                    elif tuples[0][1] > tuples[1][1]:
                        # check upper left
                        r_min =  min(tuples[j][1] for j in range(len(tuples)))
                        c_min = min(tuples[j][0] for j in range(len(tuples)))
                        count_free = 0
                        for k in range(1, 4-len(tuples)+1):
                            if r_min-k >= 0 and c_min-k >= 0 and board.get_cell(c_min-k,r_min-k) != other_player_ID:
                                count_free += 1
                                
                        if count_free == (4-len(tuples)) and len(tuples) == 3:
                            possible4_by3 += 1
                        elif count_free == (4-len(tuples)) and len(tuples) == 2:
                            possible4_by2 += 1
                            
                        # check lower right
                        r_max = max(tuples[j][1] for j in range(len(tuples)))
                        c_max = max(tuples[j][0] for j in range(len(tuples)))
                        count_free = 0
                        for k in range(1, 4-len(tuples)+1):
                            if r_max+k <= 6 and c_max+k <= 5 and board.get_cell(c_max+k, r_max+k) != other_player_ID:
                                count_free += 1
                                
                        if count_free == (4-len(tuples)) and len(tuples) == 3:
                            possible4_by3 += 1
                        elif count_free == (4-len(tuples)) and len(tuples) == 2:
                            possible4_by2 += 1
    return possible4_by3, possible4_by2
    
# TODO Finally, come up with a better evaluation function than focused-evaluate.
# By providing a different function, you should be able to beat
# simple-evaluate (or focused-evaluate) while searching to the same depth.

def better_evaluate(board):
    score = 0
    if board.is_game_over():
        score = -10*(42-board.num_tokens_on_board())-1000
        return score
    # rows
    for i in range(0,6):
        for j in range(0,4):
            tmp_score = 0
            for k in range(0,4):
                if board.get_cell(i,j+k) == board.get_other_player_id():
                    tmp_score -= 1
                elif board.get_cell(i,j+k) == board.get_current_player_id():
                    tmp_score += 1
            if tmp_score > 0:
                score += 1
            elif tmp_score < 0:
                score -= 1
                
                
    # columns
    for j in range(0,7):
        for i in range(0,3):
            for k in range(0,4):
                tmp_score = 0
                if board.get_cell(i+k, j) == board.get_other_player_id():
                    tmp_score -= 1
                elif board.get_cell(i+k, j) == board.get_current_player_id():
                    tmp_score += 1
            if tmp_score > 0:
                score += 1
            elif tmp_score < 0:
                score -= 1
                    
    # vertical down
    for i in range(0,3):
        for j in range(0,4):
            tmp_score = 0
            for k in range(0,4):
                if board.get_cell(i+k, j+k) == board.get_other_player_id():
                    tmp_score -= 1
                elif board.get_cell(i+k, j+k) == board.get_current_player_id():
                    tmp_score += 1
            if tmp_score > 0:
                score += 1
            elif tmp_score < 0:
                score -= 1
                    
    # vertical up
    for i in range(3):
        for j in range(4):
            tmp_score = 0
            for k in range(4):
                if board.get_cell(5-i-k, j+k) == board.get_other_player_id():
                    tmp_score -= 1
                elif board.get_cell(5-i-k, j+k) == board.get_current_player_id():
                    tmp_score += 1
            if tmp_score > 0:
                score += 1
            elif tmp_score < 0:
                score -= 1
                    
    return score
                
    
    
    
    
    
    
    # filter chains with length of 1
#    current_chains = list(filter(lambda x: len(x) > 1, board.chain_cells(board.get_current_player_id())))
#    other_chains = list(filter(lambda x: len(x) > 1, board.chain_cells(board.get_other_player_id())))
#    #current_chain2, current_chain3 = 0,0
#    #other_chain2, other_chain3 = 0,0
#    
#
#    if board.is_game_over():
#        score = -10*(42-board.num_tokens_on_board())-1000
#    else:
#        count = 0
#        if len(current_chains) >= 1:
#            for i in range(len(current_chains)):
#                if len(current_chains[i]) >= 2:
#                    count += 1
#                    break;
#        if count >= 1:
#            (current_possible4_by3, current_possible4_by2)  = find_possible4(board, current_chains, board.get_other_player_id())
#            (other_possible4_by3, other_possible4_by2) = find_possible4(board, other_chains, board.get_current_player_id())
#            #other_possible4_by3, other_possible4_by2 =0,0
#            score = 43*(current_possible4_by3 - other_possible4_by3) + 17*(current_possible4_by2 - other_possible4_by2)
#        elif count == 0:
#            score = board.longest_chain(board.get_current_player_id()) * 10
#            # Prefer having your pieces in the center of the board.
#            for row in range(6):
#                for col in range(7):
#                    if board.get_cell(row, col) == board.get_current_player_id():
#                        score -= abs(3-col)
#                    elif board.get_cell(row, col) == board.get_other_player_id():
#                        score += abs(3-col)
#    return score

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)


# A player that uses alpha-beta and better_evaluate:
#def my_player(board):
#    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=better_evaluate, timeout=5)

#my_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)

my_player = lambda board: run_search_function(board, search_fn = alpha_beta_search, eval_fn=better_evaluate)
