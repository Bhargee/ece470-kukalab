#!/usr/bin/python
import sys

import roslib
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import numpy as np

class image_converter:
  def __init__(self):
    cv2.namedWindow("Image window", 1)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError, e:
      print e
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    s = gray.shape
    output = cv_image.copy()
    squares = self.find_squares(gray)
    cv2.drawContours( output, squares, -1, (0, 255, 0), 3 )
    cv2.imshow('squares', output)
    waitKey(0)
if __name__ == '__main__':
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"
