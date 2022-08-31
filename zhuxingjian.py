def reward_when_out_road(speed):
    # if speed > 10:
    #     return 0.001
    # elif speed > 5:
    #     return 0.005
    # elif speed > 1:
    #     return 0.01
    # return 0.1
    return 1

def reward_when_in_road(speed, distance_from_center):
    # if distance_from_center > 2 * track_width:
    #     if speed > 10:
    #         return 0.1
    #     elif speed > 5:
    #         return 0.2
    #     elif speed > 1:
    #         return 0.3
    #     return 0.5
    # elif distance_from_center > 1 * track_width:
    #     if speed > 10:
    #         return 0.15
    #     elif speed > 5:
    #         return 0.25
    #     elif speed > 1:
    #         return 0.35
    #     return 0.55
    # elif distance_from_center > 0.5 * track_width:
    #     if speed > 10:
    #         return 0.15
    #     elif speed > 5:
    #         return 0.25
    #     elif speed > 1:
    #         return 0.35
    #     return 0.55
    # elif distance_from_center > 0.1 * track_width:
    # else:
    return 1

def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    if not all_wheels_on_track:
        reward = reward_when_out_road(speed)
    else:
        reward = reward_when_in_road(speed, distance_from_center)

    return float(reward)