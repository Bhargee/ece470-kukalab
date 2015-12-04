import numpy

def inverse(x,y,z,pitch,roll):
  theta_1 = numpy.arctan2(y,x)+numpy.pi
  theta_5 = roll
	
  print theta_1, theta_5

c = "x"

while(c!="n"):
  x = input("x:")
  y = input("y:")
  z = input("z:")
  p = input("p:")
  r = input("r:")
  inverse(x,y,z,p,r)

  c = input("c:")

