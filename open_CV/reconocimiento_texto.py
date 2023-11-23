import cv2
import pytesseract
from pytesseract import Output

#cap=cv2.VideoCapture('/dev/video0',cv2.CAP_V4L
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
placa={'placa':' '}
while True:
    # captura de cuadro por cuadro
    ret, cuadro=cap.read()
    cuadro=cv2.resize(cuadro,(1200,720))
    cuadro=cv2.cvtColor(cuadro, cv2.COLOR_BGR2RGB)
    d=pytesseract.image_to_data(cuadro,lang='spa',output_type=Output.DICT)
    cant_cajas=len(d['text'])
    for i in range(cant_cajas):
        # procesar solo con nivel de confianza mayor a 60%
        if int(d['conf'][i])>60:
            (text,x,y,w,h)=(d['text'][i],d['left'][i],d['top'][i],d['width'][i],d['height'][i])
            # no mostrar texto vacio
            
            placa['placa']=text
            if text and text.strip()!="":
                cuadro=cv2.rectangle(cuadro,(x,y),(x+w,y+h),(0,255,0),5)
                cuadro=cv2.putText(cuadro,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255),3)
            if(placa['placa']=='PDK-9493'):
                print('-------------------------------')
                print('        PLACA RECONOCIDA       ')
                print('-------------------------------')
            #print(placa['placa'])
            #print(f'longitud de texto: ', len(text))
            
    # muestra resultado
    #print(cuadro.shape)
    
    cv2.imshow('cuadro',cuadro)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()