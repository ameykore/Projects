#!/usr/bin/env python

import rospy 
import time
import roslib
from math import *
import constants as CONSTANT
from std_msgs.msg import String
from swarm.msg import path_planning
from dronekit import connect, VehicleMode, LocationGlobalRelative,LocationGlobal

#connect to drone 
connection_string = "127.0.0.1:14547"
print('test')
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
time.sleep(5)

#importing attributes from path_planning.msg
message = path_planning()
rospy.init_node('drone2_coordinate_predict')

#CONSTANTS
message.drone_id = CONSTANT.DRONE_ID_2
predict_distance = 5 #meters


def lat_lon_op(distance, theta):
	lat1_degree = vehicle.location.global_relative_frame.lat
	lon1_degree = vehicle.location.global_relative_frame.lon
	#print(lat1_degree)
	#print(lon1_degree)
	lat1_radian = radians(lat1_degree)
	lon1_radian = radians(lon1_degree)
	theta = radians(theta)

	#lon2 calculation
	north_displacement = distance*(sin(theta)/111111)
	lon_destination = lon1_degree + north_displacement

	#lat2 claculation
	east_displacement = distance*((cos(theta)/cos(lat1_radian))/111111)
	lat_destination = lat1_degree + east_displacement

	#print(lat_destination,lon_destination)
	return lat_destination, lon_destination;


def lat_lon_predict():
	message.lat_predict, message.lon_predict = lat_lon_op(predict_distance, vehicle.heading)


#publish packet
def talker():
	#define publishing node
	#print("starting publishing node")
	message.lat_home = vehicle.location.global_relative_frame.lat
	message.lon_home = vehicle.location.global_relative_frame.lon
	message.moving_flag = 1
	pub = rospy.Publisher('path_planning', path_planning, queue_size=10)	
	rate = rospy.Rate(10) # 10hz
	#publishe msg 
	#print("Publishing...")

	#store value in t_end to publish for 30 seconds
	t_end = time.time() + 60 / 60
	while time.time() < t_end:
		pub.publish(message)
		rate.sleep()

	#print("done publishing")

while True:
	lat_lon_predict()

	talker()