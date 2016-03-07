""" 
This example brings the robot's arm to the start_frame and interpolates to the end_frame 
Here we focus on how to use the function move_cartesian_frame_linear_interpolation under the robot class

Class: robot.py
Method: move_cartesian_frame_linear_interpolation(self, abs_frame, speed, False/True)
Dependencies: poseInterpolator.py / tfx

Input param:  
1st) abs_frame 		-> The frame of the end position expressed as a list type. (note you can also choose abs_Frame as a tfx.canonical.CanonicalTransform type)

2nd) speed 		-> (float) type if cubic interpolation is False
	  		-> (list) type of [velocity_Low, velocity_High] if cubic interpolation is True

3rd) False/True 	-> (Default) False which makes the interpolation linear
			-> (Optional) True which makes the interpolation a cubic function; Has yet to be implemented in future versions

Explaination:

- The function takes in an absolute frame in catresian space and applies SLERP interpolation to bring it from its current position to the position
that is specified by the user in abs_frame.

- Vector interpolation is done linearly in a straight line from the start to end points
- Rotation is done using quaternion SLERP function under the tfx.transformations.quaternion_slerp method

- We calculate the vector norm of the start and end points and divide into segments based on 1 interval per 0.1 mm of distance travelled

- The elements for abs_frame are a list type: [X,Y,Z,Roll,Pitch,Yaw] representing the vector and rotations of the end pose

- The 3rd parameter turns the cubic interpolator on / off. If cubic interpolator is False, then we are using a linear interpolator and the arm will sweep across
the coordinates at a uniform speed. As of now, no cubic interpolation function has been implemented yet so please help!!!!!!!!!!!!!!!!
"""

import time
import numpy as np
import robot
import sys
import tfx

def Interpolate(robotname):
    r = robot.robot(robotname)

    start_pose = r.get_current_cartesian_position()
    pose1 = r.get_current_cartesian_position()
    pose1.position.x -= 0.01
    pose1 = tfx.pose(pose1.as_tf()*tfx.transform(tfx.rotation_tb(0, 0.000001, 0)))


    r.move_cartesian_frame_linear_interpolation(start_pose, 0.01)
    r.move_cartesian_frame_linear_interpolation(pose1, 0.01)
    r.move_cartesian_frame_linear_interpolation(start_pose, 0.01)




if __name__ == '__main__':
    """Here will check if we are given the name of the robot arm or not, if we are we run Interpolate()"""
    """ Expected inputs are robot's arm """

    if (len(sys.argv) == 2):
        raw_input("The dvrk arm will now move. Please ensure that there not obstacles in a 1cm cube around the arm. Press any key to continue")
        Interpolate(sys.argv[1])
    else:
        print sys.argv[0] + ' requires one argument, i.e. name of dVRK arm'


