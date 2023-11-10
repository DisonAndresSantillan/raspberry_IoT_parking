import cv2
#cap=cv2.VideoCapture('/dev/video0',cv2.CAP_V4L2)
cap=cv2.VideoCapture(0)
ret,frame=cap.read()
cv2.imwrite('/home/parking/Desktop/raspberry_IoT_parking/antecedentes/nuevo.jpg',frame)
cap.release()
