

"""
An AI player for Othello. This is the template file that you need to  
complete.

@author: Aarav Patel ap4538
"""

import random
import sys
import time
import math
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move


corners = {(0,0),(0,7),
           (7,0),(7,7)}

dangerZone = {      (1,0),      (6,0),
              (0,1),(1,1),      (6,1),(7,1),

              (0,6),(1,6),      (6,6),(7,6),
                    (1,7),      (6,7)}



def compute_utility(board, color):
    scores = get_score(board)
    if color == 1:
        return scores[0] - scores[1]
    elif color == 2:
        return scores[1] - scores[0]

############ MINIMAX ###############################

def minimax_min_node(board, color, elapsed, num):
    if elapsed >= 10/num or len(get_possible_moves(board, color)) == 0:
        return compute_utility(board, color)
    startTime = time.time()
    opp_color = 1 if color == 2 else 2
    moveUtil = {}
    for move in get_possible_moves(board, color):
        endTime = time.time()
        elapsed += endTime - startTime
        moveUtil[move] = minimax_max_node(play_move(board, color, move[0], move[1]), opp_color, elapsed, num)
    return moveUtil[min(moveUtil, key=moveUtil.get)]


def minimax_max_node(board, color, elapsed, num):
    if elapsed >= 10/num or len(get_possible_moves(board, color)) == 0:
        return compute_utility(board, color)
    startTime = time.time()
    opp_color = 1 if color == 2 else 2
    moveUtil = {}
    for move in get_possible_moves(board, color):
        endTime = time.time()
        elapsed += endTime - startTime
        moveUtil[move] = minimax_min_node(play_move(board, color, move[0], move[1]), opp_color, elapsed, num)

    return moveUtil[max(moveUtil, key=moveUtil.get)]


def select_move_minimax(board, color):
    num = len(get_possible_moves(board, color))
    for move in get_possible_moves(board, color):
        if move in corners:
            return move

    opp_color = 1 if color == 2 else 2
    moveUtil = {}
    moveUtility = {}
    if len(get_possible_moves(board, color)) == 0:
        return compute_utility(board, color)
    for move in get_possible_moves(board, color):
        if move in dangerZone:
            moveUtility[move] = minimax_min_node(play_move(board, color, move[0], move[1]), opp_color, 0, num)
        else:
            moveUtil[move] = minimax_min_node(play_move(board, color, move[0], move[1]), opp_color, 0, num)
    if len(moveUtil) > 0:
        return max(moveUtil, key=moveUtil.get)
    else:
        return max(moveUtility, key=moveUtility.get)

############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, depth, alpha, beta): 
    if depth == 0 or len(get_possible_moves(board, color)) == 0:
        return compute_utility(board, color)
    opp_color = 1 if color == 2 else 2
    moveUtil = {}
    for move in get_possible_moves(board, color):
        moveUtil[move] = alphabeta_max_node(play_move(board, color, move[0], move[1]), opp_color, depth - 1, alpha, beta)
        bet = min(beta, moveUtil[move])
        if bet <= alpha:
            break
    return moveUtil[min(moveUtil, key=moveUtil.get)]


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, depth, alpha, beta):
    if depth == 0 or len(get_possible_moves(board, color)) == 0:
        return compute_utility(board, color)
    opp_color = 1 if color == 2 else 2
    moveUtil = {}
    for move in get_possible_moves(board, color):
        moveUtil[move] = alphabeta_min_node(play_move(board, color, move[0], move[1]), opp_color, depth - 1, alpha, beta)
        alph = max(alpha, moveUtil[alpha])
        if beta <= alph:
            break

    return moveUtil[max(moveUtil, key=moveUtil.get)]


def select_move_alphabeta(board, color): 
    for move in get_possible_moves(board, color):
        if move in corners:
            return move

    opp_color = 1 if color == 2 else 2
    moveUtil = {}
    if len(get_possible_moves(board, color)) == 0:
        return compute_utility(board, color)
    for move in get_possible_moves(board, color):
        moveUtil[move] = alphabeta_min_node(play_move(board, color, move[0], move[1]), opp_color, 3, 0, 0)

    return max(moveUtil, key=moveUtil.get)


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            movei, movej = select_move_minimax(board, color)
            #movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()