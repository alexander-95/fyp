""" Example of using OpenCV API to detect and draw checkerboard pattern"""

import numpy as np
import cv2

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

WIDTH = 6
HEIGHT = 9

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((WIDTH*HEIGHT,3), np.float32)
objp[:,:2] = np.mgrid[0:HEIGHT,0:WIDTH].T.reshape(-1,2)

cap = cv2.VideoCapture(0)



while (True):
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        #capture a frame
        ret, img = cap.read()

        # OUr operations on the frame come here
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (HEIGHT,WIDTH),None)
        imgpoints.append(corners)
        objpoints.append(objp)
        # If found, add object points, image points (after refining them)
        if ret == True:
            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            print 'found checkerboard'

            # Draw and display the corners
            cv2.drawChessboardCorners(img, (HEIGHT,WIDTH), corners,ret)
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
            print 'matrix =', mtx

        cv2.imshow('img',img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# release everything
cap.release()
cv2.destroyAllWindows()
