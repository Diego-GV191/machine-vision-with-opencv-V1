# librerias
import cv2
import numpy as np
import serial
import time

# funcion para determinar colores
def color(color, status, rojo=None):
  # Rojo
  if color == 'rojo' and status == 1 and rojo == 1:
    rojoBajo1 = np.array([0, 100, 20], np.uint8)
    return rojoBajo1
  else: error = True
  if color == 'rojo' and status == 1 and rojo == 2:
    rojoAlto1 = np.array([10, 255, 255], np.uint8)
    return rojoAlto1
  else: error = True

  if color == 'rojo' and status == 2 and rojo == 1:
    rojoBajo2 = np.array([175, 100, 20], np.uint8)
    return rojoBajo2
  else: error = True
  if color == 'rojo' and status == 2 and rojo == 2:
    rojoAlto2 = np.array([180, 255, 255], np.uint8)
    return rojoAlto2
  else: error = True

  # Naranja
  if color == 'naranja' and status == 1:
    naranjaBajo = np.array([11, 100, 20], np.uint8)
    return naranjaBajo
  else: error = True
  if color == 'naranja' and status == 2:
    naranjaAlto = np.array([19, 255, 255], np.uint8)
    return naranjaAlto
  else: error = True

  # Amarillo
  if color == 'amarillo' and status == 1:
    amarilloBajo = np.array([20, 100, 20], np.uint8)
    return amarilloBajo
  else: error = True
  if color == 'amarillo' and status == 2:
    amarilloAlto = np.array([32, 255, 255], np.uint8)
    return amarilloAlto
  else: error = True

  # Verde
  if color == 'verde' and status == 1:
    verdeBajo = np.array([36, 100, 20], np.uint8)
    return verdeBajo
  else: error = True
  if color == 'verde' and status == 2:
    verdeAlto = np.array([70, 255, 255], np.uint8)
    return verdeAlto
  else: error = True

  # Violeta
  if color == 'violeta' and status == 1:
    violetaBajo = np.array([130, 100, 20], np.uint8)
    return violetaBajo
  else: error = True
  if color == 'violeta' and status == 2:
    violetaAlto = np.array([145, 255, 255], np.uint8)
    return violetaAlto
  else: error = True

  # Rosa
  if color == 'rosa' and status == 1:
    rosaBajo = np.array([146, 100, 20], np.uint8)
    return rosaBajo
  else: error = True
  if color == 'rosa' and status == 2:
    rosaAlto = np.array([170, 255, 255], np.uint8)
    return rosaAlto
  else: error = True

  # Azul
  if color == 'azul' and status == 1:
    azulBajo = np.array([100,100,20], np.uint8)
    return azulBajo
  else: error = True
  if color == 'azul' and status == 2:
    azulAlto = np.array([120,255,255], np.uint8)
    return azulAlto
  else: error = True

  if error == True:
    print('Error: el color no existe')

# clase conexion
'''
  Es necesario modificar esta clase
  dependiendo el uso que se le vaya a dar
'''
class Conection:
  # se debe especificar puerto y baudios
  def __init__(self, puerto='COM3', baudios = 9600):
    self.puerto = puerto
    self.baud = baudios

    # trata de crear la conexion
    try:
      dev = serial.Serial(self.puerto.upper(), self.baud)
      time.sleep(2)
      self.errorConection = False
    except:
      self.errorConection = True
      print('Imposible conectar')

  # mandar mensajes por serial
  def send_message(self, mensaje):
    if self.errorConection == False:
      print(mensaje)
      dev.write(mensaje)
      print('Mensaje enviado')
    else:
      print('No se mando mensaje')

  # detecta el objeto mediante la señal madada desde el controlador
  def waitSignal(self, color1, color2, cam = 0):
    if self.errorConection == False:
      while True:
        try:
          valor = dev.readline()
          valor.decode('ascii')
        except:
          print('Sin señal')

        # despues de recibir la señal va a colocar las coordenadas
        # en una tupla y se mandara con la funcion send_message()
        if valor == 'detected object':
          time.sleep(5)
          # variable de coordenadas
          XY=[]
          # capturamos la camara
          camra = cv2.VideoCapture(cam)
          ret, img = camara.read()
          imagen = cv2.resize(img, (800, 600))
          # acomodamos la imagen para detectar los colores
          frameHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
          mask = cv2.inRange(frameHSV, color1, color2)
          #Eliminamos ruido
          kernel = np.ones((3,3),np.uint8)
          mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
          mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
          # buscamos contornos
          contornos, hierachy  = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

          for c in contornos:
            # calcular el centro a partir del momento
            momentos = cv2.moments(c)
            cx = int(momentos['m10']/momentos['m00'])
            cy = int(momentos['m01']/momentos['m00'])
            data = cx + ', ' + cy
            XY.append(data)
     
          # Escribimos las coordenadas del centro
          send_message(XY)

          # aqui solo revisara si se termino
          # el proceso de quitar los objetos
          while True:
            Proceso_terminado = dev.readline()
            Proceso_terminado.decode('ascii')
            if Proceso_terminado == 'Proceso listo':
              time.sleep(1)
              break

      print('Esperando señal\n')
    else:
      print('Sin señal')