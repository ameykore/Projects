import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import constants as CONSTANT
from pymavlink import mavutil

class Util:
    
    @staticmethod
    def arm(vehicle):
        vehicle.armed = True
        arming_waiting=10
        while (not vehicle.armed) and (arming_waiting>0):
            arming_check_count=5
            print('arming_waiting: %s' % arming_waiting)
            while ((not vehicle.armed) and arming_check_count>0):
                print(" Waiting for arming...")
                time.sleep(1)
                arming_check_count=arming_check_count - 1
                print('arming_check_count: %s' % arming_check_count)
            arming_waiting=arming_waiting - 1
            vehicle.armed = True
            time.sleep(1)

    @staticmethod
    def takeoff(altitude,vehicle):
        takeoff_count=10
        takeoff_check_count=5
        takeoff_altitude_check=1.0
        print("Taking off!")
        #vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

        while (takeoff_count>0) and (vehicle.location.global_relative_frame.alt <= takeoff_altitude_check * 0.95):
            vehicle.simple_takeoff(altitude)
            takeoff_check_count=5
            print('takeoff_count: %s' % takeoff_count)
            takeoff_count = takeoff_count - 1
            while takeoff_check_count>0:
                takeoff_check_count=takeoff_check_count - 1
                time.sleep(1)
                #print('takeoff_check_count: %s' % takeoff_check_count)
                #print('altitude: %s' % vehicle.location.global_relative_frame.alt)
                if vehicle.location.global_relative_frame.alt >= takeoff_altitude_check * 0.95:
                    print('Takeoff successfully')
                    break
            while True:
                #print(" Altitude: ", vehicle.location.global_relative_frame.alt)
                # Break and return from function just below target altitude.
                if vehicle.location.global_relative_frame.alt >= altitude * 0.95:
                    print("Reached target altitude")
                    break

    @staticmethod
    def send_body_ned_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration=0):
        msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,       # time_boot_ms (not used)
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_FRAME_BODY_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
            0b0000111111000111, # type_mask
            0, 0, 0, # x, y, z positions (not used)
            velocity_x, velocity_y, velocity_z, # m/s
            0, 0, 0, # x, y, z acceleration
            0, 0)
        for x in range(0,duration):
            vehicle.send_mavlink(msg)
            time.sleep(1)
            
    @staticmethod
    def move_forward(vehicle):
        velocity_x = CONSTANT.SPEED_UAV_FORWARD_BACKWARD_MOVEMENT
        velocity_y = 0      #velocity in forward direction
        velocity_z = 0      
        duration = CONSTANT.DURATION_UAV_FORWARD_BACKWARD_MOVEMENT       #duration for forward movement
    
        Util.send_body_ned_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration)
        print("moving forward")

    @staticmethod
    def move_backward(vehicle):
        velocity_x = -(CONSTANT.SPEED_UAV_FORWARD_BACKWARD_MOVEMENT)
        velocity_y = 0
        velocity_z = 0      
        duration = CONSTANT.DURATION_UAV_FORWARD_BACKWARD_MOVEMENT       #duration for forward movement
    
        Util.send_body_ned_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration)
        print("moving backward")
    @staticmethod
    def move_right(vehicle):
        velocity_x = 0
        velocity_y = CONSTANT.SPEED_UAV_FORWARD_BACKWARD_MOVEMENT      #velocity in right direction
        velocity_z = 0      
        duration = CONSTANT.DURATION_UAV_FORWARD_BACKWARD_MOVEMENT       #duration for right movement
    
        Util.send_body_ned_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration)
        print("moving right")

    @staticmethod
    def move_left(vehicle):
        velocity_x = 0
        velocity_y = -(CONSTANT.SPEED_UAV_FORWARD_BACKWARD_MOVEMENT)      #velocity in left direction
        velocity_z = 0      
        duration = CONSTANT.DURATION_UAV_FORWARD_BACKWARD_MOVEMENT       #duration for left movement
    
        Util.send_body_ned_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration)
        print("moving left")

    @staticmethod
    def stop_vehicle(vehicle):
        velocity_x = 0
        velocity_y = 0      
        velocity_z = 0      
        duration = 0
               
        print("Stopping vehicle")
        Util.send_body_ned_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration)
        
    @staticmethod
    def set_mode(vehicle,mode):
        while not vehicle.mode.name==mode:
            time.sleep(1)
            print('waiting for vehicle mode to be {0}' .format(mode))
            vehicle.mode = VehicleMode(mode)
    
    @staticmethod        
    def get_battery_status(vehicle):
        battery_status = {}
        battery_status['voltage'] = vehicle.battery.voltage
        battery_status['current'] = vehicle.battery.current
        battery_status['level'] = vehicle.battery.level
        return battery_status
    
    @staticmethod
    def get_vehicle_global_location(vehicle):
        vehicle_current_position = {}
        vehicle_current_position['latitude'] = vehicle.location.global_frame.lat
        vehicle_current_position['longitude'] = vehicle.location.global_frame.lon
        vehicle_current_position['relative_altitude'] = vehicle.location.global_frame.alt
        vehicle_current_position['global_altitude'] = vehicle.location.global_frame.alt
        return vehicle_current_position