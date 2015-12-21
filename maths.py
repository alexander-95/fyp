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
    return x*222#192

#convert px to mm
def mm(x):
    return x/222

##############################################
# Mathematical equations for entity tracking #
##############################################

#get the absolute difference between 2 values
#def delta(x, y):
#    return float(abs(x-y))

def getLocation(l, r, f, b):
    x1 = l[0] #object as seen from the left camera
    y1 = l[1]
    x2 = r[0] #object as seen from the right camera
    y2 = r[1]
    d1 = x1 - 320
    dz = y1 - 240
    d2 = x2 - 320
    f = float(px(f))
    b = px(b)
    x = (f*b)/(d1-d2)
    y = (b*d1)/(d1-d2)
    z = x*(dz/f)

    return (mm(x),mm(y),mm(z))

def mathExample():
    #relative time between each photo
    t1 = 1.0
    t2 = 2.0
    t3 = 3.0
    t4 = 4.0

    #x positions of entity
    x1 = 99.0
    x2 = 388.0
    x3 = 256.0
    x4 = 487.0

    #y positions of entity
    y1 = 81.0
    y2 = 63.0
    y3 = 57.0
    y4 = 45.0

    #disparities in x axis
    d1 = 320 - x1
    d2 = 320 - x2
    d3 = 320 - x3
    d4 = 320 - x4
    
    #disparities in y axis
    dz1 = 240 - y1
    dz2 = 240 - y2
    dz3 = 240 - y3
    dz4 = 240 - y4

    print dz1, dz2,dz3,dz4

    b = px(80.0) #baseline
    f = float(px(4.0))  #focal length

    #some extra variables
    z1 = x1*(dz1/f)
    z2 = x2*(dz2/f)
    
    Vz = (z2 - z1)/(t2 - t1)

    A = ((t2 - t1)*d2*(d3-d1)) - ((t3 - t1)*d3*(d2-d1))
    C = ((t4 - t2)*d2*(d3-d4)) - ((t4 - t3)*d3*(d2-d4))

    num = (A*b*(d2-d4))+(C*b*(d3-d1))
    denom = (C*((t2 - t1)*(d3-d1)-(t3 - t1)*(d2-d1))) + (A*((t4 - t3)*(d2-d4)-(t4 - t2)*(d3-d4)))
    
    print 'num =',num
    print 'denom =', denom
    Vy = float(num)/denom

    num = (f*b*(d2-d4)) - ((t4 - t3)*f*Vy*(d2-d4)) + ((t4 - t2)*f*Vy*(d3-d4))
    denom = (t4 - t2)*d2*(d3-d4) - (t4 - t3)*d3*(d2-d4)
    print 'num =',num
    print 'denom =', denom
    Vx = float(num)/denom

    #position at time 1
    X1 = (((-1)*b*f)/(d2-d1)) + ((t2 - t1)*(f*Vy - Vx*d2))/(d2-d1)
    Y1 = ((d1*(t2 - t1)*Vy - d1*b)/(d2-d1)) - ((d1*d2*Vx*(t2 - t1))/(f*(d2-d1)))
    Z1 = X1*(dz1/f)

    #position at time 4
    X4 = (f*b/(d3-d4)) + (((t4 - t3)*(Vx*d3 - Vy*f))/(d3-d4))
    Y4 = (((b*d3)-(d4*(t4 - t3)*Vy))/(d3-d4)) + (((t4 - t3)*Vx*d4*d3)/(f*(d3-d4)))
    Z4 = X4*(dz4/f)

    xdiff = X4 - X1
    ydiff = Y4 - Y1
    zdiff = Z4 - Z1

    print 't1:',mm(X1), mm(Y1), mm(Z1)
    print 't4:',mm(X4), mm(Y4), mm(Z4)
    print 'diff:',mm(xdiff), mm(ydiff), mm(zdiff)
    #print 'height',length((460.0, 59.0), (484.0, 444.0))
    #print 'px per mm', pixel_length(100.0, 200.0, 385.0, 4.0)
    #print 'width',length((117.0, 299.0),(629.0, 291.0))
    #print 'px per mm', pixel_length(100.0, 150.0, 512.0, 4.0)

mathExample()
