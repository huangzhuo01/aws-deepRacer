#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

LIMITS_SPEED = [1, 4]
LIMITS_STEERING_ANGLE = [-30, 30]

def reduce(f, s):
    r = 0
    for i in s:
        r = f(r, i)
    return r

def angle_of_vector(vector):
    rad = math.atan2(vector[1][1] - vector[0][1], vector[1][0] - vector[0][0])
    angle = math.degrees(rad)
    return angle if (angle >= 0) else (360.0 + angle)

def distance_of_vector(vector):
    return ((vector[1][1] - vector[0][1]) ** 2 + (vector[1][0] - vector[0][0]) ** 2) ** 0.5

def span_of_points(points):
    return reduce(lambda x, y: x + y, [distance_of_vector([points[i], points[i+1]]) for i in range(len(points)-1)])

def diff_of_angle(angle1, angle2):
    r = angle1 - angle2
    return r if (r >= 0) else (360.0 + r)

def reward_function(params):
    waypoints   = params["waypoints"]
    pre         = params['closest_waypoints'][0]
    nxt         = params['closest_waypoints'][1]

    is_offtrack             = params["is_offtrack"]
    speed                   = params["speed"]
    progress                = params["progress"]
    all_wheels_on_track     = params["all_wheels_on_track"]
    distance_from_center    = params["distance_from_center"]
    # is_left_of_center       = params["is_left_of_center"]
    steps                   = params["steps"]
    track_width             = params["track_width"]
    heading_direction       = params["heading"] # 航行方向
    # track_direction         = angle_of_vector([waypoints[pre], waypoints[nxt]]) # 道路方向
    steering_angle          = params["steering_angle"]
    # heading_angle           = abs(diff_of_angle(angle_of_vector([waypoints[pre], waypoints[nxt]]),params["heading"])) # 航向-道路夹角
    forward_waypoints       = [waypoints[(nxt+i)%len(waypoints)] for i in range(3)] # 前方航向关键点
    forward_directions      = [angle_of_vector([waypoints[(pre+i)%len(waypoints)], waypoints[(nxt+i)%len(waypoints)]]) for i in range(3)] # 前方航向弯度

    f = distance_of_vector([forward_waypoints[0], forward_waypoints[-1]]) / span_of_points(forward_waypoints)  # 前路弯曲因子 (0,1]越小说明越弯曲
    s = float(speed - LIMITS_SPEED[0]) / (LIMITS_SPEED[1] - LIMITS_SPEED[0]) # 速度因子 [0,1]
    if is_offtrack:
        reward_function.steps = None
        return -10.0
    elif not all_wheels_on_track:
        if s < f:
            A = 2.5 # or 3,4,5?
            return A*math.sin(math.pi/2*s*1/f)-(A-1)
        else:
            return math.sin(math.pi/2*s*1/f)
    else:
        B = 8.0
        a = max(LIMITS_STEERING_ANGLE[0],min(LIMITS_STEERING_ANGLE[1],reduce(
            lambda x, y: x + y,
            [diff_of_angle(forward_directions[0],heading_direction)]+
            [diff_of_angle(forward_directions[i+1],forward_directions[i]) for i in range(len(forward_directions)-1)]
        )))
        if a * steering_angle < 0:
            a1 = 2*math.sin(math.pi/2*abs(a - steering_angle)/LIMITS_STEERING_ANGLE[1]-LIMITS_STEERING_ANGLE[0])-1 # 转角因子,反向, [0,1]越小说明转角越大
            if a1 < 0:
                return a1
            else:
                a1 = B/2 * a1 + 1
        else:
            a1 = B/2 * (1.0-math.tan(abs(a - steering_angle)/abs(LIMITS_STEERING_ANGLE[0] if (a < 0 or steering_angle < 0) else LIMITS_STEERING_ANGLE[1]) * math.pi / 4)) + 1 # 转角因子,同向 [1,B+1]越小说明转角越小
        w = B * (1.0-float(distance_from_center)/track_width*2) + 1 # 偏移中心轴因子 [1,B+1]
        s1 = B * s + 1 # 速度因子 [1,B+1]
        t = 1.0
        if progress>0 and steps > 0:
            tpp = float(progress) / steps
            if hasattr(reward_function, 'steps') and reward_function.steps is not None:
                t = tpp / reward_function.steps # 完成度因子
            reward_function.steps = tpp
        rwd = a1 * s1 * w * t
        print("R=%s (a1:%s, s1:%s, w:%s, t:%s) - is_offtrack:%s, speed:%s, progress:%s, all_wheels_on_track:%s, distance_from_center:%s, steps:%s, track_width:%s, heading_direction:%s, steering_angle:%s, forward_waypoints:%s, forward_directions:%s" % (rwd, a1, s1, w, t, is_offtrack,speed,progress,all_wheels_on_track,distance_from_center,steps,track_width,heading_direction,steering_angle,forward_waypoints,forward_directions))
        return rwd

if __name__ == "__main__":
    from mock_params import params
    print(reward_function(params))


