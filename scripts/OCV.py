import cv2
import numpy as np
import pytesseract
from pytesseract import Output

ubiFoto='/home/parking/Desktop/raspberry_IoT_parking/scripts/captura.jpg'

class OpenCv(object):
    
    def captFoto():
        """
        En esta función se captura una foto
        """
        cap=cv2.VideoCapture(0)
        ret,frame=cap.read()
        cv2.imwrite(ubiFoto,frame)
        cap.release()
        print('foto capturada')
    
    def captVideo():
        """
        En esta función se captura un video
        """
        print('presionar q para salir')
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
        
    def captVideoTexto():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        while True:
            # Captura de cuadro por cuadro
            ret, cuadro = cap.read()
            d = pytesseract.image_to_data(cuadro, lang='spa', output_type=Output.DICT)
            cant_cajas = len(d['text'])
            for i in range(cant_cajas):
            # Procesar solo con nivel de confianza mayor a 60 %
                if int(d['conf'][i]) > 60:
                    (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    # no mostrar texto vacio
                    if text and text.strip() != "":
                        print(text)
                        cuadro = cv2.rectangle(cuadro, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cuadro = cv2.putText(cuadro, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
         
            # Abre ventana y muestra resultado
            cv2.imshow('cuadro', cuadro)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
         
        cap.release()
        cv2.destroyAllWindows() 
        
        
    
def main():
    #OpenCv.captVideoTexto()
    OpenCv.captFoto()
    #OpenCv.captVideo()

if __name__ == '__main__':
    main()