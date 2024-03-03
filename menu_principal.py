import pygame
from pygame.locals import *
from escena import *
from gestor_recursos import *
from gestor_sonido import GestorSonido
from fase import *
from menu_nivel import *
from menu_settings import * 
from GUIElemento import *
from botones import *


class GUIInicial(GUI):
    def __init__(self, menu):
        GUI.__init__(self, menu, "menu/wallpaper.jpg")
        botonJugar = BotonJugar(self)
        botonNivel = BotonNivel(self)
        botonAjustes = BotonAjuste(self)
        botonSalir = BotonSalir(self)
        self.GUIelementos.append(botonJugar)
        self.GUIelementos.append(botonNivel)
        self.GUIelementos.append(botonAjustes)
        self.GUIelementos.append(botonSalir)
      

class Menu(Escena):
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
                    self.ejecutarSalir()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()
        #Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    def ejecutarJugar(self):
        fase = Fase(self.director)
        self.director.apilarEscena(fase)
        
    def ejecutarAjustes(self):
        ajustes = MenuAjustes(self.director)
        self.director.apilarEscena(ajustes)
        
    def ejecutarNivel(self):
        menuSelect = MenuNivel(self.director)
        self.director.apilarEscena(menuSelect)

    def ejecutarSalir(self):
        self.director.salirPrograma()

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0
    
    def encender_musica(self):
        GestorSonido.musica_menus()      