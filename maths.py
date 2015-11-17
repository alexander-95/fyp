import math

#get the length of a line
def length(p1,p2):
    x = (p2[0] - p1[0])
    y = (p2[1] - p1[1])
    length = math.sqrt(x*x + y*y)
    return length

#get the size of a pixel
def pixel_length(x1, y1, x2, f):
    return (x2*y1)/(x1*f)

#convert mm to px
def px(x):
    return x*192

#convert px to mm
def mm(x):
    return x/192

##############################################
# Mathematical equations for entity tracking #
##############################################

#get the absolute difference between 2 values
def delta(x, y):
    return float(abs(x-y))

#relative time between each photo
t1 = 1
t2 = 2
t3 = 3
t4 = 4

#x positions of entity
x1 = 323
x2 = 184
x3 = 442
x4 = 314

#y positions of entity
y1 = 75
y2 = 68
y3 = 53
y4 = 48

#disparities in x axis
d1 = delta(x1, 320)
d2 = delta(x2, 320)
d3 = delta(x3, 320)
d4 = delta(x4, 320)

#disparities in y axis
dz1 = delta(y1, 240)
dz2 = delta(y2, 240)
dz3 = delta(y3, 240)
dz4 = delta(y4, 240)

print dz1, dz2,dz3,dz4

b = px(80) #baseline
f = px(4.0)  #disparity

#some extra variables
z1 = x1*(dz1/f)
z2 = x2*(dz2/f)

Vz = (z2 - z1)/delta(t2, t1)

A = (delta(t2, t1)*d2*(d3-d1)) - (delta(t3, t1)*d3*(d2-d1))
C = (delta(t2, t1)*d2*(d3-d1)) - (delta(t4, t3)*d3*(d2-d4))

num = (A*b*(d2-d4))+(C*b*(d3-d1))
denom = (C*(delta(t2, t1)*(d3-d1)-delta(t3, t1)*(d2-d1))) + (A*(delta(t4, t3)*(d2-d4)-delta(t4, t2)*(d3-d4)))
Vy = float(num/denom)

num = (f*b*(d2-d4)) - (delta(t4, t3)*f*Vy*(d2-d4)) + (delta(t4, t2)*f*Vy*(d3-d4))
denom = delta(t4, t2)*d2*(d3-d4) - delta(t4, t3)*d3*(d2-d4)
Vx = float(num/denom)

X1 = (((-1)*b*f)/(d2-d1)) + (delta(t2, t1)*(f*Vy - Vx*d2))/(d2-d1)
Y1 = ((d1*delta(t2, t1)*Vy - d1*b)/(d2-d1)) - ((d1*d2*Vx*delta(t2, t1))/(f*(d2-d1)))
Z1 = X1-(dz1/f)

print mm(X1),mm(Y1),mm(Z1)

#print 'height',length((460.0, 59.0), (484.0, 444.0))
#print 'px per mm', pixel_length(100.0, 200.0, 385.0, 4.0)
#print 'width',length((117.0, 299.0),(629.0, 291.0))
#print 'px per mm', pixel_length(100.0, 150.0, 512.0, 4.0)