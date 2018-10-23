#!/usr/bin/env python

from __future__ import print_function
import random
import rospy
import random
import os
import sys
from complex_communication.srv import *



def handle_player2(req): #player_choice and space_check
 
	position = 0

	while position not in [1,2,3,4,5,6,7,8,9] or not (req.brd[position]==" "):
		position = int(raw_input('Choose number input 1-9'))
	return position


def player2():
	rospy.init_node('player2_server')
	s=rospy.Service('player2', TicTacToe, handle_player2)
	rospy.spin()#just waits for the node to shutdown

if __name__ == "__main__":
	player2()
	 