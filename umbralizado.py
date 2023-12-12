import numpy as np
def threshold(imagen, umbral):
    """ Umbraliza una imagen en escala de grises de manera manual. """
    # Inicializar una imagen binaria con ceros (imagen en negro)
    imagen_umbralizada = np.zeros_like(imagen, dtype=np.uint8)

    # Asignar 255 a los píxeles donde el valor es mayor que el umbral
    imagen_umbralizada[imagen > umbral] = 255

    return imagen_umbralizada


