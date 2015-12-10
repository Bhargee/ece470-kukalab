import math
import cmath

def inverseK(xw,yw,zw, thp):
  x0 = xw
  y0 = yw
  z0 = zw
  th_p = thp
  th_r = 0

  th1 = math.atan2(y0,x0)

  x_wrist = x0-217.5*math.sin(th_p)*math.cos(th1)
  y_wrist = y0-217.5*math.sin(th_p)*math.cos(math.pi/2-th1)
  z_wrist = z0+217.5*math.cos(th_p)

  D = ((x_wrist-33*math.cos(th1))**2+(y_wrist-33*math.sin(th1))**2+(z_wrist-147)**2-155**2-135**2)/(2*155*135)
  if D>1:
    print('Wrong th_p')
    raise ValueError()

  th3 = math.atan2(-cmath.sqrt(1-D**2).real,D)
  th2 = math.atan2(z_wrist-147,math.sqrt((x_wrist-33*math.cos(th1))**2+(y_wrist-33*math.sin(th1))**2))-math.atan2(135*math.sin(th3),155+135*math.cos(th3))
  q4 = th_p - th3-th2
  th5 = th_r

  th1 = 2.9496 - th1
  th2 = 2.617 - th2
  th3 = -2.5831 -th3
  q4 = 1.7-q4+math.pi/2
  th5 = 2.9322 - th5

  if th1 <= .0115 or th1 >= 5.84:
    print "th1 oob"
    raise ValueError()
  elif th2 <= 0 or th2 >= 2.617:
    print "th2 oob"
    raise ValueError()
  elif th3 <= -5.183 or th3 >= 0:
    print "th3 oob"
    raise ValueError()
  elif q4 <= .1 or q4 >= 3.5:
    print "th4 oob"
    raise ValueError()
  elif th5 <= 0 or th5 >= 5.866:
    print "th5 oob"
    raise ValueError()
  return [th1,th2,th3,q4,th5]
