import pygame
from pygame.locals import *
from escena import *
from gestor_recursos import *
from gestor_sonido import GestorSonido
from fase import *
from GUIElemento import *
from botones import *


class GUIInicial(GUI):
    def __init__(self, menu):
        GUI.__init__(self, menu, "menu/wallpaper.jpg")
        botonPantallaCompleta = BotonPantallaCompleta(self)
        botonAtras = BotonAtras(self)
        self.GUIelementos.append(botonPantallaCompleta)
        self.GUIelementos.append(botonAtras)


class MenuAjustes(Escena):
    
    def __init__(self, director):
        #Llamamos al constructor de la clase padre
        Escena.__init__(self, director)
        #Creamos la lista de pantallas
        self.listaPantallas = []
        #Creamos las pantallas que vamos a tener
        #y las metemos en la lista
        self.listaPantallas.append(GUIInicial(self))

        #En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

    def update(self, *args):
        return

    def eventos(self, lista_eventos):
        #Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            #Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.ejecutarAtras()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()
        #Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)
    
    def ejecutarSalir(self):
        self.director.salirPrograma()

    def ejecutarPantallaCompleta(self):
        self.director.pantallaCompleta()

    
    def ejecutarAtras(self):
        self.director.salirEscena()
    
    def mostrarPantallaInicial(self):
        self.pantallaActual = 0
        
    def encender_musica(self):
        GestorSonido.musica_nivel_1()    

