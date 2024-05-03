import pygame
import sys
import random  # Importamos la biblioteca random

# Tamaño de la ventana
ANCHO_VENTANA = 300
ALTO_VENTANA = 300

# Tamaño de cada cuadrado
TAMAÑO_CUADRADO = ANCHO_VENTANA // 3

class Cuadrado:
    def __init__(self, imagen, x, y):
        self.imagen = imagen
        self.rect = imagen.get_rect()
        self.rect.topleft = (x, y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect.topleft)

class CuadradoVacio:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TAMAÑO_CUADRADO, TAMAÑO_CUADRADO)

    def obtener_adyacente(self, cuadrados, dx, dy):
        x, y = self.rect.topleft[0] + dx, self.rect.topleft[1] + dy
        for cuadrado in cuadrados:
            if cuadrado.rect.topleft == (x, y):
                return cuadrado
        return None

def dividir_imagen(imagen):
    sub_imagenes = []
    for fila in range(3):
        for columna in range(3):
            sub_imagen = imagen.subsurface(columna * TAMAÑO_CUADRADO, fila * TAMAÑO_CUADRADO, TAMAÑO_CUADRADO, TAMAÑO_CUADRADO)
            sub_imagenes.append(sub_imagen)
    random.shuffle(sub_imagenes)  # Barajamos aleatoriamente las sub-imágenes
    return sub_imagenes

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Imagen dividida")

    # Carga de la imagen
    imagen_original = pygame.image.load("300x300.jpeg")  # Reemplaza "tu_imagen.jpg" con la ruta de tu imagen
    sub_imagenes = dividir_imagen(imagen_original)

    cuadrados = []
    cuadrado_vacio = CuadradoVacio(0, 0)  # Inicializamos cuadrado_vacio

    for i, sub_imagen in enumerate(sub_imagenes):
        fila = i // 3
        columna = i % 3
        if sub_imagen:  # Si hay una sub-imagen
            cuadrado = Cuadrado(sub_imagen, columna * TAMAÑO_CUADRADO, fila * TAMAÑO_CUADRADO)
            cuadrados.append(cuadrado)
            if fila == 2 and columna == 2:  # Si es el último cuadrado
                cuadrado_vacio = CuadradoVacio(columna * TAMAÑO_CUADRADO, fila * TAMAÑO_CUADRADO)

    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    adyacente = cuadrado_vacio.obtener_adyacente(cuadrados, 0, -TAMAÑO_CUADRADO)
                    if adyacente:
                        cuadrado_vacio.rect.move_ip(0, -TAMAÑO_CUADRADO)
                        adyacente.rect.move_ip(0, TAMAÑO_CUADRADO)
                elif evento.key == pygame.K_DOWN:
                    adyacente = cuadrado_vacio.obtener_adyacente(cuadrados, 0, TAMAÑO_CUADRADO)
                    if adyacente:
                        cuadrado_vacio.rect.move_ip(0, TAMAÑO_CUADRADO)
                        adyacente.rect.move_ip(0, -TAMAÑO_CUADRADO)
                elif evento.key == pygame.K_LEFT:
                    adyacente = cuadrado_vacio.obtener_adyacente(cuadrados, -TAMAÑO_CUADRADO, 0)
                    if adyacente:
                        cuadrado_vacio.rect.move_ip(-TAMAÑO_CUADRADO, 0)
                        adyacente.rect.move_ip(TAMAÑO_CUADRADO, 0)
                elif evento.key == pygame.K_RIGHT:
                    adyacente = cuadrado_vacio.obtener_adyacente(cuadrados, TAMAÑO_CUADRADO, 0)
                    if adyacente:
                        cuadrado_vacio.rect.move_ip(TAMAÑO_CUADRADO, 0)
                        adyacente.rect.move_ip(-TAMAÑO_CUADRADO, 0)

        pantalla.fill((255, 255, 255))

        # Dibujar los cuadrados en la pantalla
        for cuadrado in cuadrados:
            if isinstance(cuadrado, Cuadrado):  # Solo dibujamos los cuadrados que son instancias de Cuadrado
                cuadrado.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
