#!/usr/bin/python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState

def callback(data):
  raw_input('hit anything to print joint state value')
  if 'arm_joint_1' in data.name:
    print data.position
  
          
def listener():
  rospy.init_node('listener', anonymous=True)
  rospy.Subscriber("joint_states", JointState, callback)
  rospy.spin()

if __name__ == '__main__':
  listener()
