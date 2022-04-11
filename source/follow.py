#!/usr/bin/env python

import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

class Follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.twist = Twist()
    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_yellow = numpy.array([ 40, 0, 0])
        upper_yellow = numpy.array([ 120, 255, 255])
        mask = cv2.inRange(hsv,  lower_yellow, upper_yellow)
        masked = cv2.bitwise_and(image, image, mask=mask)
        h, w, d = image.shape
        #created a valid way to change a list of lists/ python notation doesn't have a built in function
        #this takes a slice from a camera
        for i in range(0,200):
            mask[i]=1920 * [0]
        for z in range(220,1079):
            mask[i]=1920 * [0]
        cv2.imshow("sliver", mask)
        M = cv2.moments(mask)
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00']) + 100
            cy = int(M['m01']/M['m00'])
            err = cx - w/2
            self.twist.linear.x = 0.2
            self.twist.angular.z = -float(err) / 1000
            self.cmd_vel_pub.publish(self.twist)
        cv2.imshow("image", image)
        cv2.waitKey(3)
rospy.init_node('follower')
follower = Follower()
rospy.spin()