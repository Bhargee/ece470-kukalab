#!/usr/bin/python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from brics_actuator.msg import *
from inverse import *


numberOfJoints = 5
armPublisher = rospy.Publisher("arm_1/arm_controller/position_command", 
    JointPositions)
gripperPublisher = rospy.Publisher("arm_1/gripper_controller/position_command", JointPositions)
default_pos = [(2*3.14159)-.0114, 1.166,-2.4551, 2.0745,0]

def sender():
  rospy.init_node('sender', anonymous=True)
  rospy.sleep(1)
  while True:
    arm_pos = raw_input()
    if (arm_pos is 'q'):
      break
    vals = map(float, arm_pos.split(','))
    print 'recieved %s' % str(vals)
    try:
      pos = inverseK(vals[0], vals[1], vals[2])
      gripOpen()
      moveArm(pos)
      gripClose()
      moveArm(inverseK(0,0,200))
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
    msg.positions.append(joint)
  return msg

def createGripperPositionCmd(newPosition):
  msg = JointPositions()
  left = JointValue()
  right = JointValue()
  left.unit = "m"
  right.unit = "m"
  left.timeStamp = right.timeStamp = rospy.Time.now()
  left.value = right.value = newPosition
  left.joint_uri = "gripper_finger_joint_l"
  msg.positions.append(left)
  right.joint_uri = "gripper_finger_joint_r"
  msg.positions.append(right)
  return msg

def moveArm(angles):
  msg = createArmPositionCmd(angles)
  armPublisher.publish(msg)
  rospy.sleep(5)

def gripOpen():
    msg = createGripperPositionCmd(0.011)
    gripperPublisher.publish(msg)
    rospy.sleep(3)
   # msg = createGripperPositionCmd(0)
   # gripperPublisher.publish(msg)

def gripClose():
  msg = createGripperPositionCmd(0.001)
  gripperPublisher.publish(msg)
  rospy.sleep(3)

if __name__ == '__main__':
  sender()
  rospy.spin()
