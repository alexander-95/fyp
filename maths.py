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

#get the absolute difference between 2 values
def delta(x y):
    return abs(x-y)

t1 = 1
t2 = 2
t3 = 3
t4 = 4

d1 = 0
d2 = 0
d3 = 0
d4 = 0

b = px(80)
f = px(4)

A = (delta(t2, t1)*d2(d3-d1))-(delta(t3,t1)*d3*(d2-d1))
C = (delta(t2, t1)*d2*(d3-d1))-(delta(t4, t3)*d3*(d2-d4))

num = (A*b*(d2-d4))+(C*b*(d3-d1))
denom = (C*(delta(t2, t1)*(d3-d1)-delta(t3, t1)*(d2-d1))) + (A*(delta(t4, t3)*(d2-d4)-delta(t4, t2)*(d3-d4)))
Vy = num/denom

num = (f*b*(d2-d4)) - (delta(t4, t3)*f*Vy*(d2-d4)) + (delta(t4, t2)*f*Vy*(d3-d4))
denom = delta(t4, t2)*d2*(d3-d4) - delta(t4, t3)*d3*(d2-d4)
Vx = num/denom

#print 'height',length((460.0, 59.0), (484.0, 444.0))
#print 'px per mm', pixel_length(100.0, 200.0, 385.0, 4.0)
#print 'width',length((117.0, 299.0),(629.0, 291.0))
#print 'px per mm', pixel_length(100.0, 150.0, 512.0, 4.0)
