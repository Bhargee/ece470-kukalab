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
    cv_image_copy = cv_image.copy()
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    lower_cube = np.array([110,50,50])#np.array([50,46,75])
    upper_cube = np.array([130,255,255])#np.array([90,66,125])
    lower_dots = np.array([35,23,104])
    upper_dots = np.array([55,153,224])
    cube_mask = cv2.inRange(hsv, lower_cube, upper_cube)
    dots_mask = cv2.inRange(hsv, lower_dots, upper_dots)
    cube_contours, heirarchy = cv2.findContours(cube_mask, cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)
    dots_contours, heirarchy = cv2.findContours(dots_mask, cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for contour in dots_contours:
      x,y,w,h = cv2.boundingRect(contour)
      if (w*h) >= 100:
        cv2.circle(cv_image, (x+(w/2),y+(h/2)), 1, (0,255,0), 3)
        cv2.rectangle(cv_image, (x,y), (x+w, y+h), (255,0,0), 2)
        cv2.putText(cv_image,'%s,%s'%(x,y),(x,y), font, 1,(0,255,0),2)

    for contour in cube_contours:
      x,y,w,h = cv2.boundingRect(contour)
      if (w*h) >= 250:
        cv2.circle(cv_image_copy, (x+(w/2),y+(h/2)), 1, (0,255,0), 3)
        cv2.rectangle(cv_image_copy, (x,y), (x+w, y+h), (255,0,0), 2)
        cv2.putText(cv_image_copy,'%s,%s'%(x,y),(x,y), font, 1,(255,0,0),2)

    cv2.imshow("Image window", cv_image)
    cv2.imshow("random", cv_image_copy)
    cv2.waitKey(0)


if __name__ == '__main__':
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    cv2.destroyAllWindows()
    print "Shutting down"
