import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

#-----------Lectura de imagen previamente mejorada en Paint (mejorado.png), copia y transformación a escala de grises

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

#-----------'limites' es una lista que marca minimo y maximo en el eje x de las columnas con datos. Por lo tanto, cada 'lim' del primer bucle 
#------------representa una columna de las 15 que hay. Imaginá que el bucle empieza con la primera columna (0,60):

ROI_number=0
limites=[(0,60),(60,135),(135,210),(210,285),(285,360),(360,435),(435,505),(505,580),(580,650),(650,725),(725,795),(795,870),(870,940),(940,1010),(1010,1074)]
for lim in limites:
    columna=[]
#----------El siguiente bucle, lo que hace es asociar cada imagen de 'imagenes' con su coordenada más al noroeste (valor más bajo del eje x y del eje y), de modo que
#----------cada imagen queda asociada a 1 coordenada. Cada coordenada y su imagen, es guardada en la lista 'columna'
    for l,c in zip(range(len(imagenes)),imagenes):
        ejex=[imagenes[l][i][0][0] for i in range(len(c))]
        minimo_x=min(ejex)
        ejey=[imagenes[l][i][0][1] for i in range(len(c))]
        minimo_y=min(ejey)
        if minimo_x>lim[0] and minimo_x<lim[1]:
            coordenadas_minimas=[minimo_x,minimo_y],[imagenes[l]]
            columna.append(coordenadas_minimas)
#--------Ahora, los elementos de la lista 'columna' son ordenados de acuerdo a sus coordenadas en el eje y (de menor a mayor, es decir de arriba hacia abajo)
    columna=sorted(columna,key=lambda x:x[0][1])
#--------Con la lista 'columna' ya ordenada, los elementos son agrupados en grupos de 4, donde cada grupo representa un número completo (ej: 24.5)
    definitivo=[]
    first=0
    last=4
    while last <97:
#---------Ahora dentro de cada grupo, los elementos son ordenados de izquierda a derecha en 'linea' (eje x), y cada elemento del grupo es guardado en la lista 'definitivo'        
        linea=sorted(columna[first:last],key=lambda x:x[0][0])  
        for digito in linea:
            definitivo.append(digito)
        first +=4
        last +=4
#--------Finalmente, cada elemento en la lista 'definitivo' es definido en la imagen de la planilla de acuerdo a sus contornos, la sub-imagen es guardada con el nombre
#--------de 'ROI_number', donde number empieza con 0 y termina en total con 1439 sub-imágenes. Finalmente, el bucle sigue con la segunda columna y asi sucesivamente.
    for elemento in definitivo:
        x,y,w,h=cv2.boundingRect(elemento[1][0])
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)
        ROI=original[y:y+h,x:x+w]
        cv2.imwrite('ROI_{}.png'.format(ROI_number),ROI)
        ROI_number +=1

plt.matshow(image)
plt.show()
