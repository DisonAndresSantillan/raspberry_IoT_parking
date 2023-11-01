import cv2
import numpy as np

#cam=cv2.VideoCapture('/dev/video0',cv2.CAP_V4L)
cam=cv2.VideoCapture(0)
while True:
    ret,frame=cam.read()
    frame=cv2.resize(frame,(1200,900))
    color=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("Preview",color)
    
    if cv2.waitKey(1)&0xFF==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()