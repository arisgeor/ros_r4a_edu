#!/usr/bin/env python

from __future__ import print_function
import random
import rospy
import random
import os
import sys
from complex_communication.srv import *



def handle_player1(req): #player_choice and space_check
	
    position = 0

    while position not in [1,2,3,4,5,6,7,8,9] or not (req.brd[position]==" "):
        position = int(raw_input('Choose number input 1-9'))
    return position


def player1():
	rospy.init_node('player1_server')
	s=rospy.Service('player1', TicTacToe, handle_player1)
	rospy.spin()#just waits for the node to shutdown

if __name__ == "__main__":
	player1()
	 