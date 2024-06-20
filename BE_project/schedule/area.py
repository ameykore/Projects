import math
from operator import itemgetter
#from beginner_tutorials.msg import heartbit

curve = []
drone_home_lat_lon = [{'lat':18.578260,'lon':73.879650},{'lat':18.578494,'lon':73.879610},{'lat':18.578362,'lon':73.879622},{'lat':18.578096,'lon':73.879657}]

'''
def listener():
    #store value in t_end to publish for 10 seconds
    t_end = time.time() + 60/6
    while time.time() < t_end:
        rospy.Subscriber('heartbit', heartbit, callback_heartbit)
    time.sleep(1)
def callback_heartbit(data):
    global dict_obj
    #if(not data.drone_id in drone_id_list):
        #Creating dictionary 
    dict_obj = [data.lat,data.lon]
    drone_home_lat_lon.append(dict_obj)
        #print("DroneID:",data.drone_id)
        #drone_id_list.append(data.drone_id)

    print("done listening...")
    '''
#def get_curves(lat1,lon1):
R = 6378.1 #Radius of the Earth
brng = [0,0.7854,1.57,2.356,3.14,3.92,4.71,5.497] #Bearing is 90 degrees converted to radians.
d = 0.05 #Distance in km
#home_coordinates = [{18.578260,73.879650},'''{18.578494,73.879610},{18.578362,73.879622},{18.578096,73.879657}'''] 
for x in range(0 ,len(drone_home_lat_lon)): 
    print(len(drone_home_lat_lon))
    #dynamic name producer
    name = "curve{0}".format(x)
    for i in range(len(brng)):
        lat1 = math.radians(drone_home_lat_lon[x].get('lat')) #Current lat point converted to radians
        lon1 = math.radians(drone_home_lat_lon[x].get('lon')) #Current long point converted to radians
        lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
                math.cos(lat1)*math.sin(d/R)*math.cos(brng[i]))
        lon2 = lon1 + math.atan2(math.sin(brng[i])*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        cordinates = [lat2,lon2]
                #latlonarea = []
        dict_obj = {"curve{0}".format(x+1):cordinates}
        #name.appned(cordinates0)
        curve.append(dict_obj)
                #latlonarea.append(lat2)
                #latlonarea.append(lon2)d["string{0}".format(x)]="Hello"

print(curve)

#curve1 = {key: curve[key] for key in curve.keys()}
#curve1 = {key:val for key, val in curve.items() if key.endswith('1')}
#curve1 = {curve, key=itemgetter('1')}
#curve1 = dict((k, curve[k]) for k in ['1'] if k in curve) 

    
            #print(lat2)
            #print(lon2)
#if __name__ == '__main__':
 #   listener()

  #  for x in range(0 ,len(drone_home_lat_lon)):
  #      get_curves(drone_home_lat_lon[x].get('lat'),drone_home_lat_lon[x].get('lon'))