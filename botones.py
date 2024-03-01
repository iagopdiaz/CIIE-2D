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
        self.imagen = pygame.transform.scale(self.imagen, (160, 32))
        self.rect = self.imagen.get_rect()

        #Se llama al metodo de la clase padre con el rectangulo que ocupa el boton
        GUIElemento.__init__(self, pantalla, self.rect)
        #Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class BotonJugar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/jugar.png", (100, 150))
    
    def accion(self):
        self.pantalla.menu.ejecutarJugar()


class BotonAjuste(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/nivel.png", (300, 300))
    
    def accion(self):
        self.pantalla.menu.ejecutarAjustes()
        
class BotonNivel(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/nivel.png", (100, 300))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel()
        
class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/salir.png", (100, 450))
    
    def accion(self):
        self.pantalla.menu.ejecutarSalir()

class BotonPantallaCompleta(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/salir.png", (100, 150))
    
    def accion(self):
        self.pantalla.menu.ejecutarPantallaCompleta()

class BotonAtras(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/atras.png", (100, 480))
    
    def accion(self):
        self.pantalla.menu.ejecutarAtras()

