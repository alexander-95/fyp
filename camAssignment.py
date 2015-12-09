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
        plt.plot((x1, x2),(y1, y2), 'k-')

    plt.show()

def calibrateCamera3D(datafile):
    data = np.loadtxt(datafile)

    #new hip way of creating matrix
    A = np.empty([491*2,12])
    A[::2] = np.concatenate((data[:,0:3],np.matrix([[1,0,0,0,0]]*491),np.multiply(np.matrix(-data[::,3:4]),np.matrix(data[::,0:3])),np.matrix(-data[::,3:4])),axis=1)
    A[1::2] = np.concatenate((np.matrix([[0,0,0,0]]*491),data[:,0:3],np.matrix([[1]]*491),np.multiply(np.matrix(-data[::,4:5]),np.matrix(data[::,0:3])), np.matrix(-data[::,4:5])),axis=1)
    
    A = (A.T).dot(A)
    eigenvalue, eigenvector = np.linalg.eig(A)
    e = eigenvector[:,11]
    camera = e.reshape((3,4))
    return camera

def visualiseCameraCalibration3D(datafile, P):
    data = np.loadtxt(datafile)

    #2D plot
    fig = plt.figure()
    ax = fig.gca()
    ax.plot(data[:,3], data[:,4],'r.')
    
    points = np.concatenate((data[::,0:3],np.matrix([[1]]*491)),axis=1).T
    points = P.dot(points)
    points = np.concatenate((np.divide(points[0:1,:],points[2:3,:]),np.divide(points[1:2,:],points[2:3,:])),axis=0)
    ax.plot(points[0,:], points[1,:], 'b.')
    #ax.plot(np.divide(points[0:1,:],points[2:3,:]),np.divide(points[1:2,:],points[2:3,:]), 'g.')
    plt.show()

def evaluateCameraCalibration3D(datafile, P):
    data = np.loadtxt(datafile)
    points = np.concatenate((data[::,0:3],np.matrix([[1]]*491)),axis=1).T
    points = P.dot(points)
    points = np.concatenate((np.divide(points[0:1,:],points[2:3,:]),np.divide(points[1:2,:],points[2:3,:])),axis=0)
    diff = np.subtract(data[:,3:5], points.T) 
    square = np.multiply(diff, diff)
    dist = np.add(square[:,0], square[:,1])
    dist = np.sqrt(dist)
    mean = np.mean(dist)
    variance = np.var(dist)
    maximum = np.amax(dist)
    minimum = np.amin(dist)
    print 'mean =',mean
    print 'variance =',variance
    print 'max =',maximum
    print 'min =',minimum

simulateCamera()
P = calibrateCamera3D('data.txt')
visualiseCameraCalibration3D('data.txt', P)
evaluateCameraCalibration3D('data.txt', P)
