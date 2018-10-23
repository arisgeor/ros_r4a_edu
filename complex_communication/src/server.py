#!/usr/bin/env python
from __future__ import print_function
from complex_communication.srv import *
import rospy

from IPython.display import clear_output
import random
import string
import rospy

    
#------------------------- Server functions -----------------------


def player1_client(board):
    rospy.wait_for_service('player1')
    try:
        player1=rospy.ServiceProxy('player1', TicTacToe)
        resp1=player1(board)        
        return resp1.move
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s" % (e,))

def player2_client(board):
    rospy.wait_for_service('player2')
    try:
        player2=rospy.ServiceProxy('player2', TicTacToe)
        resp2=player2(board)
        return resp2.move
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s" % (e,))


#-------------------------------------------------------------------
#---------------------------- Board Class-----------------------
#-------------------------------------------------------------------

class Board():

    def __init__(self):
        self.board = [' '] * 10 #at initialization i create a new self.board (list)


    def display(self):

        clear_output()
        
        print(
            '   ' + self.board[7] + '|' + self.board[8] + '|' + self.board[9] + '\n' +
            '  -------  ' + '\n' +
            '   ' + self.board[4] + '|' + self.board[5] + '|' + self.board[6] + '\n' +
            '  -------  ' + '\n' + 
            '   ' + self.board[1] + '|' + self.board[2] + '|' + self.board[3]
            )

    def space_check(self, position):

        #checks if the specified position is available

        return self.board[position] == ' '

    def player_choice(self): #ask a player for the next move. If it 's free then return it

        move = 0
    
        while move not in [1,2,3,4,5,6,7,8,9] or not self.space_check(move):
            move = int(raw_input('Choose your next move: (1-9) '))
        
        return move

    def place_marker(self, marker, position): #function that takes the marker and desired position and assigns it to the self.board

        self.board[position] = marker

    def win_check(self, mark):
    
        #checks all posible scenarios of victory
        #rows columns and diagonals

        return (
        (self.board[7] == mark and self.board[8] == mark and self.board[9] == mark) or # across the top
        (self.board[4] == mark and self.board[5] == mark and self.board[6] == mark) or # across the middle
        (self.board[1] == mark and self.board[2] == mark and self.board[3] == mark) or # across the bottom
        (self.board[7] == mark and self.board[4] == mark and self.board[1] == mark) or # down the middle
        (self.board[8] == mark and self.board[5] == mark and self.board[2] == mark) or # down the middle
        (self.board[9] == mark and self.board[6] == mark and self.board[3] == mark) or # down the right side
        (self.board[7] == mark and self.board[5] == mark and self.board[3] == mark) or # diagonal
        (self.board[9] == mark and self.board[5] == mark and self.board[1] == mark) # diagonal
        ) 

    def full_board_check(self):

        #checks if the board is full and returns a boolean

        for i in range(1,10):
            if self.space_check(i):
                return False
        return True

    def choose_first(self):

        #Randomly decides who should go first

        if random.randint(0, 1) == 0:
            return 'Player 2'
        else:
            return 'Player 1'
   


#-----------------------------------------------------------------------------------
#--------------------------------The actual game------------------------------- 
#-----------------------------------------------------------------------------------


if __name__ == "__main__":

    # Reset the board
    theBoard = Board()
    player1_marker, player2_marker = ("X","O")
    print("Welcome to Tic Tac Toe!")
    turn = theBoard.choose_first()
    print(turn + ' will go first.')
    game_on = True
    
    while game_on:
        if turn == 'Player 1':

            theBoard.display()
            position=player1_client(theBoard.board)
            theBoard.place_marker(player1_marker, position)
            
            if theBoard.win_check(player1_marker):
                theBoard.display()
                print('Congratulations! You have won the game!')
                game_on = False
            else:
                if theBoard.full_board_check():
                    theBoard.display()
                    print('The game is a draw!')
                    game_on = False
                else:
                    turn = 'Player 2'

        else: 

            theBoard.display()
            position=player2_client(theBoard.board)
            theBoard.place_marker(player2_marker, position)
            
            if theBoard.win_check(player2_marker):
                theBoard.display()
                print('Congratulations! You have won the game!')
                game_on = False
            else:
                if theBoard.full_board_check():
                    theBoard.display()
                    print('The game is a draw!')
                    game_on = False
                else:
                    turn = 'Player 1'
    else:
        rospy.signal_shutdown('Quit')
