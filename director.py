import pygame, sys
from escena import *
from pygame.locals import *
 

class Director:
    """Representa el objeto principal del juego.
    
    En lugar de gestionar en nuestro archivo main el bucle del 
    juego lo que vamos a hacer es crear un clase director que 
    será la encargada de gestionar nuestro bucle de juego, este 
    bucle recibirá una escena cualquiera y se encargará de 
    ejecutar sus métodos de actualizar, eventos y dibujar  
 
    Tiene que utilizar este objeto en conjunto con objetos
    derivados de Scene.  
    
    """
 
    def __init__(self):
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("El Laberinto de las Armonías")
        self.pila = []
        self.salir_escena = False
        self.reloj = pygame.time.Clock()
 
    def loop(self, escena):
        "Pone en funcionamiento el juego."
 
        self.salir_escena = False
        #Eliminamos todos los eventos producidos antes de entrar en el bucle
        while not self.salir_escena:
            #Sincronizar el juego a 60 fps
            tiempo_pasado = self.reloj.tick(60)
            #Pasamos los eventos a la escena
            escena.eventos(pygame.event.get())
            #Actualiza la escena 
            escena.update(tiempo_pasado)
            #Se dibuja en pantalla
            escena.dibujar(self.screen)
            pygame.display.flip()
 
    def ejecutar(self):
        #Mientras haya escenas en la pila, ejecutamos la de arriba
        while (len(self.pila) > 0):
            #Se coge la escena a ejecutar como la que este en la cima de la pila
            escena = self.pila[len(self.pila) - 1]
            #Ejecutamos el bucle de eventos hasta que termine la escena
            self.loop(escena)

    def salirEscena(self):
        #Indicamos en el flag que se quiere salir de la escena
        self.salir_escena = True
        #Eliminamos la escena actual de la pila
        if (len(self.pila) > 0):
            self.pila.pop()
        
    def salirPrograma(self):
        #Vaciamos la lista de escenas pendientes
        self.pila = []
        self.salir_escena = True

    def cambiarEscena(self, escena):
        self.salirEscena()
        #Ponemos la escena en la cima de la pila eliminando la anterior
        self.pila.append(escena)

    def apilarEscena(self, escena):
        self.salir_escena = True
        #Ponemos la escena en la cima de la pila sin eliminar la anterior
        self.pila.append(escena)

