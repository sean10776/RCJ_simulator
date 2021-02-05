# rcj_soccer_player controller - ROBOT B2

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
import matplotlib.pyplot as plt 

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def __init__(self):
        super().__init__()
        self.Goal = -10                         #目標球門角度
        self.MAXSPEED = 5                       #系統限制最大速度(不可調)
        self.Deflection = math.radians(30)      #繞球
        self.limit_deg = 10

    def move(self, deg, way):                         #deg:-180~180
        if way < 0:
            left_speed = right_speed = way * self.MAXSPEED
            if deg > 0:
                right_speed -= way * self.MAXSPEED * math.sin(math.radians(abs(deg)))
            elif deg < 0:
                left_speed -=  way * self.MAXSPEED * math.sin(math.radians(abs(deg)))
        else:
            left_speed = right_speed = way * self.MAXSPEED * 0.5
            if deg > 0:
                right_speed = way * self.MAXSPEED * math.cos(math.radians(abs(deg)))
            elif deg < 0:
                left_speed =  way * self.MAXSPEED * math.cos(math.radians(abs(deg)))
        self.left_motor.setVelocity(left_speed)
        self.right_motor.setVelocity(right_speed)
        
    def run(self):
        way = -1

        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                if(self.Goal == -10):
                    #print(math.degrees(robot_pos["orientation"]))
                    self.Goal = robot_pos["orientation"]
                # Get the position of the ball
                ball_pos = data['ball']

                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle, distance = self.get_angles(ball_pos, robot_pos)

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise

                # Set the speed to motors
                if ball_pos["x"] - robot_pos["x"] < 0:
                    way = -1
                else:
                    way = 1
                if ball_angle < 90 or ball_angle > 270:
                    if ball_angle > 270:
                        ball_angle -= 360
                else:
                    ball_angle -= 360

                self.move(ball_angle, way)


my_robot = MyRobot()
# my_robot.run()
