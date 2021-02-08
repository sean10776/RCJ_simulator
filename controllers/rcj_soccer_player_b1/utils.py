import math
from typing import Tuple

def get_direction(ball_angle: float) -> int:
    """Get direction to navigate robot to face the ball

    Args:
        ball_angle (float): Angle between the ball and the robot

    Returns:
        int: 0 = forward, -1 = right, 1 = left
    """
    if ball_angle >= 345 or ball_angle <= 15:
        return 0
    return -1 if ball_angle < 180 else 1

def body_frame(left_speed: float, right_speed: float) -> dict:
    length = 0.75 + 0.01
    omega = (right_speed - left_speed) / length
    velocity = ( right_speed + left_speed) / 2
    radius = 0
    if omega != 0:
        radius = velocity / omega
    return {'velocity' : velocity, 'Omega': omega, 'Radius': radius}

def map_pwr(pwr:float or bool) -> float:
    if pwr > 10:
        pwr = 10
    if pwr <= -10:
        pwr = -10
    return pwr

def sign(value:float) -> int:
    if value == 0:
        return 1
    return abs(value) / value

def Team_dis(data:dict, name:str) -> dict:
    team_data = {}
    # bx, by = 0.0
    for i in data:
        if i[0] == name[0]:
            team_data[i] = {
                'x': data[i]['x'],
                'y': data[i]['y']
            }
        if i == 'ball':
            bx = data[i]['x']
            by = data[i]['y']
    Min_bot = {"Min":{"name":"", 'dis':999}, "Max":{"name":"", 'dis':0}}
    for i in [ name[0]+str(1), name[0]+str(2), name[0]+str(3)]:
        x = team_data[i]['x']
        y = team_data[i]['y']
        dis = math.sqrt((x-bx)**2 + (y-by)**2)
        if Min_bot['Min']['dis'] > dis:
            Min_bot['Min']['name'] = i
            Min_bot['Min']['dis'] = dis
        if Min_bot['Max']['dis'] < dis:
            Min_bot['Max']['name'] = i
            Min_bot['Max']['dis'] = dis
    return Min_bot


def ploy(role:str, ori:int, position:dict, ball:dict) -> Tuple[float, float]:
    left_speed = right_speed = 0.0
    angle = int(math.degrees(position['bot']['orientation']))
    line_pos = 0.55

    if role == "Attack":
        if position['bot']['x'] < position['ball']['x']:
            left_speed  = 10 + math.sin(math.radians(abs(angle) - 90)) * 10
            right_speed = 10 - math.sin(math.radians(abs(angle) - 90)) * 10
        elif int(position['bot']['orientation']) <= 0:      #face goal
            left_speed = right_speed = -10
            ratio = 5
            if ball['angle'] < 10 or ball['angle'] > 350:   #345 ~ 15
                ratio = 10
            elif ball['angle'] < 60:                        # 15 ~ 60
                right_speed += 5 * abs(math.sin(math.radians(ball['angle'])))
            elif ball['angle'] > 300:                       #345 ~ 300
                left_speed  += 5 * abs(math.sin(math.radians(ball['angle'])))
            else:
                left_speed = right_speed = 10
            #face front
            if ratio == 10:
                dx = -5*math.cos(math.radians(abs(angle) - 90)) + 5
                dy =  5*math.sin(math.radians(abs(angle) - 90)) - 0
                theta = math.degrees(math.atan2(dy , dx))#0
                if abs(theta) < 5:
                    theta = 0
                elif theta > 0:
                    theta =  90 - theta
                else:
                    theta = -90 - theta
            else:
                theta = 0
            left_speed  += math.sin(math.radians(abs(angle) - (90 + theta))) * ratio
            right_speed -= math.sin(math.radians(abs(angle) - (90 + theta))) * ratio
        else: # fixed to goal
            if angle > -90 and angle < 90:
                clockwise = -1
            else:
                clockwise = 1
            left_speed  =  10 * clockwise
            right_speed = -10 * clockwise
    elif role == "Defense":
        if position['bot']['x'] + line_pos * int(ori) < 0: #回場防守的方向修正要修
            if position['bot']['x'] * int(ori) > 0:
                ratio = 8
            else:
                ratio = 2
            left_speed  = 10 + math.sin(math.radians(abs(angle) - 90)) * ratio
            right_speed = 10 - math.sin(math.radians(abs(angle) - 90)) * ratio
        elif abs(angle) > 10:
            if angle < 0:
                clockwise = 1
            else:
                clockwise = -1
            left_speed  =  10 * clockwise
            right_speed = -10 * clockwise 
        else:
            ratio = 8
            dy = (position['ball']['y'] - position['bot']['y'])
            if position['ball']['x'] > position['bot']['x']:
                offset = 0.075 * sign(dy)
            else:
                offset = 0
            dy += offset
            if int(ori) * position['ball']['x'] > 0:
                left_speed = right_speed = -10 * dy * 10 + sign(dy) * (-10)
            else:
                left_speed = right_speed = -10 * dy * 100
            left_speed  -= math.sin(math.radians(angle)) * ratio
            right_speed += math.sin(math.radians(angle)) * ratio
    else:#游擊
        pass
        # if abs(position['ball']['x']) < 0.3:#原點+-0.3 -> 我方0.3 敵方 0.4~0.5
        #     if ball['angle'] < 10 or ball['angle'] > 350:
        #         return -10, -10
        #     elif ball['angle'] > 180:
        #         clockwise = 1
        #     else:
        #         clockwise = -1
        #     left_speed = 10 * clockwise
        #     right_speed = -10 * clockwise
        # else: #中場以外
        #     #校正
        #     if abs(angle - int(ori) * 90) > 3:
        #         if angle > -90 and angle < 90:
        #             clockwise = -1
        #         else:
        #             clockwise = 1
        #         left_speed  =  10 * clockwise * abs(angle - int(ori) * 90) / 90
        #         right_speed = -10 * clockwise * abs(angle - int(ori) * 90) / 90
        #     elif abs(position['ball']['x']) < 0.01 and abs(position['ball']['y']) < 0.01:
        #         return -10, -10
        #     elif position['bot']['x'] * int(ori) > -0.3: #從對面退回來
        #         left_speed = right_speed = 10
        #     elif position['ball']['x'] * int(ori) > 0 and position['ball']['x'] < position['bot']['x']:
        #         if ball['angle'] < 10 or ball['angle'] > 350:
        #             clockwise = 0
        #         elif ball['angle'] > 180:
        #             clockwise = 1
        #         else:
        #             clockwise = -1
        #         left_speed = 10 * clockwise
        #         right_speed = -10 * clockwise
        #     elif position['bot']['x'] * int(ori) > 0.3:  #從我方前進
        #         left_speed = right_speed = -10
    left_speed  = map_pwr(left_speed)
    right_speed = map_pwr(right_speed)
    return left_speed, right_speed

