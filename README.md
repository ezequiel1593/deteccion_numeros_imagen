# Deteccion_numeros_imagen

  En el siguiente escrito voy a redactar los pasos finales (en el 'prueba y error' los intentos fueron mucho más numerosos) a traves de los cuales pude detectar números en una planilla escaneada, predecir sus valores, y volcar estas predicciones en un bloc de notas, a modo de "digitalización" de la planilla. Pretendo formar y compartir una guía, ya que el material que he podido encontrar al respecto en la web no ha sido abundante (para pasos específicos si he podido encontrar ayuda en Internet, pero no para toda la tarea en su conjunto). La siguiente forma de resolver este problema no es eficiente, ya que digitalizar la planilla a mano me hubiese consumido muchísimo menos tiempo, no obstante me sirve como práctica en la programación en un proyecto enteramente personal. Sin embargo, si no hubiese tenido problemas con la despixelación de la imagen (estaré eternamente agradecido con quien pueda brindarme una ayuda al respecto), no me cabe la menor duda de que este método si sería eficiente en posteriores muestras, asumiendo que éstas cuentan exactamente con el mismo formato (debo mencionar que el código empleado aquí, no me serviría por ejemplo en caso de que hayan números de 1 cifra o números negativos).</br>
  Para llevar a cabo la tarea, utilicé:</br>
<ul>
  <li>Python 3.8.3</li>
  <li>Matplotlib 3.2.1</li>
  <li>Numpy 1.18.3</li>
  <li>Opencv-python 4.2.0.34</li>
  <li>Pandas 1.0.3</li>
  <li>Pillow 7.1.2</li>
  <li>Scikit-learn 0.23.1</li>
</ul>

<h2>1. Pre-procesamiento de la imagen. Archivo 'contornos.py'.</h2>
  Sin lugar a dudas, las mayores dificultades que encontré no fueron en relación al código,sino en relación a la imagen. Esta es la planilla en cuestión:
  
  <img src=https://github.com/ezequiel1593/deteccion_numeros_imagen/blob/master/e06.png>
  
  Para detectar correctamente los contornos de la imagen, tenía como logro intermedio hacer que el fondo sea lo más blanco posible, en tanto que los dígitos sean lo más negros que puedan ser. Con Photopea.com, modificando la exposición y otros atributos de la imagen, pude lograr algo similar.</br> 
  <b>Mención especial: Previamente a cualquier otra modificación de la imagen, lo que hice fue imprimir los contornos en la imagen (cv2.findContours), recortar y guardar las sub-imagenes (cv2.imwrite). Las sub-imágenes en donde se reconocían a simple vista números o puntos sin lugar a dudas, fueron guardadas en una carpeta aparte, y sirvieron para formar la base de datos que alimenta la red neuronal construida más adelante. En total fueron almacenados 10 recortes de cada número del 0 al 9, y del punto decimal (en total 110 muestras). </b></br> 
  Pero surgía otro problema, y era que varios dígitos se partían en 2 o 3 "pedazos" (o quizás estas particiones ya venían desde antes). Como resultado, se reconocían más de 2400 contornos, cuando en verdad deberían reconocerse 1440. Lo siguiente fue ir imprimiendo la imagen con los contornos (rectángulos rojos) y continuamente corregir los dígitos que aparecían partidos con Paint. En este paso, también eliminé las extensas barras que aparecen en la imagen, además de píxeles que formaban 'bolas' que eran reconocidas en los contornos pero que no constituían un dígito en sí.</br>
  
  Imagen final, mejorada:
  <img src=https://github.com/ezequiel1593/deteccion_numeros_imagen/blob/master/mejorado.png>
  
  Una vez abordado el tema de la imagen, podemos echarle una vista al primer código (contornos.py), que tiene como fin último recortar las sub-imagenes que contienen los números y puntos decimales, en el orden requerido.</br>
  ¿Cual era el orden requerido? El recorte de las sub-imágenes debía ser por columna, empezando con la primera. Dentro de cada columna, los recortes debían ser por fila, empezando por la primera. A su vez, en cada fila, los recortes debían ser de izquierda a derecha. Observando la imagen, los primeros recortes debían ser del número '25.2' (primera fila, primera columna), el primer dígito recortado tenía que ser el '2', luego el '5', luego el '.', y finalmente el '2'. Y así sucesivamente.</br>
  Afortunadamente, pude abordar esta tarea con éxito: https://github.com/ezequiel1593/deteccion_numeros_imagen/blob/master/contornos.py.</br>
  
  <h2>2. Alimentación de la red neuronal.</h2>
  
  El la sección anterior, mencioné en negrita que luego de una primera modificación de la imagen, lo que hice fue recortar las sub-imagenes que formaban los contornos, y guardé en una carpeta aparte los números y puntos que se reconocian a simple vista. En total fueron apartadas 110 sub-imágenes, 10 muestras para cada número del 0 al 9, y 10 muestras para el punto decimal. Estas sub-imagenes fueron redimensionadas a 16x16, es decir cada sub-imagen cuenta con 256 píxeles. Cada uno de los píxeles adopta un valor del 0 al 255 (del negro al blanco). El valor de cada uno de estos píxeles fue guardado en un archivo Excel, uno por columna. 
