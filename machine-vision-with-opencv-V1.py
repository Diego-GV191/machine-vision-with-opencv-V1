from lib import *

# variables usadar
color1 = color('azul' , 1) # color a detectar
color2 = color('azul', 2)
cam = 0 # camara a usar

# configuracion de conecciones
serial = Conection('com3', baudios=9600)

# Iniciamosla camara
camara = cv2.VideoCapture(cam)

# Cargamos una fuente de texto
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
	ret, img = camara.read()
	imagen = cv2.resize(img, (800, 600))
	if ret:

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
		  	area = cv2.contourArea(c)

		  	if area > 2000:
		  		# calcular el centro a partir del momento
			  	momentos = cv2.moments(c)
			  	cx = int(momentos['m10']/momentos['m00'])
			  	cy = int(momentos['m01']/momentos['m00'])
	 
				#Dibujar el centro
			  	cv2.circle(imagen,(cx, cy), 3, (0,0,255), -1)
	 
				#Escribimos las coordenadas del centro
			  	cv2.putText(imagen,"(x: " + str(cx) + ", y: " + str(cy) + ")",(cx+10,cy+10), font, 0.5,(255,255,255),1)


		  		# dibujamos contornos
			  	Ncontono = cv2.convexHull(c)
			  	cv2.drawContours(imagen, [Ncontono], 0, (255,0,0), 3)

			  	# esperando señal
		  		serial.waitSignal(color1, color2)


	    # pantallas
	    # camara con mascara
	  	#flip2 = cv2.flip(mask, 1)
	  	cv2.imshow('mascara', mask)

	    # camara normal
	  	#flip1 = cv2.flip(imagen, 1)
	  	cv2.imshow('camara', imagen)
	  	#cv2.imshow('camara1', flip1)

	  	if cv2.waitKey(1) & 0xFF == ord('q'): break

camara.release()
cv2.destroyAllWindows()