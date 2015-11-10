import numpy as np
import cv2
import math

def eulerToR((alpha, beta, gamma)):
    alpha = math.radians(alpha)
    beta = math.radians(beta)
    gamma = math.radians(gamma)
    #Rz = np.matrix('math.cos(gamma), (-1)*math.sin(gamma)), 0; math.sin(gamma), math.cos(gamma), 0; 0, 0, 1')
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
    print Rz
    print Ry
    print Rx
    print R


def expToR((w1, w2, w3)):
    print 'not yet implemented'

def eulerToT((X, Y, Z, w1, w2, w3)):
    print 'not yet implemented'

eulerToR((90, 0, 90))



