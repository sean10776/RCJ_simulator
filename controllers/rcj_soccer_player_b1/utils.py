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
        left_speed = right_speed = -10
        if int(position['bot']['orientation']) <= 0 and position['bot']['x'] - position['ball']['x'] > 0.065: #face goal
            print("goal")
            if ball['angle'] < 15 or ball['angle'] > 345:
                pass
            elif ball['angle'] < 180 - 20:
                print("right")
                right_speed += 10 * abs(math.sin(math.radians(ball['angle']))) * (1.5 - ball['distance']) - 5 * abs(math.cos(math.radians(angle)))
            elif ball['angle'] > 180 + 20:
                print("left")
                left_speed  += 10 * abs(math.sin(math.radians(ball['angle']))) * (1.5 - ball['distance']) - 5 * abs(math.cos(math.radians(angle)))
            else:
                left_speed = right_speed = 10
        else: # fixed to goal
            print("backs")
            left_speed = right_speed = 10
            if abs(angle - int(ori) * 90) > 5:
                print('fix')
                if angle > -90 and angle < 90:
                    clockwise = -1
                else:
                    clockwise = 1
                left_speed  =  10 * clockwise * abs(angle - int(ori) * 90) / 90
                right_speed = -10 * clockwise * abs(angle - int(ori) * 90) / 90
            else:
                dy = (position['ball']['y'] - position['bot']['y'])
                if dy > 0:
                    left_speed  += 10 * abs(dy)
                else:
                    right_speed += 10 * abs(dy)
        left_speed  = map_pwr(left_speed)
        right_speed = map_pwr(right_speed)
    elif role == "Defense" or role == "Wait":#未完成
        if position['bot']['x'] + line_pos * int(ori) < 0: #回場防守的方向修正要修
            left_speed = right_speed = 10
            if int(position['bot']['orientation']) != int(ori):
                left_speed = -10
        elif abs(angle) >= 1:
            if angle < 0:
                clockwise = 1
            else:
                clockwise = -1
            left_speed  =  10 * clockwise * abs(angle) / 90
            right_speed = -10 * clockwise * abs(angle) / 90
            left_speed  = map_pwr(left_speed)
            right_speed = map_pwr(right_speed)
        elif position['ball']['y'] != position['bot']['y']:
            dy = (position['ball']['y'] - position['bot']['y'])
            if int(ori) * position['ball']['x'] > 0:
                left_speed = right_speed = -10 * dy * 10 + sign(dy) * (-5) * abs(2 - ball['distance']) #TODO 最低速 球越近越快
            else:
                left_speed = right_speed = -10 * sign(dy)
            left_speed = right_speed = map_pwr(right_speed)
            if abs(dy) < 0.05 and position['ball']['x'] > position['bot']['x']:
                left_speed = right_speed = 0
        else:
            print(position['bot']['y'], "error")
    else:
        pass
    return left_speed, right_speed

