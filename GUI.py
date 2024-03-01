import pygame
from pygame.locals import *
from escena import *
from gestor_recursos import *
from fase import *
from menu_nivel import *
from GUIElemento import *
from botones import *

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
            
            

class GUIInicial(GUI):
    def __init__(self, menu):
        GUI.__init__(self, menu, "menu/wallpaper.jpg")
        botonFase1 = BotonNivel1(self)
        botonFase2 = BotonNivel2(self)
        botonFase3 = BotonNivel3(self)
        botonAtras = BotonAtras(self)
        self.GUIelementos.append(botonFase1)
        self.GUIelementos.append(botonFase2)
        self.GUIelementos.append(botonFase3)
        self.GUIelementos.append(botonAtras)
