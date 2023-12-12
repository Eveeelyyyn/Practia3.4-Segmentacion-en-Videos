import cv2
import numpy as np
import umbralizado as umbral

# 1. Guardar imagen de referencia
video = cv2.VideoCapture('nofi006.mp4')
ret, imagen_referencia = video.read()

# Convertir a escala de grises para simplificar el procesamiento
imagen_referencia_gris = cv2.cvtColor(imagen_referencia, cv2.COLOR_BGR2GRAY)

# Inicializar imagen acumulativa para el fondo
fondo_acumulado = np.float32(imagen_referencia)
objetos_acumulados = np.zeros_like(imagen_referencia, dtype=np.float32)

# 2. Capturar imagen actual y realizar el resto de los pasos en un bucle
while True:
    ret, frame_actual = video.read()
    if not ret:
        break

    # Convertir frame actual a escala de grises
    frame_actual_gris = cv2.cvtColor(frame_actual, cv2.COLOR_BGR2GRAY)