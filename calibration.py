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
#cap.open('http://192.168.0.5:8080/video?.mjpeg')

#axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

camera = []

#while (True):
while (False):
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    #capture a frame
    ret, img = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (HEIGHT,WIDTH),None)
    # If found, add object points, image points (after refining them)

    if ret == True:
        #corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        objpoints.append(objp)
        imgpoints.append(corners)
        # Draw and display the corners
        cv2.drawChessboardCorners(img, (HEIGHT,WIDTH), corners,ret)
        #intrinsic matrix, distortion coefficients,
        #rodrigues rotation vectors, translation vectors
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            print mtx
            #print corners
            camera.append(mtx)
            cv2.imwrite('img.png', gray)
    cv2.imshow('img',img)
    #print 'b',x,y,w,h
    if cv2.waitKey(1) & 0xFF == ord('q'):
        num = float(len(camera))
        camera = sum(camera)
        camera = camera/num
        print "matrix estimation:",camera
        print mtx
        break

#get the corners of the chessboard image
img = cv2.imread('pattern.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, corners = cv2.findChessboardCorners(gray, (HEIGHT, WIDTH), None)
if ret == False:
    print 'found corners in image'
    print corners
    cv2.imshow('checkerboard', img)

#overlay an image on the checkerboard
while True:
    #img = cv2.imread('img.png')
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners2 = cv2.findChessboardCorners(gray, (HEIGHT, WIDTH), None)
    if ret == True:
        #print 'found corners in photo'
        #print corners2
        #cv2.imshow('image', img)#color camera feed

        H,matches = cv2.findHomography(corners,corners2)
        img3 = cv2.imread('img3.png')
        warp = cv2.warpPerspective(img3, H, (640, 480))
        
        warpgray = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(warpgray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        #cv2.imshow('mask inv', mask_inv)
        
        img[:,:,0] = cv2.bitwise_and(img[:,:,0],mask_inv)#blue
        img[:,:,1] = cv2.bitwise_and(img[:,:,1],mask_inv)#green
        img[:,:,2] = cv2.bitwise_and(img[:,:,2],mask_inv)#red
        img = cv2.add(img, warp)
        cv2.imshow('image', img)#color camera feed

        gray = cv2.bitwise_and(gray,mask_inv)
        #cv2.imshow('grayscale', gray)#grayscale camera feed

        #cv2.imshow('frame', warp)#final product
    #cv2.imwrite('img2.png',warp)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

# release everything
cap.release()
cv2.destroyAllWindows()
