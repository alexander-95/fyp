import cv2

img = cv2.imread('blob.bmp',cv2.CV_LOAD_IMAGE_GRAYSCALE)
_,img = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
#h, w = img.shape[:2]

#blob detection with center points
contours, hierarchy = cv2.findContours( img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
moments  = [cv2.moments(cnt) for cnt in contours]
# Nota Bene: I rounded the centroids to integer.
centroids = [( int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ) for m in moments]
print "centroids", centroids

for c in centroids:
    # I draw a black little empty circle in the centroid position
    cv2.circle(img,c,5,(0,0,0))
            
cv2.imshow('image', img)
0xFF & cv2.waitKey()
cv2.destroyAllWindows()
