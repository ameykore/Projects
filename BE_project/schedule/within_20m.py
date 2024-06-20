#!/usr/bin/env python

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative,LocationGlobal
import rospy
import roslib
from std_msgs.msg import String
from swarm.msg import schedule
from swarm.msg import heartbit
from math import *
from Utility import Util
from operator import itemgetter
import constants as CONSTANT
import math

#defining data fields 
distance = None
drone_list_data = []
drone_id_list = []
distance_list = []
heights = [10,15,20,25]
rem_distance_list = []
uav_ids = []

 
 #importing attributes from schedule.msg
message = schedule()
rospy.init_node('scheduler_talker', anonymous=True)


#publish packet
def talker():
	#define publishing node
	print("starting publishing node")
	pub = rospy.Publisher('scheduler', schedule, queue_size=10)
	rate = rospy.Rate(10) # 10hz

	#publish msg 
	print("Publishing...")

	message.lat = float(lat_destination)
	message.lon = float(lon_destination)
	message.distance = round(float(distance),2)

	#store value in t_end to publish for 30 seconds
	t_end = time.time() + 60 / 2
	while time.time() < t_end:
		pub.publish(message)
		rate.sleep()

	print("done publishing")

#Total distance that will remain after mission completion
def cal_distance_after_one_flight(x):

	dist_max = drone_list_data[x].get('max_fly_distance_in_meters')
	rem_distance = dist_max - 2*distance_list[x]
	rem_distance_list.append(rem_distance)
	return  rem_distance


#calculating distance between home and destination
def distance_calculator(lat_destination,lon_destination,lat_home,lon_home):
	global distance
	R = CONSTANT.RADIUS_OF_EARTH  

	lat_desti = radians(lat_destination)
	lon_desti = radians(lon_destination)
	lat_home = radians(lat_home)
	lon_home = radians(lon_home)
	delta = (lat_desti - lat_home)
	lamda = (lon_desti - lon_home)
	a = sin(delta / 2)**2 + cos(lat_home) * cos(lat_desti) * sin(lamda / 2)**2
	c = 2*atan2(sqrt(a), sqrt(1-a))
	distance = R * c

	print("DroneID:",drone_id_list[x],"distance:",distance)
	distance_list.append(distance)
	return distance


#vehicle.airspeed = 5
def get_lat_lon():
	global lat_destination 
	global lon_destination
	
	lat_lon = input("Enter the destination coodinates:")  
	lat_destination = lat_lon[0]
	lon_destination = lat_lon[1]

#mission falls uder which UAV	
def in_area_of(lat_destination,lon_destination,lat_home,lon_home,Drone_ID):
	global d 
	R = 6373.0
	print(lat_destination,lon_destination,lat_home,lon_home)
	lat_desti = math.radians(lat_destination)
	lon_desti = math.radians(lon_destination)
	lat_home = math.radians(lat_home)
	lon_home = math.radians(lat_home)
	delta = (lat_desti - lat_home)
	lamda = (lon_desti - lon_home)
	a = sin(delta / 2)**2 + cos(lat_home) * cos(lat_desti) * sin(lamda / 2)**2
	c = 2*atan2(sqrt(a), sqrt(1-a))
	d = R * c
	print("distance from",format(Drone_ID),"is",format(d))
	if (d > 20):
		print("Not in area of Drone_ID : ",format(Drone_ID))
		print(format(Drone_ID),"is not available")
	else:
		print("In area of Drone_ID : ",format(Drone_ID))
			#count+=1
		uav_ids.append(Drone_ID)
		return Drone_ID
		#print("In total",format(count),"UAV are in the area")	
	

#listening Heartbit of drones 
def callback_heartbit(data):
	global dict_obj
	if(not data.drone_id in drone_id_list):
		#Creating dictionary 
		dict_obj = {"ID":data.drone_id,"lat":data.lat,"lon":data.lon,"battery_in_V":data.battery,"gps_count":data.gps_count,"max_fly_distance_in_meters":data.max_fly_distance}
		drone_list_data.append(dict_obj)
		print("DroneID:",data.drone_id)
		drone_id_list.append(data.drone_id)

	
#listen to node
def listener():
	#store value in t_end to publish for 10 seconds
	t_end = time.time() + 60/6
	while time.time() < t_end:
		rospy.Subscriber('heartbit', heartbit, callback_heartbit)
	time.sleep(1)

	print("done listening...")


#Getting index of max backup_distance
def get_max_backup_index(uav_ids, number_of_drones_to_send):
	index = []
	max = -5
	for i in range(0, len(drone_id_list)):
		if drone_list_data[i]["ID"] in uav_ids:
			index.append(i)		
	return index

#Returning drone_id
def drone_decision(uav_ids,number_of_drones_to_send):
	max_index = []
	DroneID = []
	#getting index of availble drone
	max_index = get_max_backup_index(uav_ids,number_of_drones_to_send)
	#finding drone_id from max_index
	print("max_index",max_index)
	for i in range(0,(number_of_drones_to_send)):
		print(i)			
		if drone_list_data[max_index[i]]['backup_distance'] <= 0:	
			d = drone_list_data[uav_ids[i]].get('ID')
			print("Drone:",d,"Will not go due to insuficient battery...")
		else:	
			DroneID.append(drone_list_data[max_index[i]].get('ID'))
	print("Drone_ID:"+ repr(DroneID) + ' Should go...')
	return DroneID 		

if __name__ == '__main__':
	global heartbit_data
	veriable_height = []

	#listen to node
	listener()
	#desitnation lat lon 
	get_lat_lon() 
	#destination lat lon comes under which drone 

	#uav_ids = Util.get_uav_ids(lat_destination,lon_destination)
	for x in range(0,len(drone_id_list)):
		ID = in_area_of(lat_destination,lon_destination,drone_list_data[x].get('lat'),drone_list_data[x].get('lon'),drone_list_data[x].get('ID'))
		uav_ids.append(ID)
		print("uav id:",uav_ids)
	#check if destination lat lon is in any UAV area or not
	if not len(uav_ids) == 0:
		#distance
		for x in range(0 ,len(drone_id_list)):
			distance_m = distance_calculator(lat_destination,lon_destination,drone_list_data[x].get('lat'),drone_list_data[x].get('lon'))
			drone_list_data[x]['target_distance'] = distance_m
			remaining_distance = cal_distance_after_one_flight(x)
			drone_list_data[x]['backup_distance'] = remaining_distance
		print(drone_list_data)
		#Sorting drone data according to backup distance
		drone_list_data = sorted(drone_list_data, key=itemgetter('backup_distance'),reverse = True)
		print(drone_list_data)

		number_of_drones_to_send = input("Enter the drone to be sent out off  {} : ".format(len(uav_ids)))
		#check if number of drone in uav_ids is same as user wish to send the drones
		while not number_of_drones_to_send  <= len(uav_ids) or number_of_drones_to_send == 0:
			number_of_drones_to_send = input("Enter only drones below or equal to : {} : else Enter 0 if you wish to exit:".format(len(uav_ids)))
			if number_of_drones_to_send == 0:
				exit()


		#IDs of drones than can go
		count = drone_decision(uav_ids,number_of_drones_to_send)
		message.Drone_ID = count + message.Drone_ID
		
		#publish height
		for i in range(len(uav_ids)):
			#message.Drone_height = heights[i] + message.Drone_height
			veriable_height.append(heights[i])
		message.Drone_alt = veriable_height + message.Drone_alt
		
		talker()	
	else:
		print("Point is not in uav region...")
	time.sleep(5)
	print("closing...")
