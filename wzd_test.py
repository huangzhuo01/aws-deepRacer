#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

LIMITS_SPEED = [1, 4] #速度限制
LIMITS_STEERING_ANGLE = [-30, 30] #转角限制

# 计算两个点之构成的直线与x轴的夹角。返回的是度数。
def angle_of_vector(vector):
    rad = math.atan2(vector[1][1] - vector[0][1], vector[1][0] - vector[0][0])
    return math.degrees(rad)

# 计算两个点之间的距离 函数
def distance_of_vector(vector):
    return ((vector[1][1] - vector[0][1]) ** 2 + (vector[1][0] - vector[0][0]) ** 2) ** 0.5

def span_of_points(points):
    def reduce(f, s):
        r = 0
        for i in s:
            r += i
        return r
    return reduce(lambda x, y: x + y, [distance_of_vector([points[i], points[i+1]]) for i in range(len(points)-1)])

def reward_function(params):
    waypoints   = params["waypoints"]
    pre         = params['closest_waypoints'][0]
    nxt         = params['closest_waypoints'][1]

    is_crashed              = params["is_crashed"]
    is_offtrack              = params["is_offtrack"]
    speed                   = params["speed"]
    progress                = params["progress"]
    all_wheels_on_track     = params["all_wheels_on_track"]
    distance_from_center    = params["distance_from_center"]
    is_left_of_center       = params["is_left_of_center"]
    steps                   = params["steps"]
    track_width             = params["track_width"]
    # heading_direction       = params["heading"] # 航行方向
    # track_direction         = angle_of_vector([waypoints[pre] waypoints[nxt]]) # 道路方向
    # steering_angle          = params["steering_angle"]
    # heading_angle           = abs(angle_of_vector([waypoints[pre] waypoints[nxt]])-params["heading"]) # 航向-道路夹角
    forward_waypoints       = [waypoints[(pre+i)%len(waypoints)] for i in range(3)] # 前方航向关键点
    # forward_directions      = [angle_of_vector([waypoints[(pre+i)%len(waypoints)] waypoints[(nxt+i)%len(waypoints)]]) for i in range(3)], # 前方航向弯度

    print(f'LOG_DATA:{waypoints}')
    print(f'LOG_DATA:{track_width}')
    print(f'LOG_DATA:{steps}')

    f = distance_of_vector([forward_waypoints[0], forward_waypoints[-1]]) / span_of_points(forward_waypoints)  # 前路弯曲因子 (0,1]越小说明越弯曲
    s = float(speed - LIMITS_SPEED[0]) / (LIMITS_SPEED[1] - LIMITS_SPEED[0]) # 速度因子 [0,1]
    if is_offtrack:
        # 若出界
        return -10
    else:
        # 若不出界
        # 计算前面是否需要转弯，转弯角度是向左转还是向右转。
        # 取车前点p1 车后点p2 p1与p2的角度作为当前方向计算出角度，取车前第二个点p3与车前第1个点p1计算出角度 作为将要转向的角度。
        # 若即将要转向的角度 - 当前角度 为负数数且小于-5，则表示轨道需要往右转，则车子在轨道右侧加分。否则其余情况一律车子在轨道左侧加分
        
        xPoint = 0
        
        p1 = waypoints[closest_waypoints[0]]
        p2 = waypoints[closest_waypoints[1]]
        p3 = waypoints[(closest_waypoints[0] + 1) % len(waypoints)]
        now_angle = angle_of_vector([p1,p2])
        next_angle = angle_of_vector([p3,p1])
        distance_from_border = 0.5 * track_width - distance_from_center # 车子距离边界的距离
        if next_angle - now_angle <= -5:
            if not is_left_of_center and distance_from_border >= 0.05 : # 车子在轨道右侧 且 距离边界>=0.05
                xPoint = 10
            else:
                xPoint = 1
        else:
            if is_left_of_center and distance_from_border >= 0.05 :
                xPoint = 10
            else:
                xPoint = 1

    



        # w = 9 * (1-float(distance_from_center)/track_width*2) + 1 # 偏移中心轴因子 [1,10]
        s1 = 9 * s + 1 # 速度因子 [1,10]
        t = 1.0
        if progress > 0:
            tpp = float(steps) / progress
            if hasattr(reward_function, 'steps'):
                t = tpp / reward_function.steps # 完成度因子
            reward_function.steps = tpp # 这里有个疑惑 为什么steps既是从params["steps"]读取，然后又在这里给steps赋值，感觉这里赋值会备覆盖调，没有用。通过日志里看steps会特别大，
        return s1 * t + xPoint

if __name__ == "__main__":
    from mock_params import params
    print(reward_function(params))