import pygame
from pygame.locals import *
from escena import *
from gestor_recursos import *
from fase import *
from menu_nivel import *
from GUIElemento import GUIElemento


class Boton(GUIElemento):
    def __init__(self, pantalla, nombreImagen, posicion):
        #Se carga la imagen del boton
        self.imagen = GestorRecursos.CargarImagen(nombreImagen, -1)
        self.rect = self.imagen.get_rect()

        #Se llama al metodo de la clase padre con el rectangulo que ocupa el boton
        GUIElemento.__init__(self, pantalla, self.rect)
        #Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class BotonJugar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_JUGAR, (100, 120))
    
    def accion(self):
        self.pantalla.menu.ejecutarJugar()


class BotonNivel(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_NIVEL, (100, 240))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel()


class BotonAjuste(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_AJUSTES, (100, 360))
    
    def accion(self):
        self.pantalla.menu.ejecutarAjustes()


class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_SALIR, (100, 480))
    
    def accion(self):
        self.pantalla.menu.ejecutarSalir()


class BotonPantallaCompleta(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_PANTALLA_COMPLETA, (100, 360))
    
    def accion(self):
        self.pantalla.menu.ejecutarPantallaCompleta()


class BotonAtras(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_ATRAS, (100, 480))
    
    def accion(self):
        self.pantalla.menu.ejecutarAtras()
        
class BotonBajarMusica(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_JUGAR , (100, 120))
    
    def accion(self):
        self.pantalla.menu.ejecutarBajarVolumenMusica()       
        
        
class BotonSubirMusica(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_JUGAR, (350, 120))
    
    def accion(self):
        self.pantalla.menu.ejecutarSubirVolumenMusica()

class BotonBajarSonido(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_JUGAR, (100, 240))
    
    def accion(self):
        self.pantalla.menu.ejecutarBajarVolumenSonido()
                       
class BotonSubirSonido(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, BOTON_JUGAR, (350, 240))
    
    def accion(self):
        self.pantalla.menu.ejecutarSubirVolumenSonido()        
