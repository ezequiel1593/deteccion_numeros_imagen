# Deteccion_numeros_imagen
Deteccion de números de una planilla escaneada. Vuelco de resultados a un bloc de notas.

  En el siguiente escrito voy a redactar los pasos a traves de los cuales pude detectar números en una planilla escaneada, predecir sus valores, y volcar estas predicciones en un bloc de notas, a modo de "digitalización" de la planilla. Pretendo formar y compartir una guía, ya que el material que he podido encontrar al respecto en la web no ha sido abundante (para pasos específicos si he podido encontrar ayuda en Internet, pero no para toda la tarea en su conjunto).
Para llevar a cabo la tarea, utilicé:
<ul>
  <li>Python 3.8.3</li>
  <li>Matplotlib 3.2.1</li>
  <li>Numpy 1.18.3</li>
  <li>Opencv-python 4.2.0.34</li>
  <li>Pandas 1.0.3</li>
  <li>Pillow 7.1.2</li>
  <li>Scikit-learn 0.23.1</li>
</ul>

<h2>1. Pre-procesamiento de la imagen. (Archivo 'contornos.py')</h2>
  Sin lugar a dudas, las mayores dificultades que encontré no fueron en relación al código,sino en relación a la imagen. Esta es la planilla en cuestión:

  Para detectar correctamente los contornos de la imagen, tenía como logro intermedio hacer que el fondo sea lo más blanco posible, en tanto que los dígitos sean lo más negros que puedan ser. Con Photopea.com, modificando la exposición, pude lograr algo similar, pero surgía otro problema, y era que varios dígitos se partían en 2 o 3 "pedazos" (o quizás estas particiones ya venían desde antes). Como resultado, se reconocían más de 2400 contornos, cuando en verdad deberían reconocerse 1440, por lo que tuve que agregar píxeles con Paint, para unir estos pedazos, y formar los dígitos de forma correcta. En este paso, también eliminé las extensas barras que aparecen en la imagen, además de píxeles que formaban 'bolas' pero que no constituían un dígito en sí.
<pre>
<code>
import cv2 
import matplotlib.pyplot as plt 
import numpy as np 
from PIL import Image 

image= cv2.imread('C:\\Users\\Ezequiel\\Desktop\\proyecto\\planillas_y_resultados\\mejorado.png')
original=image.copy()
gray=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
threshold_aplicado,thresholded_image=cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

ROI_number=0
cnts=cv2.findContours(thresholded_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=cnts[0] if len(cnts) == 2 else cnts[1] #(findContours devuelve contours y hierarchy)
</code>
</pre>
