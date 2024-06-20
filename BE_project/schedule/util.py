#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sin, cos, sqrt, atan2, radians
import logging
import logging.config
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import constant

class Util:
    
    @staticmethod
    def getDistanceInMeters(lat1,long1,lat2,long2):
        # approximate radius of earth in km
        radius_of_earth = 6373.0
               
        lat1 = radians(lat1)
        long1 = radians(long1)
        lat2 = radians(lat2)
        long2 = radians(long2)

        a = sin(distance_between_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(distance_between_long / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
        distance = R * c * 1000
        return distance

    @staticmethod
    def arm_and_takeoff(aTargetAltitude,vehicle):
        """
        Arms vehicle and fly to aTargetAltitude.
        """
        #import logging,logging.config,time
        #from dronekit import VehicleMode
        logging.config.fileConfig(fname='log_gather.conf', disable_existing_loggers=False)
        logger = logging.getLogger('util')
        #print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        while not vehicle.is_armable:
            logger.info(" Waiting for vehicle to initialise...")
            time.sleep(1)

        logger.info("Arming motors and mode is GUIDED")
        # Copter should arm in GUIDED mode
        vehicle.mode = VehicleMode(constant.DEFAULT_MODE)
        vehicle.armed = True

        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:
            logger.info(" Waiting for arming...")
            time.sleep(1)

        logger.info("Taking off!")
        vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto
        #  (otherwise the command after Vehicle.simple_takeoff will execute
        #   immediately).
        while True:
            logger.info(" Altitude: {0}" .format(vehicle.location.global_relative_frame.alt))
        
            if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                logger.info("Reached target altitude")
                break
            time.sleep(1)


