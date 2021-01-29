# rcj_soccer_player controller - ROBOT Y1

# Feel free to import built-in libraries
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
# You can now import scripts that you put into the folder with your
# robot B1 controller
from rcj_soccer_player_y1 import rcj_soccer_robot, utils
######

# Feel free to import built-in libraries
import math


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        # woolong = False
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                # Get angle between the robot and the ball
                # and between the robot and the north

                

                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                x = ball_pos["x"] - robot_pos["x"]
                y = ball_pos["y"] - robot_pos["y"]
                a=math.sqrt(x*x+y*y)
                if (a>0.2):
                    if direction == 0:
                        left_speed = -5
                        right_speed = -5
                    else:
                        left_speed = direction * 4
                        right_speed = direction * -4
                elif (a<=0.2):
                    left_speed = -5
                    right_speed = -2
                elif (a<=0.2):
                    left_speed = -2
                    right_speed = -5

                print("{:.2f}".format( ball_pos["x"])) 

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
#my_robot.run()