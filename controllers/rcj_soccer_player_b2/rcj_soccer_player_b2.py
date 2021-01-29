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

class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def __init__(self):
        super().__init__()
        self.Goal = -10                         #目標球門角度
        self.MAXSPEED = 5                       #系統限制最大速度(不可調)
        self.Deflection = math.radians(30)      #繞球

     def turn(self, deg) -> tuple[float, float]:
          pass    
    #     r_deg = math.radians(deg)
    #     deg = r_deg if r_deg <= math.pi else r_deg - 2 * math.pi
    #     if deg > math.pi / 2:
    #         deg = deg + self.Deflection
    #     elif deg < -math.pi / 2:
    #         deg = deg - self.Deflection

    #     left_speed = -1 * self.MAXSPEED * deg
    #     right_speed = self.MAXSPEED * deg
    #     if abs(left_speed) >= 10:
    #         left_speed = left_speed / abs(left_speed) * 10
    #     if abs(right_speed) >= 10:
    #         right_speed = right_speed / abs(right_speed) * 10
    #     return left_speed, right_speed
        
    def run(self):
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                if(self.Goal != -10):
                    #print(math.degrees(robot_pos["orientation"]))
                    self.Goal = robot_pos["orientation"]
                # Get the position of the ball
                ball_pos = data['ball']

                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle, distance = self.get_angles(ball_pos, robot_pos) #算角度
            
                #Compute the speed for motors
                
                    
                direction = utils.get_direction(ball_angle)

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                if direction == 0:
                    left_speed = -5
                    right_speed = -5
                else:
                    left_speed , right_speed = my_robot.turn(ball_angle)

                # Custom

                # print("X:{:.2f}, Y:{:.2f}".format(x, y))
                ####################

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
