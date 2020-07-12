import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from PIL import Image
import cv2
import matplotlib.pyplot as plt

#----------El modelo es entrenado. 'target' es el número o punto y 'X' son los píxeles que representan cada número o punto.

data=pd.read_csv('C:\\Users\\Ezequiel\\Desktop\\proyecto\\data_red_1616.txt',delimiter='\t')
target=data['Numero'].values
X=data.loc[:, data.columns != 'Numero'].values

mlp=MLPClassifier(max_iter=1000) #Con train_train_split, el Score es de 1.0. No obstante el modelo no es perfecto.
mlp.fit(X,target)

#------Predicciones. En el primer bucle se representan cada una de las columnas. La primera vez se predicen las sub-imágenes de la primera columna, que fueron enumeradas
#------desde el 0 al 95.
ROI=0
for columna in range(0,15):
    primero=0
    ultimo=4
    while ultimo <97:
        linea=[]
#------Se comienza con las predicciones de las primeras 4 sub-imágenes. Cada predicción es guardada como un string en la lista 'linea'.
        for numero in range(primero,ultimo):
            nombre='C:\\Users\\Ezequiel\\Desktop\\proyecto\\pik\\ROI_{}.png'.format(ROI)
            img=Image.open(nombre)
#------Para cada predicción, cada sub-imagen es redimensionada a una imagen 16x16. El valor de cada pixel es extraido y guardado en la lista 'pixels'.
            img=img.resize((16,16))
            array_0=np.array(img)
            pixels=[]
            for i in range(0,16):
                for k in range(0,16):
                    pixels.append(array_0[i][k][0])
            objeto=[pixels]
            prediccion=str((mlp.predict(objeto)[0]))
            linea.append(prediccion)
            ROI +=1
#-----El bloc de notas es creado/abierto. Los strings de la lista 'linea' se unen, formando un número completo (ej: 24.5). Cada uno de estos números completos son
#-----escritos en el archivo, uno por línea.
        file=open('predicciones.txt','a')
        unido=''.join(linea)
        file.write(unido)
        file.write('\n')
        file.close()
        primero +=4
        ultimo +=4
