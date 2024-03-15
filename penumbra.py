import pygame
from settings import *

class Penumbra:
    def __init__(self):
        self.penumbra = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        self.penumbra.fill((0, 0, 0, 0))  # Llenamos la penumbra con negro transparente

    def update(self, jugador, nivel):
        if nivel == 3:
            #Establecemos los valores 
            (radio_luz, valor_max, valor_min) = (40, 200, 0) if jugador.id == 2 else (23, 240, 90)

            # Llenamos la penumbra con negro en general la escena
            self.penumbra.fill((0, 0, 0, valor_max)) 

            # Bucle para hacer el difuminado
            for i in range(valor_max, valor_min, -10):
                # Calculamos el radio del círculo actual
                radio_actual = radio_luz + (radio_luz * i / valor_max)

                # Dibujamos un círculo con el color y alpha actuales en la posición del jugador
                pygame.draw.circle(self.penumbra, (0, 0, 0, i), (jugador.rect.centerx, jugador.rect.centery), int(radio_actual))

              
        else:
            self.penumbra.fill((0,0,0,0))

    def dibujar(self, pantalla):
        pantalla.blit(self.penumbra, (0, 0))  # Dibujamos la penumbra en la pantalla
