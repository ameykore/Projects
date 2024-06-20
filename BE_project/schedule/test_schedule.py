from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from math import *
import signal
import sys
#from endurance import *
#from schedule import *

TIMEOUT = 5

battery = 0  
battery1 = 0
altitude = 10
distance = None
lat_destination = None
lon_destination = None

lat2_degree = None
lon2_degree = None
connection_string = "127.0.0.1:14551"
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
'''
def lat_lon_op(distance,theta):
     lat1_radian = radians(lat1_degree)
     lon1_radian = radians(lon1_degree)
     theta = radians(theta)

     #lon2 calculation
     north_displacement = distance*(sin(theta)/111111)
     lon_destination = lon1_degree + north_displacement

     #lat2 claculation
     east_displacement = distance*((cos(theta)/cos(lat1_radian))/111111)
     lat_destination = lat1_degree + east_displacement
     print(lat_destination,lon_destination)
     return lat_destination, lon_destination;
def check():
    try:
            distance  = float(raw_input())
            return distance
    except:
            # timeout
            return None
'''

def distance_calculator(lat_destination,lon_destination):
	R = 6373000.0
	lat_home = 18.578579
	lon_home = 73.879910
	lat_destination = radians(lat_destination)
	lon_destination = radians(lon_destination)
	lat_home = radians(lat_home)
	lon_home = radians(lon_home)
	
	delta = (lat_destination - lat_home)
	lamda = (lon_destination - lon_home)

	a = sin(delta / 2)**2 + cos(lat_home) * cos(lat_destination) * sin(lamda / 2)**2
	#print(cos(lat_home), cos(lon_home))

	c = 2*atan2(sqrt(a), sqrt(1-a))
	distance = R * c

	print(distance)

vehicle.airspeed = 5
def get_param():
	
    global altitude
    global distance
    global theta
    global lat_destination
    global lon_destination
    #print(distance)
    #lat1_degree = vehicle.location.global_relative_frame.lat
    #lon1_degree = vehicle.location.global_relative_frame.lon
    #print(lat1_degree,lon1_degree)

    vehicle.mode = VehicleMode("GUIDED")
    #degree_offset = vehicle.heading
    #print("offset is:",degree_offset)

    
    #--time out loop
    lat_destination = input("Enter the destination lat:")
    # set alarm
    #signal.alarm(TIMEOUT)
    #lat_destination = check()
    #disable the alarm after success
    #if distance == None:
        #break
    #signal.alarm(0)
            
    lon_destination = input("Entre the destination lon:")
    # set alarm
    #signal.alarm(TIMEOUT)
   # lon_destination = check()
    # disable the alarm after success
    #if angle_given == None:
     #   break
    #signal.alarm(0)
    #theta =  angle_given + degree_offset
    #print(lat_destination,lon_destination)
    #lat_destination, lon_destination = lat_lon_op(distance,theta)
    #print(lat2_degree, lon2_degree)
if __name__ == '__main__':
	get_param()
	#distance = 10
	#theta = 0
	#lat_lon_op(distance,theta)
	#print(lat_destination,lon_destination)
	distance_calculator(lat_destination,lon_destination)
	#print ()


