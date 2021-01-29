# rcj_soccer_player controller - ROBOT Y1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils


class MyRobot(RCJSoccerRobot):
    def run(self):
        # woolong = False
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                # Get angle between the robot and the ball
                # and between the robot and the north
                x = ball_pos["x"] - robot_pos["x"]
                y = ball_pos["y"] - robot_pos["y"]
                if ((x*x+y*y)<=0.01):
                    a=ball_pos["x"]
                    b=ball_pos["x"]
                    print("b{:.2f}".format(b))     
                    if x<=0:
                         b=b-0.1
                         ball_pos["x"]=b
                    if x==-0.1 and abs(y)<0.1:
                         ball_pos["x"]=a
                    print("b改{:.2f}".format(b))
                    print("球位置{:.2f}".format( ball_pos["x"]))       
                    if abs(y)>0.1:
                        if y<0:
                             ball_pos["y"]=ball_pos["y"]+0.1
                        else:
                             ball_pos["y"]=ball_pos["y"]-0.1
               
                # if x < 1:
                #     woolong =True
                # else:
                #     woolong = False
                

                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                # Compute the speed for motors
                direction = utils.get_direction(ball_angle)

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                if direction == 0:
                    left_speed = -5
                    right_speed = -5
                else:
                    left_speed = direction * 4
                    right_speed = direction * -4

                print("{:.2f}".format( ball_pos["x"])) 

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
#my_robot.run()
