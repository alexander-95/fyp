import cv2

cap = cv2.VideoCapture(0)

#set a new resolution
cap.set(3,640)
cap.set(4,480)

#reduce the color saturation
cap.set(12,0.5)

#change the brightness
cap.set(10,0.5)

#bump up the contrast
cap.set(11,0.5)

ret, oldframe = cap.read()
oldframe = cv2.cvtColor(oldframe, cv2.COLOR_BGR2GRAY)

while(True):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(frame, oldframe)
    cv2.threshold(diff, 31, 255, cv2.THRESH_BINARY, diff)
    cv2.imshow('frame', diff)
    
    oldframe = frame

    #if the 'c' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite('image.png', diff)
        break

cap.release()
cv2.destroyAllWindows()
