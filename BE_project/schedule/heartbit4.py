#!/usr/bin/env python

from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative,LocationGlobal
import time
import rospy
from std_msgs.msg import String
from beginner_tutorials.msg import heartbit
import constants as CONSTANT


#connect to drone 
connection_string = "127.0.0.1:14561"
print('test')
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
time.sleep(5)

message = heartbit()

pub = rospy.Publisher('heartbit', heartbit, queue_size=10)
rospy.init_node('heartbit4_talker')
rate = rospy.Rate(10) # 10hz

def heartbit():
	battery = vehicle.battery.voltage
	file = open("/home/dhananjay/catkin_ws/src/beginner_tutorials/schedule/src/data4.txt",'r')
	l = file.readline()
	k = float(l.split("=")[1])
	if battery > 10.5:
		message.max_fly_distance = ((battery - 10.5)/k)- (CONSTANT.DEFAULT_ALTITUDE)*2
	else:
		message.max_fly_distance = 0	
	 # 10 is the altitude*2  



while not rospy.is_shutdown():
	max_fly_distance = heartbit()


	message.lat = vehicle.location.global_relative_frame.lat
	message.lon = vehicle.location.global_relative_frame.lon
	message.battery = vehicle.battery.voltage
	gps_count = str(vehicle.gps_0)

	print("sending heartbeat OF ", CONSTANT.DRONE_ID_4)
	message.drone_id = CONSTANT.DRONE_ID_4
	message.gps_count = str(gps_count).split(":")[1].split(",")[1].split("=")[1]
	#message.max_fly_distance = max_fly_distance
	pub.publish(message)
	rate.sleep()