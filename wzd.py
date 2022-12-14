def calculate_all_on_track(params):
    #############################################################################
    '''
    Example of using all_wheels_on_track and speed
    '''

    # Read input variables
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']

    # Set the speed threshold based your action space
    SPEED_THRESHOLD = 1.0

    if not all_wheels_on_track:
        # Penalize if the car goes off track
        reward = 1e-3
    elif speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        reward = 0.5
    else:
        # High reward if the car stays on track and goes fast
        reward = 1.0

    return float(reward)




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
    heading = params['heading']
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
    waypoints =  ['waypoints']
    heading = params['heading'] + (params['steering_angle'] / 2)
    # Calculate the immediate track angle
    wp1 = waypoints[closest_waypoints[0]]
    wp2 = waypoints[closest_waypoints[1]]
    ta1 = angle_of_vector([wp1,wp2])
    straight = True
    for i in range(3):
        wp1 = waypoints[closest_waypoints[1]+i]
        wp2 = waypoints[closest_waypoints[1]+i+1]
        ta_now = angle_of_vector([wp1, wp2])
        if ta_now != ta1:
            straight = False
            break
    if straight:
        return max(min(params["speed"]/5, 1.0), 0.0) #??????????????????
    else:
        if speed < 0.1:
            return 0
        else:
            return max(min(1-params["speed"]/5, 1.0), 0.0) #??????????????????

def rewreward_functionard(params):
    if params["all_wheels_on_track"] == False:
        return 1e-3
    return calculate_heading_factor(params) + calculate_spped_factor(params) +  calculate_spped_factor(params)
