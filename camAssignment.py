import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

#returns rotational matrix from euler angles
def eulerToR((alpha, beta, gamma)):
    Rz = np.matrix(((math.cos(gamma), -math.sin(gamma), 0),
                    (math.sin(gamma), math.cos(gamma), 0),
                    (0,0,1)))

    Ry = np.matrix(((math.cos(beta), 0, math.sin(beta)),
                    (0, 1, 0),
                    (-math.sin(beta), 0, math.cos(beta))))

    Rx = np.matrix(((1, 0, 0),
                    (0, math.cos(alpha), -math.sin(alpha)),
                    (0, math.sin(alpha), math.cos(alpha))))

    R = (Rz.dot(Ry)).dot(Rx)
    return R

#returns rotational matrix from exponential coordinates
def expToR((w1, w2, w3)):
    wh = np.matrix(((0, -w3,w2 ),(w3, 0, -w1),(-w2, w1, 0)))

    I = np.matrix(((1, 0, 0),
                    (0, 1, 0),
                    (0, 0, 1)))

    length = np.power(w1*w1 + w2*w2 + w3*w3,1/3.0)
    R = I + wh*math.sin(length)/length + (wh*wh*(1 - math.cos(length)))/(length*length)
    return R

#returns transformation matrix
def eulerToT((X, Y, Z, alpha, beta, gamma)):
    r = eulerToR((alpha, beta, gamma))
    T = np.matrix(((r.item(0,0), r.item(0,1), r.item(0,2), X),
                    (r.item(1,0), r.item(1,1), r.item(1,2), Y),
                    (r.item(2,0), r.item(2,1), r.item(2,2), Z),
                    (0, 0, 0, 1)))
    return T

#returns transformation matrix
def expToT((X, Y, Z, w1, w2, w3)):
     r = expToR((w1, w2, w3))
     T = np.matrix(((r.item(0,0), r.item(0,1), r.item(0,2), X),
                    (r.item(1,0), r.item(1,1), r.item(1,2), Y),
                    (r.item(2,0), r.item(2,1), r.item(2,2), Z),
                    (0, 0, 0, 1)))
     return T

#produces a k matrix from  intrinsic parameters
def intrinsicToK(fx, fy, x0, y0, s):
    K = np.matrix(((fx, s, x0, 0),
                    (0, fy, y0, 0),
                    (0, 0, 1, 0)))
    return K

def simulateCamera():
    #Camera = eulerToT((0, 0, 2, np.pi*1.0, np.pi*-0.4, np.pi*0.5))#yaw, roll, pitch
    Camera = eulerToT((0, 0, 2, np.pi*0.5, np.pi*-0.0, np.pi*0.0))#yaw, roll, pitch
    Camera =Camera.dot(eulerToT((0, 0, 0, np.pi*0.0, np.pi*0.0, np.pi*0.5)))#yaw, roll, pitch
    
    p = np.matrix(((80, 1, 80, 1, 80, 1),
                    (-1, -1, 0, 0, 1, 1),
                    (0, 0, 0, 0, 0, 0),
                    (1,1,1,1,1,1)))
    K = intrinsicToK(2, 2, 0, 0, 0)
    #K = K.eulerToR()
    #print p
    Camera = K.dot(Camera)
    print Camera
    p = Camera.dot(p)
    #print p
    for i in range(3):
        x1 = float(p.item(0, i*2))/p.item(2, i*2)
        x2 = float(p.item(0, i*2+1))/p.item(2, i*2+1)
        y1 = float(p.item(1, i*2))/p.item(2, i*2)
        y2 = float(p.item(1, i*2+1))/p.item(2, i*2+1)
        #print x1,',',y1,x2,',',y2
        plt.plot((x1, x2),(y1, y2), 'k-')# (p.item(2, i*2), p.item(2, i*2+1)), 'k-')

    plt.show()

def loadCalibData(datafile):
    data = np.loadtxt(datafile)
    
    a = np.matrix((data))

    first = True
    for line in data:
        X = line[0]
        Y = line[1]
        Z = line[2]
        x = line[3]
        y = line[4]

        if first:
            #A = np.matrix(((f*X, f*Y, f*Z, 0, 0, 0, x*X, x*Y, x*Z, f, 0, x),
            #                (0, 0, 0, f*X, f*Y, f*Z, y*X, y*Y, y*Z, 0, f, y)))
            A = np.matrix(((X, Y, Z, 1, 0, 0, 0, 0, -x*X, -x*Y, -x*Z, -x),
                            (0, 0, 0, 0, X, Y, Z, 1, -y*X, -y*Y, -y*Z, -y)))
            first = False
        else:
            #newrow = [f*X, f*Y, f*Z, 0, 0, 0, x*X, x*Y, x*Z, f, 0, x]
            newrow = [X, Y, Z, 1, 0, 0, 0, 0, -x*X, -x*Y, -x*Z, -x]
            #print newrow
            A = np.vstack([A, newrow])
            #newrow = [0, 0, 0, f*X, f*Y, f*Z, y*X, y*Y, y*Z, 0, f, y]
            newrow = [0, 0, 0, 0, X, Y, Z, 1, -y*X, -y*Y, -y*Z, -y]
            #print newrow
            A = np.vstack([A, newrow])
        
    A = (A.T).dot(A)
    eigenvalue, eigenvector = np.linalg.eig(A)
    print 'eigenvalues = ',eigenvalue
    print 'eigenvectors =', eigenvector
    e = eigenvector[np.argmin(eigenvalue)]
    e = eigenvector[10]
    #print eigenvector
    #print e
    camera = np.matrix(((e.item(0), e.item(1), e.item(2),e.item(9)),
                        (e.item(3), e.item(4), e.item(5),e.item(10)),
                        (e.item(6), e.item(7), e.item(8),e.item(11)),
                        (0,0,0,1)))
    #print camera

    fig = plt.figure()
    ax = fig.gca(projection="3d")
    ax.plot(data[:,0], data[:,1], data[:,2],'k.')

    fig = plt.figure()
    ax = fig.gca()
    ax.plot(data[:,3], data[:,4],'r.')
    
    for line in data:
        X = line[0]
        Y = line[1]
        Z = line[2]
        vector = np.matrix(((X),(Y),(Z),(1)))
        #print vector.T
        #vector = camera.dot(vector.T)
        vector = camera.T.dot(vector.T)
        #print vector
        #print vector.item(0), vector.item(1), vector.item(2)
        ax.plot(vector.item(0)/vector.item(2),vector.item(1)/vector.item(2), 'g.')
    plt.show()

loadCalibData('data.txt')

#R = eulerToR((90, 0, 0))
#print R
#print ''
#T = eulerToT((1, 2, 3, 90, 0, 0))
#print T
#print ''
#R = expToR((90, 0, 0))

#simulateCamera()

