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
    
    defense_fix_deg = 3

    if role == "Attack":
        left_speed = right_speed = -10
        if ball['angle'] < 10 or ball['angle'] > 350:
            pass
        elif ball['angle'] > 180 + 30:
            left_speed  += abs(math.cos(math.radians(ball['angle']))) * 5
        elif ball['angle'] < 180 - 30:
            right_speed += abs(math.cos(math.radians(ball['angle']))) * 5
        else:
            left_speed  = right_speed = 10

        if int(ori) != int(position['bot']['orientation']) and position['bot']['x'] > 0:
            if abs(angle) < 90:
                left_speed  = -10
                right_speed = 10
            else:
                left_speed  = 10
                right_speed = -10

        print(left_speed, right_speed)
        left_speed  = map_pwr(left_speed)
        right_speed = map_pwr(right_speed)
    elif role == "Defense":#未完成
        if position['bot']['x'] + 0.6 * int(ori) < 0: #回場防守的方向修正要修
            if int(ori) != int(position['bot']['orientation']):
                pass
                # left_speed  =  10
                # right_speed = -10
            else:
                left_speed = right_speed = 10
        # elif position['ball']['x'] < -0.3 and abs(position['ball']['y'] - position['bot']['y']) > 0.3:
        #     if ball['angle'] > 180:
        #         ball['angle'] -= 360
        #     left_speed = ball['angle'] / 90 * -4
        #     right_speed = ball['angle'] / 90 * 4
        #     left_speed  = map_pwr(left_speed)
        #     right_speed = map_pwr(right_speed)
        elif abs(angle) > defense_fix_deg and abs(angle) < 180 - defense_fix_deg:
            if angle < 0:
                clockwise = 1
            else:
                clockwise = -1
            left_speed  =  10 * clockwise * abs(math.sin(abs(180 - angle))) * 0.8
            right_speed = -10 * clockwise * abs(math.sin(abs(180 - angle))) * 0.8
            left_speed  = map_pwr(left_speed)
            right_speed = map_pwr(right_speed)
        elif position['ball']['y'] != position['bot']['y']:
            dy = (position['ball']['y'] - position['bot']['y'])
            left_speed = right_speed = -10 * dy * 10 + sign(dy) * -4 #TODO 最低速 球越近越快
            left_speed = right_speed = map_pwr(right_speed)
    else:
        pass
    return left_speed, right_speed
