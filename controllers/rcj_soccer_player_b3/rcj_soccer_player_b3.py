# rcj_soccer_player controller - ROBOT B3

###### REQUIRED in order to import files from B1 controller
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from rcj_soccer_player_b1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def __init__(self):
        super().__init__()
        self.__start = False
        self.__forward = -1
        self.__ori = 0
        self.__role = ""

    def run(self):
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                if self.__start == False:
                    self.__start = True
                    self.__ori = robot_pos['orientation']
                    self.__pre_pos = robot_pos
                    print(self.__ori)
                
                # 隊友遠近判斷
                Team_distance = utils.Team_dis(data, self.name)
                if Team_distance['Min']['name'] == self.name:
                    self.__role = "Attack"
                elif Team_distance['Max']['name'] == self.name:
                    self.__role = "Defense"
                else:
                    self.__role = "Wait"

                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle, distance = self.get_angles(ball_pos, robot_pos)

                pos = {"bot":robot_pos, "ball":ball_pos}
                left_speed, right_speed = utils.ploy("Defense", self.__ori, pos, ball_angle)
                
                '''Defense
                angle = int(math.degrees(robot_pos['orientation']))
                if robot_pos['x'] + 0.5 * int(self.__ori) < 0:
                    if int(self.__ori) != int(robot_pos['orientation']):
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
                    left_speed = right_speed = 0
                '''

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)



my_robot = MyRobot()
my_robot.run()
