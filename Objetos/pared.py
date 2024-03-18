import pygame
from pygame.locals import *
from Personajes.misprite import *

class Pared(MiSprite):
    def __init__(self,rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.top))
        # En el caso particular de este juego, las paredes no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))

    def update(self, scrollx, scrolly):
        # Asegúrate de que scrollx no sea menor que 0 ni mayor que la anchura de la imagen menos la anchura de la pantalla
        self.rectSubimagen.left = max(0, min(scrollx, self.imagen.get_width() - ANCHO_PANTALLA))
        # Asegúrate de que scrolly no sea menor que 0 ni mayor que la altura de la imagen menos la altura de la pantalla
        self.rectSubimagen.top = max(0, min(scrolly, self.imagen.get_height() - ALTO_PANTALLA))

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

class ParedPinchos(MiSprite):
    def __init__(self, orientacion):
        MiSprite.__init__(self)
        # Se carga la hoja
        self.image = GestorRecursos.CargarImagenPinchos(orientacion, -1)
        self.rect = self.image.get_rect()
        
        self.damage = 1


