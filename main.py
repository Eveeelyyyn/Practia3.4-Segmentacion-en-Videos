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

    # 3. Realizar la sustracción de imágenes
    diferencia = cv2.absdiff(imagen_referencia_gris, frame_actual_gris)

    # 4. Umbralizar
    umbralizado = umbral.threshold(diferencia, 5)

    # 5. Filtrar ruido
    kernel = np.ones((8,8), np.uint8)
    filtrado = cv2.morphologyEx(umbralizado, cv2.MORPH_OPEN, kernel)

    # 6. Extraer objetos y fondo
    objetos = cv2.bitwise_and(frame_actual, frame_actual, mask=filtrado)
    fondo = cv2.bitwise_and(frame_actual, frame_actual, mask=cv2.bitwise_not(filtrado))

    # Mostrar el resultado
    cv2.imshow('Diferencia', filtrado)
    cv2.imshow('Objetos en Movimiento', objetos)
    cv2.imshow('Fondo Estático', fondo)
    
    # Actualizar las imágenes acumulativas
    cv2.accumulateWeighted(frame_actual, fondo_acumulado, 0.01, mask=cv2.bitwise_not(filtrado))
    cv2.accumulateWeighted(frame_actual, objetos_acumulados, 0.01, mask=filtrado)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos de video
video.release()

# Convertir las imágenes acumulativas a uint8 para visualización
fondo_resultante = cv2.convertScaleAbs(fondo_acumulado)
objetos_resultantes = cv2.convertScaleAbs(objetos_acumulados)

# Mostrar o guardar las imágenes resultantes
cv2.imshow('Fondo resultante', fondo_resultante)
cv2.imshow('Objetos resultantes', objetos_resultantes)
cv2.waitKey(0)

# Cerrar todas las ventanas abiertas por OpenCV
cv2.destroyAllWindows()

