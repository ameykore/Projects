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
connection_string = "127.0.0.1:14546"
print('test')
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
time.sleep(5)

#importing attributes from path_planning.msg
message_path = path_planning()
message_schedule = schedule()
rospy.init_node('path_planning_drone2')

#CONSTANTS
destination_coordinate = None
path_obj = None
path_list_data = []
drone_id_list = []
schedule_id_list = []

def callback_schedule(data):
	global destination_coordinate
	#print("in callback_schedule...")
	destination_coordinate = (data.lat, data.lon)
	schedule_id_list = data.Drone_ID
	
#listen to node
def listening_to_schedule():
	global destination_coordinate
	print("listening...")
	while destination_coordinate == None:
		#store value in t_end to publish for 30 seconds
		t_end = time.time() + 60 / 4
		while time.time() < t_end:
			rospy.Subscriber("scheduler", schedule, callback_schedule)
	time.sleep(1)
	print("done listening...")

def callback_path(data):
	global path_obj
	global drone_id_list
	if data.drone_id in drone_id_list:
		path_obj = {"ID":data.drone_id,"lat_home":data.lat_home,"lon_home":data.lon_home,"lat_predict":data.lat_predict,"lon_predict":data.lon_predict,"moving_flag":data.moving_flag}
		path_list_data.append(path_obj)
		drone_id_list.append(data.drone_id)
		#print("coordinates arrived...")

def listening_to_predict_coordinate():
	global path_obj
	print("in listening_to_predict_coordinate")
	while path_obj == None:
		rospy.Subscriber('path_planning', path_planning, callback_path)
	time.sleep(1)
	print("done listening...")


if __name__ == '__main__':
	global schedule_id_list
	listening_to_schedule()
	#print(path_msg)
	print("message received....")
	if CONSTANT.DRONE_ID_2 in schedule_id_list:
		listening_to_predict_coordinate()
		print(path_list_data)
		print(destination_coordinate)
