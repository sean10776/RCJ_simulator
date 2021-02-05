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

def map_pwr(pwr:float) -> float:
    if pwr > 10:
        pwr = 10
    if pwr <= -10:
        pwr = -9.9
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
def ploy(role:str, ori:int, robot_pos:dict, ball_angle:float) -> Tuple[float, float]:
    left_speed = right_speed = 0.0
    if role == "Attack":
        pass
    elif role == "Defense":
        angle = int(math.degrees(robot_pos['orientation']))
        if robot_pos['x'] + 0.5 * int(ori) < 0:
            if int(ori) != int(robot_pos['orientation']):
                left_speed  =  10
                right_speed = -10
            else:
                left_speed = right_speed = 10
        elif ball_pos['x'] < 0 and abs(ball_pos['y'] - robot_pos['y']) > 0.3:
            if ball_angle > 180:
                ball_angle -= 360
            left_speed = ball_angle / 90 * -4
            right_speed = ball_angle / 90 * 4
            left_speed  = utils.map_pwr(left_speed)
            right_speed = utils.map_pwr(right_speed)
        elif abs(angle) > 3 and abs(angle) < 180 - 3:
            if angle < 0:
                left_speed  =  10 * abs(angle) / 45
                right_speed = -10 * abs(angle) / 45
            else:
                left_speed  = -10 * abs(180 - angle) / 45
                right_speed =  10 * abs(180 - angle) / 45
            left_speed  = utils.map_pwr(left_speed)
            right_speed = utils.map_pwr(right_speed)
        elif ball_pos['y'] != robot_pos['y']:
            dy = (ball_pos['y'] - robot_pos['y'])
            left_speed = right_speed = -10 * dy * 10 + utils.sign(dy) * -4
            left_speed = right_speed = utils.map_pwr(right_speed)
    else:
        pass
    return left_speed, right_speed
