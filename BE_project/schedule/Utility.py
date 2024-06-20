from math import sin, cos, sqrt, atan2, radians
import uav_curves as UAV_ARENA
class Util:
    @staticmethod
    def get_distance(lat1,long1,lat2,long2):
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
    def is_point_in_curve(x, y, arena):
        """
        x, y -- x and y coordinates of point
        arena -- a list of tuples [(x, y), (x, y), ...]
        """
        num = len(arena)
        i = 0
        j = num - 1
        is_point_inside_curve = False
        for i in range(num):
            if ((arena[i][1] > y) != (arena[j][1] > y)) and \
                    (x < arena[i][0] + (arena[j][0] - arena[i][0]) * (y - arena[i][1]) /
                                      (arena[j][1] - arena[i][1])):
                is_point_inside_curve = not is_point_inside_curve
            j = i
        return is_point_inside_curve

    @staticmethod
    def get_uav_ids(x,y):
        uav_ids=[];
        if(Util.is_point_in_curve(x, y, UAV_ARENA.curve1)):
            #print("UAV1 arena")
            uav_ids.append(1)
        if(Util.is_point_in_curve(x, y, UAV_ARENA.curve2)):
            #print("UAV2 arena")
            uav_ids.append(2)   
        if(Util.is_point_in_curve(x, y, UAV_ARENA.curve3)):
            #print("UAV3 arena")
            uav_ids.append(3);
        return uav_ids