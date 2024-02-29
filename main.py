import pygame, sys, os
from pygame.locals import *
from gestor_recursos import *
from jugador import *
from fase import *
from settings import *

def main():

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), 0, 32)
    colorFondo = (255, 255, 255)  # Color fondo
    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()
    fase = Fase()
    fase.start_pos = None  # Posición inicial del rectángulo
    fase.end_pos = None    # Posición final del rectángulo

    while True:

        # Sincronizar el juego a 60 fps
        tiempo_pasado = reloj.tick(60)
        pantalla.fill(colorFondo)
        # Coge la lista de eventos y se la pasa a la escena
        # Devuelve si se debe parar o no el juego
        if (fase.eventos(pygame.event.get())):
            pygame.quit()
            sys.exit()
        # Actualiza la escena
        # Devuelve si se debe parar o no el juego
        if (fase.update(tiempo_pasado)):
            pygame.quit()
            sys.exit()

        # Se dibuja en pantalla
        fase.dibujar(pantalla)
        pygame.display.flip()



if __name__ == "__main__":
    main()
