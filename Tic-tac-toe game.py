# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 22:23:01 2020

@author: hp
"""
from os import system
import numpy as np
import time
from math import inf as infinity
from random import choice
import platform


AI = -1
HUMAN = 1
board = np.zeros((3,3))




## To clears the console
def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')



## A function that returns a set contians all available moves
def Available_Moves(board):
    available_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                available_moves.append((i,j))
    return available_moves            
    


## A function that returns if the move is available or not
def IsAvailable(i, j):
    if (i,j) in Available_Moves(board):
        return True
    else:
        return False



## A function that checks if the player won or not
def IsWin(board, player):
    win_case = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    if [player, player, player] in win_case:
        return True
    else:
        return False



## A function that makes the players be able to set the moves
def Set_Moves(i, j, player):
    if IsAvailable(i, j):
        board[i][j] = player
        return True
    else:
        return False



## A function to heuristic evaluation of board
def Utility(board):
    if IsWin(board, AI):
        score = +1
    elif IsWin(board, HUMAN):
        score = -1
    else:
        score = 0
    return score   



## This function test if the human or computer wins
def Game_Over(board):
    return IsWin(board, HUMAN) or IsWin(board, AI)



## AI function that choice the best move
def MiniMax(board, depth, player):    
    if player == AI:
        bestScore = [-1, -1, -infinity]
    else:
        bestScore = [-1, -1, infinity]
    
    if depth == 0 or Game_Over(board):
        score = Utility(board)
        return [-1, -1, score]
    
    for move in Available_Moves(board):
        i, j = move[0], move[1]
        board[i][j] = player
        score = MiniMax(board, depth - 1, -player)
        board[i][j] = 0
        score[0], score[1] = i, j
        
        if player == AI:
           if score[2] > bestScore[2]:
                bestScore = score  
        else:
            if score[2] < bestScore[2]:
                bestScore = score 
    
    return bestScore        



## It calls the minimax function if the depth < 9 else it choices a random coordinate.
def AI_Turn(AI_Choice, HUMAN_Choice):
    depth = len( Available_Moves(board))
    if depth == 0 or Game_Over(board):
        return
    
    clean()
    print(f'AI turn [{AI_Choice}]')
    Board(board, AI_Choice, HUMAN_Choice)
    
    if depth == 9:
        i = choice([0, 1, 2])
        j = choice([0, 1, 2])
    else:
        move = MiniMax(board, depth, AI)
        i, j = move[0], move[1]
    
    Set_Moves(i, j, AI)
    time.sleep(1)   



## The Human plays choosing a valid move
def HUMAN_Turn(AI_Choice, HUMAN_Choice):
    depth = len( Available_Moves(board))
    if depth == 0 or Game_Over(board):
        return
    
    move = -1
    moves = {
        7: [0, 0], 8: [0, 1], 9: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        1: [2, 0], 2: [2, 1], 3: [2, 2],
    }

    clean()
    print(f'Human turn [{HUMAN_Choice}]')
    Board(board, AI_Choice, HUMAN_Choice) 

    while move < 1 or move > 9:
        try:
            move = int(input('Enter Number from 1 to 9: '))
            coordinate = moves[move]
            can_move = Set_Moves(coordinate[0], coordinate[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')        



## It's just a design for my game
def Board(board, AI_Choice, HUMAN_Choice):
    chars = {
        -1: HUMAN_Choice,
        +1: AI_Choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in board:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)





## The main function that calls all functions
def main():
    clean()
    HUMAN_Choice = ''  # X or O
    AI_Choice = ''  # X or O
    first = ''  # if human is the first
    
    while HUMAN_Choice == '':
        try:
            print('')
            HUMAN_Choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')
    
    # Setting computer's choice
    if HUMAN_Choice == 'X':
        AI_Choice = 'O'
    else:
        AI_Choice = 'X'
    
    #whose play first
    clean()
    while first == '':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')    



    # Our game is here

    while len(Available_Moves(board)) > 0 and not Game_Over(board):
         if first == 'N':
             AI_Turn(AI_Choice, HUMAN_Choice)
             first = ''

         HUMAN_Turn(AI_Choice, HUMAN_Choice)
         AI_Turn(AI_Choice, HUMAN_Choice)

        # Game over message
         if IsWin(board, HUMAN):
             clean()
             print(f'Human turn [{HUMAN_Choice}]')
             Board(board, AI_Choice, HUMAN_Choice)
             print('YOU WIN!')
         elif IsWin(board, AI):
             clean()
             print(f'AI turn [{AI_Choice}]')
             Board(board, AI_Choice, HUMAN_Choice)
             print('YOU LOSE!')
         else:
             clean()
             Board(board, AI_Choice, HUMAN_Choice)
             print('DRAW!')
         
     # If you want to play again
     
        
  
        
        
if __name__ == '__main__':
    main()        
        
        
        
        
        
        
        
        
        
        
        
        