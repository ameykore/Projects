def endurance(battery_takeoff, battery_land, mission_distance, mission_altitude):
#endurance Calculation for next flight

	#battery constant calculation
		total_distance = mission_altitude + mission_distance
		bat_consumed = battery_takeoff - battery_land
		bat_constant = round((bat_consumed/total_distance),5)
		print(bat_constant)
		
	#save battery constant to file
		file = open("/home/dhananjay/catkin_ws/src/beginner_tutorials/schedule/src/data4.txt","w")
		file.write ('bat_constant = ' + repr(bat_constant) + '\n')
		file.close() 	
		print("Saved to file")
	
