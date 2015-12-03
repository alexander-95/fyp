import cv2

cap = cv2.VideoCapture()
cap.open('http://192.168.1.107:8080/video?.mjpeg')

#set a new resolution
cap.set(3,640)
cap.set(4,480)

#reduce the color saturation
cap.set(12,0.5)

#change the brightness
cap.set(10,0.5)

#bump up the contrast
cap.set(11,0.5)

while(True):
    ret, frame = cap.read()
    
    cv2.imshow('frame', frame)
    #if the 'c' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite('image.png', diff)
        break

cap.release()
cv2.destroyAllWindows()
