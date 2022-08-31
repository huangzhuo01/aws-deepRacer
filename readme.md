1. https://github.com/cdthompson/deepracer-training-2019/blob/7d8111d1b05709cd37e8fcb20415db452659509f/models/sep/iota/reward.py
2. 赛道角度（前后坐标） 车身角度heading 和 steering_angle 车在中线左右
3. waypoint分段函数 转向时 速度小（有最小值，低于最小值，惩罚）、偏离多转角
4. 靠中线
5. 异常情况（四轮都出界、反向） 惩罚
6. process step越快达成 奖励越大
