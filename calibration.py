import numpy as np
import cv2

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

WIDTH = 6
HEIGHT = 9

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((WIDTH*HEIGHT,3), np.float32)
objp[:,:2] = np.mgrid[0:HEIGHT,0:WIDTH].T.reshape(-1,2)

cap = cv2.VideoCapture()
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
if ret == True:
    print 'found corners in image'
    print corners
    cv2.imshow('checkerboard', img)

img = cv2.imread('img.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, corners2 = cv2.findChessboardCorners(gray, (HEIGHT, WIDTH), None)
if ret == True:
    print 'found corners in photo'
    print corners2
    cv2.imshow('image', img)

H,matches = cv2.findHomography(corners,corners2)
img3 = cv2.imread('img3.png')
warp = cv2.warpPerspective(img3, H, (640, 480))
cv2.imwrite('img2.png',warp)


#data = np.concatenate((np.matrix(corners), np.matrix(corners2)), axis=1)

#print 'data =',data
#print np.shape(data)
#A = np.empty([54*2,9])
#A[::2] = np.concatenate((-data[:,0:2],np.matrix([[-1,0,0,0]]*54),np.multiply(np.matrix(data[::,2:3]),np.matrix(data[::,0:2])),np.matrix(-data[::,2:3])),axis=1)
#A[1::2] = np.concatenate((np.matrix([[0,0,0]]*54),-data[:,0:2],np.matrix([[-1]]*54),np.multiply(np.matrix(-data[::,3:4]),np.matrix(data[::,0:2])), np.matrix(-data[::,3:4])),axis=1)
            
#print A
#A = A.T.dot(A)
#eigenvalue, eigenvector = np.linalg.eig(A)
#e = eigenvector[:,8]
#e = e.reshape(3,3)
#print e
print 'img=',img
print np.shape(img)

#img2 = np.zeros((480, 640, 3))
#img3 = cv2.imread('img3.png')

#cv2.imwrite('img2.png',img2)



# release everything
cap.release()
cv2.destroyAllWindows()
