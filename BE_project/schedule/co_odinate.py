from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from math import *
import signal
import sys

TIMEOUT = 5 # number of seconds your want for timeout


#constant
battery = 0  
battery1 = 0
altitude = 10
distance = None

# Connect to the Vehicle
connection_string = "127.0.0.1:14551"
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

#taking home coordinates
lat_home = vehicle.location.global_relative_frame.lat
lon_home = vehicle.location.global_relative_frame.lon

def arm_and_takeoff(aTargetAltitude):
    global battery 
    global battery1
    global distance

    #Arms vehicle and fly to aTargetAltitude.
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    #####file input######
    print("saving to file(before arming)")
    battery = vehicle.battery.voltage
    f = open('data_saved.txt','w')
    f.write ('battery_takeoff = ' + repr(battery) + '\n')
    f.close()
   

    #####arming mototrs#####import sys
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    ######If not armed########
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
     
    
    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
 

#signal intturupt function
def interrupted(signum, frame):
#"called when read times out"
    global battery 
    global battery1
    global distance
    global altitude

    print('interrupted!')
    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")

    # Close vehicle object before exiting script
    print("Close vehicle object")

    #input to file
    print("saving to file(after landing)")
    battery1 = vehicle.battery.voltage
    f = open('data_saved.txt','a')
    f.write ('battery_land = ' + repr(battery1) +'\n')

    
    
    #battery difference before take off and after takeoff
    battery_diff = round((battery - battery1),5)
    f.write ('battery_diff = ' + repr(battery_diff) +'\n')
    
    #battery consume parameter
    battery_const = round((battery_diff/(altitude + distance)),5)
    f.write ('battery_const = ' + repr(battery_const) +'\n')

    f.close()
    #time.sleep(5)
    vehicle.close()
    exit()
    
#use to close script after no response    
signal.signal(signal.SIGALRM,interrupted)

def check():
    try:
            distance  = float(raw_input())
            return distance
    except:
            # timeout
            return None


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



vehicle.airspeed = 5

while True:
            global altitude
            global distance

            print(distance)
            lat1_degree = vehicle.location.global_relative_frame.lat
            lon1_degree = vehicle.location.global_relative_frame.lon
            print(lat1_degree,lon1_degree)

            vehicle.mode = VehicleMode("GUIDED")
            degree_offset = vehicle.heading
            print("offset is:",degree_offset)

    
            #--time out loop
            print("Entre the distance d in metres: ")
            # set alarm
            signal.alarm(TIMEOUT)
            distance = check()
            # disable the alarm after success
            if distance == None:
                break
            signal.alarm(0)
            
            print("Entre the angle in degree:")
            # set alarm
            signal.alarm(TIMEOUT)
            angle_given = check()
            # disable the alarm after success
            if angle_given == None:
                break
            signal.alarm(0)
            
            theta =  angle_given + degree_offset

            lat_destination, lon_destination = lat_lon_op(distance,theta)
            #print(lat2_degree, lon2_degree)

            arm_and_takeoff(altitude)
            #print("Going towards first point for 30 seconds ...")
            point1 = LocationGlobalRelative(lat_destination, lon_destination,altitude)
            vehicle.simple_goto(point1)
                time.sleep(distance/2)

