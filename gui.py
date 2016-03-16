import Tkinter as tk
import cv2
import threading

threshVal = 40

def change_value(val):
    global threshVal
    threshVal = val

def sliders():
    global threshVal
    master = tk.Tk()
    w1 = tk.Scale(master, from_=0, to=255, length=250, label='threshold', command=change_value)
    w1.pack()
    tk.mainloop()


def camera():
    global threshVal
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.threshold(frame, float(threshVal), 255, cv2.THRESH_BINARY, frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break
    cap.release()
    cv2.destroyAllWindows()

t = threading.Thread(target=sliders)
t.start()

t = threading.Thread(target=camera)
t.start()
