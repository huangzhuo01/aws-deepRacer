import math
import mock_params

def angle_of_vector(vector):
    """ Calculate the angle of the vector in degrees relative to
    a normal 2d coordinate system.  This is useful for finding the
    angle between two waypoints.
    vector: [[x0,y0],[x1,y1]]
    """
    rad = math.atan2(vector[1][1] - vector[0][1], vector[1][0] - vector[0][0])
    return math.degrees(rad)



def calculate_heading_factor(params):
    """ Calculate the heading factor """
    # SUPRESS: This is too experimental while we haven't finished tracks yet
    closest_waypoints = params['closest_waypoints']
    waypoints = params['waypoints']
    heading = params['heading'] + (params['steering_angle'] / 2)
    # Calculate the immediate track angle
    wp1 = waypoints[closest_waypoints[0]]
    wp2 = waypoints[closest_waypoints[1]]
    ta1 = angle_of_vector([wp1,wp2])
    print("track angle 1: %i" % ta1)
    # h: Heading Factor: apply pressure as heading is different than track angle
    # Find closest angle, accounting for possibility of wrapping
    a = abs(ta1 - heading)
    b = abs(ta1 - (heading + 360))
    heading_delta = min(a,b)
    # hard fail if going backwards
    if heading_delta > 90:
        heading_factor = 1e-3
    elif heading_delta > 60:
        heading_factor = 0.3
    elif heading_delta > 45:
        heading_factor = 0.6
    elif heading_delta > 30:
        heading_factor = 0.8
    else:
        heading_factor = 1.0
    return min(heading_factor, 1.0)

def calculate_lane_factor(params):
    distance_ratio =  params['distance_from_center'] / (params['track_width']/2)
    return max(min(1.0 - distance_ratio, 1.0), 0.0)


def calculate_spped_factor(params):
    closest_waypoints = params['closest_waypoints']
    waypoints = params['waypoints']
    # Calculate the immediate track angle
    wp1 = waypoints[closest_waypoints[0]]
    wp2 = waypoints[closest_waypoints[1]]
    ta1 = angle_of_vector([wp1,wp2])
    print("track angle 1: %i" % ta1)
    straight = True
    for i in range(3):
        wp1 = waypoints[(closest_waypoints[1]+i)%len(waypoints)]
        wp2 = waypoints[(closest_waypoints[1]+i+1)%len(waypoints)]
        ta_now = angle_of_vector([wp1, wp2])
        if ta_now != ta1:
            straight = False
            break
        ta1 = ta_now
    if straight:
        return max(min(params["speed"]/4, 1.0), 0.0)
    else:
        if params["speed"] < 0.5:
            return 0
        else:
            return max(min(1-params["speed"]/4, 1.0), 0.0)

def reward_function(params):
    if params["all_wheels_on_track"] == False:
        return 1e-3
    return calculate_heading_factor(params) + calculate_spped_factor(params) +  calculate_spped_factor(params)

print(reward_function(mock_params.params))