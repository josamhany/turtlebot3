#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray

def imucallback(msg):
    global ranges_list
    rospy.loginfo("I heard %s", msg.ranges)
    ranges_list.data = msg.ranges

def listener():
    global ranges_list
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/scan", LaserScan, imucallback)
    pub = rospy.Publisher('scanning', Float32MultiArray, queue_size=10)
    
    ranges_list = Float32MultiArray()
    
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        if ranges_list.data:  
            pub.publish(ranges_list)
        rate.sleep()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
