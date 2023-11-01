import cv2
#cap=cv2.VideoCapture('/dev/video0',cv2.CAP_V4L2)
cap=cv2.VideoCapture(0)
ret,frame=cap.read()
cv2.imwrite('/home/diartech/Desktop/antecedentes/nuevo.jpg',frame)
cap.release()
