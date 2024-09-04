#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from tf.transformations import euler_from_quaternion
import math

imu_data_val = Vector3()  

def imucallback(msg):
       global imu_data_val
       rospy.loginfo("I heard %s", msg.linear_acceleration)
       imu_data_val =  msg.linear_acceleration
       imu_data_val_list = [imu_data_val.x, imu_data_val.y, imu_data_val.z]
       radian_list = euler_from_quaternion(imu_data_val_list)
       imu_data_val.x, imu_data_val.y, imu_data_val.z = [rad * (180/math.pi) for rad in radian_list]

def listener():
    
       rospy.init_node('listener', anonymous=True)
       rospy.Subscriber("/imu", Imu, imucallback)
       pub = rospy.Publisher('/orientation/degree', Vector3, queue_size=10)
       rate = rospy.Rate(1)

       while not rospy.is_shutdown():
           pub.publish(imu_data_val)
           rate.sleep()
       rospy.spin()
   
if __name__ == '__main__':
     try:  
       listener()
     except rospy.ROSInterruptException:
       pass
     

