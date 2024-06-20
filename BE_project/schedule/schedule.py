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

#defining data fields 
distance = None
dict_obj = None
drone_list_data = []
drone_id_list = []
distance_list = []
non_busy_drone = []
heights = [10,15,20,25]
rem_distance_list = []
 
#importing attributes from schedule.msg
message = schedule()
rospy.init_node('scheduler_talker', anonymous=True)


#publish packet
def talker():
	#define publishing node
	print("starting publishing node")
	pub = rospy.Publisher('scheduler', schedule, queue_size=10)
	rate = rospy.Rate(10) # 10hz

	#publishe msg 
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

	dist_max = drone_list_data[x].get('max_fly_distance')
	rem_distance = dist_max - 2*distance_list[x]
	rem_distance_list.append(rem_distance)
	print(rem_distance)
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

#listening Heartbit of drones 
def callback_heartbit(data):
	global dict_obj
	if(not data.drone_id in drone_id_list):
		#Creating dictionary 
		dict_obj = {"ID":data.drone_id,"lat":data.lat,"lon":data.lon,"battery":data.battery,"gps_count":data.gps_count,"max_fly_distance":data.max_fly_distance,"busy_flag":data.busy_flag}
		drone_list_data.append(dict_obj)
		print("INTURUPTED!!!")
		print("DroneID:",data.drone_id)
		print("Heartbit Arrived")
		print("Enter the destination coodinates:")
		drone_id_list.append(data.drone_id)

	
#listen to node
def listener():
	#store value in t_end to publish for 10 seconds
	#t_end = time.time() + 60/6
	while dict_obj == None:
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
	for i in range(0,(number_of_drones_to_send)):
		print("battery:",drone_list_data[max_index[i]]["battery"])		
		if drone_list_data[max_index[i]]["backup_distance"] <= 0 or drone_list_data[max_index[i]]["battery"] < 10.5:	
			d = drone_list_data[uav_ids[i]].get('ID')
			print("Drone:",d,"Will not go due to insuficient battery...")
		else:	
			DroneID.append(drone_list_data[max_index[i]].get('ID'))
	print("Drone_ID:"+ repr(DroneID) + ' Should go...')
	return DroneID 		

def availble_drones(uav_ids_in_region):
	uav_ids_in_region_set = set(uav_ids_in_region)
	for i in range (0,len(drone_id_list)):
		if drone_list_data[i]["busy_flag"] == False:
			non_busy_drone.append(drone_list_data[i]['ID'])
		non_busy_drone_set = set(non_busy_drone)
	availble_drones_set = non_busy_drone_set & uav_ids_in_region_set
	availble_drones = list(availble_drones_set)
	print(availble_drones)
	return(availble_drones)

if __name__ == '__main__':
	while True:
		global heartbit_data
		veriable_height = []	

		#listen to node
		listener()
		#desitnation lat lon 
		get_lat_lon()
		print(drone_list_data)
		#destination lat lon comes under which drone area
		uav_ids_in_region = Util.get_uav_ids(lat_destination,lon_destination)
		uav_ids = availble_drones(uav_ids_in_region)

		print("uav id:",uav_ids)
		#check if destination lat lon is in any UAV area or not
		if not len(uav_ids) == 0:
			#distnace
			for x in range(0 ,len(drone_id_list)):
				distance_m = distance_calculator(lat_destination,lon_destination,drone_list_data[x].get('lat'),drone_list_data[x].get('lon'))
				drone_list_data[x]['target_distance'] = distance_m
				remaining_distance = cal_distance_after_one_flight(x)
				drone_list_data[x]['backup_distance'] = remaining_distance
			#print(drone_list_data)
			#Sorting drone data according to backup distance
			drone_list_data = sorted(drone_list_data, key=itemgetter('backup_distance'),reverse = True)
			print(drone_list_data)	

			number_of_drones_to_send = input("Enter the drone to be sent out off  {} : ".format(len(uav_ids)))
			#check if number of drone in uav_ids is same as user wish to send the drones
			while not number_of_drones_to_send  <= len(uav_ids) or number_of_drones_to_send == 0:
				number_of_drones_to_send = input("Enter only drones below or equal to {} else Enter 0 if you wish to exit:".format(len(uav_ids)))
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

		check = 'd'
		while not check == 'y' or check =='n':
			check = raw_input("Do you want to continue?[y/n]:")
			if check == 'n':
				print("closing...")
				exit()
			elif check == 'y':
				dict_obj = None
				drone_id_list = []
				drone_list_data = []
				non_busy_drone = []
				message.Drone_ID = []
				message.Drone_alt = []
				continue
		