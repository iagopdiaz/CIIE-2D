import pygame
from Ajustes.settings import *
from Personajes.misprite import MiSprite

class Penumbra(MiSprite):
    def __init__(self):
        MiSprite.__init__(self)
        self.image = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Llenamos la penumbra con negro transparente
        self.rect = self.image.get_rect()

    def update(self, jugador, nivel):
        #Establecemos los valores 
        (radio_luz, valor_max, valor_min) = (40, 200, 0) if jugador.id == 2 else (23, 240, 90)

        # Llenamos la penumbra con negro en general la escena
        self.image.fill((0, 0, 0, valor_max)) 

        # Bucle para hacer el difuminado
        for i in range(valor_max, valor_min, -10):
            # Calculamos el radio del círculo actual
            radio_actual = radio_luz + (radio_luz * i / valor_max)

            # Dibujamos un círculo con el color y alpha actuales en la posición del jugador
            pygame.draw.circle(self.image, (0, 0, 0, i), (jugador.rect.centerx, jugador.rect.centery), int(radio_actual))

    def dibujar(self, pantalla):
        pantalla.blit(self.image, (0, 0))  # Dibujamos la penumbra en la pantalla
