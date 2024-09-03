#!/usr/bin/env python3
#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
import numpy as np


Q = 0.01  
R = 0.1  
P = 1.0   
x = 0.0  

def imu_callback(msg):
    global x, P

    yaw = msg.orientation.z  

    x_pred = x
    P_pred = P + Q

    K = P_pred / (P_pred + R)
    x = x_pred + K * (yaw - x_pred)
    P = (1 - K) * P_pred

    filtered_yaw_msg = Float64()
    filtered_yaw_msg.data = x
    yaw_angle_pub.publish(filtered_yaw_msg)

    rospy.loginfo(f"Filtered YAW angle: {x}")

def listner():
    global yaw_angle_pub

    rospy.init_node('kalman_filter_node')

    yaw_angle_pub = rospy.Publisher('/yaw_angle', Float64, queue_size=10)

    rospy.Subscriber('/imu', Imu, imu_callback)

    rospy.spin()

if __name__ == '__main__':
    listner()
