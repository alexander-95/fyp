import math
import numpy as np

#convert mm to px
def px(x):
    #return x*222#192
    return x*357

#convert px to mm
def mm(x):
    #return x/222
    return x/357

##############################################
# Mathematical equations for entity tracking #
##############################################

#gets the location using synchronous stereo vision
def getLocation(l, r, f, b):
    res = [1280,960]
    x1 = l[0] #object as seen from the left camera
    y1 = l[1]
    x2 = r[0] #object as seen from the right camera
    y2 = r[1]
    d1 = x1 - (res[0]/2)
    dz = y1 - (res[1]/2)
    d2 = x2 - (res[0]/2)
    f = float(px(f))
    b = px(b)
    if d1 != d2:
        x = (f*b)/(d1-d2)
        y = (b*d1)/(d1-d2)
    else:
        x = 0
        y = 0
    z = x*(dz/f)

    return (mm(x),mm(y),mm(z))

#gets the location using asynchronous stereo vision

def getMetrics(l1,r1,l2,r2,t,f,b):
    #res = [1280,960]
    res = [640, 480]

    #relative time between each photo
    t1 = t[0]
    t2 = t[1]
    t3 = t[2]
    t4 = t[3]

    #x positions of entity
    x1 = l1[0]
    x2 = r1[0]
    x3 = l2[0]
    x4 = r2[0]

    #y positions of entity
    y1 = l1[1]
    y2 = r1[1]
    y3 = l2[1]
    y4 = r2[1]

    #disparities in x axis
    d1 = (res[0]/2) - x1
    d2 = (res[0]/2) - x2
    d3 = (res[0]/2) - x3
    d4 = (res[0]/2) - x4
    
    #disparities in y axis
    dz1 = (res[1]/2) - y1
    dz2 = (res[1]/2) - y2
    dz3 = (res[1]/2) - y3
    dz4 = (res[1]/2) - y4

    #print dz1, dz2,dz3,dz4

    b = float(px(b)) #baseline
    f = float(px(f))  #focal length

    #some extra variables
    z1 = x1*(dz1/f)
    z2 = x2*(dz2/f)
    
    Vz = (z2 - z1)/(t2 - t1)

    A = ((t2 - t1)*d2*(d3-d1)) - ((t3 - t1)*d3*(d2-d1))
    C = ((t4 - t2)*d2*(d2-d4)) - ((t4 - t3)*d3*(d3-d4))

    num = (A*b*(d2-d4))+(C*b*(d3-d1))
    denom = (C*((t2 - t1)*(d3-d1)-(t3 - t1)*(d2-d1))) + (A*((t4 - t3)*(d2-d4)-(t4 - t2)*(d3-d4)))
    
    #print 'num =', num
    #print 'denom =', denom
    if denom !=0:
        Vy = float(num)/denom
    else:
        Vy = 0
        print 'vy=0'
    num = (f*b*(d2-d4)) - ((t4 - t3)*f*Vy*(d2-d4)) + ((t4 - t2)*f*Vy*(d3-d4))
    denom = (t4 - t2)*d2*(d3-d4) - (t4 - t3)*d3*(d2-d4)
    #print 'num =',num
    #print 'denom =', denom
    if denom!=0:
        Vx = float(num)/denom
    else:
        Vx = 0
        print 'vx=0'
    #position at time 1
    X1 = (((-1)*b*f)/(d2-d1)) + ((t2 - t1)*(f*Vy - Vx*d2))/(d2-d1)
    X1*=-1
    Y1 = ( ((d1*(t2 - t1)*Vy) - d1*b)/(d2-d1)) - ((d1*d2*Vx*(t2 - t1))/(f*(d2-d1)))
    Z1 = X1*(dz1/f)

    #position at time 4
    X4 = (f*b/(d3-d4)) + (((t4 - t3)*(Vx*d3 - Vy*f))/(d3-d4))
    X4*=-1
    Y4 = (((b*d3)-(d4*(t4 - t3)*Vy))/(d3-d4)) + (((t4 - t3)*Vx*d4*d3)/(f*(d3-d4)))
    Z4 = X4*(dz4/f)

    xdiff = X4 - X1
    ydiff = Y4 - Y1
    zdiff = Z4 - Z1

    v = np.power(np.power(xdiff, 3) + np.power(ydiff, 3) + np.power(ydiff, 3), 1/3.0)
    v*=(t[3]-t[0])
    print "v:",mm(v)

    print 't1:',mm(X1), mm(Y1), mm(Z1)
    print 't4:',mm(X4), mm(Y4), mm(Z4)
    #print 'diff:',mm(xdiff), mm(ydiff), mm(zdiff)
    #print 'height',length((460.0, 59.0), (484.0, 444.0))
    #print 'px per mm', pixel_length(100.0, 200.0, 385.0, 4.0)
    #print 'width',length((117.0, 299.0),(629.0, 291.0))
    #print 'px per mm', pixel_length(100.0, 150.0, 512.0, 4.0)
    return (mm(X1), mm(Y1), mm(Z1))

