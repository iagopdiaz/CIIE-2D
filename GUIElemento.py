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


class GUI:
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        self.imagen = GestorRecursos.CargarImagen(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.GUIelementos = []

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                self.elementosClic = None
                for elemento in self.GUIelementos:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementosClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.GUIelementos:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementosClic):
                            elemento.accion()

    def dibujar(self, pantalla):
        #Dibujamos imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        #Dibujamos botones
        for elemento in self.GUIelementos:
            elemento.dibujar(pantalla)
            
