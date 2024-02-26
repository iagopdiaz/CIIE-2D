import pygame
import sys

# Configuración inicial
pygame.init()
tamaño_pantalla = (800, 600)
pantalla = pygame.display.set_mode(tamaño_pantalla)

# Cargar imágenes
mundo = pygame.image.load('pistaTenis.jpg')
personaje = pygame.image.load('pelota.png')

# Variables globales
tamaño_mundo = mundo.get_size()
posicion_personaje = [0, 0]
proporcion_vista = 1/4  # Controla la porción del mundo a ver
velocidad = 0.5  # Velocidad de movimiento del personaje
def actualizar_vista():
    # Calcula la posición de la vista basada en la posición del personaje
    posicion_vista = [posicion_personaje[0] - tamaño_pantalla[0] * proporcion_vista / 2, posicion_personaje[1] - tamaño_pantalla[1] * proporcion_vista / 2]

    # Asegura que la vista no salga de los límites del mundo
    posicion_vista[0] = max(0, min(posicion_vista[0], tamaño_mundo[0] - tamaño_pantalla[0] * proporcion_vista))
    posicion_vista[1] = max(0, min(posicion_vista[1], tamaño_mundo[1] - tamaño_pantalla[1] * proporcion_vista))

    return pygame.Rect(posicion_vista, (tamaño_pantalla[0] * proporcion_vista, tamaño_pantalla[1] * proporcion_vista))

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Control del personaje con las teclas 'ASDW'
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        posicion_personaje[0] -= velocidad
    if teclas[pygame.K_d]:
        posicion_personaje[0] += velocidad
    if teclas[pygame.K_w]:
        posicion_personaje[1] -= velocidad
    if teclas[pygame.K_s]:
        posicion_personaje[1] += velocidad

    # Asegura que el personaje no salga de los límites del mundo
    posicion_personaje[0] = max(personaje.get_width() * proporcion_vista / 2, min(posicion_personaje[0], tamaño_mundo[0] - personaje.get_width() * proporcion_vista / 2))
    posicion_personaje[1] = max(personaje.get_height() * proporcion_vista / 2, min(posicion_personaje[1], tamaño_mundo[1] - personaje.get_height() * proporcion_vista / 2))

    # Actualiza la vista y dibuja el mundo y el personaje
    rect_vista = actualizar_vista()
    pantalla.blit(pygame.transform.scale(mundo.subsurface(rect_vista), tamaño_pantalla), (0, 0))

    # Calcula la posición en la pantalla donde debemos dibujar al personaje
    posicion_personaje_pantalla = [(posicion_personaje[i] - rect_vista.topleft[i]) / proporcion_vista for i in range(2)]
    pantalla.blit(personaje, (posicion_personaje_pantalla[0] - personaje.get_width()/2, posicion_personaje_pantalla[1] - personaje.get_height()/2))

    pygame.display.flip()
