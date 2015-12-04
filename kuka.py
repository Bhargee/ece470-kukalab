#!/usr/bin/python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from brics_actuator.msg import *

numberOfJoints = 5
armPublisher = rospy.Publisher("arm_1/arm_controller/position_command", 
    JointPositions)
default_pos = [2.95,2.6,-2.44,1.73,2.95]

def sender():
  rospy.init_node('sender', anonymous=True)
  rospy.sleep(1)
  while True:
    arm_pos = raw_input()
    if (arm_pos is 'q'):
      break
    try:
      moveArm(map(float, arm_pos.split(',')))
    except ValueError as e:
      print(e)
      continue

def createArmPositionCmd(newPositions):
  if len(newPositions) < numberOfJoints:
    return None

  msg = JointPositions()
  for i in xrange(numberOfJoints):
    joint = JointValue()
    joint.timeStamp = rospy.Time.now()
    joint.value = newPositions[i]
    joint.unit = "rad"
    joint.joint_uri = ("arm_joint_" + str(i+1))
    print(joint.joint_uri)
    msg.positions.append(joint)  

  print msg
  return msg

def moveArm(angles):
  msg = createArmPositionCmd(angles)
  armPublisher.publish(msg)
  rospy.sleep(5)

if __name__ == '__main__':
  sender()
  rospy.spin()
