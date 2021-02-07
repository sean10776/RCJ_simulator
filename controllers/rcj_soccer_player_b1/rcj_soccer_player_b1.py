# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils


class MyRobot(RCJSoccerRobot):
    def __init__(self):
        super().__init__()
        self.__start = False
        self.__forward = -1
        self.__ori = 0
        self.__role = ""
        self.__stuck = False
        self.__pre_pos = {}
        
    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                if self.__start == False:
                    self.__ori = robot_pos['orientation']
                    self.__pre_pos = robot_pos
                
                # 隊友遠近判斷
                Team_distance = utils.Team_dis(data, self.name)
                if Team_distance['Min']['name'] == self.name:
                    self.__role = "Attack"
                elif Team_distance['Max']['name'] == self.name:
                    self.__role = "Defense"
                else:
                    self.__role = "Defense"

                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle, distance = self.get_angles(ball_pos, robot_pos)

                pos  = {"bot":robot_pos, "ball":ball_pos}
                ball = {"angle": ball_angle, "distance": distance}
                left_speed, right_speed = utils.ploy("Defense", self.__ori, pos, ball)

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
                self.__start = True


my_robot = MyRobot()
my_robot.run()
