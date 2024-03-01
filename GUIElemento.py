import pygame
from pygame.locals import *
from escena import *
from gestor_recursos import *
from fase import *
from menu_nivel import *

class GUIElemento:
    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rectangulo = rectangulo
    
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony
    
    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx >= self.rect.left) and (posicionx <= self.rect.right) and (posiciony >= self.rect.top) and (posiciony <= self.rect.bottom):
            return True
        else:
            return False
        
    def dibujar(self):
        raise NotImplemented("Metodo dibujar no implementado.")
    
    def accion(self):
        raise NotImplemented("Metodo accion no implementado.")
