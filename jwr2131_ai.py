#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: JACKSON RAFFETY (JWR2131)
    COLLABORATORS: MFR2156, CSR2139
"""

import random
import sys
import time
from heapq import heappop, heappush

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

utility_dict = {}

def compute_utility(board, color):
    """
    Return the utility of the given board state
    (represented as a tuple of tuples) from the perspective
    of the player "color" (1 for dark, 2 for light)
    """
    (p1_count, p2_count) = get_score(board)
    if color == 1:
        return p1_count - p2_count
    else:
        return p2_count - p1_count



############ MINIMAX ###############################

def minimax_min_node(board, color):
    if not get_possible_moves(board,color):
        if board not in utility_dict:
            utility_dict[board] = compute_utility(board,1)
            return compute_utility(board,1)
        else:
            return utility_dict[board]
    min_utility = float("inf")
    for next_position in get_possible_moves(board,color):
        i,j = next_position
        next_board = play_move(board,color,i,j)
        utility = minimax_max_node(next_board,2)
        min_utility = min(min_utility,utility)
    return min_utility

def minimax_max_node(board, color):
    if not get_possible_moves(board,color):
        if board not in utility_dict:
            utility_dict[board] = compute_utility(board,1)
            return compute_utility(board,1)
        else:
            return utility_dict[board]
    max_utility = float("-inf")
    for next_position in get_possible_moves(board,color):
        i,j = next_position
        next_board = play_move(board,color,i,j)
        utility = minimax_min_node(next_board,1)
        max_utility = max(max_utility,utility)
    return max_utility 

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    next_move = ()
    max_utility = float("-inf")
    min_utility = float("inf")
    for next_position in get_possible_moves(board,color):
        x,y = next_position
        board = play_move(board,color,x,y)
        if color == 1:
            utility = minimax_max_node(board,2)
            if utility > max_utility:
                max_utility = utility
                next_move = x,y
        else:
            utility = minimax_min_node(board,1)
            if utility < min_utility:
                min_utility = utility
                next_move = x,y
    return next_move

############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit): 
    level += 1
    if not get_possible_moves(board,color) or level > limit:
        if board not in utility_dict:
            utility_dict[board] = compute_utility(board,1)
            return compute_utility(board,1)
        else:
            return utility_dict[board]
    min_utility = float("inf")
    heap = []
    for next_position in get_possible_moves(board,color):
        i,j = next_position
        next_board = play_move(board,color,i,j)
        heappush(heap,(compute_utility(next_board,1),next_board))
    while heap:
        heuristic_cost,next_board = heappop(heap)
        utility = alphabeta_max_node(next_board,2,alpha,beta,level,limit)
        min_utility = min(min_utility,utility)
        if min_utility <= alpha:
            return min_utility
        beta = min(beta,utility)
    return min_utility


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    level += 1
    if not get_possible_moves(board,color) or level > limit:
        if board not in utility_dict:
            utility_dict[board] = compute_utility(board,1)
            return compute_utility(board,1)
        else:
            return utility_dict[board]
    max_utility = float("-inf")
    heap = []
    for next_position in get_possible_moves(board,color):
        i,j = next_position
        next_board = play_move(board,color,i,j)
        heappush(heap,(-compute_utility(next_board,1),next_board))
    while heap:
        heauristic_cost,next_board = heappop(heap)
        utility = alphabeta_min_node(next_board,1,alpha,beta,level,limit)
        max_utility = max(max_utility,utility)
        if max_utility >= beta:
            return max_utility
        alpha = max(alpha,utility)
    
    return max_utility 


def select_move_alphabeta(board, color): 
    next_move = ()
    max_utility = float("-inf")
    min_utility = float("inf")
    alpha = float("-inf")
    beta = float("inf")
    for next_position in get_possible_moves(board,color):
        x,y = next_position
        board = play_move(board,color,x,y)
        if color == 1:
            utility = alphabeta_max_node(board,2,alpha,beta,0,7)
            if utility > max_utility:
                max_utility = utility
                next_move = x,y
        else:
            utility = alphabeta_min_node(board,1,alpha,beta,0,7)
            if utility < min_utility:
                min_utility = utility
                next_move = x,y
    return next_move


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
