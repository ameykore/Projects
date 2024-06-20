#!/usr/bin/env python

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative,LocationGlobal
import rospy
from std_msgs.msg import String
from swarm.msg import schedule
from math import *
from UAV_Utility import Util
import constants as CONSTANT
import endurance2 as ENDURANCE

#connect to drone 
connection_string = "127.0.0.1:14554"
print('test')
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
time.sleep(5)

#message field  & constants
message = schedule()
rospy.init_node('drone2')
message.Drone_ID = CONSTANT.DRONE_ID_2
R = CONSTANT.RADIUS_OF_EARTH
schedule_messsage = None #To check data from scheduler

#taking home coordinates
lat_home = vehicle.location.global_relative_frame.lat
lon_home = vehicle.location.global_relative_frame.lon


#publish packet
def talker():
	#define publishing node

	print("Starting publishing node")
	pub = rospy.Publisher('Drone_ID_2', schedule, queue_size=10)
	rate = rospy.Rate(10) # 10hz

	#msg fields
	message.battery = vehicle.battery.voltage

	#battery voltage 
	print("Publishing...")

	#store value in t_end to publish for 10 seconds
	t_end = time.time() + 60 / 6

	while time.time() < t_end:
		pub.publish(message)
		rate.sleep()

	print("done publishing")


def callback(data):
	global schedule_messsage
	schedule_messsage = data

#listen to node
def listener():
	print("listening for 15 sec...")
	#store value in t_end to publish for 15 seconds
	t_end = time.time() + 60 *0.25

	while time.time() < t_end:
		rospy.Subscriber("scheduler", schedule, callback)
	if schedule_messsage == None:
		print("waiting for scheduler")
		time.sleep(5)
	else:
		print("done listening...")


#assign variable height if multiple drones are selected
def get_height():
	d = schedule_messsage.Drone_ID.index(CONSTANT.DRONE_ID_2)
	return schedule_messsage.Drone_alt[d]

#main loop
if __name__ == '__main__':
	while True:
		while schedule_messsage == None:
			listener()		
		print(schedule_messsage)		
		if CONSTANT.DRONE_ID_2 in schedule_messsage.Drone_ID:
			Util.set_mode(vehicle,"GUIDED")
			vehicle.airspeed = CONSTANT.UAV_AIR_SPEED
			
			#get height
			height = get_height()
			
			Util.arm(vehicle)
			print("Armimg done...")		
			battery_takeoff = vehicle.battery.voltage		
			Util.takeoff(height,vehicle)	
	
			print("going towards point...")
			point = LocationGlobalRelative(schedule_messsage.lat, schedule_messsage.lon,height)
			vehicle.simple_goto(point)
			time.sleep(schedule_messsage.distance)		
			Util.set_mode(vehicle,"RTL")		
			while not vehicle.location.global_relative_frame.alt <= 0:
				continue		
			battery_land = vehicle.battery.voltage		
			#to calculate K
			ENDURANCE.endurance(battery_takeoff, battery_land, schedule_messsage.distance, height)
		else :
			print("Instructions are not for me... closing")
		time.sleep(5)
		schedule_messsage = None
