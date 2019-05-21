#!/usr/bin/env python2

import time

import rospy as ros
import numpy as np
from numpy import random

from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan

def processScanCallback(msg):
    n_ranges = len(msg.ranges)
    nearest = min(msg.ranges)
    ros.loginfo("I've a total of {} measurements to process! Are you ready? Nearest = {}".format(n_ranges, nearest))

def main():
    ros.init_node('exploring')
    ros.loginfo("Robotic explorer node running and initialized! Let's have some fun!")

    scan_sub = ros.Subscriber("/base_scan", LaserScan, processScanCallback, buff_size=1000)
    move_pub = ros.Publisher("/cmd_vel", Twist, queue_size=1000)

    random.seed(time.time())

    rate = ros.Rate(2)
    begin = ros.Time.now()

    while begin.to_sec() == 0:
        begin = ros.Time.now()

    ellapsed_time = 0

    while not ros.is_shutdown() and ellapsed_time < 60.0*5.0:

        msg = Twist()
        msg.linear.x = 2*random.rand()
        msg.angular.z = 4*random.rand()-2

        move_pub.publish(msg)

        ros.loginfo("[robot_nav] Pub twist [{}, {}] ".format(msg.linear.x, msg.angular.z))

        rate.sleep()

        current = ros.Time().now()
        ellapsed_time = current.to_sec() - begin.to_sec()
        ros.loginfo('[robot_explorer] Ellpased time: {}'.format(ellapsed_time))


if __name__ == "__main__":
    main()