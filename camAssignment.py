import numpy as np
import cv2
import math

#returns rotational matrix from euler angles
def eulerToR((alpha, beta, gamma)):
    #alpha = math.radians(alpha)
    #beta = math.radians(beta)
    #gamma = math.radians(gamma)
    Rz = np.matrix(((math.cos(gamma), -math.sin(gamma), 0),
                    (math.sin(gamma), math.cos(gamma), 0),
                    (0,0,1)))

    Ry = np.matrix(((math.cos(beta), 0, math.sin(beta)),
                    (0, 1, 0),
                    (-math.sin(beta), 0, math.cos(beta))))

    Rx = np.matrix(((1, 0, 0),
                    (0, math.cos(alpha), -math.sin(alpha)),
                    (0, math.sin(alpha), math.cos(alpha))))

    R = Rx.dot(Ry).dot(Rz)
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

R = eulerToR((90, 0, 0))
print R
print ''
T = eulerToT((1, 2, 3, 90, 0, 0))
print T
print ''
R = expToR((90, 0, 0))

