import cv2
import pytesseract
import re
from pytesseract import Output


def verificar_placa(placa):
    # Definimos una expresión regular para verificar el formato de la placa
    patron = r'^[A-Z]{3}-\d{3}$'
    
    # Utilizamos la función match() de la librería re para buscar el patrón en la placa
    if re.match(patron, placa):
        return True
    else:
        return False
    
    
 
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
                print("texto: ",text,"Cantidad letras: ",len(text))
                if verificar_placa(text):
                    break
                cuadro = cv2.rectangle(cuadro, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cuadro = cv2.putText(cuadro, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
    
    if verificar_placa(text):
        print("La placa es válida.")
        break    
    # Abre ventana y muestra resultado
    cv2.imshow('cuadro', cuadro)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


print("la placa reconocida es: ",text) 
cap.release()
cv2.destroyAllWindows()


