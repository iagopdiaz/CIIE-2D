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
        Boton.__init__(self, pantalla, "menu/boton/jugar.png", (ANCHO_PANTALLA/8, (ALTO_PANTALLA/5) ))
    
    def accion(self):
        self.pantalla.menu.ejecutarJugar()

        
class BotonNivel(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/nivel.png", (ANCHO_PANTALLA/8, (ALTO_PANTALLA/5) + (ALTO_PANTALLA/5)*1))
    
    def accion(self):
        self.pantalla.menu.ejecutarNivel()
        

class BotonAjuste(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/ajustes.png", (ANCHO_PANTALLA/8, (ALTO_PANTALLA/5) + (ALTO_PANTALLA/5)*2))
    
    def accion(self):
        self.pantalla.menu.ejecutarAjustes()
        
class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/salir.png", (ANCHO_PANTALLA/8, (ALTO_PANTALLA/5) + (ALTO_PANTALLA/5)*3))
    
    def accion(self):
        self.pantalla.menu.ejecutarSalir()

class BotonPantallaCompleta(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/pantalla_completa.png", (ANCHO_PANTALLA/8, (ALTO_PANTALLA/5)))
    
    def accion(self):
        self.pantalla.menu.ejecutarPantallaCompleta()

class BotonVolumenMusica(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/volumen_musica.png", (ANCHO_PANTALLA/8, (ALTO_PANTALLA/5) + (ALTO_PANTALLA/5)*1))
    
    def accion(self):
        self.pantalla.menu.ejecutarvolumenMusica()        
        
class BotonVolumenEfectos(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/volumen_efectos.png", (ANCHO_PANTALLA/8, (ALTO_PANTALLA/5) + (ALTO_PANTALLA/5)*2))
    
    def accion(self):
        self.pantalla.menu.ejecutarVolumenEfectos()        

class BotonAtras(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, "menu/boton/atras.png", (ANCHO_PANTALLA/8, (ALTO_PANTALLA/5) + (ALTO_PANTALLA/5)*3))
    
    def accion(self):
        self.pantalla.menu.ejecutarAtras()


