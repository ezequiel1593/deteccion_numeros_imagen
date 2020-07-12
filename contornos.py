import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

#-----------Lectura de imagen previamente mejorada en Paint, copia y transformación a escala de grises

image= cv2.imread('C:\\Users\\Ezequiel\\Desktop\\proyecto\\planillas_y_resultados\\mejorado.png')
original=image.copy()
gray=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
threshold_aplicado,thresholded_image=cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

#-----------Detección de contornos (cnts)

cnts=cv2.findContours(thresholded_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=cnts[0] if len(cnts) == 2 else cnts[1] #(findContours devuelve contours y hierarchy)

#-----------Si longitud de contorno es igual o mayor a 4, se guarda en la lista 'imagenes' (pequeño ahorro en la corrección de los píxeles de la imagen)
imagenes=[]
for c in cnts:
    if len(c)>3:
        imagenes.append(c)

#-----------'limites' es una lista que marca minimo y maximo en el eje x de las columnas con datos. Por lo tanto, cada 'lim' representa una columna de las 15 que hay.

ROI_number=0
limites=[(0,60),(60,135),(135,210),(210,285),(285,360),(360,435),(435,505),(505,580),(580,650),(650,725),(725,795),(795,870),(870,940),(940,1010),(1010,1074)]
for lim in limites:
    columna=[]
    for l,c in zip(range(len(imagenes)),imagenes):
        ejex=[imagenes[l][i][0][0] for i in range(len(c))]
        minimo_x=min(ejex)
        ejey=[imagenes[l][i][0][1] for i in range(len(c))]
        minimo_y=min(ejey)
        if minimo_x>lim[0] and minimo_x<lim[1]:
            coordenadas_minimas=[minimo_x,minimo_y],[imagenes[l]]
            columna.append(coordenadas_minimas)
    columna=sorted(columna,key=lambda x:x[0][1])
    definitivo=[]
    first=0
    last=4
    while last <97:
        linea=sorted(columna[first:last],key=lambda x:x[0][0])
        for digito in linea:
            definitivo.append(digito)
        first +=4
        last +=4
    for elemento in definitivo:
        x,y,w,h=cv2.boundingRect(elemento[1][0])
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)
        ROI=original[y:y+h,x:x+w]
        cv2.imwrite('ROI_{}.png'.format(ROI_number),ROI)
        ROI_number +=1

plt.matshow(image)
plt.show()
