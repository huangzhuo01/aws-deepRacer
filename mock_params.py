params ={
    "all_wheels_on_track": True,        # flag to indicate if the agent is on the track
    "x": 0.1,                            # agent's x-coordinate in meters
    "y": 0.1,                            # agent's y-coordinate in meters
    "closest_objects": [0, 0],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
    "closest_waypoints": [0, 0],       # indices of the two nearest waypoints.
    "distance_from_center": 0.1,         # distance in meters from the track center 
    "is_crashed": False,                 # Boolean flag to indicate whether the agent has crashed.
    "is_left_of_center": False,          # Flag to indicate if the agent is on the left side to the track center or not. 
    "is_offtrack": False,                # Boolean flag to indicate whether the agent has gone off track.
    "is_reversed": False,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
    "heading": 10,                      # agent's yaw in degrees
    "objects_distance": [0.1, ],         # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
    "objects_heading": [0.1, ],          # list of the objects' headings in degrees between -180 and 180.
    "objects_left_of_center": [False, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
    "objects_location": [(0.1, 0.1),], # list of object locations [(x,y), ...].
    "objects_speed": [0.1, ],            # list of the objects' speeds in meters per second.
    "progress": 0.1,                     # percentage of track completed
    "speed": 0.1,                        # agent's speed in meters per second (m/s)
    "steering_angle": 0.1,               # agent's steering angle in degrees
    "steps": 2,                          # number steps completed
    "track_length": 0.1,                 # track length in meters.
    "track_width": 0.1,                  # width of the track
    "waypoints": [(0.1, 0.1), ]        # list of (x,y) as milestones along the track center

}