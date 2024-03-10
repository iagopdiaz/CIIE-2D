import pygame, sys, os
from pygame.locals import *
from gestor_recursos import *
from settings import *
from misprite import *
from personaje import *
#from observable import Observable

class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadX, velocidadY, retardoAnimacion, idJugador):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadX, velocidadY, retardoAnimacion, idJugador)
        self.inventario = None
        self.soltando = False
        
    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if teclasPulsadas[arriba]:
            Personaje.mover(self,ARRIBA)
        elif teclasPulsadas[izquierda]:
            Personaje.mover(self,IZQUIERDA)
        elif teclasPulsadas[derecha]:
            Personaje.mover(self,DERECHA)
        elif teclasPulsadas[abajo]:
            Personaje.mover(self,ABAJO)            
        else:
            Personaje.mover(self,QUIETO)

class PrimerPersonaje(Jugador):#and Observable
    "Personaje Bartender"
    def __init__(self):#and Observers
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Jugador.__init__(self,'Alchemist.png','coordJugador1.txt', [4, 4, 4, 4, 4, 4, 4, 4], VELOCIDAD_JUGADORX, VELOCIDAD_JUGADORY, RETARDO_ANIMACION_JUGADOR, 0)
        ##Observable.__init__(self, observers)
        

class SegundoPersonaje(Jugador):#and Observable
    "Personaje Bartender"
    def __init__(self):#and Observers
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Jugador.__init__(self,'Bartender.png','coordJugador2.txt', [4, 4, 4, 4, 4, 4, 4, 4], VELOCIDAD_JUGADORX, VELOCIDAD_JUGADORY, RETARDO_ANIMACION_JUGADOR, 1)
        #Observable.__init__(self, observers)

class TercerPersonaje(Jugador):#and Observable
    "Personaje Merchant"
    def __init__(self):#and Observers
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Jugador.__init__(self,'Merchant.png','coordJugador3.txt', [4, 4, 4, 4, 4, 4, 4, 4], VELOCIDAD_JUGADORX, VELOCIDAD_JUGADORY, RETARDO_ANIMACION_JUGADOR, 2)
        #Observable.__init__(self, observers)