#new projective geometry method for getting location
def getPosition(l1, l2, r1, r2, t, f, res, c):
    c1 = [659, 366]
    c2 = [633, 332]

    X1 = l1[0] - c1[0]#(res[0]/2)
    X2 = l2[0] - c1[0]#(res[0]/2)
    X3 = r1[0] - c2[0]#(res[0]/2)
    X4 = r2[0] - c2[0]#(res[0]/2)

    Y1 = l1[1] - c1[1]#(res[1]/2)
    Y2 = l2[1] - c1[1]#(res[1]/2)
    Y3 = r1[1] - c2[1]#(res[1]/2)
    Y4 = r2[1] - c2[1]#(res[1]/2)

    Xc = px(c[0])
    Yc = px(c[1])
    Zc = px(c[2])

    f = px(float(f))

    A = Y2 - Y1
    B = X1 - X2
    C = (X2*Y1 - X1*Y2)/f
    D = (Y4 - Y3)
    E = (X3 - X4)
    F = ((X4*Y3 - X3*Y4)/f)
    G = (D*Xc + E*Yc + F*Zc)
    
    #position at t1
    z1 = (f*B*G)/((-X1*(E*A - B*D))-(f*(E*C - B*F)))
    y1 = -Y1*z1/f
    x1 = X1*z1/f
    print 'position1:', mm(x1), mm(y1), mm(z1)

    #position at t2
    z2 = (f*B*G)/((-X2*(E*A - B*D))-(f*(E*C - B*F)))
    y2 = -Y2*z2/f
    x2 = X2*z2/f
    print 'position2:',mm(x2),mm(y2), mm(z2)
    
    #overall velocity
    v = (((x2 - x1)**2) + ((y2 - y1)**2) + ((z2 - z1)**2))**(1/2.0)
    v/=float(t[1] - t[0])
    print 'velocity:',mm(v)

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
    C = ((t4 - t2)*d2*(d2-d4)) - ((t4 - t3)*d3*(d3-d4))

    num = (A*b*(d2-d4))+(C*b*(d3-d1))
    denom = (C*((t2 - t1)*(d3-d1)-(t3 - t1)*(d2-d1))) + (A*((t4 - t3)*(d2-d4)-(t4 - t2)*(d3-d4)))
    
    #print 'num =', num
    #print 'denom =', denom
    Vy = float(num)/denom

    num = (f*b*(d2-d4)) - ((t4 - t3)*f*Vy*(d2-d4)) + ((t4 - t2)*f*Vy*(d3-d4))
    denom = (t4 - t2)*d2*(d3-d4) - (t4 - t3)*d3*(d2-d4)
    #print 'num =',num
    #print 'denom =', denom
    Vx = float(num)/denom

    #position at time 1
    X1 = (((-1)*b*f)/(d2-d1)) + ((t2 - t1)*(f*Vy - Vx*d2))/(d2-d1)
    Y1 = ( ((d1*(t2 - t1)*Vy) - d1*b)/(d2-d1)) - ((d1*d2*Vx*(t2 - t1))/(f*(d2-d1)))
    Z1 = x1*(dz1/f)

    #position at time 4
    X4 = (f*b/(d3-d4)) + (((t4 - t3)*(Vx*d3 - Vy*f))/(d3-d4))
    Y4 = (((b*d3)-(d4*(t4 - t3)*Vy))/(d3-d4)) + (((t4 - t3)*Vx*d4*d3)/(f*(d3-d4)))
    Z4 = x4*(dz4/f)

    xdiff = X4 - X1
    ydiff = Y4 - Y1
    zdiff = Z4 - Z1

    print 't1:',mm(X1), mm(Y1), mm(Z1)
    print 't4:',mm(X4), mm(Y4), mm(Z4)
    #print 'diff:',mm(xdiff), mm(ydiff), mm(zdiff)
    #print 'height',length((460.0, 59.0), (484.0, 444.0))
    #print 'px per mm', pixel_length(100.0, 200.0, 385.0, 4.0)
    #print 'width',length((117.0, 299.0),(629.0, 291.0))
    #print 'px per mm', pixel_length(100.0, 150.0, 512.0, 4.0)

#mathExample()
