#!/usr/bin/env python

import rospy 
import time
import roslib
from math import *
import constants as CONSTANT
from swarm.msg import schedule
from std_msgs.msg import String
from swarm.msg import path_planning
from dronekit import connect, VehicleMode, LocationGlobalRelative,LocationGlobal

#connect to drone 
connection_string = "127.0.0.1:14548"
print('test')
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
time.sleep(5)

#importing attributes from path_planning.msg
message_path = path_planning()
message_schedule = schedule()
rospy.init_node('path_planning_drone1')

#CONSTANTS
path_msg = None

def callback_path(data):
	global path_msg
	path_msg = data
	
#listen to node
def listener():
	

if __name__ == '__main__':

	listener()
	print(path_msg)
	print(type(path_msg.Drone_ID))
