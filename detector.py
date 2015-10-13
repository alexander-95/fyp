import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np
from time import time
#before = cv2.imread('before.png')
#after = cv2.imread('after.png')
#diff = cv2.absdiff(before, after)
#cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY, diff)

diff = cv2.imread('blob.bmp')
diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
detector = cv2.SimpleBlobDetector()
keypoints = detector.detect(diff)
#print "keypoints", keypoints
diff_with_keypoints = cv2.drawKeypoints(diff, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("Keypoints", diff_with_keypoints)
cv2.waitKey(0)

#cv2.imwrite('diff.png',diff)
