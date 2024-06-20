#!/usr/bin/env python

from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative,LocationGlobal
import time
import rospy
from std_msgs.msg import String
from beginner_tutorials.msg import heartbit
	
#connect to drone 
connection_string = "127.0.0.1:14553"
print('test')
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
time.sleep(5)
	
	while not rospy.is_shutdown():
		pub = rospy.Publisher('heartbit', heartbit, queue_size=10)
		#rospy.init_node('heartbit_talker')
		rate = rospy.Rate(10) # 10hz
		message = heartbit()

		message.lat = vehicle.location.global_relative_frame.lat
		message.lon = vehicle.location.global_relative_frame.lon
		message.battery = vehicle.battery.voltage
		max_fly_distance = 0
		print("sending heartbeat...")
		message.drone_id = DRONE_ID
		message.gps_count = str(gps_count).split(":")[1].split(",")[1].split("=")[1]
		message.max_fly_distance = max_fly_distance
		pub.publish(message)
		rate.sleep()